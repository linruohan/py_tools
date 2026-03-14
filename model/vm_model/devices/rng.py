"""Rng 设备配置 - 整合策略模式."""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List


@dataclass
class Rng:
    """Rng (随机数发生器) 设备配置"""

    model: str = 'virtio'  # virtio, virtio-transitional, virtio-non-transitional
    backend_model: str = 'random'  # random, egd, builtin
    backend_type: Optional[str] = None  # udp, tcp, unix (用于 egd)
    backend_source_mode: Optional[str] = None  # bind, connect (用于 egd)
    backend_source_host: Optional[str] = None  # 主机地址 (用于 egd)
    backend_source_service: Optional[str] = None  # 服务端口 (用于 egd)
    backend_source_path: Optional[str] = None  # 设备路径 (用于 random)
    rate_bytes: Optional[int] = None  # 速率限制字节数
    rate_period: Optional[int] = None  # 速率限制周期 (毫秒)
    address: Optional[Dict[str, str]] = None  # 设备地址
    driver: Optional[Dict[str, str]] = None  # 驱动配置

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Rng':
        """从字典创建"""
        return cls(
            model=data.get('model', 'virtio'),
            backend_model=data.get('backend_model', 'random'),
            backend_type=data.get('backend_type'),
            backend_source_mode=data.get('backend_source_mode'),
            backend_source_host=data.get('backend_source_host'),
            backend_source_service=data.get('backend_source_service'),
            backend_source_path=data.get('backend_source_path'),
            rate_bytes=data.get('rate_bytes'),
            rate_period=data.get('rate_period'),
            address=data.get('address'),
            driver=data.get('driver'),
        )

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'model': self.model,
            'backend_model': self.backend_model,
            'backend_type': self.backend_type,
            'backend_source_mode': self.backend_source_mode,
            'backend_source_host': self.backend_source_host,
            'backend_source_service': self.backend_source_service,
            'backend_source_path': self.backend_source_path,
            'rate_bytes': self.rate_bytes,
            'rate_period': self.rate_period,
            'address': self.address,
            'driver': self.driver,
        }
