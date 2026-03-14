from dataclasses import dataclass, field
from typing import Optional


@dataclass
class PollConfig:
    """轮询配置"""

    max: Optional[int] = None
    grow: Optional[int] = None
    shrink: Optional[int] = None


@dataclass
class IOThread:
    """IOThread 配置"""

    id: int
    thread_pool_min: Optional[int] = None
    thread_pool_max: Optional[int] = None
    poll: Optional[PollConfig] = None


@dataclass
class IOThreads:
    """IOThreads 分配配置"""

    count: int


@dataclass
class IOThreadIDs:
    """IOThread ID 配置"""

    iothreads: list[IOThread] = field(default_factory=list)


@dataclass
class DefaultIOThread:
    """默认 IOThread 配置"""

    thread_pool_min: Optional[int] = None
    thread_pool_max: Optional[int] = None
