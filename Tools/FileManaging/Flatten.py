import os
import shutil
from typing import Generator

import send2trash

from Core import log_manager
from Tools.Utils import utils

logger = log_manager.get_logger(__name__)


def is_single_file_folder(folder: str) -> bool:
    """
    检查文件夹是否只包含一个文件且无子文件夹

    Args:
        folder: 文件夹路径

    Returns:
        bool: 如果是单文件文件夹则返回 True，否则返回 False
    """
    items = os.listdir(folder)
    files = [item for item in items if os.path.isfile(os.path.join(folder, item))]
    subfolders = [item for item in items if os.path.isdir(os.path.join(folder, item))]
    return len(files) == 1 and len(subfolders) == 0


def _lift_single_file_up(folder_path: str) -> bool:
    """
    展平单文件文件夹，将文件移动到父目录

    Args:
        folder_path: 待处理的文件夹路径

    Returns:
        bool: 如果执行了展平操作则返回 True，否则返回 False
    """
    if not is_single_file_folder(folder_path):
        return False

    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    file_to_move = files[0]

    parent_folder = os.path.dirname(folder_path)
    new_file_name = os.path.basename(folder_path)
    file_extension = os.path.splitext(file_to_move)[1]

    # 构建目标路径
    candidate_path = os.path.join(parent_folder, new_file_name + file_extension)
    new_file_path = utils.get_unique_filename(candidate_path)

    shutil.move(os.path.join(folder_path, file_to_move), new_file_path)
    send2trash.send2trash(folder_path)

    logger.info(f"已移动文件 '{file_to_move}' 到父文件夹")
    logger.info(f"    该文件已重命名为 '{os.path.basename(new_file_path)}'")
    logger.info(f"    删除文件夹 '{folder_path}'")

    return True


def process_folder(folder_path: str) -> Generator[None, None, None]:
    """
    递归处理文件夹，执行展平操作

    Args:
        folder_path: 文件夹路径

    Yields:
        None: 用于控制流程的生成器，不包含额外信息
    """
    # 如果当前是单文件文件夹，直接展平并停止处理该分支
    if _lift_single_file_up(folder_path):
        yield
        return

    # 如果当前文件夹结构较复杂，遍历处理子文件夹
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):
            yield from process_folder(item_path)

    # 子文件夹处理完毕后，当前文件夹可能变为单文件文件夹
    if _lift_single_file_up(folder_path):
        yield


def main(folder_path: str) -> Generator[None, None, None]:
    """
    扫描指定路径下的所有顶层目录并递归展平

    Args:
        folder_path: 根文件夹路径

    Yields:
        None: 用于控制流程的生成器，不包含其他信息
    """
    # 获取指定路径下所有的顶层目录
    top_level_dirs = [os.path.join(folder_path, d) for d in os.listdir(folder_path)
                      if os.path.isdir(os.path.join(folder_path, d))]

    logger.info(f"开始扫描路径: {folder_path}")

    for dir_path in top_level_dirs:
        yield from process_folder(dir_path)
