"""基础配置 Tab - 虚拟机名称、UUID、机型、CPU、内存等."""

from typing import Any

import customtkinter as ctk

from components.base_tab import BaseConfigTab
from utils.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN


class BasicTab(BaseConfigTab):
    """基础配置 Tab."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        # 架构类型变量
        self.arch_type: ctk.StringVar = ctk.StringVar(value='x86')

        # 控件引用
        self.vm_name_entry: ctk.CTkEntry | None = None
        # CPU 分配控件
        self.max_vcpu: ctk.CTkEntry | None = None
        self.current_vcpu: ctk.CTkEntry | None = None
        self.placement: ctk.CTkOptionMenu | None = None
        self.cpuset: ctk.CTkEntry | None = None
        # vCPU 实例列表
        self.vcpu_instances: list[dict[str, Any]] = []
        # 内存分配控件
        self.memory: ctk.CTkOptionMenu | None = None
        self.current_memory: ctk.CTkOptionMenu | None = None
        self.max_memory: ctk.CTkOptionMenu | None = None
        self.memory_slots: ctk.CTkEntry | None = None
        self.memory_unit: ctk.CTkOptionMenu | None = None
        self.dump_core: ctk.CTkOptionMenu | None = None

        super().__init__(master, on_change_callback, **kwargs)

    def _init_ui(self) -> None:
        """初始化界面 - 竖向布局."""
        from utils.parsers import MEMORY_OPTIONS

        # 配置单列布局
        self.grid_columnconfigure(0, weight=1)
        # 配置行权重，让 vCPU 列表区域可以伸展
        for i in range(3):
            self.grid_rowconfigure(i, weight=0)
        self.grid_rowconfigure(2, weight=1)

        # ===== 第 1 部分：System Configuration =====
        sys_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=8)
        sys_frame.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
        sys_frame.grid_columnconfigure(0, weight=1)
        sys_frame.grid_columnconfigure(1, weight=1)
        sys_frame.grid_columnconfigure(2, weight=1)
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
        ctk.CTkLabel(sys_frame, text='VM Name:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=1, column=2, padx=8, pady=3, sticky='w'
        )
        self.vm_name_entry = ctk.CTkEntry(sys_frame, placeholder_text='vm-name', width=150)
        self.vm_name_entry.grid(row=1, column=3, padx=2, pady=3, sticky='w')
        self.vm_name_entry.insert(0, 'vm0')
        self.vm_name_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        # ===== 第 2 部分：内存分配 =====
        mem_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=8)
        mem_frame.grid(row=1, column=0, sticky='ew', padx=5, pady=5)
        # 为6个控件配置12列（每个控件占2列）
        for i in range(12):
            mem_frame.grid_columnconfigure(i, weight=1)

        ctk.CTkLabel(mem_frame, text='内存分配', font=CTK_FONT_BOLD, text_color='#4caf50').grid(
            row=0, column=0, columnspan=12, padx=8, pady=3, sticky='w'
        )

        self.memory = self._create_label_option(
            mem_frame, '内存:', MEMORY_OPTIONS, '2G', width=100, row=1, column=0, label_width=80
        )
        self.current_memory = self._create_label_option(
            mem_frame,
            '当前内存:',
            ['None', *MEMORY_OPTIONS],
            'None',
            width=100,
            row=1,
            column=2,
            label_width=80,
        )
        self.max_memory = self._create_label_option(
            mem_frame,
            '最大内存:',
            ['None', *MEMORY_OPTIONS],
            'None',
            width=100,
            row=1,
            column=4,
            label_width=80,
        )
        self.memory_slots = self._create_label_entry(
            mem_frame,
            '内存槽位:',
            placeholder='16',
            default_value='16',
            width=100,
            row=1,
            column=6,
            label_width=80,
        )
        self.memory_unit = self._create_label_option(
            mem_frame,
            '单位:',
            ['KiB', 'MiB', 'GiB', 'TiB', 'KB', 'MB', 'GB', 'TB', 'b', 'bytes'],
            'KiB',
            width=100,
            row=1,
            column=8,
            label_width=80,
        )
        self.dump_core = self._create_label_option(
            mem_frame,
            'Dump Core:',
            ['None', 'on', 'off'],
            'None',
            width=100,
            row=1,
            column=10,
            label_width=80,
        )

        # ===== 第 3 部分：CPU 分配 =====
        cpu_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=8)
        cpu_frame.grid(row=2, column=0, sticky='ew', padx=5, pady=5)
        # 为4个控件配置8列（每个控件占2列）
        for i in range(8):
            cpu_frame.grid_columnconfigure(i, weight=1)

        ctk.CTkLabel(cpu_frame, text='CPU 分配', font=CTK_FONT_BOLD, text_color='#64b5f6').grid(
            row=0, column=0, columnspan=8, padx=8, pady=3, sticky='w'
        )

        self.max_vcpu = self._create_label_entry(
            cpu_frame,
            '最大 vCPU:',
            placeholder='2',
            default_value='2',
            width=120,
            row=1,
            column=0,
            label_width=80,
        )
        self.current_vcpu = self._create_label_entry(
            cpu_frame,
            '当前 vCPU:',
            placeholder='1',
            default_value='',
            width=120,
            row=1,
            column=2,
            label_width=80,
        )
        self.placement = self._create_label_option(
            cpu_frame,
            '放置模式:',
            ['None', 'static', 'auto'],
            'None',
            width=120,
            row=1,
            column=4,
            label_width=80,
        )
        self.cpuset = self._create_label_entry(
            cpu_frame,
            'CPU 亲和性:',
            placeholder='1-4,^3,6',
            default_value='',
            width=120,
            row=1,
            column=6,
            label_width=80,
        )

        # ===== 第 4 部分：vCPU 实例 =====
        self._create_section_title(cpu_frame, 'vCPU 实例', row=2, column=0, columnspan=8)
        btn_frame = ctk.CTkFrame(cpu_frame, fg_color='transparent')
        btn_frame.grid(row=3, column=0, columnspan=8, sticky='ew', pady=5)
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
        self.vcpu_list_frame.grid(row=4, column=0, columnspan=8, sticky='nsew')
        self.vcpu_list_frame.grid_columnconfigure(0, weight=1)
        self.vcpu_list_frame.configure(height=100)

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

    def get_basic_config(self) -> dict:  # type: ignore[override]
        """获取基础配置.

        Returns:
            包含基础配置数据的字典
        """
        from utils.parsers import parse_integer_value, parse_memory_value

        max_vcpu_raw = self.max_vcpu.get().strip()  # type: ignore[union-attr]
        max_vcpu = parse_integer_value(max_vcpu_raw, default=2) if max_vcpu_raw else None

        current_vcpu_raw = self.current_vcpu.get().strip()  # type: ignore[union-attr]
        current_vcpu = (
            parse_integer_value(current_vcpu_raw, default=1) if current_vcpu_raw else None
        )

        target_unit = self.memory_unit.get()  # type: ignore[union-attr]
        memory = parse_memory_value(self.memory.get(), target_unit=target_unit)  # type: ignore[union-attr]

        current_memory_raw = self.current_memory.get()  # type: ignore[union-attr]
        current_memory = (
            None
            if current_memory_raw == 'None'
            else parse_memory_value(current_memory_raw, target_unit=target_unit)
        )

        max_memory_raw = self.max_memory.get()  # type: ignore[union-attr]
        max_memory = (
            None
            if max_memory_raw == 'None'
            else parse_memory_value(max_memory_raw, target_unit=target_unit)
        )

        # 验证内存值关系: current_memory ≤ memory ≤ max_memory
        if current_memory is not None and current_memory > memory:
            current_memory = memory
        if max_memory is not None and memory > max_memory:
            memory = max_memory
        if current_memory is not None and max_memory is not None and current_memory > max_memory:
            current_memory = max_memory

        memory_config: dict[str, Any] = {
            'memory': memory,
            'unit': self.memory_unit.get(),  # type: ignore[union-attr]
        }
        dump_core_value = self.dump_core.get()  # type: ignore[union-attr]
        if dump_core_value != 'None':
            memory_config['dump_core'] = dump_core_value == 'on'
        if current_memory is not None:
            memory_config['current_memory'] = current_memory
        if max_memory is not None:
            memory_config['max_memory'] = max_memory
            memory_config['memory_slots'] = parse_integer_value(self.memory_slots.get(), default=16)  # type: ignore[union-attr]

        return {
            'arch': self.arch_type.get(),
            'name': self.vm_name_entry.get().strip() or 'vm0',  # type: ignore[union-attr]
            'title': '',
            'description': '',
            'cpu_allocation': {
                'max_vcpu': max_vcpu,
                'current_vcpu': current_vcpu,
                'placement': None if self.placement.get() == 'None' else self.placement.get(),  # type: ignore[union-attr]
                'cpuset': self.cpuset.get().strip() or None,  # type: ignore[union-attr]
                'vcpu_instances': [
                    {
                        'id': parse_integer_value(instance['id'].get(), default=i),  # type: ignore[union-attr]
                        'enabled': instance['enabled'].get(),  # type: ignore[union-attr]
                        'hotpluggable': instance['hotpluggable'].get(),  # type: ignore[union-attr]
                        **(
                            {'order': parse_integer_value(instance['order'].get())}  # type: ignore[union-attr]
                            if instance['order'].get().strip()  # type: ignore[union-attr]
                            else {}
                        ),
                    }
                    for i, instance in enumerate(self.vcpu_instances)
                ],
            },
            'memory_allocation': memory_config,
        }

    def get_config(self) -> dict:
        """获取配置数据 (兼容新接口)."""
        return self.get_basic_config()

    def to_xml(self) -> dict:
        """生成 XML 配置字典.

        Returns:
            包含 XML 配置的字典，用于 XML 生成器
        """
        config = self.get_basic_config()
        # 直接返回 get_basic_config 的结果，确保所有配置都被正确包含
        return config

    def load_config(self, config: dict) -> None:
        """加载配置数据到 UI.

        Args:
            config: 包含配置数据的字典
        """
        # 系统配置
        if 'name' in config:
            self.vm_name_entry.delete(0, ctk.END)  # type: ignore[union-attr]
            self.vm_name_entry.insert(0, config['name'])  # type: ignore[union-attr]
        if 'arch' in config:
            self.arch_type.set(config['arch'])
            self._on_arch_change()

        # CPU 分配配置
        if 'cpu_allocation' in config:
            cpu_alloc = config['cpu_allocation']
            if 'max_vcpu' in cpu_alloc:
                self.max_vcpu.delete(0, ctk.END)  # type: ignore[union-attr]
                if cpu_alloc['max_vcpu'] is not None:
                    self.max_vcpu.insert(0, str(cpu_alloc['max_vcpu']))  # type: ignore[union-attr]
            if 'current_vcpu' in cpu_alloc:
                self.current_vcpu.delete(0, ctk.END)  # type: ignore[union-attr]
                if cpu_alloc['current_vcpu'] is not None:
                    self.current_vcpu.insert(0, str(cpu_alloc['current_vcpu']))  # type: ignore[union-attr]
            if 'placement' in cpu_alloc:
                self.placement.set(  # type: ignore[union-attr]
                    'None' if cpu_alloc['placement'] is None else cpu_alloc['placement']
                )
            if 'cpuset' in cpu_alloc:
                self.cpuset.delete(0, ctk.END)  # type: ignore[union-attr]
                if cpu_alloc['cpuset']:
                    self.cpuset.insert(0, cpu_alloc['cpuset'])  # type: ignore[union-attr]
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
                        self.memory.set(f'{memory_gb}G')  # type: ignore[union-attr]
                    else:
                        self.memory.set('1G')  # type: ignore[union-attr]
            if 'current_memory' in mem_alloc:
                current_memory = mem_alloc['current_memory']
                if isinstance(current_memory, int):
                    current_memory_gb = current_memory // (1024 * 1024)
                    if current_memory_gb > 0:
                        self.current_memory.set(f'{current_memory_gb}G')  # type: ignore[union-attr]
                    else:
                        self.current_memory.set('1G')  # type: ignore[union-attr]
            if 'max_memory' in mem_alloc:
                max_memory = mem_alloc['max_memory']
                if isinstance(max_memory, int):
                    max_memory_gb = max_memory // (1024 * 1024)
                    if max_memory_gb > 0:
                        self.max_memory.set(f'{max_memory_gb}G')  # type: ignore[union-attr]
                    else:
                        self.max_memory.set('4G')  # type: ignore[union-attr]
            if 'memory_slots' in mem_alloc:
                self.memory_slots.delete(0, ctk.END)  # type: ignore[union-attr]
                self.memory_slots.insert(0, str(mem_alloc['memory_slots']))  # type: ignore[union-attr]
            if 'unit' in mem_alloc:
                self.memory_unit.set(mem_alloc['unit'])  # type: ignore[union-attr]
            if 'dump_core' in mem_alloc:
                self.dump_core.set(mem_alloc['dump_core'])  # type: ignore[union-attr]
