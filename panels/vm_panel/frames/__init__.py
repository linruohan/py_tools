"""Frames - 可滚动配置框架."""

from .disk_frame import ScrollableDiskFrame
from .network_frame import ScrollableNetworkFrame
from .hostdev_frame import ScrollableHostdevFrame

__all__ = [
    'ScrollableDiskFrame',
    'ScrollableNetworkFrame',
    'ScrollableHostdevFrame',
]
