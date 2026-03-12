"""CPU 优化配置 Tab - CPU Tuning."""

import customtkinter as ctk

from ..styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class CPUTuningTab(ctk.CTkFrame):
    """CPU 优化配置 Tab."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent')
        self.on_change_callback = on_change_callback

        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        left_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        left_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        left_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(left_frame, text='CPU 亲和性', font=CTK_FONT_BOLD, text_color='#64b5f6').grid(
            row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
        )

        ctk.CTkLabel(left_frame, text='vCPU Pin:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.vcpupin = ctk.CTkEntry(left_frame, placeholder_text='vcpu=0 cpuset=1-4', width=150)
        self.vcpupin.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.vcpupin.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(
            left_frame, text='模拟器 Pin:', font=CTK_FONT_MAIN, width=100, anchor='w'
        ).grid(row=2, column=0, padx=10, pady=5, sticky='w')
        self.emulatorpin = ctk.CTkEntry(left_frame, placeholder_text='cpuset=1-3', width=150)
        self.emulatorpin.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.emulatorpin.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(
            left_frame, text='IOThread Pin:', font=CTK_FONT_MAIN, width=100, anchor='w'
        ).grid(row=3, column=0, padx=10, pady=5, sticky='w')
        self.iothreadpin = ctk.CTkEntry(
            left_frame, placeholder_text='iothread=1 cpuset=5-6', width=150
        )
        self.iothreadpin.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        self.iothreadpin.bind('<KeyRelease>', lambda e: self._trigger_change())

        mid_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        mid_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        mid_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(mid_frame, text='CPU 带宽', font=CTK_FONT_BOLD, text_color='#4caf50').grid(
            row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
        )

        ctk.CTkLabel(mid_frame, text='份额:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.shares = ctk.CTkEntry(mid_frame, placeholder_text='1024', width=80)
        self.shares.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.shares.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(mid_frame, text='周期 (μs):', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.period = ctk.CTkEntry(mid_frame, placeholder_text='1000000', width=80)
        self.period.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.period.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(mid_frame, text='配额 (μs):', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=3, column=0, padx=10, pady=5, sticky='w'
        )
        self.quota = ctk.CTkEntry(mid_frame, placeholder_text='-1', width=80)
        self.quota.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        self.quota.bind('<KeyRelease>', lambda e: self._trigger_change())

        right_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        right_frame.grid(row=0, column=2, sticky='nsew', padx=5, pady=5)
        right_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(right_frame, text='调度器', font=CTK_FONT_BOLD, text_color='#ff9800').grid(
            row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
        )

        ctk.CTkLabel(right_frame, text='调度器:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.scheduler = ctk.CTkOptionMenu(
            right_frame,
            values=['batch', 'idle', 'fifo', 'rr'],
            width=80,
            font=CTK_FONT_SMALL,
        )
        self.scheduler.set('batch')
        self.scheduler.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.scheduler.configure(command=self._trigger_change)

        ctk.CTkLabel(right_frame, text='优先级:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.priority = ctk.CTkEntry(right_frame, placeholder_text='1-99', width=80)
        self.priority.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.priority.bind('<KeyRelease>', lambda e: self._trigger_change())

    def _trigger_change(self, *args):
        """触发变化回调."""
        if self.on_change_callback:
            self.on_change_callback()

    def get_config(self) -> dict:
        """获取配置数据."""
        return {
            'vcpupin': self.vcpupin.get().strip(),
            'emulatorpin': self.emulatorpin.get().strip(),
            'iothreadpin': self.iothreadpin.get().strip(),
            'shares': self.shares.get().strip(),
            'period': self.period.get().strip(),
            'quota': self.quota.get().strip(),
            'scheduler': self.scheduler.get(),
            'priority': self.priority.get().strip(),
        }

    def to_xml(self) -> dict:
        """生成XML配置字典."""
        return {'cpu_tuning': self.get_config()}
