"""Crypto 设备配置 - 整合策略模式."""

from dataclasses import dataclass
from typing import Any


@dataclass
class Crypto:
    """Crypto (加密设备) 配置"""

    model: str = 'virtio'  # virtio, virtio-transitional, virtio-non-transitional
    type: str = 'cryptodev-virtio'  # 设备类型
    io_mode: str | None = None  # IO 模式
    queues: int | None = None  # 队列数
    max_size: int | None = None  # 最大尺寸
    address: dict[str, str] | None = None  # 设备地址
    driver: dict[str, str] | None = None  # 驱动配置

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'Crypto':
        """从字典创建"""
        return cls(
            model=data.get('model', 'virtio'),
            type=data.get('type', 'cryptodev-virtio'),
            io_mode=data.get('io_mode'),
            queues=data.get('queues'),
            max_size=data.get('max_size'),
            address=data.get('address'),
            driver=data.get('driver'),
        )

    def to_dict(self) -> dict[str, Any]:
        """转换为字典"""
        return {
            'model': self.model,
            'type': self.type,
            'io_mode': self.io_mode,
            'queues': self.queues,
            'max_size': self.max_size,
            'address': self.address,
            'driver': self.driver,
        }
