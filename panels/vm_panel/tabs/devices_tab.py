"""设备配置 Tab - 图形、USB/PCI/SCSI 直通、控制器、串口、TPM、磁盘设备等."""

import customtkinter as ctk

from ..inner_tab_panel import InnerTabPanel
from ..styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class USBHostdevTab(ctk.CTkFrame):
    """USB 设备直通配置."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent')
        self.on_change_callback = on_change_callback
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
            self.usb_display.configure(text=f'已添加：{", ".join(self.usb_list)}')
        else:
            self.usb_display.configure(text='暂无设备')

    def _trigger_change(self, *args):
        """触发变化回调."""
        if self.on_change_callback:
            self.on_change_callback()

    def get_config(self) -> dict:
        """获取配置."""
        return {
            'type': 'usb',
            'controller': self.usb_controller.get(),
            'startup_policy': self.startup_policy.get(),
            'guest_reset': self.guest_reset.get(),
            'devices': self.usb_list.copy(),
        }


class PCIHostdevTab(ctk.CTkFrame):
    """PCI 设备直通配置."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent')
        self.on_change_callback = on_change_callback
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
            self.pci_display.configure(text=f'已添加：{", ".join(devs)}')
        else:
            self.pci_display.configure(text='暂无设备')

    def _trigger_change(self, *args):
        """触发变化回调."""
        if self.on_change_callback:
            self.on_change_callback()

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


class SCSIHostdevTab(ctk.CTkFrame):
    """SCSI 设备直通配置."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent')
        self.on_change_callback = on_change_callback
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

        # 内容区域（动态切换）
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
            self.scsi_display.configure(text=f'已添加：{", ".join(devs)}')
        else:
            self.scsi_display.configure(text='暂无设备')

    def _trigger_change(self, *args):
        """触发变化回调."""
        if self.on_change_callback:
            self.on_change_callback()

    def get_config(self) -> dict:
        """获取配置."""
        return {
            'type': self.scsi_type.get(),
            'devices': self.scsi_list.copy(),
        }


class MdevHostdevTab(ctk.CTkFrame):
    """MDEV 设备直通配置."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent')
        self.on_change_callback = on_change_callback
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
            self.mdev_display.configure(text=f'已添加：{", ".join(devs)}')
        else:
            self.mdev_display.configure(text='暂无设备')

    def _trigger_change(self, *args):
        """触发变化回调."""
        if self.on_change_callback:
            self.on_change_callback()

    def get_config(self) -> dict:
        """获取配置."""
        return {
            'type': 'mdev',
            'devices': self.mdev_list.copy(),
        }


