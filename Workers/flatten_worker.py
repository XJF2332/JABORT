import os

from PySide6.QtCore import QThread, Signal

from Tools.FileManaging import Flatten


class FlattenWorker(QThread):
    output_updated = Signal(str)
    worker_finished = Signal()

    def __init__(self, folder: str):
        super().__init__()
        self.folder = folder
        self._stop = False

    def stop(self):
        """请求停止工作线程"""
        self._stop = True

    def run(self):
        self._stop = False

        if not self.folder or not os.path.exists(self.folder):
            self.output_updated.emit("[旧版展平] 路径不存在或为空。")
            self.worker_finished.emit()
            return

        try:
            self.folder = os.path.normpath(self.folder)
            # 生成器
            generator = Flatten.main(self.folder)
            for log_message in generator:
                if self._stop:
                    self.output_updated.emit("[旧版展平] 操作已被中止。")
                    self.worker_finished.emit()
                    return

                self.output_updated.emit(log_message)

            if not self._stop:
                self.output_updated.emit("[旧版展平] 操作完成。")
                self.worker_finished.emit()

        except Exception as e:
            self.output_updated.emit(f"[旧版展平] 发生异常: {str(e)}")
            self.worker_finished.emit()
