import os

from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QMessageBox

from Core import log_manager
from Core.error_codes import ErrorCode
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

        if not self.folder or not os.path.isdir(self.folder):
            logger.error(ErrorCode.InvalidPath.format(self.folder))
            self.worker_finished.emit(("错误", ErrorCode.InvalidPath.format(self.folder), QMessageBox.Icon.Critical))
            return

        self._stop = False

        results = ImgSeq2PDF.process_image_sequences(
            target_folder=self.folder,
            send_to_trash=self.send2trash,
            recursive=self.recursive
        )

        try:
            for res in results:
                if self._stop:
                    logger.info(ErrorCode.UserInterrupt.format("图像序列转PDF"))
                    self.worker_finished.emit(("提示", ErrorCode.UserInterrupt.format("图像序列转PDF"),
                                               QMessageBox.Icon.Information))
                    return
                elif res[0] != ErrorCode.Success:
                    logger.error(ErrorCode.Unknown.generic)
                    self.worker_finished.emit(("错误", res[0].generic, QMessageBox.Icon.Information))
                    return
                else:
                    self.progress_updated.emit(res[1])

            # 循环正常结束
            logger.info(ErrorCode.Success.format("图像序列转PDF"))
            self.worker_finished.emit(("完成", ErrorCode.Success.format("图像序列转PDF"), QMessageBox.Icon.Information))

        except Exception as e:
            logger.error(ErrorCode.Unknown.format(str(e)))
            self.worker_finished.emit(("错误", ErrorCode.Unknown.format(str(e)), QMessageBox.Icon.Critical))
            return

    def stop(self):
        self._stop = True