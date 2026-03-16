"""设备配置主模块 - 组合所有设备子模块."""

from typing import ClassVar

from components.base_tab import BaseConfigTab
from components.inner_tab_panel import InnerTabPanel

from .audio_backends import AudioBackendsTab
from .controllers import ControllersTab
from .crypto import CryptoTab
from .device_addresses import DeviceAddressesTab
from .device_leases import DeviceLeasesTab
from .disk import DiskDevicesTab
from .filesystems import FilesystemsTab
from .graphics import GraphicsTab
from .hard_disks import HardDisksTab
from .host_device_assignment import (
    ACPIInitiatorsTab,
    BlockCharDevicesTab,
    HostDeviceAssignmentTab,
    USBPCISCSIDevicesTab,
)
from .hostdev import MdevHostdevTab, PCIHostdevTab, SCSIHostdevTab, USBHostdevTab
from .iommu_devices import IOMMUDevicesTab
from .memory_devices import MemoryDevicesTab
from .network_interfaces import (
    BridgeToLANTab,
    DirectAttachmentTab,
    NetworkInterfacesTab,
    NetworkQoSTab,
    PasstConnectionTab,
    PCIPassthroughTab,
    SLIRPConnectionTab,
    VirtualNetworkTab,
)
from .nvram_device import NVRAMDeviceTab
from .other_devices import (
    ConsolesDevicesTab,
    GraphicalFramebuffersTab,
    HubDevicesTab,
    InputDevicesTab,
    MemoryBalloonTab,
    SoundDevicesTab,
    TPMDeviceTab,
    VideoDevicesTab,
    WatchdogDevicesTab,
)
from .others import OthersTab
from .panic_device import PanicDeviceTab
from .pstore import PstoreTab
from .random_number_generator import RandomNumberGeneratorTab
from .redirected_devices import RedirectedDevicesTab
from .shared_memory_device import SharedMemoryDeviceTab
from .smartcard_devices import SmartcardDevicesTab
from .virtio import VirtioDeviceModelsTab, VirtioOptionsTab
from .vsock import VsockTab


