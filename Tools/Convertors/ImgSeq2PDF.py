import os
import re
from collections import defaultdict
from typing import List, Dict, TypedDict, Generator

import fitz
from send2trash import send2trash

from Tools.Utils import utils


class SequenceInfo(TypedDict):
    """表示图像序列信息的类型定义"""
    folder: str
    sequence: List[str]
    all_files: List[str]
    has_subfolder: bool


def _process_folder(dirpath: str, dirnames: List[str], filenames: List[str]) -> List[SequenceInfo]:
    """
    处理单个文件夹中的图像序列，识别并分组序列文件。

    :param dirpath: 当前文件夹的路径
    :param dirnames: 当前文件夹下的子文件夹名称列表
    :param filenames: 当前文件夹下的文件名称列表
    :return: 包含识别到的图像序列信息的字典列表
    """
    sequence_groups: Dict[tuple, List[tuple]] = defaultdict(list)
    IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.webp', '.ico'}

    # 正则表达式，用于匹配文件名中的前缀、数字和后缀
    pattern = re.compile(r"^(.*?)(\d+)(\.[^.]+)$")

    for filename in filenames:
        match = pattern.match(filename)
        if match:
            prefix, number_str, extension = match.groups()

            #检查扩展名
            if extension.lower() not in IMAGE_EXTENSIONS:
                continue

            try:
                number = int(number_str)
                full_path = os.path.join(dirpath, filename)
                # 将 (数字, 完整路径) 添加到对应的组
                sequence_groups[(prefix, extension)].append((number, full_path))
            except ValueError:
                # 如果数字部分无法转换为整数，则跳过
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

    :param root_folder: 要扫描的根文件夹路径
    :param recursive: 是否递归查找子文件夹，默认为 False
    :return: 包含所有找到的序列信息字典的列表
    """
    all_sequences_info: List[SequenceInfo] = []

    if recursive:
        for dirpath, dirnames, filenames in os.walk(root_folder):
            all_sequences_info.extend(_process_folder(dirpath, dirnames, filenames))
    else:
        dirpath = root_folder
        dirnames = [d for d in os.listdir(dirpath) if os.path.isdir(os.path.join(dirpath, d))]
        filenames = [f for f in os.listdir(dirpath) if os.path.isfile(os.path.join(dirpath, f))]
        all_sequences_info.extend(_process_folder(dirpath, dirnames, filenames))

    return all_sequences_info


def create_pdf_from_sequence(sequence_info: SequenceInfo) -> str | None:
    """
    将一个图像序列转换为一个PDF文件。

    PDF保存在序列所在文件夹上一级，并以文件夹名命名。
    如果同名文件已存在，则在文件名末尾添加序号。

    :param sequence_info: 包含序列信息的字典
    :return: 若成功则返回None，失败则返回错误信息
    """
    folder_path = sequence_info["folder"]
    image_paths = sequence_info["sequence"]

    # 确定输出PDF的路径和名称
    parent_dir = os.path.dirname(folder_path)
    folder_name = os.path.basename(folder_path)
    output_pdf_path = utils.get_unique_filename(os.path.join(parent_dir, f"{folder_name}.pdf"))

    with fitz.open() as pdf_document:
        try:
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
            return None
        except Exception as e:
            return f"[图像序列转PDF] 无法创建PDF: {str(e)}"



def cleanup_original_files(sequence_info: SequenceInfo, send_to_trash_flag: bool) -> str:
    """
    根据用户选择和文件夹内容，将原文件或文件夹发送到回收站。

    :param sequence_info: 包含序列信息的字典
    :param send_to_trash_flag: 是否将文件发送到回收站的标志
    :return: 执行状态
    """
    if not send_to_trash_flag:
        return "[图像序列转PDF] 跳过清理"

    folder_path = sequence_info["folder"]
    sequence_files = set(sequence_info["sequence"])
    all_items_in_folder = set(sequence_info["all_files"])
    has_subfolder = sequence_info["has_subfolder"]

    # 序列文件是文件夹的所有内容，且没有子文件夹 - 直接删除父文件夹更快
    if sequence_files == all_items_in_folder and not has_subfolder:
        try:
            send2trash(os.path.normpath(folder_path))
            return "[图像序列转PDF] 删除成功"
        except Exception as e:
            return f"[图像序列转PDF] 无法删除文件夹：{str(e)}"
    else:
        try:
            send2trash([os.path.normpath(i) for i in sequence_info["sequence"]])
            return "[图像序列转PDF] 删除成功"
        except Exception as e:
            return f"[图像序列转PDF] 无法删除序列：{str(e)}"


def process_image_sequences(target_folder: str, recursive: bool = False,
                            send_to_trash: bool = False) -> Generator[tuple[int, str], None, None]:
    """
    处理图像序列转PDF的主函数。

    查找指定目录下的图像序列，将其转换为PDF，并根据参数清理原文件。

    :param target_folder: 目标文件夹路径
    :param recursive: 是否递归查找子文件夹，默认为 False
    :param send_to_trash: 处理完成后是否将原图像文件发送到回收站，默认为 False
    :return: 生成器，第一项为进度（0~100），第二项为日志信息，进度按序列数量计算
    """
    # 查找所有图像序列
    sequences = find_image_sequences(target_folder, recursive)
    seq_length = len(sequences)

    if not sequences:
        yield 0, "[图像序列转PDF] 未找到任何符合条件的图像序列"
        return None

    # 处理每个序列
    for i, seq_info in enumerate(sequences, 1):
        progress = int((i / seq_length) * 100)

        # 创建 PDF
        try:
            res = create_pdf_from_sequence(seq_info)
            yield progress, res
            if res:
                continue
        except Exception as e:
            yield progress, f"[图像序列转PDF] 无法处理序列 {i}：{str(e)}"
            continue

        # 清理原文件
        cleanup_original_files(seq_info, send_to_trash)

    yield 100, "[图像序列转PDF] 所有任务已完成！"
    return None
