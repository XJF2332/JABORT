# -*- coding: utf-8 -*-
import os
import logging
import zipfile
from datetime import datetime
import threading

LOG_DIR = "./logs"
LOG_FILENAME = "latest.log"
LOG_PATH = os.path.join(LOG_DIR, LOG_FILENAME)

# 用于确保 setup_logger 只执行一次的锁
_setup_lock = threading.Lock()
_logger_initialized = False

def _archive_existing_log():
    """
    检测 log 文件是否存在，如果存在则压缩归档并删除原文件
    """
    if not os.path.exists(LOG_PATH):
        return

    try:
        # 文件创建时间
        ctime = os.path.getmtime(LOG_PATH)
        dt = datetime.fromtimestamp(ctime)
        timestamp_str = dt.strftime("%Y%m%d_%H%M%S")

        # 归档名称
        zip_name = f"log-{timestamp_str}.zip"
        zip_path = os.path.join(LOG_DIR, zip_name)

        # 归档并清理
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.write(LOG_PATH, arcname=f"old_log_{timestamp_str}.log")
        print(f"Archived old log to: {zip_path}")
        os.remove(LOG_PATH)

    except Exception as e:
        print(f"[LogManager] Error during log archiving: {e}")

def get_logger(name="main"):
    """
    获取 Logger 的工厂方法。

    机制保证：
    1. 只有第一次调用时会执行归档和 Handler 配置。
    2. 返回的 Logger 实例将持有唯一的 FileHandler，保证线程安全。
    3. 后续调用只会返回已配置好的 Logger 或其子 Logger。
    """
    global _logger_initialized

    # 根 Logger 名称，所有模块应基于此扩展，如 App.Network, App.Database
    root_name = "main"

    # 获取根 logger
    root_logger = logging.getLogger(root_name)

    # 双重检查锁定，确保多线程初始化时的安全性
    if not _logger_initialized:
        with _setup_lock:
            if not _logger_initialized:
                # 准备目录
                if not os.path.exists(LOG_DIR):
                    os.makedirs(LOG_DIR)

                # 执行归档
                _archive_existing_log()

                # Root Logger
                root_logger.setLevel(logging.INFO)

                # 防止重复添加 Handler
                if not root_logger.handlers:
                    # 只实例化这一个 FileHandler
                    try:
                        file_handler = logging.FileHandler(LOG_PATH, mode='a', encoding='utf-8')
                        formatter = logging.Formatter(
                            '%(asctime)s - %(name)s - %(funcName)s - %(levelname)s: %(message)s'
                        )
                        file_handler.setFormatter(formatter)
                        root_logger.addHandler(file_handler)
                        console_handler = logging.StreamHandler()
                        console_handler.setFormatter(formatter)
                        root_logger.addHandler(console_handler)
                    except Exception as e:
                        print(f"[LogManager] Failed to setup file handler: {e}")

                _logger_initialized = True

    if name == root_name:
        return root_logger
    elif name.startswith(f"{root_name}."):
        return root_logger.getChild(name)
    else:
        return root_logger.getChild(name)
