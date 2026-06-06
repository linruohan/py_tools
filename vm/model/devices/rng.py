"""Rng 设备配置 - 整合策略模式."""

from dataclasses import dataclass
from typing import Any


@dataclass
class Rng:
    """Rng (随机数发生器) 设备配置"""

    model: str = 'virtio'  # virtio, virtio-transitional, virtio-non-transitional
    backend_model: str = 'random'  # random, egd, builtin
    backend_type: str | None = None  # udp, tcp, unix (用于 egd)
    backend_source_mode: str | None = None  # bind, connect (用于 egd)
    backend_source_host: str | None = None  # 主机地址 (用于 egd)
    backend_source_service: str | None = None  # 服务端口 (用于 egd)
    backend_source_path: str | None = None  # 设备路径 (用于 random)
    rate_bytes: int | None = None  # 速率限制字节数
    rate_period: int | None = None  # 速率限制周期 (毫秒)
    address: dict[str, str] | None = None  # 设备地址
    driver: dict[str, str] | None = None  # 驱动配置

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'Rng':
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

    def to_dict(self) -> dict[str, Any]:
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
