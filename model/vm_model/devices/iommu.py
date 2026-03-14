"""IOMMU 设备配置 - 整合策略模式."""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List


@dataclass
class IOMMU:
    """IOMMU 设备配置"""

    model: str = 'intel'  # intel, virtio, amd
    caching_mode: Optional[str] = None  # on/off
    aw_bits: Optional[int] = None  # 地址宽度位数 (39, 48, 57, 64)
    intsremap: Optional[str] = None  # on/off (Intel IOMMU)
    eisr: Optional[str] = None  # on/off (Intel IOMMU)
    iotlb: Optional[str] = None  # on/off (Intel IOMMU)
    translation: Optional[str] = None  # MA/PA (virtio IOMMU)
    bus: Optional[int] = None  # PCI 总线号 (virtio IOMMU)
    address: Optional[Dict[str, str]] = None  # 设备地址
    driver: Optional[Dict[str, str]] = None  # 驱动配置

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'IOMMU':
        """从字典创建"""
        return cls(
            model=data.get('model', 'intel'),
            caching_mode=data.get('caching_mode'),
            aw_bits=data.get('aw_bits'),
            intsremap=data.get('intsremap'),
            eisr=data.get('eisr'),
            iotlb=data.get('iotlb'),
            translation=data.get('translation'),
            bus=data.get('bus'),
            address=data.get('address'),
            driver=data.get('driver'),
        )

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'model': self.model,
            'caching_mode': self.caching_mode,
            'aw_bits': self.aw_bits,
            'intsremap': self.intsremap,
            'eisr': self.eisr,
            'iotlb': self.iotlb,
            'translation': self.translation,
            'bus': self.bus,
            'address': self.address,
            'driver': self.driver,
        }
