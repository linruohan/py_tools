from dataclasses import dataclass, field


@dataclass
class CPUFeature:
    """CPU 特性"""

    name: str
    policy: str | None = None  # require, optional, disable
    present: bool | None = None


@dataclass
class CPUModel:
    """CPU 模型"""

    name: str
    fallback: str | None = None  # allow, forbid, require
    check: bool | None = None


@dataclass
class CPUTopology:
    """CPU 拓扑"""

    sockets: int
    cores: int
    threads: int


@dataclass
class CPU:
    """CPU 配置"""

    model: CPUModel | None = None
    topology: CPUTopology | None = None
    features: list[CPUFeature] = field(default_factory=list)
    mode: str | None = None  # custom, host-model, host-passthrough, maximum
    match: str | None = None  # exact, minimum, strict
    vendor_id: str | None = None
    placeholder: bool | None = None
