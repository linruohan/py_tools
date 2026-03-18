"""引导/OS 配置 Tab - 按 libvirt Domain XML format 第 3 章重构."""

from typing import ClassVar

import customtkinter as ctk

from components.base_tab import FieldConfig, SectionConfig, StandardConfigTab


class OSTab(StandardConfigTab):
    """引导/OS 配置 Tab."""

    SECTIONS: ClassVar[dict] = {
        'firmware': SectionConfig(
            title='固件',
            fields=[
                FieldConfig('firmware', 'option', '无', ['无', 'bios', 'efi'], label_width=80),
                FieldConfig('type', 'option', 'hvm', ['hvm', 'linux', 'exe'], label_width=80),
                FieldConfig('arch', 'entry', 'x86_64', placeholder='x86_64', label_width=80),
                FieldConfig('machine', 'entry', 'q35', placeholder='q35', label_width=80),
                FieldConfig(
                    'loader',
                    'entry',
                    '',
                    placeholder='/usr/share/OVMF/OVMF_CODE.fd',
                    label_width=80,
                ),
                FieldConfig('loader_readonly', 'checkbox', False, label_width=80),
                FieldConfig('loader_secure', 'checkbox', False, label_width=80),
                FieldConfig('loader_stateless', 'checkbox', False, label_width=80),
                FieldConfig('loader_format', 'option', 'raw', ['raw', 'qcow2'], label_width=80),
                FieldConfig(
                    'nvram',
                    'entry',
                    '',
                    placeholder='/var/lib/libvirt/nvram/guest_VARS.fd',
                    label_width=80,
                ),
                FieldConfig(
                    'nvram_template',
                    'entry',
                    '',
                    placeholder='/usr/share/OVMF/OVMF_VARS.fd',
                    label_width=80,
                ),
                FieldConfig(
                    'nvram_type', 'option', 'file', ['file', 'block', 'network'], label_width=80
                ),
                FieldConfig('nvram_format', 'option', 'raw', ['raw', 'qcow2'], label_width=80),
                FieldConfig(
                    'varstore',
                    'entry',
                    '',
                    placeholder='/var/lib/libvirt/nvram/guest_VARS.fd',
                    label_width=80,
                ),
                FieldConfig(
                    'varstore_template',
                    'entry',
                    '',
                    placeholder='/usr/share/OVMF/OVMF_VARS.fd',
                    label_width=80,
                ),
            ],
            color='#FF6B6B',
        ),
        'boot': SectionConfig(
            title='引导',
            fields=[
                FieldConfig('boot_devices', 'info', 'hd', label_width=80),
                FieldConfig('bootmenu', 'checkbox', False, label_width=80),
                FieldConfig(
                    'bootmenu_timeout', 'entry', '3000', placeholder='3000', label_width=80
                ),
                FieldConfig(
                    'smbios',
                    'option',
                    'emulate',
                    ['None', 'emulate', 'host', 'sysinfo'],
                    label_width=80,
                ),
                FieldConfig('bios_useserial', 'checkbox', False, label_width=80),
                FieldConfig('bios_reboot', 'entry', '-1', placeholder='-1', label_width=80),
                FieldConfig('', 'info', '引导程序', text_color='#FFD93D'),
                FieldConfig(
                    'bootloader', 'entry', '', placeholder='/usr/bin/pygrub', label_width=80
                ),
                FieldConfig(
                    'bootloader_args', 'entry', '', placeholder='--append single', label_width=80
                ),
                FieldConfig('', 'info', '内核启动 (直接指定内核镜像)', text_color='#FFD93D'),
                FieldConfig('kernel', 'entry', '', placeholder='/root/vmlinuz', label_width=80),
                FieldConfig('initrd', 'entry', '', placeholder='/root/initrd', label_width=80),
                FieldConfig('cmdline', 'entry', '', placeholder='console=ttyS0', label_width=80),
                FieldConfig('shim', 'entry', '', placeholder='/path/to/shim.efi', label_width=80),
                FieldConfig('dtb', 'entry', '', placeholder='/root/ppc.dtb', label_width=80),
                FieldConfig('', 'info', 'ACPI 表配置', text_color='#FFD93D'),
                FieldConfig(
                    'acpi_type', 'option', 'slic', ['raw', 'rawset', 'slic', 'msdm'], label_width=80
                ),
                FieldConfig(
                    'acpi_path', 'entry', '', placeholder='/path/to/slic.dat', label_width=80
                ),
            ],
            color='#4ECDC4',
        ),
        'container': SectionConfig(
            title='容器启动',
            fields=[
                FieldConfig('init', 'entry', '', placeholder='/bin/systemd', label_width=80),
                FieldConfig('initdir', 'entry', '', placeholder='/my/cwd', label_width=80),
                FieldConfig('inituser', 'entry', '', placeholder='tester', label_width=80),
                FieldConfig('initgroup', 'entry', '', placeholder='1000', label_width=80),
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

        # 在 boot section 添加 boot devices
        boot_frame = self.section_frames['boot']
        boot_row = self.section_rows['boot']

        # boot: 标签和按钮放在同一行
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

        # boot 设备列表横向排列在一行
        self.boot_devices_frame = ctk.CTkFrame(boot_frame, fg_color='transparent')
        self.boot_devices_frame.grid(
            row=boot_row + 1, column=0, columnspan=2, padx=1, pady=3, sticky='w'
        )
        self._add_boot_device()

        self.section_rows['boot'] = boot_row + 2

        # 在 container section 添加 initarg/initenv/idmap
        container_frame = self.section_frames['container']
        # container section 有 4 个标准字段 (init, initdir, inituser, initgroup)，从第 5 行开始添加自定义 UI
        container_row = self.section_rows['container'] + 4

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
        """添加引导设备."""
        index = len(self.boot_devices) if hasattr(self, 'boot_devices') else 0
        if not hasattr(self, 'boot_devices'):
            self.boot_devices = []

        # 横向排列，使用 pack 而不是 grid
        device = ctk.CTkOptionMenu(
            self.boot_devices_frame,
            values=['hd', 'cdrom', 'network', 'floppy'],
            font=('', 10),
            width=80,
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
            self.initargs_frame, placeholder_text=f'arg {index + 1}', font=('', 10), width=120
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
        name = ctk.CTkEntry(self.initenvs_frame, placeholder_text='name', font=('', 10), width=60)
        name.grid(row=row, column=0, padx=2, pady=1, sticky='ew')
        name.bind('<KeyRelease>', lambda e: self._trigger_change())
        value = ctk.CTkEntry(self.initenvs_frame, placeholder_text='value', font=('', 10), width=60)
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

    def get_config(self) -> dict:
        """获取 OS 配置."""
        children = {key: frame.winfo_children() for key, frame in self.section_frames.items()}

        # 获取固件配置
        firmware = children['firmware'][1].get()
        if firmware == '无':
            firmware = None

        # 获取引导设备
        boot_devices = []
        if hasattr(self, 'boot_devices'):
            for device in self.boot_devices:
                dev = device.get()
                if dev:
                    boot_devices.append(dev)

        # 获取 initarg/initenv
        initargs = [arg.get().strip() for arg in self.initargs]
        initenvs = [
            {'name': env[0].get().strip(), 'value': env[1].get().strip()} for env in self.initenvs
        ]

        return {
            'firmware': firmware,
            'type': children['firmware'][2].get(),
            'arch': children['firmware'][3].get(),
            'machine': children['firmware'][4].get(),
            'loader': children['firmware'][5].get(),
            'loader_readonly': children['firmware'][6].get(),
            'loader_secure': children['firmware'][7].get(),
            'loader_stateless': children['firmware'][8].get(),
            'loader_format': children['firmware'][9].get(),
            'nvram': children['firmware'][10].get(),
            'nvram_template': children['firmware'][11].get(),
            'nvram_type': children['firmware'][12].get(),
            'nvram_format': children['firmware'][13].get(),
            'varstore': children['firmware'][14].get(),
            'varstore_template': children['firmware'][15].get(),
            'boot_devices': boot_devices,
            'bootmenu': children['boot'][2].get(),
            'bootmenu_timeout': children['boot'][3].get(),
            'smbios': children['boot'][4].get(),
            'bios_useserial': children['boot'][5].get(),
            'bios_reboot': children['boot'][6].get(),
            'bootloader': children['boot'][8].get(),
            'bootloader_args': children['boot'][9].get(),
            'kernel': children['boot'][11].get(),
            'initrd': children['boot'][12].get(),
            'cmdline': children['boot'][13].get(),
            'shim': children['boot'][14].get(),
            'dtb': children['boot'][15].get(),
            'acpi_type': children['boot'][17].get(),
            'acpi_path': children['boot'][18].get(),
            'init': children['container'][1].get(),
            'initargs': initargs,
            'initenvs': initenvs,
            'initdir': children['container'][2].get(),
            'inituser': children['container'][3].get(),
            'initgroup': children['container'][4].get(),
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
        nvram_config = {
            'path': config.get('nvram', ''),
            'template': config.get('nvram_template', ''),
            'type': config.get('nvram_type', 'file'),
            'format': config.get('nvram_format', 'raw'),
        }
        if nvram_config.get('path') or nvram_config.get('template'):
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
            os_booting_config['bootmenu'] = {
                'enable': True,
                'timeout': int(config.get('bootmenu_timeout', 3000)),
            }

        # smbios
        if config.get('smbios'):
            os_booting_config['smbios'] = {'mode': config['smbios']}

        # bios
        bios_attrs = {}
        if config.get('bios_useserial'):
            bios_attrs['useserial'] = 'yes'
        reboot = config.get('bios_reboot', '-1')
        if reboot and reboot != '-1' and int(reboot) >= 0:
            bios_attrs['rebootTimeout'] = reboot
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
        if config.get('acpi_path'):
            os_booting_config['acpi'] = {
                'table': {
                    'type': config.get('acpi_type', 'slic'),
                    'path': config['acpi_path'],
                }
            }

        return {'os_booting': os_booting_config}

    def load_config(self, config: dict) -> None:
        """加载配置数据到 UI."""
        children = {key: frame.winfo_children() for key, frame in self.section_frames.items()}

        # 加载固件配置
        if 'firmware' in config:
            children['firmware'][1].set(config.get('firmware') or '无')
        if 'type' in config:
            children['firmware'][2].set(config['type'])
        if 'arch' in config:
            children['firmware'][3].delete(0, ctk.END)
            children['firmware'][3].insert(0, config['arch'])
        if 'machine' in config:
            children['firmware'][4].delete(0, ctk.END)
            children['firmware'][4].insert(0, config['machine'])
        if 'loader' in config:
            children['firmware'][5].delete(0, ctk.END)
            children['firmware'][5].insert(0, config['loader'])
        if 'loader_readonly' in config:
            children['firmware'][6].select() if config['loader_readonly'] else children['firmware'][
                6
            ].deselect()
        if 'loader_secure' in config:
            children['firmware'][7].select() if config['loader_secure'] else children['firmware'][
                7
            ].deselect()
        if 'loader_stateless' in config:
            children['firmware'][8].select() if config['loader_stateless'] else children[
                'firmware'
            ][8].deselect()
        if 'loader_format' in config:
            children['firmware'][9].set(config['loader_format'])
        if 'nvram' in config:
            children['firmware'][10].delete(0, ctk.END)
            children['firmware'][10].insert(0, config['nvram'])
        if 'nvram_template' in config:
            children['firmware'][11].delete(0, ctk.END)
            children['firmware'][11].insert(0, config['nvram_template'])
        if 'nvram_type' in config:
            children['firmware'][12].set(config['nvram_type'])
        if 'nvram_format' in config:
            children['firmware'][13].set(config['nvram_format'])
        if 'varstore' in config:
            children['firmware'][14].delete(0, ctk.END)
            children['firmware'][14].insert(0, config['varstore'])
        if 'varstore_template' in config:
            children['firmware'][15].delete(0, ctk.END)
            children['firmware'][15].insert(0, config['varstore_template'])

        # 加载 boot 配置
        if 'bootmenu' in config and isinstance(config['bootmenu'], dict):
            children['boot'][2].select() if config['bootmenu'].get('enable') else children['boot'][
                2
            ].deselect()
            children['boot'][3].delete(0, ctk.END)
            children['boot'][3].insert(0, str(config['bootmenu'].get('timeout', 3000)))
        if 'smbios' in config and isinstance(config['smbios'], dict):
            children['boot'][4].set(config['smbios'].get('mode', 'emulate'))
        if 'bios' in config and isinstance(config['bios'], dict):
            children['boot'][5].select() if config['bios'].get('useserial') else children['boot'][
                5
            ].deselect()
            children['boot'][6].delete(0, ctk.END)
            children['boot'][6].insert(0, str(config['bios'].get('rebootTimeout', -1)))

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
                    width=80,
                )
                device_menu.set(device)
                device_menu.pack(side='left', padx=2, pady=1)
                device_menu.configure(command=self._trigger_change)
                self.boot_devices.append(device_menu)

        # 加载 bootloader 配置
        if 'host_bootloader' in config and isinstance(config['host_bootloader'], dict):
            children['boot'][8].delete(0, ctk.END)
            children['boot'][8].insert(0, config['host_bootloader'].get('path', ''))
            children['boot'][9].delete(0, ctk.END)
            children['boot'][9].insert(0, config['host_bootloader'].get('args', ''))

        # 加载内核启动配置
        if 'direct_kernel' in config and isinstance(config['direct_kernel'], dict):
            dk = config['direct_kernel']
            children['boot'][11].delete(0, ctk.END)
            children['boot'][11].insert(0, dk.get('kernel', ''))
            children['boot'][12].delete(0, ctk.END)
            children['boot'][12].insert(0, dk.get('initrd', ''))
            children['boot'][13].delete(0, ctk.END)
            children['boot'][13].insert(0, dk.get('cmdline', ''))
            children['boot'][14].delete(0, ctk.END)
            children['boot'][14].insert(0, dk.get('shim', ''))
            children['boot'][15].delete(0, ctk.END)
            children['boot'][15].insert(0, dk.get('dtb', ''))

        # 加载容器启动配置
        if 'container' in config and isinstance(config['container'], dict):
            c = config['container']
            children['container'][1].delete(0, ctk.END)
            children['container'][1].insert(0, c.get('init', ''))
            children['container'][2].delete(0, ctk.END)
            children['container'][2].insert(0, c.get('initdir', ''))
            children['container'][3].delete(0, ctk.END)
            children['container'][3].insert(0, c.get('inituser', ''))
            children['container'][4].delete(0, ctk.END)
            children['container'][4].insert(0, c.get('initgroup', ''))

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
            if 'table' in acpi and isinstance(acpi['table'], dict):
                children['boot'][17].set(acpi['table'].get('type', 'slic'))
                children['boot'][18].delete(0, ctk.END)
                children['boot'][18].insert(0, acpi['table'].get('path', ''))
