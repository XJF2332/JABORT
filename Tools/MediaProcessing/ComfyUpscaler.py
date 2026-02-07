import json
import os
import uuid
from typing import Generator

import requests
import websocket
from PIL import Image, UnidentifiedImageError

from Core import log_manager
from Core.error_codes import ErrorCode
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

    def _check_image_requirement(self, path: str) -> tuple[ErrorCode, str]:
        """
        判断是否是需要的图片，期望的返回只有FileSkipped和Success，其他码都是出错
        :return: (ErrorCode, 前缀字符串)
        """
        try:
            if not self._is_supported_filetype(path):
                return ErrorCode.FileSkipped, ""
            # 检查图像
            with Image.open(path) as image:
                # 分辨率 或 大小
                if self._is_required_res(image) or self._is_required_size(path):
                    prefix = ""
                    prefix += "T" if "A" in image.mode else ""
                    prefix += "L" if self._is_too_long(image) else ""
                    prefix += " " if prefix else ""
                    return ErrorCode.Success, prefix
                else:
                    return ErrorCode.FileSkipped, ""
        except UnidentifiedImageError as e:
            logger.error(f"图像损坏或无法读取 {path}: {e}")
            return ErrorCode.BrokenImage, ""
        except Exception as e:
            logger.error(f"检查文件 {path} 时发生未知错误: {e}")
            return ErrorCode.Unknown, ""

    def get_image_files(self) -> Generator[tuple[ErrorCode, str], None, None]:
        """
        获取图片文件列表
        :return: 生成器，yield (ErrorCode, 文件路径字符串(含前缀))
        """
        logger.debug(f"在 {self.img_dir} 下查找图片列表，递归：{self.recursive_search}")
        if not self.img_dir:
            logger.error(ErrorCode.InvalidPath.format(self.img_dir))
            yield ErrorCode.InvalidPath, ""
            return

        def _check_n_build_path(file2check) -> tuple[ErrorCode, str]:
            """
            对_check_image_requirement的简单封装，检查图像是否满足要求，并视情况组装文件名
            
            Args:
                file2check: 要检查的路径

            Returns:
                (ErrorCode，文件路径字符串(含前缀))
            """
            stat, prefix = self._check_image_requirement(file2check)
            logger.debug(f"{file2check} 的检查结果：{stat.name}")
            # 只有图像满足要求才需要组装新路径
            if stat == ErrorCode.Success:
                return ErrorCode.Success, f"{prefix}{file2check}"
            else:
                return stat, file2check

        iterator = os.walk(self.img_dir) if self.recursive_search else [(self.img_dir, [], os.listdir(self.img_dir))]

        try:
            for root, dirs, files in iterator:
                for file in files:
                    file_path = os.path.join(root, file)
                    if os.path.isfile(file_path):
                        res_code, res_str = _check_n_build_path(file_path)
                        if res_code == ErrorCode.Success:
                            logger.debug(f"找到文件：{file_path}")
                            yield ErrorCode.Success, res_str
                        elif res_code == ErrorCode.FileSkipped:
                            logger.info(f"已跳过：{file_path}")
                        else:
                            logger.error(res_code.generic)
        except Exception as e:
            logger.error(f"遍历目录失败: {e}")
            yield ErrorCode.Unknown, ""

    def _upload_image(self, image_path: str) -> tuple[ErrorCode, str]:
        """
        上传图片到 ComfyUI
        :return: (ErrorCode, 上传后的文件名 或 错误信息)
        """
        try:
            with open(image_path, 'rb') as f:
                logger.debug(f"上传图片到ComfyUI：{image_path}")
                response = requests.post(f"{self.api_url}/upload/image", files={'image': f})
                response.raise_for_status()
                return ErrorCode.Success, response.json().get("name")
        except requests.exceptions.RequestException as e:
            logger.error(f"上传图片失败 {image_path}: {e}")
            return ErrorCode.ApiConnectionError, str(e)
        except Exception as e:
            logger.error(f"读取或上传图片时发生错误 {image_path}: {e}")
            return ErrorCode.UploadFailed, str(e)

    def send_request_single(self, image_path: str) -> tuple[ErrorCode, str]:
        """
        发送单个放大请求
        :return: (ErrorCode, 保存图像路径)
        """
        # 上传图片
        res1 = self._upload_image(image_path)
        if res1[0] != ErrorCode.Success:
            return res1[0], ""

        # 更新 prompt
        self.prompt_text["1"]["inputs"]["image"] = res1[1]
        self.prompt_text["2"]["inputs"]["model_name"] = self.model_name
        self.prompt_text["5"]["inputs"]["scale_by"] = self.downscale  # type: ignore
        self._temp_image_data = None

        # 发送请求
        res2 = self.queue_prompt(self.prompt_text)
        if res2 != ErrorCode.Success:
            logger.error(f"图片 {image_path} 的请求失败：{res2.generic}")
            return res2, ""

        # 保存结果
        if self._temp_image_data:
            try:
                if not os.path.exists(self.save_dir):
                    os.makedirs(self.save_dir)
                original_filename = os.path.basename(image_path)
                save_file_path = os.path.join(self.save_dir, original_filename)
                res3 = utils.filename_deduplicate(2, save_file_path)
                if res3[0] != ErrorCode.Success:
                    logger.error(res3[0].generic)
                    return res3[0], ""
                with open(res3[1], 'wb') as f:
                    f.write(self._temp_image_data)
                logger.info(f"已放大图片: {original_filename} -> {res3[1]}")
                return ErrorCode.Success, res3[1]
            except OSError as e:
                logger.error(f"无法保存放大后的 {image_path}: {e}")
                return ErrorCode.CannotWriteFile, ""
            except Exception as e:
                logger.error(f"保存结果时发生未知错误: {e}")
                return ErrorCode.Unknown, ""
        else:
            logger.error(f"任务完成但未收到图像数据: {image_path}")
            return ErrorCode.WorkflowNodeError, "未接收到图像数据"

    def queue_prompt(self, prompt) -> ErrorCode:
        """
        使用 WebSocket 提交任务并接收结果
        :return: ErrorCode
        """
        logger.info("正在发送 Prompt")
        ws = websocket.WebSocket()
        try:
            ws_url = self.api_url.replace("http://", "ws://").replace("https://", "wss://")
            ws.connect(f"{ws_url}/ws?clientId={self.client_id}")

            # 发送 prompt
            p = {"prompt": prompt, "client_id": self.client_id}
            response = requests.post(f"{self.api_url}/prompt", json=p)
            response.raise_for_status()
            result = response.json()

            # 检查即时节点错误
            if result.get("node_errors"):
                logger.error(f"工作流节点错误: {result['node_errors']}")
                ws.close()
                return ErrorCode.WorkflowNodeError

            # 监听 ws 消息
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
                    # websocket保存节点（id=6）
                    if current_node == "6":
                        self._temp_image_data = out[8:]

            ws.close()
            return ErrorCode.Success
        except websocket.WebSocketException as e:
            logger.error(f"WebSocket 连接错误: {e}")
            return ErrorCode.ApiConnectionError
        except requests.exceptions.RequestException as e:
            logger.error(f"API请求失败: {e}")
            return ErrorCode.ApiConnectionError
        except Exception as e:
            logger.error(f"任务执行期间发生未知错误: {e}")
            return ErrorCode.Unknown
        finally:
            if ws.connected:
                ws.close()