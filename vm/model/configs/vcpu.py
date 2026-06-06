from dataclasses import dataclass, field


@dataclass
class VCPU:
    """虚拟 CPU 配置"""

    count: int
    placement: str | None = None  # static or auto
    cpuset: str | None = None
    current: int | None = None


@dataclass
class VCPUInstance:
    """单个 VCPU 实例配置"""

    id: int
    enabled: bool
    hotpluggable: bool
    order: int | None = None


@dataclass
class VCPUs:
    """VCPU 集合配置"""

    vcpus: list[VCPUInstance] = field(default_factory=list)
