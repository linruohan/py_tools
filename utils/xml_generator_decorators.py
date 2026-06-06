"""XML 生成器装饰器 - 提供统一的异常处理和日志记录."""

from __future__ import annotations

import logging
from functools import wraps
from typing import TYPE_CHECKING, Any, Callable, ParamSpec, TypeVar

if TYPE_CHECKING:
    from collections.abc import Callable

# 使用模块级别的 logger，确保测试时能正确捕获
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# 类型变量
P = ParamSpec('P')
R = TypeVar('R')


def xml_generation_method(func: Callable[P, R]) -> Callable[P, R]:
    """XML 生成方法装饰器 - 自动处理异常和日志记录.

    Args:
        func: 被装饰的函数

    Returns:
        包装后的函数
    """

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        try:
            logger.debug(f"开始生成：{func.__name__}")
            result = func(*args, **kwargs)
            logger.debug(f"生成完成：{func.__name__}")
            return result
        except KeyError as e:
            error_msg = f"{func.__name__} 缺少必需的键：{e}"
            logger.error(error_msg)
            raise
        except TypeError as e:
            error_msg = f"{func.__name__} 类型错误：{e}"
            logger.error(error_msg)
            raise
        except ValueError as e:
            error_msg = f"{func.__name__} 值错误：{e}"
            logger.error(error_msg)
            raise
        except Exception as e:
            error_msg = f"{func.__name__} 未知错误：{type(e).__name__}: {e}"
            logger.exception(error_msg)
            raise

    return wrapper


def safe_xml_generation(default_return: Any = None) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """安全 XML 生成装饰器 - 捕获所有异常并返回默认值.

    Args:
        default_return: 异常时的默认返回值

    Returns:
        装饰器函数
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.warning(
                    f"{func.__name__} 生成失败，使用默认值：{type(e).__name__}: {e}"
                )
                return default_return  # type: ignore

        return wrapper

    return decorator


def validate_config_keys(required_keys: list[str]) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """验证配置键装饰器 - 检查必需的键是否存在.

    Args:
        required_keys: 必需的键列表

    Returns:
        装饰器函数
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            # 检查配置参数 (可能是第一个或第二个参数)
            config = None
            if len(args) > 0 and isinstance(args[0], dict):
                # 如果没有 self 参数，config 是第一个参数
                config = args[0]
            elif len(args) > 1 and isinstance(args[1], dict):
                # 如果有 self 参数，config 是第二个参数
                config = args[1]
            
            if config is not None:
                missing_keys = [key for key in required_keys if key not in config]
                if missing_keys:
                    warning_msg = (
                        f"{func.__name__} 缺少必需的键：{missing_keys}"
                    )
                    logger.warning(warning_msg)

            return func(*args, **kwargs)

        return wrapper

    return decorator
