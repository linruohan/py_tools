from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class PerfEvent:
    """性能事件配置"""

    name: str
    enabled: bool
    period: Optional[int] = None
    freq: Optional[int] = None
    config: Optional[str] = None
    config1: Optional[str] = None
    config2: Optional[str] = None


@dataclass
class Perf:
    """性能配置"""

    events: List[PerfEvent] = field(default_factory=list)
