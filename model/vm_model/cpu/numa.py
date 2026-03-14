from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class NumaNode:
    """NUMA 节点"""

    id: int
    memory: Optional[int] = None
    unit: Optional[str] = None
    cpus: Optional[str] = None


@dataclass
class NUMA:
    """NUMA 配置"""

    nodes: List[NumaNode] = field(default_factory=list)
    memAccess: Optional[str] = None  # shared, private
