"""基础配置 Tab - 虚拟机名称、UUID、机型、CPU、内存等."""

import customtkinter as ctk

from utils.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class BasicTab(ctk.CTkFrame):
    """基础配置 Tab."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent')
        self.on_change_callback = on_change_callback

        # 架构类型变量
        self.arch_type = ctk.StringVar(value='x86')

        # 控件引用
        self.vm_name_entry = None
        self.vm_desc_entry = None
        self.uuid_entry = None
        self.machine_type = None
        self.virt_type = None
        self.chipset_type = None
        self.vcpu_entry = None
        self.cpu_mode = None
        self.memory_combo = None
        self.current_memory_combo = None
        self.max_memory_combo = None
        self.swap_entry = None
        # CPU Topology
        self.cpu_sockets_entry = None
        self.cpu_cores_entry = None
        self.cpu_threads_entry = None

        # 初始化 UI
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面."""
        # 配置 grid 权重 - 3 列布局
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 内存配置选项
        memory_options = ['1G', '2G', '4G', '8G', '16G', '32G', '64G', '128G']

        # ===== 第 1 列: 系统配置 =====
        sys_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=8)
        sys_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=10)
        sys_frame.grid_columnconfigure(1, weight=1)
        # 配置所有行的权重
        for i in range(8):
            sys_frame.grid_rowconfigure(i, weight=0)

        ctk.CTkLabel(sys_frame, text='系统配置', font=CTK_FONT_BOLD, text_color='#64b5f6').grid(
            row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
        )

        # 架构选择器
        ctk.CTkLabel(sys_frame, text='架构:', font=CTK_FONT_MAIN, width=90, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        arch_frame = ctk.CTkFrame(sys_frame, fg_color='transparent')
        arch_frame.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        arch_frame.grid_columnconfigure(0, weight=1)
        arch_frame.grid_columnconfigure(1, weight=1)

        self.arch_x86_radio = ctk.CTkRadioButton(
            arch_frame,
            text='x86',
            variable=self.arch_type,
            value='x86',
            command=self._on_arch_change,
            font=CTK_FONT_MAIN,
        )
        self.arch_x86_radio.grid(row=0, column=0, padx=5, sticky='w')

        self.arch_arm_radio = ctk.CTkRadioButton(
            arch_frame,
            text='ARM',
            variable=self.arch_type,
            value='arm',
            command=self._on_arch_change,
            font=CTK_FONT_MAIN,
        )
        self.arch_arm_radio.grid(row=0, column=1, padx=5, sticky='w')

        # 虚拟机名称
        ctk.CTkLabel(sys_frame, text='虚拟机名称:', font=CTK_FONT_MAIN, width=90, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.vm_name_entry = ctk.CTkEntry(sys_frame, placeholder_text='vm-name', width=180)
        self.vm_name_entry.grid(row=2, column=1, padx=5, pady=5, sticky='ew')
        self.vm_name_entry.insert(0, 'vm0')
        self.vm_name_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        # 描述
        ctk.CTkLabel(sys_frame, text='描述:', font=CTK_FONT_MAIN, width=90, anchor='w').grid(
            row=3, column=0, padx=10, pady=5, sticky='w'
        )
        self.vm_desc_entry = ctk.CTkEntry(sys_frame, placeholder_text='虚拟机描述', width=180)
        self.vm_desc_entry.grid(row=3, column=1, padx=5, pady=5, sticky='ew')
        self.vm_desc_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        # UUID
        ctk.CTkLabel(sys_frame, text='UUID:', font=CTK_FONT_MAIN, width=90, anchor='w').grid(
            row=4, column=0, padx=10, pady=5, sticky='w'
        )
        self.uuid_entry = ctk.CTkEntry(sys_frame, placeholder_text='自动生成', width=180)
        self.uuid_entry.grid(row=4, column=1, padx=5, pady=5, sticky='ew')
        self.uuid_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        # 机型
        ctk.CTkLabel(sys_frame, text='机型:', font=CTK_FONT_MAIN, width=90, anchor='w').grid(
            row=5, column=0, padx=10, pady=5, sticky='w'
        )
        self.machine_type = ctk.CTkOptionMenu(
            sys_frame,
            values=['q35', 'pc', 'pc-i440fx', 'virt', 'arm-virt'],
            width=180,
            font=CTK_FONT_SMALL,
        )
        self.machine_type.set('virt')
        self.machine_type.grid(row=5, column=1, padx=5, pady=5, sticky='ew')
        self.machine_type.configure(command=self._trigger_change)

        # 虚拟化类型
        ctk.CTkLabel(sys_frame, text='虚拟化:', font=CTK_FONT_MAIN, width=90, anchor='w').grid(
            row=6, column=0, padx=10, pady=5, sticky='w'
        )
        self.virt_type = ctk.CTkOptionMenu(
            sys_frame, values=['hvm', 'pv', 'exe'], width=180, font=CTK_FONT_SMALL
        )
        self.virt_type.set('hvm')
        self.virt_type.grid(row=6, column=1, padx=5, pady=5, sticky='ew')
        self.virt_type.configure(command=self._trigger_change)

        # 芯片组
        ctk.CTkLabel(sys_frame, text='芯片组:', font=CTK_FONT_MAIN, width=90, anchor='w').grid(
            row=7, column=0, padx=10, pady=5, sticky='w'
        )
        self.chipset_type = ctk.CTkOptionMenu(
            sys_frame, values=['PIIX3', 'PIIX4', 'Q35', 'virtio'], width=180, font=CTK_FONT_SMALL
        )
        self.chipset_type.set('virtio')
        self.chipset_type.grid(row=7, column=1, padx=5, pady=5, sticky='ew')
        self.chipset_type.configure(command=self._trigger_change)

        # ===== 第 2 列: CPU 配置 =====
        cpu_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=8)
        cpu_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=10)
        cpu_frame.grid_columnconfigure(1, weight=1)
        # 配置所有行的权重
        for i in range(6):
            cpu_frame.grid_rowconfigure(i, weight=0)

        ctk.CTkLabel(cpu_frame, text='CPU 配置', font=CTK_FONT_BOLD, text_color='#4caf50').grid(
            row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
        )

        # vCPU 数量
        ctk.CTkLabel(cpu_frame, text='vCPU:', font=CTK_FONT_MAIN, width=90, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.vcpu_entry = ctk.CTkEntry(cpu_frame, placeholder_text='2', width=180)
        self.vcpu_entry.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        self.vcpu_entry.insert(0, '2')
        self.vcpu_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        # CPU 模式
        ctk.CTkLabel(cpu_frame, text='CPU 模式:', font=CTK_FONT_MAIN, width=90, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.cpu_mode = ctk.CTkOptionMenu(
            cpu_frame,
            values=['host-passthrough', 'host-model', 'custom', 'host-model-required'],
            width=180,
            font=CTK_FONT_SMALL,
        )
        self.cpu_mode.set('host-model')
        self.cpu_mode.grid(row=2, column=1, padx=5, pady=5, sticky='ew')
        self.cpu_mode.configure(command=self._trigger_change)

        # CPU Topology - Sockets
        ctk.CTkLabel(cpu_frame, text='Sockets:', font=CTK_FONT_MAIN, width=90, anchor='w').grid(
            row=3, column=0, padx=10, pady=5, sticky='w'
        )
        self.cpu_sockets_entry = ctk.CTkEntry(cpu_frame, width=180, font=CTK_FONT_SMALL)
        self.cpu_sockets_entry.grid(row=3, column=1, padx=5, pady=5, sticky='ew')
        self.cpu_sockets_entry.insert(0, '1')
        self.cpu_sockets_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        # CPU Topology - Cores
        ctk.CTkLabel(cpu_frame, text='Cores:', font=CTK_FONT_MAIN, width=90, anchor='w').grid(
            row=4, column=0, padx=10, pady=5, sticky='w'
        )
        self.cpu_cores_entry = ctk.CTkEntry(cpu_frame, width=180, font=CTK_FONT_SMALL)
        self.cpu_cores_entry.grid(row=4, column=1, padx=5, pady=5, sticky='ew')
        self.cpu_cores_entry.insert(0, '2')
        self.cpu_cores_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        # CPU Topology - Threads
        ctk.CTkLabel(cpu_frame, text='Threads:', font=CTK_FONT_MAIN, width=90, anchor='w').grid(
            row=5, column=0, padx=10, pady=5, sticky='w'
        )
        self.cpu_threads_entry = ctk.CTkEntry(cpu_frame, width=180, font=CTK_FONT_SMALL)
        self.cpu_threads_entry.grid(row=5, column=1, padx=5, pady=5, sticky='ew')
        self.cpu_threads_entry.insert(0, '1')
        self.cpu_threads_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        # ===== 第 3 列: 内存配置 =====
        mem_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=8)
        mem_frame.grid(row=0, column=2, sticky='nsew', padx=5, pady=10)
        mem_frame.grid_columnconfigure(1, weight=1)
        # 配置所有行的权重
        for i in range(5):
            mem_frame.grid_rowconfigure(i, weight=0)

        ctk.CTkLabel(mem_frame, text='内存配置', font=CTK_FONT_BOLD, text_color='#81c784').grid(
            row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
        )

        # 内存大小
        ctk.CTkLabel(mem_frame, text='内存:', font=CTK_FONT_MAIN, width=90, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.memory_combo = ctk.CTkOptionMenu(
            mem_frame, values=memory_options, width=180, font=CTK_FONT_SMALL
        )
        self.memory_combo.set('2G')
        self.memory_combo.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        self.memory_combo.configure(command=self._trigger_change)

        # 当前内存
        ctk.CTkLabel(mem_frame, text='当前内存:', font=CTK_FONT_MAIN, width=90, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.current_memory_combo = ctk.CTkOptionMenu(
            mem_frame, values=memory_options, width=180, font=CTK_FONT_SMALL
        )
        self.current_memory_combo.set('2G')
        self.current_memory_combo.grid(row=2, column=1, padx=5, pady=5, sticky='ew')
        self.current_memory_combo.configure(command=self._trigger_change)

        # 最大内存
        ctk.CTkLabel(mem_frame, text='最大内存:', font=CTK_FONT_MAIN, width=90, anchor='w').grid(
            row=3, column=0, padx=10, pady=5, sticky='w'
        )
        self.max_memory_combo = ctk.CTkOptionMenu(
            mem_frame, values=memory_options, width=180, font=CTK_FONT_SMALL
        )
        self.max_memory_combo.set('4G')
        self.max_memory_combo.grid(row=3, column=1, padx=5, pady=5, sticky='ew')
        self.max_memory_combo.configure(command=self._trigger_change)

        # 交换内存
        ctk.CTkLabel(
            mem_frame, text='交换内存 (MB):', font=CTK_FONT_MAIN, width=90, anchor='w'
        ).grid(row=4, column=0, padx=10, pady=5, sticky='w')
        self.swap_entry = ctk.CTkEntry(
            mem_frame, placeholder_text='0', width=180, font=CTK_FONT_SMALL
        )
        self.swap_entry.grid(row=4, column=1, padx=5, pady=5, sticky='ew')
        self.swap_entry.insert(0, '0')
        self.swap_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

    def _parse_memory_value(self, value: str) -> int:
        """解析内存值字符串为 MB 整数.

        Args:
            value: 内存值字符串,如 '4G' 或 '512M'

        Returns:
            内存值(MB)
        """
        if not value:
            return 2048
        value = value.strip().upper()
        if value.endswith('G'):
            return int(value[:-1]) * 1024
        elif value.endswith('M'):
            return int(value[:-1])
        else:
            try:
                return int(value)
            except ValueError:
                return 2048

    def _trigger_change(self, *args):
        """触发变化回调."""
        if self.on_change_callback:
            self.on_change_callback()

    def _on_arch_change(self):
        """架构切换时更新机型."""
        arch = self.arch_type.get()
        if arch == 'x86':
            self.machine_type.set('virt')
        elif arch == 'arm':
            self.machine_type.set('arm-virt')
        self._trigger_change()

    def get_basic_config(self) -> dict:
        """获取基础配置.

        Returns:
            包含基础配置数据的字典
        """
        return {
            'arch': self.arch_type.get(),
            'name': self.vm_name_entry.get().strip() or 'vm0',
            'description': self.vm_desc_entry.get().strip(),
            'uuid': self.uuid_entry.get().strip(),
            'machine': self.machine_type.get(),
            'virt_type': self.virt_type.get(),
            'chipset': self.chipset_type.get(),
            'vcpu': int(self.vcpu_entry.get().strip() or '2'),
            'cpu_mode': self.cpu_mode.get(),
            'cpu_topology': {
                'sockets': int(self.cpu_sockets_entry.get().strip() or '1'),
                'cores': int(self.cpu_cores_entry.get().strip() or '2'),
                'threads': int(self.cpu_threads_entry.get().strip() or '1'),
            },
            'memory': self._parse_memory_value(self.memory_combo.get()),
            'current_memory': self._parse_memory_value(self.current_memory_combo.get()),
            'max_memory': self._parse_memory_value(self.max_memory_combo.get()),
            'swap': int(self.swap_entry.get().strip() or '0'),
        }

    def get_config(self) -> dict:
        """获取配置数据(兼容新接口)."""
        return self.get_basic_config()

    def to_xml(self) -> dict:
        """生成XML配置字典.

        Returns:
            包含XML配置的字典,用于XML生成器
        """
        config = self.get_basic_config()
        return {
            'name': config['name'],
            'title': config.get('description', ''),
            'description': config.get('description', ''),
            'uuid': config.get('uuid', ''),
            'memory_allocation': {
                'memory': config['memory'] * 1024,
                'current_memory': config['current_memory'] * 1024,
                'max_memory': config['max_memory'] * 1024,
                'unit': 'KiB',
            },
            'cpu_allocation': {
                'max_vcpu': config['vcpu'],
                'current_vcpu': config['vcpu'],
                'placement': 'static',
                'topology': config.get('cpu_topology', {}),
            },
            'cpu_model_topology': {
                'model': {
                    'mode': config.get('cpu_mode', 'host-model'),
                },
            },
            'os_booting': {
                'type': 'guest_firmware',
                'os_type': 'hvm',
                'arch': config.get('arch', 'x86_64'),
                'machine': config.get('machine', 'q35'),
            },
        }

    def load_config(self, config: dict):
        """加载配置数据到 UI.

        Args:
            config: 包含配置数据的字典
        """
        # 系统配置
        if 'name' in config:
            self.vm_name_entry.delete(0, ctk.END)
            self.vm_name_entry.insert(0, config['name'])
        if 'description' in config:
            self.vm_desc_entry.delete(0, ctk.END)
            self.vm_desc_entry.insert(0, config['description'])
        if 'uuid' in config:
            self.uuid_entry.delete(0, ctk.END)
            self.uuid_entry.insert(0, config['uuid'])
        if 'machine' in config:
            self.machine_type.set(config['machine'])
        if 'virt_type' in config:
            self.virt_type.set(config['virt_type'])
        if 'chipset' in config:
            self.chipset_type.set(config['chipset'])
        if 'arch' in config:
            self.arch_type.set(config['arch'])
            self._on_arch_change()

        # CPU 配置
        if 'vcpu' in config:
            self.vcpu_entry.delete(0, ctk.END)
            self.vcpu_entry.insert(0, str(config['vcpu']))
        if 'cpu_mode' in config:
            self.cpu_mode.set(config['cpu_mode'])
        if 'cpu_topology' in config:
            topology = config['cpu_topology']
            if 'sockets' in topology:
                self.cpu_sockets_entry.delete(0, ctk.END)
                self.cpu_sockets_entry.insert(0, str(topology['sockets']))
            if 'cores' in topology:
                self.cpu_cores_entry.delete(0, ctk.END)
                self.cpu_cores_entry.insert(0, str(topology['cores']))
            if 'threads' in topology:
                self.cpu_threads_entry.delete(0, ctk.END)
                self.cpu_threads_entry.insert(0, str(topology['threads']))

        # 内存配置
        if 'memory' in config:
            memory = config['memory']
            if isinstance(memory, int):
                # 转换为 GB 显示
                memory_gb = memory // 1024
                if memory_gb > 0:
                    self.memory_combo.set(f'{memory_gb}G')
                else:
                    self.memory_combo.set('1G')
        if 'current_memory' in config:
            current_memory = config['current_memory']
            if isinstance(current_memory, int):
                current_memory_gb = current_memory // 1024
                if current_memory_gb > 0:
                    self.current_memory_combo.set(f'{current_memory_gb}G')
                else:
                    self.current_memory_combo.set('1G')
        if 'max_memory' in config:
            max_memory = config['max_memory']
            if isinstance(max_memory, int):
                max_memory_gb = max_memory // 1024
                if max_memory_gb > 0:
                    self.max_memory_combo.set(f'{max_memory_gb}G')
                else:
                    self.max_memory_combo.set('2G')
        if 'swap' in config:
            self.swap_entry.delete(0, ctk.END)
            self.swap_entry.insert(0, str(config['swap']))
