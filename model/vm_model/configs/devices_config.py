"""设备配置类 - 管理虚拟机设备配置信息."""

from dataclasses import dataclass, field
from typing import Any

from ..devices.audio import Audio
from ..devices.channel import Channel
from ..devices.console import Console
from ..devices.controller import Controller
from ..devices.crypto import Crypto
from ..devices.disk import Disk
from ..devices.filesystem import Filesystem
from ..devices.graphics import Graphics
from ..devices.hostdev import Hostdev
from ..devices.hub import Hub
from ..devices.input import Input
from ..devices.interface import Interface
from ..devices.iommu import IOMMU
from ..devices.memballoon import Memballoon
from ..devices.memory import Memory
from ..devices.nvram import Nvram
from ..devices.panic import Panic
from ..devices.parallel import Parallel
from ..devices.pstore import Pstore
from ..devices.redirdev import Redirdev
from ..devices.redirfilter import Redirfilter
from ..devices.rng import Rng
from ..devices.serial import Serial
from ..devices.shmem import Shmem
from ..devices.smartcard import Smartcard
from ..devices.sound import Sound
from ..devices.tpm import TPM
from ..devices.video import Video
from ..devices.vsock import Vsock
from ..devices.watchdog import Watchdog


@dataclass
class DevicesConfig:
    """设备配置类."""

    emulator: str = ''
    disk: list[Disk] = field(default_factory=list)
    interface: list[Interface] = field(default_factory=list)
    graphic: list[Graphics] = field(default_factory=list)
    video: list[Video] = field(default_factory=list)
    audio: list[Audio] = field(default_factory=list)
    sound: list[Sound] = field(default_factory=list)
    controller: list[Controller] = field(default_factory=list)
    serial: list[Serial] = field(default_factory=list)
    parallel: list[Parallel] = field(default_factory=list)
    console: list[Console] = field(default_factory=list)
    channel: list[Channel] = field(default_factory=list)
    input: list[Input] = field(default_factory=list)
    hostdev: list[Hostdev] = field(default_factory=list)
    watchdog: list[Watchdog] = field(default_factory=list)
    memballoon: list[Memballoon] = field(default_factory=list)
    iommu: list[IOMMU] = field(default_factory=list)
    tpm: list[TPM] = field(default_factory=list)
    rng: list[Rng] = field(default_factory=list)
    smartcard: list[Smartcard] = field(default_factory=list)
    shmem: list[Shmem] = field(default_factory=list)
    vsock: list[Vsock] = field(default_factory=list)
    crypto: list[Crypto] = field(default_factory=list)
    pstore: list[Pstore] = field(default_factory=list)
    panic: list[Panic] = field(default_factory=list)
    filesystem: list[Filesystem] = field(default_factory=list)
    nvram: list[Nvram] = field(default_factory=list)
    memory: list[Memory] = field(default_factory=list)

    # USB 设备
    hub: list[Hub] = field(default_factory=list)
    redirdev: list[Redirdev] = field(default_factory=list)
    redirfilter: list[Redirfilter] = field(default_factory=list)

    # 其他配置
    hotplug: bool = True  # 热插拔支持
    monitor: bool = True  # 监控支持

    def update(self, data: dict[str, Any]) -> None:
        """更新配置.

        Args:
            data: 配置数据
        """
        if 'emulator' in data:
            self.emulator = data['emulator']
        # 支持复数形式和单数形式的字段名
        if 'disk' in data:
            self.disk = [self._convert_disk_dict(d) for d in data['disk']]
        if 'disks' in data:
            self.disk = [self._convert_disk_dict(d) for d in data['disks']]
        if 'interface' in data:
            self.interface = [
                Interface.from_dict(d) if isinstance(d, dict) else d for d in data['interface']
            ]
        if 'interfaces' in data:
            self.interface = [
                Interface.from_dict(d) if isinstance(d, dict) else d for d in data['interfaces']
            ]
        if 'graphic' in data:
            self.graphic = [
                Graphics.from_dict(d) if isinstance(d, dict) else d for d in data['graphic']
            ]
        if 'graphics' in data:
            g = data['graphics']
            if isinstance(g, dict):
                self.graphic = [Graphics.from_dict(g)]
            elif isinstance(g, list):
                self.graphic = [Graphics.from_dict(d) if isinstance(d, dict) else d for d in g]
        if 'video' in data:
            v = data['video']
            if isinstance(v, dict):
                self.video = [Video.from_dict(v)]
            elif isinstance(v, list):
                self.video = [Video.from_dict(d) if isinstance(d, dict) else d for d in v]
            else:
                self.video = []
        if 'audio' in data:
            self.audio = [Audio.from_dict(d) if isinstance(d, dict) else d for d in data['audio']]
        if 'sound' in data:
            self.sound = [Sound.from_dict(d) if isinstance(d, dict) else d for d in data['sound']]
        if 'controller' in data:
            self.controller = [
                Controller.from_dict(d) if isinstance(d, dict) else d for d in data['controller']
            ]
        if 'controllers' in data:
            self.controller = [
                Controller.from_dict(d) if isinstance(d, dict) else d for d in data['controllers']
            ]
        if 'serial' in data:
            s = data['serial']
            if isinstance(s, dict):
                self.serial = [Serial.from_dict(s)]
            elif isinstance(s, list):
                self.serial = [Serial.from_dict(d) if isinstance(d, dict) else d for d in s]
        if 'parallel' in data:
            self.parallel = [
                Parallel.from_dict(d) if isinstance(d, dict) else d for d in data['parallel']
            ]
        if 'console' in data:
            self.console = [
                Console.from_dict(d) if isinstance(d, dict) else d for d in data['console']
            ]
        if 'channel' in data:
            self.channel = [
                Channel.from_dict(d) if isinstance(d, dict) else d for d in data['channel']
            ]
        if 'input' in data:
            inp = data['input']
            if isinstance(inp, dict):
                # 处理键盘和鼠标配置
                if 'keyboard' in inp:
                    self.input = [Input(type='keyboard', bus=inp.get('keyboard', 'virtio'))]
                if 'mouse' in inp:
                    self.input.append(Input(type='mouse', bus=inp.get('mouse', 'tablet')))
            elif isinstance(inp, list):
                self.input = [Input.from_dict(d) if isinstance(d, dict) else d for d in inp]
        if 'hostdev' in data:
            self.hostdev = [
                Hostdev.from_dict(d) if isinstance(d, dict) else d for d in data['hostdev']
            ]
        if 'watchdog' in data:
            self.watchdog = [
                Watchdog.from_dict(d) if isinstance(d, dict) else d for d in data['watchdog']
            ]
        if 'memballoon' in data:
            self.memballoon = [
                Memballoon.from_dict(d) if isinstance(d, dict) else d for d in data['memballoon']
            ]
        if 'iommu' in data:
            self.iommu = [IOMMU.from_dict(d) if isinstance(d, dict) else d for d in data['iommu']]
        if 'tpm' in data:
            t = data['tpm']
            if isinstance(t, dict):
                self.tpm = [TPM.from_dict(t)]
            elif isinstance(t, list):
                self.tpm = [TPM.from_dict(d) if isinstance(d, dict) else d for d in t]
        if 'rng' in data:
            self.rng = [Rng.from_dict(d) if isinstance(d, dict) else d for d in data['rng']]
        if 'smartcard' in data:
            self.smartcard = [
                Smartcard.from_dict(d) if isinstance(d, dict) else d for d in data['smartcard']
            ]
        if 'shmem' in data:
            self.shmem = [Shmem.from_dict(d) if isinstance(d, dict) else d for d in data['shmem']]
        if 'vsock' in data:
            self.vsock = [Vsock.from_dict(d) if isinstance(d, dict) else d for d in data['vsock']]
        if 'crypto' in data:
            self.crypto = [
                Crypto.from_dict(d) if isinstance(d, dict) else d for d in data['crypto']
            ]
        if 'pstore' in data:
            self.pstore = [
                Pstore.from_dict(d) if isinstance(d, dict) else d for d in data['pstore']
            ]
        if 'panic' in data:
            self.panic = [Panic.from_dict(d) if isinstance(d, dict) else d for d in data['panic']]
        if 'filesystem' in data:
            self.filesystem = [
                Filesystem.from_dict(d) if isinstance(d, dict) else d for d in data['filesystem']
            ]
        if 'nvram' in data:
            self.nvram = [Nvram.from_dict(d) if isinstance(d, dict) else d for d in data['nvram']]
        if 'memory' in data:
            self.memory = [
                Memory.from_dict(d) if isinstance(d, dict) else d for d in data['memory']
            ]
        if 'hub' in data:
            self.hub = [Hub.from_dict(d) if isinstance(d, dict) else d for d in data['hub']]
        if 'redirdev' in data:
            self.redirdev = [
                Redirdev.from_dict(d) if isinstance(d, dict) else d for d in data['redirdev']
            ]
        if 'redirfilter' in data:
            self.redirfilter = [
                Redirfilter.from_dict(d) if isinstance(d, dict) else d for d in data['redirfilter']
            ]
        if 'usb_controller' in data:
            # 处理 USB 控制器配置
            ctrl_type = data['usb_controller']
            if ctrl_type and ctrl_type != 'none':
                self.controller.append(Controller(type=ctrl_type))
        if 'hotplug' in data:
            self.hotplug = data['hotplug']
        if 'monitor' in data:
            self.monitor = data['monitor']

    def _convert_disk_dict(self, d: Any) -> Disk:
        """转换磁盘配置字典,将模块格式转换为 Disk 格式."""
        if not isinstance(d, dict):
            return d
        # 将模块格式转换为 Disk.from_dict 期望的格式
        converted = {
            'type': d.get('format', 'qcow2'),  # format -> type
            'device': d.get('device_type', 'disk'),  # device_type -> device
            'bus': d.get('bus', 'virtio'),
            'source_file': d.get('path', ''),  # path -> source_file
            'cache': d.get('cache', 'none'),
            'readonly': d.get('readonly', False),
            'shareable': d.get('shareable', False),
            'discard': 'unmap' if d.get('discard') else None,
        }
        return Disk.from_dict(converted)

    def to_dict(self) -> dict[str, Any]:
        """转换为字典格式.

        Returns:
            配置字典
        """
        return {
            'emulator': self.emulator,
            'disk': [d.to_dict() for d in self.disk],
            'interface': [d.to_dict() for d in self.interface],
            'graphic': [d.to_dict() for d in self.graphic],
            'video': [d.to_dict() for d in self.video],
            'audio': [d.to_dict() for d in self.audio],
            'sound': [d.to_dict() for d in self.sound],
            'controller': [d.to_dict() for d in self.controller],
            'serial': [d.to_dict() for d in self.serial],
            'parallel': [d.to_dict() for d in self.parallel],
            'console': [d.to_dict() for d in self.console],
            'channel': [d.to_dict() for d in self.channel],
            'input': [d.to_dict() for d in self.input],
            'hostdev': [d.to_dict() for d in self.hostdev],
            'watchdog': [d.to_dict() for d in self.watchdog],
            'memballoon': [d.to_dict() for d in self.memballoon],
            'iommu': [d.to_dict() for d in self.iommu],
            'tpm': [d.to_dict() for d in self.tpm],
            'rng': [d.to_dict() for d in self.rng],
            'smartcard': [d.to_dict() for d in self.smartcard],
            'shmem': [d.to_dict() for d in self.shmem],
            'vsock': [d.to_dict() for d in self.vsock],
            'crypto': [d.to_dict() for d in self.crypto],
            'pstore': [d.to_dict() for d in self.pstore],
            'panic': [d.to_dict() for d in self.panic],
            'filesystem': [d.to_dict() for d in self.filesystem],
            'nvram': [d.to_dict() for d in self.nvram],
            'memory': [d.to_dict() for d in self.memory],
            'hub': [d.to_dict() for d in self.hub],
            'redirdev': [d.to_dict() for d in self.redirdev],
            'redirfilter': [d.to_dict() for d in self.redirfilter],
            'hotplug': self.hotplug,
            'monitor': self.monitor,
        }
