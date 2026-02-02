import json
import os
import uuid
from typing import Generator

import requests
import websocket
from PIL import Image

from Core import log_manager
from Tools.Utils import utils

logger = log_manager.get_logger(__name__)


class ImageUpscaler:
    def __init__(self, height_thresh: int, width_thresh: int, size_thresh: int, img_dir: str, model_name: str,
                 url: str, downscale: float, recursive: bool, save_dir: str):
        """
        使用ComfyUI API放大图片
        :param height_thresh: 查找图片时，高度小于此值的图像会被视为需要放大
        :param width_thresh: 查找图片时，宽度小于此值的图像会被视为需要放大
        :param size_thresh: 查找图片时，大小小于此值的图像会被视为需要放大
        :param img_dir: 在此目录下查找图片
        :param model_name: 使用此模型放大图像
        :param url: ComfyUI API的URL
        :param downscale: 在使用模型放大后，再缩小为此倍数 - 可以增加一些锐度
        :param recursive: 查找图片时，是否要查找img_dir的子文件夹
        :param save_dir: 图像放大后，保存到此处
        """
        self.prompt_text = {
            "1": {
                "inputs": {
                    "image": "example.png"
                },
                "class_type": "LoadImage",
                "_meta": {
                    "title": "加载图像"
                }
            },
            "2": {
                "inputs": {
                    "model_name": "1x-Bendel-Halftone.pth"
                },
                "class_type": "UpscaleModelLoader",
                "_meta": {
                    "title": "加载放大模型"
                }
            },
            "4": {
                "inputs": {
                    "upscale_model": [
                        "2",
                        0
                    ],
                    "image": [
                        "1",
                        0
                    ]
                },
                "class_type": "ImageUpscaleWithModel",
                "_meta": {
                    "title": "使用模型放大图像"
                }
            },
            "5": {
                "inputs": {
                    "upscale_method": "lanczos",
                    "scale_by": 1,
                    "image": [
                        "4",
                        0
                    ]
                },
                "class_type": "ImageScaleBy",
                "_meta": {
                    "title": "缩放图像（比例）"
                }
            },
            "6": {
                "inputs": {
                    "images": [
                        "5",
                        0
                    ]
                },
                "class_type": "SaveImageWebsocket",
                "_meta": {
                    "title": "保存图像（网络接口）"
                }
            }
        }
        self.height_threshold = height_thresh
        self.width_threshold = width_thresh
        self.size_threshold = size_thresh
        self.img_dir = img_dir
        self.model_name = model_name
        self.api_url = url
        self.downscale = downscale
        self.recursive_search = recursive
        self.save_dir = save_dir
        self.supported_types = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp')
        self.client_id = str(uuid.uuid4())
        self._temp_image_data = None

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

    def _upload_image(self, image_path: str) -> str:
        """
        辅助函数，上传图片到 ComfyUI 以便 LoadImage 节点使用
        """
        try:
            with open(image_path, 'rb') as f:
                response = requests.post(f"{self.api_url}/upload/image", files={'image': f})
                response.raise_for_status()
                # 上传后的文件名
                return response.json().get("name")
        except Exception as e:
            logger.error(f"上传图片失败: {e}")
            return ""

    def send_request_single(self, image_path: str) -> int:
        """
        发送单个放大请求
        :return: 0 成功, 1 失败
        """
        # 上传图片
        uploaded_filename = self._upload_image(image_path)
        if not uploaded_filename:
            return 1

        # 修改 Prompt
        # LoadImage
        self.prompt_text["1"]["inputs"]["image"] = uploaded_filename
        # UpscaleModelLoader
        self.prompt_text["2"]["inputs"]["model_name"] = self.model_name
        # ImageScaleBy
        self.prompt_text["5"]["inputs"]["scale_by"] = self.downscale  # type: ignore

        # 清空临时数据
        self._temp_image_data = None

        # 执行任务
        result_code = self.queue_prompt(self.prompt_text)
        if result_code != 0:
            logger.error(f"请求发送失败 (Code {result_code}) - 图片: {image_path}")
            return 1
        elif self._temp_image_data:
            # 保存文件到本地
            try:
                save_file_path = os.path.join(self.save_dir, os.path.basename(image_path))
                save_file_path = utils.get_unique_filename(save_file_path)
                with open(save_file_path, 'wb') as f:
                    f.write(self._temp_image_data)

                current_image = Image.open(image_path)
                logger.info(
                    f"已放大图片: {os.path.basename(image_path)} | "
                    f"分辨率: {current_image.size} | "
                    f"大小: {os.path.getsize(image_path) / 1024:.2f}KB"
                )
                return 0
            except Exception as e:
                logger.error(f"保存或读取处理后的图片 {image_path} 时出错: {e}")
                return 1
        else:
            logger.error(f"任务完成但未收到图像数据: {image_path}")
            return 1

    def queue_prompt(self, prompt) -> int:
        """
        使用 WebSocket 提交任务并接收结果
        向ComfyUI API发送任务并等待完成
        :return: 0 成功, 1 节点错误, 2 API请求/网络错误
        """
        ws = websocket.WebSocket()
        try:
            # 构造 WebSocket URL
            ws_url = self.api_url.replace("http://", "ws://").replace("https://", "wss://")
            ws.connect(f"{ws_url}/ws?clientId={self.client_id}")

            # 发送 Prompt (HTTP)
            p = {"prompt": prompt, "client_id": self.client_id}
            response = requests.post(f"{self.api_url}/prompt", json=p)
            response.raise_for_status()
            result = response.json()

            # 检查即时节点错误
            if result.get("node_errors"):
                logger.error(f"工作流节点错误: {result['node_errors']}")
                ws.close()
                return 1

            # 循环监听 WebSocket 消息
            current_node = ""
            while True:
                out = ws.recv()
                # 文本消息
                if isinstance(out, str):
                    message = json.loads(out)
                    if message['type'] == 'executing':
                        data = message['data']
                        if data['node'] is None:
                            break
                        else:
                            current_node = data['node']
                # 二进制消息
                elif isinstance(out, bytes):
                    # 检查节点ID 6 (websocket保存节点)
                    if current_node == "6":
                        self._temp_image_data = out[8:]

            ws.close()
            return 0

        except websocket.WebSocketException as e:
            logger.error(f"WebSocket 连接错误: {e}")
            return 2
        except requests.exceptions.RequestException as e:
            logger.error(f"无法发送API请求: {e}")
            return 2
        except Exception as e:
            logger.error(f"任务执行期间发生未知错误: {e}")
            return 2
        finally:
            if ws.connected:
                ws.close()
