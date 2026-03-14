"""Driver 设备配置 - 整合策略模式."""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List


@dataclass
class Driver:
    """Driver (驱动) 配置"""

    name: Optional[str] = None  # 驱动名称
    type: Optional[str] = None  # 驱动类型
    queues: Optional[int] = None  # 队列数
    iothread: Optional[int] = None  # IO 线程 ID
    ioeventfd: Optional[bool] = None  # IO 事件 fd
    event_idx: Optional[bool] = None  # 事件索引
    packed: Optional[str] = None  # packed ring (on/off/auto)
    driver_iommu: Optional[str] = None  # IOMMU 支持 (on/off)
    ats: Optional[str] = None  # ATS 支持 (on/off)
    cmd_per_lun: Optional[int] = None  # 每 LUN 命令数
    max_sectors: Optional[int] = None  # 最大扇区数
    x_data_plane: Optional[bool] = None  # 数据平面
    io: Optional[str] = None  # IO 模式 (threads, native)
    cache: Optional[str] = None  # 缓存模式
    discard: Optional[str] = None  # 丢弃模式
    detect_zeroes: Optional[str] = None  # 零检测

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Driver':
        """从字典创建"""
        return cls(
            name=data.get('name'),
            type=data.get('type'),
            queues=data.get('queues'),
            iothread=data.get('iothread'),
            ioeventfd=data.get('ioeventfd'),
            event_idx=data.get('event_idx'),
            packed=data.get('packed'),
            driver_iommu=data.get('driver_iommu'),
            ats=data.get('ats'),
            cmd_per_lun=data.get('cmd_per_lun'),
            max_sectors=data.get('max_sectors'),
            x_data_plane=data.get('x_data_plane'),
            io=data.get('io'),
            cache=data.get('cache'),
            discard=data.get('discard'),
            detect_zeroes=data.get('detect_zeroes'),
        )

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'name': self.name,
            'type': self.type,
            'queues': self.queues,
            'iothread': self.iothread,
            'ioeventfd': self.ioeventfd,
            'event_idx': self.event_idx,
            'packed': self.packed,
            'driver_iommu': self.driver_iommu,
            'ats': self.ats,
            'cmd_per_lun': self.cmd_per_lun,
            'max_sectors': self.max_sectors,
            'x_data_plane': self.x_data_plane,
            'io': self.io,
            'cache': self.cache,
            'discard': self.discard,
            'detect_zeroes': self.detect_zeroes,
        }
