"""Redirdev 设备配置 - 整合策略模式."""

from dataclasses import dataclass
from typing import Any


@dataclass
class Redirdev:
    """Redirdev (USB 重定向设备) 配置"""

    type: str = 'spicevmc'  # spicevmc, tcp, usb
    bus: str = 'usb'  # usb
    vendor_id: str | None = None  # 厂商 ID
    product_id: str | None = None  # 产品 ID
    port: str | None = None  # USB 端口
    source_host: str | None = None  # 源主机 (用于 tcp 模式)
    source_service: str | None = None  # 源服务 (用于 tcp 模式)
    source_path: str | None = None  # 源路径 (用于 unix 模式)
    boot_order: int | None = None  # 启动顺序
    address: dict[str, str] | None = None  # 设备地址

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'Redirdev':
        """从字典创建"""
        return cls(
            type=data.get('type', 'spicevmc'),
            bus=data.get('bus', 'usb'),
            vendor_id=data.get('vendor_id'),
            product_id=data.get('product_id'),
            port=data.get('port'),
            source_host=data.get('source_host'),
            source_service=data.get('source_service'),
            source_path=data.get('source_path'),
            boot_order=data.get('boot_order'),
            address=data.get('address'),
        )

    def to_dict(self) -> dict[str, Any]:
        """转换为字典"""
        return {
            'type': self.type,
            'bus': self.bus,
            'vendor_id': self.vendor_id,
            'product_id': self.product_id,
            'port': self.port,
            'source_host': self.source_host,
            'source_service': self.source_service,
            'source_path': self.source_path,
            'boot_order': self.boot_order,
            'address': self.address,
        }
