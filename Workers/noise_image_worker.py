import os.path
from PySide6.QtCore import QThread, Signal

from Tools.TestTools import NoiseImageGen


class NoiseImageWorker(QThread):
    progress_updated = Signal(int)
    output_updated = Signal(str)
    worker_finished = Signal(str)

    def __init__(self, num_images, output_folder):
        super().__init__()
        self.num_images = num_images
        self.output_folder = output_folder
        self._stop = False

    def stop(self):
        self._stop = True

    def run(self):
        if not self.output_folder or not os.path.exists(self.output_folder):
            self.worker_finished.emit("[噪声图像生成] 目标路径为空或不存在")
            return

        self._stop = False
        self.output_updated.emit(f"[噪声图片生成] 开始生成 {self.num_images} 张噪声图片到 {self.output_folder}")

        for i in range(self.num_images):
            if self._stop:
                self.worker_finished.emit("[噪声图像生成] 生成已被终止")
                return
            result = NoiseImageGen.generate_noise_image(self.output_folder, i + 1)
            self.output_updated.emit(result[1])
            self.progress_updated.emit(int((i + 1) / self.num_images * 100))
            if result[0] != 0:
                self.worker_finished.emit(result[1])
                return

        self.worker_finished.emit("[噪声图像生成] 生成完成")
