from dataclasses import dataclass, field
from typing import Optional, List
from .audio import Audio
from .channel import Channel
from .console import Console
from .controller import Controller
from .crypto import Crypto
from .disk import Disk
from .driver import Driver
from .filesystem import Filesystem
from .graphics import Graphics
from .hostdev import Hostdev
from .interface import Interface
from .iommu import IOMMU
from .memballoon import Memballoon
from .memory import Memory as DeviceMemory
from .nvram import Nvram as DeviceNvram
from .panic import Panic
from .parallel import Parallel
from .pstore import Pstore
from .rng import Rng
from .serial import Serial
from .shmem import Shmem
from .smartcard import Smartcard
from .sound import Sound
from .tpm import TPM
from .video import Video
from .vsock import Vsock
from .watchdog import Watchdog


@dataclass
class Devices:
    """设备配置集合"""

    audio: List[Audio] = field(default_factory=list)
    channels: List[Channel] = field(default_factory=list)
    consoles: List[Console] = field(default_factory=list)
    controllers: List[Controller] = field(default_factory=list)
    crypto: List[Crypto] = field(default_factory=list)
    disks: List[Disk] = field(default_factory=list)
    drivers: List[Driver] = field(default_factory=list)
    filesystems: List[Filesystem] = field(default_factory=list)
    graphics: List[Graphics] = field(default_factory=list)
    hostdevs: List[Hostdev] = field(default_factory=list)
    interfaces: List[Interface] = field(default_factory=list)
    iommu: Optional[IOMMU] = None
    memballoon: Optional[Memballoon] = None
    memory_devices: List[DeviceMemory] = field(default_factory=list)
    nvram: List[DeviceNvram] = field(default_factory=list)
    panic: Optional[Panic] = None
    parallel: List[Parallel] = field(default_factory=list)
    pstore: Optional[Pstore] = None
    rng: List[Rng] = field(default_factory=list)
    serial: List[Serial] = field(default_factory=list)
    shmem: List[Shmem] = field(default_factory=list)
    smartcard: List[Smartcard] = field(default_factory=list)
    sound: List[Sound] = field(default_factory=list)
    tpm: List[TPM] = field(default_factory=list)
    video: List[Video] = field(default_factory=list)
    vsock: List[Vsock] = field(default_factory=list)
    watchdog: List[Watchdog] = field(default_factory=list)


__all__ = [
    'Devices',
    'Audio',
    'Channel',
    'Console',
    'Controller',
    'Crypto',
    'Disk',
    'Driver',
    'Filesystem',
    'Graphics',
    'Hostdev',
    'Interface',
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
    'Video',
    'Vsock',
    'Watchdog',
]
