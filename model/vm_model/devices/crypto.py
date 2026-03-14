"""Crypto 设备配置 - 整合策略模式."""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List


@dataclass
class Crypto:
    """Crypto (加密设备) 配置"""

    model: str = 'virtio'  # virtio, virtio-transitional, virtio-non-transitional
    type: str = 'cryptodev-virtio'  # 设备类型
    io_mode: Optional[str] = None  # IO 模式
    queues: Optional[int] = None  # 队列数
    max_size: Optional[int] = None  # 最大尺寸
    address: Optional[Dict[str, str]] = None  # 设备地址
    driver: Optional[Dict[str, str]] = None  # 驱动配置

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Crypto':
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

    def to_dict(self) -> Dict[str, Any]:
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
