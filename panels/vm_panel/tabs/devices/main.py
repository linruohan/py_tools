"""设备配置主模块 - 组合所有设备子模块."""

from typing import ClassVar

from components.base_tab import BaseConfigTab
from components.inner_tab_panel import InnerTabPanel

from .disk import DiskDevicesTab
from .graphics import GraphicsTab
from .hostdev import MdevHostdevTab, PCIHostdevTab, SCSIHostdevTab, USBHostdevTab
from .others import OthersTab


class DevicesTab(BaseConfigTab):
    """设备配置 Tab - 包含图形、hostdev 子选项."""

    SUB_TABS_CONFIG: ClassVar[dict] = {
        'graphics': {
            'name': 'Graphics',
            'class': GraphicsTab,
            'default': True,
        },
        'disk_devices': {
            'name': 'Disk Devices',
            'class': DiskDevicesTab,
            'default': False,
        },
        'usb_hostdev': {
            'name': 'USB Devices',
            'class': USBHostdevTab,
            'default': False,
        },
        'pci_hostdev': {
            'name': 'PCI Devices',
            'class': PCIHostdevTab,
            'default': False,
        },
        'scsi_hostdev': {
            'name': 'SCSI Devices',
            'class': SCSIHostdevTab,
            'default': False,
        },
        'mdev_hostdev': {
            'name': 'MDEV Devices',
            'class': MdevHostdevTab,
            'default': False,
        },
        'others': {
            'name': 'Other Devices',
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

        # 添加磁盘设备
        for disk in devices_config.get('disk_devices', []):
            disk_xml = self._build_disk_xml(disk)
            devices['disks'].append(disk_xml)

        # 添加 USB 控制器
        hostdevs = devices_config.get('hostdevs', {})
        usb_config = hostdevs.get('usb', {})
        if usb_config.get('controller') and usb_config.get('controller') != 'none':
            devices['controllers'].append(
                {
                    'type': 'usb',
                    'model': usb_config['controller'],
                }
            )

        # 添加 USB 设备
        for usb_dev in usb_config.get('devices', []):
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

        # 添加 SCSI 设备
        for scsi_dev in hostdevs.get('scsi', []):
            devices['hostdevs'].append(
                {
                    'type': 'scsi',
                    'mode': 'subsystem',
                    'source': scsi_dev,
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
