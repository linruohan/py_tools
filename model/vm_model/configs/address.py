from dataclasses import dataclass
from typing import Optional


@dataclass
class Address:
    """设备地址配置"""

    type: str  # pci, pcie, ide, virtio-serial, usb, ccid, isa, s390
    domain: Optional[str] = None  # 域
    bus: Optional[str] = None  # 总线
    slot: Optional[str] = None  # 插槽
    function: Optional[str] = None  # 功能
    multi: Optional[bool] = None  # 多功能
    base: Optional[str] = None  # 基地址
    size: Optional[str] = None  # 大小
    offset: Optional[str] = None  # 偏移
    vector: Optional[str] = None  # 向量

    @classmethod
    def from_dict(cls, data: dict) -> 'Address':
        """从字典创建"""
        return cls(
            type=data.get('type'),
            domain=data.get('domain'),
            bus=data.get('bus'),
            slot=data.get('slot'),
            function=data.get('function'),
            multi=data.get('multi'),
            base=data.get('base'),
            size=data.get('size'),
            offset=data.get('offset'),
            vector=data.get('vector'),
        )

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            'type': self.type,
            'domain': self.domain,
            'bus': self.bus,
            'slot': self.slot,
            'function': self.function,
            'multi': self.multi,
            'base': self.base,
            'size': self.size,
            'offset': self.offset,
            'vector': self.vector,
        }
