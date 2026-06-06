from dataclasses import dataclass, field


@dataclass
class SiblingDistance:
    """NUMA 节点间距离"""

    id: int
    value: int


@dataclass
class NumaNode:
    """NUMA 节点"""

    id: int
    memory: int | None = None
    unit: str | None = None
    cpus: str | None = None
    memAccess: str | None = None  # shared, private
    discard: bool | None = None
    distances: list[SiblingDistance] = field(default_factory=list)
    cache: list[dict] = field(default_factory=list)


@dataclass
class Latency:
    """延迟配置"""

    initiator: int
    target: int
    type: str  # access, read, write
    value: int
    cache: int | None = None


@dataclass
class Bandwidth:
    """带宽配置"""

    initiator: int
    target: int
    type: str  # access, read, write
    value: int
    unit: str | None = None


@dataclass
class NUMA:
    """NUMA 配置"""

    nodes: list[NumaNode] = field(default_factory=list)
    memAccess: str | None = None  # shared, private
    interconnects: list[dict] = field(default_factory=list)
    latencies: list[Latency] = field(default_factory=list)
    bandwidths: list[Bandwidth] = field(default_factory=list)
