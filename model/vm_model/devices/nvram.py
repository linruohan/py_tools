"""Nvram 设备配置 - 整合策略模式."""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List


@dataclass
class Nvram:
    """NVRAM 设备配置"""

    type: str = 'file'
    path: Optional[str] = None
    template: Optional[str] = None
    template_format: Optional[str] = None
    source: Optional[Dict[str, Any]] = None
    format: Optional[str] = None
    address: Optional[Dict[str, str]] = None
    target: Optional[Dict[str, str]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Nvram':
        """从字典创建"""
        return cls(
            type=data.get('type', 'file'),
            path=data.get('path'),
            template=data.get('template'),
            template_format=data.get('template_format'),
            source=data.get('source'),
            format=data.get('format'),
            address=data.get('address'),
            target=data.get('target'),
        )

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'type': self.type,
            'path': self.path,
            'template': self.template,
            'template_format': self.template_format,
            'source': self.source,
            'format': self.format,
            'address': self.address,
            'target': self.target,
        }
