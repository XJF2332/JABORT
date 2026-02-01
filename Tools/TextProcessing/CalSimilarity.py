import os.path

import numpy as np
from llama_cpp import Llama

from Core import log_manager

logger = log_manager.get_logger(__name__)

embed_model = None
prev_model = ""


def calculate_similarity(embeddings1, embeddings2):
    """
    计算两个embeddings之间的相似度

    Args:
        embeddings1: 第一个embeddings列表
        embeddings2: 第二个embeddings列表

    Returns:
        相似度值
    """
    vec1 = np.array(embeddings1)
    vec2 = np.array(embeddings2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    logger.debug(f"第一个模：{norm1}，第二个模：{norm2}")
    if norm1 == 0 or norm2 == 0:
        raise ZeroDivisionError
    else:
        similarity = np.vdot(vec1, vec2) / (norm1 * norm2)
        return similarity


def main(str1: str, str2: str, model: str, persistent_model: bool):
    """
    使用嵌入模型计算两个字符串的语义相似度

    状态码
    1 - 模型为空或不存在
    2 - 输入字符串包含空字符串
    3 - 在输入中发现了模为 0 的嵌入向量

    Args:
        str1: 要计算的字符串之一
        str2: 要计算的字符串之二
        model: 要使用的嵌入模型
        persistent_model: 是否要记住上一次使用时加载的模型

    Returns:
        第一项为状态（0成功），第二项为结果
    """
    logger.info(f"使用 {model} 计算 {str1} 和 {str2} 的相似度，记住模型：{persistent_model}")
    if not model or not os.path.exists(model):
        logger.error(f"模型路径为空或不存在：{model}")
        return 1, "模型路径为空或不存在"
    if not str1 or not str2:
        logger.error(f"输入包含空字符串")
        logger.error(f"输入 1：{str1}")
        logger.error(f"输入 2：{str2}")
        return 2, "输入包含空字符串"
    # 记住模型
    global embed_model, prev_model
    logger.debug(f"当前模型：{model}，上次模型：{prev_model}")
    if persistent_model:
        if prev_model != model:
            logger.debug("正在卸载并重新加载模型")
            embed_model = None
            embed_model = Llama(model_path=model, embedding=True, n_gpu_layers=-1)
            prev_model = model
    else:
        logger.debug("正在卸载并重新加载模型")
        embed_model = None
        embed_model = Llama(model_path=model, embedding=True, n_gpu_layers=-1)
    # 计算
    embedding1 = embed_model.create_embedding(str1)
    embedding2 = embed_model.create_embedding(str2)
    try:
        sentence_similarity = calculate_similarity(embedding1["data"][0]["embedding"],
                                                   embedding2["data"][0]["embedding"])
        logger.info(f"相似度：{sentence_similarity}")
        return 0, sentence_similarity
    except ZeroDivisionError:
        logger.info("在输入中发现了模为 0 的嵌入向量")
        return 3, "在输入中发现了模为 0 的嵌入向量"
