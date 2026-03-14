"""Parallel 设备配置 - 整合策略模式."""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List


@dataclass
class Parallel:
    """Parallel (并口) 设备配置"""

    type: str = 'file'  # file, dev, null, udp, tcp
    source_path: Optional[str] = None  # 源路径
    source_mode: Optional[str] = None  # 源模式 (bind, connect)
    source_host: Optional[str] = None  # 源主机
    source_service: Optional[str] = None  # 源服务
    target_port: Optional[str] = None  # 目标端口
    address: Optional[Dict[str, str]] = None  # 设备地址

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Parallel':
        """从字典创建"""
        return cls(
            type=data.get('type', 'file'),
            source_path=data.get('source_path'),
            source_mode=data.get('source_mode'),
            source_host=data.get('source_host'),
            source_service=data.get('source_service'),
            target_port=data.get('target_port'),
            address=data.get('address'),
        )

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'type': self.type,
            'source_path': self.source_path,
            'source_mode': self.source_mode,
            'source_host': self.source_host,
            'source_service': self.source_service,
            'target_port': self.target_port,
            'address': self.address,
        }
