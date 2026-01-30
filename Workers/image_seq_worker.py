import os.path
from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QMessageBox

from Tools.TestTools import ImgSeqGen
from Core import log_manager

logger = log_manager.get_logger(__name__)


class ImageSeqWorker(QThread):
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

        res = ImgSeqGen.generate_image_sequence(self.output_folder, self.num_images, (256,256))
        for i in res:
            if self._stop:
                logger.info("生成已被用户终止")
                self.worker_finished.emit(("提示", "生成已被终止", QMessageBox.Icon.Information))
                return

            self.progress_updated.emit(i[0])

            if i[1]:
                logger.error(f"生成图片时发生错误")
                self.worker_finished.emit(("错误", "生成图片时发生错误", QMessageBox.Icon.Critical))
                return

        logger.info("所有图片生成完成")
        self.worker_finished.emit(("完成", "所有图片生成完成", QMessageBox.Icon.Information))
