"""日志系统模块"""

import logging

from datetime import datetime
from pathlib import Path


def setup_logger(
    name: str = 'py_tools',
    level: int = logging.INFO,
    log_to_file: bool = True,
    log_to_console: bool = True,
) -> logging.Logger:
    """配置日志系统

    Args:
        name: 日志记录器名称
        level: 日志级别
        log_to_file: 是否输出到文件
        log_to_console: 是否输出到控制台

    Returns:
        配置好的日志记录器
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # 避免重复添加处理器
    if logger.handlers:
        return logger

    # 格式化器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
    )

    # 文件处理器
    if log_to_file:
        log_dir = Path.home() / '.py_tools' / 'logs'
        log_dir.mkdir(parents=True, exist_ok=True)

        # 日志文件(按日期)
        log_file = log_dir / f'app_{datetime.now():%Y%m%d}.log'

        fh = logging.FileHandler(log_file, encoding='utf-8')
        fh.setLevel(level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    # 控制台处理器(仅警告及以上)
    if log_to_console:
        ch = logging.StreamHandler()
        ch.setLevel(logging.WARNING)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    return logger


def get_logger(name: str | None = None) -> logging.Logger:
    """获取日志记录器

    Args:
        name: 日志记录器名称,默认使用调用模块的名称

    Returns:
        日志记录器
    """
    if name is None:
        import inspect

        frame = inspect.currentframe()
        if frame and frame.f_back:
            name = frame.f_back.f_globals.get('__name__', 'py_tools')
        else:
            name = 'py_tools'

    return logging.getLogger(name)
