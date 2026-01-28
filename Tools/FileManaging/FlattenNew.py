import os
import re
import shutil
from typing import Generator

from anytree import Node
from send2trash import send2trash

from Core import log_manager

logger = log_manager.get_logger(__name__)


# 文件系统结点类
class FsNode(Node):
    def __init__(self, name, abs_path, is_file=False, parent=None):
        logger.debug(f"创建FsNode: name={name}, abs_path={abs_path}, is_file={is_file}")
        super().__init__(name, parent)
        self.abs_path = abs_path
        self.is_file = is_file


def build_tree(root_path) -> FsNode:
    """构建文件系统的anytree结构"""
    logger.info(f"开始构建文件树，根路径: {root_path}")
    root_path = os.path.abspath(root_path)
    root_name = os.path.basename(root_path)
    root_node = FsNode(root_name, root_path, is_file=False)
    logger.debug(f"创建根节点: {root_name}")

    # 使用字典记录路径对应的结点，方便挂载
    nodes_map = {root_path: root_node}

    for dirpath, dirnames, filenames in os.walk(root_path):
        logger.debug(f"遍历目录: {dirpath}, 子目录数: {len(dirnames)}, 文件数: {len(filenames)}")
        current_node = nodes_map[dirpath]

        # 添加子目录
        for dirname in dirnames:
            full_path = os.path.join(dirpath, dirname)
            if os.path.isdir(full_path):
                child_node = FsNode(dirname, full_path, is_file=False, parent=current_node)
                nodes_map[full_path] = child_node
                logger.debug(f"添加目录节点: {dirname}")

        # 添加文件
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            if os.path.isfile(full_path):
                FsNode(filename, full_path, is_file=True, parent=current_node)
                logger.debug(f"添加文件节点: {filename}")

    logger.info(f"文件树构建完成，总节点数: {len(nodes_map)}")
    return root_node


def get_unique_name(target_dir, base_name, ext):
    """处理文件名重复，生成唯一的文件名"""
    logger.debug(f"生成唯一文件名: target_dir={target_dir}, base_name={base_name}, ext={ext}")
    target_name = f"{base_name}{ext}"
    list_dir = os.listdir(target_dir)

    if target_name not in list_dir:
        logger.debug(f"文件名无冲突: {target_name}")
        return target_name

    # 寻找最大的index
    max_index = 0
    pattern = re.compile(re.escape(base_name) + r"_(\d+)" + re.escape(ext))
    logger.debug(f"搜索已存在的编号文件，模式: {pattern.pattern}")

    for item in list_dir:
        match = pattern.fullmatch(item)
        if match:
            index = int(match.group(1))
            if index > max_index:
                max_index = index

    result = f"{base_name}_{max_index + 1}{ext}"
    logger.info(f"检测到文件名冲突，生成新名称: {result}")
    return result


