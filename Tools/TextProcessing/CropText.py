import os

from charset_normalizer import from_path

from Core import log_manager
from Core.error_codes import ErrorCode
from Tools.Utils import utils

logger = log_manager.get_logger(__name__)


def crop_text_file(input_path: str, output_path: str = None, percentage: int = 50,
                   deduplicate: int = 2) -> tuple[ErrorCode, str]:
    """
    截取文本文件的后x%并保存

    Args:
        deduplicate: 去重模式，0 - 覆盖，1 - 跳过，2 - 保留两者（会添加序号）
        input_path: 源文件路径
        output_path: 输出文件路径。若为None，则自动生成
        percentage: 截取比例(0-100)，表示截取后x%的内容

    Returns:
        输出文件路径
    """
    # 验证参数
    logger.info(f"以 {percentage}% 截取 {input_path}")
    if not 0 <= percentage <= 100:
        logger.error(ErrorCode.InvalidRatio.format(f"{percentage}，（需要 0 ~ 100）"))
        return ErrorCode.InvalidRatio, ""
    if not input_path or not os.path.exists(input_path):
        logger.error(ErrorCode.InvalidPath.format(input_path))
        return ErrorCode.InvalidPath, ""

    # 生成输出路径
    if not output_path:
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        extension = os.path.splitext(input_path)[1]
        output_path = os.path.join(
            os.path.dirname(input_path),
            f"{base_name}_crop_{percentage}{extension}"
        )
        logger.debug(f"未提供输出路径，生成：{output_path}")

    # 去重
    if deduplicate == 1:
        logger.error(ErrorCode.FileExists.format(output_path))
        return ErrorCode.FileExists, ""
    else:
        output_path = utils.filename_deduplicate(deduplicate, output_path)

    # 读取源文件内容
    best_match = from_path(input_path).best()
    logger.debug(f"检测到的编码信息：{best_match.encoding}")
    try:
        with open(input_path, 'r', encoding=best_match.encoding) as f:
            lines = f.readlines()
            logger.info("已读取原文件")
    except Exception as e:
        logger.error(ErrorCode.CannotReadFile.format(str(e)))
        return ErrorCode.CannotReadFile, ""

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
        logger.error(ErrorCode.CannotWriteFile.format(str(e)))
        return ErrorCode.CannotWriteFile, ""

    return ErrorCode.Success, output_path
