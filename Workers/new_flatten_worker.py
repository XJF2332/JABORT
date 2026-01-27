import os.path

from PySide6.QtCore import Signal, QThread

from Tools.FileManaging import FlattenNew


class NewFlattenWorker(QThread):
    progress_updated = Signal(float)
    output_updated = Signal(str)
    worker_finished = Signal()

    def __init__(self, folder: str):
        super().__init__()
        self.folder = folder
        self._stop = False

    def stop(self):
        self._stop = True

    def run(self):
        self._stop = False
        if not self.folder or not os.path.exists(self.folder):
            self.output_updated.emit("[展平] 路径为空或不存在。")
            self.worker_finished.emit()
            return

        try:
            self.folder = os.path.normpath(self.folder)
            # 展平操作
            for progress, message in FlattenNew.process_flatten(self.folder):
                if self._stop:
                    self.output_updated.emit("[展平] 操作已被终止。")
                    self.worker_finished.emit()
                    return
                self.output_updated.emit(message)
                global_progress = progress * 0.9
                self.progress_updated.emit(global_progress)

            # 清理操作
            for progress, message in FlattenNew.process_cleanup(self.folder):
                if self._stop:
                    self.output_updated.emit("[展平] 操作已被终止。")
                    self.worker_finished.emit()
                    return
                self.output_updated.emit(message)
                global_progress = 0.9 + (progress * 0.1)
                self.progress_updated.emit(global_progress)

            # 所有任务完成
            self.output_updated.emit("[展平] 所有操作已完成")
            self.worker_finished.emit()

        except Exception as e:
            # 捕获未处理的异常
            self.output_updated.emit(f"[展平] 发生严重错误: {e}")
            self.progress_updated.emit(1.0)
            self.worker_finished.emit()
