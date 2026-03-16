"""设备配置主模块 - 组合所有设备子模块."""

from typing import Any

import customtkinter as ctk

from components.base_tab import BaseConfigTab
from components.search_filter import SearchFilter
from utils.styles import BG_COLOR_CONTENT, CTK_FONT_SMALL

from .audio_backends import AudioBackendsTab
from .controllers import ControllersTab
from .crypto import CryptoTab
from .device_addresses import DeviceAddressesTab
from .filesystems import FilesystemsTab
from .graphics import GraphicsTab
from .hard_disks import HardDisksTab
from .host_device_assignment import (
    HostDeviceAssignmentTab,
)
from .iommu_devices import IOMMUDevicesTab
from .memory_devices import MemoryDevicesTab
from .network_interfaces import (
    NetworkInterfacesTab,
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
from .panic_device import PanicDeviceTab
from .pstore import PstoreTab
from .random_number_generator import RandomNumberGeneratorTab
from .redirected_devices import RedirectedDevicesTab
from .shared_memory_device import SharedMemoryDeviceTab
from .smartcard_devices import SmartcardDevicesTab
from .vsock import VsockTab


class DevicesTab(BaseConfigTab):
    """设备配置 Tab - 包含图形、hostdev 子选项."""

    # 设备类型配置
    DEVICE_TYPES = [
        {'value': 'graphics', 'label': 'Graphics'},
        {'value': 'hard_disks', 'label': 'Hard drives, floppy disks, CDROMs'},
        {'value': 'filesystems', 'label': 'Filesystems'},
        {'value': 'device_addresses', 'label': 'Device Addresses'},
        {'value': 'controllers', 'label': 'Controllers'},
        {'value': 'host_device_assignment', 'label': 'Host device assignment'},
        {'value': 'network_interfaces', 'label': 'Network interfaces'},
        {'value': 'input_devices', 'label': 'Input devices'},
        {'value': 'hub_devices', 'label': 'Hub devices'},
        {'value': 'graphical_framebuffers', 'label': 'Graphical framebuffers'},
        {'value': 'video_devices', 'label': 'Video devices'},
        {'value': 'consoles_devices', 'label': 'Consoles, serial, parallel & channel devices'},
        {'value': 'sound_devices', 'label': 'Sound devices'},
        {'value': 'audio_backends', 'label': 'Audio backends'},
        {'value': 'watchdog_devices', 'label': 'Watchdog devices'},
        {'value': 'memory_balloon', 'label': 'Memory balloon device'},
        {'value': 'random_number_generator', 'label': 'Random number generator device'},
        {'value': 'tpm_device', 'label': 'TPM device'},
        {'value': 'nvram_device', 'label': 'NVRAM device'},
        {'value': 'panic_device', 'label': 'Panic device'},
        {'value': 'shared_memory_device', 'label': 'Shared memory device'},
        {'value': 'memory_devices', 'label': 'Memory devices'},
        {'value': 'iommu_devices', 'label': 'IOMMU devices'},
        {'value': 'vsock', 'label': 'Vsock'},
        {'value': 'crypto', 'label': 'Crypto'},
        {'value': 'pstore', 'label': 'Pstore'},
        {'value': 'redirected_devices', 'label': 'Redirected devices'},
        {'value': 'smartcard_devices', 'label': 'Smartcard devices'},
    ]

    # 设备类映射
    DEVICE_CLASSES = {
        'graphics': GraphicsTab,
        'hard_disks': HardDisksTab,
        'filesystems': FilesystemsTab,
        'device_addresses': DeviceAddressesTab,
        'controllers': ControllersTab,
        'host_device_assignment': HostDeviceAssignmentTab,
        'network_interfaces': NetworkInterfacesTab,
        'input_devices': InputDevicesTab,
        'hub_devices': HubDevicesTab,
        'graphical_framebuffers': GraphicalFramebuffersTab,
        'video_devices': VideoDevicesTab,
        'consoles_devices': ConsolesDevicesTab,
        'sound_devices': SoundDevicesTab,
        'audio_backends': AudioBackendsTab,
        'watchdog_devices': WatchdogDevicesTab,
        'memory_balloon': MemoryBalloonTab,
        'random_number_generator': RandomNumberGeneratorTab,
        'tpm_device': TPMDeviceTab,
        'nvram_device': NVRAMDeviceTab,
        'panic_device': PanicDeviceTab,
        'shared_memory_device': SharedMemoryDeviceTab,
        'memory_devices': MemoryDevicesTab,
        'iommu_devices': IOMMUDevicesTab,
        'vsock': VsockTab,
        'crypto': CryptoTab,
        'pstore': PstoreTab,
        'redirected_devices': RedirectedDevicesTab,
        'smartcard_devices': SmartcardDevicesTab,
    }

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, on_change_callback, **kwargs)
        self.devices_list = []  # 存储已添加的设备
        self.current_device_tab = None  # 当前设备配置标签页
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面 - 上下二层布局"""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)  # 第一层：设备类型搜索和设备配置
        self.grid_rowconfigure(1, weight=0)  # 第二层：已添加设备列表

        # 第一层：设备类型搜索和设备配置
        top_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        top_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        top_frame.grid_columnconfigure(1, weight=1)
        top_frame.grid_rowconfigure(0, weight=0)
        top_frame.grid_rowconfigure(1, weight=1)

        # 第一行：设备类型搜索和添加设备按钮
        # 设置列权重：column 0 和 2 为固定宽度，column 1 占据剩余空间
        top_frame.grid_columnconfigure(0, weight=0)  # Label 固定宽度
        top_frame.grid_columnconfigure(1, weight=1)  # SearchFilter 占据剩余空间
        top_frame.grid_columnconfigure(2, weight=0)  # 按钮固定宽度

        ctk.CTkLabel(top_frame, text='设备类型:', font=CTK_FONT_SMALL).grid(
            row=0, column=0, padx=5, pady=5, sticky='w'
        )

        # 设备类型搜索组件
        self.device_type_search = SearchFilter(
            top_frame,
            items=[device['label'] for device in self.DEVICE_TYPES],
            on_select_callback=self._on_device_type_select,
            placeholder_text='输入设备类型关键词...',
        )
        self.device_type_search.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        # 添加设备按钮
        self.add_device_btn = ctk.CTkButton(
            top_frame,
            text='添加设备',
            width=100,
            height=32,
            font=CTK_FONT_SMALL,
            command=self._add_device,
        )
        self.add_device_btn.grid(row=0, column=2, padx=5, pady=5, sticky='e')

        # 第二行：设备配置
        self.config_frame = ctk.CTkFrame(top_frame, fg_color='transparent')
        self.config_frame.grid(row=1, column=0, columnspan=3, sticky='nsew', padx=5, pady=5)
        self.config_frame.grid_columnconfigure(0, weight=1)
        self.config_frame.grid_rowconfigure(0, weight=1)

        # 第二层：已添加设备列表
        bottom_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        bottom_frame.grid(row=1, column=0, sticky='ew', padx=5, pady=5)
        bottom_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(bottom_frame, text='已添加设备:', font=CTK_FONT_SMALL).grid(
            row=0, column=0, padx=5, pady=5, sticky='w'
        )

        self.devices_list_frame = ctk.CTkScrollableFrame(bottom_frame, fg_color='transparent')
        self.devices_list_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
        self.devices_list_frame.grid_columnconfigure(0, weight=1)

    def _on_device_type_select(self, selected_label) -> None:
        """设备类型选择时的处理"""
        # 清空当前配置框架
        for widget in self.config_frame.winfo_children():
            widget.destroy()

        if not selected_label:
            return

        # 查找对应的设备类型值
        selected_device = None
        for device in self.DEVICE_TYPES:
            if device['label'] == selected_label:
                selected_device = device
                break

        if not selected_device:
            return

        # 获取设备类并创建实例
        device_class = self.DEVICE_CLASSES.get(selected_device['value'])
        if device_class:
            self.current_device_tab = device_class(
                self.config_frame, on_change_callback=self.on_change_callback
            )
            self.current_device_tab.grid(row=0, column=0, sticky='nsew')

    def _add_device(self) -> None:
        """添加设备到列表"""
        # 获取选中的设备类型
        selected_label = self.device_type_search.get_selected_item()
        if not selected_label:
            return

        # 查找对应的设备类型值
        selected_device = None
        for device in self.DEVICE_TYPES:
            if device['label'] == selected_label:
                selected_device = device
                break

        if not selected_device or not self.current_device_tab:
            return

        # 获取设备配置
        if hasattr(self.current_device_tab, 'get_config'):
            device_config = self.current_device_tab.get_config()
            device_info = {
                'type': selected_device['value'],
                'label': selected_device['label'],
                'config': device_config,
            }

            # 添加设备到列表
            self.devices_list.append(device_info)
            self._update_devices_list()

            # 处理设备间的关联关系
            self._handle_device_relations(device_info)

            # 触发变化回调
            if self.on_change_callback:
                self.on_change_callback()

    def _handle_device_relations(self, device_info: dict[str, Any]) -> None:
        """处理设备间的关联关系"""
        device_type = device_info['type']

        # 示例：添加SCSI设备时，自动添加SCSI控制器
        if device_type == 'scsi_hostdev':
            # 检查是否已存在SCSI控制器
            scsi_controller_exists = False
            for device in self.devices_list:
                if device['type'] == 'controllers' and 'scsi' in device['config'].get(
                    'controllers', []
                ):
                    scsi_controller_exists = True
                    break

            if not scsi_controller_exists:
                # 添加SCSI控制器
                scsi_controller_info = {
                    'type': 'controllers',
                    'label': 'Controllers',
                    'config': {'controllers': [{'type': 'scsi', 'model': 'virtio-scsi'}]},
                }
                self.devices_list.append(scsi_controller_info)

        # 示例：添加USB设备时，自动添加USB控制器
        elif device_type == 'usb_hostdev':
            # 检查是否已存在USB控制器
            usb_controller_exists = False
            for device in self.devices_list:
                if device['type'] == 'controllers' and 'usb' in device['config'].get(
                    'controllers', []
                ):
                    usb_controller_exists = True
                    break

            if not usb_controller_exists:
                # 添加USB控制器
                usb_controller_info = {
                    'type': 'controllers',
                    'label': 'Controllers',
                    'config': {'controllers': [{'type': 'usb', 'model': 'usb-xhci'}]},
                }
                self.devices_list.append(usb_controller_info)

    def _update_devices_list(self) -> None:
        """更新设备列表显示"""
        # 清空列表框架
        for widget in self.devices_list_frame.winfo_children():
            widget.destroy()

        # 显示设备列表
        for i, device in enumerate(self.devices_list):
            device_frame = ctk.CTkFrame(
                self.devices_list_frame, fg_color='#444444', corner_radius=4
            )
            device_frame.grid(row=i, column=0, sticky='ew', padx=5, pady=3)
            device_frame.grid_columnconfigure(0, weight=1)

            # 设备名称
            ctk.CTkLabel(device_frame, text=device['label'], font=CTK_FONT_SMALL).grid(
                row=0, column=0, padx=5, pady=3, sticky='w'
            )

            # 编辑按钮
            edit_btn = ctk.CTkButton(
                device_frame,
                text='编辑',
                width=60,
                height=24,
                font=CTK_FONT_SMALL,
                command=lambda idx=i: self._edit_device(idx),
            )
            edit_btn.grid(row=0, column=1, padx=5, pady=3)

            # 删除按钮
            delete_btn = ctk.CTkButton(
                device_frame,
                text='删除',
                width=60,
                height=24,
                font=CTK_FONT_SMALL,
                fg_color='#D32F2F',
                hover_color='#B71C1C',
                command=lambda idx=i: self._delete_device(idx),
            )
            delete_btn.grid(row=0, column=2, padx=5, pady=3)

    def _edit_device(self, index: int) -> None:
        """编辑设备"""
        if 0 <= index < len(self.devices_list):
            device = self.devices_list[index]
            # 设置设备类型选择
            for device_type in self.DEVICE_TYPES:
                if device_type['value'] == device['type']:
                    self.device_type_search.set_selected_item(device_type['label'])
                    break
            # 触发设备类型变化，显示配置界面
            selected_label = self.device_type_search.get_selected_item()
            self._on_device_type_select(selected_label)
            # TODO: 加载设备配置到编辑界面

    def _delete_device(self, index: int) -> None:
        """删除设备"""
        if 0 <= index < len(self.devices_list):
            self.devices_list.pop(index)
            self._update_devices_list()
            if self.on_change_callback:
                self.on_change_callback()

    def get_graphics_config(self):
        """获取图形配置."""
        for device in self.devices_list:
            if device['type'] == 'graphics' and 'config' in device:
                return device['config']
        return {
            'type': 'vnc',
            'listen': '0.0.0.0',
            'port': '-1',
            'video_model': 'qxl',
            'vram': 64,
        }

    def get_serial_config(self):
        """获取串口配置."""
        for device in self.devices_list:
            if device['type'] == 'consoles_devices' and 'config' in device:
                return device['config'].get('serial', {'type': 'pty', 'port': '0'})
        return {'type': 'pty', 'port': '0'}

    def get_tpm_config(self):
        """获取 TPM 配置."""
        for device in self.devices_list:
            if device['type'] == 'tpm_device' and 'config' in device:
                return device['config']
        return None

    def get_audio_config(self):
        """获取音频配置."""
        for device in self.devices_list:
            if device['type'] == 'sound_devices' and 'config' in device:
                return device['config']
        return {'model': 'ich9'}

    def get_controller_config(self):
        """获取控制器配置."""
        return {'disable_usb': False, 'disable_sound': False}

    def get_controllers_config(self):
        """获取控制器配置."""
        for device in self.devices_list:
            if device['type'] == 'controllers' and 'config' in device:
                return device['config'].get('controllers', [])
        return []

    def get_disk_devices_config(self) -> list:
        """获取磁盘设备配置."""
        for device in self.devices_list:
            if device['type'] == 'hard_disks' and 'config' in device:
                return device['config'].get('devices', [])
        return []

    def get_hostdev_configs(self) -> dict:
        """获取所有 hostdev 配置."""
        hostdevs = {
            'usb': [],
            'pci': [],
            'scsi': [],
            'mdev': [],
        }

        for device in self.devices_list:
            if device['type'] == 'host_device_assignment' and 'config' in device:
                config = device['config']
                # 根据配置类型添加到相应的hostdev类别
                if 'usb' in config:
                    hostdevs['usb'] = config['usb']
                if 'pci' in config:
                    hostdevs['pci'] = config['pci']
                if 'scsi' in config:
                    hostdevs['scsi'] = config['scsi']
                if 'mdev' in config:
                    hostdevs['mdev'] = config['mdev']

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
