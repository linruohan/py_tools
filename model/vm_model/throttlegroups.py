from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class ThrottleGroup:
    """节流组配置"""

    name: str
    cpu_shares: Optional[int] = None
    cpu_period: Optional[int] = None
    cpu_quota: Optional[int] = None
    memory_hard_limit: Optional[int] = None
    memory_soft_limit: Optional[int] = None
    blkio_weight: Optional[int] = None


@dataclass
class ThrottleGroups:
    """节流组集合配置"""

    throttlegroups: List[ThrottleGroup] = field(default_factory=list)
