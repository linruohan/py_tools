"""主机设备分配模块 - 包括USB、PCI、SCSI设备,ACPI Generic Initiators和Block/character devices"""

import customtkinter as ctk

from components.base_tab import BaseConfigTab
from utils.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class HostDeviceAssignmentTab(BaseConfigTab):
    """主机设备分配配置主tab"""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, on_change_callback, **kwargs)
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面"""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            frame, text='Host Device Assignment', font=CTK_FONT_BOLD, text_color='#ff5722'
        ).grid(row=0, column=0, padx=10, pady=5, sticky='w')

        ctk.CTkLabel(
            frame,
            text='主机设备分配允许将物理设备直接分配给虚拟机使用.\n'
            '支持USB、PCI、SCSI设备,以及ACPI Generic Initiators和Block/character devices.',
            font=CTK_FONT_SMALL,
            text_color='#666666',
        ).grid(row=1, column=0, padx=10, pady=5, sticky='w')


class USBPCISCSIDevicesTab(BaseConfigTab):
    """USB/PCI/SCSI设备配置"""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, on_change_callback, **kwargs)
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面"""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            frame, text='USB / PCI / SCSI Devices', font=CTK_FONT_BOLD, text_color='#2196f3'
        ).grid(row=0, column=0, padx=10, pady=5, sticky='w')

        # 设备类型选择
        type_frame = ctk.CTkFrame(frame, fg_color='transparent')
        type_frame.grid(row=1, column=0, padx=10, pady=5, sticky='w')

        ctk.CTkLabel(
            type_frame, text='Device Type:', font=CTK_FONT_MAIN, width=100, anchor='w'
        ).grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.device_type = ctk.CTkOptionMenu(
            type_frame,
            values=['USB', 'PCI', 'SCSI'],
            width=100,
            font=CTK_FONT_SMALL,
            command=self._on_device_type_change,
        )
        self.device_type.set('USB')
        self.device_type.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        # 内容区域
        self.content_frame = ctk.CTkFrame(frame, fg_color='transparent')
        self.content_frame.grid(row=2, column=0, sticky='nsew', padx=10, pady=5)
        self.content_frame.grid_columnconfigure(0, weight=1)

        self._init_usb_ui()

    def _on_device_type_change(self, *args):
        """设备类型变化"""
        device_type = self.device_type.get()
        if device_type == 'USB':
            self._init_usb_ui()
        elif device_type == 'PCI':
            self._init_pci_ui()
        elif device_type == 'SCSI':
            self._init_scsi_ui()
        self._trigger_change()

    def _init_usb_ui(self):
        """初始化USB设备配置UI"""
        # 清空现有内容
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        usb_frame = ctk.CTkFrame(self.content_frame, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        usb_frame.grid(row=0, column=0, sticky='nsew')
        usb_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            usb_frame, text='USB Device Configuration', font=CTK_FONT_MAIN, text_color='#2196f3'
        ).grid(row=0, column=0, columnspan=4, padx=10, pady=5, sticky='w')

        # Vendor:Product
        ctk.CTkLabel(
            usb_frame, text='Vendor:Product:', font=CTK_FONT_MAIN, width=100, anchor='w'
        ).grid(row=1, column=0, padx=10, pady=5, sticky='w')
        self.usb_id = ctk.CTkEntry(
            usb_frame, placeholder_text='8087:8008', width=150, font=CTK_FONT_SMALL
        )
        self.usb_id.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.usb_id.bind('<KeyRelease>', lambda e: self._trigger_change())

        # Startup Policy
        ctk.CTkLabel(
            usb_frame, text='Startup Policy:', font=CTK_FONT_MAIN, width=100, anchor='w'
        ).grid(row=2, column=0, padx=10, pady=5, sticky='w')
        self.usb_startup = ctk.CTkOptionMenu(
            usb_frame,
            values=['required', 'optional'],
            width=100,
            font=CTK_FONT_SMALL,
            command=self._trigger_change,
        )
        self.usb_startup.set('optional')
        self.usb_startup.grid(row=2, column=1, padx=5, pady=5, sticky='w')

    def _init_pci_ui(self):
        """初始化PCI设备配置UI"""
        # 清空现有内容
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        pci_frame = ctk.CTkFrame(self.content_frame, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        pci_frame.grid(row=0, column=0, sticky='nsew')
        pci_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            pci_frame, text='PCI Device Configuration', font=CTK_FONT_MAIN, text_color='#4caf50'
        ).grid(row=0, column=0, columnspan=4, padx=10, pady=5, sticky='w')

        # PCI Address
        ctk.CTkLabel(
            pci_frame, text='PCI Address:', font=CTK_FONT_MAIN, width=100, anchor='w'
        ).grid(row=1, column=0, padx=10, pady=5, sticky='w')
        self.pci_address = ctk.CTkEntry(
            pci_frame, placeholder_text='0000:00:00.0', width=150, font=CTK_FONT_SMALL
        )
        self.pci_address.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.pci_address.bind('<KeyRelease>', lambda e: self._trigger_change())

        # ROM BAR
        ctk.CTkLabel(pci_frame, text='ROM BAR:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.pci_rom = ctk.CTkOptionMenu(
            pci_frame,
            values=['on', 'off'],
            width=100,
            font=CTK_FONT_SMALL,
            command=self._trigger_change,
        )
        self.pci_rom.set('off')
        self.pci_rom.grid(row=2, column=1, padx=5, pady=5, sticky='w')

    def _init_scsi_ui(self):
        """初始化SCSI设备配置UI"""
        # 清空现有内容
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        scsi_frame = ctk.CTkFrame(self.content_frame, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        scsi_frame.grid(row=0, column=0, sticky='nsew')
        scsi_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            scsi_frame, text='SCSI Device Configuration', font=CTK_FONT_MAIN, text_color='#ff9800'
        ).grid(row=0, column=0, columnspan=4, padx=10, pady=5, sticky='w')

        # SCSI Type
        ctk.CTkLabel(scsi_frame, text='SCSI Type:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.scsi_type = ctk.CTkOptionMenu(
            scsi_frame,
            values=['scsi', 'scsi_host'],
            width=100,
            font=CTK_FONT_SMALL,
            command=self._trigger_change,
        )
        self.scsi_type.set('scsi')
        self.scsi_type.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        # Bus:Target:Unit
        ctk.CTkLabel(
            scsi_frame, text='Bus:Target:Unit:', font=CTK_FONT_MAIN, width=100, anchor='w'
        ).grid(row=2, column=0, padx=10, pady=5, sticky='w')
        self.scsi_address = ctk.CTkEntry(
            scsi_frame, placeholder_text='0:0:0', width=150, font=CTK_FONT_SMALL
        )
        self.scsi_address.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.scsi_address.bind('<KeyRelease>', lambda e: self._trigger_change())

    def get_config(self) -> dict:
        """获取配置"""
        device_type = self.device_type.get()
        config = {'type': device_type.lower()}

        if device_type == 'USB':
            config['vendor_product'] = self.usb_id.get().strip()
            config['startup_policy'] = self.usb_startup.get()
        elif device_type == 'PCI':
            config['address'] = self.pci_address.get().strip()
            config['rom_bar'] = self.pci_rom.get()
        elif device_type == 'SCSI':
            config['scsi_type'] = self.scsi_type.get()
            config['address'] = self.scsi_address.get().strip()

        return config


