"""Memballoon 设备配置 - 整合策略模式."""

from dataclasses import dataclass
from typing import Any


@dataclass
class Memballoon:
    """Memballoon 设备配置"""

    model: str = 'virtio'  # virtio, xen, virtio-transitional, virtio-non-transitional, none
    autodeflate: str | None = None  # on/off
    free_page_reporting: str | None = None  # on/off
    period: int | None = None  # 统计周期
    iommu: str | None = None  # on/off
    ats: str | None = None  # on/off
    address: dict[str, str] | None = None  # 设备地址
    stats: dict[str, Any] | None = None  # 统计配置
    driver: dict[str, str] | None = None  # 驱动配置

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'Memballoon':
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

    def to_dict(self) -> dict[str, Any]:
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
