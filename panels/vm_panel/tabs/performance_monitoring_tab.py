"""性能监控事件配置 Tab - Performance Monitoring Events."""

import customtkinter as ctk

from ..styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_SMALL


class PerformanceMonitoringTab(ctk.CTkFrame):
    """性能监控事件配置 Tab."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent')
        self.on_change_callback = on_change_callback

        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        left_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        left_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

        ctk.CTkLabel(left_frame, text='缓存监控', font=CTK_FONT_BOLD, text_color='#64b5f6').grid(
            row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
        )

        self.cmt = ctk.CTkCheckBox(
            left_frame, text='cmt (L3缓存使用)', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.cmt.grid(row=1, column=0, padx=10, pady=3, sticky='w')

        self.mbmt = ctk.CTkCheckBox(
            left_frame, text='mbmt (总带宽)', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.mbmt.grid(row=2, column=0, padx=10, pady=3, sticky='w')

        self.mbml = ctk.CTkCheckBox(
            left_frame, text='mbml (内存流量)', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.mbml.grid(row=3, column=0, padx=10, pady=3, sticky='w')

        ctk.CTkLabel(left_frame, text='CPU 事件', font=CTK_FONT_BOLD, text_color='#4caf50').grid(
            row=4, column=0, columnspan=2, padx=10, pady=10, sticky='w'
        )

        self.cpu_cycles = ctk.CTkCheckBox(
            left_frame, text='cpu_cycles', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.cpu_cycles.grid(row=5, column=0, padx=10, pady=3, sticky='w')

        self.instructions = ctk.CTkCheckBox(
            left_frame, text='instructions', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.instructions.grid(row=6, column=0, padx=10, pady=3, sticky='w')

        self.cache_references = ctk.CTkCheckBox(
            left_frame, text='cache_references', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.cache_references.grid(row=7, column=0, padx=10, pady=3, sticky='w')

        self.cache_misses = ctk.CTkCheckBox(
            left_frame, text='cache_misses', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.cache_misses.grid(row=8, column=0, padx=10, pady=3, sticky='w')

        right_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        right_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)

        ctk.CTkLabel(right_frame, text='分支事件', font=CTK_FONT_BOLD, text_color='#ff9800').grid(
            row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
        )

        self.branch_instructions = ctk.CTkCheckBox(
            right_frame,
            text='branch_instructions',
            font=CTK_FONT_SMALL,
            command=self._trigger_change,
        )
        self.branch_instructions.grid(row=1, column=0, padx=10, pady=3, sticky='w')

        self.branch_misses = ctk.CTkCheckBox(
            right_frame, text='branch_misses', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.branch_misses.grid(row=2, column=0, padx=10, pady=3, sticky='w')

        ctk.CTkLabel(right_frame, text='其他事件', font=CTK_FONT_BOLD, text_color='#9c27b0').grid(
            row=3, column=0, columnspan=2, padx=10, pady=10, sticky='w'
        )

        self.page_faults = ctk.CTkCheckBox(
            right_frame, text='page_faults', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.page_faults.grid(row=4, column=0, padx=10, pady=3, sticky='w')

        self.context_switches = ctk.CTkCheckBox(
            right_frame, text='context_switches', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.context_switches.grid(row=5, column=0, padx=10, pady=3, sticky='w')

        self.cpu_migrations = ctk.CTkCheckBox(
            right_frame, text='cpu_migrations', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.cpu_migrations.grid(row=6, column=0, padx=10, pady=3, sticky='w')

        self.alignment_faults = ctk.CTkCheckBox(
            right_frame, text='alignment_faults', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.alignment_faults.grid(row=7, column=0, padx=10, pady=3, sticky='w')

    def _trigger_change(self):
        """触发变化回调."""
        if self.on_change_callback:
            self.on_change_callback()

    def get_config(self) -> dict:
        """获取配置数据."""
        return {
            'cmt': self.cmt.get(),
            'mbmt': self.mbmt.get(),
            'mbml': self.mbml.get(),
            'cpu_cycles': self.cpu_cycles.get(),
            'instructions': self.instructions.get(),
            'cache_references': self.cache_references.get(),
            'cache_misses': self.cache_misses.get(),
            'branch_instructions': self.branch_instructions.get(),
            'branch_misses': self.branch_misses.get(),
            'page_faults': self.page_faults.get(),
            'context_switches': self.context_switches.get(),
            'cpu_migrations': self.cpu_migrations.get(),
            'alignment_faults': self.alignment_faults.get(),
        }

    def to_xml(self) -> dict:
        """生成XML配置字典."""
        return {'performance_monitoring': self.get_config()}
