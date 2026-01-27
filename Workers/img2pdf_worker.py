from Tools.Convertors import ImgSeq2PDF
from PySide6.QtCore import QThread, Signal
import os

class ImgSeq2PDFWorker(QThread):
    progress_updated = Signal(int)
    output_updated = Signal(str)
    worker_finished = Signal()

    def __init__(self, folder: str, send2trash: bool, recursive: bool):
        super().__init__()
        self.folder = folder
        self.send2trash = send2trash
        self.recursive = recursive
        self._stop = False

    def run(self):
        if not self.folder or not os.path.exists(self.folder):
            self.output_updated.emit("输入路径为空或不存在")
            self.worker_finished.emit()
            return

        self._stop = False

        res = ImgSeq2PDF.process_image_sequences(
            target_folder=self.folder,
            send_to_trash=self.send2trash,
            recursive=self.recursive
        )

        for item in res:
            if self._stop:
                self.output_updated.emit("图像序列转换已终止")
                self.worker_finished.emit()
                return
            else:
                self.progress_updated.emit(item[0])
                self.output_updated.emit(item[1])

        self.worker_finished.emit()
        return

    def stop(self):
        self._stop = True

