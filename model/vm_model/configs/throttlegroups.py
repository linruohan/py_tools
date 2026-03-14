from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class ThrottleGroup:
    """节流组配置"""

    name: str
    total_bytes_sec: Optional[int] = None
    read_bytes_sec: Optional[int] = None
    write_bytes_sec: Optional[int] = None
    read_iops_sec: Optional[int] = None
    write_iops_sec: Optional[int] = None
    total_iops_sec: Optional[int] = None


@dataclass
class ThrottleGroups:
    """节流组集合配置"""

    throttlegroups: List[ThrottleGroup] = field(default_factory=list)
