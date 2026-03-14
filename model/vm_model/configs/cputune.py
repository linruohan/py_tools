from dataclasses import dataclass, field


@dataclass
class VCPUPin:
    """VCPU 绑定配置"""

    vcpu: int
    cpuset: str


@dataclass
class EmulatorPin:
    """模拟器绑定配置"""

    cpuset: str


@dataclass
class IOThreadPin:
    """IOThread 绑定配置"""

    iothread: int
    cpuset: str


@dataclass
class Cache:
    """缓存配置"""

    id: int
    level: int
    type: str  # code, data, both
    size: int
    unit: str | None = None  # KiB, MiB, GiB, TiB


@dataclass
class CacheMonitor:
    """缓存监控配置"""

    level: int
    vcpus: str


@dataclass
class CacheTune:
    """缓存调优配置"""

    vcpus: str
    caches: list[Cache] = field(default_factory=list)
    monitors: list[CacheMonitor] = field(default_factory=list)
    id: int | None = None


@dataclass
class MemoryNode:
    """内存节点配置"""

    id: int
    bandwidth: int


@dataclass
class MemoryTune:
    """内存调优配置"""

    vcpus: str
    nodes: list[MemoryNode] = field(default_factory=list)


@dataclass
class VCpuSched:
    """VCPU 调度配置"""

    scheduler: str  # batch, idle, fifo, rr
    vcpus: str | None = None
    priority: int | None = None


@dataclass
class IOThreadSched:
    """IOThread 调度配置"""

    scheduler: str  # batch, idle, fifo, rr
    iothreads: str | None = None
    priority: int | None = None


@dataclass
class EmulatorSched:
    """模拟器调度配置"""

    scheduler: str  # batch, idle, fifo, rr
    priority: int | None = None


@dataclass
class CpuTune:
    """CPU 调优配置"""

    vcpu_pins: list[VCPUPin] = field(default_factory=list)
    emulator_pin: EmulatorPin | None = None
    iothread_pins: list[IOThreadPin] = field(default_factory=list)
    shares: int | None = None
    period: int | None = None
    quota: int | None = None
    global_period: int | None = None
    global_quota: int | None = None
    emulator_period: int | None = None
    emulator_quota: int | None = None
    iothread_period: int | None = None
    iothread_quota: int | None = None
    vcpu_sched: VCpuSched | None = None
    iothread_sched: IOThreadSched | None = None
    emulator_sched: EmulatorSched | None = None
    cache_tunes: list[CacheTune] = field(default_factory=list)
    memory_tunes: list[MemoryTune] = field(default_factory=list)
