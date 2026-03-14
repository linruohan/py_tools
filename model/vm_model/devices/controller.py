"""Controller 设备配置 - 整合策略模式."""

from dataclasses import dataclass
from typing import Any


@dataclass
class Controller:
    """Controller 设备配置"""

    type: str = (
        'ide'  # ide, fdc, scsi, virtio-serial, usb, pci, xenbus, nvme, ccid, sata, virtio-mmio
    )
    index: int = 0
    model: str | None = None  # 控制器型号
    ports: int | None = None  # 端口数
    vectors: int | None = None  # MSI-X 向量数
    max_grant_frames: int | None = None  # xenbus 最大授权帧
    max_event_channels: int | None = None  # xenbus 最大事件通道
    ioeventfd: bool | None = None  # ioeventfd 支持
    cmd_per_lun: int | None = None  # 每 LUN 命令数
    max_sectors: int | None = None  # 最大扇区数
    iothread: int | None = None  # IO 线程 ID
    iothreads: int | None = None  # IO 线程数
    queues: int | None = None  # 队列数
    pci_slot: int | None = None  # PCI 插槽号
    chassis: int | None = None  # 机箱号
    function: int | None = None  # 功能号
    address: dict[str, str] | None = None  # 设备地址
    target: int | None = None  # 目标 ID

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'Controller':
        """从字典创建"""
        return cls(
            type=data.get('type', 'ide'),
            index=data.get('index', 0),
            model=data.get('model'),
            ports=data.get('ports'),
            vectors=data.get('vectors'),
            max_grant_frames=data.get('max_grant_frames'),
            max_event_channels=data.get('max_event_channels'),
            ioeventfd=data.get('ioeventfd'),
            cmd_per_lun=data.get('cmd_per_lun'),
            max_sectors=data.get('max_sectors'),
            iothread=data.get('iothread'),
            iothreads=data.get('iothreads'),
            queues=data.get('queues'),
            pci_slot=data.get('pci_slot'),
            chassis=data.get('chassis'),
            function=data.get('function'),
            address=data.get('address'),
            target=data.get('target'),
        )

    def to_dict(self) -> dict[str, Any]:
        """转换为字典"""
        return {
            'type': self.type,
            'index': self.index,
            'model': self.model,
            'ports': self.ports,
            'vectors': self.vectors,
            'max_grant_frames': self.max_grant_frames,
            'max_event_channels': self.max_event_channels,
            'ioeventfd': self.ioeventfd,
            'cmd_per_lun': self.cmd_per_lun,
            'max_sectors': self.max_sectors,
            'iothread': self.iothread,
            'iothreads': self.iothreads,
            'queues': self.queues,
            'pci_slot': self.pci_slot,
            'chassis': self.chassis,
            'function': self.function,
            'address': self.address,
            'target': self.target,
        }
