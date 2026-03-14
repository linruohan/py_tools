from dataclasses import dataclass
from typing import Optional


@dataclass
class Memory:
    """内存配置"""

    size: int
    unit: Optional[str] = None  # b, bytes, KB, k, KiB, MB, M, MiB, GB, G, GiB, TB, T, TiB
    dumpCore: Optional[bool] = None


@dataclass
class MaxMemory:
    """最大内存配置"""

    size: int
    unit: Optional[str] = None
    slots: Optional[int] = None


@dataclass
class CurrentMemory:
    """当前内存配置"""

    size: int
    unit: Optional[str] = None
