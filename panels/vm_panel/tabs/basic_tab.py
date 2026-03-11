"""基础配置 Tab - 虚拟机名称、UUID、机型、CPU、内存等."""

import customtkinter as ctk

from ..styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class BasicTab(ctk.CTkFrame):
    """基础配置 Tab."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent')
        self.on_change_callback = on_change_callback

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
        self.swap_combo = None
        # CPU Topology
        self.cpu_sockets_entry = None
        self.cpu_cores_entry = None
        self.cpu_threads_entry = None
        # NUMA
        self.numa_enabled = None
        self.numa_frame = None

        # 初始化 UI
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面."""
        # 配置 grid 权重
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)

        # 系统配置
        sys_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=8)
        sys_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=10)
        sys_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(sys_frame, text='系统配置', font=CTK_FONT_BOLD, text_color='#64b5f6').grid(
            row=0, column=0, columnspan=4, padx=10, pady=5, sticky='w'
        )

        # 第一行：虚拟机名称和描述
        ctk.CTkLabel(sys_frame, text='虚拟机名称:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=5, pady=5, sticky='w'
        )
        self.vm_name_entry = ctk.CTkEntry(sys_frame, placeholder_text='vm-name', width=200)
        self.vm_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.vm_name_entry.insert(0, 'vm0')

        ctk.CTkLabel(sys_frame, text='描述:', font=CTK_FONT_MAIN, width=60, anchor='w').grid(
            row=1, column=2, padx=5, pady=5, sticky='w'
        )
        self.vm_desc_entry = ctk.CTkEntry(sys_frame, placeholder_text='虚拟机描述', width=200)
        self.vm_desc_entry.grid(row=1, column=3, padx=5, pady=5, sticky='w')

        # 第二行：UUID 和 机型
        ctk.CTkLabel(sys_frame, text='UUID:', font=CTK_FONT_MAIN, width=60, anchor='w').grid(
            row=2, column=0, padx=5, pady=5, sticky='w'
        )
        self.uuid_entry = ctk.CTkEntry(sys_frame, placeholder_text='自动生成', width=300)
        self.uuid_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')

        ctk.CTkLabel(sys_frame, text='机型:', font=CTK_FONT_MAIN, width=60, anchor='w').grid(
            row=2, column=2, padx=5, pady=5, sticky='w'
        )
        self.machine_type = ctk.CTkOptionMenu(
            sys_frame,
            values=['q35', 'pc', 'pc-i440fx', 'virt', 'arm-virt'],
            width=120,
            font=CTK_FONT_SMALL,
        )
        self.machine_type.set('q35')
        self.machine_type.grid(row=2, column=3, padx=5, pady=5, sticky='w')

        # 第三行：虚拟化类型和芯片组
        ctk.CTkLabel(sys_frame, text='虚拟化:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=3, column=0, padx=5, pady=5, sticky='w'
        )
        self.virt_type = ctk.CTkOptionMenu(
            sys_frame, values=['hvm', 'pv', 'exe'], width=100, font=CTK_FONT_SMALL
        )
        self.virt_type.set('hvm')
        self.virt_type.grid(row=3, column=1, padx=5, pady=5, sticky='w')

        ctk.CTkLabel(sys_frame, text='芯片组:', font=CTK_FONT_MAIN, width=70, anchor='w').grid(
            row=3, column=2, padx=5, pady=5, sticky='w'
        )
        self.chipset_type = ctk.CTkOptionMenu(
            sys_frame, values=['PIIX3', 'PIIX4', 'Q35', 'virtio'], width=100, font=CTK_FONT_SMALL
        )
        self.chipset_type.set('Q35')
        self.chipset_type.grid(row=3, column=3, padx=5, pady=5, sticky='w')

        # CPU 配置
        cpu_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=8)
        cpu_frame.grid(row=1, column=0, sticky='ew', padx=10, pady=10)
        cpu_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(cpu_frame, text='CPU 配置', font=CTK_FONT_BOLD, text_color='#4caf50').grid(
            row=0, column=0, columnspan=6, padx=10, pady=5, sticky='w'
        )

        # 第一行：vCPU 数量和 CPU 模式
        ctk.CTkLabel(cpu_frame, text='vCPU:', font=CTK_FONT_MAIN, width=60, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.vcpu_entry = ctk.CTkEntry(cpu_frame, placeholder_text='2', width=80)
        self.vcpu_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.vcpu_entry.insert(0, '2')
        self.vcpu_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(cpu_frame, text='CPU 模式:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=1, column=2, padx=10, pady=5, sticky='w'
        )
        self.cpu_mode = ctk.CTkOptionMenu(
            cpu_frame,
            values=['host-passthrough', 'host-model', 'custom', 'host-model-required'],
            width=180,
            font=CTK_FONT_SMALL,
        )
        self.cpu_mode.set('host-model')
        self.cpu_mode.grid(row=1, column=3, padx=5, pady=5, sticky='w')
        self.cpu_mode.configure(command=self._trigger_change)

        # CPU Topology
        ctk.CTkLabel(cpu_frame, text='Sockets:', font=CTK_FONT_MAIN, width=60, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.cpu_sockets_entry = ctk.CTkEntry(cpu_frame, width=60, font=CTK_FONT_SMALL)
        self.cpu_sockets_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.cpu_sockets_entry.insert(0, '1')
        self.cpu_sockets_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(cpu_frame, text='Cores:', font=CTK_FONT_MAIN, width=60, anchor='w').grid(
            row=2, column=2, padx=10, pady=5, sticky='w'
        )
        self.cpu_cores_entry = ctk.CTkEntry(cpu_frame, width=60, font=CTK_FONT_SMALL)
        self.cpu_cores_entry.grid(row=2, column=3, padx=5, pady=5, sticky='w')
        self.cpu_cores_entry.insert(0, '2')
        self.cpu_cores_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(cpu_frame, text='Threads:', font=CTK_FONT_MAIN, width=60, anchor='w').grid(
            row=2, column=4, padx=10, pady=5, sticky='w'
        )
        self.cpu_threads_entry = ctk.CTkEntry(cpu_frame, width=60, font=CTK_FONT_SMALL)
        self.cpu_threads_entry.grid(row=2, column=5, padx=5, pady=5, sticky='w')
        self.cpu_threads_entry.insert(0, '1')
        self.cpu_threads_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        # NUMA 配置
        numa_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=8)
        numa_frame.grid(row=3, column=0, sticky='ew', padx=10, pady=10)
        numa_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(numa_frame, text='NUMA 配置', font=CTK_FONT_BOLD, text_color='#ab47bc').grid(
            row=0, column=0, columnspan=4, padx=10, pady=5, sticky='w'
        )

        self.numa_enabled = ctk.CTkCheckBox(
            numa_frame, text='启用 NUMA', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.numa_enabled.grid(row=1, column=0, padx=10, pady=5, sticky='w')

        # 内存配置 - 生成 1G 2G 4G ... 128G 的选项
        memory_options = ['1G', '2G', '4G', '8G', '16G', '32G', '64G', '128G']

        mem_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=8)
        mem_frame.grid(row=2, column=0, sticky='ew', padx=10, pady=10)
        mem_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(mem_frame, text='内存配置', font=CTK_FONT_BOLD, text_color='#81c784').grid(
            row=0, column=0, columnspan=3, padx=10, pady=5, sticky='w'
        )

        # 内存大小（下拉框）
        ctk.CTkLabel(mem_frame, text='内存:', font=CTK_FONT_MAIN, width=60, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.memory_combo = ctk.CTkOptionMenu(
            mem_frame, values=memory_options, width=100, font=CTK_FONT_SMALL
        )
        self.memory_combo.set('2G')
        self.memory_combo.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        # 当前内存（下拉框）
        ctk.CTkLabel(mem_frame, text='当前内存:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=1, column=2, padx=10, pady=5, sticky='w'
        )
        self.current_memory_combo = ctk.CTkOptionMenu(
            mem_frame, values=memory_options, width=100, font=CTK_FONT_SMALL
        )
        self.current_memory_combo.set('2G')
        self.current_memory_combo.grid(row=1, column=3, padx=5, pady=5, sticky='w')

        # 最大内存（下拉框）
        ctk.CTkLabel(mem_frame, text='最大内存:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.max_memory_combo = ctk.CTkOptionMenu(
            mem_frame, values=memory_options, width=100, font=CTK_FONT_SMALL
        )
        self.max_memory_combo.set('4G')
        self.max_memory_combo.grid(row=2, column=1, padx=5, pady=5, sticky='w')

        # 交换内存（输入框）
        ctk.CTkLabel(
            mem_frame, text='交换内存 (MB):', font=CTK_FONT_MAIN, width=100, anchor='w'
        ).grid(row=2, column=2, padx=10, pady=5, sticky='w')
        self.swap_entry = ctk.CTkEntry(
            mem_frame, placeholder_text='0', width=100, font=CTK_FONT_SMALL
        )
        self.swap_entry.grid(row=2, column=3, padx=5, pady=5, sticky='w')
        self.swap_entry.insert(0, '0')

    def _parse_memory_value(self, value: str) -> int:
        """解析内存值字符串为 MB 整数.

        Args:
            value: 内存值字符串，如 '4G' 或 '512M'

        Returns:
            内存值（MB）
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

    def _trigger_change(self):
        """触发变化回调."""
        if self.on_change_callback:
            self.on_change_callback()

    def get_basic_config(self) -> dict:
        """获取基础配置.

        Returns:
            包含基础配置数据的字典
        """
        return {
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
            'numa': self.numa_enabled.get(),
            'memory': self._parse_memory_value(self.memory_combo.get()),
            'current_memory': self._parse_memory_value(self.current_memory_combo.get()),
            'max_memory': self._parse_memory_value(self.max_memory_combo.get()),
            'swap': int(self.swap_entry.get().strip() or '0'),
        }
