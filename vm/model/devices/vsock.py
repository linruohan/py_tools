"""Vsock 设备配置 - 整合策略模式."""

from dataclasses import dataclass
from typing import Any


@dataclass
class Vsock:
    """Vsock (Virtual Socket) 设备配置"""

    id: str | None = None  # vhost-vsock-pci ID
    guest_cid: int = 3  # Guest Context ID (3-4294967295)
    auto_cid: bool = False  # 自动分配 CID
    address: dict[str, str] | None = None  # 设备地址
    model: str | None = None  # 设备型号

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'Vsock':
        """从字典创建"""
        return cls(
            id=data.get('id'),
            guest_cid=data.get('guest_cid', 3),
            auto_cid=data.get('auto_cid', False),
            address=data.get('address'),
            model=data.get('model'),
        )

    def to_dict(self) -> dict[str, Any]:
        """转换为字典"""
        return {
            'id': self.id,
            'guest_cid': self.guest_cid,
            'auto_cid': self.auto_cid,
            'address': self.address,
            'model': self.model,
        }
