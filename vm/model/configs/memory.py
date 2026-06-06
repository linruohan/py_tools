from dataclasses import dataclass


@dataclass
class Memory:
    """内存配置"""

    size: int
    unit: str | None = None  # b, bytes, KB, k, KiB, MB, M, MiB, GB, G, GiB, TB, T, TiB
    dumpCore: bool | None = None


@dataclass
class MaxMemory:
    """最大内存配置"""

    size: int
    unit: str | None = None
    slots: int | None = None


@dataclass
class CurrentMemory:
    """当前内存配置"""

    size: int
    unit: str | None = None
