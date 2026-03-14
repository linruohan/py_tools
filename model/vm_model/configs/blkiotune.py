from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class WeightDevice:
    """设备权重配置"""

    path: str
    weight: int


@dataclass
class DeviceIopsLimit:
    """设备 IOPS 限制配置"""

    path: str
    read_iops_sec: Optional[int] = None
    write_iops_sec: Optional[int] = None


@dataclass
class DeviceBytesLimit:
    """设备字节数限制配置"""

    path: str
    read_bytes_sec: Optional[int] = None
    write_bytes_sec: Optional[int] = None


@dataclass
class BlkioTune:
    """块 IO 调优配置"""

    weight: Optional[int] = None
    weight_devices: List[WeightDevice] = field(default_factory=list)
    read_iops_sec: Optional[int] = None
    write_iops_sec: Optional[int] = None
    read_bytes_sec: Optional[int] = None
    write_bytes_sec: Optional[int] = None
    device_read_iops_sec: List[DeviceIopsLimit] = field(default_factory=list)
    device_write_iops_sec: List[DeviceIopsLimit] = field(default_factory=list)
    device_read_bytes_sec: List[DeviceBytesLimit] = field(default_factory=list)
    device_write_bytes_sec: List[DeviceBytesLimit] = field(default_factory=list)
