import os
import re
from typing import List, Tuple, Callable

import send2trash
from PySide6.QtWidgets import QComboBox, QMenu, QListWidget, QMessageBox, QWidget

from Core import log_manager
from Tools.Utils import utils

logger = log_manager.get_logger(__name__)


def show_message_box(parent: QWidget = None, title: str = "提示", content: str = "",
                     icon: QMessageBox.Icon = QMessageBox.Icon.NoIcon):
    """
    显示一个只有一个"确定"按钮的带图标的消息框

    可选的icon：
    - QMessageBox.Icon.NoIcon: 无图标
    - QMessageBox.Icon.Information: 信息图标
    - QMessageBox.Icon.Warning: 警告图标
    - QMessageBox.Icon.Critical: 错误图标
    - QMessageBox.Icon.Question: 问号图标

    Args:
        parent: 父窗口，默认为None
        title: 消息框标题，默认为"提示"
        content: 消息内容，默认为空
        icon: 消息图标，默认为QMessageBox.Icon.NoIcon
    """
    msg_box = QMessageBox(parent)
    msg_box.setWindowTitle(title)
    msg_box.setText(content)
    msg_box.setIcon(icon)
    msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
    msg_box.setDefaultButton(QMessageBox.StandardButton.Ok)
    msg_box.exec()


def set_widget_items(target_widget: QListWidget | QComboBox, lst: list[str], remember_prev: bool = True):
    """
    设置ListWidget或者ComboBox的项
    Args:
        target_widget: 要设置的widget
        lst: 要设置的内容
        remember_prev: （仅适用于ComboBox）记住上次选择

    Returns:
        None
    """
    if type(target_widget) == QComboBox and remember_prev:
        prev = target_widget.currentText()
        target_widget.clear()
        target_widget.addItems(lst)
        target_widget.setCurrentText(prev) if prev and prev in lst else target_widget.setCurrentIndex(0)
    else:
        target_widget.clear()
        target_widget.addItems(lst)


def refresh_combobox(target_widget: QComboBox, path: str, parent: QWidget = None, include_path: bool = False,
                     scan_type: str = "local", sub_url: str = "", location: list[int | str] = None) -> None:
    """
    :param target_widget: 要刷新的QComboBox控件
    :param path: 本地路径或URL路径
    :param parent: 父窗口，显示错误弹窗时使用
    :param include_path: 是否包含完整路径（仅限本地扫描）
    :param scan_type: 扫描类型，"local" 或 "url"
    :param sub_url: 当扫描类型为url时，它会被追加到path后面
    :param location: 定位数据位置的路径列表，列表项可以是整数（视为索引）或字符串（视为键）
    :return: None
    """
    logger.info(f"尝试刷新：{target_widget.objectName()}")
    scan_res = utils.get_list(path=path, include_path=include_path,
                              scan_type=scan_type, sub_url=sub_url, location=location)
    # 更新combobox
    if scan_res[0] == 0:
        # 检查类型
        for item in scan_res[1]:
            if not isinstance(item, str):
                target_widget.setPlaceholderText("类型错误")
                logger.error(f"列表项必须为字符串，发现类型: {type(item)}, 值: {item}")
                show_message_box(parent, "错误", f"列表项必须为字符串，发现类型: {type(item)}, 值: {item}",
                                 QMessageBox.Icon.Critical)
                return
        # 记住选择并更新
        set_widget_items(target_widget, scan_res[1], True)
        logger.info(f"已刷新：{target_widget.objectName()}")
        return
    else:
        target_widget.setCurrentIndex(-1)
        target_widget.setPlaceholderText("刷新失败")
        logger.error(f"刷新 {target_widget.objectName()} 失败：{scan_res[1]}")
        show_message_box(parent, "错误", scan_res[1], QMessageBox.Icon.Critical)
        return


