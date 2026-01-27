import os.path

import send2trash
from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QMessageBox

from Tools.Convertors import PNG2JPG
from Core import log_manager

logger = log_manager.get_logger(__name__)


class PNG2JPGWorker(QThread):
    progress_updated = Signal(int)
    worker_finished = Signal(tuple)

    def __init__(self, image_dir: str, recursive: bool, quality: int, ignore_transparency: bool,
                 preserve_metadata: bool, delete_origin: bool, deduplicate: int):
        """
        PNG转JPG初始化

        finished信号用于弹出提示框，第一项为标题，第二项为内容，第三项为图标

        :param image_dir: 要处理的目录
        :param recursive: 递归查找
        :param quality: 质量
        :param ignore_transparency: 无视透明度（即使有透明通道也转换）
        :param preserve_metadata: 保留元数据
        :param delete_origin: 是否在转换后删除原文件
        :param deduplicate: 去重模式，0覆盖，1跳过，2增加序号
        """
        super().__init__()
        self.image_dir = image_dir
        self.image_list = []
        self.get_result = (-1, [])
        self.recursive = recursive
        self.quality = quality
        self.ignore_trans = ignore_transparency
        self.metadata = preserve_metadata
        self.delete_origin = delete_origin
        self.deduplicate = deduplicate
        self._stop = False

    def get_images(self):
        logger.info("正在查找图像")
        self.get_result = PNG2JPG.get_image_list(
            folder=self.image_dir,
            recursive=self.recursive,
            pass_trans=self.ignore_trans
        )

    def stop(self):
        self._stop = True

    def run(self):
        logger.info(f"在 {self.image_dir} 下查找图像")
        self.get_images()
        # 如果出现错误
        if self.get_result[0] == 1:
            self.worker_finished.emit(("错误","路径为空或找不到指定的路径",QMessageBox.Icon.Critical))
            return
        elif self.get_result[0] == 2:
            self.worker_finished.emit(("错误","未知错误",QMessageBox.Icon.Critical))
            return
        else:
            self.image_list = self.get_result[1]
        # 检查是否未找到图像
        if not self.image_list:
            logger.info("未找到符合要求的图像")
            self.worker_finished.emit(("错误","未找到符合要求的图像",QMessageBox.Icon.Critical))
            return
        # 转换并记录状态
        logger.info("正在转换")
        stats = []
        self.image_list = [os.path.normpath(i) for i in self.image_list]
        result = PNG2JPG.convert_batch(
            paths=self.image_list,
            quality=self.quality,
            preserve_metadata=self.metadata,
            deduplicate=self.deduplicate
        )
        for item in result:
            if self._stop:
                logger.error("转换已被用户终止")
                self.worker_finished.emit(("信息","转换已被用户终止",QMessageBox.Icon.Information))
                return
            else:
                stats.append(item[1])
                self.progress_updated.emit(item[0])
        logger.debug(f"所有转换任务的状态：{stats}")
        # 删除
        if self.delete_origin:
            logger.info("正在清理原图像")
            send2trash.send2trash(self.image_list)
        # 完成
        logger.info("转换已完成")
        self.worker_finished.emit(("信息","转换已完成",QMessageBox.Icon.Information))
