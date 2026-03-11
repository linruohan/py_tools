"""Tab 切换开关 - 根据开关状态动态添加/删除 Tab."""

import customtkinter as ctk

from .styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_SMALL
from .tabs import BasicTab, DevicesTab, StorageTab


class TabToggleSwitch(ctk.CTkFrame):
    """Tab 切换开关组件."""

    def __init__(
        self,
        master,
        tab_name: str,
        tab_display_name: str,
        on_change_callback=None,
        disabled: bool = False,
        default_on: bool = True,
        **kwargs,
    ):
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent')

        self.tab_name = tab_name
        self.tab_display_name = tab_display_name
        self.on_change_callback = on_change_callback
        self.disabled = disabled

        # 创建开关变量和控件
        self.toggle_var = ctk.BooleanVar(value=default_on and not disabled)

        self.toggle_switch = ctk.CTkCheckBox(
            self,
            text=tab_display_name,
            variable=self.toggle_var,
            command=self._on_toggle,
            state='disabled' if disabled else 'normal',
            font=CTK_FONT_SMALL,
        )
        self.toggle_switch.pack(side='left', padx=5, pady=2)

    def _on_toggle(self) -> None:
        """开关状态改变时的回调."""
        if self.on_change_callback:
            self.on_change_callback(self.tab_name, self.toggle_var.get())

    def set_state(self, enabled: bool) -> None:
        """设置开关状态."""
        self.toggle_var.set(enabled)

    def is_enabled(self) -> bool:
        """获取开关状态."""
        return self.toggle_var.get()


