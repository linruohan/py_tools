"""Frames - 可滚动配置框架."""

from .disk_frame import ScrollableDiskFrame
from .hostdev_frame import ScrollableHostdevFrame
from .network_frame import ScrollableNetworkFrame

__all__ = [
    'ScrollableDiskFrame',
    'ScrollableHostdevFrame',
    'ScrollableNetworkFrame',
]
