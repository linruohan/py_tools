"""Controller 设备配置 - 整合策略模式."""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List


@dataclass
class Controller:
    """Controller 设备配置"""

    type: str = 'ide'  # ide, fdc, scsi, virtio-serial, usb, pci, xenbus, nvme, ccid, sata, virtio-mmio
    index: int = 0
    model: Optional[str] = None  # 控制器型号
    ports: Optional[int] = None  # 端口数
    vectors: Optional[int] = None  # MSI-X 向量数
    max_grant_frames: Optional[int] = None  # xenbus 最大授权帧
    max_event_channels: Optional[int] = None  # xenbus 最大事件通道
    ioeventfd: Optional[bool] = None  # ioeventfd 支持
    cmd_per_lun: Optional[int] = None  # 每 LUN 命令数
    max_sectors: Optional[int] = None  # 最大扇区数
    iothread: Optional[int] = None  # IO 线程 ID
    iothreads: Optional[int] = None  # IO 线程数
    queues: Optional[int] = None  # 队列数
    pci_slot: Optional[int] = None  # PCI 插槽号
    chassis: Optional[int] = None  # 机箱号
    function: Optional[int] = None  # 功能号
    address: Optional[Dict[str, str]] = None  # 设备地址
    target: Optional[int] = None  # 目标 ID

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Controller':
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

    def to_dict(self) -> Dict[str, Any]:
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
