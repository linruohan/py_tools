from dataclasses import dataclass


@dataclass
class Address:
    """设备地址配置"""

    type: str  # pci, pcie, ide, virtio-serial, usb, ccid, isa, s390
    domain: str | None = None  # 域
    bus: str | None = None  # 总线
    slot: str | None = None  # 插槽
    function: str | None = None  # 功能
    multi: bool | None = None  # 多功能
    base: str | None = None  # 基地址
    size: str | None = None  # 大小
    offset: str | None = None  # 偏移
    vector: str | None = None  # 向量

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
