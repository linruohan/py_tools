from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class MemNode:
    """内存节点配置"""

    cellid: int
    mode: Optional[str] = None  # strict, preferred, interleave, restrictive
    nodeset: Optional[str] = None


@dataclass
class NumaTune:
    """NUMA 节点调优配置"""

    memory_mode: Optional[str] = None  # strict, preferred, interleave, restrictive
    memory_nodeset: Optional[str] = None
    memory_placement: Optional[str] = None  # static, auto
    memnodes: List[MemNode] = field(default_factory=list)
