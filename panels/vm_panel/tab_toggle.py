"""Tab 切换开关 - 管理 24 个 Tab 的显示/隐藏."""

import customtkinter as ctk

from .styles import CTK_FONT_BOLD, CTK_FONT_SMALL


class TabToggleSwitch(ctk.CTkFrame):
    """Tab 切换开关组件."""

    def __init__(
        self,
        master,
        tab_key: str,
        tab_display_name: str,
        on_change_callback=None,
        default_on: bool = True,
        **kwargs,
    ):
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent')

        self.tab_key = tab_key
        self.tab_display_name = tab_display_name
        self.on_change_callback = on_change_callback

        self.toggle_var = ctk.BooleanVar(value=default_on)

        self.toggle_switch = ctk.CTkCheckBox(
            self,
            text=tab_display_name,
            variable=self.toggle_var,
            command=self._on_toggle,
            font=CTK_FONT_SMALL,
        )
        self.toggle_switch.pack(side='left', padx=5, pady=2)

    def _on_toggle(self) -> None:
        """开关状态改变时的回调."""
        if self.on_change_callback:
            self.on_change_callback(self.tab_key, self.toggle_var.get())

    def set_state(self, enabled: bool) -> None:
        """设置开关状态."""
        self.toggle_var.set(enabled)

    def is_enabled(self) -> bool:
        """获取开关状态."""
        return self.toggle_var.get()


class TabTogglePanel(ctk.CTkFrame):
    """Tab 切换开关面板 - 管理 24 个 Tab 的开关."""

    # Tab 配置 - 与 vm_panel.py 中的 TABS_CONFIG 保持一致
    TABS_CONFIG = {
        # 基础 Tab (默认启用)
        'general_metadata': {'name': 'General Metadata', 'default_on': True},
        'os_booting': {'name': 'Os Booting', 'default_on': True},
        'devices': {'name': 'Devices', 'default_on': True},
        'cpu_allocation': {'name': 'CPU Allocation', 'default_on': True},
        'memory_allocation': {'name': 'Memory Allocation', 'default_on': True},
        # 高级调优 Tab (默认禁用)
        'smbios_system': {'name': 'SMBIOS System Info', 'default_on': False},
        'iothreads_allocation': {'name': 'IOThreads Allocation', 'default_on': False},
        'cpu_tuning': {'name': 'CPU Tuning', 'default_on': False},
        'memory_backing': {'name': 'Memory Backing', 'default_on': False},
        'memory_tuning': {'name': 'Memory Tuning', 'default_on': False},
        'numa_node_tuning': {'name': 'NUMA Node Tuning', 'default_on': False},
        'block_io_tuning': {'name': 'Block I/O Tuning', 'default_on': False},
        'resource_partitioning': {'name': 'Resource Partitioning', 'default_on': False},
        'fibre_channel_vmid': {'name': 'Fibre Channel VMID', 'default_on': False},
        'cpu_model_topology': {'name': 'CPU Model & Topology', 'default_on': False},
        'events_configuration': {'name': 'Events Configuration', 'default_on': False},
        'power_management': {'name': 'Power Management', 'default_on': False},
        'disk_throttle_group': {'name': 'Disk Throttle Group', 'default_on': False},
        'hypervisor_features': {'name': 'Hypervisor Features', 'default_on': False},
        'time_keeping': {'name': 'Time Keeping', 'default_on': False},
        'performance_monitoring': {'name': 'Performance Monitoring', 'default_on': False},
        'security_label': {'name': 'Security Label', 'default_on': False},
        'key_wrap': {'name': 'Key Wrap', 'default_on': False},
        'launch_security': {'name': 'Launch Security', 'default_on': False},
    }

    def __init__(self, master, on_tab_toggle_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent')
        self.configure(height=120)  # 设置固定高度

        self.on_tab_toggle_callback = on_tab_toggle_callback
        self.toggle_switches = {}
        self.expanded = True

        self._create_switches()

    def _create_switches(self) -> None:
        """创建所有 Tab 的开关."""
        # 创建可滚动框架，设置固定高度
        scrollable_frame = ctk.CTkScrollableFrame(
            self, fg_color='transparent', height=100
        )
        scrollable_frame.grid(row=0, column=0, sticky='nsew')
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 标签
        ctk.CTkLabel(
            scrollable_frame,
            text='Tab 显示:',
            font=CTK_FONT_BOLD,
            text_color='#64b5f6',
        ).pack(anchor='w', padx=5, pady=2)

        # 创建开关框架 - 用于网格布局
        switch_frame = ctk.CTkFrame(scrollable_frame, fg_color='transparent')
        switch_frame.pack(fill='x', pady=2)

        # 创建开关网格 - 5 列 x 5 行
        row, col = 0, 0
        max_cols = 5

        for tab_key, config in self.TABS_CONFIG.items():
            switch = TabToggleSwitch(
                switch_frame,
                tab_key=tab_key,
                tab_display_name=config['name'],
                on_change_callback=self._on_toggle,
                default_on=config.get('default_on', True),
            )
            switch.grid(row=row, column=col, padx=3, pady=1, sticky='w')
            self.toggle_switches[tab_key] = switch

            col += 1
            if col >= max_cols:
                col = 0
                row += 1

    def _on_toggle(self, tab_key: str, enabled: bool) -> None:
        """Tab 开关改变时的回调."""
        if self.on_tab_toggle_callback:
            self.on_tab_toggle_callback(tab_key, enabled)

    def set_tab_state(self, tab_key: str, enabled: bool) -> None:
        """设置指定 Tab 的开关状态."""
        if tab_key in self.toggle_switches:
            self.toggle_switches[tab_key].set_state(enabled)

    def get_tab_state(self, tab_key: str) -> bool:
        """获取指定 Tab 的开关状态."""
        if tab_key in self.toggle_switches:
            return self.toggle_switches[tab_key].is_enabled()
        return False

    def get_all_states(self) -> dict:
        """获取所有 Tab 的开关状态."""
        return {tab_key: switch.is_enabled() for tab_key, switch in self.toggle_switches.items()}
