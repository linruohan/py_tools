"""Nvram 设备配置 - 整合策略模式."""

from dataclasses import dataclass
from typing import Any


@dataclass
class Nvram:
    """NVRAM 设备配置"""

    type: str = 'file'
    path: str | None = None
    template: str | None = None
    template_format: str | None = None
    source: dict[str, Any] | None = None
    format: str | None = None
    address: dict[str, str] | None = None
    target: dict[str, str] | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'Nvram':
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

    def to_dict(self) -> dict[str, Any]:
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