class TabTogglePanel(ctk.CTkFrame):
    """Tab 切换开关面板 - 管理所有 Tab 的开关."""

    # 定义所有 Tab 的配置
    TABS_CONFIG = {
        'general_metadata': {
            'name': '基础信息',
            'disabled': False,
            'default_on': True,
            'class': BasicTab,
            'has_callback': True,
        },
        'os_booting': {
            'name': '系统引导',
            'disabled': False,
            'default_on': True,
            'class': None,
            'has_callback': False,
        },
        'smbios_system': {
            'name': 'SMBIOS 系统信息',
            'disabled': False,
            'default_on': False,
            'class': None,
            'has_callback': False,
        },
        'cpu_allocation': {
            'name': 'CPU 分配',
            'disabled': False,
            'default_on': True,
            'class': None,
            'has_callback': False,
        },
        'iothreads_allocation': {
            'name': 'IO 线程分配',
            'disabled': False,
            'default_on': False,
            'class': None,
            'has_callback': False,
        },
        'cpu_tuning': {
            'name': 'CPU 优化',
            'disabled': False,
            'default_on': False,
            'class': None,
            'has_callback': False,
        },
        'memory_allocation': {
            'name': '内存分配',
            'disabled': False,
            'default_on': True,
            'class': None,
            'has_callback': False,
        },
        'memory_backing': {
            'name': '内存后端',
            'disabled': False,
            'default_on': False,
            'class': None,
            'has_callback': False,
        },
        'memory_tuning': {
            'name': '内存优化',
            'disabled': False,
            'default_on': False,
            'class': None,
            'has_callback': False,
        },
        'numa_node_tuning': {
            'name': 'NUMA 节点优化',
            'disabled': False,
            'default_on': False,
            'class': None,
            'has_callback': False,
        },
        'block_io_tuning': {
            'name': '块 I/O 优化',
            'disabled': False,
            'default_on': False,
            'class': None,
            'has_callback': False,
        },
        'resource_partitioning': {
            'name': '资源分区',
            'disabled': False,
            'default_on': False,
            'class': None,
            'has_callback': False,
        },
        'fibre_channel_vmid': {
            'name': '光纤通道 VMID',
            'disabled': False,
            'default_on': False,
            'class': None,
            'has_callback': False,
        },
        'cpu_model_topology': {
            'name': 'CPU 模型与拓扑',
            'disabled': False,
            'default_on': False,
            'class': None,
            'has_callback': False,
        },
        'events_configuration': {
            'name': '事件配置',
            'disabled': False,
            'default_on': False,
            'class': None,
            'has_callback': False,
        },
        'power_management': {
            'name': '电源管理',
            'disabled': False,
            'default_on': False,
            'class': None,
            'has_callback': False,
        },
        'disk_throttle_group': {
            'name': '磁盘节流组管理',
            'disabled': False,
            'default_on': False,
            'class': None,
            'has_callback': False,
        },
        'hypervisor_features': {
            'name': '虚拟化特性',
            'disabled': False,
            'default_on': False,
            'class': None,
            'has_callback': False,
        },
        'time_keeping': {
            'name': '时间同步',
            'disabled': False,
            'default_on': False,
            'class': None,
            'has_callback': False,
        },
        'performance_monitoring': {
            'name': '性能监控事件',
            'disabled': False,
            'default_on': False,
            'class': None,
            'has_callback': False,
        },
        'devices': {
            'name': '设备',
            'disabled': False,
            'default_on': True,
            'class': DevicesTab,
            'has_callback': True,
        },
        'security_label': {
            'name': '安全标签',
            'disabled': False,
            'default_on': False,
            'class': None,
            'has_callback': False,
        },
        'key_wrap': {
            'name': '密钥封装',
            'disabled': False,
            'default_on': True,
            'class': StorageTab,
            'has_callback': True,
        },
        'launch_security': {
            'name': '启动安全',
            'disabled': False,
            'default_on': False,
            'class': None,
            'has_callback': False,
        },
    }

    def __init__(self, master, on_tab_toggle_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color=BG_COLOR_CONTENT, corner_radius=6)

        self.on_tab_toggle_callback = on_tab_toggle_callback
        self.toggle_switches = {}
        self.expanded = True

        # 创建开关面板
        self._create_switches()

    def _create_switches(self) -> None:
        """创建所有 Tab 的开关."""
        # 配置列权重 - 所有列权重为 0，保持左对齐
        for col in range(25):
            self.grid_columnconfigure(col, weight=0)

        # 标题
        ctk.CTkLabel(
            self,
            text='Tab 显示控制:',
            font=CTK_FONT_BOLD,
            text_color='#64b5f6',
        ).grid(row=0, column=0, padx=10, pady=5, sticky='w')

        # 创建开关 - 两行布局
        tab_keys = list(self.TABS_CONFIG.keys())
        mid_point = len(tab_keys) // 2

        # 第一行
        for i, tab_key in enumerate(tab_keys[:mid_point]):
            tab_config = self.TABS_CONFIG[tab_key]
            switch = TabToggleSwitch(
                self,
                tab_name=tab_key,
                tab_display_name=tab_config['name'],
                on_change_callback=self._on_tab_toggle,
                disabled=tab_config['disabled'],
                default_on=tab_config.get('default_on', True),
            )
            switch.grid(row=1, column=i, padx=5, pady=2, sticky='w')
            self.toggle_switches[tab_key] = switch

        # 第二行
        for i, tab_key in enumerate(tab_keys[mid_point:]):
            tab_config = self.TABS_CONFIG[tab_key]
            switch = TabToggleSwitch(
                self,
                tab_name=tab_key,
                tab_display_name=tab_config['name'],
                on_change_callback=self._on_tab_toggle,
                disabled=tab_config['disabled'],
                default_on=tab_config.get('default_on', True),
            )
            switch.grid(row=2, column=i, padx=5, pady=2, sticky='w')
            self.toggle_switches[tab_key] = switch

        # 展开/收起按钮
        self.toggle_btn = ctk.CTkButton(
            self,
            text='▼',
            width=30,
            fg_color='transparent',
            border_width=1,
            hover_color='#e0e0e0',
            font=CTK_FONT_SMALL,
            command=self._toggle_panel,
        )
        btn_col = max(mid_point, len(tab_keys) - mid_point)
        self.toggle_btn.grid(row=1, column=btn_col, rowspan=2, padx=10, pady=2, sticky='e')

    def _on_tab_toggle(self, tab_name: str, enabled: bool) -> None:
        """Tab 开关改变时的回调."""
        if self.on_tab_toggle_callback:
            self.on_tab_toggle_callback(tab_name, enabled)

    def _toggle_panel(self) -> None:
        """展开/收起面板."""
        if self.expanded:
            # 收起 - 隐藏第二行
            mid_point = len(self.TABS_CONFIG) // 2
            for i, (tab_key, switch) in enumerate(self.toggle_switches.items()):
                if i >= mid_point:
                    switch.grid_remove()
            self.toggle_btn.configure(text='▲')
            self.expanded = False
        else:
            # 展开 - 显示所有
            mid_point = len(self.TABS_CONFIG) // 2
            for i, (tab_key, switch) in enumerate(self.toggle_switches.items()):
                if i < mid_point:
                    switch.grid(row=1, column=i, padx=5, pady=2, sticky='w')
                else:
                    switch.grid(row=2, column=(i - mid_point), padx=5, pady=2, sticky='w')
            self.toggle_btn.configure(text='▼')
            self.expanded = True

    def set_tab_state(self, tab_name: str, enabled: bool) -> None:
        """设置指定 Tab 的开关状态."""
        if tab_name in self.toggle_switches:
            self.toggle_switches[tab_name].set_state(enabled)

    def get_tab_state(self, tab_name: str) -> bool:
        """获取指定 Tab 的开关状态."""
        if tab_name in self.toggle_switches:
            return self.toggle_switches[tab_name].is_enabled()
        return False

    def get_all_states(self) -> dict:
        """获取所有 Tab 的开关状态."""
        return {tab_name: switch.is_enabled() for tab_name, switch in self.toggle_switches.items()}
