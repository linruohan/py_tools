from dataclasses import dataclass, field
from typing import Optional


@dataclass
class VCPU:
    """虚拟 CPU 配置"""

    count: int
    placement: Optional[str] = None  # static or auto
    cpuset: Optional[str] = None
    current: Optional[int] = None


@dataclass
class VCPUInstance:
    """单个 VCPU 实例配置"""

    id: int
    enabled: bool
    hotpluggable: bool
    order: Optional[int] = None


@dataclass
class VCPUs:
    """VCPU 集合配置"""

    vcpus: list[VCPUInstance] = field(default_factory=list)
