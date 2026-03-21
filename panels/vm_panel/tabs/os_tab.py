"""引导/OS 配置 Tab - 按 libvirt Domain XML format 第 3 章重构."""

from typing import ClassVar

import customtkinter as ctk

from components.base_tab import SectionConfig, StandardConfigTab


class OSTab(StandardConfigTab):
    """引导/OS 配置 Tab."""

    SECTIONS: ClassVar[dict] = {
        'firmware': SectionConfig(
            title='固件',
            fields=[
                # firmware section 的所有 UI 都通过 _init_sections_ui 中的自定义代码创建
            ],
            color='#FF6B6B',
        ),
        'boot': SectionConfig(
            title='引导',
            fields=[
                # boot section 的所有 UI 都通过 _init_sections_ui 中的自定义代码创建
            ],
            color='#4ECDC4',
        ),
        'container': SectionConfig(
            title='容器启动',
            fields=[
                # container section 的标准字段通过自定义代码创建，全部放一行
            ],
            color='#AA96DA',
        ),
    }

    def __init__(self, master, on_change_callback=None, **kwargs):
        # 动态添加 initarg/initenv 支持
        self.initargs = []
        self.initenvs = []

        super().__init__(master, on_change_callback, **kwargs)

    def _init_sections_ui(self) -> None:
        """初始化基于 Sections 的 UI，添加 boot devices 和 initarg/initenv/idmap 支持."""
        super()._init_sections_ui()

        # 在 firmware section 添加自定义 UI
        firmware_frame = self.section_frames['firmware']
        firmware_row = 1  # 从第1行开始（第0行是标题）

        # === 基本信息 ===
        ctk.CTkLabel(firmware_frame, text='基本信息', font=('', 11), text_color='#FFD93D').grid(
            row=firmware_row, column=0, columnspan=2, padx=10, pady=3, sticky='w'
        )
        firmware_row += 1

        # firmware、type、arch、machine 全部放一行
        self._create_firmware_basic_row(firmware_frame, firmware_row)
        firmware_row += 1

        # === Loader 配置 ===
        ctk.CTkLabel(firmware_frame, text='Loader 配置', font=('', 11), text_color='#FFD93D').grid(
            row=firmware_row, column=0, columnspan=2, padx=10, pady=3, sticky='w'
        )
        firmware_row += 1

        # loader、format、readonly、secure、stateless 全部放一行
        self._create_loader_row(firmware_frame, firmware_row)
        firmware_row += 1

        # === NVRAM 配置 ===
        ctk.CTkLabel(firmware_frame, text='NVRAM 配置', font=('', 11), text_color='#FFD93D').grid(
            row=firmware_row, column=0, columnspan=2, padx=10, pady=3, sticky='w'
        )
        firmware_row += 1

        # nvram、template、type、format 全部放一行
        rows_used = self._create_nvram_row(firmware_frame, firmware_row)
        firmware_row += rows_used

        # === Varstore 配置 ===
        ctk.CTkLabel(
            firmware_frame, text='Varstore 配置', font=('', 11), text_color='#FFD93D'
        ).grid(row=firmware_row, column=0, columnspan=2, padx=10, pady=3, sticky='w')
        firmware_row += 1

        # varstore 和 varstore_template 放一行
        self._create_varstore_row(firmware_frame, firmware_row)
        firmware_row += 1

        self.section_rows['firmware'] = firmware_row

        # 在 boot section 添加自定义 UI
        boot_frame = self.section_frames['boot']
        boot_row = 1  # 从第1行开始（第0行是标题）

        # === 引导设备 ===
        ctk.CTkLabel(boot_frame, text='引导设备', font=('', 11), text_color='#FFD93D').grid(
            row=boot_row, column=0, columnspan=2, padx=10, pady=3, sticky='w'
        )
        boot_row += 1

        # boot: 标签、按钮和设备放在同一行
        boot_header_frame = ctk.CTkFrame(boot_frame, fg_color='transparent')
        boot_header_frame.grid(row=boot_row, column=0, columnspan=2, padx=10, pady=3, sticky='w')

        ctk.CTkLabel(boot_header_frame, text='boot:', font=('', 11), text_color='#4ECDC4').pack(
            side='left', padx=0
        )

        # 加减号按钮紧跟在 boot: 后面
        ctk.CTkButton(
            boot_header_frame, text='+', width=5, height=10, command=self._add_boot_device
        ).pack(side='left', padx=(10, 2))
        ctk.CTkButton(
            boot_header_frame, text='-', width=5, height=10, command=self._remove_boot_device
        ).pack(side='left', padx=2)

        # boot 设备列表紧跟在加减号后面，使用 pack 横向排列
        self.boot_devices_frame = ctk.CTkFrame(boot_header_frame, fg_color='transparent')
        self.boot_devices_frame.pack(side='left', padx=(10, 0))
        self._add_boot_device()

        boot_row += 1

        # 添加标准字段: bootmenu, bootmenu_timeout, smbios, bios_useserial, bios_reboot
        self._create_boot_standard_fields(boot_frame, boot_row)
        boot_row += 1  # 所有字段在一行

        # === 引导程序 ===
        ctk.CTkLabel(boot_frame, text='引导程序', font=('', 11), text_color='#FFD93D').grid(
            row=boot_row, column=0, columnspan=2, padx=10, pady=3, sticky='w'
        )
        boot_row += 1

        # bootloader 和 bootloader_args 放一行
        self._create_bootloader_row(boot_frame, boot_row)
        boot_row += 1

        # === 内核启动 ===
        ctk.CTkLabel(
            boot_frame, text='内核启动 (直接指定内核镜像)', font=('', 11), text_color='#FFD93D'
        ).grid(row=boot_row, column=0, columnspan=2, padx=10, pady=3, sticky='w')
        boot_row += 1

        # kernel 和 initrd 放一行，cmdline 和 shim 放一行，dtb 单独一行
        self._create_kernel_rows(boot_frame, boot_row)
        boot_row += 3

        # === ACPI 表配置 ===
        acpi_header_frame = ctk.CTkFrame(boot_frame, fg_color='transparent')
        acpi_header_frame.grid(row=boot_row, column=0, columnspan=2, padx=10, pady=3, sticky='w')

        ctk.CTkLabel(
            acpi_header_frame, text='ACPI 表配置', font=('', 11), text_color='#FFD93D'
        ).pack(side='left', padx=0)

        # 加减号按钮
        ctk.CTkButton(
            acpi_header_frame, text='+', width=5, height=10, command=self._add_acpi_table
        ).pack(side='left', padx=(10, 2))
        ctk.CTkButton(
            acpi_header_frame, text='-', width=5, height=10, command=self._remove_acpi_table
        ).pack(side='left', padx=2)

        boot_row += 1

        # ACPI 表列表
        self.acpi_tables_frame = ctk.CTkFrame(boot_frame, fg_color='transparent')
        self.acpi_tables_frame.grid(
            row=boot_row, column=0, columnspan=2, padx=10, pady=3, sticky='w'
        )
        self.acpi_tables = []
        self._add_acpi_table()

        boot_row += 1

        self.section_rows['boot'] = boot_row

        # 在 container section 添加 init/initdir/inituser/initgroup 一行显示
        container_frame = self.section_frames['container']
        container_row = 1  # 从第1行开始（第0行是标题）

        # init, initdir, inituser, initgroup 全部放一行
        self._create_container_basic_row(container_frame, container_row)
        container_row += 1

        # initarg: 标签和按钮放在同一行
        initarg_header_frame = ctk.CTkFrame(container_frame, fg_color='transparent')
        initarg_header_frame.grid(row=container_row, column=0, padx=10, pady=3, sticky='w')

        ctk.CTkLabel(
            initarg_header_frame, text='initarg:', font=('', 11), text_color='#AA96DA'
        ).pack(side='left', padx=0)

        # 加减号按钮紧跟在 initarg: 后面
        ctk.CTkButton(
            initarg_header_frame, text='+', width=25, height=20, command=self._add_initarg
        ).pack(side='left', padx=(10, 2))
        ctk.CTkButton(
            initarg_header_frame, text='-', width=25, height=20, command=self._remove_initarg
        ).pack(side='left', padx=2)

        self.initargs_frame = ctk.CTkFrame(container_frame, fg_color='transparent')
        self.initargs_frame.grid(row=container_row, column=1, padx=10, pady=3, sticky='ew')
        self.initargs_frame.grid_columnconfigure(0, weight=1)
        self._add_initarg()

        container_row += 1

        # initenv: 标签和按钮放在同一行
        initenv_header_frame = ctk.CTkFrame(container_frame, fg_color='transparent')
        initenv_header_frame.grid(row=container_row, column=0, padx=10, pady=3, sticky='w')

        ctk.CTkLabel(
            initenv_header_frame, text='initenv:', font=('', 11), text_color='#AA96DA'
        ).pack(side='left', padx=0)

        # 加减号按钮紧跟在 initenv: 后面
        ctk.CTkButton(
            initenv_header_frame, text='+', width=25, height=20, command=self._add_initenv
        ).pack(side='left', padx=(10, 2))
        ctk.CTkButton(
            initenv_header_frame, text='-', width=25, height=20, command=self._remove_initenv
        ).pack(side='left', padx=2)

        self.initenvs_frame = ctk.CTkFrame(container_frame, fg_color='transparent')
        self.initenvs_frame.grid(row=container_row, column=1, padx=10, pady=3, sticky='ew')
        self.initenvs_frame.grid_columnconfigure(0, weight=1)
        self.initenvs_frame.grid_columnconfigure(1, weight=1)
        self._add_initenv()

        container_row += 1

        # ID 映射 (容器多用户权限映射)
        self._init_idmap_ui(container_frame, container_row)

        self.section_rows['container'] = container_row + 3

    def _init_idmap_ui(self, parent: ctk.CTkFrame, start_row: int) -> None:
        """初始化 ID 映射 UI.

        布局设计:
        - 第一行: ID 映射 (容器多用户权限映射) 标题 + checkbox 开关
        - 第二行: uid 标签 + start/target/count 输入框(placeholder显示表头)
        - 第三行: gid 标签 + start/target/count 输入框(placeholder显示表头)
        """
        # 标题行 + checkbox 开关
        header_frame = ctk.CTkFrame(parent, fg_color='transparent')
        header_frame.grid(row=start_row, column=0, columnspan=2, padx=10, pady=5, sticky='w')

        ctk.CTkLabel(
            header_frame, text='ID 映射 (容器多用户权限映射):', font=('', 11), text_color='#FFD93D'
        ).pack(side='left', padx=0)

        # ID 映射启用开关 (使用 checkbox)
        self.idmap_enabled = ctk.CTkCheckBox(
            header_frame, text='', width=20, command=self._on_idmap_toggle
        )
        self.idmap_enabled.pack(side='left', padx=(10, 0))
        self.idmap_enabled.deselect()  # 默认关闭

        # 内容框架 (包含输入框)
        self.idmap_content_frame = ctk.CTkFrame(parent, fg_color='transparent')
        self.idmap_content_frame.grid(
            row=start_row + 1, column=0, columnspan=2, padx=10, pady=2, sticky='w'
        )

        # ID 映射输入框
        self.idmap_entries = {}

        # 注册数字验证命令
        vcmd = (self.register(self._validate_number), '%P')

        # uid 行
        uid_frame = ctk.CTkFrame(self.idmap_content_frame, fg_color='transparent')
        uid_frame.grid(row=0, column=0, columnspan=4, padx=0, pady=2, sticky='w')

        ctk.CTkLabel(uid_frame, text='uid', font=('', 10), width=40, anchor='w').pack(
            side='left', padx=(0, 5)
        )

        for field_name, placeholder in [
            ('uid_start', 'start'),
            ('uid_target', 'target'),
            ('uid_count', 'count'),
        ]:
            entry = ctk.CTkEntry(
                uid_frame,
                width=60,
                font=('', 10),
                placeholder_text=placeholder,
                validate='key',
                validatecommand=vcmd,
            )
            entry.pack(side='left', padx=5)
            entry.bind('<KeyRelease>', lambda e: self._trigger_change())
            self.idmap_entries[field_name] = entry

        # gid 行
        gid_frame = ctk.CTkFrame(self.idmap_content_frame, fg_color='transparent')
        gid_frame.grid(row=1, column=0, columnspan=4, padx=0, pady=2, sticky='w')

        ctk.CTkLabel(gid_frame, text='gid', font=('', 10), width=40, anchor='w').pack(
            side='left', padx=(0, 5)
        )

        for field_name, placeholder in [
            ('gid_start', 'start'),
            ('gid_target', 'target'),
            ('gid_count', 'count'),
        ]:
            entry = ctk.CTkEntry(
                gid_frame,
                width=60,
                font=('', 10),
                placeholder_text=placeholder,
                validate='key',
                validatecommand=vcmd,
            )
            entry.pack(side='left', padx=5)
            entry.bind('<KeyRelease>', lambda e: self._trigger_change())
            self.idmap_entries[field_name] = entry

        # 初始状态：禁用输入框
        self._update_idmap_ui_state()

    def _create_boot_standard_fields(self, parent: ctk.CTkFrame, start_row: int) -> None:
        """创建 boot section 的标准字段: bootmenu, bootmenu_timeout, smbios, bios_useserial, bios_reboot.

        布局: 全部字段放在同一行

        Args:
            parent: 父容器 (boot_frame)
            start_row: 起始行号
        """
        # 所有字段放在同一行
        row_frame = ctk.CTkFrame(parent, fg_color='transparent')
        row_frame.grid(row=start_row, column=0, columnspan=2, padx=5, pady=2, sticky='w')

        # bootmenu
        ctk.CTkLabel(row_frame, text='bootmenu:', font=('', 10), width=55, anchor='w').pack(
            side='left', padx=(0, 3)
        )
        self.bootmenu_checkbox = ctk.CTkCheckBox(
            row_frame, text='', font=('', 10), width=20, command=self._trigger_change
        )
        self.bootmenu_checkbox.pack(side='left', padx=3)

        # bootmenu_timeout
        ctk.CTkLabel(row_frame, text='timeout:', font=('', 10), width=45, anchor='w').pack(
            side='left', padx=(10, 3)
        )
        self.bootmenu_timeout_entry = ctk.CTkEntry(
            row_frame, placeholder_text='3000', width=50, font=('', 10)
        )
        self.bootmenu_timeout_entry.pack(side='left', padx=3)
        self.bootmenu_timeout_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        # smbios
        ctk.CTkLabel(row_frame, text='smbios:', font=('', 10), width=45, anchor='w').pack(
            side='left', padx=(10, 3)
        )
        self.smbios_option = ctk.CTkOptionMenu(
            row_frame,
            values=['None', 'emulate', 'host', 'sysinfo'],
            width=70,
            font=('', 10),
        )
        self.smbios_option.set('emulate')
        self.smbios_option.pack(side='left', padx=3)
        self.smbios_option.configure(command=self._trigger_change)

        # bios_useserial
        ctk.CTkLabel(row_frame, text='useserial:', font=('', 10), width=55, anchor='w').pack(
            side='left', padx=(10, 3)
        )
        self.bios_useserial_checkbox = ctk.CTkCheckBox(
            row_frame, text='', font=('', 10), width=20, command=self._trigger_change
        )
        self.bios_useserial_checkbox.pack(side='left', padx=3)

        # bios_reboot
        ctk.CTkLabel(row_frame, text='reboot:', font=('', 10), width=45, anchor='w').pack(
            side='left', padx=(10, 3)
        )
        self.bios_reboot_entry = ctk.CTkEntry(
            row_frame, placeholder_text='-1', width=50, font=('', 10)
        )
        self.bios_reboot_entry.pack(side='left', padx=3)
        self.bios_reboot_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

    def _create_bootloader_row(self, parent: ctk.CTkFrame, row: int) -> None:
        """创建引导程序行: bootloader 和 bootloader_args 放一行."""
        frame = ctk.CTkFrame(parent, fg_color='transparent')
        frame.grid(row=row, column=0, columnspan=2, padx=10, pady=3, sticky='w')

        # bootloader 标签和输入框
        ctk.CTkLabel(frame, text='bootloader:', font=('', 11), width=30, anchor='w').pack(
            side='left', padx=(0, 5)
        )
        self.bootloader_entry = ctk.CTkEntry(
            frame, placeholder_text='/usr/bin/pygrub', width=140, font=('', 11)
        )
        self.bootloader_entry.pack(side='left', padx=5)
        self.bootloader_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        # bootloader_args 标签和输入框
        ctk.CTkLabel(frame, text='args:', font=('', 11), width=40, anchor='w').pack(
            side='left', padx=(15, 5)
        )
        self.bootloader_args_entry = ctk.CTkEntry(
            frame, placeholder_text='--append single', width=140, font=('', 11)
        )
        self.bootloader_args_entry.pack(side='left', padx=5)
        self.bootloader_args_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

    def _create_kernel_rows(self, parent: ctk.CTkFrame, start_row: int) -> None:
        """创建内核启动行: kernel 和 initrd 放一行，cmdline 和 shim 放一行."""
        # 第一行: kernel 和 initrd
        row1_frame = ctk.CTkFrame(parent, fg_color='transparent')
        row1_frame.grid(row=start_row, column=0, columnspan=2, padx=10, pady=3, sticky='w')

        ctk.CTkLabel(row1_frame, text='kernel:', font=('', 11), width=30, anchor='w').pack(
            side='left', padx=(0, 5)
        )
        self.kernel_entry = ctk.CTkEntry(
            row1_frame, placeholder_text='/root/vmlinuz', width=140, font=('', 11)
        )
        self.kernel_entry.pack(side='left', padx=5)
        self.kernel_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(row1_frame, text='initrd:', font=('', 11), width=50, anchor='w').pack(
            side='left', padx=(15, 5)
        )
        self.initrd_entry = ctk.CTkEntry(
            row1_frame, placeholder_text='/root/initrd', width=140, font=('', 11)
        )
        self.initrd_entry.pack(side='left', padx=5)
        self.initrd_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        # 第二行: cmdline 和 shim
        row2_frame = ctk.CTkFrame(parent, fg_color='transparent')
        row2_frame.grid(row=start_row + 1, column=0, columnspan=2, padx=10, pady=3, sticky='w')

        ctk.CTkLabel(row2_frame, text='cmdline:', font=('', 11), width=30, anchor='w').pack(
            side='left', padx=(0, 5)
        )
        self.cmdline_entry = ctk.CTkEntry(
            row2_frame, placeholder_text='console=ttyS0', width=140, font=('', 11)
        )
        self.cmdline_entry.pack(side='left', padx=5)
        self.cmdline_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(row2_frame, text='shim:', font=('', 11), width=50, anchor='w').pack(
            side='left', padx=(15, 5)
        )
        self.shim_entry = ctk.CTkEntry(
            row2_frame, placeholder_text='/path/to/shim.efi', width=140, font=('', 11)
        )
        self.shim_entry.pack(side='left', padx=5)
        self.shim_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        # dtb 单独一行
        row3_frame = ctk.CTkFrame(parent, fg_color='transparent')
        row3_frame.grid(row=start_row + 2, column=0, columnspan=2, padx=10, pady=3, sticky='w')

        ctk.CTkLabel(row3_frame, text='dtb:', font=('', 11), width=30, anchor='w').pack(
            side='left', padx=(0, 5)
        )
        self.dtb_entry = ctk.CTkEntry(
            row3_frame, placeholder_text='/root/ppc.dtb', width=300, font=('', 11)
        )
        self.dtb_entry.pack(side='left', padx=5)
        self.dtb_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

    # === 固件部分辅助方法 ===

    def _create_firmware_basic_row(self, parent: ctk.CTkFrame, row: int) -> None:
        """创建固件基本信息行: firmware、type、arch、machine 全部放一行."""
        frame = ctk.CTkFrame(parent, fg_color='transparent')
        frame.grid(row=row, column=0, columnspan=2, padx=10, pady=3, sticky='w')

        # firmware
        ctk.CTkLabel(frame, text='firmware:', font=('', 11), width=60, anchor='w').pack(
            side='left', padx=(0, 3)
        )
        self.firmware_option = ctk.CTkOptionMenu(
            frame, values=['无', 'bios', 'efi'], width=70, font=('', 11)
        )
        self.firmware_option.set('无')
        self.firmware_option.pack(side='left', padx=3)
        self.firmware_option.configure(command=self._trigger_change)

        # type
        ctk.CTkLabel(frame, text='type:', font=('', 11), width=40, anchor='w').pack(
            side='left', padx=(10, 3)
        )
        self.type_option = ctk.CTkOptionMenu(
            frame, values=['hvm', 'linux', 'exe'], width=70, font=('', 11)
        )
        self.type_option.set('hvm')
        self.type_option.pack(side='left', padx=3)
        self.type_option.configure(command=self._trigger_change)

        # arch
        ctk.CTkLabel(frame, text='arch:', font=('', 11), width=40, anchor='w').pack(
            side='left', padx=(10, 3)
        )
        self.arch_option = ctk.CTkOptionMenu(
            frame,
            values=['None', 'x86_64', 'i686', 'aarch64', 'armv7l', 'ppc64', 'ppc64le', 's390x'],
            width=70,
            font=('', 11),
        )
        self.arch_option.set('None')
        self.arch_option.pack(side='left', padx=3)
        self.arch_option.configure(command=self._trigger_change)

        # machine
        ctk.CTkLabel(frame, text='machine:', font=('', 11), width=50, anchor='w').pack(
            side='left', padx=(10, 3)
        )
        self.machine_option = ctk.CTkOptionMenu(
            frame,
            values=['None', 'q35', 'pc', 'isapc', 'vexpress', 'virt', 'peium'],
            width=70,
            font=('', 11),
        )
        self.machine_option.set('None')
        self.machine_option.pack(side='left', padx=3)
        self.machine_option.configure(command=self._trigger_change)

    def _create_loader_row(self, parent: ctk.CTkFrame, row: int) -> None:
        """创建 Loader 配置行: loader、format、readonly、secure、stateless 全部放一行."""
        frame = ctk.CTkFrame(parent, fg_color='transparent')
        frame.grid(row=row, column=0, columnspan=2, padx=10, pady=3, sticky='w')

        # loader
        ctk.CTkLabel(frame, text='loader:', font=('', 11), width=50, anchor='w').pack(
            side='left', padx=(0, 3)
        )
        self.loader_entry = ctk.CTkEntry(
            frame, placeholder_text='/usr/share/OVMF/OVMF_CODE.fd', width=100, font=('', 11)
        )
        self.loader_entry.pack(side='left', padx=3)
        self.loader_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        # format
        ctk.CTkLabel(frame, text='format:', font=('', 11), width=50, anchor='w').pack(
            side='left', padx=(10, 3)
        )
        self.loader_format_option = ctk.CTkOptionMenu(
            frame, values=['raw', 'qcow2'], width=70, font=('', 11)
        )
        self.loader_format_option.set('raw')
        self.loader_format_option.pack(side='left', padx=3)
        self.loader_format_option.configure(command=self._trigger_change)

        # readonly
        ctk.CTkLabel(frame, text='readonly:', font=('', 11), width=55, anchor='w').pack(
            side='left', padx=(10, 3)
        )
        self.loader_readonly_checkbox = ctk.CTkCheckBox(
            frame, text='', font=('', 11), width=20, command=self._trigger_change
        )
        self.loader_readonly_checkbox.pack(side='left', padx=3)

        # secure
        ctk.CTkLabel(frame, text='secure:', font=('', 11), width=45, anchor='w').pack(
            side='left', padx=(10, 3)
        )
        self.loader_secure_checkbox = ctk.CTkCheckBox(
            frame, text='', font=('', 11), width=20, command=self._trigger_change
        )
        self.loader_secure_checkbox.pack(side='left', padx=3)

        # stateless
        ctk.CTkLabel(frame, text='stateless:', font=('', 11), width=55, anchor='w').pack(
            side='left', padx=(10, 3)
        )
        self.loader_stateless_checkbox = ctk.CTkCheckBox(
            frame, text='', font=('', 11), width=20, command=self._trigger_change
        )
        self.loader_stateless_checkbox.pack(side='left', padx=3)

    def _create_nvram_row(self, parent: ctk.CTkFrame, row: int) -> int:
        """创建 NVRAM 配置行: 支持 file/block/network 类型切换.

        Args:
            parent: 父容器
            row: 起始行号

        Returns:
            实际占用的行数
        """
        # 第一行: 基础配置 (type, format, template)
        frame = ctk.CTkFrame(parent, fg_color='transparent')
        frame.grid(row=row, column=0, columnspan=2, padx=10, pady=3, sticky='w')

        # type
        ctk.CTkLabel(frame, text='type:', font=('', 11), width=40, anchor='w').pack(
            side='left', padx=(0, 3)
        )
        self.nvram_type_option = ctk.CTkOptionMenu(
            frame, values=['file', 'block', 'network'], width=70, font=('', 11)
        )
        self.nvram_type_option.set('file')
        self.nvram_type_option.pack(side='left', padx=3)
        self.nvram_type_option.configure(command=self._on_nvram_type_change)

        # format
        ctk.CTkLabel(frame, text='format:', font=('', 11), width=50, anchor='w').pack(
            side='left', padx=(10, 3)
        )
        self.nvram_format_option = ctk.CTkOptionMenu(
            frame, values=['raw', 'qcow2'], width=70, font=('', 11)
        )
        self.nvram_format_option.set('raw')
        self.nvram_format_option.pack(side='left', padx=3)
        self.nvram_format_option.configure(command=self._trigger_change)

        # template (file/block 类型使用)
        ctk.CTkLabel(frame, text='template:', font=('', 11), width=55, anchor='w').pack(
            side='left', padx=(10, 3)
        )
        self.nvram_template_entry = ctk.CTkEntry(
            frame, placeholder_text='/usr/share/OVMF/OVMF_VARS.fd', width=140, font=('', 11)
        )
        self.nvram_template_entry.pack(side='left', padx=3)
        self.nvram_template_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        # 第二行: file/block 类型的 source file 路径
        self.nvram_file_frame = ctk.CTkFrame(parent, fg_color='transparent')
        self.nvram_file_frame.grid(row=row + 1, column=0, columnspan=2, padx=10, pady=3, sticky='w')

        ctk.CTkLabel(
            self.nvram_file_frame, text='source file:', font=('', 11), width=70, anchor='w'
        ).pack(side='left', padx=(0, 3))
        self.nvram_file_entry = ctk.CTkEntry(
            self.nvram_file_frame,
            placeholder_text='/var/lib/libvirt/nvram/guest_VARS.fd',
            width=300,
            font=('', 11),
        )
        self.nvram_file_entry.pack(side='left', padx=3)
        self.nvram_file_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        # 第三行: network 类型的 source 配置
        self.nvram_network_frame = ctk.CTkFrame(parent, fg_color='transparent')
        self.nvram_network_frame.grid(
            row=row + 2, column=0, columnspan=2, padx=10, pady=3, sticky='w'
        )

        # protocol 和 name
        ctk.CTkLabel(
            self.nvram_network_frame, text='protocol:', font=('', 11), width=55, anchor='w'
        ).pack(side='left', padx=(0, 3))
        self.nvram_protocol_option = ctk.CTkOptionMenu(
            self.nvram_network_frame,
            values=['iscsi', 'rbd', 'sheepdog', 'gluster', 'nbd'],
            width=70,
            font=('', 11),
        )
        self.nvram_protocol_option.set('iscsi')
        self.nvram_protocol_option.pack(side='left', padx=3)
        self.nvram_protocol_option.configure(command=self._trigger_change)

        ctk.CTkLabel(
            self.nvram_network_frame, text='name:', font=('', 11), width=40, anchor='w'
        ).pack(side='left', padx=(10, 3))
        self.nvram_name_entry = ctk.CTkEntry(
            self.nvram_network_frame,
            placeholder_text='iqn.2013-07.com.example:iscsi-nopool/0',
            width=220,
            font=('', 11),
        )
        self.nvram_name_entry.pack(side='left', padx=3)
        self.nvram_name_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        # 第四行: network 类型的 host 配置
        self.nvram_host_frame = ctk.CTkFrame(parent, fg_color='transparent')
        self.nvram_host_frame.grid(row=row + 3, column=0, columnspan=2, padx=10, pady=3, sticky='w')

        ctk.CTkLabel(self.nvram_host_frame, text='host:', font=('', 11), width=40, anchor='w').pack(
            side='left', padx=(0, 3)
        )
        self.nvram_host_entry = ctk.CTkEntry(
            self.nvram_host_frame, placeholder_text='example.com', width=140, font=('', 11)
        )
        self.nvram_host_entry.pack(side='left', padx=3)
        self.nvram_host_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(self.nvram_host_frame, text='port:', font=('', 11), width=35, anchor='w').pack(
            side='left', padx=(10, 3)
        )
        self.nvram_port_entry = ctk.CTkEntry(
            self.nvram_host_frame, placeholder_text='6000', width=60, font=('', 11)
        )
        self.nvram_port_entry.pack(side='left', padx=3)
        self.nvram_port_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        # 第五行: network 类型的 auth 配置
        self.nvram_auth_frame = ctk.CTkFrame(parent, fg_color='transparent')
        self.nvram_auth_frame.grid(row=row + 4, column=0, columnspan=2, padx=10, pady=3, sticky='w')

        # auth 启用开关
        self.nvram_auth_enabled = ctk.CTkCheckBox(
            self.nvram_auth_frame,
            text='启用认证',
            font=('', 11),
            width=80,
            command=self._on_nvram_auth_toggle,
        )
        self.nvram_auth_enabled.pack(side='left', padx=(0, 10))
        self.nvram_auth_enabled.deselect()

        # auth 内容框架
        self.nvram_auth_content = ctk.CTkFrame(self.nvram_auth_frame, fg_color='transparent')
        self.nvram_auth_content.pack(side='left', padx=0)

        ctk.CTkLabel(
            self.nvram_auth_content, text='username:', font=('', 11), width=60, anchor='w'
        ).pack(side='left', padx=(0, 3))
        self.nvram_username_entry = ctk.CTkEntry(
            self.nvram_auth_content, placeholder_text='myname', width=80, font=('', 11)
        )
        self.nvram_username_entry.pack(side='left', padx=3)
        self.nvram_username_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(
            self.nvram_auth_content, text='secret type:', font=('', 11), width=70, anchor='w'
        ).pack(side='left', padx=(10, 3))
        self.nvram_secret_type_option = ctk.CTkOptionMenu(
            self.nvram_auth_content, values=['iscsi', 'ceph', 'tls'], width=70, font=('', 11)
        )
        self.nvram_secret_type_option.set('iscsi')
        self.nvram_secret_type_option.pack(side='left', padx=3)
        self.nvram_secret_type_option.configure(command=self._trigger_change)

        ctk.CTkLabel(
            self.nvram_auth_content, text='usage:', font=('', 11), width=45, anchor='w'
        ).pack(side='left', padx=(10, 3))
        self.nvram_secret_usage_entry = ctk.CTkEntry(
            self.nvram_auth_content, placeholder_text='mycluster_myname', width=120, font=('', 11)
        )
        self.nvram_secret_usage_entry.pack(side='left', padx=3)
        self.nvram_secret_usage_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        # 初始状态
        self._update_nvram_ui_state()

        return 5  # 返回实际占用的行数 (基础配置 + file配置 + network配置 + host配置 + auth配置)

    def _on_nvram_type_change(self, value: str | None = None) -> None:
        """处理 NVRAM 类型切换事件.

        Args:
            value: 选中的类型值 (CTkOptionMenu 回调传入)
        """
        self._update_nvram_ui_state()
        self._trigger_change()

    def _on_nvram_auth_toggle(self) -> None:
        """处理 NVRAM 认证开关切换事件."""
        self._update_nvram_auth_ui_state()
        self._trigger_change()

    def _update_nvram_ui_state(self) -> None:
        """根据 NVRAM 类型更新 UI 显示状态."""
        nvram_type = self.nvram_type_option.get()

        if nvram_type in ('file', 'block'):
            # 显示 file 相关配置
            self.nvram_file_frame.grid()
            self.nvram_network_frame.grid_remove()
            self.nvram_host_frame.grid_remove()
            self.nvram_auth_frame.grid_remove()
        elif nvram_type == 'network':
            # 显示 network 相关配置
            self.nvram_file_frame.grid_remove()
            self.nvram_network_frame.grid()
            self.nvram_host_frame.grid()
            self.nvram_auth_frame.grid()
            self._update_nvram_auth_ui_state()

    def _update_nvram_auth_ui_state(self) -> None:
        """根据认证开关状态更新认证 UI 的启用/禁用状态."""
        enabled = self.nvram_auth_enabled.get()

        if enabled:
            self.nvram_username_entry.configure(state='normal')
            self.nvram_secret_type_option.configure(state='normal')
            self.nvram_secret_usage_entry.configure(state='normal')
        else:
            self.nvram_username_entry.configure(state='disabled')
            self.nvram_secret_type_option.configure(state='disabled')
            self.nvram_secret_usage_entry.configure(state='disabled')

    def _create_varstore_row(self, parent: ctk.CTkFrame, row: int) -> None:
        """创建 Varstore 配置行: varstore 和 varstore_template."""
        frame = ctk.CTkFrame(parent, fg_color='transparent')
        frame.grid(row=row, column=0, columnspan=2, padx=10, pady=3, sticky='w')

        # varstore
        ctk.CTkLabel(frame, text='varstore:', font=('', 11), width=80, anchor='w').pack(
            side='left', padx=(0, 5)
        )
        self.varstore_entry = ctk.CTkEntry(
            frame, placeholder_text='/var/lib/libvirt/nvram/guest_VARS.fd', width=120, font=('', 11)
        )
        self.varstore_entry.pack(side='left', padx=5)
        self.varstore_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        # varstore_template
        ctk.CTkLabel(frame, text='template:', font=('', 11), width=60, anchor='w').pack(
            side='left', padx=(15, 5)
        )
        self.varstore_template_entry = ctk.CTkEntry(
            frame, placeholder_text='/usr/share/OVMF/OVMF_VARS.fd', width=120, font=('', 11)
        )
        self.varstore_template_entry.pack(side='left', padx=5)
        self.varstore_template_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

    def _create_container_basic_row(self, parent: ctk.CTkFrame, row: int) -> None:
        """创建容器基本信息行: init、initdir、inituser、initgroup 全部放一行."""
        frame = ctk.CTkFrame(parent, fg_color='transparent')
        frame.grid(row=row, column=0, columnspan=2, padx=10, pady=3, sticky='w')

        # init
        ctk.CTkLabel(frame, text='init:', font=('', 11), width=30, anchor='w').pack(
            side='left', padx=(0, 3)
        )
        self.init_entry = ctk.CTkEntry(
            frame, placeholder_text='/bin/systemd', width=80, font=('', 11)
        )
        self.init_entry.pack(side='left', padx=3)
        self.init_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        # initdir
        ctk.CTkLabel(frame, text='initdir:', font=('', 11), width=45, anchor='w').pack(
            side='left', padx=(10, 3)
        )
        self.initdir_entry = ctk.CTkEntry(
            frame, placeholder_text='/my/cwd', width=60, font=('', 11)
        )
        self.initdir_entry.pack(side='left', padx=3)
        self.initdir_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        # inituser
        ctk.CTkLabel(frame, text='inituser:', font=('', 11), width=50, anchor='w').pack(
            side='left', padx=(10, 3)
        )
        self.inituser_entry = ctk.CTkEntry(
            frame, placeholder_text='tester', width=60, font=('', 11)
        )
        self.inituser_entry.pack(side='left', padx=3)
        self.inituser_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        # initgroup
        ctk.CTkLabel(frame, text='initgroup:', font=('', 11), width=55, anchor='w').pack(
            side='left', padx=(10, 3)
        )
        self.initgroup_entry = ctk.CTkEntry(frame, placeholder_text='1000', width=50, font=('', 11))
        self.initgroup_entry.pack(side='left', padx=3)
        self.initgroup_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

    def _on_idmap_toggle(self) -> None:
        """处理 ID 映射开关切换事件."""
        self._update_idmap_ui_state()
        self._trigger_change()

    def _update_idmap_ui_state(self) -> None:
        """根据开关状态更新 ID 映射 UI 的启用/禁用状态."""
        enabled = self.idmap_enabled.get()

        for entry in self.idmap_entries.values():
            if enabled:
                entry.configure(state='normal')
            else:
                entry.configure(state='disabled')

    def _validate_number(self, value: str) -> bool:
        """验证输入值是否为数字（允许空值）.

        Args:
            value: 输入框的当前值

        Returns:
            True 如果值为空或纯数字，False 否则
        """
        if value == '':
            return True
        try:
            int(value)
            return True
        except ValueError:
            return False

    def _add_boot_device(self) -> None:
        """添加引导设备，紧跟在加减号后面横向排列."""
        index = len(self.boot_devices) if hasattr(self, 'boot_devices') else 0
        if not hasattr(self, 'boot_devices'):
            self.boot_devices = []

        # 使用 pack 横向排列
        device = ctk.CTkOptionMenu(
            self.boot_devices_frame,
            values=['hd', 'cdrom', 'network', 'floppy'],
            font=('', 10),
            width=50,
        )
        device.set('hd')
        device.pack(side='left', padx=2, pady=1)
        device.configure(command=self._trigger_change)

        self.boot_devices.append(device)
        self._trigger_change()

    def _remove_boot_device(self) -> None:
        """删除最后一个引导设备."""
        if self.boot_devices:
            device = self.boot_devices.pop()
            device.destroy()
            self._trigger_change()

    def _add_initarg(self) -> None:
        """添加 initarg."""
        index = len(self.initargs)
        row = len(self.initargs)
        arg = ctk.CTkEntry(
            self.initargs_frame, placeholder_text=f'arg {index + 1}', font=('', 10), width=50
        )
        arg.grid(row=row, column=0, padx=2, pady=1, sticky='ew')
        arg.bind('<KeyRelease>', lambda e: self._trigger_change())
        self.initargs.append(arg)
        self._trigger_change()

    def _remove_initarg(self) -> None:
        """删除最后一个 initarg."""
        if self.initargs:
            arg = self.initargs.pop()
            arg.destroy()
            self._trigger_change()

    def _add_initenv(self) -> None:
        """添加 initenv."""
        index = len(self.initenvs)
        row = len(self.initenvs)
        name = ctk.CTkEntry(self.initenvs_frame, placeholder_text='name', font=('', 10), width=20)
        name.grid(row=row, column=0, padx=2, pady=1, sticky='ew')
        name.bind('<KeyRelease>', lambda e: self._trigger_change())
        value = ctk.CTkEntry(self.initenvs_frame, placeholder_text='value', font=('', 10), width=20)
        value.grid(row=row, column=1, padx=2, pady=1, sticky='ew')
        value.bind('<KeyRelease>', lambda e: self._trigger_change())
        self.initenvs.append((name, value))
        self._trigger_change()

    def _remove_initenv(self) -> None:
        """删除最后一个 initenv."""
        if self.initenvs:
            name, value = self.initenvs.pop()
            name.destroy()
            value.destroy()
            self._trigger_change()

    def _add_acpi_table(self) -> None:
        """添加 ACPI 表配置."""
        index = len(self.acpi_tables) if hasattr(self, 'acpi_tables') else 0
        if not hasattr(self, 'acpi_tables'):
            self.acpi_tables = []

        frame = ctk.CTkFrame(self.acpi_tables_frame, fg_color='transparent')
        frame.pack(side='left', padx=2, pady=1)

        type_label = ctk.CTkLabel(frame, text='type:', font=('', 10), width=30, anchor='w')
        type_label.pack(side='left', padx=(0, 2))
        acpi_type = ctk.CTkOptionMenu(
            frame, values=['raw', 'rawset', 'slic', 'msdm'], width=80, font=('', 10)
        )
        acpi_type.set('slic')
        acpi_type.pack(side='left', padx=2)
        acpi_type.configure(command=self._trigger_change)

        path_label = ctk.CTkLabel(frame, text='path:', font=('', 10), width=35, anchor='w')
        path_label.pack(side='left', padx=(5, 2))
        acpi_path = ctk.CTkEntry(
            frame, placeholder_text='/path/to/table.dat', width=150, font=('', 10)
        )
        acpi_path.pack(side='left', padx=2)
        acpi_path.bind('<KeyRelease>', lambda e: self._trigger_change())

        self.acpi_tables.append(
            {
                'frame': frame,
                'type_label': type_label,
                'type': acpi_type,
                'path_label': path_label,
                'path': acpi_path,
            }
        )
        self._trigger_change()

    def _remove_acpi_table(self) -> None:
        """删除最后一个 ACPI 表配置."""
        if self.acpi_tables:
            table = self.acpi_tables.pop()
            table['type'].destroy()
            table['path'].destroy()
            table['type_label'].destroy()
            table['path_label'].destroy()
            table['frame'].destroy()
            self._trigger_change()

    def get_config(self) -> dict:
        """获取 OS 配置."""
        # 获取固件配置
        firmware = self.firmware_option.get()
        if firmware == '无':
            firmware = None

        # 获取引导设备
        boot_devices = []
        if hasattr(self, 'boot_devices'):
            for device in self.boot_devices:
                dev = device.get()
                if dev:
                    boot_devices.append(dev)

        # 获取 initarg/initenv (过滤空值)
        initargs = [arg.get().strip() for arg in self.initargs if arg.get().strip()]
        initenvs = [
            {'name': env[0].get().strip(), 'value': env[1].get().strip()}
            for env in self.initenvs
            if env[0].get().strip() or env[1].get().strip()
        ]

        return {
            'firmware': firmware,
            'type': self.type_option.get(),
            'arch': self.arch_option.get() if self.arch_option.get() != 'None' else None,
            'machine': self.machine_option.get() if self.machine_option.get() != 'None' else None,
            'loader': self.loader_entry.get(),
            'loader_readonly': self.loader_readonly_checkbox.get(),
            'loader_secure': self.loader_secure_checkbox.get(),
            'loader_stateless': self.loader_stateless_checkbox.get(),
            'loader_format': self.loader_format_option.get(),
            'nvram_type': self.nvram_type_option.get(),
            'nvram_format': self.nvram_format_option.get(),
            'nvram_template': self.nvram_template_entry.get(),
            # file/block 类型
            'nvram_file': self.nvram_file_entry.get(),
            # network 类型
            'nvram_protocol': self.nvram_protocol_option.get(),
            'nvram_name': self.nvram_name_entry.get(),
            'nvram_host': self.nvram_host_entry.get(),
            'nvram_port': self.nvram_port_entry.get(),
            # network auth
            'nvram_auth_enabled': bool(self.nvram_auth_enabled.get()),
            'nvram_username': self.nvram_username_entry.get(),
            'nvram_secret_type': self.nvram_secret_type_option.get(),
            'nvram_secret_usage': self.nvram_secret_usage_entry.get(),
            'varstore': self.varstore_entry.get(),
            'varstore_template': self.varstore_template_entry.get(),
            'boot_devices': boot_devices,
            'bootmenu': bool(self.bootmenu_checkbox.get()),
            'bootmenu_timeout': self.bootmenu_timeout_entry.get(),
            'smbios': self.smbios_option.get(),
            'bios_useserial': bool(self.bios_useserial_checkbox.get()),
            'bios_reboot': self.bios_reboot_entry.get(),
            'bootloader': self.bootloader_entry.get(),
            'bootloader_args': self.bootloader_args_entry.get(),
            'kernel': self.kernel_entry.get(),
            'initrd': self.initrd_entry.get(),
            'cmdline': self.cmdline_entry.get(),
            'shim': self.shim_entry.get(),
            'dtb': self.dtb_entry.get(),
            'acpi_tables': [
                {'type': table['type'].get(), 'path': table['path'].get()}
                for table in self.acpi_tables
            ]
            if hasattr(self, 'acpi_tables')
            else [],
            'init': self.init_entry.get(),
            'initargs': initargs,
            'initenvs': initenvs,
            'initdir': self.initdir_entry.get(),
            'inituser': self.inituser_entry.get(),
            'initgroup': self.initgroup_entry.get(),
            'idmap_enabled': bool(self.idmap_enabled.get()),
            'uid_start': self.idmap_entries['uid_start'].get(),
            'uid_target': self.idmap_entries['uid_target'].get(),
            'uid_count': self.idmap_entries['uid_count'].get(),
            'gid_start': self.idmap_entries['gid_start'].get(),
            'gid_target': self.idmap_entries['gid_target'].get(),
            'gid_count': self.idmap_entries['gid_count'].get(),
        }

    def to_xml(self) -> dict:
        """生成 XML 配置字典."""
        config = self.get_config()

        os_booting_config = {
            'type': config.get('type', 'hvm'),
            'arch': config.get('arch', 'x86_64'),
            'machine': config.get('machine', 'q35'),
            'boot_devices': config['boot_devices'],
        }

        if config['firmware']:
            os_booting_config['firmware'] = config['firmware']

        # loader
        loader_config = {
            'path': config.get('loader', ''),
            'readonly': config.get('loader_readonly', False),
            'secure': config.get('loader_secure', False),
            'stateless': config.get('loader_stateless', False),
            'format': config.get('loader_format', 'raw'),
        }
        if any(loader_config.values()):
            os_booting_config['loader'] = loader_config

        # nvram
        nvram_type = config.get('nvram_type', 'file')
        nvram_config = {
            'type': nvram_type,
            'format': config.get('nvram_format', 'raw'),
            'template': config.get('nvram_template', ''),
        }

        if nvram_type in ('file', 'block'):
            # file/block 类型: 使用 source file 属性
            nvram_file = config.get('nvram_file', '')
            if nvram_file:
                nvram_config['source'] = {'file': nvram_file}
        elif nvram_type == 'network':
            # network 类型: 使用 source 子元素
            source_config = {}
            protocol = config.get('nvram_protocol', 'iscsi')
            name = config.get('nvram_name', '')
            host = config.get('nvram_host', '')
            port = config.get('nvram_port', '')

            if protocol:
                source_config['protocol'] = protocol
            if name:
                source_config['name'] = name
            if host:
                source_config['host'] = {'name': host}
                if port:
                    source_config['host']['port'] = port

            # auth 认证配置
            if config.get('nvram_auth_enabled'):
                username = config.get('nvram_username', '')
                secret_type = config.get('nvram_secret_type', 'iscsi')
                secret_usage = config.get('nvram_secret_usage', '')
                if username:
                    auth_config = {'username': username}
                    if secret_usage:
                        auth_config['secret'] = {'type': secret_type, 'usage': secret_usage}
                    source_config['auth'] = auth_config

            if source_config:
                nvram_config['source'] = source_config

        if nvram_config.get('template') or nvram_config.get('source'):
            os_booting_config['nvram'] = nvram_config

        # varstore
        varstore_config = {
            'path': config.get('varstore', ''),
            'template': config.get('varstore_template', ''),
        }
        if varstore_config.get('path') or varstore_config.get('template'):
            os_booting_config['varstore'] = varstore_config

        # bootmenu
        if config.get('bootmenu'):
            timeout_raw = config.get('bootmenu_timeout', '')
            # 处理空字符串或无效值
            try:
                timeout = int(timeout_raw) if timeout_raw else 3000
            except (ValueError, TypeError):
                timeout = 3000
            os_booting_config['bootmenu'] = {
                'enable': True,
                'timeout': timeout,
            }

        # smbios
        smbios_value = config.get('smbios')
        if smbios_value and smbios_value != 'None':
            os_booting_config['smbios'] = {'mode': smbios_value}

        # bios
        bios_attrs = {}
        if config.get('bios_useserial'):
            bios_attrs['useserial'] = 'yes'
        reboot = config.get('bios_reboot', '-1')
        if reboot and reboot != '-1':
            try:
                if int(reboot) >= 0:
                    bios_attrs['rebootTimeout'] = reboot
            except (ValueError, TypeError):
                pass
        if bios_attrs:
            os_booting_config['bios'] = bios_attrs

        # bootloader
        if config.get('bootloader'):
            os_booting_config['host_bootloader'] = {
                'path': config['bootloader'],
                'args': config.get('bootloader_args', ''),
            }

        # direct kernel
        if config.get('kernel'):
            os_booting_config['direct_kernel'] = {
                'kernel': config['kernel'],
                'initrd': config.get('initrd', ''),
                'cmdline': config.get('cmdline', ''),
                'shim': config.get('shim', ''),
                'dtb': config.get('dtb', ''),
            }

        # container
        if config.get('init'):
            os_booting_config['container'] = {
                'init': config['init'],
                'initargs': config.get('initargs', []),
                'initenvs': config.get('initenvs', []),
                'initdir': config.get('initdir', ''),
                'inituser': config.get('inituser', ''),
                'initgroup': config.get('initgroup', ''),
            }

        # idmap (仅在启用时生成)
        if config.get('idmap_enabled'):
            idmap_config = {}
            uid_target = config.get('uid_target', '0')
            if uid_target and uid_target != '0':
                idmap_config['uid'] = {
                    'start': int(config.get('uid_start', 0) or 0),
                    'target': int(uid_target or 0),
                    'count': int(config.get('uid_count', 0) or 0),
                }
            gid_target = config.get('gid_target', '0')
            if gid_target and gid_target != '0':
                idmap_config['gid'] = {
                    'start': int(config.get('gid_start', 0) or 0),
                    'target': int(gid_target or 0),
                    'count': int(config.get('gid_count', 0) or 0),
                }
            if idmap_config:
                os_booting_config['idmap'] = idmap_config

        # acpi
        acpi_tables = config.get('acpi_tables', [])
        if acpi_tables:
            os_booting_config['acpi'] = {'tables': acpi_tables}

        return {'os_booting': os_booting_config}

    def load_config(self, config: dict) -> None:
        """加载配置数据到 UI."""
        # 加载固件配置
        if 'firmware' in config:
            self.firmware_option.set(config.get('firmware') or '无')
        if 'type' in config:
            self.type_option.set(config['type'])
        if 'arch' in config:
            self.arch_option.set(config['arch'])
        if 'machine' in config:
            self.machine_option.set(config['machine'])
        if 'loader' in config:
            self.loader_entry.delete(0, ctk.END)
            self.loader_entry.insert(0, config['loader'])
        if 'loader_readonly' in config:
            if config['loader_readonly']:
                self.loader_readonly_checkbox.select()
            else:
                self.loader_readonly_checkbox.deselect()
        if 'loader_secure' in config:
            if config['loader_secure']:
                self.loader_secure_checkbox.select()
            else:
                self.loader_secure_checkbox.deselect()
        if 'loader_stateless' in config:
            if config['loader_stateless']:
                self.loader_stateless_checkbox.select()
            else:
                self.loader_stateless_checkbox.deselect()
        if 'loader_format' in config:
            self.loader_format_option.set(config['loader_format'])
        if 'nvram_type' in config:
            self.nvram_type_option.set(config['nvram_type'])
        if 'nvram_format' in config:
            self.nvram_format_option.set(config['nvram_format'])
        if 'nvram_template' in config:
            self.nvram_template_entry.delete(0, ctk.END)
            self.nvram_template_entry.insert(0, config['nvram_template'])

        # 加载 file/block 类型的 source file
        if 'nvram_file' in config:
            self.nvram_file_entry.delete(0, ctk.END)
            self.nvram_file_entry.insert(0, config['nvram_file'])

        # 加载 network 类型的配置
        if 'nvram_protocol' in config:
            self.nvram_protocol_option.set(config['nvram_protocol'])
        if 'nvram_name' in config:
            self.nvram_name_entry.delete(0, ctk.END)
            self.nvram_name_entry.insert(0, config['nvram_name'])
        if 'nvram_host' in config:
            self.nvram_host_entry.delete(0, ctk.END)
            self.nvram_host_entry.insert(0, config['nvram_host'])
        if 'nvram_port' in config:
            self.nvram_port_entry.delete(0, ctk.END)
            self.nvram_port_entry.insert(0, config['nvram_port'])

        # 加载 network auth 配置
        if 'nvram_auth_enabled' in config:
            if config['nvram_auth_enabled']:
                self.nvram_auth_enabled.select()
            else:
                self.nvram_auth_enabled.deselect()
        if 'nvram_username' in config:
            self.nvram_username_entry.delete(0, ctk.END)
            self.nvram_username_entry.insert(0, config['nvram_username'])
        if 'nvram_secret_type' in config:
            self.nvram_secret_type_option.set(config['nvram_secret_type'])
        if 'nvram_secret_usage' in config:
            self.nvram_secret_usage_entry.delete(0, ctk.END)
            self.nvram_secret_usage_entry.insert(0, config['nvram_secret_usage'])

        # 更新 UI 状态
        self._update_nvram_ui_state()
        if 'varstore' in config:
            self.varstore_entry.delete(0, ctk.END)
            self.varstore_entry.insert(0, config['varstore'])
        if 'varstore_template' in config:
            self.varstore_template_entry.delete(0, ctk.END)
            self.varstore_template_entry.insert(0, config['varstore_template'])

        # 加载 boot 配置
        if 'bootmenu' in config and isinstance(config['bootmenu'], dict):
            if config['bootmenu'].get('enable'):
                self.bootmenu_checkbox.select()
            else:
                self.bootmenu_checkbox.deselect()
            self.bootmenu_timeout_entry.delete(0, ctk.END)
            self.bootmenu_timeout_entry.insert(0, str(config['bootmenu'].get('timeout', 3000)))
        if 'smbios' in config and isinstance(config['smbios'], dict):
            self.smbios_option.set(config['smbios'].get('mode', 'emulate'))
        if 'bios' in config and isinstance(config['bios'], dict):
            if config['bios'].get('useserial'):
                self.bios_useserial_checkbox.select()
            else:
                self.bios_useserial_checkbox.deselect()
            self.bios_reboot_entry.delete(0, ctk.END)
            self.bios_reboot_entry.insert(0, str(config['bios'].get('rebootTimeout', -1)))

        # 加载引导设备
        if 'boot_devices' in config and isinstance(config['boot_devices'], list):
            if hasattr(self, 'boot_devices'):
                for device in self.boot_devices:
                    device.destroy()
                self.boot_devices = []
            for device in config['boot_devices']:
                if not hasattr(self, 'boot_devices'):
                    self.boot_devices = []
                device_menu = ctk.CTkOptionMenu(
                    self.boot_devices_frame,
                    values=['hd', 'cdrom', 'network', 'floppy'],
                    font=('', 10),
                    width=50,
                )
                device_menu.set(device)
                device_menu.pack(side='left', padx=2, pady=1)
                device_menu.configure(command=self._trigger_change)
                self.boot_devices.append(device_menu)

        # 加载 bootloader 配置
        if 'host_bootloader' in config and isinstance(config['host_bootloader'], dict):
            self.bootloader_entry.delete(0, ctk.END)
            self.bootloader_entry.insert(0, config['host_bootloader'].get('path', ''))
            self.bootloader_args_entry.delete(0, ctk.END)
            self.bootloader_args_entry.insert(0, config['host_bootloader'].get('args', ''))

        # 加载内核启动配置
        if 'direct_kernel' in config and isinstance(config['direct_kernel'], dict):
            dk = config['direct_kernel']
            self.kernel_entry.delete(0, ctk.END)
            self.kernel_entry.insert(0, dk.get('kernel', ''))
            self.initrd_entry.delete(0, ctk.END)
            self.initrd_entry.insert(0, dk.get('initrd', ''))
            self.cmdline_entry.delete(0, ctk.END)
            self.cmdline_entry.insert(0, dk.get('cmdline', ''))
            self.shim_entry.delete(0, ctk.END)
            self.shim_entry.insert(0, dk.get('shim', ''))
            self.dtb_entry.delete(0, ctk.END)
            self.dtb_entry.insert(0, dk.get('dtb', ''))

        # 加载容器启动配置
        if 'container' in config and isinstance(config['container'], dict):
            c = config['container']
            self.init_entry.delete(0, ctk.END)
            self.init_entry.insert(0, c.get('init', ''))
            self.initdir_entry.delete(0, ctk.END)
            self.initdir_entry.insert(0, c.get('initdir', ''))
            self.inituser_entry.delete(0, ctk.END)
            self.inituser_entry.insert(0, c.get('inituser', ''))
            self.initgroup_entry.delete(0, ctk.END)
            self.initgroup_entry.insert(0, c.get('initgroup', ''))

            # 加载 initargs
            if hasattr(self, 'initargs'):
                for arg in self.initargs:
                    arg.destroy()
                self.initargs = []
            for arg_val in c.get('initargs', []):
                self._add_initarg()
                if self.initargs:
                    self.initargs[-1].delete(0, ctk.END)
                    self.initargs[-1].insert(0, arg_val)

            # 加载 initenvs
            if hasattr(self, 'initenvs'):
                for name, value in self.initenvs:
                    name.destroy()
                    value.destroy()
                self.initenvs = []
            for env in c.get('initenvs', []):
                self._add_initenv()
                if self.initenvs:
                    self.initenvs[-1][0].delete(0, ctk.END)
                    self.initenvs[-1][0].insert(0, env.get('name', ''))
                    self.initenvs[-1][1].delete(0, ctk.END)
                    self.initenvs[-1][1].insert(0, env.get('value', ''))

        # 加载 idmap 配置
        if 'idmap_enabled' in config:
            if config['idmap_enabled']:
                self.idmap_enabled.select()
            else:
                self.idmap_enabled.deselect()
            self._update_idmap_ui_state()

        if 'idmap' in config and isinstance(config['idmap'], dict):
            idmap = config['idmap']
            if 'uid' in idmap:
                self.idmap_entries['uid_start'].delete(0, ctk.END)
                self.idmap_entries['uid_start'].insert(0, str(idmap['uid'].get('start', 0)))
                self.idmap_entries['uid_target'].delete(0, ctk.END)
                self.idmap_entries['uid_target'].insert(0, str(idmap['uid'].get('target', 0)))
                self.idmap_entries['uid_count'].delete(0, ctk.END)
                self.idmap_entries['uid_count'].insert(0, str(idmap['uid'].get('count', 0)))
            if 'gid' in idmap:
                self.idmap_entries['gid_start'].delete(0, ctk.END)
                self.idmap_entries['gid_start'].insert(0, str(idmap['gid'].get('start', 0)))
                self.idmap_entries['gid_target'].delete(0, ctk.END)
                self.idmap_entries['gid_target'].insert(0, str(idmap['gid'].get('target', 0)))
                self.idmap_entries['gid_count'].delete(0, ctk.END)
                self.idmap_entries['gid_count'].insert(0, str(idmap['gid'].get('count', 0)))

        # 加载 ACPI 配置
        if 'acpi' in config and isinstance(config['acpi'], dict):
            acpi = config['acpi']
            if 'tables' in acpi and isinstance(acpi['tables'], list):
                # 清空现有表
                if hasattr(self, 'acpi_tables'):
                    for table in self.acpi_tables:
                        table['type'].destroy()
                        table['path'].destroy()
                        table['type_label'].destroy()
                        table['path_label'].destroy()
                        table['frame'].destroy()
                    self.acpi_tables = []

                # 加载表
                for table_data in acpi['tables']:
                    self._add_acpi_table()
                    if self.acpi_tables:
                        last_table = self.acpi_tables[-1]
                        last_table['type'].set(table_data.get('type', 'slic'))
                        last_table['path'].delete(0, ctk.END)
                        last_table['path'].insert(0, table_data.get('path', ''))
