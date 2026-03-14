"""Smartcard 设备配置 - 整合策略模式."""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List


@dataclass
class Smartcard:
    """Smartcard (智能卡) 设备配置"""

    mode: str = 'host'  # host, host-certificates, passthrough, simulated
    type: Optional[str] = None  # tcp, spicevmc (用于 passthrough 模式)
    source_mode: Optional[str] = None  # bind, connect (用于 tcp 模式)
    source_host: Optional[str] = None  # 主机地址
    source_service: Optional[str] = None  # 服务端口
    source_path: Optional[str] = None  # 设备路径
    certificate: Optional[str] = None  # 证书路径 (用于 host-certificates 模式)
    database: Optional[str] = None  # 证书数据库路径
    name: Optional[str] = None  # 证书名称
    address: Optional[Dict[str, str]] = None  # 设备地址

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Smartcard':
        """从字典创建"""
        return cls(
            mode=data.get('mode', 'host'),
            type=data.get('type'),
            source_mode=data.get('source_mode'),
            source_host=data.get('source_host'),
            source_service=data.get('source_service'),
            source_path=data.get('source_path'),
            certificate=data.get('certificate'),
            database=data.get('database'),
            name=data.get('name'),
            address=data.get('address'),
        )

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'mode': self.mode,
            'type': self.type,
            'source_mode': self.source_mode,
            'source_host': self.source_host,
            'source_service': self.source_service,
            'source_path': self.source_path,
            'certificate': self.certificate,
            'database': self.database,
            'name': self.name,
            'address': self.address,
        }
