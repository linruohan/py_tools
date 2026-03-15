"""基础配置 Tab - 虚拟机名称、UUID、机型、CPU、内存等."""

import customtkinter as ctk

from components.base_tab import BaseConfigTab
from utils.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN


class BasicTab(BaseConfigTab):
    """基础配置 Tab."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        # 架构类型变量
        self.arch_type = ctk.StringVar(value='x86')

        # 控件引用
        self.vm_name_entry = None
        # CPU 分配控件
        self.max_vcpu = None
        self.current_vcpu = None
        self.placement = None
        self.cpuset = None
        # vCPU 实例列表
        self.vcpu_instances = []
        # 内存分配控件
        self.memory = None
        self.current_memory = None
        self.max_memory = None
        self.memory_slots = None
        self.memory_unit = None
        self.dump_core = None

        super().__init__(master, on_change_callback, **kwargs)

    def _init_ui(self) -> None:
        """初始化界面."""
        # 配置 grid 权重 - 2 列布局
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # ===== 第 1 行: 系统配置 =====
        sys_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=8)
        sys_frame.grid(row=0, column=0, columnspan=2, sticky='ew', padx=5, pady=5)
        sys_frame.grid_columnconfigure(1, weight=0)
        sys_frame.grid_columnconfigure(2, weight=0)
        sys_frame.grid_columnconfigure(3, weight=1)

        ctk.CTkLabel(
            sys_frame, text='System Configuration', font=CTK_FONT_BOLD, text_color='#64b5f6'
        ).grid(row=0, column=0, columnspan=4, padx=8, pady=3, sticky='w')

        # 架构选择器
        ctk.CTkLabel(
            sys_frame, text='Architecture:', font=CTK_FONT_MAIN, width=80, anchor='w'
        ).grid(row=1, column=0, padx=8, pady=3, sticky='w')
        arch_frame = ctk.CTkFrame(sys_frame, fg_color='transparent')
        arch_frame.grid(row=1, column=1, padx=2, pady=3, sticky='w')
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
        self.arch_x86_radio.grid(row=0, column=0, padx=2, sticky='w')

        self.arch_arm_radio = ctk.CTkRadioButton(
            arch_frame,
            text='ARM',
            variable=self.arch_type,
            value='arm',
            command=self._on_arch_change,
            font=CTK_FONT_MAIN,
        )
        self.arch_arm_radio.grid(row=0, column=1, padx=2, sticky='w')

        # 虚拟机名称
        ctk.CTkLabel(sys_frame, text='VM Name:', font=CTK_FONT_MAIN, width=60, anchor='w').grid(
            row=1, column=2, padx=8, pady=3, sticky='w'
        )
        self.vm_name_entry = ctk.CTkEntry(sys_frame, placeholder_text='vm-name', width=150)
        self.vm_name_entry.grid(row=1, column=3, padx=2, pady=3, sticky='ew')
        self.vm_name_entry.insert(0, 'vm0')
        self.vm_name_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        # ===== 第 2 行: CPU 和内存分配配置 =====
        from components.base_tab import create_two_column_layout
        from utils.parsers import MEMORY_OPTIONS

        # 创建一个容器来放置 CPU 和内存分配面板
        cpu_mem_frame = ctk.CTkFrame(self, fg_color='transparent')
        cpu_mem_frame.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=5, pady=5)
        cpu_mem_frame.grid_columnconfigure(0, weight=1)
        cpu_mem_frame.grid_columnconfigure(1, weight=1)

        # 使用 create_two_column_layout 创建两列布局
        cpu_frame, mem_frame = create_two_column_layout(
            cpu_mem_frame,
            left_title='CPU 分配',
            right_title='内存分配',
            left_color='#64b5f6',
            right_color='#4caf50',
        )

        # 基本 CPU 配置
        self.max_vcpu = self._create_label_entry(
            cpu_frame,
            '最大 vCPU:',
            placeholder='2',
            default_value='2',
            width=200,
            row=1,
            column=0,
        )
        self.current_vcpu = self._create_label_entry(
            cpu_frame,
            '当前 vCPU:',
            placeholder='1',
            default_value='1',
            width=200,
            row=2,
            column=0,
        )
        self.placement = self._create_label_option(
            cpu_frame, '放置模式:', ['static', 'auto'], 'static', width=200, row=3, column=0
        )
        self.cpuset = self._create_label_entry(
            cpu_frame,
            'CPU 亲和性:',
            placeholder='1-4,^3,6',
            default_value='1-4,^3,6',
            width=200,
            row=4,
            column=0,
        )

        # vCPU 实例
        self._create_section_title(cpu_frame, 'vCPU 实例', row=5, column=0, columnspan=2)
        btn_frame = ctk.CTkFrame(cpu_frame, fg_color='transparent')
        btn_frame.grid(row=6, column=0, columnspan=2, sticky='ew', pady=5)
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)

        add_btn = ctk.CTkButton(
            btn_frame,
            text='添加 vCPU',
            font=CTK_FONT_MAIN,
            command=lambda: self._add_vcpu_instance(cpu_frame),
        )
        add_btn.grid(row=0, column=0, padx=2, pady=2, sticky='ew')

        remove_btn = ctk.CTkButton(
            btn_frame,
            text='删除 vCPU',
            font=CTK_FONT_MAIN,
            command=lambda: self._remove_vcpu_instance(cpu_frame),
        )
        remove_btn.grid(row=0, column=1, padx=2, pady=2, sticky='ew')

        # vCPU 实例列表容器
        self.vcpu_list_frame = ctk.CTkFrame(cpu_frame, fg_color='transparent')
        self.vcpu_list_frame.grid(row=7, column=0, columnspan=2, sticky='nsew')
        self.vcpu_list_frame.grid_columnconfigure(0, weight=1)
        # 添加最小高度，确保即使没有 vCPU 实例也能占据足够空间
        self.vcpu_list_frame.configure(height=120)

        # 为 cpu_frame 添加行权重配置，确保 vCPU 列表区域即使为空也能占据空间
        for i in range(1, 7):
            cpu_frame.grid_rowconfigure(i, weight=0)
        cpu_frame.grid_rowconfigure(7, weight=1)

        # 默认不添加 vCPU 实例，保持 vcpu_instances 为空

        # 内存配置内容
        mem_frame.grid_columnconfigure(0, weight=1)
        mem_frame.grid_columnconfigure(1, weight=1)
        # 为内存面板添加行权重配置，与 CPU 面板保持一致
        for i in range(1, 8):
            mem_frame.grid_rowconfigure(i, weight=0)
        mem_frame.grid_rowconfigure(8, weight=1)

        # 内存基本配置
        self.memory = self._create_label_option(
            mem_frame, '内存:', MEMORY_OPTIONS, '2G', width=200, row=1, column=0
        )
        self.current_memory = self._create_label_option(
            mem_frame, '当前内存:', MEMORY_OPTIONS, '2G', width=200, row=2, column=0
        )
        self.max_memory = self._create_label_option(
            mem_frame, '最大内存:', MEMORY_OPTIONS, '4G', width=200, row=3, column=0
        )
        self.memory_slots = self._create_label_entry(
            mem_frame,
            '内存槽位:',
            placeholder='16',
            default_value='16',
            width=200,
            row=4,
            column=0,
        )
        self.memory_unit = self._create_label_option(
            mem_frame,
            '单位:',
            ['KiB', 'MiB', 'GiB', 'TiB', 'KB', 'MB', 'GB', 'TB', 'b', 'bytes'],
            'KiB',
            width=200,
            row=5,
            column=0,
        )
        self.dump_core = self._create_label_option(
            mem_frame, 'Dump Core:', ['on', 'off'], 'on', width=200, row=6, column=0
        )

        # 说明信息
        self._create_section_title(
            mem_frame, '说明', text_color='#ff9800', row=7, column=0, columnspan=2
        )
        info_text = (
            '内存 (memory):启动时分配的最大内存.\n'
            '当前内存 (currentMemory):实际分配的内存,可以小于最大值以支持内存气球.\n'
            '最大内存 (maxMemory):运行时可通过热插拔增加到的最大内存限制.'
        )
        self._create_info_label(mem_frame, info_text, row=8, column=0, columnspan=2)

    def _on_arch_change(self):
        """架构切换时的处理."""
        self._trigger_change()

    def _add_vcpu_instance(self, parent):
        """添加 vCPU 实例.

        Args:
            parent: 父容器
        """
        # 计算新 vCPU ID
        new_id = len(self.vcpu_instances)

        # 创建 vCPU 实例框架
        from utils.styles import BG_COLOR_SELECT

        instance_frame = ctk.CTkFrame(
            self.vcpu_list_frame, fg_color=BG_COLOR_SELECT, corner_radius=4
        )
        instance_frame.grid(row=len(self.vcpu_instances), column=0, sticky='ew', pady=2, padx=2)
        instance_frame.grid_columnconfigure(0, weight=1)
        instance_frame.grid_columnconfigure(1, weight=1)
        instance_frame.grid_columnconfigure(2, weight=1)
        instance_frame.grid_columnconfigure(3, weight=1)

        # vCPU ID
        id_entry = ctk.CTkEntry(instance_frame, placeholder_text=str(new_id), width=60)
        id_entry.grid(row=0, column=0, padx=2, pady=2, sticky='ew')
        id_entry.insert(0, str(new_id))
        id_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        # 启用状态
        enabled_var = ctk.BooleanVar(value=True if new_id == 0 else False)
        enabled_checkbox = ctk.CTkCheckBox(instance_frame, text='启用', variable=enabled_var)
        enabled_checkbox.grid(row=0, column=1, padx=2, pady=2, sticky='w')
        enabled_var.trace('w', lambda *args: self._trigger_change())

        # 热插拔
        hotpluggable_var = ctk.BooleanVar(value=False if new_id == 0 else True)
        hotpluggable_checkbox = ctk.CTkCheckBox(
            instance_frame, text='热插拔', variable=hotpluggable_var
        )
        hotpluggable_checkbox.grid(row=0, column=2, padx=2, pady=2, sticky='w')
        hotpluggable_var.trace('w', lambda *args: self._trigger_change())

        # 顺序
        order_entry = ctk.CTkEntry(instance_frame, placeholder_text=str(new_id + 1), width=60)
        order_entry.grid(row=0, column=3, padx=2, pady=2, sticky='ew')
        order_entry.insert(0, str(new_id + 1))
        order_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        # 保存实例信息
        self.vcpu_instances.append(
            {
                'frame': instance_frame,
                'id': id_entry,
                'enabled': enabled_var,
                'hotpluggable': hotpluggable_var,
                'order': order_entry,
            }
        )

        # 触发配置变更
        self._trigger_change()

    def _remove_vcpu_instance(self, parent):
        """删除 vCPU 实例.

        Args:
            parent: 父容器
        """
        if len(self.vcpu_instances) > 0:
            # 获取最后一个实例
            instance = self.vcpu_instances[-1]
            # 销毁框架
            instance['frame'].destroy()
            # 从列表中移除
            self.vcpu_instances.pop()
            # 触发配置变更
            self._trigger_change()

    def get_basic_config(self) -> dict:
        """获取基础配置.

        Returns:
            包含基础配置数据的字典
        """
        from utils.parsers import parse_integer_value, parse_memory_to_kib

        max_vcpu = parse_integer_value(self.max_vcpu.get(), default=2)
        current_vcpu = parse_integer_value(self.current_vcpu.get(), default=1)

        return {
            'arch': self.arch_type.get(),
            'name': self.vm_name_entry.get().strip() or 'vm0',
            'title': '',
            'description': '',
            'cpu_allocation': {
                'max_vcpu': max_vcpu,
                'current_vcpu': current_vcpu,
                'placement': self.placement.get(),
                'cpuset': self.cpuset.get().strip(),
                'vcpu_instances': [
                    {
                        'id': parse_integer_value(instance['id'].get(), default=i),
                        'enabled': instance['enabled'].get(),
                        'hotpluggable': instance['hotpluggable'].get(),
                        **(
                            {'order': parse_integer_value(instance['order'].get())}
                            if instance['order'].get().strip()
                            else {}
                        ),
                    }
                    for i, instance in enumerate(self.vcpu_instances)
                ],
            },
            'memory_allocation': {
                'memory': parse_memory_to_kib(self.memory.get()),
                'current_memory': parse_memory_to_kib(self.current_memory.get()),
                'max_memory': parse_memory_to_kib(self.max_memory.get()),
                'memory_slots': parse_integer_value(self.memory_slots.get(), default=16),
                'unit': self.memory_unit.get(),
                'dump_core': self.dump_core.get(),
            },
            'os_booting': {
                'type': 'guest_firmware',
                'os_type': 'hvm',
                'arch': self.arch_type.get(),
            },
        }

    def get_config(self) -> dict:
        """获取配置数据 (兼容新接口)."""
        return self.get_basic_config()

    def to_xml(self) -> dict:
        """生成 XML 配置字典.

        Returns:
            包含 XML 配置的字典, 用于 XML 生成器
        """
        config = self.get_basic_config()
        # 直接返回get_basic_config的结果，确保所有配置都被正确包含
        return config

    def load_config(self, config: dict):
        """加载配置数据到 UI.

        Args:
            config: 包含配置数据的字典
        """
        # 系统配置
        if 'name' in config:
            self.vm_name_entry.delete(0, ctk.END)
            self.vm_name_entry.insert(0, config['name'])
        if 'arch' in config:
            self.arch_type.set(config['arch'])
            self._on_arch_change()

        # CPU 分配配置
        if 'cpu_allocation' in config:
            cpu_alloc = config['cpu_allocation']
            if 'max_vcpu' in cpu_alloc:
                self.max_vcpu.delete(0, ctk.END)
                self.max_vcpu.insert(0, str(cpu_alloc['max_vcpu']))
            if 'current_vcpu' in cpu_alloc:
                self.current_vcpu.delete(0, ctk.END)
                self.current_vcpu.insert(0, str(cpu_alloc['current_vcpu']))
            if 'placement' in cpu_alloc:
                self.placement.set(cpu_alloc['placement'])
            if 'cpuset' in cpu_alloc:
                self.cpuset.delete(0, ctk.END)
                self.cpuset.insert(0, cpu_alloc['cpuset'])
            if 'vcpu_instances' in cpu_alloc:
                # 清空现有实例
                for instance in self.vcpu_instances:
                    instance['frame'].destroy()
                self.vcpu_instances = []

                # 加载 vCPU 实例
                for vcpu_instance in cpu_alloc['vcpu_instances']:
                    # 创建实例
                    new_id = len(self.vcpu_instances)
                    from utils.styles import BG_COLOR_SELECT

                    instance_frame = ctk.CTkFrame(
                        self.vcpu_list_frame, fg_color=BG_COLOR_SELECT, corner_radius=4
                    )
                    instance_frame.grid(row=new_id, column=0, sticky='ew', pady=2, padx=2)
                    instance_frame.grid_columnconfigure(0, weight=1)
                    instance_frame.grid_columnconfigure(1, weight=1)
                    instance_frame.grid_columnconfigure(2, weight=1)
                    instance_frame.grid_columnconfigure(3, weight=1)

                    # vCPU ID
                    id_entry = ctk.CTkEntry(instance_frame, placeholder_text=str(new_id), width=60)
                    id_entry.grid(row=0, column=0, padx=2, pady=2, sticky='ew')
                    id_entry.insert(0, str(vcpu_instance.get('id', new_id)))
                    id_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

                    # 启用状态
                    enabled_var = ctk.BooleanVar(
                        value=vcpu_instance.get('enabled', True if new_id == 0 else False)
                    )
                    enabled_checkbox = ctk.CTkCheckBox(
                        instance_frame, text='启用', variable=enabled_var
                    )
                    enabled_checkbox.grid(row=0, column=1, padx=2, pady=2, sticky='w')
                    enabled_var.trace('w', lambda *args: self._trigger_change())

                    # 热插拔
                    hotpluggable_var = ctk.BooleanVar(
                        value=vcpu_instance.get('hotpluggable', False if new_id == 0 else True)
                    )
                    hotpluggable_checkbox = ctk.CTkCheckBox(
                        instance_frame, text='热插拔', variable=hotpluggable_var
                    )
                    hotpluggable_checkbox.grid(row=0, column=2, padx=2, pady=2, sticky='w')
                    hotpluggable_var.trace('w', lambda *args: self._trigger_change())

                    # 顺序
                    order_entry = ctk.CTkEntry(
                        instance_frame, placeholder_text=str(new_id + 1), width=60
                    )
                    order_entry.grid(row=0, column=3, padx=2, pady=2, sticky='ew')
                    order_entry.insert(0, str(vcpu_instance.get('order', new_id + 1)))
                    order_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

                    # 保存实例信息
                    self.vcpu_instances.append(
                        {
                            'frame': instance_frame,
                            'id': id_entry,
                            'enabled': enabled_var,
                            'hotpluggable': hotpluggable_var,
                            'order': order_entry,
                        }
                    )
            elif 'vcpu_state' in cpu_alloc:
                # 兼容旧格式
                vcpu_state = cpu_alloc['vcpu_state']
                # 清空现有实例
                for instance in self.vcpu_instances:
                    instance['frame'].destroy()
                self.vcpu_instances = []

                # 创建单个实例
                from utils.styles import BG_COLOR_SELECT

                instance_frame = ctk.CTkFrame(
                    self.vcpu_list_frame, fg_color=BG_COLOR_SELECT, corner_radius=4
                )
                instance_frame.grid(row=0, column=0, sticky='ew', pady=2, padx=2)
                instance_frame.grid_columnconfigure(0, weight=1)
                instance_frame.grid_columnconfigure(1, weight=1)
                instance_frame.grid_columnconfigure(2, weight=1)
                instance_frame.grid_columnconfigure(3, weight=1)

                # vCPU ID
                id_entry = ctk.CTkEntry(instance_frame, placeholder_text='0', width=60)
                id_entry.grid(row=0, column=0, padx=2, pady=2, sticky='ew')
                id_entry.insert(0, str(vcpu_state.get('id', 0)))
                id_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

                # 启用状态
                enabled_var = ctk.BooleanVar(value=vcpu_state.get('enabled', True))
                enabled_checkbox = ctk.CTkCheckBox(
                    instance_frame, text='启用', variable=enabled_var
                )
                enabled_checkbox.grid(row=0, column=1, padx=2, pady=2, sticky='w')
                enabled_var.trace('w', lambda *args: self._trigger_change())

                # 热插拔
                hotpluggable_var = ctk.BooleanVar(value=vcpu_state.get('hotpluggable', False))
                hotpluggable_checkbox = ctk.CTkCheckBox(
                    instance_frame, text='热插拔', variable=hotpluggable_var
                )
                hotpluggable_checkbox.grid(row=0, column=2, padx=2, pady=2, sticky='w')
                hotpluggable_var.trace('w', lambda *args: self._trigger_change())

                # 顺序
                order_entry = ctk.CTkEntry(instance_frame, placeholder_text='1', width=60)
                order_entry.grid(row=0, column=3, padx=2, pady=2, sticky='ew')
                order_entry.insert(0, str(vcpu_state.get('order', 1)))
                order_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

                # 保存实例信息
                self.vcpu_instances.append(
                    {
                        'frame': instance_frame,
                        'id': id_entry,
                        'enabled': enabled_var,
                        'hotpluggable': hotpluggable_var,
                        'order': order_entry,
                    }
                )

        # 内存分配配置
        if 'memory_allocation' in config:
            mem_alloc = config['memory_allocation']
            if 'memory' in mem_alloc:
                memory = mem_alloc['memory']
                # 转换为 GB 显示
                if isinstance(memory, int):
                    # 从 KiB 转换为 GB
                    memory_gb = memory // (1024 * 1024)
                    if memory_gb > 0:
                        self.memory.set(f'{memory_gb}G')
                    else:
                        self.memory.set('1G')
            if 'current_memory' in mem_alloc:
                current_memory = mem_alloc['current_memory']
                if isinstance(current_memory, int):
                    current_memory_gb = current_memory // (1024 * 1024)
                    if current_memory_gb > 0:
                        self.current_memory.set(f'{current_memory_gb}G')
                    else:
                        self.current_memory.set('1G')
            if 'max_memory' in mem_alloc:
                max_memory = mem_alloc['max_memory']
                if isinstance(max_memory, int):
                    max_memory_gb = max_memory // (1024 * 1024)
                    if max_memory_gb > 0:
                        self.max_memory.set(f'{max_memory_gb}G')
                    else:
                        self.max_memory.set('4G')
            if 'memory_slots' in mem_alloc:
                self.memory_slots.delete(0, ctk.END)
                self.memory_slots.insert(0, str(mem_alloc['memory_slots']))
            if 'unit' in mem_alloc:
                self.memory_unit.set(mem_alloc['unit'])
            if 'dump_core' in mem_alloc:
                self.dump_core.set(mem_alloc['dump_core'])
