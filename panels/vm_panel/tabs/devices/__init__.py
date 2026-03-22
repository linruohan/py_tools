"""设备配置模块 - 包含所有设备子模块."""

# 主模块
from .devices import DevicesTab

# 基础设备
from .graphics import GraphicsTab
from .video_devices import VideoDevicesTab
from .hard_disks import HardDisksTab
from .filesystems import FilesystemsTab
from .network_interfaces import NetworkInterfacesTab
from .controllers import ControllersTab
from .disk import DiskDevicesTab, DiskConfigDialog
from .hostdev import USBHostdevTab, PCIHostdevTab, SCSIHostdevTab, MdevHostdevTab
from .others import OthersTab

# 从 other_devices 导入
from .other_devices import (
    InputDevicesTab,
    HubDevicesTab,
    GraphicalFramebuffersTab,
    SoundDevicesTab,
    WatchdogDevicesTab,
    MemoryBalloonTab,
    TPMDeviceTab,
    ConsolesDevicesTab,
)

# 控制台和串口
from .console_serial import SerialPortTab
from .console_parallel import ParallelPortTab
from .console_console import ConsoleTab
from .console_channel import ChannelTab
from .console_domain_logfile import DomainLogfileTab

# 主机设备
from .host_device_assignment import HostDeviceAssignmentTab
from .redirected_devices import RedirectedDevicesTab
from .smartcard_devices import SmartcardDevicesTab

# 特殊设备
from .random_number_generator import RandomNumberGeneratorTab
from .nvram_device import NVRAMDeviceTab
from .panic_device import PanicDeviceTab
from .vsock import VsockTab
from .crypto import CryptoTab
from .pstore import PstoreTab

# 内存设备
from .memory_devices import MemoryDevicesTab
from .shared_memory_device import SharedMemoryDeviceTab

# 高级功能
from .iommu_devices import IOMMUDevicesTab
from .device_addresses import DeviceAddressesTab
from .device_leases import DeviceLeasesTab
from .virtio import VirtioOptionsTab as VirtioTab

# 音频后端
from .audio_backends import AudioBackendsTab

__all__ = [
    # 主模块
    'DevicesTab',

    # 基础设备
    'GraphicsTab',
    'VideoDevicesTab',
    'HardDisksTab',
    'FilesystemsTab',
    'NetworkInterfacesTab',
    'ControllersTab',
    'DiskDevicesTab',
    'DiskConfigDialog',

    # 其他设备
    'InputDevicesTab',
    'HubDevicesTab',
    'GraphicalFramebuffersTab',
    'SoundDevicesTab',
    'WatchdogDevicesTab',
    'MemoryBalloonTab',
    'TPMDeviceTab',
    'ConsolesDevicesTab',
    'OthersTab',

    # 控制台和串口
    'SerialPortTab',
    'ParallelPortTab',
    'ConsoleTab',
    'ChannelTab',
    'DomainLogfileTab',

    # 主机设备
    'HostDeviceAssignmentTab',
    'RedirectedDevicesTab',
    'SmartcardDevicesTab',
    'USBHostdevTab',
    'PCIHostdevTab',
    'SCSIHostdevTab',
    'MdevHostdevTab',

    # 特殊设备
    'RandomNumberGeneratorTab',
    'NVRAMDeviceTab',
    'PanicDeviceTab',
    'VsockTab',
    'CryptoTab',
    'PstoreTab',

    # 内存设备
    'MemoryDevicesTab',
    'SharedMemoryDeviceTab',

    # 高级功能
    'IOMMUDevicesTab',
    'DeviceAddressesTab',
    'DeviceLeasesTab',
    'VirtioTab',

    # 音频后端
    'AudioBackendsTab',
]
