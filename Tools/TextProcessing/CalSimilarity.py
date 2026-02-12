import os.path

import numpy as np
from llama_cpp import Llama

from Core import log_manager
from Core.error_codes import ErrorCode

logger = log_manager.get_logger(__name__)

embed_model = None
prev_model = ""


def calculate_similarity(embeddings1, embeddings2) -> tuple[ErrorCode, float]:
    """
    计算两个embeddings之间的相似度

    Args:
        embeddings1: 第一个embeddings列表
        embeddings2: 第二个embeddings列表

    Returns:
        相似度值
    """
    try:
        vec1 = np.array(embeddings1)
        vec2 = np.array(embeddings2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        logger.debug(f"第一个模：{norm1}，第二个模：{norm2}")
        if norm1 == 0 or norm2 == 0:
            logger.error(ErrorCode.ZeroDivision.format("有至少一个嵌入向量的模为零"))
            return ErrorCode.ZeroDivision, 0
        else:
            similarity = np.vdot(vec1, vec2) / (norm1 * norm2) # type:ignore
            logger.info(f"计算结果：{similarity}")
            return ErrorCode.Success, similarity
    except Exception as e:
        logger.error(ErrorCode.Unknown.format(str(e)))
        return ErrorCode.Unknown, 0


def unload_model() -> str:
    global embed_model, prev_model
    embed_model = None
    prev_model = ""
    logger.info("模型已卸载")
    return "模型已卸载"


def main(str1: str, str2: str, model: str, persistent_model: bool) -> tuple[ErrorCode, float]:
    """
    使用嵌入模型计算两个字符串的语义相似度

    Args:
        str1: 要计算的字符串之一
        str2: 要计算的字符串之二
        model: 要使用的嵌入模型
        persistent_model: 是否要记住上一次使用时加载的模型

    Returns:
        计算结果
    """
    logger.info(f"使用 {model} 计算 {str1} 和 {str2} 的相似度，记住模型：{persistent_model}")
    if not model or not os.path.exists(model):
        logger.error(ErrorCode.InvalidPath.format(model))
        return ErrorCode.InvalidPath, 0
    if not str1 or not str2:
        logger.error(ErrorCode.EmptyString.format())
        logger.error(f"输入 1：{str1}")
        logger.error(f"输入 2：{str2}")
        return ErrorCode.EmptyString, 0
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
    res = calculate_similarity(embedding1["data"][0]["embedding"], embedding2["data"][0]["embedding"])
    if res[0].code:
        logger.error(f"计算失败：{res}")
        return res[0], 0
    else:
        logger.info(f"计算结果：{res}")
        return ErrorCode.Success, res[1]
