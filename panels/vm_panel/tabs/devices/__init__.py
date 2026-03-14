"""设备配置模块 - 包含图形、磁盘、hostdev 等子模块."""

from .main import DevicesTab
from .hostdev import USBHostdevTab, PCIHostdevTab, SCSIHostdevTab, MdevHostdevTab
from .disk import DiskDevicesTab, DiskConfigDialog
from .graphics import GraphicsTab
from .others import OthersTab

__all__ = [
    'DevicesTab',
    'USBHostdevTab',
    'PCIHostdevTab',
    'SCSIHostdevTab',
    'MdevHostdevTab',
    'DiskDevicesTab',
    'DiskConfigDialog',
    'GraphicsTab',
    'OthersTab',
]