def process_flatten(root_path: str) -> Generator:
    """
    执行文件展平操作
    Args:
        root_path: 要展平的文件夹

    Returns:
        生成器，包含当前进度（0-100）
    """
    logger.info(f"开始文件展平处理，根路径: {root_path}")
    root_node = build_tree(root_path)
    op_queue = []

    logger.info("开始扫描符合条件的文件节点...")
    eligible_nodes = 0

    # 遍历树寻找符合条件的结点
    for node in root_node.descendants:
        # 是目录，只有一个子结点，且子结点是文件
        if not node.is_file and len(node.children) == 1:
            child = node.children[0]
            if child.is_file:
                eligible_nodes += 1
                logger.debug(f"找到符合条件的节点: {node.name} -> {child.name}")
                node_a = child  # 将这个文件记为节点A

                # 从A向上查找结点B，检查父结点是否满足停止条件，从而确定B和B1
                current_node = node_a.parent
                node_b = None  # 根目录记为 B
                node_b1 = None  # 到达根目录上一级的目录记为 B1

                while current_node:
                    parent_node = current_node.parent
                    # 如果 current_node 已经是树的根节点（没有父节点了）
                    # 这种情况下，current_node 就是根目录
                    if parent_node is None:
                        node_b = current_node
                        node_b1 = current_node
                        logger.debug(f"到达根节点: {node_b.name}")
                        break

                    # 检查 parent_node 是否满足下列停止条件
                    # 是根目录
                    if parent_node.is_root:
                        node_b = parent_node
                        node_b1 = current_node
                        logger.debug(f"找到根节点: {node_b.name}")
                        break
                    # 有超过一个的目录类型的子结点
                    parent_dir_children = [n for n in parent_node.children if not n.is_file]
                    if len(parent_dir_children) > 1:
                        node_b = parent_node
                        node_b1 = current_node
                        logger.debug(f"找到分支节点: {node_b.name}, 子目录数: {len(parent_dir_children)}")
                        break
                    # 有文件类型的子结点 (排除当前处理分支)
                    parent_file_children = [n for n in parent_node.children if n.is_file]
                    # 检查是否有不在当前路径下的文件
                    if parent_file_children:
                        node_b = parent_node
                        node_b1 = current_node
                        logger.debug(f"找到包含文件的节点: {node_b.name}, 文件数: {len(parent_file_children)}")
                        break

                    # 如果父结点不满足停止条件，继续向上查找
                    current_node = parent_node

                # 构建操作队列
                if node_b and node_b1:
                    _, ext = os.path.splitext(node_a.name)
                    new_base_name = node_b1.name
                    rename_target = f"{new_base_name}{ext}"

                    op = {
                        "path": node_a.abs_path,
                        "move_to": node_b.abs_path,
                        "rename": rename_target,
                        "original_ext": ext,
                        "base_name": new_base_name
                    }
                    op_queue.append(op)
                    logger.debug(f"添加到操作队列: {op}")

    logger.info(f"扫描完成，找到 {eligible_nodes} 个符合条件的节点，共 {len(op_queue)} 项任务需要处理")
    yield 0

    # 执行操作队列
    total_ops = len(op_queue)
    if total_ops > 0:
        logger.info(f"开始执行展平操作，总共 {total_ops} 项")
        for i, op in enumerate(op_queue):
            source = op["path"]
            target_dir = op["move_to"]

            logger.debug(f"处理第 {i + 1}/{total_ops} 项: {os.path.basename(source)}")

            # 检查重复并确定最终名称
            final_name = get_unique_name(target_dir, op["base_name"], op["original_ext"])
            target_path = os.path.join(target_dir, final_name)

            # 执行队列项
            try:
                logger.info(f"移动文件: {os.path.basename(source)} -> {final_name}")
                shutil.move(source, target_path)
                progress = int(((i + 1) / total_ops) * 100)
                logger.debug(f"移动完成，进度: {progress}%")
                yield progress
            except Exception as e:
                progress = int(((i + 1) / total_ops) * 100)
                logger.error(f"无法移动 {source} 到 {target_path}: {e}")
                logger.exception("移动文件时发生异常")
                yield progress
    else:
        logger.warning("没有需要移动的文件")
        yield 100

    logger.info("文件展平处理完成")


def process_cleanup(root_path: str) -> None:
    """
    清理空文件夹
    Args:
        root_path: 要展平的文件夹

    Returns:
        None
    """
    logger.info(f"开始清理空文件夹，根路径: {root_path}")
    root_node = build_tree(root_path)
    cleanup_queue = []
    recorded_nodes = set()

    # 寻找目录类型且无子结点的节点C
    logger.info("正在扫描空文件夹...")
    leaf_dirs = [node for node in root_node.descendants if not node.is_file and len(node.children) == 0]
    logger.debug(f"找到 {len(leaf_dirs)} 个叶子目录")

    for node_c in leaf_dirs:
        logger.debug(f"处理叶子目录: {node_c.name}")
        # 从C向上查找结点D
        current = node_c
        node_d = None

        while current and not current.is_root:
            parent = current.parent
            if not parent:
                logger.debug("父节点为空，终止循环")
                break

            # 检查父级是否满足停止条件
            parent_dir_children = [n for n in parent.children if not n.is_file]
            if len(parent_dir_children) > 1:
                node_d = current
                logger.debug(f"找到分支节点，停止条件1: {parent.name} 有 {len(parent_dir_children)} 个子目录")
                break

            if any(n.is_file for n in parent.children):
                node_d = current
                logger.debug(f"找到包含文件的节点，停止条件2: {parent.name} 包含文件")
                break

            current = parent

        if node_d is None:
            if current.is_root:
                node_d = current.children[0] if current.children else node_c
                logger.debug(f"到达根节点，设置node_d为: {node_d.name}")

        if node_d and node_d.abs_path not in recorded_nodes:
            cleanup_queue.append(node_d.abs_path)
            recorded_nodes.add(node_d.abs_path)
            logger.debug(f"添加到清理队列: {node_d.abs_path}")

    logger.info(f"扫描完成，需要清理的空文件夹数: {len(cleanup_queue)}")

    if cleanup_queue:
        logger.info(f"开始发送 {len(cleanup_queue)} 个空文件夹到回收站")
        try:
            cleanup_queue = [os.path.normpath(i) for i in cleanup_queue]
            logger.debug(f"清理队列路径规范化完成")
            send2trash(cleanup_queue)
            logger.info(f"已成功发送所有空文件夹到回收站")
        except Exception as e:
            logger.error(f"无法清理空文件夹: {str(e)}")
            logger.exception("清理空文件夹时发生异常")
    else:
        logger.info("没有需要清理的空文件夹")

    logger.info("空文件夹清理操作完成")
    return None
