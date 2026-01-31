import os
import time
from typing import Generator

import PIL.Image
import requests


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

    def _is_required_res(self, image: PIL.Image.Image):
        return image.size[0] < self.width_threshold or image.size[1] < self.height_threshold

    def _is_required_size(self, path: str):
        return os.path.getsize(path) < self.size_threshold * 1024

    @staticmethod
    def _is_too_long(image: PIL.Image.Image):
        return image.size[0] / image.size[1] > 2.5 or image.size[1] / image.size[0] > 2.5

    def _is_required_image(self, path: str) -> tuple[bool, str]:
        """
        判断是否是需要的图片
        返回的字符串不为空时，若返回值是True则是标志位，如果是False则是报错信息
        标志位：
        透明 - T（transparent）
        长图 - L（long）
        :param path: 图片路径
        :return: 元组，如果是，则第一项返回True，否则第一项返回False，同时第二项会跟一个字符串。
        """
        try:
            # 文件类型
            if self._is_supported_filetype(path):
                # 使用 with 语句确保文件句柄正确关闭
                with PIL.Image.open(path) as image:
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
            return False, f"[ComfyUI 放大器] 无法打开文件 {path}: {str(e)}"

    def get_image_files(self) -> Generator:
        """
        获取图片文件列表，返回生成器，生成器的第一项为状态（0-正常，1-错误），第二项为信息（正常时为图像列表，错误时为错误信息）
        """
        if not self.img_dir:
            yield []
            return None

        image_files = []
        # 递归查找
        if self.recursive_search:
            for root, dirs, files in os.walk(self.img_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    if os.path.isfile(file_path):
                        judgement = self._is_required_image(file_path)
                        if judgement[0]:
                            image_files.append(f"{judgement[1]}{file_path}")
                            yield 0, image_files
                        elif judgement[1]:
                            yield 1, judgement[1]
        # 非递归查找
        else:
            for file in os.listdir(self.img_dir):
                file_path = os.path.join(self.img_dir, file)
                if os.path.isfile(file_path):
                    judgement = self._is_required_image(file_path)
                    if judgement[0]:
                        image_files.append(f"{judgement[1]}{file_path}")
                        yield 0, image_files
                    elif judgement[1]:
                        yield 1, judgement[1]

        yield 0, image_files
        return None

    def send_request_single(self, image_path: str):
        """发送单个放大请求，由调用方传入图像路径"""
        self.prompt_text["1"]["inputs"]["image"] = image_path
        self.prompt_text["1"]["inputs"]["upload"] = "image"
        self.prompt_text["11"]["inputs"]["model_name"] = self.model_name
        self.prompt_text["15"]["inputs"]["filename_prefix"] = os.path.splitext(os.path.basename(image_path))[0]

        result = self.queue_prompt(self.prompt_text)
        if result:
            return f"[ComfyUI 放大器] 请求发送失败：{result}"
        else:
            try:
                current_image = PIL.Image.open(image_path)
                returns = f"""
[ComfyUI 放大器] 已放大：{image_path}
    图片分辨率：{current_image.size}
    图片大小：{os.path.getsize(image_path) / 1024:.2f}KB"""
                return returns
            except Exception as e:
                return f"[ComfyUI 放大器] 处理图片 {image_path} 时出错：{e}"

    def queue_prompt(self, prompt):
        try:
            p = {"prompt": prompt}
            response = requests.post(f"{self.api_url}/prompt", json=p)
            response.raise_for_status()
            result = response.json()

            # 检查节点错误
            if result.get("node_errors"):
                return f"[ComfyUI 放大器] 工作流节点错误: {result['node_errors']}"

            # 查询任务队列
            current_retries = 0
            max_retries = 2
            while True:
                time.sleep(self.get_interval)
                try:
                    remaining_queue = requests.get(f"{self.api_url}/prompt").json()
                    remaining_queue = remaining_queue.get("exec_info", {}).get("queue_remaining", 0)
                    current_retries = 0
                    if remaining_queue == 0:
                        break
                except Exception as e:
                    print(f"[ComfyUI 放大器] 查询队列状态出错: {e}，剩余重试次数：{max_retries - current_retries}")
                    current_retries = current_retries + 1
                    time.sleep(1)
                    if current_retries > max_retries:
                        break
            return None
        except Exception as e:
            return f"[ComfyUI 放大器] 无法发送请求: {e}"