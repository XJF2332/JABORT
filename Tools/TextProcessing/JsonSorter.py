import json
import os.path

import charset_normalizer

from Core import log_manager

logger = log_manager.get_logger(__name__)


def sort_dict_recursive(d):
    logger.debug(f"正在排序：{d}")
    if isinstance(d, dict):
        return {k: sort_dict_recursive(v) for k, v in sorted(d.items())}
    elif isinstance(d, list):
        return [sort_dict_recursive(item) for item in d]
    else:
        return d


def process(json_path):
    """
    对输入的json文件进行排序

    状态码：
    0 - 成功
    1 - 输入的路径为空或不存在
    2 - 没有权限读取文件
    3 - 其他读取错误
    4 - 没有权限写入文件
    5 - 其他写入错误

    Args:
        json_path: json文件路径

    Returns:
        包含状态码和错误信息（如果有的话）的元组
    """
    logger.info(f"排序文件：{json_path}")
    if not os.path.exists(json_path):
        logger.error(f"文件路径为空或不存在：{json_path}")
        return 1, "文件路径为空或不存在"
    # 检测编码
    with open(json_path, 'rb') as file:
        content_bytes = file.read()
    encoding_info = charset_normalizer.detect(content_bytes)
    logger.debug(f"检测到的编码信息：{encoding_info}")
    encoding = encoding_info['encoding'] if encoding_info else 'utf-8'
    # 读取文件
    try:
        with open(json_path, 'r', encoding=encoding) as f:
            logger.info("成功读取文件")
            doc = json.load(f)
    except PermissionError:
        logger.error("没有权限读取文件")
        return 2, f"没有权限读取文件：{json_path}"
    except Exception as e:
        logger.error(f"读取失败：{str(e)}")
        return 3, f"读取失败：{str(e)}"

    sorted_doc = sort_dict_recursive(doc)

    try:
        with open(json_path, 'w', encoding=encoding) as sorted_json:
            json.dump(sorted_doc, sorted_json, ensure_ascii=False, indent=4)
    except PermissionError:
        logger.error(f"没有权限写入文件：{json_path}")
        return 4, "没有权限写入文件"
    except Exception as e:
        logger.error(f"保存失败：{str(e)}")
        return 5, f"保存失败：{str(e)}"

    return 0, ""


def main(json_path: str):
    return process(json_path)
