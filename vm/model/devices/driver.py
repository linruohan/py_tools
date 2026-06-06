"""Driver 设备配置 - 整合策略模式."""

from dataclasses import dataclass
from typing import Any


@dataclass
class Driver:
    """Driver (驱动) 配置"""

    name: str | None = None  # 驱动名称
    type: str | None = None  # 驱动类型
    queues: int | None = None  # 队列数
    iothread: int | None = None  # IO 线程 ID
    ioeventfd: bool | None = None  # IO 事件 fd
    event_idx: bool | None = None  # 事件索引
    packed: str | None = None  # packed ring (on/off/auto)
    driver_iommu: str | None = None  # IOMMU 支持 (on/off)
    ats: str | None = None  # ATS 支持 (on/off)
    cmd_per_lun: int | None = None  # 每 LUN 命令数
    max_sectors: int | None = None  # 最大扇区数
    x_data_plane: bool | None = None  # 数据平面
    io: str | None = None  # IO 模式 (threads, native)
    cache: str | None = None  # 缓存模式
    discard: str | None = None  # 丢弃模式
    detect_zeroes: str | None = None  # 零检测

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'Driver':
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

    def to_dict(self) -> dict[str, Any]:
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
