"""Hostdev 设备配置 - 整合策略模式."""

from dataclasses import dataclass
from typing import Any


@dataclass
class Hostdev:
    """Hostdev 设备配置 - PCI/USB/SCSI 直通"""

    mode: str = 'subsystem'  # subsystem, capabilities
    type: str = 'pci'  # pci, usb, scsi, scsi_host, mdev
    managed: bool = True  # 是否由 libvirt 管理
    model: str | None = None  # 设备型号 (vfio-pci, vfio-ccw 等)
    rawio: bool | None = None  # 原始 IO 访问

    # USB 设备属性
    vendor_id: str | None = None  # 厂商 ID
    product_id: str | None = None  # 产品 ID

    # SCSI 设备属性
    host: int | None = None  # SCSI 主机号
    bus: int | None = None  # SCSI 总线号
    target: int | None = None  # SCSI 目标 ID
    unit: int | None = None  # SCSI LUN

    # PCI 设备属性
    domain: str | None = None  # PCI 域
    pci_bus: str | None = None  # PCI 总线
    slot: str | None = None  # PCI 插槽
    function: str | None = None  # PCI 功能

    # 启动配置
    boot_order: int | None = None  # 启动顺序
    boot: dict[str, str] | None = None  # 启动配置

    # ROM 配置
    rom_bar: str | None = None  # ROM BAR
    rom_file: str | None = None  # ROM 文件

    # 驱动配置
    driver: dict[str, str] | None = None  # 驱动配置

    # 地址配置
    address: dict[str, str] | None = None  # 设备地址

    # 共享配置
    readonly: bool = False  # 只读
    shareable: bool = False  # 可共享

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'Hostdev':
        """从字典创建"""
        return cls(
            mode=data.get('mode', 'subsystem'),
            type=data.get('type', 'pci'),
            managed=data.get('managed', True),
            model=data.get('model'),
            rawio=data.get('rawio'),
            vendor_id=data.get('vendor_id'),
            product_id=data.get('product_id'),
            host=data.get('host'),
            bus=data.get('bus'),
            target=data.get('target'),
            unit=data.get('unit'),
            domain=data.get('domain'),
            pci_bus=data.get('pci_bus'),
            slot=data.get('slot'),
            function=data.get('function'),
            boot_order=data.get('boot_order'),
            boot=data.get('boot'),
            rom_bar=data.get('rom_bar'),
            rom_file=data.get('rom_file'),
            driver=data.get('driver'),
            address=data.get('address'),
            readonly=data.get('readonly', False),
            shareable=data.get('shareable', False),
        )

    def to_dict(self) -> dict[str, Any]:
        """转换为字典"""
        return {
            'mode': self.mode,
            'type': self.type,
            'managed': self.managed,
            'model': self.model,
            'rawio': self.rawio,
            'vendor_id': self.vendor_id,
            'product_id': self.product_id,
            'host': self.host,
            'bus': self.bus,
            'target': self.target,
            'unit': self.unit,
            'domain': self.domain,
            'pci_bus': self.pci_bus,
            'slot': self.slot,
            'function': self.function,
            'boot_order': self.boot_order,
            'boot': self.boot,
            'rom_bar': self.rom_bar,
            'rom_file': self.rom_file,
            'driver': self.driver,
            'address': self.address,
            'readonly': self.readonly,
            'shareable': self.shareable,
        }
