"""Tab 切换开关 - 管理 24 个 Tab 的显示/隐藏."""

from typing import ClassVar

import customtkinter as ctk

from utils.styles import CTK_FONT_BOLD, CTK_FONT_SMALL
from utils.color import get_random_color


# Tab 配置 - 统一的配置
TABS_CONFIG: dict = {
    # 基础 Tab (默认启用)
    'general_metadata': {'name': '通用元数据', 'class': 'BasicTab', 'default_on': True},
    'os_booting': {'name': '系统启动', 'class': 'OSTab', 'default_on': True},
    'devices': {'name': 'Devices', 'class': 'DevicesTab', 'default_on': True},
    'cpu_allocation': {'name': 'CPU分配', 'class': 'CPUAllocationTab', 'default_on': True},
    'memory_allocation': {
        'name': 'Memory分配',
        'class': 'MemoryAllocationTab',
        'default_on': True,
    },
    # 高级调优 Tab (默认禁用)
    'smbios_system': {
        'name': 'SMBIOS系统信息',
        'class': 'SMBIOSSystemTab',
        'default_on': False,
    },
    'iothreads_allocation': {
        'name': 'IOThreads分配',
        'class': 'IOThreadsAllocationTab',
        'default_on': False,
    },
    'cpu_tuning': {'name': 'CPU调优', 'class': 'CPUTuningTab', 'default_on': False},
    'memory_backing': {'name': 'Memory支持', 'class': 'MemoryBackingTab', 'default_on': False},
    'memory_tuning': {'name': 'Memory调优', 'class': 'MemoryTuningTab', 'default_on': False},
    'numa_node_tuning': {
        'name': 'NUMA Node调优',
        'class': 'NUMANodeTuningTab',
        'default_on': False,
    },
    'block_io_tuning': {
        'name': 'Block I/O调优',
        'class': 'BlockIOTuningTab',
        'default_on': False,
    },
    'resource_partitioning': {
        'name': '资源分区',
        'class': 'ResourcePartitioningTab',
        'default_on': False,
    },
    'fibre_channel_vmid': {
        'name': '光纤通道VMID',
        'class': 'FibreChannelVMIDTab',
        'default_on': False,
    },
    'cpu_model_topology': {
        'name': 'CPU模型和拓扑',
        'class': 'CPUModelTopologyTab',
        'default_on': False,
    },
    'events_configuration': {
        'name': '事件配置',
        'class': 'EventsConfigurationTab',
        'default_on': False,
    },
    'power_management': {
        'name': '电源管理',
        'class': 'PowerManagementTab',
        'default_on': False,
    },
    'disk_throttle_group': {
        'name': '磁盘限流组',
        'class': 'DiskThrottleGroupTab',
        'default_on': False,
    },
    'hypervisor_features': {
        'name': '虚拟机特性',
        'class': 'HypervisorFeaturesTab',
        'default_on': False,
    },
    'time_keeping': {'name': '时间管理', 'class': 'TimeKeepingTab', 'default_on': False},
    'performance_monitoring': {
        'name': '性能监测',
        'class': 'PerformanceMonitoringTab',
        'default_on': False,
    },
    'security_label': {'name': '安全标签', 'class': 'SecurityLabelTab', 'default_on': False},
    'key_wrap': {'name': '密钥封装', 'class': 'KeyWrapTab', 'default_on': False},
    'launch_security': {
        'name': '启动安全',
        'class': 'LaunchSecurityTab',
        'default_on': False,
    },
}


class TabToggleSwitch(ctk.CTkFrame):
    """Tab 切换开关组件."""

    def __init__(
        self,
        master,
        tab_key: str,
        tab_display_name: str,
        on_change_callback=None,
        default_on: bool = True,
        text_color: str | None = None,
        **kwargs,
    ):
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent')

        self.tab_key = tab_key
        self.tab_display_name = tab_display_name
        self.on_change_callback = on_change_callback

        self.toggle_var = ctk.BooleanVar(value=default_on)

        # 如果没有指定颜色，随机选择一个
        self.text_color = text_color if text_color else get_random_color()

        self.toggle_switch = ctk.CTkCheckBox(
            self,
            text=tab_display_name,
            variable=self.toggle_var,
            command=self._on_toggle,
            font=CTK_FONT_SMALL,
            checkbox_width=14,
            checkbox_height=14,
            text_color=self.text_color,
        )
        self.toggle_switch.pack(side='left', padx=2, pady=0)

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

    def __init__(self, master, on_tab_toggle_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent')

        self.on_tab_toggle_callback = on_tab_toggle_callback
        self.toggle_switches = {}
        self.expanded = True

        self._create_switches()

    def _create_switches(self) -> None:
        """创建所有 Tab 的开关."""
        # 主面板配置 - 紧凑布局
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 内容框架
        content_frame = ctk.CTkFrame(self, fg_color='transparent')
        content_frame.grid(row=0, column=0, sticky='ew', pady=5)

        # 标签
        ctk.CTkLabel(
            content_frame,
            text='vm cfgs:',
            font=CTK_FONT_BOLD,
            text_color='#64b5f6',
        ).pack(side='left', padx=(3, 5), pady=0)

        # 创建开关框架 - 用于网格布局
        switch_frame = ctk.CTkFrame(content_frame, fg_color='transparent')
        switch_frame.pack(side='left', fill='x', expand=True)

        # 创建开关网格 - 12 列 x 多行, 紧凑布局
        row, col = 0, 0
        max_cols = 12

        for tab_key, config in TABS_CONFIG.items():
            switch = TabToggleSwitch(
                switch_frame,
                tab_key=tab_key,
                tab_display_name=config['name'],
                on_change_callback=self._on_toggle,
                default_on=config.get('default_on', True),
            )
            switch.grid(row=row, column=col, padx=1, pady=0, sticky='w')
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
