import glob
import os

from PIL import Image

from Tools.Utils import utils
from Core import log_manager

logger = log_manager.get_logger(__name__)


def convert_single(path: str, quality: int, preserve_metadata: bool, deduplicate: int) -> int:
    """
    转换单个图像文件

    转换状态：
    0 - 成功
    1 - 跳过

    :param path: 图像路径
    :param quality: 质量
    :param preserve_metadata: 保留元数据
    :param deduplicate: 去重模式，0 - 覆盖，1 - 跳过，2 - 保留两者（会添加序号）
    :return: 状态码
    """
    logger.debug(f"正在转换：{path}")
    with Image.open(path) as image:
        logger.debug(f"图像模式：{image.mode}")
        if 'A' in image.mode:
            image = image.convert('RGB')

        # 新图像路径
        new_path = path.replace("png", "jpg")
        if new_path.endswith(".jpg"):
            pass
        else:
            new_path = new_path + ".jpg"

        # 去重
        logger.debug(f"去重模式：{deduplicate}")
        if deduplicate == 1 and os.path.exists(new_path):
            logger.info(f"已跳过 {new_path} ，因为其已存在")
            return 1
        elif deduplicate == 2:
            new_path = utils.get_unique_filename(new_path)
            logger.debug(f"唯一路径：{new_path}")

        # 转换
        if preserve_metadata:
            metadata = image.info
            image.save(new_path, 'JPEG', quality=quality, metadata=metadata)
        else:
            image.save(new_path, 'JPEG', quality=quality)

        logger.info(f"已转换 {new_path}")
        return 0


def convert_batch(paths: list, quality: int, preserve_metadata: bool, deduplicate: int):
    """
    对输入的路径列表进行批量转换

    状态码：
    0 - 此项成功
    1 - 此项被跳过
    10 - 此图像不存在
    20 - 此项失败

    :param paths: 所有图像文件路径的列表
    :param quality: 质量
    :param preserve_metadata: 保留元数据
    :param deduplicate: 去重模式，0 - 覆盖，1 - 跳过，2 - 保留两者（会添加序号）
    :return: 返回生成器，第一项为当前进度，第二项为状态码
    """
    if not paths:
        logger.info("输入列表为空")
        return "[PNG转JPG] 输入列表为空"
    else:
        length = len(paths)
        for index, path in enumerate(paths):
            try:
                logger.info(f"正在转换：{path}")
                if not os.path.exists(path):
                    logger.error(f"图像不存在：{path}")
                    return 10
                # 0 - 成功，1 - 此项被跳过
                result = convert_single(
                    path=path,
                    quality=quality,
                    preserve_metadata=preserve_metadata,
                    deduplicate=deduplicate
                )
                logger.info(f"已跳过：{path}" if result else f"已转换：{path}")
                yield int(((index + 1) / length) * 100), result
            except Exception as e:
                logger.error(f"转换失败：{str(e)}")
                yield int(((index + 1) / length) * 100), 20
        return None


def get_image_list(folder: str, recursive: bool, pass_trans: bool) -> tuple[int, list | str]:
    """
    在指定路径下递归或不递归地查找png图像

    状态：
    0 - 成功
    1 - 路径为空或找不到指定的路径
    2 - 其他未知错误

    :param folder: 要查找的路径
    :param recursive: 是否递归查找
    :param pass_trans: 是否跳过有透明通道的图像
    :return: 元组，第一项为查找状态，第二项为空（失败时）或图像列表（成功时）
    """
    try:
        if not folder or not os.path.exists(folder):
            logger.error(f"路径为空或找不到指定的路径")
            return 1, []
        # 确定pattern
        if recursive:
            logger.info(f"递归扫描文件夹：{folder}")
            pattern = os.path.join(folder, '**', '*.[Pp][Nn][Gg]')
        else:
            logger.info(f"扫描文件夹：{folder}")
            pattern = os.path.join(folder, '*.[Pp][Nn][Gg]')
        # 查找图像
        png_files = glob.glob(pattern, recursive=recursive)
        # 移除透明图片
        if pass_trans:
            valid_files = []
            for path in png_files:
                with Image.open(path) as img:
                    if 'A' not in img.mode:
                        valid_files.append(path)
            png_files = valid_files
        # 返回值
        return 0, png_files
    except Exception as e:
        logger.error(f"查找失败：{str(e)}")
        return 2, []
