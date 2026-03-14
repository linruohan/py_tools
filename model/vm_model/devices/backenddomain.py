"""BackendDomain 设备配置 - 整合策略模式."""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List


@dataclass
class BackendDomain:
    """BackendDomain (后端域) 配置"""

    name: Optional[str] = None  # 后端域名称
    uuid: Optional[str] = None  # 后端域 UUID

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BackendDomain':
        """从字典创建"""
        return cls(
            name=data.get('name'),
            uuid=data.get('uuid'),
        )

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'name': self.name,
            'uuid': self.uuid,
        }
