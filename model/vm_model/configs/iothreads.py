from dataclasses import dataclass, field


@dataclass
class PollConfig:
    """轮询配置"""

    max: int | None = None
    grow: int | None = None
    shrink: int | None = None


@dataclass
class IOThread:
    """IOThread 配置"""

    id: int
    thread_pool_min: int | None = None
    thread_pool_max: int | None = None
    poll: PollConfig | None = None


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

    thread_pool_min: int | None = None
    thread_pool_max: int | None = None
