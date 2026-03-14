from dataclasses import dataclass


@dataclass
class MemTune:
    """内存调优配置"""

    hard_limit: int | None = None
    hard_limit_unit: str | None = None  # b, bytes, KB, k, KiB, MB, M, MiB, GB, G, GiB, TB, T, TiB
    soft_limit: int | None = None
    soft_limit_unit: str | None = None
    swap_hard_limit: int | None = None
    swap_hard_limit_unit: str | None = None
    min_guarantee: int | None = None
    min_guarantee_unit: str | None = None
