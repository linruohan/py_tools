"""Watchdog 设备配置 - 整合策略模式."""

from dataclasses import dataclass
from typing import Any


@dataclass
class Watchdog:
    """Watchdog 设备配置"""

    model: str = 'i6300esb'  # i6300esb, ib700, diag288, itco
    action: str = 'reset'  # reset, shutdown, poweroff, pause, none, dump, inject-nmi
    address: dict[str, str] | None = None  # 设备地址

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'Watchdog':
        """从字典创建"""
        return cls(
            model=data.get('model', 'i6300esb'),
            action=data.get('action', 'reset'),
            address=data.get('address'),
        )

    def to_dict(self) -> dict[str, Any]:
        """转换为字典"""
        return {
            'model': self.model,
            'action': self.action,
            'address': self.address,
        }
