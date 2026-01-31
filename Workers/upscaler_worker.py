import os

from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QMessageBox

from Core import log_manager
from Tools.MediaProcessing import ComfyUpscaler
from Tools.Utils import utils

logger = log_manager.get_logger(__name__)


class UpscalerWorker(QThread):
    progress_updated = Signal(int)
    image_list_got = Signal(list)
    worker_finished = Signal(tuple)

    def __init__(
            self,
            model_name: str,
            img_dir: str,
            recursive_search: bool,
            width_threshold: int,
            height_threshold: int,
            jpg_size_threshold: int,
            post_downscale_scale: float,
            url: str,
            get_interval: float,
            image_list: list,
            mode: str = "upscale"
    ):
        """
        初始化放大器
        """
        super().__init__()
        self.model_name = model_name
        self.img_dir = img_dir
        self.recursive_search = recursive_search
        self.width_threshold = width_threshold
        self.height_threshold = height_threshold
        self.jpg_size_threshold = jpg_size_threshold
        self.post_downscale_scale = post_downscale_scale
        self.api_url = url
        self.get_interval = get_interval
        self.image_list = image_list
        self.upscaler = None
        self.mode = mode
        self._stop = False

    def run(self):
        self._stop = False
        logger.info(f"放大器工作线程启动，模式: {self.mode}")

        # 基础检查
        if not self.img_dir:
            logger.error("输入的路径为空")
            self.worker_finished.emit(("错误", "输入的路径为空", QMessageBox.Icon.Critical))
            return
        elif not os.path.exists(self.img_dir):
            logger.error(f"输入的路径不存在: {self.img_dir}")
            self.worker_finished.emit(("错误", "输入的路径不存在", QMessageBox.Icon.Critical))
            return

        # 初始化放大器
        try:
            self.upscaler = ComfyUpscaler.ImageUpscaler(
                url=self.api_url,
                height_thresh=self.height_threshold,
                width_thresh=self.width_threshold,
                size_thresh=self.jpg_size_threshold,
                img_dir=self.img_dir,
                model_name=self.model_name,
                recursive=self.recursive_search,
                downscale=self.post_downscale_scale,
                get_interval=self.get_interval
            )
        except Exception as e:
            logger.exception("初始化放大器失败")
            self.worker_finished.emit(("错误", f"初始化放大器失败: {e}", QMessageBox.Icon.Critical))
            return

        # 运行模式：查找图像
        if self.mode == "find":
            logger.info("开始查找图像...")
            found_images = []

            # 适配修改：get_image_files 现在只生成路径字符串，不返回错误信息（错误已内部记录）
            for file_path in self.upscaler.get_image_files():
                if self._stop:
                    logger.warning("图像查找已终止")
                    self.worker_finished.emit(("提示", "图像查找已终止", QMessageBox.Icon.Warning))
                    return
                found_images.append(file_path)

            self.image_list = found_images

            if not self.image_list:
                logger.info("未找到符合条件的图像")
                self.image_list_got.emit([])
                self.worker_finished.emit(("提示", "未找到符合条件的图像", QMessageBox.Icon.Information))
            else:
                logger.info(f"已找到 {len(self.image_list)} 个图像")
                self.image_list_got.emit(self.image_list)
                self.worker_finished.emit(
                    ("完成", f"已找到 {len(self.image_list)} 个图像", QMessageBox.Icon.Information))
            return

        # 运行模式：放大图像
        elif self.mode == "upscale":
            # 检查列表
            if not self.image_list:
                logger.warning("图像列表为空，无法开始放大")
                self.worker_finished.emit(("错误", "图像列表为空", QMessageBox.Icon.Warning))
                return
            # 检查模型
            if not self.model_name:
                logger.warning("未选择模型，无法开始放大")
                self.worker_finished.emit(("错误", "未选择模型", QMessageBox.Icon.Warning))
                return

            logger.info(f"开始放大任务，共 {len(self.image_list)} 张图像")
            img_list_length = len(self.image_list)
            success_count = 0

            for index, image in enumerate(self.image_list):
                if self._stop:
                    logger.warning("放大任务已被用户终止")
                    self.worker_finished.emit(("提示", "放大已被终止", QMessageBox.Icon.Warning))
                    return

                # 处理前缀
                clean_image_path = utils.remove_substring(image, ["T ", "L ", "TL "], "prefix")

                # 适配修改：send_request_single 返回 int 状态码 (0=成功)
                result_code = self.upscaler.send_request_single(clean_image_path)

                if result_code == 0:
                    success_count += 1
                else:
                    logger.warning(f"图像放大失败 (Code {result_code}): {clean_image_path}")

                progress = int(100 * (index + 1) / img_list_length)
                self.progress_updated.emit(progress)

            logger.info(f"放大任务完成。成功: {success_count}, 总计: {img_list_length}")
            self.worker_finished.emit(
                ("完成", f"处理完成\n成功：{success_count}\n总计：{img_list_length}", QMessageBox.Icon.Information))

        # 其他模式
        else:
            logger.error(f"不受支持的运行模式：{self.mode}")
            self.worker_finished.emit(("错误", f"内部错误：无效模式 {self.mode}", QMessageBox.Icon.Critical))
            return

    def stop(self):
        self._stop = True