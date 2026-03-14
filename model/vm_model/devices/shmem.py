"""Shmem 设备配置 - 整合策略模式."""

from dataclasses import dataclass
from typing import Any


@dataclass
class Shmem:
    """Shmem (共享内存) 设备配置"""

    name: str = ''  # 共享内存名称
    size: int = 0  # 共享内存大小
    unit: str = 'MiB'  # 单位
    address: dict[str, str] | None = None  # 设备地址

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'Shmem':
        """从字典创建"""
        return cls(
            name=data.get('name', ''),
            size=data.get('size', 0),
            unit=data.get('unit', 'MiB'),
            address=data.get('address'),
        )

    def to_dict(self) -> dict[str, Any]:
        """转换为字典"""
        return {
            'name': self.name,
            'size': self.size,
            'unit': self.unit,
            'address': self.address,
        }
