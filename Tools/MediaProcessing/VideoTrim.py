import os

from PySide6.QtCore import QTime
from ffmpy import FFmpeg, FFRuntimeError, FFExecutableNotFoundError

from Core import log_manager
from Core.error_codes import ErrorCode

logger = log_manager.get_logger(__name__)


def trim_video(input_path: str, input_time: QTime, output_path: str = "", preserve: int = 0) -> tuple[ErrorCode, str]:
    """
    调用 FFmpeg 对视频进行无损剪辑。

    Args:
        input_path: 输入视频文件的路径。
        input_time: 剪切的时间点。
        output_path: 输出文件路径。如果为空，则根据规则自动生成。
        preserve: 保留模式。0 为保留该时间点之前的内容，1 为保留该时间点之后的内容。

    Returns:
        tuple[ErrorCode, str]: 返回错误码和最终输出的文件路径。
    """
    logger.info(f"剪切 {input_path}，时间点：{input_time}，保留：{preserve}")
    if not input_path or not os.path.isfile(input_path):
        logger.error(f"输入路径为空或不是一个文件：{input_path}")
        return ErrorCode.InvalidPath, ""
    elif not output_path or not os.path.exists(os.path.dirname(output_path)):
        logger.error(ErrorCode.InvalidPath.format(output_path))
        return ErrorCode.InvalidPath, ""
    # 准备参数
    time_ffmpeg = input_time.toString("HH:mm:ss.zzz")
    if preserve == 0:
        output_options = f'-to {time_ffmpeg} -c copy'
    elif preserve == 1:
        output_options = f'-ss {time_ffmpeg} -c copy'
    else:
        logger.error(ErrorCode.InvalidArgument.format(f"{preserve} (期望 0 或 1)"))
        return ErrorCode.InvalidArgument, ""
    logger.debug(f"output: {output_options}, input: {input_path}")
    # 构建并执行 FFmpeg 命令
    try:
        logger.info(f"开始剪切 {input_path}")
        ff = FFmpeg(
            global_options="",
            inputs={input_path: None},
            outputs={output_path: output_options}
        )
        ff.run()
        logger.info(f"成功剪切 {input_path} 并保存到 {output_path}")
        return ErrorCode.Success, output_path
    except FFExecutableNotFoundError:
        logger.error(ErrorCode.NoFFmpeg)
        return ErrorCode.NoFFmpeg, ""
    except FFRuntimeError as e:
        logger.error(ErrorCode.FFRuntimeError.format(str(e)))
        return ErrorCode.FFRuntimeError, ""
