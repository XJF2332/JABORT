import os
import time
from typing import Generator

import requests
from PIL import Image

from Core import log_manager

logger = log_manager.get_logger(__name__)


class ImageUpscaler:
    def __init__(self, height_thresh: int, width_thresh: int, size_thresh: int, img_dir: str, model_name: str,
                 url: str, downscale: float, get_interval: float, recursive: bool):
        """
        使用ComfyUI API放大图片
        :param height_thresh: 查找图片时，高度小于此值的图像会被视为需要放大
        :param width_thresh: 查找图片时，宽度小于此值的图像会被视为需要放大
        :param size_thresh: 查找图片时，大小小于此值的图像会被视为需要放大
        :param img_dir: 在此目录下查找图片
        :param model_name: 使用此模型放大图像
        :param url: ComfyUI API的URL
        :param downscale: 在使用模型放大后，再缩小为此倍数 - 可以增加一些锐度
        :param get_interval: 每隔此时间查询一次放大队列状态，查询到任务队列为空时认为放大成功
        :param recursive: 查找图片时，是否要查找img_dir的子文件夹
        """
        self.prompt_text = {
            "1": {
                "inputs": {
                    "image": "example.jpg",
                    "upload": "image"
                },
                "class_type": "LoadImage",
                "_meta": {
                    "title": "加载图像"
                }
            },
            "6": {
                "inputs": {
                    "upscale_method": "lanczos",
                    "scale_by": downscale,
                    "image": [
                        "10",
                        0
                    ]
                },
                "class_type": "ImageScaleBy",
                "_meta": {
                    "title": "图像按系数缩放"
                }
            },
            "10": {
                "inputs": {
                    "upscale_model": [
                        "11",
                        0
                    ],
                    "image": [
                        "1",
                        0
                    ]
                },
                "class_type": "ImageUpscaleWithModel",
                "_meta": {
                    "title": "图像通过模型放大"
                }
            },
            "11": {
                "inputs": {
                    "model_name": "4x-WTP-UDS-Esrgan.pth"
                },
                "class_type": "UpscaleModelLoader",
                "_meta": {
                    "title": "放大模型加载器"
                }
            },
            "15": {
                "inputs": {
                    "filename_prefix": "Upscale",
                    "images": [
                        "6",
                        0
                    ]
                },
                "class_type": "SaveImage",
                "_meta": {
                    "title": "保存图像"
                }
            }
        }
        self.height_threshold = height_thresh
        self.width_threshold = width_thresh
        self.size_threshold = size_thresh
        self.img_dir = img_dir
        self.model_name = model_name
        self.api_url = url
        self.get_interval = get_interval
        self.recursive_search = recursive
        self.supported_types = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp')

    def _is_supported_filetype(self, path: str):
        return path.lower().endswith(self.supported_types) and not path.lower().endswith('.gif')

    def _is_required_res(self, image: Image.Image):
        return image.size[0] < self.width_threshold or image.size[1] < self.height_threshold

    def _is_required_size(self, path: str):
        return os.path.getsize(path) < self.size_threshold * 1024

    @staticmethod
    def _is_too_long(image: Image.Image):
        return image.size[0] / image.size[1] > 2.5 or image.size[1] / image.size[0] > 2.5

    def _is_required_image(self, path: str) -> tuple[bool, str]:
        """
        判断是否是需要的图片
        :return: 元组，(是否符合条件, 前缀字符串)
        """
        try:
            # 文件类型
            if self._is_supported_filetype(path):
                with Image.open(path) as image:
                    # 分辨率 或 大小
                    if self._is_required_res(image) or self._is_required_size(path):
                        prefix = ""
                        prefix += "T" if "A" in image.mode else ""
                        prefix += "L" if self._is_too_long(image) else ""
                        prefix += " " if prefix else ""
                        return True, prefix
                    else:
                        return False, ""
            else:
                return False, ""
        except Exception as e:
            logger.error(f"无法检查文件 {path}: {e}")
            return False, ""

    def get_image_files(self) -> Generator[str, None, None]:
        """
        获取图片文件列表
        现在仅生成有效的文件路径字符串，错误信息在内部记录日志。
        保留生成器模式以便 Worker 可以在搜索过程中随时终止。
        :return: 生成器，yield 文件路径字符串
        """
        if not self.img_dir:
            return

        # 辅助函数：处理单个文件
        def process_file(file_p):
            judgement = self._is_required_image(file_p)
            if judgement[0]:
                return f"{judgement[1]}{file_p}"
            return None

        # 递归查找
        if self.recursive_search:
            for root, dirs, files in os.walk(self.img_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    if os.path.isfile(file_path):
                        res = process_file(file_path)
                        if res:
                            yield res
        # 非递归查找
        else:
            try:
                for file in os.listdir(self.img_dir):
                    file_path = os.path.join(self.img_dir, file)
                    if os.path.isfile(file_path):
                        res = process_file(file_path)
                        if res:
                            yield res
            except Exception as e:
                logger.error(f"遍历目录失败: {e}")

    def send_request_single(self, image_path: str) -> int:
        """
        发送单个放大请求
        :return: 0 成功, 1 失败
        """
        self.prompt_text["1"]["inputs"]["image"] = image_path
        self.prompt_text["1"]["inputs"]["upload"] = "image"
        self.prompt_text["11"]["inputs"]["model_name"] = self.model_name
        self.prompt_text["15"]["inputs"]["filename_prefix"] = os.path.splitext(os.path.basename(image_path))[0]

        result_code = self.queue_prompt(self.prompt_text)

        if result_code != 0:
            logger.error(f"请求发送失败 (Code {result_code}) - 图片: {image_path}")
            return 1
        else:
            try:
                current_image = Image.open(image_path)
                logger.info(
                    f"已放大图片: {os.path.basename(image_path)} | "
                    f"分辨率: {current_image.size} | "
                    f"大小: {os.path.getsize(image_path) / 1024:.2f}KB"
                )
                return 0
            except Exception as e:
                logger.error(f"处理图片 {image_path} 时出错: {e}")
                return 1

    def queue_prompt(self, prompt) -> int:
        """
        向ComfyUI API发送任务并等待完成
        :return: 0 成功, 1 节点错误, 2 API请求/网络错误
        """
        try:
            p = {"prompt": prompt}
            response = requests.post(f"{self.api_url}/prompt", json=p)
            response.raise_for_status()
            result = response.json()

            # 检查节点错误
            if result.get("node_errors"):
                logger.error(f"工作流节点错误: {result['node_errors']}")
                return 1

            # 查询任务队列
            current_retries = 0
            max_retries = 2
            while True:
                time.sleep(self.get_interval)
                try:
                    remaining_queue_resp = requests.get(f"{self.api_url}/prompt").json()
                    remaining_queue = remaining_queue_resp.get("exec_info", {}).get("queue_remaining", 0)
                    current_retries = 0
                    if remaining_queue == 0:
                        break
                except Exception as e:
                    logger.warning(f"查询队列状态出错: {e}，剩余重试次数：{max_retries - current_retries}")
                    current_retries += 1
                    time.sleep(1)
                    if current_retries > max_retries:
                        logger.error("查询队列状态超时或失败")
                        return 2
            return 0
        except Exception as e:
            logger.error(f"无法发送API请求: {e}")
            return 2
