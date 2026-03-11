"""OS 引导配置 Tab - 包含多种引导方式的子选项."""

import customtkinter as ctk

from ..inner_tab_panel import InnerTabPanel
from ..styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class GuestFirmwareTab(ctk.CTkFrame):
    """Guest firmware 引导配置."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent')
        self.on_change_callback = on_change_callback

        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        left_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        left_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        left_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(left_frame, text='固件配置', font=CTK_FONT_BOLD, text_color='#64b5f6').grid(
            row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
        )

        ctk.CTkLabel(left_frame, text='固件类型:', font=CTK_FONT_MAIN, width=90, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.firmware_type = ctk.CTkOptionMenu(
            left_frame,
            values=['bios', 'efi'],
            width=120,
            font=CTK_FONT_SMALL,
        )
        self.firmware_type.set('bios')
        self.firmware_type.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.firmware_type.configure(command=self._trigger_change)

        ctk.CTkLabel(left_frame, text='OS 类型:', font=CTK_FONT_MAIN, width=90, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.os_type = ctk.CTkOptionMenu(
            left_frame,
            values=['hvm', 'linux', 'exe'],
            width=120,
            font=CTK_FONT_SMALL,
        )
        self.os_type.set('hvm')
        self.os_type.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.os_type.configure(command=self._trigger_change)

        ctk.CTkLabel(left_frame, text='架构:', font=CTK_FONT_MAIN, width=90, anchor='w').grid(
            row=3, column=0, padx=10, pady=5, sticky='w'
        )
        self.arch = ctk.CTkOptionMenu(
            left_frame,
            values=[
                'x86_64',
                'aarch64',
                # 'i686','armv7l', 'ppc64', 'ppc64le', 's390x', 'riscv64'
            ],
            width=120,
            font=CTK_FONT_SMALL,
        )
        self.arch.set('x86_64')
        self.arch.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        self.arch.configure(command=self._trigger_change)

        ctk.CTkLabel(
            left_frame, text='Loader 路径:', font=CTK_FONT_MAIN, width=90, anchor='w'
        ).grid(row=4, column=0, padx=10, pady=5, sticky='w')
        self.loader_path = ctk.CTkEntry(left_frame, placeholder_text='固件路径 (可选)', width=200)
        self.loader_path.grid(row=4, column=1, padx=5, pady=5, sticky='ew')
        self.loader_path.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(left_frame, text='NVRAM 路径:', font=CTK_FONT_MAIN, width=90, anchor='w').grid(
            row=5, column=0, padx=10, pady=5, sticky='w'
        )
        self.nvram_path = ctk.CTkEntry(left_frame, placeholder_text='NVRAM 路径 (可选)', width=200)
        self.nvram_path.grid(row=5, column=1, padx=5, pady=5, sticky='ew')
        self.nvram_path.bind('<KeyRelease>', lambda e: self._trigger_change())

        right_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        right_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        right_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(right_frame, text='启动选项', font=CTK_FONT_BOLD, text_color='#4caf50').grid(
            row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
        )

        ctk.CTkLabel(right_frame, text='启动设备:', font=CTK_FONT_MAIN, width=90, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.boot_dev = ctk.CTkOptionMenu(
            right_frame,
            values=['hd', 'cdrom', 'network', 'fd'],
            width=120,
            font=CTK_FONT_SMALL,
        )
        self.boot_dev.set('hd')
        self.boot_dev.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.boot_dev.configure(command=self._trigger_change)

        ctk.CTkLabel(right_frame, text='启动菜单:', font=CTK_FONT_MAIN, width=90, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.boot_menu = ctk.CTkCheckBox(
            right_frame, text='启用', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.boot_menu.grid(row=2, column=1, padx=5, pady=5, sticky='w')

        ctk.CTkLabel(
            right_frame, text='菜单超时(ms):', font=CTK_FONT_MAIN, width=90, anchor='w'
        ).grid(row=3, column=0, padx=10, pady=5, sticky='w')
        self.boot_timeout = ctk.CTkEntry(right_frame, placeholder_text='3000', width=80)
        self.boot_timeout.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        self.boot_timeout.insert(0, '3000')
        self.boot_timeout.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(
            right_frame, text='Secure Boot:', font=CTK_FONT_MAIN, width=90, anchor='w'
        ).grid(row=4, column=0, padx=10, pady=5, sticky='w')
        self.secure_boot = ctk.CTkCheckBox(
            right_frame, text='启用', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.secure_boot.grid(row=4, column=1, padx=5, pady=5, sticky='w')

        ctk.CTkLabel(right_frame, text='SMBIOS:', font=CTK_FONT_MAIN, width=90, anchor='w').grid(
            row=5, column=0, padx=10, pady=5, sticky='w'
        )
        self.smbios_mode = ctk.CTkOptionMenu(
            right_frame,
            values=['emulate', 'host', 'sysinfo'],
            width=120,
            font=CTK_FONT_SMALL,
        )
        self.smbios_mode.set('emulate')
        self.smbios_mode.grid(row=5, column=1, padx=5, pady=5, sticky='w')
        self.smbios_mode.configure(command=self._trigger_change)

    def _trigger_change(self):
        """触发变化回调."""
        if self.on_change_callback:
            self.on_change_callback()

    def get_config(self) -> dict:
        """获取配置数据."""
        return {
            'type': 'guest_firmware',
            'firmware': self.firmware_type.get(),
            'os_type': self.os_type.get(),
            'arch': self.arch.get(),
            'loader_path': self.loader_path.get().strip(),
            'nvram_path': self.nvram_path.get().strip(),
            'boot_dev': self.boot_dev.get(),
            'boot_menu': self.boot_menu.get(),
            'boot_timeout': int(self.boot_timeout.get().strip() or '3000'),
            'secure_boot': self.secure_boot.get(),
            'smbios_mode': self.smbios_mode.get(),
        }


class DirectKernelTab(ctk.CTkFrame):
    """直接内核引导配置."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent')
        self.on_change_callback = on_change_callback

        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        left_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        left_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        left_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(left_frame, text='内核引导', font=CTK_FONT_BOLD, text_color='#ff9800').grid(
            row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
        )

        ctk.CTkLabel(left_frame, text='内核路径:', font=CTK_FONT_MAIN, width=90, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.kernel_path = ctk.CTkEntry(left_frame, placeholder_text='/path/to/vmlinuz', width=200)
        self.kernel_path.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        self.kernel_path.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(
            left_frame, text='Initrd 路径:', font=CTK_FONT_MAIN, width=90, anchor='w'
        ).grid(row=2, column=0, padx=10, pady=5, sticky='w')
        self.initrd_path = ctk.CTkEntry(
            left_frame, placeholder_text='/path/to/initrd (可选)', width=200
        )
        self.initrd_path.grid(row=2, column=1, padx=5, pady=5, sticky='ew')
        self.initrd_path.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(left_frame, text='DTB 路径:', font=CTK_FONT_MAIN, width=90, anchor='w').grid(
            row=3, column=0, padx=10, pady=5, sticky='w'
        )
        self.dtb_path = ctk.CTkEntry(left_frame, placeholder_text='设备树 (可选)', width=200)
        self.dtb_path.grid(row=3, column=1, padx=5, pady=5, sticky='ew')
        self.dtb_path.bind('<KeyRelease>', lambda e: self._trigger_change())

        right_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        right_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        right_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(right_frame, text='启动参数', font=CTK_FONT_BOLD, text_color='#9c27b0').grid(
            row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
        )

        ctk.CTkLabel(right_frame, text='命令行:', font=CTK_FONT_MAIN, width=90, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.cmdline = ctk.CTkEntry(right_frame, placeholder_text='console=ttyS0', width=200)
        self.cmdline.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        self.cmdline.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(right_frame, text='Shim 路径:', font=CTK_FONT_MAIN, width=90, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.shim_path = ctk.CTkEntry(right_frame, placeholder_text='UEFI shim (可选)', width=200)
        self.shim_path.grid(row=2, column=1, padx=5, pady=5, sticky='ew')
        self.shim_path.bind('<KeyRelease>', lambda e: self._trigger_change())

    def _trigger_change(self):
        """触发变化回调."""
        if self.on_change_callback:
            self.on_change_callback()

    def get_config(self) -> dict:
        """获取配置数据."""
        return {
            'type': 'direct_kernel',
            'kernel': self.kernel_path.get().strip(),
            'initrd': self.initrd_path.get().strip(),
            'dtb': self.dtb_path.get().strip(),
            'cmdline': self.cmdline.get().strip(),
            'shim': self.shim_path.get().strip(),
        }


class ContainerBootTab(ctk.CTkFrame):
    """容器引导配置."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent')
        self.on_change_callback = on_change_callback

        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        left_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        left_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        left_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(left_frame, text='容器配置', font=CTK_FONT_BOLD, text_color='#2196f3').grid(
            row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
        )

        ctk.CTkLabel(left_frame, text='Init 路径:', font=CTK_FONT_MAIN, width=90, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.init_path = ctk.CTkEntry(left_frame, placeholder_text='/bin/systemd', width=200)
        self.init_path.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        self.init_path.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(left_frame, text='Init 参数:', font=CTK_FONT_MAIN, width=90, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.init_args = ctk.CTkEntry(left_frame, placeholder_text='启动参数 (可选)', width=200)
        self.init_args.grid(row=2, column=1, padx=5, pady=5, sticky='ew')
        self.init_args.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(left_frame, text='工作目录:', font=CTK_FONT_MAIN, width=90, anchor='w').grid(
            row=3, column=0, padx=10, pady=5, sticky='w'
        )
        self.init_dir = ctk.CTkEntry(left_frame, placeholder_text='工作目录 (可选)', width=200)
        self.init_dir.grid(row=3, column=1, padx=5, pady=5, sticky='ew')
        self.init_dir.bind('<KeyRelease>', lambda e: self._trigger_change())

        right_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        right_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        right_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(right_frame, text='用户/组', font=CTK_FONT_BOLD, text_color='#7986cb').grid(
            row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
        )

        ctk.CTkLabel(right_frame, text='用户:', font=CTK_FONT_MAIN, width=90, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.init_user = ctk.CTkEntry(right_frame, placeholder_text='用户名或UID', width=150)
        self.init_user.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.init_user.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(right_frame, text='组:', font=CTK_FONT_MAIN, width=90, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.init_group = ctk.CTkEntry(right_frame, placeholder_text='组名或GID', width=150)
        self.init_group.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.init_group.bind('<KeyRelease>', lambda e: self._trigger_change())

    def _trigger_change(self):
        """触发变化回调."""
        if self.on_change_callback:
            self.on_change_callback()

    def get_config(self) -> dict:
        """获取配置数据."""
        return {
            'type': 'container',
            'init': self.init_path.get().strip(),
            'init_args': self.init_args.get().strip(),
            'init_dir': self.init_dir.get().strip(),
            'init_user': self.init_user.get().strip(),
            'init_group': self.init_group.get().strip(),
        }


class HostBootloaderTab(ctk.CTkFrame):
    """Host bootloader 配置."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent')
        self.on_change_callback = on_change_callback

        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面."""
        self.grid_columnconfigure(0, weight=1)

        frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(frame, text='Host Bootloader', font=CTK_FONT_BOLD, text_color='#e91e63').grid(
            row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
        )

        ctk.CTkLabel(frame, text='Bootloader:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.bootloader_path = ctk.CTkEntry(frame, placeholder_text='/usr/bin/pygrub', width=250)
        self.bootloader_path.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        self.bootloader_path.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(frame, text='参数:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.bootloader_args = ctk.CTkEntry(frame, placeholder_text='--append single', width=250)
        self.bootloader_args.grid(row=2, column=1, padx=5, pady=5, sticky='ew')
        self.bootloader_args.bind('<KeyRelease>', lambda e: self._trigger_change())

    def _trigger_change(self):
        """触发变化回调."""
        if self.on_change_callback:
            self.on_change_callback()

    def get_config(self) -> dict:
        """获取配置数据."""
        return {
            'type': 'host_bootloader',
            'bootloader': self.bootloader_path.get().strip(),
            'bootloader_args': self.bootloader_args.get().strip(),
        }


class OSBootingTab(ctk.CTkFrame):
    """OS 引导配置 Tab - 包含多种引导方式."""

    SUB_TABS_CONFIG = {
        'guest_firmware': {
            'name': '固件引导',
            'class': GuestFirmwareTab,
            'default': True,
        },
        'direct_kernel': {
            'name': '内核引导',
            'class': DirectKernelTab,
            'default': False,
        },
        'container': {
            'name': '容器引导',
            'class': ContainerBootTab,
            'default': False,
        },
        'host_bootloader': {
            'name': 'Host引导',
            'class': HostBootloaderTab,
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

    def get_config(self) -> dict:
        """获取配置数据."""
        current = self.inner_panel.get_current_tab()
        instance = self.inner_panel.get_tab_instance(current)
        if instance and hasattr(instance, 'get_config'):
            return instance.get_config()
        return {'type': 'guest_firmware'}

    def to_xml(self) -> dict:
        """生成XML配置字典."""
        return {'os_booting': self.get_config()}
