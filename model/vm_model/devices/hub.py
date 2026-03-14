"""Hub 设备配置 - 整合策略模式."""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List


@dataclass
class Hub:
    """Hub (USB Hub) 设备配置"""

    type: str = 'usb'  # usb
    ports: Optional[int] = None  # 端口数
    address: Optional[Dict[str, str]] = None  # 设备地址

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Hub':
        """从字典创建"""
        return cls(
            type=data.get('type', 'usb'),
            ports=data.get('ports'),
            address=data.get('address'),
        )

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'type': self.type,
            'ports': self.ports,
            'address': self.address,
        }
