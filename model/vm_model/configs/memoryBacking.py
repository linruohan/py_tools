from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class HugePage:
    """大页内存配置"""

    size: int
    unit: Optional[str] = None  # KiB, MiB, GiB, TiB
    nodeset: Optional[str] = None


@dataclass
class MemoryBacking:
    """内存后端配置"""

    hugepages: List[HugePage] = field(default_factory=list)
    nosharepages: Optional[bool] = None
    locked: Optional[bool] = None
    source_type: Optional[str] = None  # file, anonymous, memfd
    access_mode: Optional[str] = None  # shared, private
    allocation_mode: Optional[str] = None  # immediate, ondemand
    allocation_threads: Optional[int] = None
    discard: Optional[bool] = None
