"""设备直通模块 - USB、PCI、SCSI、MDEV 设备直通配置."""

import customtkinter as ctk

from components.base_tab import BaseConfigTab
from utils.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class USBHostdevTab(BaseConfigTab):
    """USB 设备直通配置."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, on_change_callback, **kwargs)
        self.usb_list = []

        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            frame, text='USB Device Passthrough', font=CTK_FONT_BOLD, text_color='#2196f3'
        ).grid(row=0, column=0, columnspan=4, padx=10, pady=5, sticky='w')

        # USB Controller
        ctk.CTkLabel(frame, text='Controller:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.usb_controller = ctk.CTkOptionMenu(
            frame,
            values=[
                'qemu-xhci',
                'piix3-uhci',
                'piix4-uhci',
                'nec-xhci',
                'vt82c686b-uhci',
                'ich9-ehci1',
                'none',
            ],
            width=150,
            font=CTK_FONT_SMALL,
        )
        self.usb_controller.set('qemu-xhci')
        self.usb_controller.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.usb_controller.configure(command=self._trigger_change)

        # 添加 USB 设备输入
        ctk.CTkLabel(frame, text='Vendor:Product:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=2, padx=10, pady=5, sticky='w'
        )
        self.usb_entry = ctk.CTkEntry(
            frame, placeholder_text='8087:8008', width=150, font=CTK_FONT_SMALL
        )
        self.usb_entry.grid(row=1, column=3, padx=5, pady=5, sticky='w')
        self.usb_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        # Startup Policy
        ctk.CTkLabel(frame, text='Startup Policy:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.startup_policy = ctk.CTkOptionMenu(
            frame,
            values=['required', 'optional'],
            width=100,
            font=CTK_FONT_SMALL,
        )
        self.startup_policy.set('optional')
        self.startup_policy.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.startup_policy.configure(command=self._trigger_change)

        # Guest Reset
        ctk.CTkLabel(frame, text='Guest Reset:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=2, column=2, padx=10, pady=5, sticky='w'
        )
        self.guest_reset = ctk.CTkCheckBox(frame, text='Enable', font=CTK_FONT_SMALL)
        self.guest_reset.grid(row=2, column=3, padx=5, pady=5, sticky='w')
        self.guest_reset.configure(command=self._trigger_change)

        # Device List
        self.usb_display = ctk.CTkLabel(
            frame, text='', font=CTK_FONT_SMALL, text_color='#aaaaaa', anchor='w'
        )
        self.usb_display.grid(row=3, column=0, columnspan=4, padx=10, pady=10, sticky='w')

        # 按钮
        btn_frame = ctk.CTkFrame(frame, fg_color='transparent')
        btn_frame.grid(row=4, column=0, columnspan=4, padx=10, pady=5, sticky='w')

        add_btn = ctk.CTkButton(
            btn_frame,
            text='Add Device',
            command=self._add_usb_device,
            fg_color='#00bcd4',
            hover_color='#0097a7',
            width=100,
            font=CTK_FONT_SMALL,
        )
        add_btn.grid(row=0, column=0, padx=5)

        clear_btn = ctk.CTkButton(
            btn_frame,
            text='Clear List',
            command=self._clear_usb_list,
            fg_color='#f44336',
            hover_color='#d32f2f',
            width=100,
            font=CTK_FONT_SMALL,
        )
        clear_btn.grid(row=0, column=1, padx=5)

    def _add_usb_device(self):
        """Add USB device."""
        from tkinter import messagebox

        usb_id = self.usb_entry.get().strip()
        if not usb_id:
            messagebox.showwarning('Warning', 'Please enter USB device ID!')
            return
        if ':' not in usb_id:
            messagebox.showwarning('Warning', 'Format should be Vendor:Product (e.g. 8087:8008)!')
            return
        self.usb_list.append(usb_id)
        self._update_display()
        self.usb_entry.delete(0, 'end')
        self._trigger_change()

    def _clear_usb_list(self):
        """清空 USB 设备列表."""
        self.usb_list.clear()
        self._update_display()
        self._trigger_change()

    def _update_display(self):
        """更新显示."""
        if self.usb_list:
            self.usb_display.configure(text=f'已添加:{", ".join(self.usb_list)}')
        else:
            self.usb_display.configure(text='暂无设备')

    def get_config(self) -> dict:
        """获取配置."""
        return {
            'type': 'usb',
            'controller': self.usb_controller.get(),
            'startup_policy': self.startup_policy.get(),
            'guest_reset': self.guest_reset.get(),
            'devices': self.usb_list.copy(),
        }


class PCIHostdevTab(BaseConfigTab):
    """PCI 设备直通配置."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, on_change_callback, **kwargs)
        self.pci_list = []

        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            frame, text='PCI Device Passthrough', font=CTK_FONT_BOLD, text_color='#4caf50'
        ).grid(row=0, column=0, columnspan=5, padx=10, pady=5, sticky='w')

        # Domain
        ctk.CTkLabel(frame, text='Domain:', font=CTK_FONT_MAIN, width=70, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.pci_domain = ctk.CTkEntry(frame, width=80, font=CTK_FONT_SMALL)
        self.pci_domain.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.pci_domain.insert(0, '0x0000')
        self.pci_domain.bind('<KeyRelease>', lambda e: self._trigger_change())

        # Bus
        ctk.CTkLabel(frame, text='Bus:', font=CTK_FONT_MAIN, width=50, anchor='w').grid(
            row=1, column=2, padx=5, pady=5, sticky='w'
        )
        self.pci_bus = ctk.CTkEntry(frame, width=80, font=CTK_FONT_SMALL)
        self.pci_bus.grid(row=1, column=3, padx=5, pady=5, sticky='w')
        self.pci_bus.insert(0, '0x00')
        self.pci_bus.bind('<KeyRelease>', lambda e: self._trigger_change())

        # Slot
        ctk.CTkLabel(frame, text='Slot:', font=CTK_FONT_MAIN, width=50, anchor='w').grid(
            row=1, column=4, padx=5, pady=5, sticky='w'
        )
        self.pci_slot = ctk.CTkEntry(frame, width=80, font=CTK_FONT_SMALL)
        self.pci_slot.grid(row=1, column=5, padx=5, pady=5, sticky='w')
        self.pci_slot.insert(0, '0x00')
        self.pci_slot.bind('<KeyRelease>', lambda e: self._trigger_change())

        # Function
        ctk.CTkLabel(frame, text='Function:', font=CTK_FONT_MAIN, width=70, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.pci_function = ctk.CTkEntry(frame, width=80, font=CTK_FONT_SMALL)
        self.pci_function.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.pci_function.insert(0, '0x0')
        self.pci_function.bind('<KeyRelease>', lambda e: self._trigger_change())

        # Managed
        ctk.CTkLabel(frame, text='Managed:', font=CTK_FONT_MAIN, width=70, anchor='w').grid(
            row=2, column=2, padx=10, pady=5, sticky='w'
        )
        self.pci_managed = ctk.CTkOptionMenu(
            frame, values=['yes', 'no'], width=80, font=CTK_FONT_SMALL
        )
        self.pci_managed.set('yes')
        self.pci_managed.grid(row=2, column=3, padx=5, pady=5, sticky='w')
        self.pci_managed.configure(command=self._trigger_change)

        # Boot order
        ctk.CTkLabel(frame, text='Boot:', font=CTK_FONT_MAIN, width=50, anchor='w').grid(
            row=2, column=4, padx=5, pady=5, sticky='w'
        )
        self.pci_boot_order = ctk.CTkEntry(frame, width=60, font=CTK_FONT_SMALL)
        self.pci_boot_order.grid(row=2, column=5, padx=5, pady=5, sticky='w')
        self.pci_boot_order.insert(0, '1')
        self.pci_boot_order.bind('<KeyRelease>', lambda e: self._trigger_change())

        # ROM BAR
        ctk.CTkLabel(frame, text='ROM BAR:', font=CTK_FONT_MAIN, width=70, anchor='w').grid(
            row=3, column=0, padx=10, pady=5, sticky='w'
        )
        self.rom_bar = ctk.CTkOptionMenu(frame, values=['on', 'off'], width=80, font=CTK_FONT_SMALL)
        self.rom_bar.set('off')
        self.rom_bar.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        self.rom_bar.configure(command=self._trigger_change)

        ctk.CTkLabel(frame, text='ROM File:', font=CTK_FONT_MAIN, width=70, anchor='w').grid(
            row=3, column=2, padx=5, pady=5, sticky='w'
        )
        self.rom_file = ctk.CTkEntry(frame, placeholder_text='/path/to/boot.bin', width=200)
        self.rom_file.grid(row=3, column=3, columnspan=2, padx=5, pady=5, sticky='w')
        self.rom_file.bind('<KeyRelease>', lambda e: self._trigger_change())

        # 设备列表
        self.pci_display = ctk.CTkLabel(
            frame, text='', font=CTK_FONT_SMALL, text_color='#aaaaaa', anchor='w'
        )
        self.pci_display.grid(row=4, column=0, columnspan=6, padx=10, pady=10, sticky='w')

        # 按钮
        btn_frame = ctk.CTkFrame(frame, fg_color='transparent')
        btn_frame.grid(row=5, column=0, columnspan=6, padx=10, pady=5, sticky='w')

        add_btn = ctk.CTkButton(
            btn_frame,
            text='Add Device',
            command=self._add_pci_device,
            fg_color='#00bcd4',
            hover_color='#0097a7',
            width=100,
            font=CTK_FONT_SMALL,
        )
        add_btn.grid(row=0, column=0, padx=5)

        clear_btn = ctk.CTkButton(
            btn_frame,
            text='Clear List',
            command=self._clear_pci_list,
            fg_color='#f44336',
            hover_color='#d32f2f',
            width=100,
            font=CTK_FONT_SMALL,
        )
        clear_btn.grid(row=0, column=1, padx=5)

    def _add_pci_device(self):
        """Add PCI device."""
        from tkinter import messagebox

        device = {
            'domain': self.pci_domain.get().strip(),
            'bus': self.pci_bus.get().strip(),
            'slot': self.pci_slot.get().strip(),
            'function': self.pci_function.get().strip(),
        }
        if not all(device.values()):
            messagebox.showwarning('Warning', 'Please fill in the complete PCI address!')
            return
        self.pci_list.append(device)
        self._update_display()
        self._trigger_change()

    def _clear_pci_list(self):
        """清空 PCI 设备列表."""
        self.pci_list.clear()
        self._update_display()
        self._trigger_change()

    def _update_display(self):
        """更新显示."""
        if self.pci_list:
            devs = [f'{d["domain"]}:{d["bus"]}:{d["slot"]}.{d["function"]}' for d in self.pci_list]
            self.pci_display.configure(text=f'已添加:{", ".join(devs)}')
        else:
            self.pci_display.configure(text='暂无设备')

    def get_config(self) -> dict:
        """获取配置."""
        return {
            'type': 'pci',
            'devices': self.pci_list.copy(),
            'managed': self.pci_managed.get(),
            'boot_order': self.pci_boot_order.get().strip() or '1',
            'rom_bar': self.rom_bar.get(),
            'rom_file': self.rom_file.get().strip(),
        }


class SCSIHostdevTab(BaseConfigTab):
    """SCSI 设备直通配置."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, on_change_callback, **kwargs)
        self.scsi_list = []

        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # SCSI 类型选择
        type_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        type_frame.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
        type_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(type_frame, text='SCSI 类型:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=0, column=0, padx=10, pady=5, sticky='w'
        )
        self.scsi_type = ctk.CTkOptionMenu(
            type_frame,
            values=['scsi', 'scsi_host'],
            width=120,
            font=CTK_FONT_SMALL,
        )
        self.scsi_type.set('scsi')
        self.scsi_type.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        self.scsi_type.configure(command=self._on_type_change)

        # 内容区域(动态切换)
        self.content_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.content_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
        self.content_frame.grid_columnconfigure(0, weight=1)

        self._init_scsi_ui()

    def _init_scsi_ui(self):
        """初始化 SCSI 配置 UI."""
        # 清空现有内容
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        scsi_type = self.scsi_type.get()

        if scsi_type == 'scsi_host':
            # VHost SCSI
            frame = ctk.CTkFrame(self.content_frame, fg_color=BG_COLOR_CONTENT, corner_radius=6)
            frame.grid(row=0, column=0, sticky='nsew')
            frame.grid_columnconfigure(1, weight=1)

            ctk.CTkLabel(
                frame, text='VHost SCSI Configuration', font=CTK_FONT_BOLD, text_color='#ff9800'
            ).grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky='w')

            ctk.CTkLabel(frame, text='Protocol:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
                row=1, column=0, padx=10, pady=5, sticky='w'
            )
            self.vhost_protocol = ctk.CTkOptionMenu(
                frame, values=['vhost'], width=100, font=CTK_FONT_SMALL
            )
            self.vhost_protocol.set('vhost')
            self.vhost_protocol.grid(row=1, column=1, padx=5, pady=5, sticky='w')
            self.vhost_protocol.configure(command=self._trigger_change)

            ctk.CTkLabel(frame, text='WWPN:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
                row=1, column=2, padx=10, pady=5, sticky='w'
            )
            self.wwpn = ctk.CTkEntry(frame, placeholder_text='naa.50014057667280d8', width=200)
            self.wwpn.grid(row=1, column=3, padx=5, pady=5, sticky='w')
            self.wwpn.bind('<KeyRelease>', lambda e: self._trigger_change())
        else:
            # 普通 SCSI 或 iSCSI
            frame = ctk.CTkFrame(self.content_frame, fg_color=BG_COLOR_CONTENT, corner_radius=6)
            frame.grid(row=0, column=0, sticky='nsew')
            frame.grid_columnconfigure(1, weight=1)

            ctk.CTkLabel(
                frame, text='SCSI Device Configuration', font=CTK_FONT_BOLD, text_color='#ff9800'
            ).grid(row=0, column=0, columnspan=4, padx=10, pady=5, sticky='w')

            # SCSI Subtype
            self.scsi_subtype = ctk.CTkOptionMenu(
                frame,
                values=['local', 'iscsi'],
                width=100,
                font=CTK_FONT_SMALL,
                command=self._on_subtype_change,
            )
            self.scsi_subtype.set('local')
            ctk.CTkLabel(
                frame, text='SCSI Subtype:', font=CTK_FONT_MAIN, width=100, anchor='w'
            ).grid(row=1, column=0, padx=10, pady=5, sticky='w')
            self.scsi_subtype.grid(row=1, column=1, padx=5, pady=5, sticky='w')

            self._init_local_scsi_ui(frame)

        # 设备列表显示
        self.scsi_display = ctk.CTkLabel(
            self.content_frame, text='', font=CTK_FONT_SMALL, text_color='#aaaaaa', anchor='w'
        )
        self.scsi_display.grid(row=1, column=0, sticky='ew', padx=10, pady=10)

        # 按钮
        btn_frame = ctk.CTkFrame(self.content_frame, fg_color='transparent')
        btn_frame.grid(row=2, column=0, sticky='w', padx=10, pady=5)

        add_btn = ctk.CTkButton(
            btn_frame,
            text='Add Device',
            command=self._add_scsi_device,
            fg_color='#00bcd4',
            hover_color='#0097a7',
            width=100,
            font=CTK_FONT_SMALL,
        )
        add_btn.grid(row=0, column=0, padx=5)

        clear_btn = ctk.CTkButton(
            btn_frame,
            text='Clear List',
            command=self._clear_scsi_list,
            fg_color='#f44336',
            hover_color='#d32f2f',
            width=100,
            font=CTK_FONT_SMALL,
        )
        clear_btn.grid(row=0, column=1, padx=5)

    def _init_local_scsi_ui(self, frame):
        """初始化本地 SCSI UI."""
        # 清除 iSCSI 相关 UI
        for widget in frame.winfo_children():
            if widget.grid_info().get('row', 0) > 1:
                widget.destroy()

        ctk.CTkLabel(frame, text='Adapter:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.adapter_name = ctk.CTkEntry(frame, placeholder_text='scsi_host0', width=150)
        self.adapter_name.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.adapter_name.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(frame, text='Bus:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=2, column=2, padx=10, pady=5, sticky='w'
        )
        self.scsi_bus = ctk.CTkEntry(frame, width=60, font=CTK_FONT_SMALL)
        self.scsi_bus.grid(row=2, column=3, padx=5, pady=5, sticky='w')
        self.scsi_bus.insert(0, '0')
        self.scsi_bus.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(frame, text='Target:', font=CTK_FONT_MAIN, width=60, anchor='w').grid(
            row=3, column=0, padx=10, pady=5, sticky='w'
        )
        self.scsi_target = ctk.CTkEntry(frame, width=60, font=CTK_FONT_SMALL)
        self.scsi_target.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        self.scsi_target.insert(0, '0')
        self.scsi_target.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(frame, text='Unit:', font=CTK_FONT_MAIN, width=60, anchor='w').grid(
            row=3, column=2, padx=10, pady=5, sticky='w'
        )
        self.scsi_unit = ctk.CTkEntry(frame, width=60, font=CTK_FONT_SMALL)
        self.scsi_unit.grid(row=3, column=3, padx=5, pady=5, sticky='w')
        self.scsi_unit.insert(0, '0')
        self.scsi_unit.bind('<KeyRelease>', lambda e: self._trigger_change())

        # Read-only
        self.readonly = ctk.CTkCheckBox(frame, text='Read-only', font=CTK_FONT_SMALL)
        self.readonly.grid(row=3, column=4, padx=10, pady=5, sticky='w')
        self.readonly.configure(command=self._trigger_change)

    def _init_iscsi_scsi_ui(self, frame):
        """初始化 iSCSI SCSI UI."""
        # 清除本地 SCSI UI
        for widget in frame.winfo_children():
            if widget.grid_info().get('row', 0) > 1:
                widget.destroy()

        ctk.CTkLabel(frame, text='IQN:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.iscsi_iqn = ctk.CTkEntry(
            frame, placeholder_text='iqn.2014-08.com.example:iscsi-nopool/1', width=300
        )
        self.iscsi_iqn.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky='w')
        self.iscsi_iqn.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(frame, text='Host:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=3, column=0, padx=10, pady=5, sticky='w'
        )
        self.iscsi_host = ctk.CTkEntry(frame, placeholder_text='example.com', width=150)
        self.iscsi_host.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        self.iscsi_host.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(frame, text='Port:', font=CTK_FONT_MAIN, width=60, anchor='w').grid(
            row=3, column=2, padx=5, pady=5, sticky='w'
        )
        self.iscsi_port = ctk.CTkEntry(frame, width=60, font=CTK_FONT_SMALL)
        self.iscsi_port.grid(row=3, column=3, padx=5, pady=5, sticky='w')
        self.iscsi_port.insert(0, '3260')
        self.iscsi_port.bind('<KeyRelease>', lambda e: self._trigger_change())

        # Authentication
        ctk.CTkLabel(frame, text='Authentication:', font=CTK_FONT_MAIN, width=60, anchor='w').grid(
            row=4, column=0, padx=10, pady=5, sticky='w'
        )
        self.iscsi_auth = ctk.CTkCheckBox(
            frame, text='Enable CHAP Authentication', font=CTK_FONT_SMALL
        )
        self.iscsi_auth.grid(row=4, column=1, padx=5, pady=5, sticky='w')
        self.iscsi_auth.configure(command=self._trigger_change)

        ctk.CTkLabel(frame, text='Username:', font=CTK_FONT_MAIN, width=60, anchor='w').grid(
            row=4, column=2, padx=5, pady=5, sticky='w'
        )
        self.iscsi_username = ctk.CTkEntry(frame, placeholder_text='myuser', width=100)
        self.iscsi_username.grid(row=4, column=3, padx=5, pady=5, sticky='w')
        self.iscsi_username.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(frame, text='Secret:', font=CTK_FONT_MAIN, width=60, anchor='w').grid(
            row=4, column=4, padx=5, pady=5, sticky='w'
        )
        self.iscsi_secret = ctk.CTkEntry(frame, placeholder_text='libvirtiscsi', width=120)
        self.iscsi_secret.grid(row=4, column=5, padx=5, pady=5, sticky='w')
        self.iscsi_secret.bind('<KeyRelease>', lambda e: self._trigger_change())

    def _on_type_change(self, *args):
        """类型变化."""
        self._init_scsi_ui()
        self._trigger_change()

    def _on_subtype_change(self, *args):
        """子类型变化."""
        frame = self.content_frame.winfo_children()[0]
        if self.scsi_subtype.get() == 'iscsi':
            self._init_iscsi_scsi_ui(frame)
        else:
            self._init_local_scsi_ui(frame)
        self._trigger_change()

    def _add_scsi_device(self):
        """添加 SCSI 设备."""
        from tkinter import messagebox

        scsi_type = self.scsi_type.get()
        if scsi_type == 'scsi_host':
            wwpn = self.wwpn.get().strip()
            if not wwpn:
                messagebox.showwarning('警告', '请输入 WWPN!')
                return
            self.scsi_list.append({'type': 'scsi_host', 'protocol': 'vhost', 'wwpn': wwpn})
        else:
            if self.scsi_subtype.get() == 'iscsi':
                iqn = self.iscsi_iqn.get().strip()
                if not iqn:
                    messagebox.showwarning('警告', '请输入 IQN!')
                    return
                device = {
                    'type': 'scsi',
                    'protocol': 'iscsi',
                    'name': iqn,
                    'host': self.iscsi_host.get().strip(),
                    'port': self.iscsi_port.get().strip() or '3260',
                }
                if self.iscsi_auth.get():
                    device['auth'] = {
                        'username': self.iscsi_username.get().strip(),
                        'secret': self.iscsi_secret.get().strip(),
                    }
                self.scsi_list.append(device)
            else:
                adapter = self.adapter_name.get().strip()
                if not adapter:
                    messagebox.showwarning('警告', '请输入 Adapter 名称!')
                    return
                device = {
                    'type': 'scsi',
                    'adapter': adapter,
                    'bus': self.scsi_bus.get().strip() or '0',
                    'target': self.scsi_target.get().strip() or '0',
                    'unit': self.scsi_unit.get().strip() or '0',
                    'readonly': self.readonly.get(),
                }
                self.scsi_list.append(device)

        self._update_display()
        self._trigger_change()

    def _clear_scsi_list(self):
        """清空 SCSI 设备列表."""
        self.scsi_list.clear()
        self._update_display()
        self._trigger_change()

    def _update_display(self):
        """更新显示."""
        if self.scsi_list:
            devs = []
            for d in self.scsi_list:
                if d['type'] == 'scsi_host':
                    devs.append(f'vhost:{d["wwpn"]}')
                elif d.get('protocol') == 'iscsi':
                    devs.append(f'iscsi:{d["name"]}')
                else:
                    devs.append(f'{d["adapter"]}:{d["bus"]}:{d["target"]}.{d["unit"]}')
            self.scsi_display.configure(text=f'已添加:{", ".join(devs)}')
        else:
            self.scsi_display.configure(text='暂无设备')

    def get_config(self) -> dict:
        """获取配置."""
        return {
            'type': self.scsi_type.get(),
            'devices': self.scsi_list.copy(),
        }


class MdevHostdevTab(BaseConfigTab):
    """MDEV 设备直通配置."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, on_change_callback, **kwargs)
        self.mdev_list = []

        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            frame, text='MDEV Device Passthrough', font=CTK_FONT_BOLD, text_color='#9c27b0'
        ).grid(row=0, column=0, columnspan=4, padx=10, pady=5, sticky='w')

        # UUID
        ctk.CTkLabel(frame, text='UUID:', font=CTK_FONT_MAIN, width=70, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.mdev_uuid = ctk.CTkEntry(
            frame, placeholder_text='c2177883-f1bb-47f0-914d-32a22e3a8804', width=300
        )
        self.mdev_uuid.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.mdev_uuid.bind('<KeyRelease>', lambda e: self._trigger_change())

        # Model
        ctk.CTkLabel(frame, text='Model:', font=CTK_FONT_MAIN, width=70, anchor='w').grid(
            row=1, column=2, padx=10, pady=5, sticky='w'
        )
        self.mdev_model = ctk.CTkOptionMenu(
            frame,
            values=['vfio-pci', 'vfio-ccw', 'vfio-ap'],
            width=120,
            font=CTK_FONT_SMALL,
        )
        self.mdev_model.set('vfio-pci')
        self.mdev_model.grid(row=1, column=3, padx=5, pady=5, sticky='w')
        self.mdev_model.configure(command=self._trigger_change)

        # CCW Address (vfio-ccw only)
        self.ccw_frame = ctk.CTkFrame(frame, fg_color='transparent')
        self.ccw_frame.grid(row=2, column=0, columnspan=4, padx=10, pady=5, sticky='w')

        ctk.CTkLabel(self.ccw_frame, text='CCW:', font=CTK_FONT_MAIN, width=50, anchor='w').grid(
            row=0, column=0, padx=5, pady=5, sticky='w'
        )
        self.ccw_cssid = ctk.CTkEntry(self.ccw_frame, placeholder_text='0xfe', width=60)
        self.ccw_cssid.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        self.ccw_cssid.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(self.ccw_frame, text='SSID:', font=CTK_FONT_MAIN, width=50, anchor='w').grid(
            row=0, column=2, padx=5, pady=5, sticky='w'
        )
        self.ccw_ssid = ctk.CTkEntry(self.ccw_frame, placeholder_text='0x0', width=60)
        self.ccw_ssid.grid(row=0, column=3, padx=5, pady=5, sticky='w')
        self.ccw_ssid.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(self.ccw_frame, text='DevNo:', font=CTK_FONT_MAIN, width=50, anchor='w').grid(
            row=0, column=4, padx=5, pady=5, sticky='w'
        )
        self.ccw_devno = ctk.CTkEntry(self.ccw_frame, placeholder_text='0x0001', width=80)
        self.ccw_devno.grid(row=0, column=5, padx=5, pady=5, sticky='w')
        self.ccw_devno.bind('<KeyRelease>', lambda e: self._trigger_change())

        # Device List
        self.mdev_display = ctk.CTkLabel(
            frame, text='', font=CTK_FONT_SMALL, text_color='#aaaaaa', anchor='w'
        )
        self.mdev_display.grid(row=3, column=0, columnspan=4, padx=10, pady=10, sticky='w')

        # 按钮
        btn_frame = ctk.CTkFrame(frame, fg_color='transparent')
        btn_frame.grid(row=4, column=0, columnspan=4, padx=10, pady=5, sticky='w')

        add_btn = ctk.CTkButton(
            btn_frame,
            text='Add Device',
            command=self._add_mdev_device,
            fg_color='#00bcd4',
            hover_color='#0097a7',
            width=100,
            font=CTK_FONT_SMALL,
        )
        add_btn.grid(row=0, column=0, padx=5)

        clear_btn = ctk.CTkButton(
            btn_frame,
            text='Clear List',
            command=self._clear_mdev_list,
            fg_color='#f44336',
            hover_color='#d32f2f',
            width=100,
            font=CTK_FONT_SMALL,
        )
        clear_btn.grid(row=0, column=1, padx=5)

    def _add_mdev_device(self):
        """Add MDEV device."""
        from tkinter import messagebox

        uuid = self.mdev_uuid.get().strip()
        if not uuid:
            messagebox.showwarning('Warning', 'Please enter UUID!')
            return

        device = {
            'uuid': uuid,
            'model': self.mdev_model.get(),
        }
        if self.mdev_model.get() == 'vfio-ccw':
            device['ccw'] = {
                'cssid': self.ccw_cssid.get().strip(),
                'ssid': self.ccw_ssid.get().strip(),
                'devno': self.ccw_devno.get().strip(),
            }
        self.mdev_list.append(device)
        self._update_display()
        self._trigger_change()

    def _clear_mdev_list(self):
        """清空 MDEV 设备列表."""
        self.mdev_list.clear()
        self._update_display()
        self._trigger_change()

    def _update_display(self):
        """更新显示."""
        if self.mdev_list:
            devs = [f'{d["model"]}:{d["uuid"][:8]}...' for d in self.mdev_list]
            self.mdev_display.configure(text=f'已添加:{", ".join(devs)}')
        else:
            self.mdev_display.configure(text='暂无设备')

    def get_config(self) -> dict:
        """获取配置."""
        return {
            'type': 'mdev',
            'devices': self.mdev_list.copy(),
        }
