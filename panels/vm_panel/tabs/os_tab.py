"""引导/OS 配置 Tab."""

import customtkinter as ctk

from components.base_tab import BaseConfigTab
from utils.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class OSTab(BaseConfigTab):
    """引导/OS 配置 Tab."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, on_change_callback, **kwargs)

        # 控件引用
        self.firmware_type = None
        self.secure_boot = None
        self.boot_device_1 = None
        self.boot_device_2 = None
        self.boot_device_3 = None
        self.boot_timeout_entry = None

        # 初始化 UI
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面."""
        # 配置 grid 权重
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)

        # 固件配置
        fw_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=8)
        fw_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=10)
        fw_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(fw_frame, text='固件配置', font=CTK_FONT_BOLD, text_color='#64b5f6').grid(
            row=0, column=0, columnspan=4, padx=10, pady=5, sticky='w'
        )

        # 固件类型
        ctk.CTkLabel(fw_frame, text='固件:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.firmware_type = ctk.CTkOptionMenu(
            fw_frame, values=['BIOS', 'UEFI', 'EFIVARS'], width=120, font=CTK_FONT_SMALL
        )
        self.firmware_type.set('BIOS')
        self.firmware_type.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.firmware_type.configure(command=self._trigger_change)

        # 安全启动
        ctk.CTkLabel(fw_frame, text='安全启动:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=1, column=2, padx=10, pady=5, sticky='w'
        )
        self.secure_boot = ctk.CTkCheckBox(fw_frame, text='启用', font=CTK_FONT_SMALL)
        self.secure_boot.grid(row=1, column=3, padx=5, pady=5, sticky='w')
        self.secure_boot.configure(command=self._trigger_change)

        # 引导设备
        boot_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=8)
        boot_frame.grid(row=1, column=0, sticky='ew', padx=10, pady=10)
        boot_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(boot_frame, text='引导顺序', font=CTK_FONT_BOLD, text_color='#4caf50').grid(
            row=0, column=0, columnspan=4, padx=10, pady=5, sticky='w'
        )

        # 第一引导设备
        ctk.CTkLabel(boot_frame, text='第一引导:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.boot_device_1 = ctk.CTkOptionMenu(
            boot_frame, values=['hd', 'cdrom', 'network', 'floppy'], width=100, font=CTK_FONT_SMALL
        )
        self.boot_device_1.set('hd')
        self.boot_device_1.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.boot_device_1.configure(command=self._trigger_change)

        # 第二引导设备
        ctk.CTkLabel(boot_frame, text='第二引导:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=1, column=2, padx=10, pady=5, sticky='w'
        )
        self.boot_device_2 = ctk.CTkOptionMenu(
            boot_frame,
            values=['none', 'hd', 'cdrom', 'network', 'floppy'],
            width=100,
            font=CTK_FONT_SMALL,
        )
        self.boot_device_2.set('cdrom')
        self.boot_device_2.grid(row=1, column=3, padx=5, pady=5, sticky='w')
        self.boot_device_2.configure(command=self._trigger_change)

        # 第三引导设备
        ctk.CTkLabel(boot_frame, text='第三引导:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.boot_device_3 = ctk.CTkOptionMenu(
            boot_frame,
            values=['none', 'hd', 'cdrom', 'network', 'floppy'],
            width=100,
            font=CTK_FONT_SMALL,
        )
        self.boot_device_3.set('network')
        self.boot_device_3.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.boot_device_3.configure(command=self._trigger_change)

        # 超时
        ctk.CTkLabel(boot_frame, text='超时 (ms):', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=2, column=2, padx=10, pady=5, sticky='w'
        )
        self.boot_timeout_entry = ctk.CTkEntry(boot_frame, placeholder_text='-1', width=100)
        self.boot_timeout_entry.grid(row=2, column=3, padx=5, pady=5, sticky='w')
        self.boot_timeout_entry.insert(0, '-1')
        self.boot_timeout_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

    def get_os_config(self):
        """获取 OS 配置."""
        boot_devices = []
        for dev in [self.boot_device_1.get(), self.boot_device_2.get(), self.boot_device_3.get()]:
            if dev and dev != 'none':
                boot_devices.append(dev)
        return {
            'firmware': self.firmware_type.get(),
            'secure_boot': self.secure_boot.get(),
            'boot_devices': boot_devices,
            'boot_timeout': int(self.boot_timeout_entry.get().strip() or '-1'),
        }

    def to_xml(self) -> dict:
        """生成 XML 配置字典."""
        config = self.get_os_config()
        firmware_map = {
            'BIOS': 'bios',
            'UEFI': 'efi',
            'EFIVARS': 'efi',
        }
        return {
            'os_booting': {
                'type': 'hvm',
                'arch': 'x86_64',
                'machine': 'q35',
                'firmware': firmware_map.get(config['firmware'], 'bios'),
                'secure_boot': config['secure_boot'],
                'boot_devices': config['boot_devices'],
                'boot_timeout': config['boot_timeout'],
            }
        }

    def load_config(self, config: dict):
        """加载配置数据到 UI."""
        if 'firmware' in config:
            fw_map = {'bios': 'BIOS', 'efi': 'UEFI'}
            self.firmware_type.set(fw_map.get(config.get('firmware', 'BIOS'), 'BIOS'))
        if 'secure_boot' in config:
            if config['secure_boot']:
                self.secure_boot.select()
            else:
                self.secure_boot.deselect()
        if 'boot_devices' in config:
            devices = config['boot_devices'] + ['none', 'none']
            self.boot_device_1.set(devices[0] if len(devices) > 0 else 'hd')
            self.boot_device_2.set(devices[1] if len(devices) > 1 else 'none')
            self.boot_device_3.set(devices[2] if len(devices) > 2 else 'none')
        if 'boot_timeout' in config:
            self.boot_timeout_entry.delete(0, ctk.END)
            self.boot_timeout_entry.insert(0, str(config['boot_timeout']))
