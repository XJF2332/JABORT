import os
import re
from collections import defaultdict
from typing import List, Dict, TypedDict, Generator

import fitz
from send2trash import send2trash

from Tools.Utils import utils
from Core import log_manager

logger = log_manager.get_logger(__name__)


class SequenceInfo(TypedDict):
    """表示图像序列信息的类型定义"""
    folder: str
    sequence: List[str]
    all_files: List[str]
    has_subfolder: bool


def _process_folder(dirpath: str, dirnames: List[str], filenames: List[str]) -> List[SequenceInfo]:
    """
    处理单个文件夹中的图像序列，识别并分组序列文件。
    """
    sequence_groups: Dict[tuple, List[tuple]] = defaultdict(list)
    IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.webp', '.ico'}

    # 正则表达式，用于匹配文件名中的前缀、数字和后缀
    pattern = re.compile(r"^(.*?)(\d+)(\.[^.]+)$")

    for filename in filenames:
        match = pattern.match(filename)
        if match:
            prefix, number_str, extension = match.groups()

            # 检查扩展名
            if extension.lower() not in IMAGE_EXTENSIONS:
                continue

            try:
                number = int(number_str)
                full_path = os.path.join(dirpath, filename)
                # 将 (数字, 完整路径) 添加到对应的组
                sequence_groups[(prefix, extension)].append((number, full_path))
            except ValueError:
                continue

    sequences: List[SequenceInfo] = []

    # 检查每个分组，如果文件数量大于1，则认为是一个序列
    for _, files in sequence_groups.items():
        if len(files) > 1:
            # 按数字从小到大排序
            files.sort(key=lambda x: x[0])

            # 提取排序后的文件路径
            sequence_paths = [path for num, path in files]

            # 构建所需字典的 'all_files' 部分
            all_files_in_dir = [os.path.join(dirpath, f) for f in filenames] + \
                               [os.path.join(dirpath, d) for d in dirnames]

            sequence_info: SequenceInfo = {
                "folder": dirpath,
                "sequence": sequence_paths,
                "all_files": all_files_in_dir,
                "has_subfolder": bool(dirnames)
            }
            sequences.append(sequence_info)

    return sequences


def find_image_sequences(root_folder: str, recursive: bool = False) -> List[SequenceInfo]:
    """
    查找指定文件夹及其子文件夹（可选）中的所有图像序列。
    """
    logger.debug(f"正在扫描图像序列: {root_folder}, 递归: {recursive}")
    all_sequences_info: List[SequenceInfo] = []

    if recursive:
        for dirpath, dirnames, filenames in os.walk(root_folder):
            all_sequences_info.extend(_process_folder(dirpath, dirnames, filenames))
    else:
        dirpath = root_folder
        if os.path.isdir(dirpath):
            dirnames = [d for d in os.listdir(dirpath) if os.path.isdir(os.path.join(dirpath, d))]
            filenames = [f for f in os.listdir(dirpath) if os.path.isfile(os.path.join(dirpath, f))]
            all_sequences_info.extend(_process_folder(dirpath, dirnames, filenames))

    logger.info(f"扫描完成，共找到 {len(all_sequences_info)} 个图像序列")
    return all_sequences_info


def create_pdf_from_sequence(sequence_info: SequenceInfo) -> int:
    """
    将一个图像序列转换为一个PDF文件。

    :return: 0 表示成功，1 表示失败
    """
    folder_path = sequence_info["folder"]
    image_paths = sequence_info["sequence"]

    # 确定输出PDF的路径和名称
    parent_dir = os.path.dirname(folder_path)
    folder_name = os.path.basename(folder_path)

    # 简单的防御性检查，防止路径错误
    if not parent_dir or not folder_name:
        logger.error(f"路径解析错误: {folder_path}")
        return 1

    output_pdf_path = utils.get_unique_filename(os.path.join(parent_dir, f"{folder_name}.pdf"))

    logger.debug(f"正在创建PDF: {output_pdf_path}, 源文件数: {len(image_paths)}")

    try:
        with fitz.open() as pdf_document:
            # 追加图像
            for img_path in image_paths:
                img_doc = fitz.open(img_path)
                pdf_bytes = img_doc.convert_to_pdf()
                img_pdf = fitz.open("pdf", pdf_bytes)
                pdf_document.insert_pdf(img_pdf)
                img_pdf.close()
                img_doc.close()
            # 保存 PDF
            pdf_document.save(output_pdf_path)

        logger.info(f"成功创建PDF: {output_pdf_path}")
        return 0
    except Exception as e:
        logger.error(f"无法创建PDF ({folder_name}): {str(e)}")
        return 1


def cleanup_original_files(sequence_info: SequenceInfo, send_to_trash_flag: bool) -> int:
    """
    根据用户选择和文件夹内容，将原文件或文件夹发送到回收站。

    :return: 0 表示成功或跳过，1 表示失败
    """
    if not send_to_trash_flag:
        logger.debug("跳过清理：未启用发送到回收站")
        return 0

    folder_path = sequence_info["folder"]
    sequence_files = set(sequence_info["sequence"])
    all_items_in_folder = set(sequence_info["all_files"])
    has_subfolder = sequence_info["has_subfolder"]

    # 序列文件是文件夹的所有内容，且没有子文件夹 - 直接删除父文件夹更快
    if sequence_files == all_items_in_folder and not has_subfolder:
        try:
            norm_path = os.path.normpath(folder_path)
            send2trash(norm_path)
            logger.info(f"文件夹已移至回收站: {norm_path}")
            return 0
        except Exception as e:
            logger.error(f"无法删除文件夹 ({folder_path}): {str(e)}")
            return 1
    else:
        try:
            files_to_trash = [os.path.normpath(i) for i in sequence_info["sequence"]]
            send2trash(files_to_trash)
            logger.info(f"序列文件已移至回收站，共 {len(files_to_trash)} 个文件")
            return 0
        except Exception as e:
            logger.error(f"无法删除序列文件: {str(e)}")
            return 1


def process_image_sequences(target_folder: str, recursive: bool = False,
                            send_to_trash: bool = False) -> Generator[int, None, None]:
    """
    处理图像序列转PDF的主函数。

    :return: 进度生成器 (Yields int: 0-100)
    """
    # 查找所有图像序列
    sequences = find_image_sequences(target_folder, recursive)
    seq_length = len(sequences)

    if not sequences:
        logger.warning("未找到任何符合条件的图像序列")
        yield 100
        return

    # 处理每个序列
    for i, seq_info in enumerate(sequences, 1):
        progress = int((i / seq_length) * 100)

        # 创建 PDF
        result_code = create_pdf_from_sequence(seq_info)

        if result_code != 0:
            # 如果创建失败，跳过后续清理步骤，继续下一个序列
            logger.warning(f"序列 {i} 处理失败，跳过清理")
            yield progress
            continue

        # 清理原文件
        cleanup_original_files(seq_info, send_to_trash)

        yield progress

    return