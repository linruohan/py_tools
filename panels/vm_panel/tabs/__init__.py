"""Tabs - 虚拟机配置 Tab 模块."""

from .basic_tab import BasicTab
from .os_tab import OSTab
from .storage_tab import StorageTab
from .network_tab import NetworkTab
from .devices_tab import DevicesTab
from .features_tab import FeaturesTab
from .hostdev_tab import HostdevTab
from .memory_tab import MemoryTab
from .clock_tab import ClockTab

__all__ = [
    'BasicTab',
    'OSTab',
    'StorageTab',
    'NetworkTab',
    'DevicesTab',
    'FeaturesTab',
    'HostdevTab',
    'MemoryTab',
    'ClockTab',
]
