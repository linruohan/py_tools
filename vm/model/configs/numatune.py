from dataclasses import dataclass, field


@dataclass
class MemNode:
    """内存节点配置"""

    cellid: int
    mode: str | None = None  # strict, preferred, interleave, restrictive
    nodeset: str | None = None


@dataclass
class NumaTune:
    """NUMA 节点调优配置"""

    memory_mode: str | None = None  # strict, preferred, interleave, restrictive
    memory_nodeset: str | None = None
    memory_placement: str | None = None  # static, auto
    memnodes: list[MemNode] = field(default_factory=list)
