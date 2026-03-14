"""解析工具函数 - 提供各种数据解析功能.

这个模块包含了解析各种配置值的工具函数，
主要用于处理用户输入并转换为内部使用的数据格式。
"""

# 内存选项常量 - 统一在所有地方使用
MEMORY_OPTIONS = [
    '256M',
    '512M',
    '1G',
    '2G',
    '4G',
    '8G',
    '16G',
    '32G',
    '64G',
    '128G',
    '256G',
    '512G',
]

# 基础内存选项（用于简单场景）
MEMORY_OPTIONS_BASIC = ['1G', '2G', '4G', '8G', '16G', '32G', '64G', '128G']

# 内存单位换算因子（转换为 KiB）
MEMORY_UNIT_FACTORS = {
    'B': 1 / 1024,
    'BYTES': 1 / 1024,
    'B': 1 / 1024,
    'K': 1,
    'KB': 1,
    'KIB': 1,
    'M': 1024,
    'MB': 1024,
    'MIB': 1024,
    'G': 1024 * 1024,
    'GB': 1024 * 1024,
    'GIB': 1024 * 1024,
    'T': 1024 * 1024 * 1024,
    'TB': 1024 * 1024 * 1024,
    'TIB': 1024 * 1024 * 1024,
}


def parse_memory_value(value: str, default: int = 2048, target_unit: str = 'MiB') -> int:
    """解析内存值为指定单位的数值.

    支持各种单位后缀（B, K, M, G, T 及其变体），
    自动识别并转换为指定的目标单位。

    Args:
        value: 要解析的内存值字符串，如 '2G', '512M', '1024'
        default: 解析失败时返回的默认值
        target_unit: 目标单位，可选 'KiB', 'MiB', 'GiB', 'TiB'

    Returns:
        转换后的整数值

    Examples:
        >>> parse_memory_value('2G')
        2048
        >>> parse_memory_value('512M')
        512
        >>> parse_memory_value('1T')
        1048576
        >>> parse_memory_value('invalid', default=1024)
        1024
    """
    if not value:
        return default

    value = value.strip().upper()

    # 提取数值和单位
    numeric_part = ''
    unit_part = ''

    for char in value:
        if char.isdigit() or char == '.' or char == '-':
            numeric_part += char
        else:
            unit_part += char

    if not numeric_part:
        return default

    try:
        num_value = float(numeric_part)
    except ValueError:
        return default

    # 获取源单位的换算因子（转换为 KiB）
    source_factor = MEMORY_UNIT_FACTORS.get(unit_part, 1)  # 默认按 KiB 处理

    # 计算 KiB 值
    kib_value = num_value * source_factor

    # 转换为目标单位
    target_unit_upper = target_unit.upper()
    if target_unit_upper in ('K', 'KB', 'KIB'):
        return int(kib_value)
    elif target_unit_upper in ('M', 'MB', 'MIB'):
        return int(kib_value / 1024)
    elif target_unit_upper in ('G', 'GB', 'GIB'):
        return int(kib_value / (1024 * 1024))
    elif target_unit_upper in ('T', 'TB', 'TIB'):
        return int(kib_value / (1024 * 1024 * 1024))
    else:
        return int(kib_value)  # 默认返回 KiB


def parse_memory_to_kib(value: str, default: int = 2097152) -> int:
    """解析内存值为 KiB.

    这是 parse_memory_value 的便捷封装，专门用于获取 KiB 值。

    Args:
        value: 要解析的内存值字符串
        default: 解析失败时返回的默认值（默认 2GiB = 2097152 KiB）

    Returns:
        以 KiB 为单位的整数值

    Examples:
        >>> parse_memory_to_kib('2G')
        2097152
        >>> parse_memory_to_kib('512M')
        524288
    """
    return parse_memory_value(value, default=default, target_unit='KiB')


def parse_memory_to_mib(value: str, default: int = 2048) -> int:
    """解析内存值为 MiB.

    这是 parse_memory_value 的便捷封装，专门用于获取 MiB 值。

    Args:
        value: 要解析的内存值字符串
        default: 解析失败时返回的默认值（默认 2GiB = 2048 MiB）

    Returns:
        以 MiB 为单位的整数值

    Examples:
        >>> parse_memory_to_mib('2G')
        2048
        >>> parse_memory_to_mib('512M')
        512
    """
    return parse_memory_value(value, default=default, target_unit='MiB')


def format_memory_value(value: int, unit: str = 'MiB') -> str:
    """将内存值格式化为易读的字符串.

    Args:
        value: 内存数值
        unit: 数值的单位

    Returns:
        格式化后的字符串，如 '2G', '512M'

    Examples:
        >>> format_memory_value(2048, 'MiB')
        '2G'
        >>> format_memory_value(524288, 'KiB')
        '512M'
    """
    unit_upper = unit.upper()

    # 先统一转换为 KiB
    if unit_upper in ('K', 'KB', 'KIB'):
        kib_value = value
    elif unit_upper in ('M', 'MB', 'MIB'):
        kib_value = value * 1024
    elif unit_upper in ('G', 'GB', 'GIB'):
        kib_value = value * 1024 * 1024
    elif unit_upper in ('T', 'TB', 'TIB'):
        kib_value = value * 1024 * 1024 * 1024
    else:
        kib_value = value

    # 选择合适的单位显示
    if kib_value >= 1024 * 1024 * 1024 and kib_value % (1024 * 1024 * 1024) == 0:
        return f'{kib_value // (1024 * 1024 * 1024)}T'
    elif kib_value >= 1024 * 1024 and kib_value % (1024 * 1024) == 0:
        return f'{kib_value // (1024 * 1024)}G'
    elif kib_value >= 1024 and kib_value % 1024 == 0:
        return f'{kib_value // 1024}M'
    else:
        return f'{kib_value}K'


def parse_integer_value(
    value: str, default: int = 0, min_value: int = None, max_value: int = None
) -> int:
    """解析整数值，支持范围限制.

    Args:
        value: 要解析的字符串
        default: 解析失败时的默认值
        min_value: 最小值限制
        max_value: 最大值限制

    Returns:
        解析后的整数值

    Examples:
        >>> parse_integer_value('42')
        42
        >>> parse_integer_value('invalid', default=10)
        10
        >>> parse_integer_value('100', min_value=0, max_value=50)
        50
    """
    if not value:
        return default

    try:
        result = int(value.strip())
    except (ValueError, TypeError):
        return default

    if min_value is not None:
        result = max(result, min_value)
    if max_value is not None:
        result = min(result, max_value)

    return result


def parse_float_value(
    value: str, default: float = 0.0, min_value: float = None, max_value: float = None
) -> float:
    """解析浮点数值，支持范围限制.

    Args:
        value: 要解析的字符串
        default: 解析失败时的默认值
        min_value: 最小值限制
        max_value: 最大值限制

    Returns:
        解析后的浮点数值

    Examples:
        >>> parse_float_value('3.14')
        3.14
        >>> parse_float_value('invalid', default=1.0)
        1.0
    """
    if not value:
        return default

    try:
        result = float(value.strip())
    except (ValueError, TypeError):
        return default

    if min_value is not None:
        result = max(result, min_value)
    if max_value is not None:
        result = min(result, max_value)

    return result
