"""VM Model - KVM/QEMU 虚拟机配置模型."""

from .configs.blkiotune import BlkioTune, DeviceBytesLimit, DeviceIopsLimit, WeightDevice
from .configs.clock import Clock, Timer
from .configs.cputune import CacheTune, CpuTune, EmulatorPin, IOThreadPin, MemoryTune, VCPUPin
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
from .configs.memoryBacking import HugePage, MemoryBacking
from .configs.memtune import MemTune
from .configs.metadata import Metadata
from .configs.numatune import MemNode, NumaTune
from .configs.os import OS, Bios, Boot, Bootmenu, Smbios
from .configs.perf import Perf
from .configs.pm import PM
from .configs.seclabel import SecLabel, SecLabels
from .configs.sysinfo import SMBIOSBIOS, SMBIOSBaseBoard, SMBIOSChassis, SMBIOSSystem, SysInfo
from .configs.throttlegroups import ThrottleGroup, ThrottleGroups
from .configs.vcpu import VCPU

# 配置类
from .configs.basic_config import BasicConfig
from .configs.cpu_allocation_config import CPUAllocationConfig
from .configs.devices_config import DevicesConfig
from .configs.memory_allocation_config import MemoryAllocationConfig
from .configs.os_booting_config import OSBootingConfig as OSConfig

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
    Memory as MemoryDevice,
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

__all__ = [
    # 核心配置
    'Domain',
    'DomainMemory',
    'CPUTopology',
    'OSType',
    'MachineType',
    'CpuMode',
    'VirtType',
    'VMConfig',
    'DomainConfigConverter',
    # OS 配置
    'OSConfig',
    'OS',
    'Boot',
    'Bootmenu',
    'Bios',
    'Smbios',
    # CPU 配置
    'CPU',
    'CPUFeature',
    'VCPU',
    'CPUAllocationConfig',
    # NUMA 配置
    'NUMA',
    'NumaNode',
    # 内存配置
    'MemoryBacking',
    'HugePage',
    'MemTune',
    'NumaTune',
    'MemNode',
    'MemoryAllocationConfig',
    # IO 配置
    'BlkioTune',
    'WeightDevice',
    'DeviceIopsLimit',
    'DeviceBytesLimit',
    'CpuTune',
    'VCPUPin',
    'EmulatorPin',
    'IOThreadPin',
    'CacheTune',
    'MemoryTune',
    'IOThreads',
    'IOThreadIDs',
    'IOThread',
    'Perf',
    # 电源管理
    'PM',
    # 功能特性
    'Features',
    'ACPI',
    'APIC',
    'PMU',
    'VMPort',
    'GIC',
    'SMM',
    'IOAPIC',
    'KVMFeature',
    'HypervFeature',
    'XenFeature',
    # 时钟
    'Clock',
    'Timer',
    # 系统信息
    'SysInfo',
    'SMBIOSBIOS',
    'SMBIOSSystem',
    'SMBIOSBaseBoard',
    'SMBIOSChassis',
    # 元数据和安全
    'Metadata',
    'SecLabel',
    'SecLabels',
    'KeyWrap',
    'LaunchSecurity',
    'ThrottleGroups',
    'ThrottleGroup',
    # 设备配置
    'DevicesConfig',
    'BasicConfig',
    # 设备类型
    'Disk',
    'Interface',
    'Graphics',
    'Video',
    'Audio',
    'Sound',
    'Controller',
    'Input',
    'Hostdev',
    'BackendDomain',
    'Watchdog',
    'Memballoon',
    'IOMMU',
    'TPM',
    'Rng',
    'Crypto',
    'Pstore',
    'Console',
    'Channel',
    'Serial',
    'Parallel',
    'Hub',
    'Redirdev',
    'Redirfilter',
    'UsbFilterRule',
    'Smartcard',
    'Shmem',
    'Vsock',
    'Panic',
    'Driver',
    'Filesystem',
    'Nvram',
    'MemoryDevice',
]
