from dataclasses import dataclass, field


@dataclass
class Resource:
    """资源配置"""

    name: str
    value: int
    unit: str | None = None


@dataclass
class FibreChannel:
    """光纤通道配置"""

    appid: str


@dataclass
class Resources:
    """资源集合配置"""

    resources: list[Resource] = field(default_factory=list)
    partition: str | None = None
    fibrechannel: FibreChannel | None = None
