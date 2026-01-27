from __future__ import annotations

import os
import sys
from pathlib import Path

from PySide6.QtGui import QFont, QPainter, QPixmap
from PySide6.QtWidgets import QApplication, QHBoxLayout, QLayout, QMainWindow, QPushButton, QScrollArea, QStyle, \
    QVBoxLayout, \
    QWidget
from PySide6.QtCore import QSize, Qt


class IconExporter:
    """图标导出器"""

    @staticmethod
    def export_all_icons(output_dir: str = "Icons", size: QSize = QSize(64, 64)):
        """
        导出所有QStyle图标到指定目录

        Args:
            output_dir: 输出目录
            size: 图标尺寸
        """
        # 创建输出目录
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # 获取QStyle
        app = QApplication.instance() or QApplication(sys.argv)
        widget = QWidget()
        style = widget.style()

        # 导出统计
        exported_count = 0
        failed_count = 0

        print(f"开始导出QStyle图标到目录: {output_path.absolute()}")
        print(f"图标尺寸: {size.width()}x{size.height()}")

        # 遍历所有标准图标
        for pixmap in QStyle.StandardPixmap:
            try:
                # 获取图标
                icon = style.standardIcon(pixmap)
                if icon.isNull():
                    print(f"警告: {pixmap.name} 图标为空")
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
                    print(f"✓ 已导出: {filename}")
                else:
                    print(f"✗ 保存失败: {filename}")
                    failed_count += 1

            except Exception as e:
                print(f"✗ 处理 {pixmap.name} 时出错: {e}")
                failed_count += 1

        print(f"\n导出完成!")
        print(f"成功: {exported_count}, 失败: {failed_count}")
        print(f"总图标数: {len(list(QStyle.StandardPixmap))}")
        print(f"图标保存在: {output_path.absolute()}")


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Hello, QStyle Icons!')

        # 添加导出按钮
        export_button = QPushButton("导出所有图标")
        export_button.clicked.connect(self.export_icons)

        v_main_layout = QVBoxLayout()
        v_main_layout.addWidget(export_button)

        count = 0
        h_layout = QHBoxLayout()
        for pixmap in QStyle.StandardPixmap:
            button = QPushButton(pixmap.name, parent=self)
            button.setFont(QFont('Ubuntu nf', 12))  # 减小字体大小以适应按钮
            style = button.style()
            icon = style.standardIcon(pixmap)
            button.setIcon(icon)
            button.setToolTip(pixmap.name)
            h_layout.addWidget(button)
            count += 1
            if count % 4 == 0:  # 每行显示4个按钮
                v_main_layout.addLayout(h_layout)
                count = 0
                h_layout = QHBoxLayout()
        if count > 0:
            v_main_layout.addLayout(h_layout)

        self.setCentralWidget(self.init_scroll_area(v_main_layout))

    def export_icons(self):
        """导出图标按钮的回调"""
        IconExporter.export_all_icons()

    def init_scroll_area(self, layout: QLayout) -> QScrollArea:
        colors_container = QWidget()
        colors_container.setLayout(layout)
        colors_scroll_area = QScrollArea(self)
        colors_scroll_area.setWidgetResizable(True)
        colors_scroll_area.setWidget(colors_container)
        return colors_scroll_area


if __name__ == '__main__':
    # 检查命令行参数
    if "--export" in sys.argv or "-e" in sys.argv:
        # 静默导出模式
        app = QApplication(sys.argv)
        IconExporter.export_all_icons()
        sys.exit(0)
    else:
        # GUI模式
        app = QApplication(sys.argv)
        window = MyMainWindow()
        window.resize(1000, 800)
        window.show()
        sys.exit(app.exec())