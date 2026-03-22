"""设备配置模块 - 包含所有设备子模块."""

# 主模块
# 音频后端
from .audio_backends import AudioBackendsTab
from .console_channel import ChannelTab
from .console_console import ConsoleTab
from .console_domain_logfile import DomainLogfileTab
from .console_parallel import ParallelPortTab

# 控制台和串口
from .console_serial import SerialPortTab
from .controllers import ControllersTab
from .crypto import CryptoTab
from .device_addresses import DeviceAddressesTab
from .device_leases import DeviceLeasesTab
from .devices import DevicesTab
from .disk import DiskConfigDialog, DiskDevicesTab
from .filesystems import FilesystemsTab

# 基础设备
from .graphics import GraphicsTab
from .hard_disks import HardDisksTab

# 主机设备
from .host_device_assignment import HostDeviceAssignmentTab
from .hostdev import MdevHostdevTab, PCIHostdevTab, SCSIHostdevTab, USBHostdevTab

# 高级功能
from .iommu_devices import IOMMUDevicesTab

# 内存设备
from .memory_devices import MemoryDevicesTab
from .network_interfaces import NetworkInterfacesTab
from .nvram_device import NVRAMDeviceTab

# 从 other_devices 导入
from .other_devices import (
    ConsolesDevicesTab,
    GraphicalFramebuffersTab,
    HubDevicesTab,
    InputDevicesTab,
    MemoryBalloonTab,
    SoundDevicesTab,
    TPMDeviceTab,
    WatchdogDevicesTab,
)
from .others import OthersTab
from .panic_device import PanicDeviceTab
from .pstore import PstoreTab

# 特殊设备
from .random_number_generator import RandomNumberGeneratorTab
from .redirected_devices import RedirectedDevicesTab
from .shared_memory_device import SharedMemoryDeviceTab
from .smartcard_devices import SmartcardDevicesTab
from .video_devices import VideoDevicesTab
from .virtio import VirtioOptionsTab as VirtioTab
from .vsock import VsockTab

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
