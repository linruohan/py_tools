"""BackendDomain 设备配置 - 整合策略模式."""

from dataclasses import dataclass
from typing import Any


@dataclass
class BackendDomain:
    """BackendDomain (后端域) 配置"""

    name: str | None = None  # 后端域名称
    uuid: str | None = None  # 后端域 UUID

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'BackendDomain':
        """从字典创建"""
        return cls(
            name=data.get('name'),
            uuid=data.get('uuid'),
        )

    def to_dict(self) -> dict[str, Any]:
        """转换为字典"""
        return {
            'name': self.name,
            'uuid': self.uuid,
        }
