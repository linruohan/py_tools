import random

# 预定义的鲜艳颜色列表 - 用于 Tab 文本随机化
TAB_TEXT_COLORS: list[str] = [
    '#FF6B6B',  # 珊瑚红
    '#4ECDC4',  # 青绿色
    '#45B7D1',  # 天蓝色
    '#96CEB4',  # 薄荷绿
    '#FFEAA7',  # 淡黄色
    '#DDA0DD',  # 梅花色
    '#98D8C8',  # 海泡绿
    '#F7DC6F',  # 柠檬黄
    '#BB8FCE',  # 薰衣草紫
    '#85C1E2',  # 浅蓝色
    '#F8B739',  # 金黄色
    '#6C5CE7',  # 紫罗兰
    '#A29BFE',  # 淡紫色
    '#FD79A8',  # 粉红色
    '#FDCB6E',  # 琥珀色
    '#6C5CE7',  # 蓝紫色
    '#00B894',  # 翠绿色
    '#E17055',  # 橙红色
    '#74B9FF',  # 亮蓝色
    '#A8E6CF',  # 浅薄荷绿
    '#FF8B94',  # 浅珊瑚色
    '#C7CEEA',  # 淡蓝紫色
    '#B4A7D6',  # 淡紫罗兰
    '#81ECEC',  # 青色
]


def get_random_color() -> str:
    """获取随机 Tab 文本颜色.

    Returns:
        随机颜色十六进制字符串
    """
    return random.choice(TAB_TEXT_COLORS)
