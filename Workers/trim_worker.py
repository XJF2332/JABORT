import os

from PySide6.QtCore import QThread, Signal, QTime
from PySide6.QtWidgets import QMessageBox

from Core import log_manager
from Core.error_codes import ErrorCode
from Tools.Utils import utils
from Tools.MediaProcessing import VideoTrim

logger = log_manager.get_logger(__name__)

class TrimmerWorker(QThread):
    worker_finished = Signal(tuple)
    output_path_built = Signal(str)

    def __init__(self, input_path: str, input_time: QTime, output_path: str, preserve: int):
        super().__init__()
        self.input_path = input_path
        self.input_time = input_time
        self.output_path = output_path
        self.preserve = preserve

    def run(self):
        logger.info(f"开始剪切：{self.input_path}")
        # 检查输入
        if not self.input_path or not os.path.exists(self.input_path):
            logger.error(ErrorCode.InvalidPath.format(self.input_path))
            self.worker_finished.emit(("错误", ErrorCode.InvalidPath.format(self.input_path), QMessageBox.Icon.Critical))
            return
        # 检查重名
        if self.input_path == self.output_path:
            logger.error(ErrorCode.DuplicateIOName.generic)
            self.worker_finished.emit(("错误", ErrorCode.DuplicateIOName.generic, QMessageBox.Icon.Critical))
            return
        # 构建输出
        if not self.output_path:
            build_res = utils.build_output_path(
                input_path=self.input_path, suffix=self.input_time.toString("HHmmss"), spacing="_"
            )
        else:
            build_res = utils.filename_deduplicate(2, self.output_path)
        # 检查构建结果
        if build_res[0] == ErrorCode.FileSkipped:
            logger.info(f"已跳过输出，因为输出文件路径已存在")
            self.worker_finished.emit(("警告", "已跳过输出，因为输出文件路径已存在", QMessageBox.Icon.Warning))
            return
        elif build_res[0] != ErrorCode.Success:
            logger.error(build_res[0].generic)
            self.worker_finished.emit(("错误", build_res[0].generic, QMessageBox.Icon.Critical))
            return
        else:
            logger.debug(f"构建输出文件名：{build_res[1]}")
            self.output_path = build_res[1]
            if not os.path.exists(os.path.dirname(self.output_path)):
                os.makedirs(os.path.dirname(self.output_path))
                logger.debug(f"输出文件所在文件夹不存在，已创建")
        # 进行剪切
        err, output = VideoTrim.trim_video(self.input_path, self.input_time, self.output_path, self.preserve)
        if err != ErrorCode.Success:
            logger.error(err.generic)
            self.worker_finished.emit(("错误", err.generic, QMessageBox.Icon.Critical))
            return
        else:
            logger.info(f"剪切后的视频已保存到 {output}")
            self.worker_finished.emit(("信息", f"剪切后的视频已保存到 {output}", QMessageBox.Icon.Information))
            return