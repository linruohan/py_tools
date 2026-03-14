from dataclasses import dataclass, field
from typing import Optional, List


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
    unit: Optional[str] = None  # KiB, MiB, GiB, TiB


@dataclass
class CacheMonitor:
    """缓存监控配置"""

    level: int
    vcpus: str


@dataclass
class CacheTune:
    """缓存调优配置"""

    vcpus: str
    caches: List[Cache] = field(default_factory=list)
    monitors: List[CacheMonitor] = field(default_factory=list)
    id: Optional[int] = None


@dataclass
class MemoryNode:
    """内存节点配置"""

    id: int
    bandwidth: int


@dataclass
class MemoryTune:
    """内存调优配置"""

    vcpus: str
    nodes: List[MemoryNode] = field(default_factory=list)


@dataclass
class VCpuSched:
    """VCPU 调度配置"""

    scheduler: str  # batch, idle, fifo, rr
    vcpus: Optional[str] = None
    priority: Optional[int] = None


@dataclass
class IOThreadSched:
    """IOThread 调度配置"""

    scheduler: str  # batch, idle, fifo, rr
    iothreads: Optional[str] = None
    priority: Optional[int] = None


@dataclass
class EmulatorSched:
    """模拟器调度配置"""

    scheduler: str  # batch, idle, fifo, rr
    priority: Optional[int] = None


@dataclass
class CpuTune:
    """CPU 调优配置"""

    vcpu_pins: List[VCPUPin] = field(default_factory=list)
    emulator_pin: Optional[EmulatorPin] = None
    iothread_pins: List[IOThreadPin] = field(default_factory=list)
    shares: Optional[int] = None
    period: Optional[int] = None
    quota: Optional[int] = None
    global_period: Optional[int] = None
    global_quota: Optional[int] = None
    emulator_period: Optional[int] = None
    emulator_quota: Optional[int] = None
    iothread_period: Optional[int] = None
    iothread_quota: Optional[int] = None
    vcpu_sched: Optional[VCpuSched] = None
    iothread_sched: Optional[IOThreadSched] = None
    emulator_sched: Optional[EmulatorSched] = None
    cache_tunes: List[CacheTune] = field(default_factory=list)
    memory_tunes: List[MemoryTune] = field(default_factory=list)
