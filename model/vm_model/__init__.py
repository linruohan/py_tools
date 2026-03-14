"""VM Model - KVM/QEMU 虚拟机配置模型."""

# 配置类
from .configs.basic_config import BasicConfig
from .configs.blkiotune import BlkioTune, DeviceBytesLimit, DeviceIopsLimit, WeightDevice
from .configs.clock import Clock, Timer
from .configs.cpu_allocation_config import CPUAllocationConfig
from .configs.cputune import CacheTune, CpuTune, EmulatorPin, IOThreadPin, MemoryTune, VCPUPin
from .configs.devices_config import DevicesConfig
from .configs.features import (
    ACPI,
    APIC,
    GIC,
    IOAPIC,
    PMU,
    SMM,
    Features,
    HypervFeature,
    KVMFeature,
    VMPort,
    XenFeature,
)
from .configs.iothreads import IOThread, IOThreadIDs, IOThreads
from .configs.keywrap import KeyWrap
from .configs.launchSecurity import LaunchSecurity
from .configs.memory import Memory as DomainMemory
from .configs.memory_allocation_config import MemoryAllocationConfig
from .configs.memoryBacking import HugePage, MemoryBacking
from .configs.memtune import MemTune
from .configs.metadata import Metadata
from .configs.numatune import MemNode, NumaTune
from .configs.os import OS, Bios, Boot, Bootmenu, Smbios
from .configs.os_booting_config import OSBootingConfig as OSConfig
from .configs.perf import Perf
from .configs.pm import PM
from .configs.seclabel import SecLabel, SecLabels
from .configs.sysinfo import SMBIOSBIOS, SMBIOSBaseBoard, SMBIOSChassis, SMBIOSSystem, SysInfo
from .configs.throttlegroups import ThrottleGroup, ThrottleGroups
from .configs.vcpu import VCPU

# 核心类
from .core.converter import DomainConfigConverter
from .core.domain import CpuMode, CPUTopology, Domain, MachineType, OSType, VirtType
from .core.vm_config import VMConfig

# CPU 相关
from .cpu import NUMA, NumaNode
from .cpu.cpu import CPU, CPUFeature

# 设备相关
from .devices import (
    IOMMU,
    TPM,
    Audio,
    BackendDomain,
    Channel,
    Console,
    Controller,
    Crypto,
    Disk,
    Driver,
    Filesystem,
    Graphics,
    Hostdev,
    Hub,
    Input,
    Interface,
    Memballoon,
    Nvram,
    Panic,
    Parallel,
    Pstore,
    Redirdev,
    Redirfilter,
    Rng,
    Serial,
    Shmem,
    Smartcard,
    Sound,
    UsbFilterRule,
    Video,
    Vsock,
    Watchdog,
)
from .devices import (
    Memory as MemoryDevice,
)

__all__ = [
    # 功能特性
    'ACPI',
    'APIC',
    # CPU 配置
    'CPU',
    'GIC',
    'IOAPIC',
    'IOMMU',
    # NUMA 配置
    'NUMA',
    'OS',
    # 电源管理
    'PM',
    'PMU',
    'SMBIOSBIOS',
    'SMM',
    'TPM',
    'VCPU',
    # 设备类型
    'Audio',
    'BackendDomain',
    # 设备配置
    'BasicConfig',
    # OS 配置
    'Bios',
    # IO 配置
    'BlkioTune',
    'Boot',
    'Bootmenu',
    'CPUAllocationConfig',
    'CPUFeature',
    # 核心配置
    'CPUTopology',
    'CacheTune',
    'Channel',
    # 时钟
    'Clock',
    'Console',
    'Controller',
    'CpuMode',
    'CpuTune',
    'Crypto',
    'DeviceBytesLimit',
    'DeviceIopsLimit',
    'DevicesConfig',
    'Disk',
    'Domain',
    'DomainConfigConverter',
    'DomainMemory',
    'Driver',
    'EmulatorPin',
    'Features',
    'Filesystem',
    'Graphics',
    'Hostdev',
    'Hub',
    # 内存配置
    'HugePage',
    'HypervFeature',
    'IOThread',
    'IOThreadIDs',
    'IOThreadPin',
    'IOThreads',
    'Input',
    'Interface',
    'KVMFeature',
    # 元数据和安全
    'KeyWrap',
    'LaunchSecurity',
    'MachineType',
    'MemNode',
    'MemTune',
    'Memballoon',
    'MemoryAllocationConfig',
    'MemoryBacking',
    'MemoryDevice',
    'MemoryTune',
    'Metadata',
    'NumaNode',
    'NumaTune',
    'Nvram',
    'OSConfig',
    'OSType',
    'Panic',
    'Parallel',
    'Perf',
    'Pstore',
    'Redirdev',
    'Redirfilter',
    'Rng',
    # 系统信息
    'SMBIOSBaseBoard',
    'SMBIOSChassis',
    'SMBIOSSystem',
    'SecLabel',
    'SecLabels',
    'Serial',
    'Shmem',
    'Smartcard',
    'Smbios',
    'Sound',
    'SysInfo',
    'ThrottleGroup',
    'ThrottleGroups',
    'Timer',
    'UsbFilterRule',
    'VCPUPin',
    'VMConfig',
    'VMPort',
    'Video',
    'VirtType',
    'Vsock',
    'Watchdog',
    'WeightDevice',
    'XenFeature',
]
