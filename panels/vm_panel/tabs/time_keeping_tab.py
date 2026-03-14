"""时间同步配置 Tab - Clock 配置."""

import customtkinter as ctk

from utils.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class TimeKeepingTab(ctk.CTkFrame):
    """时间同步配置 Tab."""

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
        left_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(left_frame, text='时钟配置', font=CTK_FONT_BOLD, text_color='#64b5f6').grid(
            row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
        )

        ctk.CTkLabel(left_frame, text='偏移模式:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.offset = ctk.CTkOptionMenu(
            left_frame,
            values=['utc', 'localtime', 'timezone', 'variable', 'absolute'],
            width=120,
            font=CTK_FONT_SMALL,
        )
        self.offset.set('utc')
        self.offset.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.offset.configure(command=self._trigger_change)

        ctk.CTkLabel(left_frame, text='时区:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.timezone = ctk.CTkEntry(left_frame, placeholder_text='Asia/Shanghai', width=150)
        self.timezone.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.timezone.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(left_frame, text='调整值:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=3, column=0, padx=10, pady=5, sticky='w'
        )
        self.adjustment = ctk.CTkEntry(left_frame, placeholder_text='秒数', width=100)
        self.adjustment.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        self.adjustment.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(left_frame, text='基准:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=4, column=0, padx=10, pady=5, sticky='w'
        )
        self.basis = ctk.CTkOptionMenu(
            left_frame,
            values=['utc', 'localtime'],
            width=100,
            font=CTK_FONT_SMALL,
        )
        self.basis.set('utc')
        self.basis.grid(row=4, column=1, padx=5, pady=5, sticky='w')
        self.basis.configure(command=self._trigger_change)

        right_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        right_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        right_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(right_frame, text='定时器配置', font=CTK_FONT_BOLD, text_color='#4caf50').grid(
            row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
        )

        ctk.CTkLabel(right_frame, text='RTC:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.rtc_tickpolicy = ctk.CTkOptionMenu(
            right_frame,
            values=['catchup', 'delay', 'merge', 'discard'],
            width=100,
            font=CTK_FONT_SMALL,
        )
        self.rtc_tickpolicy.set('catchup')
        self.rtc_tickpolicy.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.rtc_tickpolicy.configure(command=self._trigger_change)

        ctk.CTkLabel(right_frame, text='PIT:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.pit_tickpolicy = ctk.CTkOptionMenu(
            right_frame,
            values=['delay', 'catchup', 'merge', 'discard'],
            width=100,
            font=CTK_FONT_SMALL,
        )
        self.pit_tickpolicy.set('delay')
        self.pit_tickpolicy.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.pit_tickpolicy.configure(command=self._trigger_change)

        ctk.CTkLabel(right_frame, text='TSC:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=3, column=0, padx=10, pady=5, sticky='w'
        )
        self.tsc_mode = ctk.CTkOptionMenu(
            right_frame,
            values=['auto', 'native', 'emulate', 'paravirt', 'smpsafe'],
            width=100,
            font=CTK_FONT_SMALL,
        )
        self.tsc_mode.set('auto')
        self.tsc_mode.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        self.tsc_mode.configure(command=self._trigger_change)

        ctk.CTkLabel(right_frame, text='HPET:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=4, column=0, padx=10, pady=5, sticky='w'
        )
        self.hpet_present = ctk.CTkOptionMenu(
            right_frame,
            values=['yes', 'no'],
            width=80,
            font=CTK_FONT_SMALL,
        )
        self.hpet_present.set('yes')
        self.hpet_present.grid(row=4, column=1, padx=5, pady=5, sticky='w')
        self.hpet_present.configure(command=self._trigger_change)

        ctk.CTkLabel(right_frame, text='kvmclock:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=5, column=0, padx=10, pady=5, sticky='w'
        )
        self.kvmclock_present = ctk.CTkOptionMenu(
            right_frame,
            values=['yes', 'no'],
            width=80,
            font=CTK_FONT_SMALL,
        )
        self.kvmclock_present.set('yes')
        self.kvmclock_present.grid(row=5, column=1, padx=5, pady=5, sticky='w')
        self.kvmclock_present.configure(command=self._trigger_change)

    def _trigger_change(self, *args):
        """触发变化回调."""
        if self.on_change_callback:
            self.on_change_callback()

    def get_config(self) -> dict:
        """获取配置数据."""
        return {
            'offset': self.offset.get(),
            'timezone': self.timezone.get().strip(),
            'adjustment': self.adjustment.get().strip(),
            'basis': self.basis.get(),
            'timers': {
                'rtc_tickpolicy': self.rtc_tickpolicy.get(),
                'pit_tickpolicy': self.pit_tickpolicy.get(),
                'tsc_mode': self.tsc_mode.get(),
                'hpet_present': self.hpet_present.get(),
                'kvmclock_present': self.kvmclock_present.get(),
            },
        }

    def to_xml(self) -> dict:
        """生成XML配置字典."""
        return {'time_keeping': self.get_config()}
