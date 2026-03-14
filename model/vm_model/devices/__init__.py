"""Devices 子模块 - 包含所有设备类型定义."""

from .audio import Audio
from .backenddomain import BackendDomain
from .channel import Channel
from .console import Console
from .controller import Controller
from .crypto import Crypto
from .disk import Disk
from .driver import Driver
from .filesystem import Filesystem
from .graphics import Graphics
from .hostdev import Hostdev
from .hub import Hub
from .input import Input
from .interface import Interface
from .iommu import IOMMU
from .memballoon import Memballoon
from .memory import Memory
from .nvram import Nvram
from .panic import Panic
from .parallel import Parallel
from .pstore import Pstore
from .redirdev import Redirdev
from .redirfilter import Redirfilter, UsbFilterRule
from .rng import Rng
from .serial import Serial
from .shmem import Shmem
from .smartcard import Smartcard
from .sound import Sound
from .tpm import TPM
from .video import Video
from .vsock import Vsock
from .watchdog import Watchdog

__all__ = [
    'IOMMU',
    'TPM',
    # 基础设备
    'Audio',
    # 主机设备
    'BackendDomain',
    # 控制台和串行设备
    'Channel',
    'Console',
    'Controller',
    # 监控和安全设备
    'Crypto',
    'Disk',
    # 其他设备
    'Driver',
    'Filesystem',
    'Graphics',
    'Hostdev',
    # USB 设备
    'Hub',
    'Input',
    'Interface',
    'Memballoon',
    'Memory',
    'Nvram',
    'Panic',
    'Parallel',
    'Pstore',
    'Redirdev',
    'Redirfilter',
    'Rng',
    'Serial',
    'Shmem',
    'Smartcard',
    'Sound',
    'UsbFilterRule',
    'Video',
    'Vsock',
    'Watchdog',
]
