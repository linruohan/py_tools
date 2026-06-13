"""设备配置模块 - 整合所有设备配置到一个 Tab (根据 libvirt devices 文档)."""

from collections.abc import Callable
from typing import Any, ClassVar

import customtkinter as ctk

from components.base_tab import BaseConfigTab
from utils.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class DevicesConfigTab(BaseConfigTab):
    """设备配置 Tab - 整合所有设备配置，支持 XML 动态预览。"""

    # 所有设备类型 (根据 libvirt devices 文档)
    DEVICE_TYPES: ClassVar[dict] = {
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
    DEVICE_CATEGORIES: ClassVar[dict] = {
        'all': 'All Devices (所有设备)',
        'base': 'Base Devices (基础设备)',
        'console': 'Consoles & Ports (控制台和端口)',
        'hostdev': 'Host Devices (主机设备)',
        'special': 'Special Devices (特殊设备)',
        'memory': 'Memory Devices (内存设备)',
        'advanced': 'Advanced (高级功能)',
    }

    # 类别与设备类型的映射
    CATEGORY_DEVICES: ClassVar[dict] = {
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

    def __init__(self, master, on_change_callback: Callable | None = None, **kwargs):
        super().__init__(master, on_change_callback, **kwargs)
        self.devices_list: list[dict] = []  # 已添加的设备列表
        self.current_category = 'all'  # 当前选中的类别
        self.selected_device_type: str | None = None  # 当前选中的设备类型
        self.config_widgets: dict = {}  # 当前配置界面的 widget 引用
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面 - 上下布局：上部设备选择和配置，下部已添加设备列表。"""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)  # 上部：设备配置
        self.grid_rowconfigure(1, weight=0)  # 下部：设备列表

        # ===== 上部：设备选择和配置 =====
        top_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        top_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        top_frame.grid_columnconfigure(0, weight=1)
        top_frame.grid_rowconfigure(2, weight=1)

        # 第一行：类别筛选
        category_toolbar = ctk.CTkFrame(top_frame, fg_color='transparent')
        category_toolbar.grid(row=0, column=0, sticky='ew', padx=5, pady=5)

        ctk.CTkLabel(category_toolbar, text='Category:', font=CTK_FONT_SMALL, width=70).pack(
            side='left', padx=5
        )

        self.category_menu = ctk.CTkOptionMenu(
            category_toolbar,
            values=list(self.DEVICE_CATEGORIES.values()),
            width=180,
            font=CTK_FONT_SMALL,
            command=self._on_category_change,
        )
        self.category_menu.set('All Devices (所有设备)')
        self.category_menu.pack(side='left', padx=5)

        # 设备类型选择
        ctk.CTkLabel(category_toolbar, text='Device Type:', font=CTK_FONT_SMALL, width=80).pack(
            side='left', padx=10
        )

        self.device_type_menu = ctk.CTkOptionMenu(
            category_toolbar,
            values=['None'],
            width=200,
            font=CTK_FONT_SMALL,
            command=self._on_device_type_change,
        )
        self.device_type_menu.set('None')
        self.device_type_menu.pack(side='left', padx=5)

        # 添加设备按钮
        self.add_btn = ctk.CTkButton(
            category_toolbar,
            text='Add Device',
            width=100,
            height=30,
            font=CTK_FONT_SMALL,
            command=self._add_device,
            fg_color='#4caf50',
            hover_color='#388e3c',
        )
        self.add_btn.pack(side='right', padx=5)

        # 第二行：XML 预览开关
        xml_toolbar = ctk.CTkFrame(top_frame, fg_color='transparent')
        xml_toolbar.grid(row=1, column=0, sticky='ew', padx=5, pady=2)

        ctk.CTkLabel(xml_toolbar, text='XML Preview:', font=CTK_FONT_SMALL, width=80).pack(
            side='left', padx=5
        )

        self.xml_preview_check = ctk.CTkCheckBox(
            xml_toolbar,
            text='Show XML Preview',
            font=CTK_FONT_SMALL,
            command=self._toggle_xml_preview,
        )
        self.xml_preview_check.pack(side='left', padx=5)

        # 第三行：设备配置 + XML 预览
        config_container = ctk.CTkFrame(top_frame, fg_color='transparent')
        config_container.grid(row=2, column=0, sticky='nsew', padx=5, pady=5)
        config_container.grid_columnconfigure(0, weight=1)
        config_container.grid_rowconfigure(0, weight=1)

        # 设备配置框架
        self.config_frame = ctk.CTkScrollableFrame(
            config_container, fg_color=BG_COLOR_CONTENT, corner_radius=6
        )
        self.config_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

        # XML 预览框架 (默认隐藏)
        self.xml_frame = ctk.CTkScrollableFrame(
            config_container, fg_color='#1e1e1e', corner_radius=6
        )
        self.xml_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        self.xml_frame.grid_remove()

        xml_label = ctk.CTkLabel(
            self.xml_frame, text='XML Preview', font=CTK_FONT_BOLD, text_color='#4caf50'
        )
        xml_label.pack(anchor='w', padx=5, pady=5)

        self.xml_preview_label = ctk.CTkLabel(
            self.xml_frame,
            text='',
            font=('Consolas', 10),
            text_color='#cccccc',
            justify='left',
            anchor='nw',
        )
        self.xml_preview_label.pack(fill='both', expand=True, padx=5, pady=5)

        # ===== 下部：已添加设备列表 =====
        bottom_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        bottom_frame.grid(row=1, column=0, sticky='ew', padx=5, pady=5)
        bottom_frame.grid_columnconfigure(0, weight=1)

        # 工具栏
        list_toolbar = ctk.CTkFrame(bottom_frame, fg_color='transparent')
        list_toolbar.grid(row=0, column=0, sticky='ew', padx=5, pady=3)

        ctk.CTkLabel(list_toolbar, text='Added Devices:', font=CTK_FONT_SMALL).grid(
            row=0, column=0, padx=5, pady=3, sticky='w'
        )

        clear_btn = ctk.CTkButton(
            list_toolbar,
            text='Clear All',
            width=80,
            height=28,
            font=CTK_FONT_SMALL,
            command=self._clear_all_devices,
            fg_color='#f44336',
            hover_color='#d32f2f',
        )
        clear_btn.grid(row=0, column=1, padx=5)

        # 设备列表
        self.devices_list_frame = ctk.CTkScrollableFrame(
            bottom_frame, fg_color='transparent', height=120
        )
        self.devices_list_frame.grid(row=1, column=0, sticky='ew', padx=5, pady=3)

    def _on_category_change(self, selected_label: str) -> None:
        """类别改变时的处理。"""
        # 获取选中的类别值
        category_value: str | None = None
        for key, label in self.DEVICE_CATEGORIES.items():
            if label == selected_label:
                category_value = key
                break

        self.current_category = category_value or 'all'

        # 更新设备类型选项
        if category_value == 'all':
            device_types = ['None', *list(self.DEVICE_TYPES.values())]
        else:
            device_types_in_category = self.CATEGORY_DEVICES.get(category_value, [])
            device_types = ['None'] + [
                self.DEVICE_TYPES[dt] for dt in device_types_in_category if dt in self.DEVICE_TYPES
            ]

        self.device_type_menu.configure(values=device_types)
        self.device_type_menu.set('None')
        self._on_device_type_change('None')

    def _on_device_type_change(self, selected_label: str) -> None:
        """设备类型改变时的处理 - 动态生成配置界面。"""
        # 清空配置框架
        for widget in self.config_frame.winfo_children():
            widget.destroy()
        self.config_widgets.clear()

        if selected_label == 'None':
            self.selected_device_type = None
            # 显示提示信息
            info_label = ctk.CTkLabel(
                self.config_frame,
                text='Please select a device type from the dropdown above.',
                font=CTK_FONT_MAIN,
                text_color='#888888',
            )
            info_label.pack(padx=10, pady=20)
            return

        # 找到对应的设备类型键
        for key, label in self.DEVICE_TYPES.items():
            if label == selected_label:
                self.selected_device_type = key
                break

        # 动态生成配置界面
        self._build_device_config_ui()
        self._update_xml_preview()

    def _build_device_config_ui(self) -> None:
        """根据选中的设备类型动态构建配置界面。"""
        device_type = self.selected_device_type
        if not device_type:
            return

        # 配置框架
        self.config_frame.configure(fg_color=BG_COLOR_CONTENT)

        # 标题
        title = ctk.CTkLabel(
            self.config_frame,
            text=f'Configuring: {self.DEVICE_TYPES.get(device_type, device_type)}',
            font=CTK_FONT_BOLD,
            text_color='#4caf50',
        )
        title.pack(anchor='w', padx=10, pady=10)

        # 根据设备类型构建不同的配置界面
        if device_type == 'disk':
            self._build_disk_config()
        elif device_type == 'graphics':
            self._build_graphics_config()
        elif device_type == 'video':
            self._build_video_config()
        elif device_type == 'sound':
            self._build_sound_config()
        elif device_type == 'controller':
            self._build_controller_config()
        elif device_type == 'interface':
            self._build_interface_config()
        elif device_type == 'input':
            self._build_input_config()
        elif device_type == 'hostdev':
            self._build_hostdev_config()
        elif device_type == 'watchdog':
            self._build_watchdog_config()
        elif device_type == 'memballoon':
            self._build_memballoon_config()
        elif device_type == 'rng':
            self._build_rng_config()
        elif device_type == 'tpm':
            self._build_tpm_config()
        elif device_type == 'filesystem':
            self._build_filesystem_config()
        elif device_type == 'console':
            self._build_console_config()
        elif device_type == 'serial':
            self._build_serial_config()
        elif device_type == 'parallel':
            self._build_parallel_config()
        elif device_type == 'channel':
            self._build_channel_config()
        elif device_type == 'iommu':
            self._build_iommu_config()
        elif device_type == 'memory':
            self._build_memory_config()
        elif device_type == 'shmem':
            self._build_shmem_config()
        else:
            # 其他设备类型的通用配置
            self._build_generic_config(device_type)

    def _create_row(self, parent, label_text: str, widgets: list | None = None, **kwargs):
        """创建一行配置（label + widgets），pack 布局，左对齐。"""
        row_frame = ctk.CTkFrame(parent, fg_color='transparent')
        row_frame.pack(fill='x', padx=5, pady=2, anchor='w')

        if label_text:
            label = ctk.CTkLabel(
                row_frame,
                text=label_text,
                font=CTK_FONT_MAIN,
                width=kwargs.get('label_width', 120),
                anchor='w',
            )
            label.pack(side='left', padx=5)

        if widgets:
            for widget in widgets:
                widget.pack(side='left', padx=3)

        return row_frame

    def _build_disk_config(self) -> None:
        """构建磁盘设备配置界面。"""
        # 第一行：type, device, bus
        self._create_row(
            self.config_frame,
            'Type:',
            [
                self._create_optionmenu(
                    'disk_type',
                    [
                        'file',
                        'block',
                        'network',
                        'volume',
                        'dir',
                        'nvme',
                        'vhostuser',
                        'vhostvdpa',
                        'ctl',
                        'none',
                    ],
                    'file',
                )
            ],
        )
        self._create_row(
            self.config_frame,
            'Device:',
            [self._create_optionmenu('disk_device', ['disk', 'cdrom', 'lun', 'floppy'], 'disk')],
        )
        self._create_row(
            self.config_frame,
            'Bus:',
            [
                self._create_optionmenu(
                    'disk_bus', ['virtio', 'sata', 'ide', 'scsi', 'usb', 'nvme'], 'virtio'
                )
            ],
        )

        # 第二行：source path
        self._create_row(
            self.config_frame,
            'Source Path:',
            [self._create_entry('disk_source', '/var/lib/libvirt/images/disk.qcow2', 400)],
        )

        # 第三行：driver format
        self._create_row(
            self.config_frame,
            'Driver Format:',
            [
                self._create_optionmenu(
                    'disk_driver', ['qcow2', 'raw', 'vmdk', 'vdi', 'none'], 'qcow2'
                )
            ],
        )

        # 第四行：target dev
        self._create_row(
            self.config_frame, 'Target Device:', [self._create_entry('disk_target', 'vda', 100)]
        )

        # 第五行：readonly, boot_order, startup_policy
        self._create_row(
            self.config_frame,
            'Options:',
            [
                self._create_checkbox('disk_readonly', 'Read-only'),
                self._create_entry('disk_boot_order', '', 60, placeholder='Boot Order'),
                self._create_optionmenu(
                    'disk_startup', ['mandatory', 'requisite', 'optional', 'none'], 'none'
                ),
            ],
        )

    def _build_graphics_config(self) -> None:
        """构建图形显示配置界面。"""
        # 第一行：type, autoport
        self._create_row(
            self.config_frame,
            'Type:',
            [
                self._create_optionmenu(
                    'gfx_type',
                    ['vnc', 'spice', 'rdp', 'sdl', 'desktop', 'egl-headless', 'dbus', 'none'],
                    'vnc',
                )
            ],
        )
        self._create_row(
            self.config_frame, 'Autoport:', [self._create_checkbox('gfx_autoport', 'Enabled', True)]
        )

        # 第二行：port, listen, tls_port (SPICE)
        self._create_row(self.config_frame, 'Port:', [self._create_entry('gfx_port', '-1', 80)])
        self._create_row(
            self.config_frame, 'Listen:', [self._create_entry('gfx_listen', '0.0.0.0', 120)]
        )
        self._create_row(
            self.config_frame, 'TLS Port:', [self._create_entry('gfx_tls_port', '-1', 80)]
        )

        # 第三行：passwd, keymap
        self._create_row(
            self.config_frame, 'Password:', [self._create_entry('gfx_passwd', '', 150, show='*')]
        )
        self._create_row(
            self.config_frame, 'Keymap:', [self._create_entry('gfx_keymap', 'en-us', 100)]
        )

        # 第四行：share_policy (VNC), power_control
        self._create_row(
            self.config_frame,
            'Share Policy:',
            [
                self._create_optionmenu(
                    'gfx_share',
                    ['allow-exclusive', 'force-shared', 'ignore', 'none'],
                    'allow-exclusive',
                )
            ],
        )
        self._create_row(
            self.config_frame, 'Power Control:', [self._create_checkbox('gfx_power', 'Enabled')]
        )

        # SPICE 选项
        spice_frame = ctk.CTkFrame(self.config_frame, fg_color='transparent')
        spice_frame.pack(fill='x', padx=5, pady=10)
        ctk.CTkLabel(
            spice_frame, text='SPICE Options:', font=CTK_FONT_BOLD, text_color='#ff9800'
        ).pack(anchor='w')

        self._create_row(
            spice_frame,
            'Default Mode:',
            [self._create_optionmenu('spice_mode', ['any', 'secure', 'insecure'], 'any')],
        )
        self._create_row(
            spice_frame,
            'Image Compression:',
            [
                self._create_optionmenu(
                    'spice_image', ['auto_glz', 'auto_lz', 'quic', 'glz', 'lz', 'off'], 'auto_glz'
                )
            ],
        )
        self._create_row(
            spice_frame,
            'Clipboard:',
            [self._create_optionmenu('spice_clipboard', ['yes', 'no'], 'yes')],
        )
        self._create_row(
            spice_frame,
            'Mouse Mode:',
            [self._create_optionmenu('spice_mouse', ['client', 'server'], 'client')],
        )

    def _build_video_config(self) -> None:
        """构建视频设备配置界面。"""
        self._create_row(
            self.config_frame,
            'Model:',
            [
                self._create_optionmenu(
                    'video_model',
                    ['vga', 'cirrus', 'vmvga', 'qxl', 'virtio', 'gop', 'bochs', 'ramfb', 'none'],
                    'qxl',
                )
            ],
        )
        self._create_row(
            self.config_frame, 'VRAM (KiB):', [self._create_entry('video_vram', '16384', 100)]
        )
        self._create_row(self.config_frame, 'Heads:', [self._create_entry('video_heads', '1', 60)])
        self._create_row(
            self.config_frame,
            '3D Acceleration:',
            [self._create_checkbox('video_accel3d', 'Enabled')],
        )

    def _build_sound_config(self) -> None:
        """构建音频设备配置界面。"""
        self._create_row(
            self.config_frame,
            'Model:',
            [
                self._create_optionmenu(
                    'sound_model',
                    ['sb16', 'es1370', 'ac97', 'ich6', 'ich9', 'usb', 'virtio', 'none'],
                    'ich9',
                )
            ],
        )
        self._create_row(
            self.config_frame,
            'Codec:',
            [
                self._create_optionmenu(
                    'sound_codec', ['duplex', 'micro', 'output', 'none'], 'duplex'
                )
            ],
        )

    def _build_controller_config(self) -> None:
        """构建控制器配置界面。"""
        self._create_row(
            self.config_frame,
            'Type:',
            [
                self._create_optionmenu(
                    'ctrl_type',
                    ['ide', 'fdc', 'scsi', 'sata', 'usb', 'virtio-serial', 'pci'],
                    'usb',
                )
            ],
        )
        self._create_row(
            self.config_frame,
            'Model:',
            [
                self._create_optionmenu(
                    'ctrl_model',
                    ['auto', 'virtio-scsi', 'pci-root', 'pci-bridge', 'pcie-root', 'none'],
                    'usb-xhci',
                )
            ],
        )
        self._create_row(self.config_frame, 'Index:', [self._create_entry('ctrl_index', '0', 60)])
        self._create_row(
            self.config_frame,
            'Queues:',
            [self._create_entry('ctrl_queues', '', 60, placeholder='optional')],
        )

    def _build_interface_config(self) -> None:
        """构建网络接口配置界面。"""
        self._create_row(
            self.config_frame,
            'Type:',
            [
                self._create_optionmenu(
                    'iface_type',
                    ['network', 'bridge', 'direct', 'user', 'vhostuser', 'vdpa', 'none'],
                    'network',
                )
            ],
        )
        self._create_row(
            self.config_frame, 'Source:', [self._create_entry('iface_source', 'default', 150)]
        )
        self._create_row(
            self.config_frame,
            'Model:',
            [
                self._create_optionmenu(
                    'iface_model', ['virtio', 'e1000', 'e1000e', 'rtl8139', 'vmxnet3'], 'virtio'
                )
            ],
        )
        self._create_row(
            self.config_frame,
            'MAC Address:',
            [self._create_entry('iface_mac', '', 150, placeholder='auto-generated')],
        )
        self._create_row(
            self.config_frame,
            'Boot Order:',
            [self._create_entry('iface_boot', '', 60, placeholder='optional')],
        )

    def _build_input_config(self) -> None:
        """构建输入设备配置界面。"""
        self._create_row(
            self.config_frame,
            'Type:',
            [self._create_optionmenu('input_type', ['mouse', 'tablet', 'keyboard'], 'tablet')],
        )
        self._create_row(
            self.config_frame,
            'Bus:',
            [self._create_optionmenu('input_bus', ['usb', 'virtio', 'ps2'], 'usb')],
        )

    def _build_hostdev_config(self) -> None:
        """构建主机设备配置界面。"""
        self._create_row(
            self.config_frame,
            'Type:',
            [self._create_optionmenu('hostdev_type', ['usb', 'pci', 'scsi', 'mdev'], 'usb')],
        )

        # USB 设备
        self._create_row(
            self.config_frame,
            'Vendor/Product:',
            [self._create_entry('hostdev_usb', '', 200, placeholder='e.g., 1234:abcd')],
        )
        self._create_row(
            self.config_frame,
            'Startup Policy:',
            [
                self._create_optionmenu(
                    'hostdev_policy', ['mandatory', 'requisite', 'optional'], 'optional'
                )
            ],
        )

        # PCI 设备
        self._create_row(
            self.config_frame,
            'PCI Address:',
            [self._create_entry('hostdev_pci', '', 200, placeholder='domain:bus:slot.func')],
        )
        self._create_row(
            self.config_frame,
            'Managed:',
            [self._create_optionmenu('hostdev_managed', ['yes', 'no'], 'yes')],
        )

        # MDEV 设备
        self._create_row(
            self.config_frame,
            'MDEV UUID:',
            [self._create_entry('hostdev_mdev', '', 300, placeholder='UUID of mediated device')],
        )

    def _build_watchdog_config(self) -> None:
        """构建看门狗设备配置界面。"""
        self._create_row(
            self.config_frame,
            'Model:',
            [
                self._create_optionmenu(
                    'watchdog_model', ['i6300esb', 'ib700', 'itco', 'diag288'], 'i6300esb'
                )
            ],
        )
        self._create_row(
            self.config_frame,
            'Action:',
            [
                self._create_optionmenu(
                    'watchdog_action',
                    ['reset', 'shutdown', 'poweroff', 'pause', 'none', 'dump', 'inject-nmi'],
                    'reset',
                )
            ],
        )

    def _build_memballoon_config(self) -> None:
        """构建内存气球配置界面。"""
        self._create_row(
            self.config_frame,
            'Model:',
            [self._create_optionmenu('memballoon_model', ['virtio', 'xen', 'none'], 'virtio')],
        )
        self._create_row(
            self.config_frame,
            'Stats Period:',
            [self._create_entry('memballoon_period', '', 80, placeholder='seconds, optional')],
        )

    def _build_rng_config(self) -> None:
        """构建随机数发生器配置界面。"""
        self._create_row(
            self.config_frame,
            'Model:',
            [
                self._create_optionmenu(
                    'rng_model',
                    ['virtio', 'virtio-transitional', 'virtio-non-transitional'],
                    'virtio',
                )
            ],
        )
        self._create_row(
            self.config_frame,
            'Backend Model:',
            [self._create_optionmenu('rng_backend', ['random', 'egd', 'builtin'], 'random')],
        )
        self._create_row(
            self.config_frame, 'Source:', [self._create_entry('rng_source', '/dev/urandom', 300)]
        )
        self._create_row(
            self.config_frame,
            'Rate (bytes/period):',
            [self._create_entry('rng_rate', '', 80, placeholder='optional')],
        )

    def _build_tpm_config(self) -> None:
        """构建 TPM 设备配置界面。"""
        self._create_row(
            self.config_frame,
            'Model:',
            [
                self._create_optionmenu(
                    'tpm_model', ['tpm-tis', 'tpm-crb', 'tpm-spapr', 'spapr-tpm-proxy'], 'tpm-tis'
                )
            ],
        )
        self._create_row(
            self.config_frame,
            'Backend Type:',
            [
                self._create_optionmenu(
                    'tpm_backend', ['passthrough', 'emulator', 'external'], 'emulator'
                )
            ],
        )
        self._create_row(
            self.config_frame, 'Device Path:', [self._create_entry('tpm_device', '/dev/tpm0', 300)]
        )
        self._create_row(
            self.config_frame,
            'Version:',
            [self._create_optionmenu('tpm_version', ['1.2', '2.0'], '2.0')],
        )

    def _build_filesystem_config(self) -> None:
        """构建文件系统配置界面。"""
        self._create_row(
            self.config_frame,
            'Type:',
            [
                self._create_optionmenu(
                    'fs_type', ['mount', 'template', 'file', 'block', 'ram', 'bind'], 'mount'
                )
            ],
        )
        self._create_row(
            self.config_frame,
            'Access Mode:',
            [
                self._create_optionmenu(
                    'fs_access', ['passthrough', 'mapped', 'squash'], 'passthrough'
                )
            ],
        )
        self._create_row(
            self.config_frame,
            'Source Dir:',
            [self._create_entry('fs_source', '/export/to/guest', 300)],
        )
        self._create_row(
            self.config_frame,
            'Target Dir:',
            [self._create_entry('fs_target', '/import/from/host', 300)],
        )
        self._create_row(
            self.config_frame, 'Read-only:', [self._create_checkbox('fs_readonly', 'Enabled')]
        )

    def _build_console_config(self) -> None:
        """构建控制台配置界面。"""
        self._create_row(
            self.config_frame,
            'Type:',
            [
                self._create_optionmenu(
                    'console_type',
                    [
                        'pty',
                        'vc',
                        'stdio',
                        'null',
                        'tty',
                        'udp',
                        'unix',
                        'spicevmc',
                        'qemu-vdagent',
                    ],
                    'pty',
                )
            ],
        )
        self._create_row(
            self.config_frame,
            'Target Type:',
            [self._create_optionmenu('console_target', ['serial', 'virtio', 'xen'], 'virtio')],
        )

    def _build_serial_config(self) -> None:
        """构建串口配置界面。"""
        self._create_row(
            self.config_frame,
            'Type:',
            [
                self._create_optionmenu(
                    'serial_type',
                    ['pty', 'file', 'dev', 'null', 'udp', 'tcp', 'unix', 'spiceport'],
                    'pty',
                )
            ],
        )
        self._create_row(self.config_frame, 'Port:', [self._create_entry('serial_port', '0', 60)])
        self._create_row(
            self.config_frame,
            'Path:',
            [self._create_entry('serial_path', '', 300, placeholder='/dev/ttyS0 or log file path')],
        )

    def _build_parallel_config(self) -> None:
        """构建并口配置界面。"""
        self._create_row(
            self.config_frame,
            'Type:',
            [self._create_optionmenu('parallel_type', ['pty', 'dev', 'null'], 'pty')],
        )
        self._create_row(self.config_frame, 'Port:', [self._create_entry('parallel_port', '0', 60)])
        self._create_row(
            self.config_frame,
            'Path:',
            [self._create_entry('parallel_path', '', 300, placeholder='/dev/parport0')],
        )

    def _build_channel_config(self) -> None:
        """构建通道配置界面。"""
        self._create_row(
            self.config_frame,
            'Type:',
            [
                self._create_optionmenu(
                    'channel_type', ['unix', 'pty', 'spicevmc', 'qemu-vdagent', 'virtio'], 'unix'
                )
            ],
        )
        self._create_row(
            self.config_frame,
            'Target Name:',
            [self._create_entry('channel_name', 'org.qemu.guest_agent.0', 300)],
        )
        self._create_row(
            self.config_frame,
            'Source Path:',
            [
                self._create_entry(
                    'channel_path', '', 300, placeholder='/var/lib/libvirt/qemu/agent.sock'
                )
            ],
        )

    def _build_iommu_config(self) -> None:
        """构建 IOMMU 设备配置界面。"""
        self._create_row(
            self.config_frame,
            'Model:',
            [self._create_optionmenu('iommu_model', ['intel', 'amd', 'virtio', 'smmuv3'], 'intel')],
        )
        self._create_row(
            self.config_frame,
            'Interrupt Remap:',
            [self._create_checkbox('iommu_intremap', 'Enabled')],
        )
        self._create_row(
            self.config_frame, 'Caching Mode:', [self._create_checkbox('iommu_caching', 'Enabled')]
        )
        self._create_row(
            self.config_frame,
            'Address Width:',
            [self._create_entry('iommu_aw', '', 80, placeholder='e.g., 48')],
        )

    def _build_memory_config(self) -> None:
        """构建内存设备配置界面。"""
        self._create_row(
            self.config_frame,
            'Model:',
            [
                self._create_optionmenu(
                    'memory_model',
                    ['dimm', 'nvdimm', 'virtio-pmem', 'virtio-mem', 'sgx-epc'],
                    'dimm',
                )
            ],
        )
        self._create_row(
            self.config_frame, 'Size (KiB):', [self._create_entry('memory_size', '524288', 100)]
        )
        self._create_row(
            self.config_frame, 'NUMA Node:', [self._create_entry('memory_node', '0', 60)]
        )
        self._create_row(
            self.config_frame,
            'Access:',
            [self._create_optionmenu('memory_access', ['private', 'shared'], 'private')],
        )

    def _build_shmem_config(self) -> None:
        """构建共享内存配置界面。"""
        self._create_row(
            self.config_frame, 'Name:', [self._create_entry('shmem_name', 'my_shmem', 150)]
        )
        self._create_row(
            self.config_frame,
            'Model:',
            [
                self._create_optionmenu(
                    'shmem_model', ['ivshmem-plain', 'ivshmem-doorbell'], 'ivshmem-plain'
                )
            ],
        )
        self._create_row(
            self.config_frame, 'Size (MiB):', [self._create_entry('shmem_size', '4', 80)]
        )
        self._create_row(
            self.config_frame,
            'Role:',
            [self._create_optionmenu('shmem_role', ['master', 'peer'], 'peer')],
        )

    def _build_generic_config(self, device_type: str) -> None:
        """通用配置界面（用于其他设备类型）。"""
        info_label = ctk.CTkLabel(
            self.config_frame,
            text=f'Configuration for {self.DEVICE_TYPES.get(device_type, device_type)}\n\nUse XML editing for advanced configuration.',
            font=CTK_FONT_MAIN,
            text_color='#888888',
            justify='center',
        )
        info_label.pack(padx=10, pady=30)

    # ===== 辅助方法：创建 widget =====
    def _create_optionmenu(
        self, name: str, values: list, default: str | None = None, width: int = 120
    ) -> ctk.CTkOptionMenu:
        """创建 OptionMenu widget。"""
        widget = ctk.CTkOptionMenu(
            self.config_frame,
            values=values,
            width=width,
            font=CTK_FONT_SMALL,
            command=lambda e=None: self._on_config_change(),
        )
        if default:
            widget.set(default)
        self.config_widgets[name] = widget
        return widget

    def _create_entry(
        self,
        name: str,
        default: str = '',
        width: int = 200,
        placeholder: str = '',
        show: str | None = None,
    ) -> ctk.CTkEntry:
        """创建 Entry widget。"""
        widget = ctk.CTkEntry(
            self.config_frame,
            width=width,
            font=CTK_FONT_SMALL,
            placeholder_text=placeholder,
            show=show,
        )
        if default:
            widget.insert(0, default)
        widget.bind('<KeyRelease>', lambda e: self._on_config_change())
        self.config_widgets[name] = widget
        return widget

    def _create_checkbox(self, name: str, text: str, default: bool = False) -> ctk.CTkCheckBox:
        """创建 Checkbox widget。"""
        widget = ctk.CTkCheckBox(
            self.config_frame,
            text=text,
            font=CTK_FONT_SMALL,
            command=self._on_config_change,
        )
        if default:
            widget.select()
        else:
            widget.deselect()
        self.config_widgets[name] = widget
        return widget

    # ===== XML 预览 =====
    def _toggle_xml_preview(self) -> None:
        """切换 XML 预览显示。"""
        if self.xml_preview_check.get():
            self.xml_frame.grid()
            self.config_frame.grid_remove()
        else:
            self.config_frame.grid()
            self.xml_frame.grid_remove()
        self._update_xml_preview()

    def _update_xml_preview(self) -> None:
        """更新 XML 预览。"""
        xml_text = self._generate_device_xml()
        self.xml_preview_label.configure(text=xml_text)

    def _generate_device_xml(self) -> str:
        """根据当前配置生成 XML。"""
        if not self.selected_device_type:
            return '<!-- No device selected -->'

        device_type = self.selected_device_type

        # 检查是否选择了 "none"
        if device_type == 'disk':
            disk_type = (
                self.config_widgets.get('disk_type', {}).get()
                if hasattr(self.config_widgets.get('disk_type'), 'get')
                else 'file'
            )
            if disk_type == 'none':
                return '<!-- disk: none selected, element will be removed -->'

        if device_type == 'graphics':
            gfx_type = (
                self.config_widgets.get('gfx_type', {}).get()
                if hasattr(self.config_widgets.get('gfx_type'), 'get')
                else 'vnc'
            )
            if gfx_type == 'none':
                return '<!-- graphics: none selected, element will be removed -->'

        if device_type == 'video':
            video_model = (
                self.config_widgets.get('video_model', {}).get()
                if hasattr(self.config_widgets.get('video_model'), 'get')
                else 'qxl'
            )
            if video_model == 'none':
                return '<!-- video: none selected, element will be removed -->'

        if device_type == 'sound':
            sound_model = (
                self.config_widgets.get('sound_model', {}).get()
                if hasattr(self.config_widgets.get('sound_model'), 'get')
                else 'ich9'
            )
            if sound_model == 'none':
                return '<!-- sound: none selected, element will be removed -->'

        if device_type == 'memballoon':
            memballoon_model = (
                self.config_widgets.get('memballoon_model', {}).get()
                if hasattr(self.config_widgets.get('memballoon_model'), 'get')
                else 'virtio'
            )
            if memballoon_model == 'none':
                return '<!-- memballoon: none selected, element will be removed -->'

        if device_type == 'iommu':
            iommu_model = (
                self.config_widgets.get('iommu_model', {}).get()
                if hasattr(self.config_widgets.get('iommu_model'), 'get')
                else 'intel'
            )
            if iommu_model == 'none':
                return '<!-- iommu: none selected, element will be removed -->'

        # 生成 XML
        xml_lines = []

        if device_type == 'disk':
            xml_lines = self._generate_disk_xml()
        elif device_type == 'graphics':
            xml_lines = self._generate_graphics_xml()
        elif device_type == 'video':
            xml_lines = self._generate_video_xml()
        elif device_type == 'sound':
            xml_lines = self._generate_sound_xml()
        elif device_type == 'controller':
            xml_lines = self._generate_controller_xml()
        elif device_type == 'interface':
            xml_lines = self._generate_interface_xml()
        elif device_type == 'input':
            xml_lines = self._generate_input_xml()
        elif device_type == 'watchdog':
            xml_lines = self._generate_watchdog_xml()
        elif device_type == 'rng':
            xml_lines = self._generate_rng_xml()
        elif device_type == 'tpm':
            xml_lines = self._generate_tpm_xml()
        elif device_type == 'filesystem':
            xml_lines = self._generate_filesystem_xml()
        elif device_type == 'console':
            xml_lines = self._generate_console_xml()
        elif device_type == 'serial':
            xml_lines = self._generate_serial_xml()
        elif device_type == 'iommu':
            xml_lines = self._generate_iommu_xml()
        elif device_type == 'memory':
            xml_lines = self._generate_memory_xml()
        else:
            xml_lines = [f'<!-- {device_type} configuration not fully implemented -->']

        return '\n'.join(xml_lines) if xml_lines else f'<{device_type}/>'

    def _get_widget_value(self, name: str, default=None):
        """获取 widget 的值。"""
        widget = self.config_widgets.get(name)
        if widget:
            if hasattr(widget, 'get'):
                return widget.get()
            elif hasattr(widget, 'get'):
                return widget.get()
        return default

    def _generate_disk_xml(self) -> list:
        """生成磁盘设备 XML。"""
        disk_type = self._get_widget_value('disk_type', 'file')
        disk_device = self._get_widget_value('disk_device', 'disk')
        disk_bus = self._get_widget_value('disk_bus', 'virtio')
        disk_source = self._get_widget_value('disk_source', '')
        disk_driver = self._get_widget_value('disk_driver', 'qcow2')
        disk_target = self._get_widget_value('disk_target', 'vda')
        disk_readonly = self._get_widget_value('disk_readonly', False)
        disk_boot_order = self._get_widget_value('disk_boot_order', '')
        disk_startup = self._get_widget_value('disk_startup', 'none')

        if disk_type == 'none':
            return []

        xml = [f"<disk type='{disk_type}' device='{disk_device}'>"]

        if disk_driver and disk_driver != 'none' and disk_type == 'file':
            xml.append(f"  <driver name='qemu' type='{disk_driver}'/>")

        if disk_source:
            xml.append(f"  <source file='{disk_source}'/>")

        xml.append(f"  <target dev='{disk_target}' bus='{disk_bus}'/>")

        if disk_readonly:
            xml.append('  <readonly/>')

        if disk_boot_order:
            xml.append(f"  <boot order='{disk_boot_order}'/>")

        if disk_startup != 'none':
            xml.append(f"  <source startupPolicy='{disk_startup}'/>")

        xml.append('</disk>')
        return xml

    def _generate_graphics_xml(self) -> list:
        """生成图形显示 XML。"""
        gfx_type = self._get_widget_value('gfx_type', 'vnc')
        gfx_autoport = self._get_widget_value('gfx_autoport', True)
        gfx_port = self._get_widget_value('gfx_port', '-1')
        gfx_listen = self._get_widget_value('gfx_listen', '0.0.0.0')
        gfx_tls_port = self._get_widget_value('gfx_tls_port', '-1')
        gfx_passwd = self._get_widget_value('gfx_passwd', '')
        gfx_keymap = self._get_widget_value('gfx_keymap', 'en-us')
        gfx_share = self._get_widget_value('gfx_share', 'allow-exclusive')
        gfx_power = self._get_widget_value('gfx_power', False)

        if gfx_type == 'none':
            return []

        xml = [f"<graphics type='{gfx_type}'"]

        if gfx_autoport:
            xml[-1] += " autoport='yes'"
        else:
            xml[-1] += f" port='{gfx_port}'"

        xml[-1] += f" listen='{gfx_listen}'"

        if gfx_passwd:
            xml[-1] += f" passwd='{gfx_passwd}'"

        if gfx_keymap:
            xml[-1] += f" keymap='{gfx_keymap}'"

        if gfx_type == 'vnc' and gfx_share != 'none':
            xml[-1] += f" sharePolicy='{gfx_share}'"

        if gfx_type == 'vnc' and gfx_power:
            xml[-1] += " powerControl='on'"

        xml[-1] += '/>'

        # SPICE 额外配置
        if gfx_type == 'spice':
            if gfx_tls_port and gfx_tls_port != '-1':
                xml.append(f"<graphics type='spice' tlsPort='{gfx_tls_port}' autoport='yes'/>")

        return xml

    def _generate_video_xml(self) -> list:
        """生成视频设备 XML。"""
        video_model = self._get_widget_value('video_model', 'qxl')
        video_vram = self._get_widget_value('video_vram', '16384')
        video_heads = self._get_widget_value('video_heads', '1')
        video_accel3d = self._get_widget_value('video_accel3d', False)

        if video_model == 'none':
            return []

        xml = ['<video>']
        accel_attrs = " accel3d='yes'" if video_accel3d else ''
        xml.append(
            f"  <model type='{video_model}' vram='{video_vram}' heads='{video_heads}'{accel_attrs}/>"
        )
        xml.append('</video>')
        return xml

    def _generate_sound_xml(self) -> list:
        """生成音频设备 XML。"""
        sound_model = self._get_widget_value('sound_model', 'ich9')
        sound_codec = self._get_widget_value('sound_codec', 'duplex')

        if sound_model == 'none':
            return []

        xml = [f"<sound model='{sound_model}'>"]
        if sound_codec and sound_codec != 'none':
            xml.append(f"  <codec type='{sound_codec}'/>")
        xml.append('</sound>')
        return xml

    def _generate_controller_xml(self) -> list:
        """生成控制器 XML。"""
        ctrl_type = self._get_widget_value('ctrl_type', 'usb')
        ctrl_model = self._get_widget_value('ctrl_model', 'usb-xhci')
        ctrl_index = self._get_widget_value('ctrl_index', '0')
        # ctrl_queues reserved for future use

        if ctrl_model == 'none':
            return []

        xml = [f"<controller type='{ctrl_type}' index='{ctrl_index}' model='{ctrl_model}'/>"]
        return xml

    def _generate_interface_xml(self) -> list:
        """生成网络接口 XML。"""
        iface_type = self._get_widget_value('iface_type', 'network')
        iface_source = self._get_widget_value('iface_source', 'default')
        iface_model = self._get_widget_value('iface_model', 'virtio')
        iface_mac = self._get_widget_value('iface_mac', '')
        iface_boot = self._get_widget_value('iface_boot', '')

        if iface_type == 'none':
            return []

        xml = [f"<interface type='{iface_type}'>"]

        if iface_type == 'network':
            xml.append(f"  <source network='{iface_source}'/>")
        elif iface_type == 'bridge':
            xml.append(f"  <source bridge='{iface_source}'/>")
        elif iface_type == 'direct':
            xml.append(f"  <source dev='{iface_source}' mode='vepa'/>")

        if iface_mac:
            xml.append(f"  <mac address='{iface_mac}'/>")

        xml.append(f"  <model type='{iface_model}'/>")

        if iface_boot:
            xml.append(f"  <boot order='{iface_boot}'/>")

        xml.append('</interface>')
        return xml

    def _generate_input_xml(self) -> list:
        """生成输入设备 XML。"""
        input_type = self._get_widget_value('input_type', 'tablet')
        input_bus = self._get_widget_value('input_bus', 'usb')

        xml = [f"<input type='{input_type}' bus='{input_bus}'/>"]
        return xml

    def _generate_watchdog_xml(self) -> list:
        """生成看门狗 XML。"""
        watchdog_model = self._get_widget_value('watchdog_model', 'i6300esb')
        watchdog_action = self._get_widget_value('watchdog_action', 'reset')

        xml = [f"<watchdog model='{watchdog_model}' action='{watchdog_action}'/>"]
        return xml

    def _generate_rng_xml(self) -> list:
        """生成随机数发生器 XML。"""
        rng_model = self._get_widget_value('rng_model', 'virtio')
        rng_backend = self._get_widget_value('rng_backend', 'random')
        rng_source = self._get_widget_value('rng_source', '/dev/urandom')
        rng_rate = self._get_widget_value('rng_rate', '')

        xml = [f"<rng model='{rng_model}'>"]
        xml.append(f"  <backend model='{rng_backend}'>{rng_source}</backend>")
        if rng_rate:
            xml.append(f"  <rate period='1000' bytes='{rng_rate}'/>")
        xml.append('</rng>')
        return xml

    def _generate_tpm_xml(self) -> list:
        """生成 TPM 设备 XML。"""
        tpm_model = self._get_widget_value('tpm_model', 'tpm-tis')
        tpm_backend = self._get_widget_value('tpm_backend', 'emulator')
        tpm_device = self._get_widget_value('tpm_device', '/dev/tpm0')
        tpm_version = self._get_widget_value('tpm_version', '2.0')

        xml = [f"<tpm model='{tpm_model}'>"]
        xml.append(f"  <backend type='{tpm_backend}' version='{tpm_version}'>")
        xml.append(f"    <device path='{tpm_device}'/>")
        xml.append('  </backend>')
        xml.append('</tpm>')
        return xml

    def _generate_filesystem_xml(self) -> list:
        """生成文件系统 XML。"""
        fs_type = self._get_widget_value('fs_type', 'mount')
        fs_access = self._get_widget_value('fs_access', 'passthrough')
        fs_source = self._get_widget_value('fs_source', '/export/to/guest')
        fs_target = self._get_widget_value('fs_target', '/import/from/host')
        fs_readonly = self._get_widget_value('fs_readonly', False)

        xml = [f"<filesystem type='{fs_type}' accessmode='{fs_access}'>"]
        xml.append(f"  <source dir='{fs_source}'/>")
        xml.append(f"  <target dir='{fs_target}'/>")
        if fs_readonly:
            xml.append('  <readonly/>')
        xml.append('</filesystem>')
        return xml

    def _generate_console_xml(self) -> list:
        """生成控制台 XML。"""
        console_type = self._get_widget_value('console_type', 'pty')
        console_target = self._get_widget_value('console_target', 'virtio')

        xml = [f"<console type='{console_type}'>"]
        xml.append(f"  <target type='{console_target}'/>")
        xml.append('</console>')
        return xml

    def _generate_serial_xml(self) -> list:
        """生成串口 XML。"""
        serial_type = self._get_widget_value('serial_type', 'pty')
        serial_port = self._get_widget_value('serial_port', '0')
        serial_path = self._get_widget_value('serial_path', '')

        xml = [f"<serial type='{serial_type}'>"]
        xml.append(f"  <target port='{serial_port}'/>")
        if serial_path:
            xml.append(f"  <source path='{serial_path}'/>")
        xml.append('</serial>')
        return xml

    def _generate_iommu_xml(self) -> list:
        """生成 IOMMU XML。"""
        iommu_model = self._get_widget_value('iommu_model', 'intel')
        iommu_intremap = self._get_widget_value('iommu_intremap', False)
        iommu_caching = self._get_widget_value('iommu_caching', False)
        iommu_aw = self._get_widget_value('iommu_aw', '')

        xml = [f"<iommu model='{iommu_model}'>"]
        driver_attrs = []
        if iommu_intremap:
            driver_attrs.append("intremap='on'")
        if iommu_caching:
            driver_attrs.append("caching_mode='on'")
        if iommu_aw:
            driver_attrs.append(f"aw_bits='{iommu_aw}'")

        if driver_attrs:
            xml.append(f'  <driver {" ".join(driver_attrs)}/>')
        else:
            xml.append('  <driver/>')
        xml.append('</iommu>')
        return xml

    def _generate_memory_xml(self) -> list:
        """生成内存设备 XML。"""
        memory_model = self._get_widget_value('memory_model', 'dimm')
        memory_size = self._get_widget_value('memory_size', '524288')
        memory_node = self._get_widget_value('memory_node', '0')
        memory_access = self._get_widget_value('memory_access', 'private')

        xml = [f"<memory model='{memory_model}' access='{memory_access}'>"]
        xml.append('  <target>')
        xml.append(f"    <size unit='KiB'>{memory_size}</size>")
        xml.append(f'    <node>{memory_node}</node>')
        xml.append('  </target>')
        xml.append('</memory>')
        return xml

    # ===== 设备列表管理 =====
    def _add_device(self) -> None:
        """添加设备到列表。"""
        if not self.selected_device_type:
            return

        # 获取配置
        config = self._get_current_config()
        xml = self._generate_device_xml()

        device_info = {
            'type': self.selected_device_type,
            'label': self.DEVICE_TYPES.get(self.selected_device_type, self.selected_device_type),
            'config': config,
            'xml': xml,
        }

        self.devices_list.append(device_info)
        self._update_devices_list_display()
        self._trigger_change()

    def _get_current_config(self) -> dict:
        """获取当前配置。"""
        config = {}
        for name, widget in self.config_widgets.items():
            if hasattr(widget, 'get'):
                config[name] = widget.get()
        return config

    def _update_devices_list_display(self) -> None:
        """更新设备列表显示。"""
        # 清空列表
        for widget in self.devices_list_frame.winfo_children():
            widget.destroy()

        if not self.devices_list:
            label = ctk.CTkLabel(
                self.devices_list_frame,
                text='No devices added yet.',
                font=CTK_FONT_SMALL,
                text_color='#888888',
            )
            label.pack(padx=5, pady=10)
            return

        # 显示设备列表
        for i, device in enumerate(self.devices_list):
            device_frame = ctk.CTkFrame(
                self.devices_list_frame, fg_color='#3a3a3a', corner_radius=4
            )
            device_frame.pack(fill='x', padx=5, pady=2)

            label_text = f'{device["label"]}'
            ctk.CTkLabel(
                device_frame,
                text=label_text,
                font=CTK_FONT_SMALL,
            ).pack(side='left', padx=5, pady=3)

            # 编辑按钮
            edit_btn = ctk.CTkButton(
                device_frame,
                text='Edit',
                width=50,
                height=24,
                font=CTK_FONT_SMALL,
                command=lambda idx=i: self._edit_device(idx),
            )
            edit_btn.pack(side='right', padx=3)

            # 删除按钮
            del_btn = ctk.CTkButton(
                device_frame,
                text='Delete',
                width=50,
                height=24,
                font=CTK_FONT_SMALL,
                fg_color='#f44336',
                hover_color='#d32f2f',
                command=lambda idx=i: self._delete_device(idx),
            )
            del_btn.pack(side='right', padx=3)

    def _edit_device(self, index: int) -> None:
        """编辑设备。"""
        if 0 <= index < len(self.devices_list):
            device = self.devices_list[index]
            # 设置设备类型
            for key, label in self.DEVICE_TYPES.items():
                if key == device['type']:
                    self.device_type_menu.set(label)
                    self._on_device_type_change(label)
                    break
            # TODO: 加载配置到界面

    def _delete_device(self, index: int) -> None:
        """删除设备。"""
        if 0 <= index < len(self.devices_list):
            self.devices_list.pop(index)
            self._update_devices_list_display()
            self._trigger_change()

    def _clear_all_devices(self) -> None:
        """清空所有设备。"""
        self.devices_list.clear()
        self._update_devices_list_display()
        self._trigger_change()

    # ===== 配置变更回调 =====
    def _on_config_change(self) -> None:
        """配置变更时的处理。"""
        self._update_xml_preview()
        self._trigger_change()

    def get_config(self) -> dict:
        """获取配置（供父类调用）。"""
        return {
            'devices': self.devices_list,
        }

    def to_xml(self) -> dict:
        """生成 XML 配置字典。"""
        devices: dict[str, list[Any]] = {}
        for device in self.devices_list:
            device_type = device['type']
            if device_type not in devices:
                devices[device_type] = []
            devices[device_type].append(device['config'])

        return {'devices': devices}

    def _config_change(self) -> None:
        """配置变更通知。"""
        if self.on_change_callback:
            self.on_change_callback()
