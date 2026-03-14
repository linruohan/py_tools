"""Redirdev 设备配置 - 整合策略模式."""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List


@dataclass
class Redirdev:
    """Redirdev (USB 重定向设备) 配置"""

    type: str = 'spicevmc'  # spicevmc, tcp, usb
    bus: str = 'usb'  # usb
    vendor_id: Optional[str] = None  # 厂商 ID
    product_id: Optional[str] = None  # 产品 ID
    port: Optional[str] = None  # USB 端口
    source_host: Optional[str] = None  # 源主机 (用于 tcp 模式)
    source_service: Optional[str] = None  # 源服务 (用于 tcp 模式)
    source_path: Optional[str] = None  # 源路径 (用于 unix 模式)
    boot_order: Optional[int] = None  # 启动顺序
    address: Optional[Dict[str, str]] = None  # 设备地址

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Redirdev':
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

    def to_dict(self) -> Dict[str, Any]:
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
