import os

from charset_normalizer import from_path

from Core import log_manager

logger = log_manager.get_logger(__name__)


def crop_text_file(source_path, output_path=None, percentage=50) -> tuple[int, str]:
    """
    截取文本文件的后x%并保存

    状态码
    1 - 截取比例错误
    2 - 原文件不存在
    3 - 不能覆盖已存在的文件
    4 - 无法读取文件
    5 - 无法输出文件

    Args:
        source_path (str): 源文件路径
        output_path (str, optional): 输出文件路径。若为None，则自动生成
        percentage (float): 截取比例(0-100)，表示截取后x%的内容

    Returns:
        第一项为状态（0为成功），第二项为输出文件路径或错误信息
    """
    # 验证参数
    logger.info(f"以 {percentage}% 截取 {source_path}")
    if not 0 <= percentage <= 100:
        logger.error(f"截取比例必须在0-100之间，当前比例：{percentage}")
        return 1, "截取比例必须在0-100之间"

    if not source_path or not os.path.exists(source_path):
        logger.error(f"输入路径为空或不存在: {source_path}")
        return 2, "输入路径为空或不存在"

    # 生成输出路径
    if not output_path:
        base_name = os.path.splitext(os.path.basename(source_path))[0]
        extension = os.path.splitext(source_path)[1]
        output_path = os.path.join(
            os.path.dirname(source_path),
            f"{base_name}_crop_{percentage}{extension}"
        )
        logger.debug(f"未提供输出路径，生成：{output_path}")

    # 检查输出文件是否已存在且不为空
    if os.path.exists(output_path):
        file_size = os.path.getsize(output_path)
        if file_size > 0:
            logger.error("不能覆盖已存在的文件")
            return 3, "不能覆盖已存在的文件"

    # 读取源文件内容
    best_match = from_path(source_path).best()
    logger.debug(f"检测到的编码信息：{best_match.encoding}")
    try:
        with open(source_path, 'r', encoding=best_match.encoding) as f:
            lines = f.readlines()
            logger.info("已读取原文件")
    except Exception as e:
        logger.error(f"读取文件失败：{str(e)}")
        return 4, f"读取文件失败：{str(e)}"

    # 截取文本
    if percentage == 0:
        cropped_lines = []
    elif percentage == 100:
        cropped_lines = lines
    else:
        start_index = int(len(lines) * (100 - percentage) / 100)
        cropped_lines = lines[start_index:]

    # 写入输出文件
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.writelines(cropped_lines)
            logger.info(f"已将截取后的文件写入到 {output_path}")
    except Exception as e:
        logger.error(f"写入文件失败：{str(e)}")
        return 5, f"写入文件失败：{str(e)}"

    return 0, output_path
