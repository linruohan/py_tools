from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class CPUFeature:
    """CPU 特性"""

    name: str
    policy: Optional[str] = None  # require, optional, disable
    present: Optional[bool] = None


@dataclass
class CPUModel:
    """CPU 模型"""

    name: str
    fallback: Optional[str] = None  # allow, forbid, require
    check: Optional[bool] = None


@dataclass
class CPUTopology:
    """CPU 拓扑"""

    sockets: int
    cores: int
    threads: int


@dataclass
class CPU:
    """CPU 配置"""

    model: Optional[CPUModel] = None
    topology: Optional[CPUTopology] = None
    features: List[CPUFeature] = field(default_factory=list)
    mode: Optional[str] = None  # custom, host-model, host-passthrough
    match: Optional[str] = None  # exact, minimum, strict
    vendor_id: Optional[str] = None
    placeholder: Optional[bool] = None
