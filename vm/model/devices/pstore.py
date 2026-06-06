"""Pstore 设备配置 - 整合策略模式."""

from dataclasses import dataclass
from typing import Any


@dataclass
class Pstore:
    """Pstore (持久化存储) 设备配置"""

    backend: str = 'builtin'  # builtin, file
    path: str | None = None  # 存储路径 (用于 file backend)
    size: int | None = None  # 存储大小
    address: dict[str, str] | None = None  # 设备地址

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'Pstore':
        """从字典创建"""
        return cls(
            backend=data.get('backend', 'builtin'),
            path=data.get('path'),
            size=data.get('size'),
            address=data.get('address'),
        )

    def to_dict(self) -> dict[str, Any]:
        """转换为字典"""
        return {
            'backend': self.backend,
            'path': self.path,
            'size': self.size,
            'address': self.address,
        }
