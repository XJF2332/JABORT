import glob
import os

from PIL import Image

from Tools.Utils import utils


def convert_single(path: str, quality: int, preserve_metadata: bool, deduplicate: int):
    """
    转换单个图像文件
    :param path: 图像路径
    :param quality: 质量
    :param preserve_metadata: 保留元数据
    :param deduplicate: 去重模式，0 - 覆盖，1 - 跳过，2 - 保留两者（会添加序号）
    :return:
    """
    with Image.open(path) as image:
        if 'A' in image.mode:
            image = image.convert('RGB')

        # build new image path
        new_path = path.replace("png", "jpg")
        if new_path.endswith(".jpg"):
            pass
        else:
            new_path = new_path + ".jpg"

        # 去重
        if deduplicate == 1 and os.path.exists(new_path):
            return f"[PNG转JPG] 已跳过 {new_path} ，因为其已存在"
        elif deduplicate == 2:
            new_path = utils.get_unique_filename(new_path)

        # 转换
        if preserve_metadata:
            metadata = image.info
            image.save(new_path, 'JPEG', quality=quality, metadata=metadata)
        else:
            image.save(new_path, 'JPEG', quality=quality)
        return f"[PNG转JPG] 已转换 {new_path}"


def convert_batch(paths: list, quality: int, preserve_metadata: bool, deduplicate: int):
    """
    返回生成器，第一项为当前进度，第二项为日志信息
    :param paths: 所有图像文件路径的列表
    :param quality: 质量
    :param preserve_metadata: 保留元数据
    :param deduplicate: 去重模式，0 - 覆盖，1 - 跳过，2 - 保留两者（会添加序号）
    :return:
    """
    if not paths:
        return "[PNG转JPG] 输入列表为空"
    else:
        length = len(paths)
        for index, path in enumerate(paths):
            try:
                if not os.path.exists(path):
                    return "[PNG转JPG] 图像不存在"
                result = convert_single(
                    path=path,
                    quality=quality,
                    preserve_metadata=preserve_metadata,
                    deduplicate=deduplicate
                )
                yield int(((index + 1) / length) * 100), result
            except Exception as e:
                yield int(((index + 1) / length) * 100), f"[PNG转JPG] 转换失败：{str(e)}"
        return None


def get_image_list(folder: str, recursive: bool, ignore_transparency: bool) -> tuple[int, list | str]:
    """
    返回元组，第一项为查找状态，第二项为日志信息（失败时）或图像列表（成功时）
    :param folder: 要查找的路径
    :param recursive: 是否递归查找
    :param ignore_transparency: 是否无视透明度
    :return:
    """
    try:
        if not folder:
            return 1, f"[PNG转JPG] 路径为空"
        elif not os.path.exists(folder):
            return 1, f"[PNG转JPG] 找不到指定的路径：{folder}"

        if recursive:
            pattern = os.path.join(folder, '**', '*.[Pp][Nn][Gg]')
        else:
            pattern = os.path.join(folder, '*.[Pp][Nn][Gg]')

        png_files = glob.glob(pattern, recursive=recursive)

        # 不忽略透明度 - 跳过透明图片
        if not ignore_transparency:
            valid_files = []
            for path in png_files:
                try:
                    with Image.open(path) as img:
                        if 'A' not in img.mode:
                            valid_files.append(path)
                except:
                    continue
            png_files = valid_files

        return 0, png_files
    except Exception as e:
        return 1, f"查找失败：{str(e)}"
