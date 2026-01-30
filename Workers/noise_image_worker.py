import os.path
from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QMessageBox

from Tools.TestTools import NoiseImageGen
from Core import log_manager

logger = log_manager.get_logger(__name__)


class NoiseImageWorker(QThread):
    progress_updated = Signal(int)
    worker_finished = Signal(tuple)

    def __init__(self, num_images, output_folder):
        super().__init__()
        self.num_images = num_images
        self.output_folder = output_folder
        self._stop = False

    def stop(self):
        self._stop = True
        logger.info(f"停止标志已更新为 {self._stop}")

    def run(self):
        if not self.output_folder or not os.path.exists(self.output_folder):
            logger.error("路径不存在或为空")
            self.worker_finished.emit(("错误", "路径不存在或为空", QMessageBox.Icon.Critical))
            return

        self._stop = False
        logger.info(f"开始生成 {self.num_images} 张噪声图片到 {self.output_folder}")

        for i in range(self.num_images):
            if self._stop:
                logger.info("生成已被用户终止")
                self.worker_finished.emit(("提示", "生成已被终止", QMessageBox.Icon.Information))
                return

            # NoiseImageGen 现在直接返回 int (0成功, 1失败)
            result = NoiseImageGen.generate_noise_image(self.output_folder, i + 1)

            self.progress_updated.emit(int((i + 1) / self.num_images * 100))

            if result != 0:
                logger.error(f"生成第 {i + 1} 张图片时发生错误")
                self.worker_finished.emit(("错误", "生成噪声图片时发生错误", QMessageBox.Icon.Critical))
                return

        logger.info("所有图片生成完成")
        self.worker_finished.emit(("完成", "生成完成", QMessageBox.Icon.Information))
