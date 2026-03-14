from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class SecLabel:
    """安全标签配置"""

    type: str  # dynamic, static
    model: Optional[str] = None  # selinux, apparmor, smack, windows
    relabel: Optional[bool] = None
    label: Optional[str] = None
    imagelabel: Optional[str] = None
    baselabel: Optional[str] = None
    restriction: Optional[str] = None  # none, mandatory, advisory


@dataclass
class SecLabels:
    """安全标签集合配置"""

    seclabels: List[SecLabel] = field(default_factory=list)
