from dataclasses import dataclass, field


@dataclass
class Metadata:
    """元数据配置"""

    name: str | None = None
    uuid: str | None = None
    description: str | None = None
    title: str | None = None
    os_type: str | None = None
    os_variant: str | None = None
    annotations: list[dict] = field(default_factory=list)
