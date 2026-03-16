"""设备配置模块 - 包含图形、磁盘、hostdev 等子模块."""

from .disk import DiskConfigDialog, DiskDevicesTab
from .graphics import GraphicsTab
from .hostdev import MdevHostdevTab, PCIHostdevTab, SCSIHostdevTab, USBHostdevTab
from .devices import DevicesTab
from .others import OthersTab
from .hard_disks import HardDisksTab, HardDiskConfigDialog
from .filesystems import FilesystemsTab, FilesystemConfigDialog
from .device_addresses import DeviceAddressesTab, DeviceAddressConfigDialog
from .virtio import VirtioOptionsTab, VirtioDeviceModelsTab
from .controllers import ControllersTab, ControllerConfigDialog
from .device_leases import DeviceLeasesTab, DeviceLeaseConfigDialog
from .host_device_assignment import HostDeviceAssignmentTab, USBPCISCSIDevicesTab, ACPIInitiatorsTab, BlockCharDevicesTab
from .network_interfaces import NetworkInterfacesTab, VirtualNetworkTab, BridgeToLANTab, SLIRPConnectionTab, PasstConnectionTab, DirectAttachmentTab, PCIPassthroughTab, NetworkQoSTab
from .other_devices import InputDevicesTab, HubDevicesTab, GraphicalFramebuffersTab, VideoDevicesTab, ConsolesDevicesTab, SoundDevicesTab, WatchdogDevicesTab, MemoryBalloonTab, TPMDeviceTab
from .audio_backends import AudioBackendsTab
from .random_number_generator import RandomNumberGeneratorTab
from .nvram_device import NVRAMDeviceTab
from .panic_device import PanicDeviceTab
from .shared_memory_device import SharedMemoryDeviceTab
from .memory_devices import MemoryDevicesTab
from .iommu_devices import IOMMUDevicesTab
from .vsock import VsockTab
from .crypto import CryptoTab
from .pstore import PstoreTab
from .console_channel import ChannelTab
from .console_console import ConsoleTab
from .console_domain_logfile import DomainLogfileTab
from .console_parallel import ParallelPortTab
from .console_serial import SerialPortTab
from .redirected_devices import RedirectedDevicesTab
from .smartcard_devices import SmartcardDevicesTab

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
    'HardDisksTab',
    'HardDiskConfigDialog',
    'FilesystemsTab',
    'FilesystemConfigDialog',
    'DeviceAddressesTab',
    'DeviceAddressConfigDialog',
    'VirtioOptionsTab',
    'VirtioDeviceModelsTab',
    'ControllersTab',
    'ControllerConfigDialog',
    'DeviceLeasesTab',
    'DeviceLeaseConfigDialog',
    'HostDeviceAssignmentTab',
    'USBPCISCSIDevicesTab',
    'ACPIInitiatorsTab',
    'BlockCharDevicesTab',
    'NetworkInterfacesTab',
    'VirtualNetworkTab',
    'BridgeToLANTab',
    'SLIRPConnectionTab',
    'PasstConnectionTab',
    'DirectAttachmentTab',
    'PCIPassthroughTab',
    'NetworkQoSTab',
    'InputDevicesTab',
    'HubDevicesTab',
    'GraphicalFramebuffersTab',
    'VideoDevicesTab',
    'ConsolesDevicesTab',
    'SoundDevicesTab',
    'WatchdogDevicesTab',
    'MemoryBalloonTab',
    'TPMDeviceTab',
    'AudioBackendsTab',
    'RandomNumberGeneratorTab',
    'NVRAMDeviceTab',
    'PanicDeviceTab',
    'SharedMemoryDeviceTab',
    'MemoryDevicesTab',
    'IOMMUDevicesTab',
    'VsockTab',
    'CryptoTab',
    'PstoreTab',
    'ChannelTab',
    'ConsoleTab',
    'DomainLogfileTab',
    'ParallelPortTab',
    'SerialPortTab',
    'RedirectedDevicesTab',
    'SmartcardDevicesTab',
]
