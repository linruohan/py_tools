from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class SiblingDistance:
    """NUMA 节点间距离"""

    id: int
    value: int


@dataclass
class NumaNode:
    """NUMA 节点"""

    id: int
    memory: Optional[int] = None
    unit: Optional[str] = None
    cpus: Optional[str] = None
    memAccess: Optional[str] = None  # shared, private
    discard: Optional[bool] = None
    distances: List[SiblingDistance] = field(default_factory=list)
    cache: List[dict] = field(default_factory=list)


@dataclass
class Latency:
    """延迟配置"""

    initiator: int
    target: int
    type: str  # access, read, write
    value: int
    cache: Optional[int] = None


@dataclass
class Bandwidth:
    """带宽配置"""

    initiator: int
    target: int
    type: str  # access, read, write
    value: int
    unit: Optional[str] = None


@dataclass
class NUMA:
    """NUMA 配置"""

    nodes: List[NumaNode] = field(default_factory=list)
    memAccess: Optional[str] = None  # shared, private
    interconnects: List[dict] = field(default_factory=list)
    latencies: List[Latency] = field(default_factory=list)
    bandwidths: List[Bandwidth] = field(default_factory=list)
