"""Panic 设备配置 - 整合策略模式."""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List


@dataclass
class Panic:
    """Panic (Panic 设备) 配置"""

    model: str = 'isa'  # isa, pvpanic, virtio
    iobase: Optional[int] = None  # IO 基地址 (isa 模式)
    use_isa: Optional[bool] = None  # 是否使用 ISA
    address: Optional[Dict[str, str]] = None  # 设备地址

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Panic':
        """从字典创建"""
        return cls(
            model=data.get('model', 'isa'),
            iobase=data.get('iobase'),
            use_isa=data.get('use_isa'),
            address=data.get('address'),
        )

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'model': self.model,
            'iobase': self.iobase,
            'use_isa': self.use_isa,
            'address': self.address,
        }