class ACPIInitiatorsTab(BaseConfigTab):
    """ACPI Generic Initiators配置"""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, on_change_callback, **kwargs)
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面"""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            frame, text='ACPI Generic Initiators', font=CTK_FONT_BOLD, text_color='#9c27b0'
        ).grid(row=0, column=0, columnspan=4, padx=10, pady=5, sticky='w')

        # ACPI Device ID
        ctk.CTkLabel(frame, text='Device ID:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.acpi_id = ctk.CTkEntry(
            frame, placeholder_text='ACPI0004', width=150, font=CTK_FONT_SMALL
        )
        self.acpi_id.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.acpi_id.bind('<KeyRelease>', lambda e: self._trigger_change())

        # ACPI Path
        ctk.CTkLabel(frame, text='ACPI Path:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.acpi_path = ctk.CTkEntry(
            frame, placeholder_text=r'\_SB.PCI0.I2C0', width=200, font=CTK_FONT_SMALL
        )
        self.acpi_path.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.acpi_path.bind('<KeyRelease>', lambda e: self._trigger_change())

    def get_config(self) -> dict:
        """获取配置"""
        return {
            'type': 'acpi',
            'device_id': self.acpi_id.get().strip(),
            'path': self.acpi_path.get().strip(),
        }


class BlockCharDevicesTab(BaseConfigTab):
    """Block/character devices配置"""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, on_change_callback, **kwargs)
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面"""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            frame, text='Block / Character Devices', font=CTK_FONT_BOLD, text_color='#ff5722'
        ).grid(row=0, column=0, columnspan=4, padx=10, pady=5, sticky='w')

        # Device Type
        ctk.CTkLabel(frame, text='Device Type:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.dev_type = ctk.CTkOptionMenu(
            frame,
            values=['block', 'char'],
            width=100,
            font=CTK_FONT_SMALL,
            command=self._trigger_change,
        )
        self.dev_type.set('block')
        self.dev_type.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        # Device Path
        ctk.CTkLabel(frame, text='Device Path:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.dev_path = ctk.CTkEntry(
            frame, placeholder_text='/dev/sda', width=200, font=CTK_FONT_SMALL
        )
        self.dev_path.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.dev_path.bind('<KeyRelease>', lambda e: self._trigger_change())

        # Read-only
        ctk.CTkLabel(frame, text='Mode:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=3, column=0, padx=10, pady=5, sticky='w'
        )
        self.readonly = ctk.CTkCheckBox(
            frame, text='Read-only', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.readonly.grid(row=3, column=1, padx=5, pady=5, sticky='w')

    def get_config(self) -> dict:
        """获取配置"""
        return {
            'type': self.dev_type.get(),
            'path': self.dev_path.get().strip(),
            'readonly': self.readonly.get(),
        }
