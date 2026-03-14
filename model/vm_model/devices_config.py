"""设备配置类 - 管理虚拟机设备配置信息."""

from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field

from .devices.disk import Disk
from .devices.interface import Interface
from .devices.graphics import Graphics
from .devices.video import Video
from .devices.audio import Audio
from .devices.sound import Sound
from .devices.controller import Controller
from .devices.hostdev import Hostdev
from .devices.watchdog import Watchdog
from .devices.memballoon import Memballoon
from .devices.iommu import IOMMU
from .devices.tpm import TPM
from .devices.rng import Rng
from .devices.console import Console
from .devices.channel import Channel
from .devices.serial import Serial
from .devices.parallel import Parallel
from .devices.smartcard import Smartcard
from .devices.shmem import Shmem
from .devices.vsock import Vsock
from .devices.crypto import Crypto
from .devices.pstore import Pstore
from .devices.panic import Panic
from .devices.driver import Driver
from .devices.hub import Hub
from .devices.redirdev import Redirdev
from .devices.redirfilter import Redirfilter
from .devices.filesystem import Filesystem
from .devices.input import Input
from .devices.nvram import Nvram
from .devices.memory import Memory


@dataclass
class DevicesConfig:
    """设备配置类."""

    emulator: str = ''
    disks: List[Disk] = field(default_factory=list)
    interfaces: List[Interface] = field(default_factory=list)
    graphics: List[Graphics] = field(default_factory=list)
    videos: List[Video] = field(default_factory=list)
    audios: List[Audio] = field(default_factory=list)
    sounds: List[Sound] = field(default_factory=list)
    controllers: List[Controller] = field(default_factory=list)
    serials: List[Serial] = field(default_factory=list)
    parallels: List[Parallel] = field(default_factory=list)
    consoles: List[Console] = field(default_factory=list)
    channels: List[Channel] = field(default_factory=list)
    inputs: List[Input] = field(default_factory=list)
    hostdevs: List[Hostdev] = field(default_factory=list)
    watchdogs: List[Watchdog] = field(default_factory=list)
    memballoons: List[Memballoon] = field(default_factory=list)
    iommus: List[IOMMU] = field(default_factory=list)
    tpms: List[TPM] = field(default_factory=list)
    rngs: List[Rng] = field(default_factory=list)
    smartcards: List[Smartcard] = field(default_factory=list)
    shmems: List[Shmem] = field(default_factory=list)
    vsocks: List[Vsock] = field(default_factory=list)
    cryptos: List[Crypto] = field(default_factory=list)
    pstores: List[Pstore] = field(default_factory=list)
    panics: List[Panic] = field(default_factory=list)
    filesystems: List[Filesystem] = field(default_factory=list)
    nvrams: List[Nvram] = field(default_factory=list)
    memories: List[Memory] = field(default_factory=list)

    # USB 设备
    hubs: List[Hub] = field(default_factory=list)
    redirdevs: List[Redirdev] = field(default_factory=list)
    redirfilters: List[Redirfilter] = field(default_factory=list)

    # 其他配置
    hotplug: bool = True  # 热插拔支持
    monitor: bool = True  # 监控支持

    def update(self, data: Dict[str, Any]) -> None:
        """更新配置.

        Args:
            data: 配置数据
        """
        if 'emulator' in data:
            self.emulator = data['emulator']
        if 'disks' in data:
            self.disks = [Disk.from_dict(d) if isinstance(d, dict) else d for d in data['disks']]
        if 'interfaces' in data:
            self.interfaces = [Interface.from_dict(d) if isinstance(d, dict) else d for d in data['interfaces']]
        if 'graphics' in data:
            self.graphics = [Graphics.from_dict(d) if isinstance(d, dict) else d for d in data['graphics']]
        if 'videos' in data:
            self.videos = [Video.from_dict(d) if isinstance(d, dict) else d for d in data['videos']]
        if 'audios' in data:
            self.audios = [Audio.from_dict(d) if isinstance(d, dict) else d for d in data['audios']]
        if 'sounds' in data:
            self.sounds = [Sound.from_dict(d) if isinstance(d, dict) else d for d in data['sounds']]
        if 'controllers' in data:
            self.controllers = [Controller.from_dict(d) if isinstance(d, dict) else d for d in data['controllers']]
        if 'serials' in data:
            self.serials = [Serial.from_dict(d) if isinstance(d, dict) else d for d in data['serials']]
        if 'parallels' in data:
            self.parallels = [Parallel.from_dict(d) if isinstance(d, dict) else d for d in data['parallels']]
        if 'consoles' in data:
            self.consoles = [Console.from_dict(d) if isinstance(d, dict) else d for d in data['consoles']]
        if 'channels' in data:
            self.channels = [Channel.from_dict(d) if isinstance(d, dict) else d for d in data['channels']]
        if 'inputs' in data:
            self.inputs = [Input.from_dict(d) if isinstance(d, dict) else d for d in data['inputs']]
        if 'hostdevs' in data:
            self.hostdevs = [Hostdev.from_dict(d) if isinstance(d, dict) else d for d in data['hostdevs']]
        if 'watchdogs' in data:
            self.watchdogs = [Watchdog.from_dict(d) if isinstance(d, dict) else d for d in data['watchdogs']]
        if 'memballoons' in data:
            self.memballoons = [Memballoon.from_dict(d) if isinstance(d, dict) else d for d in data['memballoons']]
        if 'iommus' in data:
            self.iommus = [IOMMU.from_dict(d) if isinstance(d, dict) else d for d in data['iommus']]
        if 'tpms' in data:
            self.tpms = [TPM.from_dict(d) if isinstance(d, dict) else d for d in data['tpms']]
        if 'rngs' in data:
            self.rngs = [Rng.from_dict(d) if isinstance(d, dict) else d for d in data['rngs']]
        if 'smartcards' in data:
            self.smartcards = [Smartcard.from_dict(d) if isinstance(d, dict) else d for d in data['smartcards']]
        if 'shmems' in data:
            self.shmems = [Shmem.from_dict(d) if isinstance(d, dict) else d for d in data['shmems']]
        if 'vsocks' in data:
            self.vsocks = [Vsock.from_dict(d) if isinstance(d, dict) else d for d in data['vsocks']]
        if 'cryptos' in data:
            self.cryptos = [Crypto.from_dict(d) if isinstance(d, dict) else d for d in data['cryptos']]
        if 'pstores' in data:
            self.pstores = [Pstore.from_dict(d) if isinstance(d, dict) else d for d in data['pstores']]
        if 'panics' in data:
            self.panics = [Panic.from_dict(d) if isinstance(d, dict) else d for d in data['panics']]
        if 'filesystems' in data:
            self.filesystems = [Filesystem.from_dict(d) if isinstance(d, dict) else d for d in data['filesystems']]
        if 'nvrams' in data:
            self.nvrams = [Nvram.from_dict(d) if isinstance(d, dict) else d for d in data['nvrams']]
        if 'memories' in data:
            self.memories = [Memory.from_dict(d) if isinstance(d, dict) else d for d in data['memories']]
        if 'hubs' in data:
            self.hubs = [Hub.from_dict(d) if isinstance(d, dict) else d for d in data['hubs']]
        if 'redirdevs' in data:
            self.redirdevs = [Redirdev.from_dict(d) if isinstance(d, dict) else d for d in data['redirdevs']]
        if 'redirfilters' in data:
            self.redirfilters = [Redirfilter.from_dict(d) if isinstance(d, dict) else d for d in data['redirfilters']]
        if 'hotplug' in data:
            self.hotplug = data['hotplug']
        if 'monitor' in data:
            self.monitor = data['monitor']

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式.

        Returns:
            配置字典
        """
        return {
            'emulator': self.emulator,
            'disks': [d.to_dict() for d in self.disks],
            'interfaces': [d.to_dict() for d in self.interfaces],
            'graphics': [d.to_dict() for d in self.graphics],
            'videos': [d.to_dict() for d in self.videos],
            'audios': [d.to_dict() for d in self.audios],
            'sounds': [d.to_dict() for d in self.sounds],
            'controllers': [d.to_dict() for d in self.controllers],
            'serials': [d.to_dict() for d in self.serials],
            'parallels': [d.to_dict() for d in self.parallels],
            'consoles': [d.to_dict() for d in self.consoles],
            'channels': [d.to_dict() for d in self.channels],
            'inputs': [d.to_dict() for d in self.inputs],
            'hostdevs': [d.to_dict() for d in self.hostdevs],
            'watchdogs': [d.to_dict() for d in self.watchdogs],
            'memballoons': [d.to_dict() for d in self.memballoons],
            'iommus': [d.to_dict() for d in self.iommus],
            'tpms': [d.to_dict() for d in self.tpms],
            'rngs': [d.to_dict() for d in self.rngs],
            'smartcards': [d.to_dict() for d in self.smartcards],
            'shmems': [d.to_dict() for d in self.shmems],
            'vsocks': [d.to_dict() for d in self.vsocks],
            'cryptos': [d.to_dict() for d in self.cryptos],
            'pstores': [d.to_dict() for d in self.pstores],
            'panics': [d.to_dict() for d in self.panics],
            'filesystems': [d.to_dict() for d in self.filesystems],
            'nvrams': [d.to_dict() for d in self.nvrams],
            'memories': [d.to_dict() for d in self.memories],
            'hubs': [d.to_dict() for d in self.hubs],
            'redirdevs': [d.to_dict() for d in self.redirdevs],
            'redirfilters': [d.to_dict() for d in self.redirfilters],
            'hotplug': self.hotplug,
            'monitor': self.monitor,
        }
