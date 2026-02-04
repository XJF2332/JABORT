import glob
import os
from typing import Generator

from PIL import Image, UnidentifiedImageError

from Core import log_manager
from Core.error_codes import ErrorCode
from Tools.Utils import utils

logger = log_manager.get_logger(__name__)


def convert_single(input_path: str, quality: int, preserve_metadata: bool, deduplicate: int,
                   old: str = "png") -> tuple[ErrorCode, str]:
    """
    转换单个图像文件

    :param input_path: 图像路径
    :param quality: 质量
    :param preserve_metadata: 保留元数据
    :param deduplicate: 去重模式，0 - 覆盖，1 - 跳过，2 - 保留两者（会添加序号）
    :param old: 旧文件的扩展名，因为它不只能转PNG，也可以转别的，此处留下这个接口以便其他脚本调用
    :return: 包含错误码和新文件路径的元组
    """
    logger.debug(f"正在转换：{input_path}")
    with Image.open(input_path) as image:
        logger.debug(f"图像模式：{image.mode}")
        if 'A' in image.mode:
            image = image.convert('RGB')

        # 新图像路径
        output_path = input_path.replace(old, "jpg")
        if not output_path.endswith(".jpg"):
            output_path = output_path + ".jpg"
        dedup_res = utils.filename_deduplicate(deduplicate, output_path)
        if dedup_res[0] != ErrorCode.Success:
            logger.error(dedup_res[0].format(input_path))
            return dedup_res
        else:
            output_path = dedup_res[1]
            logger.debug(f"构建的输出图像路径：{output_path}")

        # 转换
        if preserve_metadata:
            image.save(output_path, 'JPEG', quality=quality, metadata=image.info)
        else:
            image.save(output_path, 'JPEG', quality=quality)

        logger.info(f"已转换 {output_path}")
        return ErrorCode.Success, output_path


def convert_batch(images: list, quality: int, preserve_metadata: bool,
                  deduplicate: int) -> Generator[tuple[ErrorCode, int], None, tuple[ErrorCode, int]]:
    """
    对输入的路径列表进行批量转换

    20 - 此项失败

    :param images: 所有图像文件路径的列表
    :param quality: 质量
    :param preserve_metadata: 保留元数据
    :param deduplicate: 去重模式，0 - 覆盖，1 - 跳过，2 - 保留两者（会添加序号）
    :return: 返回生成器，第一项为当前进度，第二项为错误码
    """
    if not images:
        logger.info("输入列表为空")
        return ErrorCode.EmptyList, 0
    else:
        length = len(images)
        for index, image in enumerate(images):
            try:
                logger.info(f"正在转换：{image}")
                if not os.path.exists(image):
                    logger.error(ErrorCode.InvalidPath.format(image))
                    return ErrorCode.InvalidPath, 0
                res = convert_single(input_path=image, quality=quality, preserve_metadata=preserve_metadata,
                                     deduplicate=deduplicate)
                if res[0] == ErrorCode.Success:
                    yield ErrorCode.Success, int(((index + 1) / length) * 100)
                elif res[0] == ErrorCode.FileSkipped:
                    logger.warning(f"已跳过：{image}")
                    yield ErrorCode.FileSkipped, int(((index + 1) / length) * 100)
                else:
                    logger.error(res[0].format(image))
                    return res[0], int(((index + 1) / length) * 100)
            except UnidentifiedImageError:
                logger.error(ErrorCode.BrokenImage.format(image))
                yield ErrorCode.BrokenImage, int(((index + 1) / length) * 100)
            except Exception as e:
                logger.error(f"转换失败：{str(e)}")
                yield ErrorCode.Unknown, int(((index + 1) / length) * 100)
        return ErrorCode.Success, 100


def get_image_list(folder: str, recursive: bool, pass_trans: bool) -> tuple[ErrorCode, list]:
    """
    在指定路径下递归或不递归地查找png图像

    :param folder: 要查找的路径
    :param recursive: 是否递归查找
    :param pass_trans: 是否跳过有透明通道的图像
    :return: 元组，第一项为错误码，第二项为图像列表
    """
    try:
        if not folder or not os.path.exists(folder):
            logger.error(f"路径为空或找不到指定的路径")
            return ErrorCode.InvalidPath, []
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
            for png in png_files:
                with Image.open(png) as img:
                    if 'A' not in img.mode:
                        logger.debug(f"图像 {png} 的模式：{img.mode}")
                        valid_files.append(png)
            png_files = valid_files
        # 返回值
        logger.info(f"共找到 {len(png_files)} 项文件")
        return ErrorCode.Success, png_files
    except Exception as e:
        logger.error(f"查找失败：{str(e)}")
        return ErrorCode.Unknown, []
