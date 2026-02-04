from enum import Enum


class ErrorCodeBase(Enum):
    """
    通用错误码枚举类基类
    """
    def __init__(self, code: int, message_template: str, generic_msg: str = ""):
        self._code = code
        self._message_template = message_template
        self._generic_msg = generic_msg if generic_msg else self._message_template

    @property
    def code(self) -> int:
        """错误码数值"""
        return self._code

    @property
    def generic(self) -> str:
        """不支持格式化的通用消息"""
        return self._generic_msg

    def format(self, msg: str = "") -> str:
        """
        格式化错误消息
        - 如果模板没有 {item} 占位符，直接返回模板
        - 如果模板有 {item} 占位符，用 msg 填充
        """
        try:
            return self._message_template.format(item=msg)
        except (KeyError, ValueError):
            return self._message_template

    def __str__(self) -> str:
        return f"[{self._code}] {self._generic_msg}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}.{self.name}"

class ErrorCode(ErrorCodeBase):
    """
    通用错误码类
    """
    Success = (0, "操作成功完成")
    Unknown = (1, "未知错误：{item}", "未知错误")
    ZeroDivision = (2, "出现了除零错误，因为 {item}", "除零错误")
    EmptyString = (3, "输入包含空字符串")
    InvalidPath = (4, "输入路径为空或不存在：{item}", "输入路径为空或不存在")
    InvalidRatio = (5, "无效的比例值：{item}", "输入的比例无效")
    FileExists = (6, "文件 {item} 已存在，跳过此项", "输出文件已存在")
    CannotReadFile = (7, "无法读取文件：{item}", "无法读取文件")
    CannotWriteFile = (8, "无法写入文件：{item}", "无法写入文件")