class DiskDevicesTab(ctk.CTkFrame):
    """磁盘设备配置 Tab - 支持 file, block, network, volume, dir, nvme, vhostuser, vhostvdpa, ctl 类型."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent')
        self.on_change_callback = on_change_callback
        self.disk_list = []

        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # 工具栏
        toolbar = ctk.CTkFrame(self, fg_color='transparent')
        toolbar.grid(row=0, column=0, sticky='ew', padx=5, pady=5)

        add_btn = ctk.CTkButton(
            toolbar,
            text='Add Disk Device',
            command=self._add_disk,
            fg_color='#4caf50',
            hover_color='#388e3c',
            width=120,
        )
        add_btn.pack(side='left', padx=5)

        clear_btn = ctk.CTkButton(
            toolbar,
            text='Clear List',
            command=self._clear_list,
            fg_color='#f44336',
            hover_color='#d32f2f',
            width=100,
        )
        clear_btn.pack(side='left', padx=5)

        # 内容区域
        self.content_frame = ctk.CTkScrollableFrame(
            self, fg_color=BG_COLOR_CONTENT, corner_radius=6
        )
        self.content_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)

        # 设备列表显示
        self.disk_display = ctk.CTkLabel(
            self.content_frame,
            text='暂无设备',
            font=CTK_FONT_SMALL,
            text_color='#aaaaaa',
            anchor='w',
        )
        self.disk_display.grid(row=0, column=0, sticky='w', padx=10, pady=10)

    def _add_disk(self):
        """Add disk device configuration dialog."""
        dialog = ctk.CTkToplevel(self)
        dialog.title('Add Disk Device')
        dialog.geometry('700x600')
        dialog.transient(self)
        dialog.grab_set()

        DiskConfigDialog(dialog, self._on_disk_added)

    def _on_disk_added(self, disk_config):
        """磁盘设备添加完成回调."""
        self.disk_list.append(disk_config)
        self._update_display()
        self._trigger_change()

    def _clear_list(self):
        """清空磁盘设备列表."""
        self.disk_list.clear()
        self._update_display()
        self._trigger_change()

    def _update_display(self):
        """更新显示."""
        # 清除旧的显示
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        if not self.disk_list:
            label = ctk.CTkLabel(
                self.content_frame,
                text='暂无设备',
                font=CTK_FONT_SMALL,
                text_color='#aaaaaa',
                anchor='w',
            )
            label.grid(row=0, column=0, sticky='w', padx=10, pady=10)
            return

        # 显示所有磁盘设备
        for i, disk in enumerate(self.disk_list):
            disk_frame = ctk.CTkFrame(self.content_frame, fg_color='transparent')
            disk_frame.grid(row=i, column=0, sticky='ew', padx=10, pady=5)

            # 设备类型标签
            type_label = f'[{disk.get("type", "file")}] {disk.get("device", "disk")}'
            source_label = disk.get('source', '')
            if disk.get('protocol'):
                source_label = f'{disk["protocol"]}:{source_label}'

            label = ctk.CTkLabel(
                disk_frame,
                text=f'{type_label}: {source_label} -> {disk.get("target_dev", "N/A")} ({disk.get("bus", "N/A")})',
                font=CTK_FONT_MAIN,
                anchor='w',
            )
            label.grid(row=0, column=0, sticky='w')

            # 删除按钮
            del_btn = ctk.CTkButton(
                disk_frame,
                text='删除',
                width=60,
                fg_color='#f44336',
                hover_color='#d32f2f',
                font=CTK_FONT_SMALL,
                command=lambda idx=i: self._remove_disk(idx),
            )
            del_btn.grid(row=0, column=1, padx=10)

    def _remove_disk(self, index):
        """删除指定索引的磁盘设备."""
        self.disk_list.pop(index)
        self._update_display()
        self._trigger_change()

    def _trigger_change(self, *args):
        """触发变化回调."""
        if self.on_change_callback:
            self.on_change_callback()

    def get_config(self) -> dict:
        """获取配置."""
        return {
            'type': 'disk_devices',
            'devices': self.disk_list.copy(),
        }


class DiskConfigDialog:
    """磁盘设备配置对话框."""

    def __init__(self, dialog, on_confirm_callback):
        self.dialog = dialog
        self.on_confirm_callback = on_confirm_callback
        self.config = {}
        self._init_ui()

    def _init_ui(self):
        """初始化 UI."""
        # 基本信息
        info_frame = ctk.CTkFrame(self.dialog, fg_color='transparent')
        info_frame.grid(row=0, column=0, sticky='ew', padx=20, pady=10)
        info_frame.grid_columnconfigure(1, weight=1)

        # Disk Type
        ctk.CTkLabel(info_frame, text='Type:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=0, column=0, padx=5, pady=5, sticky='w'
        )
        self.type_menu = ctk.CTkOptionMenu(
            info_frame,
            values=[
                'file',
                'block',
                'network',
                'volume',
                'dir',
                'nvme',
                'vhostuser',
                'vhostvdpa',
                'ctl',
            ],
            width=120,
            font=CTK_FONT_SMALL,
            command=self._on_type_changed,
        )
        self.type_menu.set('file')
        self.type_menu.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        # Device Type
        ctk.CTkLabel(
            info_frame, text='Device Type:', font=CTK_FONT_MAIN, width=80, anchor='w'
        ).grid(row=0, column=2, padx=5, pady=5, sticky='w')
        self.device_menu = ctk.CTkOptionMenu(
            info_frame,
            values=['disk', 'cdrom', 'lun', 'floppy'],
            width=100,
            font=CTK_FONT_SMALL,
        )
        self.device_menu.set('disk')
        self.device_menu.grid(row=0, column=3, padx=5, pady=5, sticky='w')

        # Target Device
        ctk.CTkLabel(
            info_frame, text='Target Device:', font=CTK_FONT_MAIN, width=80, anchor='w'
        ).grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.target_entry = ctk.CTkEntry(
            info_frame, placeholder_text='vda', width=100, font=CTK_FONT_SMALL
        )
        self.target_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        # Bus Type
        ctk.CTkLabel(info_frame, text='Bus:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=1, column=2, padx=5, pady=5, sticky='w'
        )
        self.bus_menu = ctk.CTkOptionMenu(
            info_frame,
            values=['virtio', 'sata', 'ide', 'scsi', 'usb', 'nvme'],
            width=80,
            font=CTK_FONT_SMALL,
        )
        self.bus_menu.set('virtio')
        self.bus_menu.grid(row=1, column=3, padx=5, pady=5, sticky='w')

        # 动态内容区域
        self.dynamic_frame = ctk.CTkFrame(self.dialog, fg_color='transparent')
        self.dynamic_frame.grid(row=1, column=0, sticky='nsew', padx=20, pady=10)
        self.dynamic_frame.grid_columnconfigure(1, weight=1)

        self._init_dynamic_ui()

        # Other Options
        options_frame = ctk.CTkFrame(self.dialog, fg_color='transparent')
        options_frame.grid(row=2, column=0, sticky='ew', padx=20, pady=10)
        options_frame.grid_columnconfigure(1, weight=1)

        # Read-only
        self.readonly_check = ctk.CTkCheckBox(options_frame, text='Read-only', font=CTK_FONT_SMALL)
        self.readonly_check.grid(row=0, column=0, padx=5, pady=5, sticky='w')

        # Boot Order
        ctk.CTkLabel(
            options_frame, text='Boot Order:', font=CTK_FONT_MAIN, width=80, anchor='w'
        ).grid(row=0, column=1, padx=5, pady=5, sticky='w')
        self.boot_order_entry = ctk.CTkEntry(options_frame, width=60, font=CTK_FONT_SMALL)
        self.boot_order_entry.grid(row=0, column=2, padx=5, pady=5, sticky='w')
        self.boot_order_entry.insert(0, '')

        # Startup Policy
        ctk.CTkLabel(
            options_frame, text='Startup Policy:', font=CTK_FONT_MAIN, width=80, anchor='w'
        ).grid(row=0, column=3, padx=5, pady=5, sticky='w')
        self.startup_menu = ctk.CTkOptionMenu(
            options_frame, values=['required', 'optional'], width=100, font=CTK_FONT_SMALL
        )
        self.startup_menu.set('optional')
        self.startup_menu.grid(row=0, column=4, padx=5, pady=5, sticky='w')

        # 按钮
        btn_frame = ctk.CTkFrame(self.dialog, fg_color='transparent')
        btn_frame.grid(row=3, column=0, sticky='e', padx=20, pady=10)

        ctk.CTkButton(
            btn_frame,
            text='Cancel',
            command=self.dialog.destroy,
            width=80,
            fg_color='#9e9e9e',
            hover_color='#757575',
        ).pack(side='right', padx=5)

        ctk.CTkButton(
            btn_frame,
            text='OK',
            command=self._confirm,
            width=80,
            fg_color='#4caf50',
            hover_color='#388e3c',
        ).pack(side='right', padx=5)

    def _init_dynamic_ui(self):
        """初始化动态内容 UI."""
        # 清除现有内容
        for widget in self.dynamic_frame.winfo_children():
            widget.destroy()

        disk_type = self.type_menu.get()

        row = 0

        # file type
        if disk_type == 'file':
            ctk.CTkLabel(
                self.dynamic_frame, text='File Path:', font=CTK_FONT_MAIN, width=80, anchor='w'
            ).grid(row=row, column=0, padx=5, pady=5, sticky='w')
            self.source_entry = ctk.CTkEntry(
                self.dynamic_frame,
                placeholder_text='/var/lib/libvirt/images/disk.qcow2',
                width=400,
                font=CTK_FONT_SMALL,
            )
            self.source_entry.grid(row=row, column=1, padx=5, pady=5, sticky='ew')

            ctk.CTkLabel(
                self.dynamic_frame, text='Driver Format:', font=CTK_FONT_MAIN, width=80, anchor='w'
            ).grid(row=row + 1, column=0, padx=5, pady=5, sticky='w')
            self.driver_menu = ctk.CTkOptionMenu(
                self.dynamic_frame,
                values=['qcow2', 'raw', 'vmdk', 'vdi', 'vpc', 'parallels'],
                width=100,
                font=CTK_FONT_SMALL,
            )
            self.driver_menu.set('qcow2')
            self.driver_menu.grid(row=row + 1, column=1, padx=5, pady=5, sticky='w')

        # block type
        elif disk_type == 'block':
            ctk.CTkLabel(
                self.dynamic_frame, text='Block Device:', font=CTK_FONT_MAIN, width=80, anchor='w'
            ).grid(row=row, column=0, padx=5, pady=5, sticky='w')
            self.source_entry = ctk.CTkEntry(
                self.dynamic_frame, placeholder_text='/dev/sda', width=300, font=CTK_FONT_SMALL
            )
            self.source_entry.grid(row=row, column=1, padx=5, pady=5, sticky='w')

        # network type
        elif disk_type == 'network':
            ctk.CTkLabel(
                self.dynamic_frame, text='Protocol:', font=CTK_FONT_MAIN, width=80, anchor='w'
            ).grid(row=row, column=0, padx=5, pady=5, sticky='w')
            self.protocol_menu = ctk.CTkOptionMenu(
                self.dynamic_frame,
                values=['sheepdog', 'rbd', 'iscsi', 'nfs', 'http', 'https', 'ftp', 'ftps', 'tftp'],
                width=100,
                font=CTK_FONT_SMALL,
                command=self._on_protocol_changed,
            )
            self.protocol_menu.set('rbd')
            self.protocol_menu.grid(row=row, column=1, padx=5, pady=5, sticky='w')

            ctk.CTkLabel(
                self.dynamic_frame, text='Image Name:', font=CTK_FONT_MAIN, width=80, anchor='w'
            ).grid(row=row + 1, column=0, padx=5, pady=5, sticky='w')
            self.source_entry = ctk.CTkEntry(
                self.dynamic_frame, placeholder_text='pool/image', width=300, font=CTK_FONT_SMALL
            )
            self.source_entry.grid(row=row + 1, column=1, padx=5, pady=5, sticky='ew')

            ctk.CTkLabel(
                self.dynamic_frame, text='Host:', font=CTK_FONT_MAIN, width=80, anchor='w'
            ).grid(row=row + 2, column=0, padx=5, pady=5, sticky='w')
            self.host_entry = ctk.CTkEntry(
                self.dynamic_frame, placeholder_text='hostname', width=150, font=CTK_FONT_SMALL
            )
            self.host_entry.grid(row=row + 2, column=1, padx=5, pady=5, sticky='w')

            ctk.CTkLabel(
                self.dynamic_frame, text='Port:', font=CTK_FONT_MAIN, width=50, anchor='w'
            ).grid(row=row + 2, column=2, padx=5, pady=5, sticky='w')
            self.port_entry = ctk.CTkEntry(
                self.dynamic_frame, placeholder_text='7000', width=60, font=CTK_FONT_SMALL
            )
            self.port_entry.grid(row=row + 2, column=3, padx=5, pady=5, sticky='w')

            # Authentication
            self.auth_check = ctk.CTkCheckBox(
                self.dynamic_frame, text='Enable Authentication', font=CTK_FONT_SMALL
            )
            self.auth_check.grid(row=row + 3, column=0, padx=5, pady=5, sticky='w')

            ctk.CTkLabel(
                self.dynamic_frame, text='Username:', font=CTK_FONT_MAIN, width=80, anchor='w'
            ).grid(row=row + 3, column=1, padx=5, pady=5, sticky='w')
            self.username_entry = ctk.CTkEntry(
                self.dynamic_frame, placeholder_text='myuser', width=100, font=CTK_FONT_SMALL
            )
            self.username_entry.grid(row=row + 3, column=2, padx=5, pady=5, sticky='w')

            ctk.CTkLabel(
                self.dynamic_frame, text='Secret:', font=CTK_FONT_MAIN, width=60, anchor='w'
            ).grid(row=row + 3, column=3, padx=5, pady=5, sticky='w')
            self.secret_entry = ctk.CTkEntry(
                self.dynamic_frame, placeholder_text='libvirtiscsi', width=120, font=CTK_FONT_SMALL
            )
            self.secret_entry.grid(row=row + 3, column=4, padx=5, pady=5, sticky='w')

        # volume type
        elif disk_type == 'volume':
            ctk.CTkLabel(
                self.dynamic_frame, text='Storage Pool:', font=CTK_FONT_MAIN, width=80, anchor='w'
            ).grid(row=row, column=0, padx=5, pady=5, sticky='w')
            self.pool_entry = ctk.CTkEntry(
                self.dynamic_frame, placeholder_text='blk-pool0', width=200, font=CTK_FONT_SMALL
            )
            self.pool_entry.grid(row=row, column=1, padx=5, pady=5, sticky='w')

            ctk.CTkLabel(
                self.dynamic_frame, text='Volume:', font=CTK_FONT_MAIN, width=80, anchor='w'
            ).grid(row=row + 1, column=0, padx=5, pady=5, sticky='w')
            self.volume_entry = ctk.CTkEntry(
                self.dynamic_frame, placeholder_text='vol0', width=200, font=CTK_FONT_SMALL
            )
            self.volume_entry.grid(row=row + 1, column=1, padx=5, pady=5, sticky='w')

        # dir type
        elif disk_type == 'dir':
            ctk.CTkLabel(
                self.dynamic_frame, text='Directory:', font=CTK_FONT_MAIN, width=80, anchor='w'
            ).grid(row=row, column=0, padx=5, pady=5, sticky='w')
            self.source_entry = ctk.CTkEntry(
                self.dynamic_frame,
                placeholder_text='/var/somefiles',
                width=300,
                font=CTK_FONT_SMALL,
            )
            self.source_entry.grid(row=row, column=1, padx=5, pady=5, sticky='ew')

        # nvme type
        elif disk_type == 'nvme':
            ctk.CTkLabel(
                self.dynamic_frame, text='Namespace:', font=CTK_FONT_MAIN, width=80, anchor='w'
            ).grid(row=row, column=0, padx=5, pady=5, sticky='w')
            self.ns_entry = ctk.CTkEntry(
                self.dynamic_frame, placeholder_text='1', width=60, font=CTK_FONT_SMALL
            )
            self.ns_entry.grid(row=row, column=1, padx=5, pady=5, sticky='w')

            ctk.CTkLabel(
                self.dynamic_frame, text='PCI Address:', font=CTK_FONT_MAIN, width=80, anchor='w'
            ).grid(row=row + 1, column=0, padx=5, pady=5, sticky='w')
            self.pci_entry = ctk.CTkEntry(
                self.dynamic_frame, placeholder_text='0000:01:00.0', width=150, font=CTK_FONT_SMALL
            )
            self.pci_entry.grid(row=row + 1, column=1, padx=5, pady=5, sticky='w')

        # vhostuser type
        elif disk_type == 'vhostuser':
            ctk.CTkLabel(
                self.dynamic_frame, text='Socket:', font=CTK_FONT_MAIN, width=80, anchor='w'
            ).grid(row=row, column=0, padx=5, pady=5, sticky='w')
            self.source_entry = ctk.CTkEntry(
                self.dynamic_frame,
                placeholder_text='/tmp/vhost-blk.sock',
                width=300,
                font=CTK_FONT_SMALL,
            )
            self.source_entry.grid(row=row, column=1, padx=5, pady=5, sticky='ew')

        # vhostvdpa type
        elif disk_type == 'vhostvdpa':
            ctk.CTkLabel(
                self.dynamic_frame, text='Device:', font=CTK_FONT_MAIN, width=80, anchor='w'
            ).grid(row=row, column=0, padx=5, pady=5, sticky='w')
            self.source_entry = ctk.CTkEntry(
                self.dynamic_frame,
                placeholder_text='/dev/vhost-vdpa-0',
                width=200,
                font=CTK_FONT_SMALL,
            )
            self.source_entry.grid(row=row, column=1, padx=5, pady=5, sticky='w')

        # ctl type
        elif disk_type == 'ctl':
            ctk.CTkLabel(
                self.dynamic_frame, text='Device:', font=CTK_FONT_MAIN, width=80, anchor='w'
            ).grid(row=row, column=0, padx=5, pady=5, sticky='w')
            self.source_entry = ctk.CTkEntry(
                self.dynamic_frame, placeholder_text='/dev/cam/ctl', width=200, font=CTK_FONT_SMALL
            )
            self.source_entry.grid(row=row, column=1, padx=5, pady=5, sticky='w')

    def _on_type_changed(self, new_type):
        """类型改变."""
        self._init_dynamic_ui()

    def _on_protocol_changed(self, new_protocol):
        """协议改变."""
        # 根据协议设置默认端口
        default_ports = {
            'sheepdog': '7000',
            'rbd': '6789',
            'iscsi': '3260',
            'nfs': '2049',
            'http': '80',
            'https': '443',
            'ftp': '21',
            'ftps': '990',
            'tftp': '69',
        }
        if hasattr(self, 'port_entry'):
            self.port_entry.delete(0, 'end')
            self.port_entry.insert(0, default_ports.get(new_protocol, ''))

    def _confirm(self):
        """确认添加."""
        disk_type = self.type_menu.get()
        device_type = self.device_menu.get()

        config = {
            'type': disk_type,
            'device': device_type,
            'target_dev': self.target_entry.get().strip(),
            'bus': self.bus_menu.get(),
            'readonly': self.readonly_check.get(),
            'boot_order': self.boot_order_entry.get().strip() or None,
            'startup_policy': self.startup_menu.get(),
        }

        # 收集不同类型的配置
        if disk_type == 'file':
            config['source'] = self.source_entry.get().strip()
            config['driver'] = self.driver_menu.get()
        elif disk_type == 'block':
            config['source'] = self.source_entry.get().strip()
        elif disk_type == 'network':
            config['protocol'] = self.protocol_menu.get()
            config['source'] = self.source_entry.get().strip()
            config['host'] = self.host_entry.get().strip()
            config['port'] = self.port_entry.get().strip()
            if self.auth_check.get():
                config['username'] = self.username_entry.get().strip()
                config['secret'] = self.secret_entry.get().strip()
        elif disk_type == 'volume':
            config['pool'] = self.pool_entry.get().strip()
            config['volume'] = self.volume_entry.get().strip()
        elif disk_type == 'dir':
            config['source'] = self.source_entry.get().strip()
        elif disk_type == 'nvme':
            config['namespace'] = self.ns_entry.get().strip() or '1'
            config['pci'] = self.pci_entry.get().strip()
        elif disk_type == 'vhostuser':
            config['source'] = self.source_entry.get().strip()
        elif disk_type == 'vhostvdpa':
            config['source'] = self.source_entry.get().strip()
        elif disk_type == 'ctl':
            config['source'] = self.source_entry.get().strip()

        self.on_confirm_callback(config)
        self.dialog.destroy()


class GraphicsTab(ctk.CTkFrame):
    """图形显示配置 Tab."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent')
        self.on_change_callback = on_change_callback

        self.graphics_type = None
        self.graphics_listen = None
        self.graphics_port = None
        self.video_model = None
        self.vram_entry = None

        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(frame, text='Graphics', font=CTK_FONT_BOLD, text_color='#ba68c8').grid(
            row=0, column=0, columnspan=6, padx=10, pady=5, sticky='w'
        )

        ctk.CTkLabel(frame, text='Graphics:', font=CTK_FONT_MAIN, width=70, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.graphics_type = ctk.CTkOptionMenu(
            frame, values=['vnc', 'spice', 'none'], width=90, font=CTK_FONT_SMALL
        )
        self.graphics_type.set('vnc')
        self.graphics_type.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.graphics_type.configure(command=self._trigger_change)

        ctk.CTkLabel(frame, text='Listen:', font=CTK_FONT_MAIN, width=50, anchor='w').grid(
            row=1, column=2, padx=5, pady=5, sticky='w'
        )
        self.graphics_listen = ctk.CTkEntry(frame, width=100, font=CTK_FONT_SMALL)
        self.graphics_listen.grid(row=1, column=3, padx=5, pady=5, sticky='w')
        self.graphics_listen.insert(0, '0.0.0.0')
        self.graphics_listen.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(frame, text='Port:', font=CTK_FONT_MAIN, width=40, anchor='w').grid(
            row=1, column=4, padx=5, pady=5, sticky='w'
        )
        self.graphics_port = ctk.CTkEntry(frame, width=60, font=CTK_FONT_SMALL)
        self.graphics_port.grid(row=1, column=5, padx=5, pady=5, sticky='w')
        self.graphics_port.insert(0, '-1')
        self.graphics_port.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(frame, text='Video:', font=CTK_FONT_MAIN, width=50, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.video_model = ctk.CTkOptionMenu(
            frame,
            values=['qxl', 'virtio', 'vmvga', 'bochs', 'ramfb', 'virtio-vga', 'virtio-vga-gl'],
            width=120,
            font=CTK_FONT_SMALL,
        )
        self.video_model.set('qxl')
        self.video_model.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.video_model.configure(command=self._trigger_change)

        ctk.CTkLabel(frame, text='VRAM (MB):', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=2, column=2, padx=5, pady=5, sticky='w'
        )
        self.vram_entry = ctk.CTkEntry(frame, width=60, font=CTK_FONT_SMALL)
        self.vram_entry.grid(row=2, column=3, padx=5, pady=5, sticky='w')
        self.vram_entry.insert(0, '64')
        self.vram_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

    def _trigger_change(self, *args):
        """触发变化回调."""
        if self.on_change_callback:
            self.on_change_callback()

    def get_config(self) -> dict:
        """获取图形配置."""
        return {
            'type': self.graphics_type.get(),
            'listen': self.graphics_listen.get().strip() or '0.0.0.0',
            'port': self.graphics_port.get().strip() or '-1',
            'video_model': self.video_model.get(),
            'vram': int(self.vram_entry.get().strip() or '64'),
        }


class OthersTab(ctk.CTkFrame):
    """其他设备配置 Tab - 串口、TPM、控制器."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent')
        self.on_change_callback = on_change_callback

        self.serial_type = None
        self.serial_port = None
        self.tpm_model = None
        self.tpm_version = None
        self.disable_usb_check = None
        self.disable_sound_check = None
        self.audio_model = None

        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=1)

        # 串口配置
        serial_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        serial_frame.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
        serial_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            serial_frame, text='Serial Configuration', font=CTK_FONT_BOLD, text_color='#ff9800'
        ).grid(row=0, column=0, columnspan=4, padx=10, pady=5, sticky='w')

        ctk.CTkLabel(serial_frame, text='类型:', font=CTK_FONT_MAIN, width=60, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.serial_type = ctk.CTkOptionMenu(
            serial_frame,
            values=['pty', 'tcp', 'udp', 'unix', 'spicevmc', 'none'],
            width=100,
            font=CTK_FONT_SMALL,
        )
        self.serial_type.set('pty')
        self.serial_type.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.serial_type.configure(command=self._trigger_change)

        ctk.CTkLabel(serial_frame, text='端口:', font=CTK_FONT_MAIN, width=50, anchor='w').grid(
            row=1, column=2, padx=10, pady=5, sticky='w'
        )
        self.serial_port = ctk.CTkEntry(serial_frame, width=80, font=CTK_FONT_SMALL)
        self.serial_port.grid(row=1, column=3, padx=5, pady=5, sticky='w')
        self.serial_port.insert(0, '0')
        self.serial_port.bind('<KeyRelease>', lambda e: self._trigger_change())

        # TPM 配置
        tpm_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        tpm_frame.grid(row=1, column=0, sticky='ew', padx=5, pady=5)
        tpm_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(tpm_frame, text='TPM Device', font=CTK_FONT_BOLD, text_color='#7986cb').grid(
            row=0, column=0, columnspan=4, padx=10, pady=5, sticky='w'
        )

        ctk.CTkLabel(tpm_frame, text='模型:', font=CTK_FONT_MAIN, width=60, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.tpm_model = ctk.CTkOptionMenu(
            tpm_frame,
            values=['none', 'tpm-crb', 'tpm-tis', 'tpm-spapr'],
            width=100,
            font=CTK_FONT_SMALL,
        )
        self.tpm_model.set('none')
        self.tpm_model.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.tpm_model.configure(command=self._trigger_change)

        ctk.CTkLabel(tpm_frame, text='版本:', font=CTK_FONT_MAIN, width=50, anchor='w').grid(
            row=1, column=2, padx=10, pady=5, sticky='w'
        )
        self.tpm_version = ctk.CTkOptionMenu(
            tpm_frame, values=['1.2', '2.0'], width=60, font=CTK_FONT_SMALL
        )
        self.tpm_version.set('2.0')
        self.tpm_version.grid(row=1, column=3, padx=5, pady=5, sticky='w')
        self.tpm_version.configure(command=self._trigger_change)

        # 控制器配置
        ctrl_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        ctrl_frame.grid(row=2, column=0, sticky='ew', padx=5, pady=5)
        ctrl_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(ctrl_frame, text='Controller', font=CTK_FONT_BOLD, text_color='#ff7043').grid(
            row=0, column=0, columnspan=3, padx=10, pady=5, sticky='w'
        )

        self.disable_usb_check = ctk.CTkCheckBox(
            ctrl_frame, text='Disable USB', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.disable_usb_check.grid(row=1, column=0, padx=10, pady=5, sticky='w')

        self.disable_sound_check = ctk.CTkCheckBox(
            ctrl_frame, text='Disable Sound', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.disable_sound_check.grid(row=1, column=1, padx=10, pady=5, sticky='w')

        ctk.CTkLabel(ctrl_frame, text='Audio:', font=CTK_FONT_MAIN, width=50, anchor='w').grid(
            row=1, column=2, padx=10, pady=5, sticky='w'
        )
        self.audio_model = ctk.CTkOptionMenu(
            ctrl_frame,
            values=['ich9', 'ich6', 'ac97', 'hda', 'none'],
            width=80,
            font=CTK_FONT_SMALL,
        )
        self.audio_model.set('ich9')
        self.audio_model.grid(row=1, column=3, padx=5, pady=5, sticky='w')
        self.audio_model.configure(command=self._trigger_change)

    def _trigger_change(self, *args):
        """触发变化回调."""
        if self.on_change_callback:
            self.on_change_callback()

    def get_serial_config(self):
        """获取串口配置."""
        return {
            'type': self.serial_type.get(),
            'port': self.serial_port.get().strip() or '0',
        }

    def get_tpm_config(self):
        """获取 TPM 配置."""
        model = self.tpm_model.get()
        if model == 'none':
            return None
        return {
            'model': model,
            'version': self.tpm_version.get(),
        }

    def get_audio_config(self):
        """获取音频配置."""
        model = self.audio_model.get()
        if model == 'none':
            return None
        return {'model': model}

    def get_controller_config(self):
        """获取控制器配置."""
        return {
            'disable_usb': self.disable_usb_check.get(),
            'disable_sound': self.disable_sound_check.get(),
        }


class DevicesTab(ctk.CTkFrame):
    """设备配置 Tab - 包含图形、hostdev 子选项."""

    SUB_TABS_CONFIG = {
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
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent')
        self.on_change_callback = on_change_callback

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

    def _trigger_change(self, *args):
        """触发变化回调."""
        if self.on_change_callback:
            self.on_change_callback()

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
