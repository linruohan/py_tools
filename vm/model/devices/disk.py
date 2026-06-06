"""Disk 设备配置 - 整合策略模式."""

from dataclasses import dataclass
from typing import Any

# 从 config 模块导入枚举类型
from config.strategies.option_strategies import CacheMode, DiskBusType, DiskType


@dataclass
class Disk:
    """磁盘设备配置"""

    type: DiskType = DiskType.QCOW2
    device: str = 'disk'  # disk, cdrom, floppy, lun
    bus: DiskBusType = DiskBusType.VIRTIO
    target: str = 'vda'
    driver: str | None = None
    cache: CacheMode = CacheMode.NONE
    io: str | None = None
    discard: str | None = None
    detect_zeroes: bool | None = None
    source_file: str | None = None
    source_protocol: str | None = None
    source_dev: str | None = None
    snapshot: str | None = None  # on, off
    readonly: bool = False
    shareable: bool = False
    transient: bool = False
    capacity: int | None = None
    allocation: int | None = None
    physical: int | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'Disk':
        """从字典创建"""
        disk_type = data.get('type', 'qcow2')
        if isinstance(disk_type, str):
            disk_type = DiskType(disk_type)

        bus = data.get('bus', 'virtio')
        if isinstance(bus, str):
            bus = DiskBusType(bus)

        cache = data.get('cache', 'none')
        if isinstance(cache, str):
            cache = CacheMode(cache)

        return cls(
            type=disk_type,
            device=data.get('device', 'disk'),
            bus=bus,
            target=data.get('target', 'vda'),
            driver=data.get('driver'),
            cache=cache,
            io=data.get('io'),
            discard=data.get('discard'),
            detect_zeroes=data.get('detect_zeroes'),
            source_file=data.get('source_file'),
            source_protocol=data.get('source_protocol'),
            source_dev=data.get('source_dev'),
            snapshot=data.get('snapshot'),
            readonly=data.get('readonly', False),
            shareable=data.get('shareable', False),
            transient=data.get('transient', False),
            capacity=data.get('capacity'),
            allocation=data.get('allocation'),
            physical=data.get('physical'),
        )

    def to_dict(self) -> dict[str, Any]:
        """转换为字典"""
        return {
            'type': self.type.value,
            'device': self.device,
            'bus': self.bus.value,
            'target': self.target,
            'driver': self.driver,
            'cache': self.cache.value,
            'io': self.io,
            'discard': self.discard,
            'detect_zeroes': self.detect_zeroes,
            'source_file': self.source_file,
            'source_protocol': self.source_protocol,
            'source_dev': self.source_dev,
            'snapshot': self.snapshot,
            'readonly': self.readonly,
            'shareable': self.shareable,
            'transient': self.transient,
            'capacity': self.capacity,
            'allocation': self.allocation,
            'physical': self.physical,
        }
