from dataclasses import dataclass, field


@dataclass
class WeightDevice:
    """设备权重配置"""

    path: str
    weight: int


@dataclass
class DeviceIopsLimit:
    """设备 IOPS 限制配置"""

    path: str
    read_iops_sec: int | None = None
    write_iops_sec: int | None = None


@dataclass
class DeviceBytesLimit:
    """设备字节数限制配置"""

    path: str
    read_bytes_sec: int | None = None
    write_bytes_sec: int | None = None


@dataclass
class BlkioTune:
    """块 IO 调优配置"""

    weight: int | None = None
    weight_devices: list[WeightDevice] = field(default_factory=list)
    read_iops_sec: int | None = None
    write_iops_sec: int | None = None
    read_bytes_sec: int | None = None
    write_bytes_sec: int | None = None
    device_read_iops_sec: list[DeviceIopsLimit] = field(default_factory=list)
    device_write_iops_sec: list[DeviceIopsLimit] = field(default_factory=list)
    device_read_bytes_sec: list[DeviceBytesLimit] = field(default_factory=list)
    device_write_bytes_sec: list[DeviceBytesLimit] = field(default_factory=list)
