import json
import os.path

import charset_normalizer


class JSONSorter:
    @staticmethod
    def sort_dict_recursive(d):
        if isinstance(d, dict):
            return {k: JSONSorter.sort_dict_recursive(v) for k, v in sorted(d.items())}
        elif isinstance(d, list):
            return [JSONSorter.sort_dict_recursive(item) for item in d]
        else:
            return d

    @staticmethod
    def process(json_path):
        if not os.path.exists(json_path):
            return f"文件不存在：{json_path}"
        with open(json_path, 'rb') as file:
            content_bytes = file.read()

        encoding_info = charset_normalizer.detect(content_bytes)
        print("检测到的编码信息：", encoding_info)
        encoding = encoding_info['encoding'] if encoding_info else 'utf-8'

        try:
            with open(json_path, 'r', encoding=encoding) as f:
                doc = json.load(f)
        except PermissionError:
            return "没有权限读取文件"
        except Exception as e:
            return f"读取失败：{str(e)}"

        sorted_doc = JSONSorter.sort_dict_recursive(doc)

        try:
            with open(json_path, 'w', encoding=encoding) as sorted_json:
                json.dump(sorted_doc, sorted_json, ensure_ascii=False, indent=4)
        except PermissionError:
            return "没有权限写入文件"
        except Exception as e:
            return f"保存失败：{str(e)}"

        return "JSON 文件已排序，文件已保存到原文件"


def main(json_path: str):
    return JSONSorter.process(json_path)
