import os
import send2trash
import shutil
from Tools.Utils import utils


def is_single_file_folder(folder):
    items = os.listdir(folder)
    files = [item for item in items if os.path.isfile(os.path.join(folder, item))]
    subfolders = [item for item in items if os.path.isdir(os.path.join(folder, item))]
    return len(files) == 1 and len(subfolders) == 0


def _lift_single_file_up(folder_path):
    """
    [内部辅助函数] 返回日志生成器
    """
    if not is_single_file_folder(folder_path):
        return

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

    yield f"[旧版展平] 已移动文件 '{file_to_move}' 到父文件夹"
    yield f"    该文件已重命名为 '{os.path.basename(new_file_path)}'"
    yield f"    删除文件夹 '{folder_path}'。"


def process_folder(folder_path):
    """
    递归处理文件夹，并 yield 所有的日志
    """
    # 如果当前是单文件文件夹，直接展平并停止处理该分支
    # 使用 list() 来消费生成器，如果有日志返回则说明进行了展平
    if list(_lift_single_file_up(folder_path)):
        return

    # 如果当前文件夹结构较复杂，遍历处理子文件夹
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):
            # 使用 yield from 将子文件夹的日志传递上去
            yield from process_folder(item_path)

    # 子文件夹处理完毕后，当前文件夹可能变为单文件文件夹
    yield from _lift_single_file_up(folder_path)


def main(folder_path: str):
    # 获取指定路径下所有的顶层目录
    top_level_dirs = [os.path.join(folder_path, d) for d in os.listdir(folder_path)
                      if os.path.isdir(os.path.join(folder_path, d))]

    yield f"[旧版展平] 开始扫描路径: {folder_path}"

    for dir_path in top_level_dirs:
        yield from process_folder(dir_path)
