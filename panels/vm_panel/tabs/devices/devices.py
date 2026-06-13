"""设备配置模块 - 重新设计的 UI，上下布局，选择后直接添加到列表."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, ClassVar

import customtkinter as ctk

from components.base_tab import BaseConfigTab
from utils.styles import (
    BG_COLOR_CONTENT,
    CTK_FONT_BOLD,
    CTK_FONT_SMALL,
)


@dataclass
class DeviceConfig:
    """设备配置数据类."""

    device_type: str
    device_label: str
    config: dict
    controller_ref: str | None = None  # 关联的 controller 引用


class DevicesConfigTab(BaseConfigTab):
    """设备配置 Tab - 重新设计的 UI.

    功能特性:
    - 上下布局：上部设备选择（固定一行），下部已添加设备列表（滚动显示）
    - 上面部分选择一个设备类型后，直接添加到下面的列表
    - 设备配置参数在列表中每行显示
    - 支持设备关联（如 SCSI 设备自动添加 controller）
    - 删除最后一个关联设备时自动删除 controller
    """

    # 所有设备类型 (根据 libvirt devices 文档)
    DEVICE_TYPES: ClassVar[dict[str, str]] = {
        # ========== 基础设备 ==========
        'disk': 'Disk (磁盘/光驱/软驱)',
        'filesystem': 'Filesystem (文件系统)',
        'controller': 'Controller (控制器)',
        'interface': 'Network Interface (网络接口)',
        'input': 'Input Device (输入设备)',
        'hub': 'Hub Device (集线器)',
        'graphics': 'Graphics (图形显示)',
        'video': 'Video Device (视频设备)',
        'sound': 'Sound Device (音频设备)',
        'audio': 'Audio Backend (音频后端)',
        'console': 'Console (控制台)',
        'serial': 'Serial Port (串口)',
        'parallel': 'Parallel Port (并口)',
        'channel': 'Channel (通道)',
        # ========== 主机设备 ==========
        'hostdev': 'Host Device (USB/PCI/SCSI/MDEV)',
        'smartcard': 'Smartcard Device (智能卡)',
        'redirecteddev': 'Redirected Device (重定向设备)',
        # ========== 特殊设备 ==========
        'watchdog': 'Watchdog Device (看门狗)',
        'memballoon': 'Memory Balloon (内存气球)',
        'rng': 'RNG (随机数发生器)',
        'tpm': 'TPM Device (可信平台模块)',
        'nvram': 'NVRAM Device',
        'panic': 'Panic Device',
        'vsock': 'Vsock Device',
        'crypto': 'Crypto Device (加密设备)',
        'pstore': 'Pstore (持久存储)',
        'shmem': 'Shared Memory (共享内存)',
        'memory': 'Memory Device (内存设备)',
        'iommu': 'IOMMU Device',
    }

    # 设备类别分组
    DEVICE_CATEGORIES: ClassVar[dict[str, str]] = {
        'all': 'All Devices (所有设备)',
        'base': 'Base Devices (基础设备)',
        'console': 'Consoles & Ports (控制台和端口)',
        'hostdev': 'Host Devices (主机设备)',
        'special': 'Special Devices (特殊设备)',
        'memory': 'Memory Devices (内存设备)',
        'advanced': 'Advanced (高级功能)',
    }

    # 类别与设备类型的映射
    CATEGORY_DEVICES: ClassVar[dict[str, list[str]]] = {
        'base': [
            'disk',
            'filesystem',
            'controller',
            'interface',
            'input',
            'hub',
            'graphics',
            'video',
            'sound',
            'audio',
        ],
        'console': ['console', 'serial', 'parallel', 'channel'],
        'hostdev': ['hostdev', 'smartcard', 'redirecteddev'],
        'special': [
            'watchdog',
            'memballoon',
            'rng',
            'tpm',
            'nvram',
            'panic',
            'vsock',
            'crypto',
            'pstore',
        ],
        'memory': ['shmem', 'memory'],
        'advanced': ['iommu'],
    }

    # 设备类型与 controller 的映射关系
    DEVICE_CONTROLLER_MAP: ClassVar[dict[str, dict[str, str]]] = {
        'disk': {
            'scsi': 'scsi',
            'sata': 'sata',
            'ide': 'ide',
        },
        'hostdev': {
            'scsi': 'scsi',
        },
    }

    def __init__(self, master, on_change_callback: Callable | None = None, **kwargs):
        # 在调用父类 __init__ 之前初始化属性 (因为 _init_ui 会被父类 __init__ 调用)
        self.devices_list: list[DeviceConfig] = []  # 已添加的设备列表
        self.controllers_list: list[dict] = []  # 已添加的控制器列表
        self.current_category = 'all'  # 当前选中的类别
        self.controller_counter: dict[str, int] = {}  # 各类 controller 计数器
        super().__init__(master, on_change_callback, **kwargs)

    def _init_ui(self) -> None:
        """初始化界面 - 上下布局：上部设备选择（固定一行），下部已添加设备列表（滚动）."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # 上部：设备选择（固定一行）
        self.grid_rowconfigure(1, weight=1)  # 下部：设备列表（滚动）

        # ===== 上部：设备选择（固定一行）=====
        top_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        top_frame.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
        top_frame.grid_columnconfigure(1, weight=1)

        # Category 标签
        ctk.CTkLabel(top_frame, text='Category:', font=CTK_FONT_SMALL, width=70).grid(
            row=0, column=0, padx=5, pady=5, sticky='w'
        )

        # Category 下拉框
        self.category_menu = ctk.CTkOptionMenu(
            top_frame,
            values=list(self.DEVICE_CATEGORIES.values()),
            width=180,
            font=CTK_FONT_SMALL,
            command=self._on_category_change,
        )
        self.category_menu.set('All Devices (所有设备)')
        self.category_menu.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        # Device Type 标签
        ctk.CTkLabel(top_frame, text='Device:', font=CTK_FONT_SMALL, width=50).grid(
            row=0, column=2, padx=10, pady=5, sticky='w'
        )

        # Device Type 下拉框
        self.device_type_menu = ctk.CTkOptionMenu(
            top_frame,
            values=['None'],
            width=220,
            font=CTK_FONT_SMALL,
            command=self._on_device_type_select,
        )
        self.device_type_menu.set('None')
        self.device_type_menu.grid(row=0, column=3, padx=5, pady=5, sticky='w')

        # Add 按钮
        self.add_btn = ctk.CTkButton(
            top_frame,
            text='Add',
            width=80,
            height=30,
            font=CTK_FONT_SMALL,
            command=self._add_selected_device,
            fg_color='#4caf50',
            hover_color='#388e3c',
        )
        self.add_btn.grid(row=0, column=4, padx=10, pady=5, sticky='e')

        # ===== 下部：已添加设备列表（滚动）=====
        bottom_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        bottom_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
        bottom_frame.grid_columnconfigure(0, weight=1)
        bottom_frame.grid_rowconfigure(0, weight=1)

        # 设备列表标题栏
        list_header = ctk.CTkFrame(bottom_frame, fg_color='transparent')
        list_header.grid(row=0, column=0, sticky='ew', padx=5, pady=3)

        ctk.CTkLabel(
            list_header, text='Added Devices:', font=CTK_FONT_BOLD, text_color='#4caf50'
        ).pack(side='left', padx=5)

        self.device_count_label = ctk.CTkLabel(
            list_header, text='(0 devices)', font=CTK_FONT_SMALL, text_color='#888888'
        )
        self.device_count_label.pack(side='left', padx=5)

        clear_btn = ctk.CTkButton(
            list_header,
            text='Clear All',
            width=80,
            height=26,
            font=CTK_FONT_SMALL,
            command=self._clear_all_devices,
            fg_color='#f44336',
            hover_color='#d32f2f',
        )
        clear_btn.pack(side='right', padx=5)

        # 设备列表滚动区域
        self.devices_scroll_frame = ctk.CTkScrollableFrame(
            bottom_frame, fg_color='transparent', corner_radius=4
        )
        self.devices_scroll_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=3)

        # 初始化设备类型选项
        self._update_device_type_options()

    def _on_category_change(self, selected_label: str) -> None:
        """类别改变时的处理。"""
        category_value: str | None = None
        for key, label in self.DEVICE_CATEGORIES.items():
            if label == selected_label:
                category_value = key
                break

        self.current_category = category_value or 'all'
        self._update_device_type_options()

    def _update_device_type_options(self) -> None:
        """更新设备类型选项。"""
        if self.current_category == 'all':
            device_types = ['None', *list(self.DEVICE_TYPES.values())]
        else:
            device_types_in_category = self.CATEGORY_DEVICES.get(self.current_category, [])
            device_types = [
                'None',
                *[
                    self.DEVICE_TYPES[dt]
                    for dt in device_types_in_category
                    if dt in self.DEVICE_TYPES
                ],
            ]

        self.device_type_menu.configure(values=device_types)
        self.device_type_menu.set('None')

    def _on_device_type_select(self, selected_label: str) -> None:
        """设备类型选择时的处理（仅更新 UI 状态）."""
        pass  # 不需要额外处理，点击 Add 按钮时才会添加

    def _add_selected_device(self) -> None:
        """添加选中的设备类型到列表。"""
        selected_label = self.device_type_menu.get()
        if selected_label == 'None':
            return

        # 找到对应的设备类型键
        device_type = None
        for key, label in self.DEVICE_TYPES.items():
            if label == selected_label:
                device_type = key
                break

        if not device_type:
            return

        # 创建设备配置
        config = self._get_default_config(device_type)
        device_label = self.DEVICE_TYPES.get(device_type, device_type)

        # 检查是否需要关联 controller
        controller_ref = None
        if device_type in self.DEVICE_CONTROLLER_MAP:
            bus_type = config.get('disk_bus', '') or config.get('hostdev_type', '')
            if bus_type in self.DEVICE_CONTROLLER_MAP[device_type]:
                controller_type = self.DEVICE_CONTROLLER_MAP[device_type][bus_type]
                controller_ref = self._get_or_create_controller(controller_type)

        device_info = DeviceConfig(
            device_type=device_type,
            device_label=device_label,
            config=config,
            controller_ref=controller_ref,
        )

        self.devices_list.append(device_info)
        self._update_devices_list_display()
        self._trigger_change()

        # 重置选择
        self.device_type_menu.set('None')

    def _get_default_config(self, device_type: str) -> dict[str, Any]:
        """获取设备类型的默认配置。"""
        defaults: dict[str, dict[str, Any]] = {
            'disk': {
                'disk_type': 'file',
                'disk_device': 'disk',
                'disk_bus': 'virtio',
                'disk_driver': 'qcow2',
                'disk_target': 'vda',
                'disk_source': '',
                'disk_readonly': False,
                'disk_boot_order': '',
                'disk_startup': 'none',
            },
            'graphics': {
                'gfx_type': 'vnc',
                'gfx_autoport': True,
                'gfx_port': '-1',
                'gfx_listen': '0.0.0.0',
                'gfx_keymap': 'en-us',
                'gfx_tls_port': '-1',
                'gfx_passwd': '',
                'gfx_share': 'allow-exclusive',
                'gfx_power': False,
                'gfx_wait': False,
            },
            'video': {
                'video_model': 'qxl',
                'video_vram': '16384',
                'video_heads': '1',
                'video_accel3d': False,
            },
            'sound': {
                'sound_model': 'ich9',
                'sound_codec': 'duplex',
            },
            'controller': {
                'ctrl_type': 'usb',
                'ctrl_model': 'usb-xhci',
                'ctrl_index': '0',
                'ctrl_queues': '',
            },
            'interface': {
                'iface_type': 'network',
                'iface_source': 'default',
                'iface_model': 'virtio',
                'iface_mac': '',
                'iface_boot': '',
            },
            'input': {
                'input_type': 'tablet',
                'input_bus': 'usb',
            },
            'hostdev': {
                'hostdev_type': 'usb',
                'hostdev_usb': '',
                'hostdev_policy': 'optional',
                'hostdev_pci': '',
                'hostdev_managed': 'yes',
                'hostdev_mdev': '',
            },
            'watchdog': {
                'watchdog_model': 'i6300esb',
                'watchdog_action': 'reset',
            },
            'memballoon': {
                'memballoon_model': 'virtio',
                'memballoon_period': '',
            },
            'rng': {
                'rng_model': 'virtio',
                'rng_backend': 'random',
                'rng_source': '/dev/urandom',
                'rng_rate': '',
            },
            'tpm': {
                'tpm_model': 'tpm-tis',
                'tpm_backend': 'emulator',
                'tpm_device': '/dev/tpm0',
                'tpm_version': '2.0',
            },
            'filesystem': {
                'fs_type': 'mount',
                'fs_access': 'passthrough',
                'fs_source': '',
                'fs_target': '',
                'fs_readonly': False,
            },
            'console': {
                'console_type': 'pty',
                'console_target': 'virtio',
            },
            'serial': {
                'serial_type': 'pty',
                'serial_port': '0',
                'serial_path': '',
            },
            'parallel': {
                'parallel_type': 'pty',
                'parallel_port': '0',
                'parallel_path': '',
            },
            'channel': {
                'channel_type': 'unix',
                'channel_name': 'org.qemu.guest_agent.0',
                'channel_path': '',
            },
            'iommu': {
                'iommu_model': 'intel',
                'iommu_intremap': False,
                'iommu_caching': False,
                'iommu_aw': '',
            },
            'memory': {
                'memory_model': 'dimm',
                'memory_size': '524288',
                'memory_node': '0',
                'memory_access': 'private',
            },
            'shmem': {
                'shmem_name': 'shmem0',
                'shmem_model': 'ivshmem-plain',
                'shmem_size': '4',
                'shmem_role': 'peer',
            },
        }
        return defaults.get(device_type, {})

    def _update_devices_list_display(self) -> None:
        """更新设备列表显示。"""
        # 清空列表
        for widget in self.devices_scroll_frame.winfo_children():
            widget.destroy()

        if not self.devices_list:
            label = ctk.CTkLabel(
                self.devices_scroll_frame,
                text='No devices added yet. Select a device type above and click "Add".',
                font=CTK_FONT_SMALL,
                text_color='#888888',
            )
            label.pack(padx=5, pady=20)
            self.device_count_label.configure(text='(0 devices)')
            return

        self.device_count_label.configure(text=f'({len(self.devices_list)} devices)')

        # 显示设备列表
        for i, device in enumerate(self.devices_list):
            self._create_device_row(device, i)

    def _create_device_row(self, device: DeviceConfig, index: int) -> None:
        """创建设备配置行。"""
        device_frame = ctk.CTkFrame(self.devices_scroll_frame, fg_color='#3a3a3a', corner_radius=4)
        device_frame.pack(fill='x', padx=5, pady=2)
        device_frame.grid_columnconfigure(0, weight=1)

        # 根据设备类型创建配置行
        row_frame = ctk.CTkFrame(device_frame, fg_color='transparent')
        row_frame.grid(row=0, column=0, sticky='ew', padx=5, pady=3)

        # 设备类型标签
        type_label = ctk.CTkLabel(
            row_frame,
            text=f'[{device.device_type}]',
            font=CTK_FONT_SMALL,
            text_color='#4caf50',
            width=100,
            anchor='w',
        )
        type_label.pack(side='left', padx=3)

        # 根据设备类型创建配置 widget
        self._create_device_config_widgets(row_frame, device, index)

        # 删除按钮
        del_btn = ctk.CTkButton(
            row_frame,
            text='X',
            width=30,
            height=24,
            font=CTK_FONT_SMALL,
            fg_color='#f44336',
            hover_color='#d32f2f',
            command=lambda idx=index: self._delete_device(idx),
        )
        del_btn.pack(side='right', padx=3)

    def _create_device_config_widgets(self, parent, device: DeviceConfig, index: int) -> list:
        """创建设备配置 widget。"""
        widgets = []

        if device.device_type == 'disk':
            widgets = self._create_disk_widgets(parent, device, index)
        elif device.device_type == 'graphics':
            widgets = self._create_graphics_widgets(parent, device, index)
        elif device.device_type == 'video':
            widgets = self._create_video_widgets(parent, device, index)
        elif device.device_type == 'sound':
            widgets = self._create_sound_widgets(parent, device, index)
        elif device.device_type == 'controller':
            widgets = self._create_controller_widgets(parent, device, index)
        elif device.device_type == 'interface':
            widgets = self._create_interface_widgets(parent, device, index)
        elif device.device_type == 'input':
            widgets = self._create_input_widgets(parent, device, index)
        elif device.device_type == 'hostdev':
            widgets = self._create_hostdev_widgets(parent, device, index)
        elif device.device_type == 'watchdog':
            widgets = self._create_watchdog_widgets(parent, device, index)
        elif device.device_type == 'memballoon':
            widgets = self._create_memballoon_widgets(parent, device, index)
        elif device.device_type == 'rng':
            widgets = self._create_rng_widgets(parent, device, index)
        elif device.device_type == 'tpm':
            widgets = self._create_tpm_widgets(parent, device, index)
        elif device.device_type == 'filesystem':
            widgets = self._create_filesystem_widgets(parent, device, index)
        elif device.device_type == 'console':
            widgets = self._create_console_widgets(parent, device, index)
        elif device.device_type == 'serial':
            widgets = self._create_serial_widgets(parent, device, index)
        elif device.device_type == 'parallel':
            widgets = self._create_parallel_widgets(parent, device, index)
        elif device.device_type == 'channel':
            widgets = self._create_channel_widgets(parent, device, index)
        elif device.device_type == 'iommu':
            widgets = self._create_iommu_widgets(parent, device, index)
        elif device.device_type == 'memory':
            widgets = self._create_memory_widgets(parent, device, index)
        elif device.device_type == 'shmem':
            widgets = self._create_shmem_widgets(parent, device, index)

        return widgets

    # ========== 设备配置 Widget 创建方法 ==========
    def _create_disk_widgets(self, parent, device: DeviceConfig, index: int) -> list:
        """磁盘设备 widget。"""
        widgets = []
        config = device.config

        # Type
        type_menu = ctk.CTkOptionMenu(
            parent,
            values=['file', 'block', 'network', 'volume', 'dir', 'nvme', 'vhostuser'],
            width=80,
            font=CTK_FONT_SMALL,
            command=lambda v, idx=index: self._on_config_change(idx, 'disk_type', v),
        )
        type_menu.set(config.get('disk_type', 'file'))
        type_menu.pack(side='left', padx=2)
        widgets.append(('disk_type', type_menu))

        # Device
        dev_menu = ctk.CTkOptionMenu(
            parent,
            values=['disk', 'cdrom', 'lun', 'floppy'],
            width=70,
            font=CTK_FONT_SMALL,
            command=lambda v, idx=index: self._on_config_change(idx, 'disk_device', v),
        )
        dev_menu.set(config.get('disk_device', 'disk'))
        dev_menu.pack(side='left', padx=2)
        widgets.append(('disk_device', dev_menu))

        # Bus
        bus_menu = ctk.CTkOptionMenu(
            parent,
            values=['virtio', 'sata', 'ide', 'scsi', 'usb', 'nvme'],
            width=70,
            font=CTK_FONT_SMALL,
            command=lambda v, idx=index: self._on_bus_change(idx, v),
        )
        bus_menu.set(config.get('disk_bus', 'virtio'))
        bus_menu.pack(side='left', padx=2)
        widgets.append(('disk_bus', bus_menu))

        # Driver
        drv_menu = ctk.CTkOptionMenu(
            parent,
            values=['qcow2', 'raw', 'vmdk', 'vdi', 'none'],
            width=70,
            font=CTK_FONT_SMALL,
            command=lambda v, idx=index: self._on_config_change(idx, 'disk_driver', v),
        )
        drv_menu.set(config.get('disk_driver', 'qcow2'))
        drv_menu.pack(side='left', padx=2)
        widgets.append(('disk_driver', drv_menu))

        # Target
        target_entry = ctk.CTkEntry(parent, width=60, font=CTK_FONT_SMALL)
        target_entry.insert(0, config.get('disk_target', 'vda'))
        target_entry.bind(
            '<KeyRelease>',
            lambda e, idx=index: self._on_entry_change(idx, 'disk_target', target_entry.get()),
        )
        target_entry.pack(side='left', padx=2)
        widgets.append(('disk_target', target_entry))

        # Source
        source_entry = ctk.CTkEntry(
            parent, width=200, font=CTK_FONT_SMALL, placeholder_text='Source path'
        )
        source_entry.insert(0, config.get('disk_source', ''))
        source_entry.bind(
            '<KeyRelease>',
            lambda e, idx=index: self._on_entry_change(idx, 'disk_source', source_entry.get()),
        )
        source_entry.pack(side='left', padx=2)
        widgets.append(('disk_source', source_entry))

        # Readonly
        ro_check: ctk.CTkCheckBox = ctk.CTkCheckBox(
            parent,
            text='RO',
            width=30,
            font=CTK_FONT_SMALL,
            command=lambda idx=index: self._on_checkbox_change(
                idx, 'disk_readonly', ro_check.get()
            ),
        )
        if config.get('disk_readonly', False):
            ro_check.select()
        ro_check.pack(side='left', padx=2)
        widgets.append(('disk_readonly', ro_check))

        return widgets

    def _create_graphics_widgets(self, parent, device: DeviceConfig, index: int) -> list:
        """图形显示 widget。"""
        widgets = []
        config = device.config

        # Type
        type_menu = ctk.CTkOptionMenu(
            parent,
            values=['vnc', 'spice', 'rdp', 'sdl', 'desktop', 'egl-headless', 'dbus'],
            width=90,
            font=CTK_FONT_SMALL,
            command=lambda v, idx=index: self._on_config_change(idx, 'gfx_type', v),
        )
        type_menu.set(config.get('gfx_type', 'vnc'))
        type_menu.pack(side='left', padx=2)
        widgets.append(('gfx_type', type_menu))

        # Autoport
        ap_check: ctk.CTkCheckBox = ctk.CTkCheckBox(
            parent,
            text='Autoport',
            width=70,
            font=CTK_FONT_SMALL,
            command=lambda idx=index: self._on_checkbox_change(idx, 'gfx_autoport', ap_check.get()),
        )
        if config.get('gfx_autoport', True):
            ap_check.select()
        ap_check.pack(side='left', padx=2)
        widgets.append(('gfx_autoport', ap_check))

        # Port
        port_entry = ctk.CTkEntry(parent, width=45, font=CTK_FONT_SMALL)
        port_entry.insert(0, str(config.get('gfx_port', '-1')))
        port_entry.bind(
            '<KeyRelease>',
            lambda e, idx=index: self._on_entry_change(idx, 'gfx_port', port_entry.get()),
        )
        port_entry.pack(side='left', padx=2)
        widgets.append(('gfx_port', port_entry))

        # Listen
        listen_entry = ctk.CTkEntry(parent, width=90, font=CTK_FONT_SMALL)
        listen_entry.insert(0, config.get('gfx_listen', '0.0.0.0'))
        listen_entry.bind(
            '<KeyRelease>',
            lambda e, idx=index: self._on_entry_change(idx, 'gfx_listen', listen_entry.get()),
        )
        listen_entry.pack(side='left', padx=2)
        widgets.append(('gfx_listen', listen_entry))

        # Keymap
        keymap_entry = ctk.CTkEntry(parent, width=70, font=CTK_FONT_SMALL)
        keymap_entry.insert(0, config.get('gfx_keymap', 'en-us'))
        keymap_entry.bind(
            '<KeyRelease>',
            lambda e, idx=index: self._on_entry_change(idx, 'gfx_keymap', keymap_entry.get()),
        )
        keymap_entry.pack(side='left', padx=2)
        widgets.append(('gfx_keymap', keymap_entry))

        return widgets

    def _create_video_widgets(self, parent, device: DeviceConfig, index: int) -> list:
        """视频设备 widget。"""
        widgets = []
        config = device.config

        # Model
        model_menu = ctk.CTkOptionMenu(
            parent,
            values=['vga', 'cirrus', 'vmvga', 'qxl', 'virtio', 'gop', 'bochs', 'ramfb'],
            width=80,
            font=CTK_FONT_SMALL,
            command=lambda v, idx=index: self._on_config_change(idx, 'video_model', v),
        )
        model_menu.set(config.get('video_model', 'qxl'))
        model_menu.pack(side='left', padx=2)
        widgets.append(('video_model', model_menu))

        # VRAM
        vram_entry = ctk.CTkEntry(parent, width=60, font=CTK_FONT_SMALL)
        vram_entry.insert(0, str(config.get('video_vram', '16384')))
        vram_entry.bind(
            '<KeyRelease>',
            lambda e, idx=index: self._on_entry_change(idx, 'video_vram', vram_entry.get()),
        )
        vram_entry.pack(side='left', padx=2)
        widgets.append(('video_vram', vram_entry))

        # Heads
        heads_entry = ctk.CTkEntry(parent, width=40, font=CTK_FONT_SMALL)
        heads_entry.insert(0, str(config.get('video_heads', '1')))
        heads_entry.bind(
            '<KeyRelease>',
            lambda e, idx=index: self._on_entry_change(idx, 'video_heads', heads_entry.get()),
        )
        heads_entry.pack(side='left', padx=2)
        widgets.append(('video_heads', heads_entry))

        # 3D Acceleration
        accel_check: ctk.CTkCheckBox = ctk.CTkCheckBox(
            parent,
            text='3D',
            width=35,
            font=CTK_FONT_SMALL,
            command=lambda idx=index: self._on_checkbox_change(
                idx, 'video_accel3d', accel_check.get()
            ),
        )
        if config.get('video_accel3d', False):
            accel_check.select()
        accel_check.pack(side='left', padx=2)
        widgets.append(('video_accel3d', accel_check))

        return widgets

    def _create_sound_widgets(self, parent, device: DeviceConfig, index: int) -> list:
        """音频设备 widget。"""
        widgets = []
        config = device.config

        # Model
        model_menu = ctk.CTkOptionMenu(
            parent,
            values=['sb16', 'es1370', 'ac97', 'ich6', 'ich9', 'usb', 'virtio'],
            width=80,
            font=CTK_FONT_SMALL,
            command=lambda v, idx=index: self._on_config_change(idx, 'sound_model', v),
        )
        model_menu.set(config.get('sound_model', 'ich9'))
        model_menu.pack(side='left', padx=2)
        widgets.append(('sound_model', model_menu))

        # Codec
        codec_menu = ctk.CTkOptionMenu(
            parent,
            values=['duplex', 'micro', 'output', 'none'],
            width=80,
            font=CTK_FONT_SMALL,
            command=lambda v, idx=index: self._on_config_change(idx, 'sound_codec', v),
        )
        codec_menu.set(config.get('sound_codec', 'duplex'))
        codec_menu.pack(side='left', padx=2)
        widgets.append(('sound_codec', codec_menu))

        return widgets

    def _create_controller_widgets(self, parent, device: DeviceConfig, index: int) -> list:
        """控制器 widget。"""
        widgets = []
        config = device.config

        # Type
        type_menu = ctk.CTkOptionMenu(
            parent,
            values=['ide', 'fdc', 'scsi', 'sata', 'usb', 'virtio-serial', 'pci'],
            width=90,
            font=CTK_FONT_SMALL,
            command=lambda v, idx=index: self._on_config_change(idx, 'ctrl_type', v),
        )
        type_menu.set(config.get('ctrl_type', 'usb'))
        type_menu.pack(side='left', padx=2)
        widgets.append(('ctrl_type', type_menu))

        # Model
        model_menu = ctk.CTkOptionMenu(
            parent,
            values=[
                'auto',
                'virtio-scsi',
                'pci-root',
                'pci-bridge',
                'pcie-root',
                'usb-xhci',
                'usb-ehci',
                'uhci',
            ],
            width=100,
            font=CTK_FONT_SMALL,
            command=lambda v, idx=index: self._on_config_change(idx, 'ctrl_model', v),
        )
        model_menu.set(config.get('ctrl_model', 'usb-xhci'))
        model_menu.pack(side='left', padx=2)
        widgets.append(('ctrl_model', model_menu))

        # Index
        index_entry = ctk.CTkEntry(parent, width=40, font=CTK_FONT_SMALL)
        index_entry.insert(0, str(config.get('ctrl_index', '0')))
        index_entry.bind(
            '<KeyRelease>',
            lambda e, idx=index: self._on_entry_change(idx, 'ctrl_index', index_entry.get()),
        )
        index_entry.pack(side='left', padx=2)
        widgets.append(('ctrl_index', index_entry))

        return widgets

    def _create_interface_widgets(self, parent, device: DeviceConfig, index: int) -> list:
        """网络接口 widget。"""
        widgets = []
        config = device.config

        # Type
        type_menu = ctk.CTkOptionMenu(
            parent,
            values=['network', 'bridge', 'direct', 'user', 'vhostuser', 'vdpa'],
            width=80,
            font=CTK_FONT_SMALL,
            command=lambda v, idx=index: self._on_config_change(idx, 'iface_type', v),
        )
        type_menu.set(config.get('iface_type', 'network'))
        type_menu.pack(side='left', padx=2)
        widgets.append(('iface_type', type_menu))

        # Source
        source_entry = ctk.CTkEntry(parent, width=100, font=CTK_FONT_SMALL)
        source_entry.insert(0, config.get('iface_source', 'default'))
        source_entry.bind(
            '<KeyRelease>',
            lambda e, idx=index: self._on_entry_change(idx, 'iface_source', source_entry.get()),
        )
        source_entry.pack(side='left', padx=2)
        widgets.append(('iface_source', source_entry))

        # Model
        model_menu = ctk.CTkOptionMenu(
            parent,
            values=['virtio', 'e1000', 'e1000e', 'rtl8139', 'vmxnet3'],
            width=70,
            font=CTK_FONT_SMALL,
            command=lambda v, idx=index: self._on_config_change(idx, 'iface_model', v),
        )
        model_menu.set(config.get('iface_model', 'virtio'))
        model_menu.pack(side='left', padx=2)
        widgets.append(('iface_model', model_menu))

        # MAC
        mac_entry = ctk.CTkEntry(
            parent, width=120, font=CTK_FONT_SMALL, placeholder_text='MAC address'
        )
        mac_entry.insert(0, config.get('iface_mac', ''))
        mac_entry.bind(
            '<KeyRelease>',
            lambda e, idx=index: self._on_entry_change(idx, 'iface_mac', mac_entry.get()),
        )
        mac_entry.pack(side='left', padx=2)
        widgets.append(('iface_mac', mac_entry))

        return widgets

    def _create_input_widgets(self, parent, device: DeviceConfig, index: int) -> list:
        """输入设备 widget。"""
        widgets = []
        config = device.config

        # Type
        type_menu = ctk.CTkOptionMenu(
            parent,
            values=['mouse', 'tablet', 'keyboard'],
            width=80,
            font=CTK_FONT_SMALL,
            command=lambda v, idx=index: self._on_config_change(idx, 'input_type', v),
        )
        type_menu.set(config.get('input_type', 'tablet'))
        type_menu.pack(side='left', padx=2)
        widgets.append(('input_type', type_menu))

        # Bus
        bus_menu = ctk.CTkOptionMenu(
            parent,
            values=['usb', 'virtio', 'ps2'],
            width=70,
            font=CTK_FONT_SMALL,
            command=lambda v, idx=index: self._on_config_change(idx, 'input_bus', v),
        )
        bus_menu.set(config.get('input_bus', 'usb'))
        bus_menu.pack(side='left', padx=2)
        widgets.append(('input_bus', bus_menu))

        return widgets

    def _create_hostdev_widgets(self, parent, device: DeviceConfig, index: int) -> list:
        """主机设备 widget。"""
        widgets = []
        config = device.config

        # Type
        type_menu = ctk.CTkOptionMenu(
            parent,
            values=['usb', 'pci', 'scsi', 'mdev'],
            width=70,
            font=CTK_FONT_SMALL,
            command=lambda v, idx=index: self._on_config_change(idx, 'hostdev_type', v),
        )
        type_menu.set(config.get('hostdev_type', 'usb'))
        type_menu.pack(side='left', padx=2)
        widgets.append(('hostdev_type', type_menu))

        # USB
        usb_entry = ctk.CTkEntry(
            parent, width=130, font=CTK_FONT_SMALL, placeholder_text='Vendor:Product'
        )
        usb_entry.insert(0, config.get('hostdev_usb', ''))
        usb_entry.bind(
            '<KeyRelease>',
            lambda e, idx=index: self._on_entry_change(idx, 'hostdev_usb', usb_entry.get()),
        )
        usb_entry.pack(side='left', padx=2)
        widgets.append(('hostdev_usb', usb_entry))

        # Policy
        policy_menu = ctk.CTkOptionMenu(
            parent,
            values=['mandatory', 'requisite', 'optional'],
            width=90,
            font=CTK_FONT_SMALL,
            command=lambda v, idx=index: self._on_config_change(idx, 'hostdev_policy', v),
        )
        policy_menu.set(config.get('hostdev_policy', 'optional'))
        policy_menu.pack(side='left', padx=2)
        widgets.append(('hostdev_policy', policy_menu))

        return widgets

    def _create_watchdog_widgets(self, parent, device: DeviceConfig, index: int) -> list:
        """看门狗 widget。"""
        widgets = []
        config = device.config

        # Model
        model_menu = ctk.CTkOptionMenu(
            parent,
            values=['i6300esb', 'ib700', 'itco', 'diag288'],
            width=90,
            font=CTK_FONT_SMALL,
            command=lambda v, idx=index: self._on_config_change(idx, 'watchdog_model', v),
        )
        model_menu.set(config.get('watchdog_model', 'i6300esb'))
        model_menu.pack(side='left', padx=2)
        widgets.append(('watchdog_model', model_menu))

        # Action
        action_menu = ctk.CTkOptionMenu(
            parent,
            values=['reset', 'shutdown', 'poweroff', 'pause', 'none', 'dump', 'inject-nmi'],
            width=100,
            font=CTK_FONT_SMALL,
            command=lambda v, idx=index: self._on_config_change(idx, 'watchdog_action', v),
        )
        action_menu.set(config.get('watchdog_action', 'reset'))
        action_menu.pack(side='left', padx=2)
        widgets.append(('watchdog_action', action_menu))

        return widgets

    def _create_memballoon_widgets(self, parent, device: DeviceConfig, index: int) -> list:
        """内存气球 widget。"""
        widgets = []
        config = device.config

        # Model
        model_menu = ctk.CTkOptionMenu(
            parent,
            values=['virtio', 'xen', 'none'],
            width=70,
            font=CTK_FONT_SMALL,
            command=lambda v, idx=index: self._on_config_change(idx, 'memballoon_model', v),
        )
        model_menu.set(config.get('memballoon_model', 'virtio'))
        model_menu.pack(side='left', padx=2)
        widgets.append(('memballoon_model', model_menu))

        # Period
        period_entry = ctk.CTkEntry(
            parent, width=70, font=CTK_FONT_SMALL, placeholder_text='Period(s)'
        )
        period_entry.insert(0, str(config.get('memballoon_period', '')))
        period_entry.bind(
            '<KeyRelease>',
            lambda e, idx=index: self._on_entry_change(
                idx, 'memballoon_period', period_entry.get()
            ),
        )
        period_entry.pack(side='left', padx=2)
        widgets.append(('memballoon_period', period_entry))

        return widgets

    def _create_rng_widgets(self, parent, device: DeviceConfig, index: int) -> list:
        """随机数发生器 widget。"""
        widgets = []
        config = device.config

        # Model
        model_menu = ctk.CTkOptionMenu(
            parent,
            values=['virtio', 'virtio-transitional', 'virtio-non-transitional'],
            width=130,
            font=CTK_FONT_SMALL,
            command=lambda v, idx=index: self._on_config_change(idx, 'rng_model', v),
        )
        model_menu.set(config.get('rng_model', 'virtio'))
        model_menu.pack(side='left', padx=2)
        widgets.append(('rng_model', model_menu))

        # Backend
        backend_menu = ctk.CTkOptionMenu(
            parent,
            values=['random', 'egd', 'builtin'],
            width=80,
            font=CTK_FONT_SMALL,
            command=lambda v, idx=index: self._on_config_change(idx, 'rng_backend', v),
        )
        backend_menu.set(config.get('rng_backend', 'random'))
        backend_menu.pack(side='left', padx=2)
        widgets.append(('rng_backend', backend_menu))

        # Source
        source_entry = ctk.CTkEntry(
            parent, width=150, font=CTK_FONT_SMALL, placeholder_text='Source'
        )
        source_entry.insert(0, config.get('rng_source', '/dev/urandom'))
        source_entry.bind(
            '<KeyRelease>',
            lambda e, idx=index: self._on_entry_change(idx, 'rng_source', source_entry.get()),
        )
        source_entry.pack(side='left', padx=2)
        widgets.append(('rng_source', source_entry))

        return widgets

    def _create_tpm_widgets(self, parent, device: DeviceConfig, index: int) -> list:
        """TPM 设备 widget。"""
        widgets = []
        config = device.config

        # Model
        model_menu = ctk.CTkOptionMenu(
            parent,
            values=['tpm-tis', 'tpm-crb', 'tpm-spapr', 'spapr-tpm-proxy'],
            width=80,
            font=CTK_FONT_SMALL,
            command=lambda v, idx=index: self._on_config_change(idx, 'tpm_model', v),
        )
        model_menu.set(config.get('tpm_model', 'tpm-tis'))
        model_menu.pack(side='left', padx=2)
        widgets.append(('tpm_model', model_menu))

        # Backend
        backend_menu = ctk.CTkOptionMenu(
            parent,
            values=['passthrough', 'emulator', 'external'],
            width=90,
            font=CTK_FONT_SMALL,
            command=lambda v, idx=index: self._on_config_change(idx, 'tpm_backend', v),
        )
        backend_menu.set(config.get('tpm_backend', 'emulator'))
        backend_menu.pack(side='left', padx=2)
        widgets.append(('tpm_backend', backend_menu))

        # Device
        device_entry = ctk.CTkEntry(parent, width=120, font=CTK_FONT_SMALL)
        device_entry.insert(0, config.get('tpm_device', '/dev/tpm0'))
        device_entry.bind(
            '<KeyRelease>',
            lambda e, idx=index: self._on_entry_change(idx, 'tpm_device', device_entry.get()),
        )
        device_entry.pack(side='left', padx=2)
        widgets.append(('tpm_device', device_entry))

        return widgets

    def _create_filesystem_widgets(self, parent, device: DeviceConfig, index: int) -> list:
        """文件系统 widget。"""
        widgets = []
        config = device.config

        # Type
        type_menu = ctk.CTkOptionMenu(
            parent,
            values=['mount', 'template', 'file', 'block', 'ram', 'bind'],
            width=70,
            font=CTK_FONT_SMALL,
            command=lambda v, idx=index: self._on_config_change(idx, 'fs_type', v),
        )
        type_menu.set(config.get('fs_type', 'mount'))
        type_menu.pack(side='left', padx=2)
        widgets.append(('fs_type', type_menu))

        # Access
        access_menu = ctk.CTkOptionMenu(
            parent,
            values=['passthrough', 'mapped', 'squash'],
            width=90,
            font=CTK_FONT_SMALL,
            command=lambda v, idx=index: self._on_config_change(idx, 'fs_access', v),
        )
        access_menu.set(config.get('fs_access', 'passthrough'))
        access_menu.pack(side='left', padx=2)
        widgets.append(('fs_access', access_menu))

        # Source
        source_entry = ctk.CTkEntry(
            parent, width=150, font=CTK_FONT_SMALL, placeholder_text='Source path'
        )
        source_entry.insert(0, config.get('fs_source', ''))
        source_entry.bind(
            '<KeyRelease>',
            lambda e, idx=index: self._on_entry_change(idx, 'fs_source', source_entry.get()),
        )
        source_entry.pack(side='left', padx=2)
        widgets.append(('fs_source', source_entry))

        # Target
        target_entry = ctk.CTkEntry(
            parent, width=150, font=CTK_FONT_SMALL, placeholder_text='Target path'
        )
        target_entry.insert(0, config.get('fs_target', ''))
        target_entry.bind(
            '<KeyRelease>',
            lambda e, idx=index: self._on_entry_change(idx, 'fs_target', target_entry.get()),
        )
        target_entry.pack(side='left', padx=2)
        widgets.append(('fs_target', target_entry))

        return widgets

    def _create_console_widgets(self, parent, device: DeviceConfig, index: int) -> list:
        """控制台 widget。"""
        widgets = []
        config = device.config

        # Type
        type_menu = ctk.CTkOptionMenu(
            parent,
            values=['pty', 'vc', 'stdio', 'null', 'tty', 'udp', 'unix', 'spicevmc', 'qemu-vdagent'],
            width=110,
            font=CTK_FONT_SMALL,
            command=lambda v, idx=index: self._on_config_change(idx, 'console_type', v),
        )
        type_menu.set(config.get('console_type', 'pty'))
        type_menu.pack(side='left', padx=2)
        widgets.append(('console_type', type_menu))

        # Target
        target_menu = ctk.CTkOptionMenu(
            parent,
            values=['serial', 'virtio', 'xen'],
            width=80,
            font=CTK_FONT_SMALL,
            command=lambda v, idx=index: self._on_config_change(idx, 'console_target', v),
        )
        target_menu.set(config.get('console_target', 'virtio'))
        target_menu.pack(side='left', padx=2)
        widgets.append(('console_target', target_menu))

        return widgets

    def _create_serial_widgets(self, parent, device: DeviceConfig, index: int) -> list:
        """串口 widget。"""
        widgets = []
        config = device.config

        # Type
        type_menu = ctk.CTkOptionMenu(
            parent,
            values=['pty', 'file', 'dev', 'null', 'udp', 'tcp', 'unix', 'spiceport'],
            width=70,
            font=CTK_FONT_SMALL,
            command=lambda v, idx=index: self._on_config_change(idx, 'serial_type', v),
        )
        type_menu.set(config.get('serial_type', 'pty'))
        type_menu.pack(side='left', padx=2)
        widgets.append(('serial_type', type_menu))

        # Port
        port_entry = ctk.CTkEntry(parent, width=45, font=CTK_FONT_SMALL)
        port_entry.insert(0, str(config.get('serial_port', '0')))
        port_entry.bind(
            '<KeyRelease>',
            lambda e, idx=index: self._on_entry_change(idx, 'serial_port', port_entry.get()),
        )
        port_entry.pack(side='left', padx=2)
        widgets.append(('serial_port', port_entry))

        # Path
        path_entry = ctk.CTkEntry(parent, width=150, font=CTK_FONT_SMALL, placeholder_text='Path')
        path_entry.insert(0, config.get('serial_path', ''))
        path_entry.bind(
            '<KeyRelease>',
            lambda e, idx=index: self._on_entry_change(idx, 'serial_path', path_entry.get()),
        )
        path_entry.pack(side='left', padx=2)
        widgets.append(('serial_path', path_entry))

        return widgets

    def _create_parallel_widgets(self, parent, device: DeviceConfig, index: int) -> list:
        """并口 widget。"""
        widgets = []
        config = device.config

        # Type
        type_menu = ctk.CTkOptionMenu(
            parent,
            values=['pty', 'dev', 'null'],
            width=70,
            font=CTK_FONT_SMALL,
            command=lambda v, idx=index: self._on_config_change(idx, 'parallel_type', v),
        )
        type_menu.set(config.get('parallel_type', 'pty'))
        type_menu.pack(side='left', padx=2)
        widgets.append(('parallel_type', type_menu))

        # Port
        port_entry = ctk.CTkEntry(parent, width=45, font=CTK_FONT_SMALL)
        port_entry.insert(0, str(config.get('parallel_port', '0')))
        port_entry.bind(
            '<KeyRelease>',
            lambda e, idx=index: self._on_entry_change(idx, 'parallel_port', port_entry.get()),
        )
        port_entry.pack(side='left', padx=2)
        widgets.append(('parallel_port', port_entry))

        # Path
        path_entry = ctk.CTkEntry(
            parent, width=150, font=CTK_FONT_SMALL, placeholder_text='/dev/parport0'
        )
        path_entry.insert(0, config.get('parallel_path', ''))
        path_entry.bind(
            '<KeyRelease>',
            lambda e, idx=index: self._on_entry_change(idx, 'parallel_path', path_entry.get()),
        )
        path_entry.pack(side='left', padx=2)
        widgets.append(('parallel_path', path_entry))

        return widgets

    def _create_channel_widgets(self, parent, device: DeviceConfig, index: int) -> list:
        """通道 widget。"""
        widgets = []
        config = device.config

        # Type
        type_menu = ctk.CTkOptionMenu(
            parent,
            values=['unix', 'pty', 'spicevmc', 'qemu-vdagent', 'virtio'],
            width=80,
            font=CTK_FONT_SMALL,
            command=lambda v, idx=index: self._on_config_change(idx, 'channel_type', v),
        )
        type_menu.set(config.get('channel_type', 'unix'))
        type_menu.pack(side='left', padx=2)
        widgets.append(('channel_type', type_menu))

        # Name
        name_entry = ctk.CTkEntry(parent, width=180, font=CTK_FONT_SMALL)
        name_entry.insert(0, config.get('channel_name', 'org.qemu.guest_agent.0'))
        name_entry.bind(
            '<KeyRelease>',
            lambda e, idx=index: self._on_entry_change(idx, 'channel_name', name_entry.get()),
        )
        name_entry.pack(side='left', padx=2)
        widgets.append(('channel_name', name_entry))

        return widgets

    def _create_iommu_widgets(self, parent, device: DeviceConfig, index: int) -> list:
        """IOMMU widget。"""
        widgets = []
        config = device.config

        # Model
        model_menu = ctk.CTkOptionMenu(
            parent,
            values=['intel', 'amd', 'virtio', 'smmuv3', 'none'],
            width=70,
            font=CTK_FONT_SMALL,
            command=lambda v, idx=index: self._on_config_change(idx, 'iommu_model', v),
        )
        model_menu.set(config.get('iommu_model', 'intel'))
        model_menu.pack(side='left', padx=2)
        widgets.append(('iommu_model', model_menu))

        # Intremap
        intremap_check: ctk.CTkCheckBox = ctk.CTkCheckBox(
            parent,
            text='Intremap',
            width=60,
            font=CTK_FONT_SMALL,
            command=lambda idx=index: self._on_checkbox_change(
                idx, 'iommu_intremap', intremap_check.get()
            ),
        )
        if config.get('iommu_intremap', False):
            intremap_check.select()
        intremap_check.pack(side='left', padx=2)
        widgets.append(('iommu_intremap', intremap_check))

        # Caching
        caching_check: ctk.CTkCheckBox = ctk.CTkCheckBox(
            parent,
            text='Caching',
            width=60,
            font=CTK_FONT_SMALL,
            command=lambda idx=index: self._on_checkbox_change(
                idx, 'iommu_caching', caching_check.get()
            ),
        )
        if config.get('iommu_caching', False):
            caching_check.select()
        caching_check.pack(side='left', padx=2)
        widgets.append(('iommu_caching', caching_check))

        return widgets

    def _create_memory_widgets(self, parent, device: DeviceConfig, index: int) -> list:
        """内存设备 widget。"""
        widgets = []
        config = device.config

        # Model
        model_menu = ctk.CTkOptionMenu(
            parent,
            values=['dimm', 'nvdimm', 'virtio-pmem', 'virtio-mem', 'sgx-epc'],
            width=90,
            font=CTK_FONT_SMALL,
            command=lambda v, idx=index: self._on_config_change(idx, 'memory_model', v),
        )
        model_menu.set(config.get('memory_model', 'dimm'))
        model_menu.pack(side='left', padx=2)
        widgets.append(('memory_model', model_menu))

        # Size
        size_entry = ctk.CTkEntry(parent, width=90, font=CTK_FONT_SMALL)
        size_entry.insert(0, str(config.get('memory_size', '524288')))
        size_entry.bind(
            '<KeyRelease>',
            lambda e, idx=index: self._on_entry_change(idx, 'memory_size', size_entry.get()),
        )
        size_entry.pack(side='left', padx=2)
        widgets.append(('memory_size', size_entry))

        # Node
        node_entry = ctk.CTkEntry(parent, width=50, font=CTK_FONT_SMALL)
        node_entry.insert(0, str(config.get('memory_node', '0')))
        node_entry.bind(
            '<KeyRelease>',
            lambda e, idx=index: self._on_entry_change(idx, 'memory_node', node_entry.get()),
        )
        node_entry.pack(side='left', padx=2)
        widgets.append(('memory_node', node_entry))

        return widgets

    def _create_shmem_widgets(self, parent, device: DeviceConfig, index: int) -> list:
        """共享内存 widget。"""
        widgets = []
        config = device.config

        # Name
        name_entry = ctk.CTkEntry(parent, width=80, font=CTK_FONT_SMALL)
        name_entry.insert(0, config.get('shmem_name', 'shmem0'))
        name_entry.bind(
            '<KeyRelease>',
            lambda e, idx=index: self._on_entry_change(idx, 'shmem_name', name_entry.get()),
        )
        name_entry.pack(side='left', padx=2)
        widgets.append(('shmem_name', name_entry))

        # Model
        model_menu = ctk.CTkOptionMenu(
            parent,
            values=['ivshmem-plain', 'ivshmem-doorbell'],
            width=120,
            font=CTK_FONT_SMALL,
            command=lambda v, idx=index: self._on_config_change(idx, 'shmem_model', v),
        )
        model_menu.set(config.get('shmem_model', 'ivshmem-plain'))
        model_menu.pack(side='left', padx=2)
        widgets.append(('shmem_model', model_menu))

        # Size
        size_entry = ctk.CTkEntry(parent, width=50, font=CTK_FONT_SMALL)
        size_entry.insert(0, str(config.get('shmem_size', '4')))
        size_entry.bind(
            '<KeyRelease>',
            lambda e, idx=index: self._on_entry_change(idx, 'shmem_size', size_entry.get()),
        )
        size_entry.pack(side='left', padx=2)
        widgets.append(('shmem_size', size_entry))

        return widgets

    # ========== 配置变更处理 ==========
    def _on_config_change(self, index: int, key: str, value: str) -> None:
        """配置变更处理（OptionMenu）。"""
        if 0 <= index < len(self.devices_list):
            self.devices_list[index].config[key] = value
            self._trigger_change()

    def _on_entry_change(self, index: int, key: str, value: str) -> None:
        """Entry 变更处理。"""
        if 0 <= index < len(self.devices_list):
            self.devices_list[index].config[key] = value
            self._trigger_change()

    def _on_checkbox_change(self, index: int, key: str, value: bool) -> None:
        """Checkbox 变更处理。"""
        if 0 <= index < len(self.devices_list):
            self.devices_list[index].config[key] = value
            self._trigger_change()

    def _on_bus_change(self, index: int, value: str) -> None:
        """Bus 变更处理（可能需要更新 controller 关联）。"""
        if 0 <= index < len(self.devices_list):
            device = self.devices_list[index]
            device.config['disk_bus'] = value

            # 检查是否需要更新 controller 关联
            if device.controller_ref:
                # 检查旧的 controller 是否还需要
                old_bus = device.controller_ref.split('_')[0]
                if value not in ['scsi', 'sata', 'ide'] or value != old_bus:
                    # 可能需要删除旧的 controller
                    self._check_and_remove_controller(device.controller_ref)

            # 如果需要，创建新的 controller
            if value in ['scsi', 'sata', 'ide']:
                new_controller_ref = self._get_or_create_controller(value)
                device.controller_ref = new_controller_ref

            self._trigger_change()

    def _check_and_remove_controller(self, controller_id: str) -> None:
        """检查并删除不需要的 controller。"""
        # 检查是否还有其他设备使用该 controller
        in_use = False
        for device in self.devices_list:
            if device.controller_ref == controller_id:
                in_use = True
                break

        if not in_use:
            self._remove_controller(controller_id)

    def _get_or_create_controller(self, controller_type: str) -> str:
        """获取或创建 controller，返回 controller 引用 ID。"""
        # 检查是否已存在该类型的 controller
        for ctrl in self.controllers_list:
            if ctrl.get('type') == controller_type:
                controller_id = ctrl.get('id')
                if controller_id:
                    return controller_id

        # 创建新的 controller
        if controller_type not in self.controller_counter:
            self.controller_counter[controller_type] = 0
        else:
            self.controller_counter[controller_type] += 1

        controller_id = f'{controller_type}_ctrl_{self.controller_counter[controller_type]}'

        model_map = {
            'scsi': 'virtio-scsi',
            'sata': 'sata',
            'ide': 'ide',
            'usb': 'usb-xhci',
        }

        controller = {
            'id': controller_id,
            'type': controller_type,
            'model': model_map.get(controller_type, 'auto'),
            'index': str(self.controller_counter[controller_type]),
        }

        self.controllers_list.append(controller)
        return controller_id

    def _remove_controller(self, controller_id: str) -> None:
        """删除指定的 controller。"""
        self.controllers_list = [c for c in self.controllers_list if c.get('id') != controller_id]

    # ========== 设备列表管理 ==========
    def _delete_device(self, index: int) -> None:
        """删除设备，并处理关联的 controller。"""
        if 0 <= index < len(self.devices_list):
            device = self.devices_list[index]

            # 检查是否需要删除关联的 controller
            if device.controller_ref:
                # 检查是否还有其他设备使用同一个 controller
                controller_in_use = False
                for other_device in self.devices_list:
                    if (
                        other_device != device
                        and other_device.controller_ref == device.controller_ref
                    ):
                        controller_in_use = True
                        break

                # 如果没有其他设备使用该 controller，删除它
                if not controller_in_use:
                    self._remove_controller(device.controller_ref)

            self.devices_list.pop(index)
            self._update_devices_list_display()
            self._trigger_change()

    def _clear_all_devices(self) -> None:
        """清空所有设备。"""
        self.devices_list.clear()
        self.controllers_list.clear()
        self.controller_counter.clear()
        self._update_devices_list_display()
        self._trigger_change()

    # ========== 配置获取 ==========
    def get_config(self) -> dict:
        """获取配置（供父类调用）。"""
        return {
            'devices': self.devices_list,
            'controllers': self.controllers_list,
        }

    def to_xml(self) -> dict[str, Any]:
        """生成 XML 配置字典 - 与 xml_generator.py 期望的格式匹配。"""
        result: dict[str, Any] = {}

        # 按设备类型分组
        for device in self.devices_list:
            device_type = device.device_type
            config = device.config.copy()

            # 将配置转换为 xml_generator 期望的格式
            if device_type == 'disk':
                # 转换为 xml_generator 期望的 disk 格式
                disk_config = self._convert_disk_config(config)
                if 'disks' not in result:
                    result['disks'] = []
                result['disks'].append(disk_config)

            elif device_type == 'graphics':
                gfx_config = self._convert_graphics_config(config)
                if 'graphics' not in result:
                    result['graphics'] = []
                result['graphics'].append(gfx_config)

            elif device_type == 'video':
                video_config = self._convert_video_config(config)
                if 'videos' not in result:
                    result['videos'] = []
                result['videos'].append(video_config)

            elif device_type == 'sound':
                sound_config = self._convert_sound_config(config)
                if 'sounds' not in result:
                    result['sounds'] = []
                result['sounds'].append(sound_config)

            elif device_type == 'controller':
                ctrl_config = self._convert_controller_config(config)
                if 'controllers' not in result:
                    result['controllers'] = []
                result['controllers'].append(ctrl_config)

            elif device_type == 'interface':
                iface_config = self._convert_interface_config(config)
                if 'interfaces' not in result:
                    result['interfaces'] = []
                result['interfaces'].append(iface_config)

            elif device_type == 'input':
                input_config = self._convert_input_config(config)
                if 'inputs' not in result:
                    result['inputs'] = []
                result['inputs'].append(input_config)

            elif device_type == 'hostdev':
                hostdev_config = self._convert_hostdev_config(config)
                if 'hostdevs' not in result:
                    result['hostdevs'] = []
                result['hostdevs'].append(hostdev_config)

            elif device_type == 'serial':
                serial_config = self._convert_serial_config(config)
                if 'serials' not in result:
                    result['serials'] = []
                result['serials'].append(serial_config)

            elif device_type == 'console':
                console_config = self._convert_console_config(config)
                if 'consoles' not in result:
                    result['consoles'] = []
                result['consoles'].append(console_config)

            elif device_type == 'parallel':
                parallel_config = self._convert_parallel_config(config)
                if 'parallels' not in result:
                    result['parallels'] = []
                result['parallels'].append(parallel_config)

            elif device_type == 'channel':
                channel_config = self._convert_channel_config(config)
                if 'channels' not in result:
                    result['channels'] = []
                result['channels'].append(channel_config)

            elif device_type == 'filesystem':
                fs_config = self._convert_filesystem_config(config)
                if 'filesystems' not in result:
                    result['filesystems'] = []
                result['filesystems'].append(fs_config)

            elif device_type == 'rng':
                rng_config = self._convert_rng_config(config)
                if 'rngs' not in result:
                    result['rngs'] = []
                result['rngs'].append(rng_config)

            elif device_type == 'tpm':
                tpm_config = self._convert_tpm_config(config)
                if 'tpms' not in result:
                    result['tpms'] = []
                result['tpms'].append(tpm_config)

            elif device_type == 'watchdog':
                watchdog_config = self._convert_watchdog_config(config)
                if 'watchdogs' not in result:
                    result['watchdogs'] = []
                result['watchdogs'].append(watchdog_config)

            elif device_type == 'memballoon':
                memballoon_config = self._convert_memballoon_config(config)
                if 'memballoons' not in result:
                    result['memballoons'] = []
                result['memballoons'].append(memballoon_config)

            elif device_type == 'iommu':
                iommu_config = self._convert_iommu_config(config)
                if 'iommu' not in result:
                    result['iommu'] = []
                result['iommu'].append(iommu_config)

            elif device_type == 'memory':
                memory_config = self._convert_memory_config(config)
                if 'memory_devices' not in result:
                    result['memory_devices'] = []
                result['memory_devices'].append(memory_config)

            elif device_type == 'shmem':
                shmem_config = self._convert_shmem_config(config)
                if 'shmems' not in result:
                    result['shmems'] = []
                result['shmems'].append(shmem_config)

        # 添加 controllers
        if self.controllers_list:
            if 'controllers' not in result:
                result['controllers'] = []
            for ctrl in self.controllers_list:
                result['controllers'].append(
                    {
                        'type': ctrl.get('type', 'usb'),
                        'model': ctrl.get('model', 'usb-xhci'),
                        'index': ctrl.get('index', '0'),
                    }
                )

        return result

    # ========== 配置转换方法 ==========
    def _convert_disk_config(self, config: dict) -> dict:
        """转换 disk 配置为 xml_generator 期望的格式。"""
        return {
            'type': config.get('disk_type', 'file'),
            'device': config.get('disk_device', 'disk'),
            'bus': config.get('disk_bus', 'virtio'),
            'driver_type': config.get('disk_driver', 'qcow2'),
            'target_dev': config.get('disk_target', 'vda'),
            'source': config.get('disk_source', ''),
            'source_file': config.get('disk_source', ''),
            'readonly': config.get('disk_readonly', False),
            'boot_order': config.get('disk_boot_order', ''),
        }

    def _convert_graphics_config(self, config: dict) -> dict:
        """转换 graphics 配置。"""
        return {
            'type': config.get('gfx_type', 'vnc'),
            'port': config.get('gfx_port', '-1'),
            'autoport': config.get('gfx_autoport', True),
            'listen': config.get('gfx_listen', '0.0.0.0'),
            'keymap': config.get('gfx_keymap', 'en-us'),
            'passwd': config.get('gfx_passwd', ''),
        }

    def _convert_video_config(self, config: dict) -> dict:
        """转换 video 配置。"""
        return {
            'model': config.get('video_model', 'qxl'),
            'vram': config.get('video_vram', '16384'),
            'heads': config.get('video_heads', '1'),
            'accel3d': config.get('video_accel3d', False),
        }

    def _convert_sound_config(self, config: dict) -> dict:
        """转换 sound 配置。"""
        return {
            'model': config.get('sound_model', 'ich9'),
            'codec': config.get('sound_codec', 'duplex'),
        }

    def _convert_controller_config(self, config: dict) -> dict:
        """转换 controller 配置。"""
        return {
            'type': config.get('ctrl_type', 'usb'),
            'model': config.get('ctrl_model', 'usb-xhci'),
            'index': config.get('ctrl_index', '0'),
            'queues': config.get('ctrl_queues', ''),
        }

    def _convert_interface_config(self, config: dict) -> dict:
        """转换 interface 配置。"""
        return {
            'type': config.get('iface_type', 'network'),
            'source': config.get('iface_source', 'default'),
            'model': config.get('iface_model', 'virtio'),
            'mac': config.get('iface_mac', ''),
            'boot_order': config.get('iface_boot', ''),
        }

    def _convert_input_config(self, config: dict) -> dict:
        """转换 input 配置。"""
        return {
            'type': config.get('input_type', 'tablet'),
            'bus': config.get('input_bus', 'usb'),
        }

    def _convert_hostdev_config(self, config: dict) -> dict:
        """转换 hostdev 配置。"""
        return {
            'type': config.get('hostdev_type', 'usb'),
            'usb': config.get('hostdev_usb', ''),
            'pci': config.get('hostdev_pci', ''),
            'managed': config.get('hostdev_managed', 'yes'),
            'policy': config.get('hostdev_policy', 'optional'),
        }

    def _convert_serial_config(self, config: dict) -> dict:
        """转换 serial 配置。"""
        return {
            'type': config.get('serial_type', 'pty'),
            'port': config.get('serial_port', '0'),
            'path': config.get('serial_path', ''),
        }

    def _convert_console_config(self, config: dict) -> dict:
        """转换 console 配置。"""
        return {
            'type': config.get('console_type', 'pty'),
            'target': config.get('console_target', 'virtio'),
        }

    def _convert_parallel_config(self, config: dict) -> dict:
        """转换 parallel 配置。"""
        return {
            'type': config.get('parallel_type', 'pty'),
            'port': config.get('parallel_port', '0'),
            'path': config.get('parallel_path', ''),
        }

    def _convert_channel_config(self, config: dict) -> dict:
        """转换 channel 配置。"""
        return {
            'type': config.get('channel_type', 'unix'),
            'name': config.get('channel_name', 'org.qemu.guest_agent.0'),
            'path': config.get('channel_path', ''),
        }

    def _convert_filesystem_config(self, config: dict) -> dict:
        """转换 filesystem 配置。"""
        return {
            'type': config.get('fs_type', 'mount'),
            'accessmode': config.get('fs_access', 'passthrough'),
            'source': config.get('fs_source', ''),
            'target': config.get('fs_target', ''),
            'readonly': config.get('fs_readonly', False),
        }

    def _convert_rng_config(self, config: dict) -> dict:
        """转换 rng 配置。"""
        return {
            'model': config.get('rng_model', 'virtio'),
            'backend': config.get('rng_backend', 'random'),
            'source': config.get('rng_source', '/dev/urandom'),
            'rate': config.get('rng_rate', ''),
        }

    def _convert_tpm_config(self, config: dict) -> dict:
        """转换 tpm 配置。"""
        return {
            'model': config.get('tpm_model', 'tpm-tis'),
            'backend': config.get('tpm_backend', 'emulator'),
            'device': config.get('tpm_device', '/dev/tpm0'),
            'version': config.get('tpm_version', '2.0'),
        }

    def _convert_watchdog_config(self, config: dict) -> dict:
        """转换 watchdog 配置。"""
        return {
            'model': config.get('watchdog_model', 'i6300esb'),
            'action': config.get('watchdog_action', 'reset'),
        }

    def _convert_memballoon_config(self, config: dict) -> dict:
        """转换 memballoon 配置。"""
        return {
            'model': config.get('memballoon_model', 'virtio'),
            'period': config.get('memballoon_period', ''),
        }

    def _convert_iommu_config(self, config: dict) -> dict:
        """转换 iommu 配置。"""
        return {
            'model': config.get('iommu_model', 'intel'),
            'intremap': config.get('iommu_intremap', False),
            'caching': config.get('iommu_caching', False),
            'aw': config.get('iommu_aw', ''),
        }

    def _convert_memory_config(self, config: dict) -> dict:
        """转换 memory 配置。"""
        return {
            'model': config.get('memory_model', 'dimm'),
            'size': config.get('memory_size', '524288'),
            'node': config.get('memory_node', '0'),
            'access': config.get('memory_access', 'private'),
        }

    def _convert_shmem_config(self, config: dict) -> dict:
        """转换 shmem 配置。"""
        return {
            'name': config.get('shmem_name', 'shmem0'),
            'model': config.get('shmem_model', 'ivshmem-plain'),
            'size': config.get('shmem_size', '4'),
            'role': config.get('shmem_role', 'peer'),
        }


# 兼容别名
DevicesTab = DevicesConfigTab
