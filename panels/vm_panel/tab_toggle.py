"""Tab 切换开关 - 根据开关状态动态添加/删除 Tab."""

import customtkinter as ctk

from .styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_SMALL
from .tabs import (
    BasicTab,
    BlockIOTuningTab,
    CPUAllocationTab,
    CPUModelTopologyTab,
    CPUTuningTab,
    DevicesTab,
    DiskThrottleGroupTab,
    EventsConfigurationTab,
    FibreChannelVMIDTab,
    HypervisorFeaturesTab,
    IOThreadsAllocationTab,
    KeyWrapTab,
    LaunchSecurityTab,
    MemoryAllocationTab,
    MemoryBackingTab,
    MemoryTuningTab,
    NUMANodeTuningTab,
    OSBootingTab,
    PerformanceMonitoringTab,
    PowerManagementTab,
    ResourcePartitioningTab,
    SecurityLabelTab,
    SMBIOSSystemTab,
    TimeKeepingTab,
)


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
            'class': OSBootingTab,
            'has_callback': True,
        },
        'smbios_system': {
            'name': 'SMBIOS',
            'disabled': False,
            'default_on': False,
            'class': SMBIOSSystemTab,
            'has_callback': True,
        },
        'cpu_allocation': {
            'name': 'CPU分配',
            'disabled': False,
            'default_on': True,
            'class': CPUAllocationTab,
            'has_callback': True,
        },
        'iothreads_allocation': {
            'name': 'IO线程',
            'disabled': False,
            'default_on': False,
            'class': IOThreadsAllocationTab,
            'has_callback': True,
        },
        'cpu_tuning': {
            'name': 'CPU优化',
            'disabled': False,
            'default_on': False,
            'class': CPUTuningTab,
            'has_callback': True,
        },
        'memory_allocation': {
            'name': '内存分配',
            'disabled': False,
            'default_on': True,
            'class': MemoryAllocationTab,
            'has_callback': True,
        },
        'memory_backing': {
            'name': '内存后端',
            'disabled': False,
            'default_on': False,
            'class': MemoryBackingTab,
            'has_callback': True,
        },
        'memory_tuning': {
            'name': '内存优化',
            'disabled': False,
            'default_on': False,
            'class': MemoryTuningTab,
            'has_callback': True,
        },
        'numa_node_tuning': {
            'name': 'NUMA优化',
            'disabled': False,
            'default_on': False,
            'class': NUMANodeTuningTab,
            'has_callback': True,
        },
        'block_io_tuning': {
            'name': '块IO优化',
            'disabled': False,
            'default_on': False,
            'class': BlockIOTuningTab,
            'has_callback': True,
        },
        'resource_partitioning': {
            'name': '资源分区',
            'disabled': False,
            'default_on': False,
            'class': ResourcePartitioningTab,
            'has_callback': True,
        },
        'fibre_channel_vmid': {
            'name': 'FC VMID',
            'disabled': False,
            'default_on': False,
            'class': FibreChannelVMIDTab,
            'has_callback': True,
        },
        'cpu_model_topology': {
            'name': 'CPU模型',
            'disabled': False,
            'default_on': False,
            'class': CPUModelTopologyTab,
            'has_callback': True,
        },
        'events_configuration': {
            'name': '事件配置',
            'disabled': False,
            'default_on': False,
            'class': EventsConfigurationTab,
            'has_callback': True,
        },
        'power_management': {
            'name': '电源管理',
            'disabled': False,
            'default_on': False,
            'class': PowerManagementTab,
            'has_callback': True,
        },
        'disk_throttle_group': {
            'name': '磁盘节流组',
            'disabled': False,
            'default_on': False,
            'class': DiskThrottleGroupTab,
            'has_callback': True,
        },
        'hypervisor_features': {
            'name': '虚拟化特性',
            'disabled': False,
            'default_on': False,
            'class': HypervisorFeaturesTab,
            'has_callback': True,
        },
        'time_keeping': {
            'name': '时间同步',
            'disabled': False,
            'default_on': False,
            'class': TimeKeepingTab,
            'has_callback': True,
        },
        'performance_monitoring': {
            'name': '性能监控',
            'disabled': False,
            'default_on': False,
            'class': PerformanceMonitoringTab,
            'has_callback': True,
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
            'class': SecurityLabelTab,
            'has_callback': True,
        },
        'key_wrap': {
            'name': '密钥包装',
            'disabled': False,
            'default_on': False,
            'class': KeyWrapTab,
            'has_callback': True,
        },
        'launch_security': {
            'name': '启动安全',
            'disabled': False,
            'default_on': False,
            'class': LaunchSecurityTab,
            'has_callback': True,
        },
    }

    def __init__(self, master, on_tab_toggle_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color=BG_COLOR_CONTENT, corner_radius=6)

        self.on_tab_toggle_callback = on_tab_toggle_callback
        self.toggle_switches = {}
        self.expanded = True

        self._create_switches()

    def _create_switches(self) -> None:
        """创建所有 Tab 的开关."""
        for col in range(30):
            self.grid_columnconfigure(col, weight=0)

        ctk.CTkLabel(
            self,
            text='Tab显示:',
            font=CTK_FONT_BOLD,
            text_color='#64b5f6',
        ).grid(row=0, column=0, padx=10, pady=5, sticky='w')

        tab_keys = list(self.TABS_CONFIG.keys())
        mid_point = (len(tab_keys) + 1) // 2

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
        self.toggle_btn.grid(row=1, column=btn_col + 1, rowspan=2, padx=10, pady=2, sticky='e')

    def _on_tab_toggle(self, tab_name: str, enabled: bool) -> None:
        """Tab 开关改变时的回调."""
        if self.on_tab_toggle_callback:
            self.on_tab_toggle_callback(tab_name, enabled)

    def _toggle_panel(self) -> None:
        """展开/收起面板."""
        if self.expanded:
            tab_keys = list(self.TABS_CONFIG.keys())
            mid_point = (len(tab_keys) + 1) // 2
            for i, (tab_key, switch) in enumerate(self.toggle_switches.items()):
                if i >= mid_point:
                    switch.grid_remove()
            self.toggle_btn.configure(text='▲')
            self.expanded = False
        else:
            tab_keys = list(self.TABS_CONFIG.keys())
            mid_point = (len(tab_keys) + 1) // 2
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
