import os
import numpy as np
from PIL import Image


def generate_noise_image(output_folder: str, index: int = 1) -> (int, str):
    """
    生成噪声图片
    :param index: 当前图片的序号
    :param output_folder: 输出文件夹路径
    :return: 生成状态
    """
    try:
        noise = np.random.rand(1024, 1024, 3) * 255
        noise = noise.astype(np.uint8)
        img = Image.fromarray(noise)
        img_name = f'noise_{index}.png'
        img_path = os.path.join(output_folder, img_name)
        img.save(img_path)
        return 0, f"[噪声图像生成] 已生成第 {index} 张图像"
    except Exception as e:
        return 1, f"[噪声图像生成] {str(e)}"
