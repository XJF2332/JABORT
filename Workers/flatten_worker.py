import os

from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QMessageBox

from Core import log_manager
from Tools.FileManaging import Flatten

logger = log_manager.get_logger(__name__)


class FlattenWorker(QThread):
    worker_finished = Signal(tuple)

    def __init__(self, folder: str):
        """
        初始化旧版展平 worker

        finished 信号传递一个元组，第一项为标题，第二项为内容，第三项为图标

        Args:
            folder: 展平这个文件夹

        Returns:
             None
        """
        super().__init__()
        self.folder = folder
        self._stop = False

    def stop(self):
        """请求停止工作线程"""
        self._stop = True

    def run(self):
        self._stop = False

        if not self.folder or not os.path.exists(self.folder):
            logger.info("路径不存在或为空")
            self.worker_finished.emit(("错误", "路径不存在或为空", QMessageBox.Icon.Critical))
            return

        try:
            self.folder = os.path.normpath(self.folder)
            # 生成器
            generator = Flatten.main(self.folder)
            for _ in generator:
                if self._stop:
                    logger.info("操作已被用户中止")
                    self.worker_finished.emit(("信息", "操作已被用户中止", QMessageBox.Icon.Information))
                    return

            logger.info("展平操作完成")
            self.worker_finished.emit(("信息", "展平完成", QMessageBox.Icon.Information))

        except Exception as e:
            logger.error(f"展平失败: {str(e)}")
            self.worker_finished.emit(("错误", f"展平失败：{str(e)}", QMessageBox.Icon.Critical))
