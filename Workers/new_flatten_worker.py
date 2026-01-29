import os.path

from PySide6.QtCore import Signal, QThread
from PySide6.QtWidgets import QMessageBox

from Core import log_manager
from Tools.FileManaging import FlattenNew

logger = log_manager.get_logger(__name__)

class NewFlattenWorker(QThread):
    progress_updated = Signal(int)
    worker_finished = Signal(tuple)

    def __init__(self, folder: str):
        """
        展平一个文件夹

        finished信号用于弹出提示框，第一项为标题，第二项为内容，第三项为图标

        Args:
            folder: 要展平的文件夹
        """
        super().__init__()
        self.folder = folder
        self._stop = False

    def stop(self):
        self._stop = True
        logger.info("停止标志已更新")

    def run(self):
        self._stop = False
        if not self.folder or not os.path.exists(self.folder):
            logger.error("路径不存在或为空")
            self.worker_finished.emit(("错误", "路径不存在或为空", QMessageBox.Icon.Critical))
            return

        try:
            logger.info(f"准备展平：{self.folder}")
            self.folder = os.path.normpath(self.folder)
            # 展平为麦考米克
            for progress in FlattenNew.process_flatten(self.folder):
                if self._stop:
                    logger.info("展平已被用户终止")
                    self.worker_finished.emit(("信息", "展平已被终止", QMessageBox.Icon.Information))
                    return
                self.progress_updated.emit(progress * 0.9)
            logger.info(f"展平完成，准备清理")
            # 清理空文件夹
            FlattenNew.process_cleanup(self.folder)
            logger.info("清理完成")
            # 所有任务完成
            self.progress_updated.emit(100)
            self.worker_finished.emit(("信息", "展平完成", QMessageBox.Icon.Information))

        except Exception as e:
            logger.error(f"无法完成展平：{e}")
            self.worker_finished.emit(("错误", f"无法完成展平：{e}", QMessageBox.Icon.Critical))
