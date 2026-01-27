import os.path

import send2trash
from PySide6.QtCore import QThread, Signal

from Tools.Convertors import PNG2JPG


class PNG2JPGWorker(QThread):
    progress_updated = Signal(int)
    output_updated = Signal(str)
    worker_finished = Signal()

    def __init__(self, image_dir: str, recursive: bool, quality: int, ignore_transparency: bool,
                 preserve_metadata: bool, delete_origin: bool, deduplicate: int):
        """
        PNG转JPG初始化

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
        self.get_result = PNG2JPG.get_image_list(
            folder=self.image_dir,
            recursive=self.recursive,
            ignore_transparency=self.ignore_trans
        )

    def stop(self):
        self._stop = True

    def run(self):
        self.get_images()
        self.image_list = self.get_result[1]
        if self.get_result[0] != 0:
            self.output_updated.emit(self.get_result[1])
            self.worker_finished.emit()
            return
        if not self.image_list:
            self.output_updated.emit("[PNG转JPG] 未找到图像")
            self.worker_finished.emit()
            return
        # 转换
        self.image_list = [os.path.normpath(i) for i in self.image_list]
        result = PNG2JPG.convert_batch(
            paths=self.image_list,
            quality=self.quality,
            preserve_metadata=self.metadata,
            deduplicate=self.deduplicate
        )
        for item in result:
            if self._stop:
                self.output_updated.emit("[PNG转JPG] 转换已被终止")
                self.worker_finished.emit()
                return
            self.output_updated.emit(item[1])
            self.progress_updated.emit(item[0])
        # 删除
        if self.delete_origin:
            send2trash.send2trash(self.image_list)
        # 完成
        self.output_updated.emit("[PNG转JPG] 已完成转换")
        self.worker_finished.emit()
