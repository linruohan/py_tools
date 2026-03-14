"""VM Model - KVM/QEMU 虚拟机配置模型."""

from .blkiotune import BlkioTune, DeviceBytesLimit, DeviceIopsLimit, WeightDevice
from .clock import Clock, Timer
from .cpu import NUMA, NumaNode
from .cpu.cpu import CPU, CPUFeature
from .cputune import CacheTune, CpuTune, EmulatorPin, IOThreadPin, MemoryTune, VCPUPin
from .devices import (
    IOMMU,
    TPM,
    Audio,
    BackendDomain,
    Channel,
    # 控制台和串行设备
    Console,
    Controller,
    Crypto,
    # 基础设备
    Disk,
    Driver,
    Filesystem,
    Graphics,
    # 主机设备
    Hostdev,
    # USB 设备
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
    # 其他设备
    Smartcard,
    Sound,
    UsbFilterRule,
    Video,
    Vsock,
    # 监控和安全设备
    Watchdog,
)
from .devices import (
    Memory as MemoryDevice,
)

# 设备相关
from .devices_config import DevicesConfig
from .domain import CpuMode, CPUTopology, Domain, MachineType, OSType, VirtType
from .features import (
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
from .iothreads import IOThread, IOThreadIDs, IOThreads
from .keywrap import KeyWrap
from .launchSecurity import LaunchSecurity
from .memory import Memory as DomainMemory
from .memoryBacking import HugePage, MemoryBacking
from .memtune import MemTune
from .metadata import Metadata
from .numatune import MemNode, NumaTune
from .os import OS, Bios, Boot, Bootmenu, Smbios
from .os_booting_config import OSBootingConfig as OSConfig
from .perf import Perf
from .pm import PM
from .seclabel import SecLabel, SecLabels
from .sysinfo import SMBIOSBIOS, SMBIOSBaseBoard, SMBIOSChassis, SMBIOSSystem, SysInfo
from .throttlegroups import ThrottleGroup, ThrottleGroups
from .vcpu import VCPU

__all__ = [
    # 核心配置
    'Domain',
    'DomainMemory',
    'CPUTopology',
    'OSType',
    'MachineType',
    'CpuMode',
    'VirtType',
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
    # NUMA 配置
    'NUMA',
    'NumaNode',
    # 内存配置
    'MemoryBacking',
    'HugePage',
    'MemTune',
    'NumaTune',
    'MemNode',
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
