import os.path

import numpy as np
from llama_cpp import Llama

embed_model = None
prev_model = ""

def calculate_similarity(embeddings1, embeddings2):
    """
    计算两个embeddings之间的相似度

    参数：
    embeddings1 (list): 第一个embeddings列表
    embeddings2 (list): 第二个embeddings列表

    返回值：
    float: 相似度值
    """
    # 将embeddings转换为numpy数组
    embeddings1 = np.array(embeddings1)
    embeddings2 = np.array(embeddings2)

    # 使用vdot计算向量点积（自动展平）
    similarity = np.vdot(embeddings1, embeddings2) / (np.linalg.norm(embeddings1) * np.linalg.norm(embeddings2))

    return similarity


def main(str1: str, str2: str, model: str, persistent_model: bool):
    if not os.path.exists(model):
        return "模型文件不存在"
    if not str1 or not str2:
        return "不要给我输入空字符串"
    # 记住模型
    global embed_model, prev_model
    if persistent_model:
        if prev_model == model:
            pass
        else:
            embed_model = None
            embed_model = Llama(model_path=model, embedding=True, n_gpu_layers=-1)
            prev_model = model
    else:
        embed_model = None
        embed_model = Llama(model_path=model, embedding=True, n_gpu_layers=-1)
    # 计算
    embedding1 = embed_model.create_embedding(str1)
    embedding2 = embed_model.create_embedding(str2)
    sentence_similarity = calculate_similarity(embedding1["data"][0]["embedding"], embedding2["data"][0]["embedding"])
    return sentence_similarity