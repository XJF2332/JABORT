import os

from PySide6.QtCore import QThread, Signal

from Tools.MediaProcessing import ComfyUpscaler
from Tools.Utils import utils


class UpscalerWorker(QThread):
    progress_updated = Signal(int)
    output_updated = Signal(str)
    image_list_got = Signal(list)
    worker_finished = Signal()

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
        :param model_name: 放大模型名称
        :param img_dir: 查找图像路径
        :param recursive_search: 是否递归查找
        :param width_threshold: 图像宽度阈值
        :param height_threshold: 图像高度阈值
        :param jpg_size_threshold: jpg大小阈值
        :param post_downscale_scale: 放大后缩小为多少倍
        :param url: comfyui api url
        :param get_interval: 多久查询一次任务队列状态
        :param image_list: 图像列表
        :param mode: 运行模式，有效值：upscale - 放大， find - 查找图像
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
        if not self.img_dir:
            self.output_updated.emit("[ComfyUI 放大器] 输入的路径为空")
            self.worker_finished.emit()
            return
        elif not os.path.exists(self.img_dir):
            self.output_updated.emit(f"[ComfyUI 放大器] 输入的路径不存在")
            self.worker_finished.emit()
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
            self.output_updated.emit(f"[ComfyUI 放大器] 初始化放大器失败: {e}")
            self.worker_finished.emit()
            return
        # 查找图像
        if self.mode == "find":
            self._stop = False
            get_result = self.upscaler.get_image_files()
            self.image_list = []

            for item in get_result:
                if self._stop:
                    self.output_updated.emit("[ComfyUI 放大器] 图像查找已终止")
                    self.worker_finished.emit()
                    return
                if item[0]:
                    self.output_updated.emit(item[1])
                elif item[0] == 0:
                    self.image_list = item[1]
                    self.image_list_got.emit(self.image_list if self.image_list else [])

            if len(self.image_list) == 0:
                self.output_updated.emit("[ComfyUI 放大器] 未找到符合条件的图像")
                self.image_list_got.emit([])
            else:
                self.output_updated.emit(f"[ComfyUI 放大器] 已找到{len(self.image_list)}个图像")
                self.image_list_got.emit(self.image_list)

            self.worker_finished.emit()
            return

        # 放大图像
        elif self.mode == "upscale":
            # 检查列表
            if not self.image_list or len(self.image_list) == 0:
                self.output_updated.emit("[ComfyUI 放大器] 图像列表为空")
                self.worker_finished.emit()
                return
            # 检查模型
            if not self.model_name:
                self.output_updated.emit("[ComfyUI 放大器] 未选择模型")
                self.worker_finished.emit()
                return
            # 放大
            img_list_length = len(self.image_list)

            for index, image in enumerate(self.image_list):
                if self._stop:
                    self.output_updated.emit("[ComfyUI 放大器] 放大已被终止")
                    self.worker_finished.emit()
                    return
                image = utils.remove_substring(image, ["T ", "L ", "TL "], "prefix")
                current_result = self.upscaler.send_request_single(image)
                progress = int(100 * (index + 1) / img_list_length)
                self.progress_updated.emit(progress)
                self.output_updated.emit(current_result)

            self.worker_finished.emit()
        # 其他
        else:
            self.output_updated.emit(f"[ComfyUI 放大器] 不受支持的运行模式：{self.mode}")
            self.worker_finished.emit()
            return

    def stop(self):
        self._stop = True
