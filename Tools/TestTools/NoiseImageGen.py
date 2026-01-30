import os

import numpy as np
from PIL import Image

from Core import log_manager

logger = log_manager.get_logger(__name__)


def generate_noise_image(output_folder: str, index: int = 1) -> int:
    """
    生成噪声图片
    :param index: 当前图片的序号
    :param output_folder: 输出文件夹路径
    :return: 生成状态，0成功1失败
    """
    try:
        noise = np.random.rand(1024, 1024, 3) * 255
        noise = noise.astype(np.uint8)
        img = Image.fromarray(noise)
        img_name = f'noise_{index}.png'
        img_path = os.path.join(output_folder, img_name)
        img.save(img_path)
        logger.info(f"已在 {output_folder} 生成第 {index} 张图像")
        return 0
    except Exception as e:
        logger.error(f"生成失败：{str(e)}")
        return 1
