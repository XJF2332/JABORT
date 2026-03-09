from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QPainter, QPixmap
from PySide6.QtWidgets import QStyle, QWidget

from Core import log_manager

logger = log_manager.get_logger(__name__)


def export_all_icons(output_dir: str = "icons", size: QSize = QSize(64, 64)) -> tuple[int, int]:
    """
    导出所有QStyle图标到指定目录

    Args:
        output_dir: 输出目录
        size: 图标尺寸

    Returns:
        第一项为成功数量，第二项为失败数量
    """
    # 创建输出目录
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # 获取QStyle
    widget = QWidget()
    style = widget.style()

    # 导出统计
    exported_count = 0
    failed_count = 0

    logger.info(f"开始导出QStyle图标到目录: {output_path.absolute()}")
    logger.debug(f"图标尺寸: {size.width()}x{size.height()}")

    # 遍历所有标准图标
    for pixmap in QStyle.StandardPixmap:
        try:
            # 获取图标
            icon = style.standardIcon(pixmap)
            if icon.isNull():
                logger.warning(f"{pixmap.name} 为空")
                failed_count += 1
                continue

            # 创建pixmap并渲染
            pixmap_img = QPixmap(size)
            pixmap_img.fill(Qt.GlobalColor.transparent)

            painter = QPainter(pixmap_img)
            icon.paint(painter, 0, 0, size.width(), size.height())
            painter.end()

            # 保存文件
            filename = f"{pixmap.name}.png"
            filepath = output_path / filename
            if pixmap_img.save(str(filepath), "PNG"):
                exported_count += 1
                logger.info(f"已导出: {filename}")
            else:
                logger.error(f"保存失败: {filename}")
                failed_count += 1

        except Exception as e:
            logger.error(f"处理 {pixmap.name} 时出错: {e}")
            failed_count += 1

    logger.info(f"导出已完成，成功 {exported_count}，失败 {failed_count}")

    return exported_count, failed_count
