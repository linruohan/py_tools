"""CPU 模型定义."""

from __future__ import annotations

from dataclasses import dataclass, field

from .topology import CPUTopology


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
class CPU:
    """CPU 配置"""

    model: CPUModel | None = None
    topology: CPUTopology | None = None
    features: list[CPUFeature] = field(default_factory=list)
    mode: str | None = None  # custom, host-model, host-passthrough, maximum
    match: str | None = None  # exact, minimum, strict
    vendor_id: str | None = None
    placeholder: bool | None = None
