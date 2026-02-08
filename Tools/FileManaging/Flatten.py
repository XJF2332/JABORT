import os
import shutil
from typing import Generator

import send2trash

from Core import log_manager
from Core.error_codes import ErrorCode
from Tools.Utils import utils

logger = log_manager.get_logger(__name__)


def _has_one_file(folder: str) -> tuple[ErrorCode, bool]:
    """
    检查文件夹是否只包含一个文件且无子文件夹，即满足被展平的要求

    Args:
        folder: 文件夹路径

    Returns:
        tuple[ErrorCode, bool]: 错误码和布尔值
    """
    try:
        if not os.path.exists(folder):
            return ErrorCode.InvalidPath, False

        items = os.listdir(folder)
        files = [item for item in items if os.path.isfile(os.path.join(folder, item))]
        subfolders = [item for item in items if os.path.isdir(os.path.join(folder, item))]

        result = len(files) == 1 and len(subfolders) == 0
        return ErrorCode.Success, result
    except PermissionError:
        logger.error(ErrorCode.NotPermitted.format(folder))
        return ErrorCode.NotPermitted, False
    except Exception as e:
        logger.error(f"检查文件夹结构时出错: {str(e)}")
        return ErrorCode.Unknown, False


def _lift_file(folder_path: str) -> tuple[ErrorCode, str]:
    """
    展平单文件文件夹，将文件移动到父目录

    Args:
        folder_path: 待处理的文件夹路径

    Returns:
        tuple[ErrorCode, str]: 错误码和消息/路径
    """
    # 检查结构
    code, is_single = _has_one_file(folder_path)
    if code != ErrorCode.Success:
        logger.error(code.generic)
        return code, ""
    elif not is_single:
        # 不满足条件，跳过，这不算错误
        logger.info(f"{folder_path} 不满足展平要求")
        return ErrorCode.FileSkipped, ""

    try:
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        if not files:
            return ErrorCode.FileSkipped, ""

        # 构建输出路径
        file_to_move = files[0]
        source_file_path = os.path.join(folder_path, file_to_move)
        candidate_path = os.path.join(
            os.path.dirname(folder_path), os.path.basename(folder_path) + os.path.splitext(file_to_move)[1]
        )
        new_file_path = utils.get_unique_filename(candidate_path)[1]

        # 移动文件
        shutil.move(source_file_path, new_file_path)
        logger.info(f"已移动文件 '{file_to_move}' 到 '{new_file_path}'")

        # 删除原文件夹
        try:
            send2trash.send2trash(folder_path)
            logger.info(f"    删除文件夹 '{folder_path}'")
        except Exception as e:
            logger.warning(f"文件已移动，但无法将原文件夹移入回收站: {str(e)}")
            return ErrorCode.TrashFailed, folder_path

        return ErrorCode.Success, new_file_path

    except PermissionError:
        logger.error(ErrorCode.NotPermitted.format(folder_path))
        return ErrorCode.NotPermitted, folder_path
    except OSError as e:
        logger.error(ErrorCode.CannotWriteFile.format(str(e)))
        return ErrorCode.CannotWriteFile, f"{folder_path} -> {str(e)}"
    except Exception as e:
        logger.error(f"展平操作异常: {str(e)}")
        return ErrorCode.FlattenFailed, str(e)


def process_folder(folder_path: str) -> Generator[tuple[ErrorCode, str], None, None]:
    """
    递归处理文件夹，执行展平操作

    Args:
        folder_path: 文件夹路径

    Yields:
        tuple[ErrorCode, str]: 错误码和当前处理的路径/消息
    """
    # 尝试作为单文件文件夹展平
    code, msg = _lift_file(folder_path)

    if code == ErrorCode.Success:
        # 成功展平，不再需要处理子项
        yield code, msg
        return
    elif code != ErrorCode.FileSkipped:
        # 发生了真正的错误（权限、IO等），报错并停止处理该分支
        yield code, msg
        return

    # 如果是因为"不满足单文件条件"而跳过，则继续遍历子文件夹
    try:
        # 使用 listdir 获取列表，避免在遍历过程中目录结构变化导致的问题
        items = os.listdir(folder_path)
    except OSError as e:
        yield ErrorCode.CannotReadFile, f"{folder_path}: {str(e)}"
        return

    for item in items:
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):
            yield from process_folder(item_path)

    # 子文件夹处理完毕后，当前文件夹可能变为单文件文件夹，再次尝试
    code, msg = _lift_file(folder_path)
    if code == ErrorCode.Success:
        yield code, msg
    elif code != ErrorCode.FileSkipped:
        yield code, msg


def main(folder_path: str) -> Generator[tuple[ErrorCode, str], None, None]:
    """
    扫描指定路径下的所有顶层目录并递归展平

    Args:
        folder_path: 根文件夹路径

    Yields:
        tuple[ErrorCode, str]: 错误码和处理结果
    """
    if not folder_path or not os.path.exists(folder_path):
        yield ErrorCode.InvalidPath, folder_path
        return

    try:
        # 获取指定路径下所有的顶层目录
        top_level_dirs = [os.path.join(folder_path, d) for d in os.listdir(folder_path)
                          if os.path.isdir(os.path.join(folder_path, d))]
    except Exception as e:
        yield ErrorCode.CannotReadFile, f"{folder_path}: {str(e)}"
        return

    logger.info(f"开始扫描路径: {folder_path}")

    if not top_level_dirs:
        logger.info("未找到顶层子文件夹")
        # 也可以视为 Success，只是没做任何事
        return

    for dir_path in top_level_dirs:
        yield from process_folder(dir_path)