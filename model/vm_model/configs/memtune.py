from dataclasses import dataclass
from typing import Optional


@dataclass
class MemTune:
    """内存调优配置"""

    hard_limit: Optional[int] = None
    hard_limit_unit: Optional[str] = (
        None  # b, bytes, KB, k, KiB, MB, M, MiB, GB, G, GiB, TB, T, TiB
    )
    soft_limit: Optional[int] = None
    soft_limit_unit: Optional[str] = None
    swap_hard_limit: Optional[int] = None
    swap_hard_limit_unit: Optional[str] = None
    min_guarantee: Optional[int] = None
    min_guarantee_unit: Optional[str] = None
