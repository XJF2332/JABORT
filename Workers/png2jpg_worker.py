import os.path

import send2trash
from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QMessageBox

from Tools.Convertors import PNG2JPG
from Core import log_manager
from Core.error_codes import ErrorCode

logger = log_manager.get_logger(__name__)


class PNG2JPGWorker(QThread):
    progress_updated = Signal(int)
    worker_finished = Signal(tuple)

    def __init__(self, image_dir: str, recursive: bool, quality: int, skip_transparency: bool,
                 preserve_metadata: bool, delete_origin: bool, deduplicate: int):
        """
        PNG转JPG初始化

        finished信号用于弹出提示框，第一项为标题，第二项为内容，第三项为图标

        :param image_dir: 要处理的目录
        :param recursive: 递归查找
        :param quality: 质量
        :param skip_transparency: 跳过有透明通道的图像
        :param preserve_metadata: 保留元数据
        :param delete_origin: 是否在转换后删除原文件
        :param deduplicate: 去重模式，0覆盖，1跳过，2增加序号
        """
        super().__init__()
        self.image_dir = image_dir
        self.image_list = []
        self.get_result = (ErrorCode.Success, [])
        self.recursive = recursive
        self.quality = quality
        self.skip_trans = skip_transparency
        self.metadata = preserve_metadata
        self.delete_origin = delete_origin
        self.deduplicate = deduplicate
        self._stop = False

    def get_images(self):
        self.get_result = PNG2JPG.get_image_list(
            folder=self.image_dir,
            recursive=self.recursive,
            pass_trans=self.skip_trans
        )

    def stop(self):
        self._stop = True

    def run(self):
        logger.info(f"在 {self.image_dir} 下查找图像")
        self.get_images()
        # 如果出现错误
        if self.get_result[0] == ErrorCode.Success:
            self.image_list = self.get_result[1]
        else:
            self.worker_finished.emit(("错误",self.get_result[0].generic,QMessageBox.Icon.Critical))
            return
        # 检查是否找到图像
        if not self.image_list:
            logger.error(ErrorCode.NoImageFound.generic)
            self.worker_finished.emit(("错误",ErrorCode.NoImageFound.generic,QMessageBox.Icon.Critical))
            return
        # 转换并记录状态
        logger.info("正在转换")
        self.image_list = [os.path.normpath(i) for i in self.image_list]
        res = PNG2JPG.convert_batch(
            images=self.image_list,
            quality=self.quality,
            preserve_metadata=self.metadata,
            deduplicate=self.deduplicate
        )
        for item in res:
            # 手动终止
            if self._stop:
                logger.error(ErrorCode.UserInterrupt.format("转换"))
                self.worker_finished.emit(("信息",ErrorCode.UserInterrupt.format("转换"),QMessageBox.Icon.Information))
                return
            # 状态异常
            elif item[0] != ErrorCode.Success and item[0] != ErrorCode.FileSkipped:
                logger.error(item[0].generic)
                self.worker_finished.emit(("错误", item[0].generic, QMessageBox.Icon.Critical))
                return
            # 状态正常
            else:
                self.progress_updated.emit(item[1])
        # 删除
        if self.delete_origin:
            logger.info("正在清理原图像")
            send2trash.send2trash(self.image_list)
        # 完成
        logger.info("转换已完成")
        self.worker_finished.emit(("信息","转换已完成",QMessageBox.Icon.Information))
