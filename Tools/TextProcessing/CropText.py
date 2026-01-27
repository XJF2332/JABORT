import os


def crop_text_file(source_path, output_path=None, percentage=50):
    """
    截取文本文件的后x%并保存

    Args:
        source_path (str): 源文件路径
        output_path (str, optional): 输出文件路径。若为None，则自动生成
        percentage (float): 截取比例(0-100)，表示截取后x%的内容

    Returns:
        str: 输出文件路径或错误信息
    """
    # 验证参数
    if not 0 <= percentage <= 100:
        return "截取比例必须在0-100之间"

    if not os.path.exists(source_path):
        return f"源文件不存在: {source_path}"

    # 如果未提供输出路径，自动生成
    if not output_path:
        base_name = os.path.splitext(os.path.basename(source_path))[0]
        extension = os.path.splitext(source_path)[1]
        output_path = os.path.join(
            os.path.dirname(source_path),
            f"{base_name}_crop_{percentage}{extension}"
        )

    # 检查输出文件是否已存在且不为空
    if os.path.exists(output_path):
        # 获取文件大小（字节数）
        file_size = os.path.getsize(output_path)
        if file_size > 0:
            return "不能覆盖已存在的文件"

    # 读取源文件内容
    try:
        with open(source_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        # 如果UTF-8解码失败，尝试使用系统默认编码
        try:
            with open(source_path, 'r', encoding='gbk') as f:
                lines = f.readlines()
        except UnicodeDecodeError:
            # 如果GBK也失败，尝试其他常见编码
            try:
                with open(source_path, 'r', encoding='latin-1') as f:
                    lines = f.readlines()
            except Exception as e:
                return f"解码失败：{str(e)}"
    except Exception as e:
        return f"读取文件失败：{str(e)}"

    # 计算要截取的起始行号
    if percentage == 0:
        cropped_lines = []
    elif percentage == 100:
        cropped_lines = lines
    else:
        start_index = int(len(lines) * (100 - percentage) / 100)
        cropped_lines = lines[start_index:]

    # 写入输出文件
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.writelines(cropped_lines)
    except Exception as e:
        return f"写入文件失败：{str(e)}"

    return f"文件已保存到{output_path}"