import os, re
from typing import List, Tuple, Callable

import send2trash
from PySide6.QtWidgets import QComboBox, QPlainTextEdit, QMenu, QListWidget

from Tools.Utils import utils

def refresh_combobox(target_widget: QComboBox, path: str, error_widget: QPlainTextEdit, include_path: bool = False,
                     scan_type: str = "local", sub_url: str = "", location: list[int | str] = None) -> None:
    """
    :param target_widget: 要刷新的QComboBox控件
    :param path: 本地路径或URL路径
    :param error_widget: 出现错误时，将详细的错误信息追加到此处
    :param include_path: 是否包含完整路径（仅限本地扫描）
    :param scan_type: 扫描类型，"local" 或 "url"
    :param sub_url: 当扫描类型为url时，它会被追加到path后面
    :param location: 定位数据位置的路径列表，列表项可以是整数（视为索引）或字符串（视为键）
    :return:
    """
    scan_res = utils.get_list(path = path, include_path=include_path,
                              scan_type=scan_type, sub_url=sub_url, location=location)
    # 更新combobox
    if scan_res[0] == 0:
        # 检查类型
        for item in scan_res[1]:
            if not isinstance(item, str):
                target_widget.setPlaceholderText("数据包含非字符串")
                error_widget.appendPlainText(f"列表项必须为字符串，发现类型: {type(item)}, 值: {item}")
                return
        # 记住选择并更新
        prev = target_widget.currentText()
        target_widget.clear()
        target_widget.addItems(scan_res[1])
        prev_str = prev if prev else ""
        target_widget.setCurrentText(prev_str) if prev_str and prev_str in scan_res[1] else target_widget.setCurrentIndex(0)
        return
    else:
        target_widget.setPlaceholderText("查找失败")
        error_widget.appendPlainText(scan_res[1])
        return


def set_list_widget_items(target_widget: QListWidget, lst: list[str]):
    target_widget.clear()
    target_widget.addItems(lst)


def remove_entry(target_widget: QListWidget, mode: str, log_widget: QPlainTextEdit, pattern: str = "",
                 substring: str | list = "", remove_type: str = "generic"):
    """
    从ListWidget中移除项，若此项对应一个文件系统中的路径，还可选择是否将其移动到回收站

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
    :param log_widget: 日志输出目标
    :param pattern: 用于匹配的正则表达式项
    :param substring: 在删除前，从项的文本中移除的子串，例如此参数为[test]，则[test]1.txt会被当成1.txt删除，此参数不会修改ListWidget
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
        log_widget.appendPlainText(f"未知的模式: {mode}")
        return

    if not items_to_process:
        return

    # 删除文件
    if mode.startswith("delete_"):
        paths_to_delete = [
            os.path.normpath(utils.remove_substring(item.text(), substring, remove_type))
            for item in items_to_process
        ]

        try:
            send2trash.send2trash(paths_to_delete)
            log_widget.appendPlainText(f"已将 {len(paths_to_delete)} 个文件移动到回收站。")
        except Exception as e:
            log_widget.appendPlainText(f"移动到回收站时出错: {e}")

    # 移除项
    rows_to_remove = sorted([target_widget.row(item) for item in items_to_process], reverse=True)

    for row in rows_to_remove:
        target_widget.takeItem(row)

    log_widget.appendPlainText(f"已从列表中移除 {len(rows_to_remove)} 项")


def add_double_click_open(item, log_widget: QPlainTextEdit, substring: str | list, remove_type: str):
    display_path = item.text()
    real_path = utils.remove_substring(display_path, substring, remove_type)

    try:
        os.startfile(real_path)
        log_widget.appendPlainText(f"已打开：{display_path}")
    except Exception as e:
        log_widget.appendPlainText(f"打开失败：{e}")


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
