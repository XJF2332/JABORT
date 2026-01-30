import os
from typing import Generator

from PIL import Image, ImageDraw

from Core import log_manager

logger = log_manager.get_logger(__name__)


def generate_image_sequence(target: str, amount: int,
                            resolution: tuple[int, int]) -> Generator[tuple[int, int], None, None]:
    """
    生成一个图像序列，保存为目标文件夹中的JPG文件。

    Args:
        target: 目标文件夹路径。
        amount: 要生成的图像数量。
        resolution: 图像的分辨率 (width, height)。

    Returns:
        Generator[tuple[int, int], None, None]: 生成当前进度的百分比 (0-100)和状态码（0成功1失败）。
    """
    if not os.path.exists(target):
        os.makedirs(target)
        logger.info(f"{target} 不存在，已创建")

    width, height = resolution
    logger.debug(f"分辨率：{resolution}")

    logger.info(f"正在 {target} 下生成 {amount} 张图像")
    for i in range(amount):
        try:
            logger.debug(f"生成第 {i} 张图像")
            img = Image.new('RGB', (width, height), color='white')
            draw = ImageDraw.Draw(img)
            text_content = str(i)

            # 文本位置
            bbox = draw.textbbox((0, 0), text_content)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x = (width - text_width) / 2
            y = (height - text_height) / 2
            logger.debug(f"文本位置：{x}, {y}")

            draw.text((x, y), text_content, fill='black')
            file_path = os.path.join(target, f"seq_{i}.jpg")
            img.save(file_path, quality=80)

            # 进度
            progress = int(((i + 1) / amount) * 100)
            yield progress, 0
        except Exception as e:
            logger.error(f"在生成第 {i} 张图像时出现错误：{str(e)}")
            progress = int(((i + 1) / amount) * 100)
            yield progress, 1
    logger.info(f"已生成 {amount} 张图像")
    return None