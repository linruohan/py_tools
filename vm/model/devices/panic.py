"""Panic 设备配置 - 整合策略模式."""

from dataclasses import dataclass
from typing import Any


@dataclass
class Panic:
    """Panic (Panic 设备) 配置"""

    model: str = 'isa'  # isa, pvpanic, virtio
    iobase: int | None = None  # IO 基地址 (isa 模式)
    use_isa: bool | None = None  # 是否使用 ISA
    address: dict[str, str] | None = None  # 设备地址

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'Panic':
        """从字典创建"""
        return cls(
            model=data.get('model', 'isa'),
            iobase=data.get('iobase'),
            use_isa=data.get('use_isa'),
            address=data.get('address'),
        )

    def to_dict(self) -> dict[str, Any]:
        """转换为字典"""
        return {
            'model': self.model,
            'iobase': self.iobase,
            'use_isa': self.use_isa,
            'address': self.address,
        }
