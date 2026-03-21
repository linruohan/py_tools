"""性能监控事件配置 Tab - Performance Monitoring Events.

根据 libvirt 文档第 20 章实现:
https://www.libvirt.org/formatdomain.html#perf
"""

import customtkinter as ctk

from components.base_tab import BaseConfigTab
from components.event_toggle import EventToggleSwitch
from utils.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_SMALL


class PerformanceMonitoringTab(BaseConfigTab):
    """性能监控事件配置 Tab."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        # 在调用父类 __init__ 之前初始化实例属性
        self._event_switches = {}
        self._perf_events = {}
        # 先不调用 _init_ui，让父类调用
        super().__init__(master, on_change_callback, **kwargs)

    def _init_ui(self) -> None:
        """初始化界面."""
        # 定义所有性能监控事件，按类别分组
        self._perf_events = {
            '缓存监控': {
                'cmt': 'L3 缓存使用量',
                'mbmt': '总系统带宽',
                'mbml': '内存控制器带宽',
            },
            'CPU 事件': {
                'cpu_cycles': 'CPU 周期计数',
                'instructions': '指令计数',
                'cache_references': '缓存命中计数',
                'cache_misses': '缓存未命中计数',
                'bus_cycles': '总线周期计数',
                'stalled_cycles_frontend': '前端停顿周期',
                'stalled_cycles_backend': '后端停顿周期',
                'ref_cpu_cycles': '参考 CPU 周期',
                'cpu_clock': 'CPU 时钟时间',
                'task_clock': '任务时钟时间',
            },
            '分支事件': {
                'branch_instructions': '分支指令计数',
                'branch_misses': '分支未命中计数',
            },
            '其他事件': {
                'page_faults': '缺页异常计数',
                'context_switches': '上下文切换计数',
                'cpu_migrations': 'CPU 迁移计数',
                'page_faults_min': '次要缺页异常',
                'page_faults_maj': '主要缺页异常',
                'alignment_faults': '对齐异常计数',
                'emulation_faults': '仿真异常计数',
            },
        }

        # 说明信息
        info_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        info_frame.pack(fill='x', padx=10, pady=5)
        info_label = ctk.CTkLabel(
            info_frame,
            text='提示：勾选事件启用，选择 enabled 值；取消勾选则不生成该事件的 XML',
            font=CTK_FONT_SMALL,
            text_color='#888888',
        )
        info_label.pack(padx=10, pady=5, anchor='w')

        # 为每个类别创建一行
        for category, events in self._perf_events.items():
            self._create_category_row(category, events)

    def _create_category_row(self, category: str, events: dict[str, str]) -> None:
        """创建类别行.

        Args:
            category: 类别名称
            events: 事件字典 {event_name: event_desc}
        """
        # 类别框架
        category_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        category_frame.pack(fill='x', padx=10, pady=5, anchor='w')

        # 类别标题
        title_label = ctk.CTkLabel(
            category_frame,
            text=f'{category}:',
            font=CTK_FONT_BOLD,
            text_color='#64b5f6',
            width=100,
            anchor='w',
        )
        title_label.pack(side='left', padx=5, pady=5)

        # 创建事件容器
        events_container = ctk.CTkFrame(category_frame, fg_color='transparent')
        events_container.pack(side='left', padx=5, pady=5)

        # 创建事件切换开关
        for event_name, event_desc in events.items():
            switch = EventToggleSwitch(
                events_container,
                event_name=event_name,
                event_desc=event_desc,
                on_change_callback=self._on_event_change,
            )
            switch.pack(side='left', padx=2, pady=2)
            self._event_switches[event_name] = (switch, event_desc)

    def _on_event_change(self, event_name: str, state: tuple[bool, str]) -> None:
        """事件状态改变时的回调.

        Args:
            event_name: 事件名称
            state: (enabled, enabled_value) 元组
        """
        self._trigger_change()

    def _trigger_change(self) -> None:
        """触发配置改变回调."""
        if self.on_change_callback:
            self.on_change_callback()

    def get_config(self) -> dict:
        """获取配置数据.

        Returns:
            配置字典，格式为:
            {
                'enabled': True/False,
                'events': {event_name: enabled_value, ...}
            }
        """
        events = {}
        has_enabled = False

        for event_name, (switch, _) in self._event_switches.items():
            enabled, enabled_value = switch.get_state()
            if enabled:
                events[event_name] = enabled_value
                has_enabled = True

        if has_enabled:
            return {'enabled': True, 'events': events}
        return {'enabled': False, 'events': {}}

    def to_xml(self) -> dict:
        """生成 XML 配置字典."""
        config = self.get_config()
        return {'performance_monitoring': config}

    def load_config(self, config: dict) -> None:
        """加载配置数据.

        Args:
            config: 配置字典
        """
        if not config:
            # 重置所有开关
            for switch, _ in self._event_switches.values():
                switch.set_state(False, 'yes')
            return

        perf_config = config.get('performance_monitoring', config)
        if not isinstance(perf_config, dict):
            return

        if perf_config.get('enabled') is False:
            # 禁用所有
            for switch, _ in self._event_switches.values():
                switch.set_state(False, 'yes')
            return

        events = perf_config.get('events', {})
        for event_name, (switch, _) in self._event_switches.items():
            enabled_value = events.get(event_name, 'yes')
            enabled = event_name in events
            switch.set_state(enabled, enabled_value)
