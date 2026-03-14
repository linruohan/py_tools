"""Smartcard 设备配置 - 整合策略模式."""

from dataclasses import dataclass
from typing import Any


@dataclass
class Smartcard:
    """Smartcard (智能卡) 设备配置"""

    mode: str = 'host'  # host, host-certificates, passthrough, simulated
    type: str | None = None  # tcp, spicevmc (用于 passthrough 模式)
    source_mode: str | None = None  # bind, connect (用于 tcp 模式)
    source_host: str | None = None  # 主机地址
    source_service: str | None = None  # 服务端口
    source_path: str | None = None  # 设备路径
    certificate: str | None = None  # 证书路径 (用于 host-certificates 模式)
    database: str | None = None  # 证书数据库路径
    name: str | None = None  # 证书名称
    address: dict[str, str] | None = None  # 设备地址

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'Smartcard':
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

    def to_dict(self) -> dict[str, Any]:
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
