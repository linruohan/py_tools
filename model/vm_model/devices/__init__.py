"""Devices 子模块 - 包含所有设备类型定义."""

from .disk import Disk
from .interface import Interface
from .graphics import Graphics
from .video import Video
from .audio import Audio
from .sound import Sound
from .controller import Controller
from .hostdev import Hostdev
from .watchdog import Watchdog
from .memballoon import Memballoon
from .iommu import IOMMU
from .tpm import TPM
from .rng import Rng
from .console import Console
from .channel import Channel
from .serial import Serial
from .parallel import Parallel
from .smartcard import Smartcard
from .shmem import Shmem
from .vsock import Vsock
from .crypto import Crypto
from .pstore import Pstore
from .panic import Panic
from .driver import Driver
from .hub import Hub
from .redirdev import Redirdev
from .redirfilter import Redirfilter, UsbFilterRule
from .backenddomain import BackendDomain
from .filesystem import Filesystem
from .input import Input
from .nvram import Nvram
from .memory import Memory

__all__ = [
    # 基础设备
    'Disk',
    'Interface',
    'Graphics',
    'Video',
    'Audio',
    'Sound',
    'Controller',
    'Input',

    # 主机设备
    'Hostdev',
    'BackendDomain',

    # 监控和安全设备
    'Watchdog',
    'Memballoon',
    'IOMMU',
    'TPM',
    'Rng',
    'Crypto',
    'Pstore',

    # 控制台和串行设备
    'Console',
    'Channel',
    'Serial',
    'Parallel',

    # USB 设备
    'Hub',
    'Redirdev',
    'Redirfilter',
    'UsbFilterRule',

    # 其他设备
    'Smartcard',
    'Shmem',
    'Vsock',
    'Panic',
    'Driver',
    'Filesystem',
    'Nvram',
    'Memory',
]