def remove_entry(target_widget: QListWidget, mode: str, parent: QWidget, pattern: str = "",
                 substring: str | list = "", remove_type: str = "generic"):
    """
    从ListWidget中移除项，若此项对应一个文件系统中的路径，还可选择是否将其移动到回收站。

    可用移除模式：
    delete_all - 移除并删除全部
    delete_selected - 移除并删除选中项
    delete_matched - 移除并删除匹配项
    remove_all - 移除所有项
    remove_selected - 移除选中项
    remove_matched - 移除匹配项

    可用子串移除模式：
    generic - 全部移除
    prefix - 移除前缀
    suffix - 移除后缀

    :param target_widget: 要移除项的ListWidget
    :param mode: 移除模式
    :param parent: 父窗口，用于显示消息框
    :param pattern: 用于匹配的正则表达式项
    :param substring: 在删除前，从项的文本中移除的子串
    :param remove_type: 移除子串的模式
    :return:
    """
    # 待处理的项
    if mode in ["delete_all", "remove_all"]:
        items_to_process = [target_widget.item(i) for i in range(target_widget.count())]
    elif mode in ["delete_selected", "remove_selected"]:
        items_to_process = target_widget.selectedItems()
    elif mode in ["delete_matched", "remove_matched"]:
        items_to_process = [
            target_widget.item(i)
            for i in range(target_widget.count())
            if re.search(pattern, target_widget.item(i).text())
        ]
    else:
        logger.error(f"未知的移除模式：{mode}")
        show_message_box(parent, "内部错误", f"未知的模式: {mode}", QMessageBox.Icon.Warning)
        return

    if not items_to_process:
        show_message_box(parent, "提示", "没有匹配的项可供处理", QMessageBox.Icon.Information)
        return

    deleted_files_count = 0
    delete_error_occurred = False

    # 删除文件逻辑
    if mode.startswith("delete_"):
        paths_to_delete = [
            os.path.normpath(utils.remove_substring(item.text(), substring, remove_type))
            for item in items_to_process
        ]

        try:
            logger.info(f"正在删除 {len(paths_to_delete)} 项文件")
            send2trash.send2trash(paths_to_delete)
            deleted_files_count = len(paths_to_delete)
            logger.info(f"成功移动 {deleted_files_count} 项到回收站")
        except Exception as e:
            delete_error_occurred = True
            logger.error(f"Error moving files to trash: {e}")
            show_message_box(parent, "删除错误", f"移动文件到回收站时出错:\n{e}", QMessageBox.Icon.Critical)

    # 移除列表项逻辑
    rows_to_remove = sorted([target_widget.row(item) for item in items_to_process], reverse=True)
    removed_items_count = len(rows_to_remove)

    for row in rows_to_remove:
        target_widget.takeItem(row)

    logger.info(f"已从 {target_widget.objectName()} 中移除 {removed_items_count} 项")

    # 反馈总结
    if not delete_error_occurred:
        msg_parts = []
        if removed_items_count > 0:
            msg_parts.append(f"已从列表中移除 {removed_items_count} 项")
        if deleted_files_count > 0:
            msg_parts.append(f"已将 {deleted_files_count} 个文件移动到回收站")

        full_msg = "\n".join(msg_parts) if msg_parts else "操作完成，无变动"
        show_message_box(parent, "操作完成", full_msg, QMessageBox.Icon.Information)


def add_double_click_open(item, parent: QWidget, substring: str | list, remove_type: str):
    """
    双击打开文件。
    """
    display_path = item.text()
    real_path = utils.remove_substring(display_path, substring, remove_type)

    try:
        os.startfile(real_path)
        logger.info(f"已打开 {display_path} -> {real_path}")
    except Exception as e:
        logger.error(f"无法打开 {real_path}: {e}")
        show_message_box(parent, "打开失败", f"无法打开文件:\n{display_path}\n\n错误信息:\n{e}",
                         QMessageBox.Icon.Critical)


def show_context_menu(list_widget, position, menu_items: List[Tuple[str, Callable[[], None]]]):
    """
    通用的右键菜单显示函数
    :param list_widget: 目标列表控件
    :param position: 鼠标点击位置
    :param menu_items: 菜单项列表，格式为 [("菜单名", 回调函数), ...]
    """
    item = list_widget.itemAt(position)
    if not item:
        return

    list_widget.setCurrentItem(item)
    context_menu = QMenu(list_widget)

    for text, callback in menu_items:
        action = context_menu.addAction(text)
        action.triggered.connect(callback)

    context_menu.exec(list_widget.mapToGlobal(position))