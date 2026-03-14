"""设备配置模块 - 包含图形、磁盘、hostdev 等子模块."""

from .disk import DiskConfigDialog, DiskDevicesTab
from .graphics import GraphicsTab
from .hostdev import MdevHostdevTab, PCIHostdevTab, SCSIHostdevTab, USBHostdevTab
from .devices import DevicesTab
from .others import OthersTab

__all__ = [
    'DevicesTab',
    'DiskConfigDialog',
    'DiskDevicesTab',
    'GraphicsTab',
    'MdevHostdevTab',
    'OthersTab',
    'PCIHostdevTab',
    'SCSIHostdevTab',
    'USBHostdevTab',
]
