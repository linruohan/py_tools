"""设备配置 Tab - 兼容层,从新模块导入所有类."""

# 兼容层:从新的 devices 子模块导入所有类
# 新代码请使用:from panels.vm_panel.tabs.devices import DevicesTab

from .devices import (
    DevicesTab,
    DiskConfigDialog,
    DiskDevicesTab,
    GraphicsTab,
    MdevHostdevTab,
    OthersTab,
    PCIHostdevTab,
    SCSIHostdevTab,
    USBHostdevTab,
)

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
