"""Pstore 设备配置 - 整合策略模式."""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List


@dataclass
class Pstore:
    """Pstore (持久化存储) 设备配置"""

    backend: str = 'builtin'  # builtin, file
    path: Optional[str] = None  # 存储路径 (用于 file backend)
    size: Optional[int] = None  # 存储大小
    address: Optional[Dict[str, str]] = None  # 设备地址

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Pstore':
        """从字典创建"""
        return cls(
            backend=data.get('backend', 'builtin'),
            path=data.get('path'),
            size=data.get('size'),
            address=data.get('address'),
        )

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'backend': self.backend,
            'path': self.path,
            'size': self.size,
            'address': self.address,
        }
