from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class Resource:
    """资源配置"""

    name: str
    value: int
    unit: Optional[str] = None


@dataclass
class FibreChannel:
    """光纤通道配置"""

    appid: str


@dataclass
class Resources:
    """资源集合配置"""

    resources: List[Resource] = field(default_factory=list)
    partition: Optional[str] = None
    fibrechannel: Optional[FibreChannel] = None
