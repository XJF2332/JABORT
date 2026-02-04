import os, re
from typing import Any, Tuple

import requests

from Core import log_manager
from Core.error_codes import ErrorCode

logger = log_manager.get_logger(__name__)


def remove_substring(source_string: str, substring: str | list, remove_type: str) -> str:
    """
    移除字符串中的字串
    :param source_string: 源字符串，可以是一个字符串或一个字符串列表
    :param substring: 子串
    :param remove_type: 方式，接受prefix、suffix和generic
    :return: 处理后的字符串
    """
    # 对单个字符串执行移除
    def remove_single(original: str, sub: str):
        # 前缀模式
        if remove_type == "prefix":
            if original.startswith(sub):
                return original[len(sub):]
            else:
                return original
        # 普通模式
        elif remove_type == "generic":
            return original.replace(sub, "")
        # 后缀模式
        elif remove_type == "suffix":
            if original.endswith(sub):
                return original[:len(original) - len(sub)]
            else:
                return original
        # 未知模式不做处理
        else:
            return original
    # 字符串 - 直接移除
    if type(substring) == str:
        return remove_single(source_string, substring)
    # 列表 - 逐个移除
    elif type(substring) == list:
        removed = source_string
        for item in substring:
            removed = remove_single(removed, item)
        return removed
    # 其他类型不处理
    else:
        return source_string


def get_unique_filename(path: str) -> tuple[ErrorCode, str]:
    """
    获取唯一的文件名，为重名的文件添加序号
    :param path: 要处理的路径
    :return: 唯一文件路径
    """
    logger.debug(f"为 {path} 获取唯一的文件名")
    dir_path = os.path.dirname(path) or '.'
    filename, ext = os.path.splitext(os.path.basename(path))

    # 文件不存在 - 没有重名
    if not os.path.exists(path):
        logger.debug("没有检测到重复文件")
        return ErrorCode.Success, path
    # 文件存在 - 有重名
    files = os.listdir(dir_path)
    pattern_str = f"^{re.escape(filename)}_(\\d+){re.escape(ext)}$"
    logger.debug(f"检测到重复文件，构建正则表达式：{pattern_str}")
    pattern = re.compile(pattern_str)

    indices = [int(match.group(1)) for f in files if (match := pattern.match(f))]
    logger.debug(f"检测到的序列：{indices}")
    max_index = max(indices, default=0)

    new_index = max_index + 1
    new_filename = f"{filename}_{new_index}{ext}"
    logger.debug(f"唯一文件名：{new_filename}")

    return ErrorCode.Success, os.path.join(dir_path, new_filename)


def filename_deduplicate(mode: int, path: str) -> tuple[ErrorCode, str]:
    """
    对get_unique_filename的简单封装，以适配UI的三种去重模式

    可能的错误码：
    Success
    FileSkipped

    Args:
        mode: 去重模式，0 - 覆盖，1 - 跳过，2 - 保留两者（会添加序号）
        path: 要去重的路径

    Returns:
        （错误码，去重后的文件名）
    """
    logger.debug(f"使用 {mode} 进行文件名去重")
    # 覆盖模式 或 跳过模式但文件当前不存在 - 输入本身
    if mode == 0 or (mode == 1 and not os.path.exists(path)):
        return ErrorCode.Success, path
    # 保留两者 - 去重
    elif mode == 2:
        return get_unique_filename(path)
    # 跳过模式且文件当前存在 或 其他模式 - 返回 None
    else:
        return ErrorCode.FileSkipped, path


def get_list(path: str, include_path: bool = False, scan_type: str = "local",
             sub_url: str = "", location: Any = None) -> Tuple[int, str | list[str]]:
    """
    从路径获取列表
    :param path: 路径
    :param include_path: 返回的列表中是否要包含路径
    :param scan_type: 扫描模式，"local" 或 "url"
    :param sub_url: url 模式下，将要追加到输入 url 后的部分
    :param location: url 模式下，数据的位置
    :return: 包含运行状态和结果的元组
    """
    if scan_type == "local":
        if not path or not os.path.exists(path):
            return 1, f"路径为空或未找到路径：{path}"
        # 决定要不要包含路径
        lst = [os.path.join(path, item) for item in os.listdir(path)] if include_path else os.listdir(path)
        return 0, lst
    elif scan_type == "url":
        try:
            full_url = f"{path}{sub_url}" if sub_url else path
            response = requests.get(full_url, timeout=10)
            response.raise_for_status()
            data = response.json()
            # 未提供数据位置
            if location is None:
                res = (0, data) if isinstance(data, list) else (1, "找到的数据不是列表类型")
                return res
            # 提供了数据位置
            else:
                current_data = data
                # 定位数据
                for key in location:
                    # 当前目标项为整数 - 认为是索引
                    if isinstance(key, int) and isinstance(current_data, list):
                        if 0 <= key < len(current_data):
                            current_data = current_data[key]
                        else:
                            return 1, f"无法定位数据：列表索引 {key} 超出范围"
                    # 当前目标项为字符串 - 认为是键
                    elif isinstance(key, str) and isinstance(current_data, dict):
                        if key in current_data:
                            current_data = current_data[key]
                        else:
                            return 1, f"无法定位数据：键'{key}'不存在于数据中"
                    else:
                        return 1, f"无法访问键'{key}'，当前类型为{type(current_data)}"
                # 返回值
                res = (0, current_data) if isinstance(current_data, list) else \
                    (1, f"定位到的的数据不是列表类型，当前类型为{type(current_data)}")
                return res
        # 错误处理
        except requests.exceptions.RequestException as e:
            return 1, f"网络请求失败: {str(e)}"
        except ValueError as e:
            return 1, f"JSON解析失败: {str(e)}"
        except Exception as e:
            return 1, f"获取数据时出错: {str(e)}"
    else:
        return 1, f"不受支持的扫描类型：{scan_type}"