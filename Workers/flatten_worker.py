import os

from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QMessageBox

from Core import log_manager
from Core.error_codes import ErrorCode
from Tools.FileManaging import Flatten

logger = log_manager.get_logger(__name__)


class FlattenWorker(QThread):
    worker_finished = Signal(tuple)

    def __init__(self, folder: str):
        """
        初始化展平 worker

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

        if not self.folder:
            logger.info("路径为空")
            self.worker_finished.emit(("错误", ErrorCode.InvalidPath.format("路径为空"), QMessageBox.Icon.Critical))
            return

        try:
            self.folder = os.path.normpath(self.folder)

            # 统计信息（可选）
            success_count = 0
            error_count = 0

            # 生成器
            generator = Flatten.main(self.folder)

            for result in generator:
                if self._stop:
                    logger.info("操作已被用户中止")
                    self.worker_finished.emit(
                        ("信息", ErrorCode.UserInterrupt.format("展平操作"), QMessageBox.Icon.Information))
                    return

                code, msg = result

                if code == ErrorCode.Success:
                    success_count += 1
                    # 可以在这里 emit 进度更新信号，如果需要的话
                elif code == ErrorCode.FileSkipped:
                    # 跳过不需要报错，但可以记录 debug 日志
                    logger.debug(f"跳过: {msg}")
                else:
                    error_count += 1
                    logger.error(code.format(msg))
                    # 如果遇到严重错误，是否要中止？这里选择继续尝试其他文件

            # 最终总结
            if error_count > 0:
                final_msg = f"操作完成，但有 {error_count} 个错误。请查看日志。"
                icon = QMessageBox.Icon.Warning
                title = "完成（有警告）"
            else:
                final_msg = ErrorCode.Success.format("展平")
                icon = QMessageBox.Icon.Information
                title = "信息"

            logger.info("展平操作流程结束")
            self.worker_finished.emit((title, final_msg, icon))

        except Exception as e:
            logger.critical(f"展平Worker发生未捕获异常: {str(e)}")
            self.worker_finished.emit(("严重错误", ErrorCode.Unknown.format(str(e)), QMessageBox.Icon.Critical))