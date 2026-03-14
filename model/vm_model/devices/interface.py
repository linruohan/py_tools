"""Interface 设备配置 - 整合策略模式."""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any


@dataclass
class Interface:
    """网络设备配置"""

    type: str = 'network'  # network, bridge, user, internal, direct
    source: Optional[str] = None
    target: Optional[str] = None
    mac: Optional[str] = None
    model: str = 'virtio'
    driver: Optional[Dict[str, str]] = None
    address: Optional[Dict[str, str]] = None
    mtu: Optional[int] = None
    virtualport_type: Optional[str] = None
    virtualport_params: Optional[Dict[str, str]] = None
    port: Optional[str] = None
    portgroup: Optional[str] = None
    inbound: Optional[Dict[str, str]] = None
    outbound: Optional[Dict[str, str]] = None
    link_state: str = 'up'

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Interface':
        """从字典创建"""
        return cls(
            type=data.get('type', 'network'),
            source=data.get('source'),
            target=data.get('target'),
            mac=data.get('mac'),
            model=data.get('model', 'virtio'),
            driver=data.get('driver'),
            address=data.get('address'),
            mtu=data.get('mtu'),
            virtualport_type=data.get('virtualport_type'),
            virtualport_params=data.get('virtualport_params'),
            port=data.get('port'),
            portgroup=data.get('portgroup'),
            inbound=data.get('inbound'),
            outbound=data.get('outbound'),
            link_state=data.get('link_state', 'up'),
        )

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'type': self.type,
            'source': self.source,
            'target': self.target,
            'mac': self.mac,
            'model': self.model,
            'driver': self.driver,
            'address': self.address,
            'mtu': self.mtu,
            'virtualport_type': self.virtualport_type,
            'virtualport_params': self.virtualport_params,
            'port': self.port,
            'portgroup': self.portgroup,
            'inbound': self.inbound,
            'outbound': self.outbound,
            'link_state': self.link_state,
        }
