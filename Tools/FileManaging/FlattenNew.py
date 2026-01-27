import os
import re
import shutil
from anytree import Node
from send2trash import send2trash


# 文件系统结点类
class FsNode(Node):
    def __init__(self, name, abs_path, is_file=False, parent=None):
        super().__init__(name, parent)
        self.abs_path = abs_path
        self.is_file = is_file


def build_tree(root_path):
    """构建文件系统的anytree结构"""
    root_path = os.path.abspath(root_path)
    root_name = os.path.basename(root_path)
    root_node = FsNode(root_name, root_path, is_file=False)

    # 使用字典记录路径对应的结点，方便挂载
    nodes_map = {root_path: root_node}

    for dirpath, dirnames, filenames in os.walk(root_path):
        current_node = nodes_map[dirpath]

        # 添加子目录
        for dirname in dirnames:
            full_path = os.path.join(dirpath, dirname)
            if os.path.isdir(full_path):
                child_node = FsNode(dirname, full_path, is_file=False, parent=current_node)
                nodes_map[full_path] = child_node

        # 添加文件
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            if os.path.isfile(full_path):
                FsNode(filename, full_path, is_file=True, parent=current_node)

    return root_node


def get_unique_name(target_dir, base_name, ext):
    """处理文件名重复，生成唯一的文件名"""
    target_name = f"{base_name}{ext}"
    list_dir = os.listdir(target_dir)

    if target_name not in list_dir:
        return target_name

    # 寻找最大的index
    max_index = 0
    pattern = re.compile(re.escape(base_name) + r"_(\d+)" + re.escape(ext))

    for item in list_dir:
        match = pattern.fullmatch(item)
        if match:
            index = int(match.group(1))
            if index > max_index:
                max_index = index

    return f"{base_name}_{max_index + 1}{ext}"


def process_flatten(root_path):
    """执行文件展平操作"""
    yield 0.0, f"[展平] 正在扫描路径: {root_path}"

    root_node = build_tree(root_path)
    op_queue = []

    # 遍历树寻找符合条件的结点
    for node in root_node.descendants:
        # 如果是目录，且只有一个子结点，且子结点是文件
        if not node.is_file and len(node.children) == 1:
            child = node.children[0]
            if child.is_file:
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
                        break

                    # 检查 parent_node 是否满足下列停止条件
                    # 是根目录
                    if parent_node.is_root:
                        node_b = parent_node
                        node_b1 = current_node
                        break
                    # 有超过一个的目录类型的子结点
                    parent_dir_children = [n for n in parent_node.children if not n.is_file]
                    if len(parent_dir_children) > 1:
                        node_b = parent_node
                        node_b1 = current_node
                        break
                    # 有文件类型的子结点 (排除当前处理分支)
                    parent_file_children = [n for n in parent_node.children if n.is_file]
                    # 检查是否有不在当前路径下的文件
                    if parent_file_children:
                        node_b = parent_node
                        node_b1 = current_node
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

    # 执行操作队列
    yield 0.0, f"[展平] 扫描完成，开始执行展平操作，共 {len(op_queue)} 项任务..."

    total_ops = len(op_queue)
    if total_ops > 0:
        for i, op in enumerate(op_queue):
            source = op["path"]
            target_dir = op["move_to"]

            # 检查重复并确定最终名称
            final_name = get_unique_name(target_dir, op["base_name"], op["original_ext"])
            target_path = os.path.join(target_dir, final_name)

            # 执行队列项
            try:
                shutil.move(source, target_path)
                progress = (i + 1) / total_ops
                yield progress, f"[展平] 移动：{os.path.basename(source)} -> {final_name}"
            except Exception as e:
                progress = (i + 1) / total_ops
                yield progress, f"[展平] 无法移动 {source} 到 {target_path}: {e}"
    else:
        yield 1.0, "[展平] 没有需要移动的文件"


def process_cleanup(root_path):
    """执行空文件夹清理"""
    yield 0.0, f"[展平] 正在扫描空文件夹..."

    root_node = build_tree(root_path)
    cleanup_queue = []
    recorded_nodes = set()

    # 寻找目录类型且无子结点的节点C
    leaf_dirs = [node for node in root_node.descendants if not node.is_file and len(node.children) == 0]

    for node_c in leaf_dirs:
        # 从C向上查找结点D
        current = node_c
        node_d = None

        while current and not current.is_root:
            parent = current.parent
            if not parent: break

            # 检查父级是否满足停止条件
            parent_dir_children = [n for n in parent.children if not n.is_file]
            if len(parent_dir_children) > 1:
                node_d = current
                break

            if any(n.is_file for n in parent.children):
                node_d = current
                break

            current = parent

        if node_d is None:
            if current.is_root:
                node_d = current.children[0] if current.children else node_c

        if node_d and node_d.abs_path not in recorded_nodes:
            cleanup_queue.append(node_d.abs_path)
            recorded_nodes.add(node_d.abs_path)

    yield 0.0, f"[展平] 扫描完成，开始清理空文件夹，共 {len(cleanup_queue)} 项..."

    if cleanup_queue:
        try:
            cleanup_queue = [os.path.normpath(i) for i in cleanup_queue]
            send2trash(cleanup_queue)
            yield 1.0, "[展平] 已发送到回收站"
        except Exception as e:
            yield 1.0, f"[展平] 删除出错：{str(e)}"
    else:
        yield 1.0, "[展平] 没有需要清理的空文件夹"
