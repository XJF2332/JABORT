import os

from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QMessageBox

from Core import log_manager
from Core.error_codes import ErrorCode
from Tools.MediaProcessing import ComfyUpscaler
from Tools.Utils import utils

logger = log_manager.get_logger(__name__)


class UpscalerWorker(QThread):
    progress_updated = Signal(int)
    image_list_got = Signal(list)
    output_path_updated = Signal(str)
    worker_finished = Signal(tuple)

    def __init__(self, model_name: str, img_dir: str, recursive_search: bool, width_threshold: int,
                 height_threshold: int, jpg_size_threshold: int, post_downscale_scale: float, url: str,
                 image_list: list, save_dir: str, mode: str = "upscale"):
        super().__init__()
        self.model_name = model_name
        self.img_dir = img_dir
        self.recursive_search = recursive_search
        self.width_threshold = width_threshold
        self.height_threshold = height_threshold
        self.jpg_size_threshold = jpg_size_threshold
        self.post_downscale_scale = post_downscale_scale
        self.api_url = url
        self.image_list = image_list
        self.mode = mode
        self.save_dir = save_dir if save_dir else os.path.join(self.img_dir, "Upscaled")
        self.upscaler = None
        self._stop = False

    def run(self):
        self._stop = False
        logger.info(f"放大器工作线程启动，模式: {self.mode}")

        # 无效的输入
        if not self.img_dir or not os.path.exists(self.img_dir):
            self.worker_finished.emit(("错误", ErrorCode.InvalidPath.format(self.img_dir), QMessageBox.Icon.Critical))
            return
        # 输出不存在
        elif not os.path.exists(self.save_dir):
            try:
                os.makedirs(self.save_dir)
                self.output_path_updated.emit(self.save_dir)
            except PermissionError as e:
                logger.error(f"无法创建输出文件夹 {self.save_dir}：{str(e)}")
                self.worker_finished.emit("错误", ErrorCode.CannotMakeDir.format(self.save_dir),
                                          QMessageBox.Icon.Critical)
                return
            except Exception as e:
                logger.error(f"创建输出文件夹 {self.save_dir} 时出现未知错误：{str(e)}")
                self.worker_finished.emit("错误", ErrorCode.Unknown.format("创建输出文件夹"),
                                          QMessageBox.Icon.Critical)

        # 初始化放大器
        self.upscaler = ComfyUpscaler.ImageUpscaler(
            url=self.api_url,
            height_thresh=self.height_threshold,
            width_thresh=self.width_threshold,
            size_thresh=self.jpg_size_threshold,
            img_dir=self.img_dir,
            model_name=self.model_name,
            recursive=self.recursive_search,
            downscale=self.post_downscale_scale,
            save_dir=self.save_dir
        )

        # 查找图像
        if self.mode == "find":
            logger.info(f"在 {self.img_dir} 下查找图像")
            self.image_list = []

            for res in self.upscaler.get_image_files():
                if self._stop:
                    logger.info("图像查找已终止")
                    self.worker_finished.emit(("提示", ErrorCode.UserInterrupt.generic, QMessageBox.Icon.Warning))
                    return
                elif res[0] == ErrorCode.Success:
                    self.image_list.append(res[1])
                elif res[0] == ErrorCode.BrokenImage:
                    logger.warning(f"发现损坏的图像，已跳过: {res[1]}")
                elif res[0] == ErrorCode.FileSkipped:
                    pass
                else:
                    logger.error(res[0].generic)
                    self.worker_finished.emit("错误", res[0].generic, QMessageBox.Icon.Critical)
                    return

            if not self.image_list:
                logger.info("未找到符合条件的图像")
                self.image_list_got.emit([])
                self.worker_finished.emit(("提示", ErrorCode.NoImageFound.generic, QMessageBox.Icon.Information))
            else:
                logger.info(f"已找到 {len(self.image_list)} 个图像")
                self.image_list_got.emit(self.image_list)
                self.worker_finished.emit(
                    ("完成", f"已找到 {len(self.image_list)} 个图像", QMessageBox.Icon.Information))

            return
        # 放大图像
        elif self.mode == "upscale":
            if not self.image_list:
                logger.error("图像列表为空")
                self.worker_finished.emit(("错误", ErrorCode.EmptyList.generic, QMessageBox.Icon.Warning))
                return
            elif not self.model_name:
                logger.error("未选择模型")
                self.worker_finished.emit(("错误", "未选择模型", QMessageBox.Icon.Warning))
                return

            img_count = len(self.image_list)
            logger.info(f"开始放大任务，共 {img_count} 张图像")
            success_count = 0
            fail_count = 0

            for index, image in enumerate(self.image_list):
                if self._stop:
                    logger.info(ErrorCode.UserInterrupt.format("放大"))
                    self.worker_finished.emit(
                        ("提示", ErrorCode.UserInterrupt.format("放大"), QMessageBox.Icon.Warning))
                    return

                res = self.upscaler.send_request_single(
                    utils.remove_substring(image, ["T ", "L ", "TL "], "prefix"))

                if res[0] == ErrorCode.Success:
                    success_count += 1
                # 链接错误就没必要再发送请求了
                elif res[0] == ErrorCode.ApiConnectionError:
                    fail_count += 1
                    logger.error("检测到连接错误，停止后续任务")
                    self.worker_finished.emit(("错误", res[0].generic, QMessageBox.Icon.Critical))
                    return
                else:
                    fail_count += 1
                    logger.error(f"无法放大 {image}：{res[0].generic}")

                self.progress_updated.emit(int(100 * (index + 1) / img_count))

            logger.info(f"放大任务完成，成功：{success_count}，失败：{fail_count}")
            msg_icon = QMessageBox.Icon.Information if fail_count == 0 else QMessageBox.Icon.Warning
            self.worker_finished.emit(("完成", f"放大完成\n成功：{success_count}\n失败：{fail_count}", msg_icon))
        # 其他模式
        else:
            logger.error(f"不受支持的运行模式：{self.mode}")
            self.worker_finished.emit(("错误", f"不受支持的运行模式：{self.mode}", QMessageBox.Icon.Critical))
            return

    def stop(self):
        self._stop = True