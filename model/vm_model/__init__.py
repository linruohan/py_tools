# 导出所有配置类
from .os import (
    OS,
    FirmwareFeature,
    Loader,
    Nvram,
    NvramSource,
    Varstore,
    Boot,
    Smbios,
    Bootmenu,
    Bios,
    Acpi,
    AcpiTable,
    Idmap,
    IdmapEntry,
)
from .sysinfo import SysInfo, SMBIOSBIOS, SMBIOSSystem, SMBIOSBaseBoard, SMBIOSChassis, FWCFGEntry
from .vcpu import VCPU, VCPUInstance, VCPUs
from .iothreads import IOThreads, IOThread, IOThreadIDs, DefaultIOThread, PollConfig
from .cputune import (
    CpuTune,
    VCPUPin,
    EmulatorPin,
    IOThreadPin,
    Cache,
    CacheMonitor,
    CacheTune,
    MemoryNode,
    MemoryTune,
    VCpuSched,
    IOThreadSched,
    EmulatorSched,
)
from .memoryBacking import MemoryBacking, HugePage
from .memtune import MemTune
from .numatune import NumaTune, MemNode as NumaMemNode
from .blkiotune import BlkioTune, WeightDevice, DeviceIopsLimit, DeviceBytesLimit
from .clock import Clock, Timer
from .features import Features, Feature
from .pm import PM
from .seclabel import SecLabels, SecLabel
from .keywrap import KeyWrap
from .launchSecurity import LaunchSecurity
from .metadata import Metadata
from .perf import Perf, PerfEvent
from .resource import Resources, Resource
from .throttlegroups import ThrottleGroups, ThrottleGroup
from .memory import Memory, MaxMemory, CurrentMemory
from .domain import (
    Domain,
    # 新增整合类
    VirtType,
    OSType,
    MachineType,
    CpuMode,
    CPUTopology,
    CPUModel,
    CPUFeature,
    CPU,
    VCPU as NewVCPU,
    Memory as NewMemory,
    MaxMemory as NewMaxMemory,
    CurrentMemory as NewCurrentMemory,
    Boot as NewBoot,
    Bootmenu as NewBootmenu,
    Loader as NewLoader,
    Nvram as NewNvram,
    OS as NewOS,
    Disk,
    Graphics,
    Video,
    NetworkInterface,
    Devices as NewDevices,
    Features as NewFeatures,
    Clock as NewClock,
)
from .devices import Devices

# 导出设备类
from .devices.disk import Disk as LegacyDisk
from .devices.graphics import Graphics as LegacyGraphics
from .devices.interface import Interface as LegacyInterface
from .devices.video import Video as LegacyVideo
from .devices.audio import Audio
from .devices.channel import Channel
from .devices.console import Console
from .devices.controller import Controller
from .devices.crypto import Crypto
from .devices.driver import Driver
from .devices.filesystem import Filesystem
from .devices.hostdev import Hostdev
from .devices.iommu import IOMMU
from .devices.memballoon import Memballoon
from .devices.memory import Memory as DeviceMemory
from .devices.nvram import Nvram as DeviceNvram
from .devices.panic import Panic
from .devices.parallel import Parallel
from .devices.pstore import Pstore
from .devices.rng import Rng
from .devices.serial import Serial
from .devices.shmem import Shmem
from .devices.smartcard import Smartcard
from .devices.sound import Sound
from .devices.tpm import TPM
from .devices.vsock import Vsock
from .devices.watchdog import Watchdog

__all__ = [
    # 核心域配置
    'Domain',
    # 新增整合类
    'VirtType',
    'OSType',
    'MachineType',
    'CpuMode',
    'CPUTopology',
    'CPUModel',
    'CPUFeature',
    'CPU',
    'NewVCPU',
    'NewMemory',
    'NewMaxMemory',
    'NewCurrentMemory',
    'NewBoot',
    'NewBootmenu',
    'NewLoader',
    'NewNvram',
    'NewOS',
    'Disk',
    'Graphics',
    'Video',
    'NetworkInterface',
    'NewDevices',
    'NewFeatures',
    'NewClock',
    # OS 相关
    'OS',
    'FirmwareFeature',
    'Loader',
    'Nvram',
    'NvramSource',
    'Varstore',
    'Boot',
    'Smbios',
    'Bootmenu',
    'Bios',
    'Acpi',
    'AcpiTable',
    'Idmap',
    'IdmapEntry',
    # SysInfo 相关
    'SysInfo',
    'SMBIOSBIOS',
    'SMBIOSSystem',
    'SMBIOSBaseBoard',
    'SMBIOSChassis',
    'FWCFGEntry',
    # VCPU 相关
    'VCPU',
    'VCPUInstance',
    'VCPUs',
    # IOThreads 相关
    'IOThreads',
    'IOThread',
    'IOThreadIDs',
    'DefaultIOThread',
    'PollConfig',
    # CPU 调优相关
    'CpuTune',
    'VCPUPin',
    'EmulatorPin',
    'IOThreadPin',
    'Cache',
    'CacheMonitor',
    'CacheTune',
    'MemoryNode',
    'MemoryTune',
    'VCpuSched',
    'IOThreadSched',
    'EmulatorSched',
    # 内存相关
    'Memory',
    'MaxMemory',
    'CurrentMemory',
    'MemoryBacking',
    'HugePage',
    'MemTune',
    'NumaTune',
    'NumaMemNode',
    # 块 IO 调优相关
    'BlkioTune',
    'WeightDevice',
    'DeviceIopsLimit',
    'DeviceBytesLimit',
    # 时钟相关
    'Clock',
    'Timer',
    # 特性相关
    'Features',
    'Feature',
    # 电源管理相关
    'PM',
    # 安全标签相关
    'SecLabels',
    'SecLabel',
    # 密钥包装相关
    'KeyWrap',
    # 启动安全相关
    'LaunchSecurity',
    # 元数据相关
    'Metadata',
    # 性能相关
    'Perf',
    'PerfEvent',
    # 资源相关
    'Resources',
    'Resource',
    # 节流组相关
    'ThrottleGroups',
    'ThrottleGroup',
    # CPU 相关
    'CPU',
    'CPUTopology',
    'CPUModel',
    'CPUFeature',
    'NUMA',
    'NumaNode',
    # 设备相关
    'Devices',
    # 具体设备类
    'Disk',
    'Graphics',
    'Video',
    'NetworkInterface',
    'Audio',
    'Channel',
    'Console',
    'Controller',
    'Crypto',
    'Driver',
    'Filesystem',
    'Hostdev',
    'IOMMU',
    'Memballoon',
    'DeviceMemory',
    'DeviceNvram',
    'Panic',
    'Parallel',
    'Pstore',
    'Rng',
    'Serial',
    'Shmem',
    'Smartcard',
    'Sound',
    'TPM',
    'Vsock',
    'Watchdog',
    # 传统设备类（兼容）
    'LegacyDisk',
    'LegacyGraphics',
    'LegacyInterface',
    'LegacyVideo',
]
