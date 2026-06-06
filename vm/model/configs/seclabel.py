from dataclasses import dataclass, field


@dataclass
class SecLabel:
    """安全标签配置"""

    type: str  # dynamic, static
    model: str | None = None  # selinux, apparmor, smack, windows
    relabel: bool | None = None
    label: str | None = None
    imagelabel: str | None = None
    baselabel: str | None = None
    restriction: str | None = None  # none, mandatory, advisory


@dataclass
class SecLabels:
    """安全标签集合配置"""

    seclabels: list[SecLabel] = field(default_factory=list)
