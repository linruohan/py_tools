"""Channel 设备配置 - 整合策略模式."""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List


@dataclass
class Channel:
    """Channel (Virtio 串行通道) 设备配置"""

    type: str = 'unix'  # unix, tcp, udp, dev, file, pipe, nmdm, spicevmc, spiceport
    name: Optional[str] = None  # 通道名称 (如 com.redhat.rhevm.vdsm)
    source_path: Optional[str] = None  # 源路径
    source_mode: Optional[str] = None  # 源模式 (bind, connect)
    source_host: Optional[str] = None  # 源主机
    source_service: Optional[str] = None  # 源服务
    target_type: Optional[str] = None  # 目标类型
    target_name: Optional[str] = None  # 目标名称
    target_state: Optional[str] = None  # 目标状态 (connected, disconnected)
    address: Optional[Dict[str, str]] = None  # 设备地址

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Channel':
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

    def to_dict(self) -> Dict[str, Any]:
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
