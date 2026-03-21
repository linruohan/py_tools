"""CPU 模型定义."""

from __future__ import annotations

from dataclasses import dataclass, field

from .topology import CPUTopology


@dataclass
class CPUFeature:
    """CPU 特性

    Attributes:
        name: 特性名称
        policy: 策略 (require, optional, force, disable, forbid)
        present: 是否存在
    """

    name: str
    policy: str | None = None  # require, optional, force, disable, forbid
    present: bool | None = None


@dataclass
class CPUModel:
    """CPU 模型

    Attributes:
        name: CPU 模型名称 (如 core2duo, IvyBridge)
        fallback: 回退策略 (allow, forbid) - 是否允许回退到相似模型
        vendor: CPU 厂商标识 (如 Intel, AMD)
        vendor_id: CPU 厂商标识符 (12 字符，如 AuthenticAMD, GenuineIntel)
    """

    name: str
    fallback: str | None = None  # allow, forbid
    vendor: str | None = None
    vendor_id: str | None = None


@dataclass
class CPU:
    """CPU 配置

    Attributes:
        model: CPU 模型
        topology: CPU 拓扑结构
        features: CPU 特性列表
        mode: CPU 模式 (custom, host-model, host-passthrough, maximum)
        match: 匹配模式 (exact, minimum, strict)
        check: 检查模式 (none, partial, full)
        migratable: 可迁移性 (on, off)
        vendor_id: CPU 厂商标识符 (12 字符)
        cache: 缓存配置
        maxphysaddr: 物理地址配置
    """

    model: CPUModel | None = None
    topology: CPUTopology | None = None
    features: list[CPUFeature] = field(default_factory=list)
    mode: str | None = None  # custom, host-model, host-passthrough, maximum
    match: str | None = None  # exact, minimum, strict
    check: str | None = None  # none, partial, full
    migratable: str | None = None  # on, off
    vendor_id: str | None = None
    cache: dict | None = None
    maxphysaddr: dict | None = None
    placeholder: bool | None = None
