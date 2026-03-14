from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class Feature:
    """特性配置"""

    name: str
    policy: Optional[str] = None  # require, optional, disable
    present: Optional[bool] = None
    state: Optional[str] = None  # on, off


@dataclass
class Features:
    """特性集合配置"""

    features: List[Feature] = field(default_factory=list)
