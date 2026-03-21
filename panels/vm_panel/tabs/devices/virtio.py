"""Virtio设备模块 - Virtio相关配置."""

import customtkinter as ctk

from components.base_tab import BaseConfigTab
from utils.styles import BG_COLOR_CONTENT, CTK_FONT_MAIN, CTK_FONT_SMALL


class VirtioOptionsTab(BaseConfigTab):
    """Virtio相关选项配置 Tab - 支持Virtio相关选项配置."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, on_change_callback, **kwargs)

        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # 左侧面板
        left_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        left_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        left_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(left_frame, text='Virtio 选项', font=CTK_FONT_MAIN, text_color='#64b5f6').grid(
            row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
        )

        # virtio_ring
        ctk.CTkLabel(
            left_frame, text='Virtio Ring Size:', font=CTK_FONT_MAIN, width=120, anchor='w'
        ).grid(row=1, column=0, padx=10, pady=5, sticky='w')
        self.ring_size_entry = ctk.CTkEntry(left_frame, placeholder_text='256', width=100)
        self.ring_size_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.ring_size_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        # virtio_iommu_platform
        ctk.CTkLabel(
            left_frame, text='IOMMU Platform:', font=CTK_FONT_MAIN, width=120, anchor='w'
        ).grid(row=2, column=0, padx=10, pady=5, sticky='w')
        self.iommu_platform_var = ctk.StringVar(value='auto')
        iommu_frame = ctk.CTkFrame(left_frame, fg_color='transparent')
        iommu_frame.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        ctk.CTkRadioButton(
            iommu_frame,
            text='Auto',
            variable=self.iommu_platform_var,
            value='auto',
            command=self._trigger_change,
        ).pack(side='left', padx=5)
        ctk.CTkRadioButton(
            iommu_frame,
            text='On',
            variable=self.iommu_platform_var,
            value='on',
            command=self._trigger_change,
        ).pack(side='left', padx=5)
        ctk.CTkRadioButton(
            iommu_frame,
            text='Off',
            variable=self.iommu_platform_var,
            value='off',
            command=self._trigger_change,
        ).pack(side='left', padx=5)

        # virtio_transport
        ctk.CTkLabel(left_frame, text='Transport:', font=CTK_FONT_MAIN, width=120, anchor='w').grid(
            row=3, column=0, padx=10, pady=5, sticky='w'
        )
        self.transport_menu = ctk.CTkOptionMenu(
            left_frame,
            values=['auto', 'pci', 'mmio'],
            width=100,
            font=CTK_FONT_SMALL,
        )
        self.transport_menu.set('auto')
        self.transport_menu.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        self.transport_menu.configure(command=self._trigger_change)

        # 右侧面板
        right_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        right_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        right_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            right_frame, text='Virtio 性能选项', font=CTK_FONT_MAIN, text_color='#4caf50'
        ).grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w')

        # virtio_native_io
        self.native_io_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            right_frame, text='Native IO', variable=self.native_io_var, command=self._trigger_change
        ).grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky='w')

        # virtio_no_mrg_rx_buf
        self.no_mrg_rx_buf_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            right_frame,
            text='No MRG RX Buffer',
            variable=self.no_mrg_rx_buf_var,
            command=self._trigger_change,
        ).grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky='w')

        # virtio_blk_discard
        self.blk_discard_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(
            right_frame,
            text='Block Discard',
            variable=self.blk_discard_var,
            command=self._trigger_change,
        ).grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky='w')

        # virtio_blk_write_zeroes
        self.blk_write_zeroes_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(
            right_frame,
            text='Block Write Zeroes',
            variable=self.blk_write_zeroes_var,
            command=self._trigger_change,
        ).grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky='w')

    def get_config(self) -> dict:
        """获取配置."""
        return {
            'type': 'virtio_options',
            'ring_size': self.ring_size_entry.get().strip(),
            'iommu_platform': self.iommu_platform_var.get(),
            'transport': self.transport_menu.get(),
            'native_io': self.native_io_var.get(),
            'no_mrg_rx_buf': self.no_mrg_rx_buf_var.get(),
            'blk_discard': self.blk_discard_var.get(),
            'blk_write_zeroes': self.blk_write_zeroes_var.get(),
        }

    def load_config(self, config: dict) -> None:
        """加载配置."""
        if 'ring_size' in config:
            self.ring_size_entry.delete(0, 'end')
            self.ring_size_entry.insert(0, config['ring_size'])
        if 'iommu_platform' in config:
            self.iommu_platform_var.set(config['iommu_platform'])
        if 'transport' in config:
            self.transport_menu.set(config['transport'])
        if 'native_io' in config:
            self.native_io_var.set(config['native_io'])
        if 'no_mrg_rx_buf' in config:
            self.no_mrg_rx_buf_var.set(config['no_mrg_rx_buf'])
        if 'blk_discard' in config:
            self.blk_discard_var.set(config['blk_discard'])
        if 'blk_write_zeroes' in config:
            self.blk_write_zeroes_var.set(config['blk_write_zeroes'])


class VirtioDeviceModelsTab(BaseConfigTab):
    """Virtio设备模型配置 Tab - 支持Virtio设备模型配置."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, on_change_callback, **kwargs)

        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # 左侧面板 - 网络设备
        left_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        left_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        left_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            left_frame, text='网络设备模型', font=CTK_FONT_MAIN, text_color='#64b5f6'
        ).grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w')

        ctk.CTkLabel(left_frame, text='NIC Model:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.nic_model_menu = ctk.CTkOptionMenu(
            left_frame,
            values=[
                'virtio',
                'virtio-net-pci',
                'virtio-net-mmio',
                'e1000',
                'e1000e',
                'rtl8139',
                'pcnet',
            ],
            width=150,
            font=CTK_FONT_SMALL,
        )
        self.nic_model_menu.set('virtio')
        self.nic_model_menu.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.nic_model_menu.configure(command=self._trigger_change)

        # 右侧面板 - 块设备
        right_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        right_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        right_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(right_frame, text='块设备模型', font=CTK_FONT_MAIN, text_color='#4caf50').grid(
            row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
        )

        ctk.CTkLabel(
            right_frame, text='Disk Model:', font=CTK_FONT_MAIN, width=100, anchor='w'
        ).grid(row=1, column=0, padx=10, pady=5, sticky='w')
        self.disk_model_menu = ctk.CTkOptionMenu(
            right_frame,
            values=['virtio', 'virtio-blk-pci', 'virtio-blk-mmio', 'ide', 'scsi', 'sata'],
            width=150,
            font=CTK_FONT_SMALL,
        )
        self.disk_model_menu.set('virtio')
        self.disk_model_menu.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.disk_model_menu.configure(command=self._trigger_change)

        # 底部面板 - 其他设备
        bottom_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        bottom_frame.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=5, pady=5)
        bottom_frame.grid_columnconfigure(1, weight=1)
        bottom_frame.grid_columnconfigure(3, weight=1)

        ctk.CTkLabel(
            bottom_frame, text='其他设备模型', font=CTK_FONT_MAIN, text_color='#ff9800'
        ).grid(row=0, column=0, columnspan=4, padx=10, pady=5, sticky='w')

        # 控制台设备
        ctk.CTkLabel(
            bottom_frame, text='Console Model:', font=CTK_FONT_MAIN, width=120, anchor='w'
        ).grid(row=1, column=0, padx=10, pady=5, sticky='w')
        self.console_model_menu = ctk.CTkOptionMenu(
            bottom_frame,
            values=['virtio', 'virtio-console-pci', 'virtio-console-mmio', 'serial'],
            width=150,
            font=CTK_FONT_SMALL,
        )
        self.console_model_menu.set('virtio')
        self.console_model_menu.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.console_model_menu.configure(command=self._trigger_change)

        # 串口设备
        ctk.CTkLabel(
            bottom_frame, text='Serial Model:', font=CTK_FONT_MAIN, width=120, anchor='w'
        ).grid(row=1, column=2, padx=10, pady=5, sticky='w')
        self.serial_model_menu = ctk.CTkOptionMenu(
            bottom_frame,
            values=['virtio', 'virtio-serial-pci', 'virtio-serial-mmio', 'serial'],
            width=150,
            font=CTK_FONT_SMALL,
        )
        self.serial_model_menu.set('serial')
        self.serial_model_menu.grid(row=1, column=3, padx=5, pady=5, sticky='w')
        self.serial_model_menu.configure(command=self._trigger_change)

        # 输入设备
        ctk.CTkLabel(
            bottom_frame, text='Input Model:', font=CTK_FONT_MAIN, width=120, anchor='w'
        ).grid(row=2, column=0, padx=10, pady=5, sticky='w')
        self.input_model_menu = ctk.CTkOptionMenu(
            bottom_frame,
            values=['virtio', 'virtio-input-pci', 'virtio-input-mmio', 'ps2'],
            width=150,
            font=CTK_FONT_SMALL,
        )
        self.input_model_menu.set('ps2')
        self.input_model_menu.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.input_model_menu.configure(command=self._trigger_change)

        # 球oon设备
        ctk.CTkLabel(
            bottom_frame, text='Balloon Model:', font=CTK_FONT_MAIN, width=120, anchor='w'
        ).grid(row=2, column=2, padx=10, pady=5, sticky='w')
        self.balloon_model_menu = ctk.CTkOptionMenu(
            bottom_frame,
            values=['virtio', 'virtio-balloon-pci', 'virtio-balloon-mmio'],
            width=150,
            font=CTK_FONT_SMALL,
        )
        self.balloon_model_menu.set('virtio')
        self.balloon_model_menu.grid(row=2, column=3, padx=5, pady=5, sticky='w')
        self.balloon_model_menu.configure(command=self._trigger_change)

    def get_config(self) -> dict:
        """获取配置."""
        return {
            'type': 'virtio_device_models',
            'nic_model': self.nic_model_menu.get(),
            'disk_model': self.disk_model_menu.get(),
            'console_model': self.console_model_menu.get(),
            'serial_model': self.serial_model_menu.get(),
            'input_model': self.input_model_menu.get(),
            'balloon_model': self.balloon_model_menu.get(),
        }

    def load_config(self, config: dict) -> None:
        """加载配置."""
        if 'nic_model' in config:
            self.nic_model_menu.set(config['nic_model'])
        if 'disk_model' in config:
            self.disk_model_menu.set(config['disk_model'])
        if 'console_model' in config:
            self.console_model_menu.set(config['console_model'])
        if 'serial_model' in config:
            self.serial_model_menu.set(config['serial_model'])
        if 'input_model' in config:
            self.input_model_menu.set(config['input_model'])
        if 'balloon_model' in config:
            self.balloon_model_menu.set(config['balloon_model'])
