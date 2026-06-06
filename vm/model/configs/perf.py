from dataclasses import dataclass, field


@dataclass
class PerfEvent:
    """性能事件配置"""

    name: str
    enabled: bool
    period: int | None = None
    freq: int | None = None
    config: str | None = None
    config1: str | None = None
    config2: str | None = None


@dataclass
class Perf:
    """性能配置"""

    events: list[PerfEvent] = field(default_factory=list)
