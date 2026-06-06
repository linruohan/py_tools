"""Channel 设备配置 - 整合策略模式."""

from dataclasses import dataclass
from typing import Any


@dataclass
class Channel:
    """Channel (Virtio 串行通道) 设备配置"""

    type: str = 'unix'  # unix, tcp, udp, dev, file, pipe, nmdm, spicevmc, spiceport
    name: str | None = None  # 通道名称 (如 com.redhat.rhevm.vdsm)
    source_path: str | None = None  # 源路径
    source_mode: str | None = None  # 源模式 (bind, connect)
    source_host: str | None = None  # 源主机
    source_service: str | None = None  # 源服务
    target_type: str | None = None  # 目标类型
    target_name: str | None = None  # 目标名称
    target_state: str | None = None  # 目标状态 (connected, disconnected)
    address: dict[str, str] | None = None  # 设备地址

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'Channel':
        """从字典创建"""
        return cls(
            type=data.get('type', 'unix'),
            name=data.get('name'),
            source_path=data.get('source_path'),
            source_mode=data.get('source_mode'),
            source_host=data.get('source_host'),
            source_service=data.get('source_service'),
            target_type=data.get('target_type'),
            target_name=data.get('target_name'),
            target_state=data.get('target_state'),
            address=data.get('address'),
        )

    def to_dict(self) -> dict[str, Any]:
        """转换为字典"""
        return {
            'type': self.type,
            'name': self.name,
            'source_path': self.source_path,
            'source_mode': self.source_mode,
            'source_host': self.source_host,
            'source_service': self.source_service,
            'target_type': self.target_type,
            'target_name': self.target_name,
            'target_state': self.target_state,
            'address': self.address,
        }
