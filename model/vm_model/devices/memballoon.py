"""Memballoon 设备配置 - 整合策略模式."""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List


@dataclass
class Memballoon:
    """Memballoon 设备配置"""

    model: str = 'virtio'  # virtio, xen, virtio-transitional, virtio-non-transitional, none
    autodeflate: Optional[str] = None  # on/off
    free_page_reporting: Optional[str] = None  # on/off
    period: Optional[int] = None  # 统计周期
    iommu: Optional[str] = None  # on/off
    ats: Optional[str] = None  # on/off
    address: Optional[Dict[str, str]] = None  # 设备地址
    stats: Optional[Dict[str, Any]] = None  # 统计配置
    driver: Optional[Dict[str, str]] = None  # 驱动配置

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Memballoon':
        """从字典创建"""
        return cls(
            model=data.get('model', 'virtio'),
            autodeflate=data.get('autodeflate'),
            free_page_reporting=data.get('free_page_reporting'),
            period=data.get('period'),
            iommu=data.get('iommu'),
            ats=data.get('ats'),
            address=data.get('address'),
            stats=data.get('stats'),
            driver=data.get('driver'),
        )

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'model': self.model,
            'autodeflate': self.autodeflate,
            'free_page_reporting': self.free_page_reporting,
            'period': self.period,
            'iommu': self.iommu,
            'ats': self.ats,
            'address': self.address,
            'stats': self.stats,
            'driver': self.driver,
        }