class DevicesTab(BaseConfigTab):
    """设备配置 Tab - 包含图形、hostdev 子选项."""

    SUB_TABS_CONFIG: ClassVar[dict] = {
        'graphics': {
            'name': 'Graphics',
            'class': GraphicsTab,
            'default': True,
        },
        'hard_disks': {
            'name': 'Hard drives, floppy disks, CDROMs',
            'class': HardDisksTab,
            'default': False,
        },
        'filesystems': {
            'name': 'Filesystems',
            'class': FilesystemsTab,
            'default': False,
        },
        'device_addresses': {
            'name': 'Device Addresses',
            'class': DeviceAddressesTab,
            'default': False,
        },
        'virtio_options': {
            'name': 'Virtio-related options',
            'class': VirtioOptionsTab,
            'default': False,
        },
        'virtio_models': {
            'name': 'Virtio device models',
            'class': VirtioDeviceModelsTab,
            'default': False,
        },
        'controllers': {
            'name': 'Controllers',
            'class': ControllersTab,
            'default': False,
        },
        'device_leases': {
            'name': 'Device leases',
            'class': DeviceLeasesTab,
            'default': False,
        },
        'host_device_assignment': {
            'name': 'Host device assignment',
            'class': HostDeviceAssignmentTab,
            'default': False,
        },
        'usb_pci_scsi': {
            'name': 'USB / PCI / SCSI devices',
            'class': USBPCISCSIDevicesTab,
            'default': False,
        },
        'acpi_initiators': {
            'name': 'ACPI Generic Initiators',
            'class': ACPIInitiatorsTab,
            'default': False,
        },
        'block_char_devices': {
            'name': 'Block / character devices',
            'class': BlockCharDevicesTab,
            'default': False,
        },
        'network_interfaces': {
            'name': 'Network interfaces',
            'class': NetworkInterfacesTab,
            'default': False,
        },
        'virtual_network': {
            'name': 'Virtual network',
            'class': VirtualNetworkTab,
            'default': False,
        },
        'bridge_to_lan': {
            'name': 'Bridge to LAN',
            'class': BridgeToLANTab,
            'default': False,
        },
        'slirp_connection': {
            'name': 'Userspace connection using SLIRP',
            'class': SLIRPConnectionTab,
            'default': False,
        },
        'passt_connection': {
            'name': 'Userspace connection using passt',
            'class': PasstConnectionTab,
            'default': False,
        },
        'direct_attachment': {
            'name': 'Direct attachment to physical interface',
            'class': DirectAttachmentTab,
            'default': False,
        },
        'pci_passthrough': {
            'name': 'PCI Passthrough',
            'class': PCIPassthroughTab,
            'default': False,
        },
        'network_qos': {
            'name': 'Quality of service',
            'class': NetworkQoSTab,
            'default': False,
        },
        'input_devices': {
            'name': 'Input devices',
            'class': InputDevicesTab,
            'default': False,
        },
        'hub_devices': {
            'name': 'Hub devices',
            'class': HubDevicesTab,
            'default': False,
        },
        'graphical_framebuffers': {
            'name': 'Graphical framebuffers',
            'class': GraphicalFramebuffersTab,
            'default': False,
        },
        'video_devices': {
            'name': 'Video devices',
            'class': VideoDevicesTab,
            'default': False,
        },
        'consoles_devices': {
            'name': 'Consoles, serial, parallel & channel devices',
            'class': ConsolesDevicesTab,
            'default': False,
        },
        'sound_devices': {
            'name': 'Sound devices',
            'class': SoundDevicesTab,
            'default': False,
        },
        'audio_backends': {
            'name': 'Audio backends',
            'class': AudioBackendsTab,
            'default': False,
        },
        'watchdog_devices': {
            'name': 'Watchdog devices',
            'class': WatchdogDevicesTab,
            'default': False,
        },
        'memory_balloon': {
            'name': 'Memory balloon device',
            'class': MemoryBalloonTab,
            'default': False,
        },
        'random_number_generator': {
            'name': 'Random number generator device',
            'class': RandomNumberGeneratorTab,
            'default': False,
        },
        'tpm_device': {
            'name': 'TPM device',
            'class': TPMDeviceTab,
            'default': False,
        },
        'nvram_device': {
            'name': 'NVRAM device',
            'class': NVRAMDeviceTab,
            'default': False,
        },
        'panic_device': {
            'name': 'Panic device',
            'class': PanicDeviceTab,
            'default': False,
        },
        'shared_memory_device': {
            'name': 'Shared memory device',
            'class': SharedMemoryDeviceTab,
            'default': False,
        },
        'memory_devices': {
            'name': 'Memory devices',
            'class': MemoryDevicesTab,
            'default': False,
        },
        'iommu_devices': {
            'name': 'IOMMU devices',
            'class': IOMMUDevicesTab,
            'default': False,
        },
        'vsock': {
            'name': 'Vsock',
            'class': VsockTab,
            'default': False,
        },
        'crypto': {
            'name': 'Crypto',
            'class': CryptoTab,
            'default': False,
        },
        'pstore': {
            'name': 'Pstore',
            'class': PstoreTab,
            'default': False,
        },
        'redirected_devices': {
            'name': 'Redirected devices',
            'class': RedirectedDevicesTab,
            'default': False,
        },
        'smartcard_devices': {
            'name': 'Smartcard devices',
            'class': SmartcardDevicesTab,
            'default': False,
        },
        'disk_devices': {
            'name': 'Disk Devices (Legacy)',
            'class': DiskDevicesTab,
            'default': False,
        },
        'usb_hostdev': {
            'name': 'USB Devices (Legacy)',
            'class': USBHostdevTab,
            'default': False,
        },
        'pci_hostdev': {
            'name': 'PCI Devices (Legacy)',
            'class': PCIHostdevTab,
            'default': False,
        },
        'scsi_hostdev': {
            'name': 'SCSI Devices (Legacy)',
            'class': SCSIHostdevTab,
            'default': False,
        },
        'mdev_hostdev': {
            'name': 'MDEV Devices (Legacy)',
            'class': MdevHostdevTab,
            'default': False,
        },
        'others': {
            'name': 'Other Devices (Legacy)',
            'class': OthersTab,
            'default': False,
        },
    }

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, on_change_callback, **kwargs)

        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.inner_panel = InnerTabPanel(
            self,
            tabs_config=self.SUB_TABS_CONFIG,
            on_change_callback=self.on_change_callback,
        )
        self.inner_panel.grid(row=0, column=0, sticky='nsew')

    def get_graphics_config(self):
        """获取图形配置."""
        graphics_tab = self.inner_panel.get_tab_instance('graphics')
        if graphics_tab and hasattr(graphics_tab, 'get_config'):
            return graphics_tab.get_config()
        return {
            'type': 'vnc',
            'listen': '0.0.0.0',
            'port': '-1',
            'video_model': 'qxl',
            'vram': 64,
        }

    def get_serial_config(self):
        """获取串口配置."""
        others_tab = self.inner_panel.get_tab_instance('others')
        if others_tab and hasattr(others_tab, 'get_serial_config'):
            return others_tab.get_serial_config()
        return {'type': 'pty', 'port': '0'}

    def get_tpm_config(self):
        """获取 TPM 配置."""
        others_tab = self.inner_panel.get_tab_instance('others')
        if others_tab and hasattr(others_tab, 'get_tpm_config'):
            return others_tab.get_tpm_config()
        return None

    def get_audio_config(self):
        """获取音频配置."""
        others_tab = self.inner_panel.get_tab_instance('others')
        if others_tab and hasattr(others_tab, 'get_audio_config'):
            return others_tab.get_audio_config()
        return {'model': 'ich9'}

    def get_controller_config(self):
        """获取控制器配置."""
        others_tab = self.inner_panel.get_tab_instance('others')
        if others_tab and hasattr(others_tab, 'get_controller_config'):
            return others_tab.get_controller_config()
        return {'disable_usb': False, 'disable_sound': False}

    def get_controllers_config(self):
        """获取控制器配置."""
        controllers_tab = self.inner_panel.get_tab_instance('controllers')
        if controllers_tab and hasattr(controllers_tab, 'get_config'):
            config = controllers_tab.get_config()
            return config.get('controllers', [])
        return []

    def get_disk_devices_config(self) -> list:
        """获取磁盘设备配置."""
        disk_tab = self.inner_panel.get_tab_instance('disk_devices')
        if disk_tab and hasattr(disk_tab, 'get_config'):
            config = disk_tab.get_config()
            return config.get('devices', [])
        return []

    def get_hostdev_configs(self) -> dict:
        """获取所有 hostdev 配置."""
        hostdevs = {
            'usb': [],
            'pci': [],
            'scsi': [],
            'mdev': [],
        }

        # USB
        usb_tab = self.inner_panel.get_tab_instance('usb_hostdev')
        if usb_tab and hasattr(usb_tab, 'get_config'):
            config = usb_tab.get_config()
            hostdevs['usb'] = {
                'controller': config.get('controller'),
                'devices': config.get('devices', []),
                'startup_policy': config.get('startup_policy'),
                'guest_reset': config.get('guest_reset'),
            }

        # PCI
        pci_tab = self.inner_panel.get_tab_instance('pci_hostdev')
        if pci_tab and hasattr(pci_tab, 'get_config'):
            config = pci_tab.get_config()
            hostdevs['pci'] = config.get('devices', [])

        # SCSI
        scsi_tab = self.inner_panel.get_tab_instance('scsi_hostdev')
        if scsi_tab and hasattr(scsi_tab, 'get_config'):
            config = scsi_tab.get_config()
            hostdevs['scsi'] = config.get('devices', [])

        # MDEV
        mdev_tab = self.inner_panel.get_tab_instance('mdev_hostdev')
        if mdev_tab and hasattr(mdev_tab, 'get_config'):
            config = mdev_tab.get_config()
            hostdevs['mdev'] = config.get('devices', [])

        return hostdevs

    def get_devices_config(self):
        """获取所有设备配置."""
        return {
            'graphics': self.get_graphics_config(),
            'serial': self.get_serial_config(),
            'tpm': self.get_tpm_config(),
            'audio': self.get_audio_config(),
            'disable_usb': self.get_controller_config().get('disable_usb', False),
            'disable_sound': self.get_controller_config().get('disable_sound', False),
            'hostdevs': self.get_hostdev_configs(),
            'disk_devices': self.get_disk_devices_config(),
            'controllers': self.get_controllers_config(),
        }

    def to_xml(self) -> dict:
        """生成 XML 配置字典."""
        devices_config = self.get_devices_config()
        devices = {
            'emulator': '/usr/bin/qemu-system-x86_64',
            'graphics': devices_config.get('graphics'),
            'videos': [
                {
                    'model': devices_config.get('graphics', {}).get('video_model', 'qxl'),
                    'vram': devices_config.get('graphics', {}).get('vram', 64),
                }
            ],
            'controllers': [],
            'serials': [],
            'sounds': [],
            'hostdevs': [],
            'disks': [],
        }

        # 收集已有的控制器类型
        existing_controllers = set()
        for controller in devices_config.get('controllers', []):
            ctrl_type = controller.get('type')
            if ctrl_type:
                existing_controllers.add(ctrl_type)
            devices['controllers'].append(controller)

        # 添加磁盘设备
        for disk in devices_config.get('disk_devices', []):
            disk_xml = self._build_disk_xml(disk)
            devices['disks'].append(disk_xml)

            # 检查磁盘设备的总线类型，添加相应的控制器
            bus = disk.get('bus')
            if bus:
                if bus == 'scsi' and 'scsi' not in existing_controllers:
                    devices['controllers'].append({'type': 'scsi', 'model': 'virtio-scsi'})
                    existing_controllers.add('scsi')
                elif bus == 'usb' and 'usb' not in existing_controllers:
                    devices['controllers'].append({'type': 'usb', 'model': 'usb-xhci'})
                    existing_controllers.add('usb')
                elif bus == 'sata' and 'sata' not in existing_controllers:
                    devices['controllers'].append({'type': 'sata', 'model': 'sata'})
                    existing_controllers.add('sata')

        # 处理主机设备
        hostdevs = devices_config.get('hostdevs', {})

        # 添加 USB 控制器和设备
        usb_config = hostdevs.get('usb', {})
        if usb_config.get('controller') and usb_config.get('controller') != 'none':
            if 'usb' not in existing_controllers:
                devices['controllers'].append(
                    {
                        'type': 'usb',
                        'model': usb_config['controller'],
                    }
                )
                existing_controllers.add('usb')

        # 添加 USB 设备
        for usb_dev in usb_config.get('devices', []):
            if 'usb' not in existing_controllers:
                devices['controllers'].append({'type': 'usb', 'model': 'usb-xhci'})
                existing_controllers.add('usb')
            devices['hostdevs'].append(
                {
                    'type': 'usb',
                    'mode': 'subsystem',
                    'source': {
                        'vendor_product': usb_dev,
                        'startup_policy': usb_config.get('startup_policy', 'optional'),
                        'guest_reset': usb_config.get('guest_reset', False),
                    },
                }
            )

        # 添加 SCSI 设备
        for scsi_dev in hostdevs.get('scsi', []):
            if 'scsi' not in existing_controllers:
                devices['controllers'].append({'type': 'scsi', 'model': 'virtio-scsi'})
                existing_controllers.add('scsi')
            devices['hostdevs'].append(
                {
                    'type': 'scsi',
                    'mode': 'subsystem',
                    'source': scsi_dev,
                }
            )

        # 添加 PCI 设备
        for pci_dev in hostdevs.get('pci', []):
            devices['hostdevs'].append(
                {
                    'type': 'pci',
                    'mode': 'subsystem',
                    'managed': pci_dev.get('managed', 'yes'),
                    'source': {
                        'domain': pci_dev.get('domain', '0x0000'),
                        'bus': pci_dev.get('bus', '0x00'),
                        'slot': pci_dev.get('slot', '0x00'),
                        'function': pci_dev.get('function', '0x0'),
                    },
                    'boot_order': pci_dev.get('boot_order'),
                    'rom_bar': pci_dev.get('rom_bar'),
                    'rom_file': pci_dev.get('rom_file'),
                }
            )

        # 添加 MDEV 设备
        for mdev_dev in hostdevs.get('mdev', []):
            devices['hostdevs'].append(
                {
                    'type': 'mdev',
                    'mode': 'subsystem',
                    'model': mdev_dev.get('model', 'vfio-pci'),
                    'source': {
                        'uuid': mdev_dev.get('uuid'),
                    },
                }
            )

        # 添加串口
        serial_config = devices_config.get('serial', {})
        if serial_config.get('type') and serial_config.get('type') != 'none':
            devices['serials'].append(
                {
                    'type': serial_config['type'],
                    'port': serial_config.get('port', '0'),
                }
            )

        # 添加音频
        audio_config = devices_config.get('audio', {})
        if audio_config and audio_config.get('model') != 'none':
            devices['sounds'].append({'model': audio_config['model']})

        return {'devices': devices}

    def _build_disk_xml(self, disk: dict) -> dict:
        """构建磁盘设备 XML 字典."""
        disk_type = disk.get('type', 'file')
        device_type = disk.get('device', 'disk')

        disk_xml = {
            'type': disk_type,
            'device': device_type,
            'target': {
                'dev': disk.get('target_dev', 'vda'),
                'bus': disk.get('bus', 'virtio'),
            },
            'readonly': disk.get('readonly', False),
            'boot_order': disk.get('boot_order'),
            'startup_policy': disk.get('startup_policy'),
        }

        # 根据类型设置 source
        if disk_type == 'file':
            disk_xml['source'] = disk.get('source', '')
            disk_xml['driver'] = disk.get('driver', 'qcow2')
        elif disk_type == 'block':
            disk_xml['source'] = disk.get('source', '')
        elif disk_type == 'network':
            disk_xml['protocol'] = disk.get('protocol', 'rbd')
            disk_xml['source'] = disk.get('source', '')
            disk_xml['host'] = disk.get('host', '')
            disk_xml['port'] = disk.get('port', '')
            if disk.get('username') and disk.get('secret'):
                disk_xml['auth'] = {
                    'username': disk['username'],
                    'secret': disk['secret'],
                }
        elif disk_type == 'volume':
            disk_xml['pool'] = disk.get('pool', '')
            disk_xml['volume'] = disk.get('volume', '')
        elif disk_type == 'dir':
            disk_xml['source'] = disk.get('source', '')
        elif disk_type == 'nvme':
            disk_xml['namespace'] = disk.get('namespace', '1')
            disk_xml['pci'] = disk.get('pci', '')
        elif disk_type == 'vhostuser':
            disk_xml['source'] = disk.get('source', '')
        elif disk_type == 'vhostvdpa':
            disk_xml['source'] = disk.get('source', '')
        elif disk_type == 'ctl':
            disk_xml['source'] = disk.get('source', '')

        return disk_xml
