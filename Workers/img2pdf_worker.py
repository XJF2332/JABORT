import os

from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QMessageBox

from Core import log_manager
from Tools.Convertors import ImgSeq2PDF

logger = log_manager.get_logger(__name__)


class ImgSeq2PDFWorker(QThread):
    progress_updated = Signal(int)
    worker_finished = Signal(tuple)

    def __init__(self, folder: str, send2trash: bool, recursive: bool):
        super().__init__()
        self.folder = folder
        self.send2trash = send2trash
        self.recursive = recursive
        self._stop = False

    def run(self):
        logger.info(
            f"开始图像序列转PDF任务，目标路径: {self.folder}, 递归: {self.recursive}, 清理原文件: {self.send2trash}")

        if not self.folder or not os.path.exists(self.folder):
            msg = "输入路径为空或不存在"
            logger.error(msg)
            self.worker_finished.emit(("错误", msg, QMessageBox.Icon.Critical))
            return

        self._stop = False

        progress_gen = ImgSeq2PDF.process_image_sequences(
            target_folder=self.folder,
            send_to_trash=self.send2trash,
            recursive=self.recursive
        )

        try:
            for progress in progress_gen:
                if self._stop:
                    logger.info("用户终止了图像序列转换任务")
                    self.worker_finished.emit(("提示", "操作已停止", QMessageBox.Icon.Information))
                    return
                elif progress[0]:
                    logger.error("转换过程出错")
                    self.worker_finished.emit(("错误", "转换失败", QMessageBox.Icon.Information))
                    return
                else:
                    self.progress_updated.emit(progress[1])

            # 循环正常结束
            logger.info("图像序列转换任务完成")
            self.worker_finished.emit(("完成", "所有任务已完成！", QMessageBox.Icon.Information))

        except Exception as e:
            logger.error(f"发生未知错误: {str(e)}")
            self.worker_finished.emit(("错误", f"发生未知错误: {str(e)}", QMessageBox.Icon.Critical))
            return

    def stop(self):
        self._stop = True