"""时钟/看门狗 Tab."""

import customtkinter as ctk

from utils.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class ClockTab(ctk.CTkFrame):
    """时钟/看门狗 Tab."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent')
        self.on_change_callback = on_change_callback

        # 控件引用
        self.watchdog_model = None
        self.watchdog_action = None
        self.rtc_clock = None
        self.kvm_clock_check = None

        # 初始化 UI
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面."""
        # 配置 grid 权重
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)

        # 看门狗
        wd_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=8)
        wd_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=10)
        wd_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(wd_frame, text='看门狗', font=CTK_FONT_BOLD, text_color='#ef5350').grid(
            row=0, column=0, columnspan=3, padx=10, pady=5, sticky='w'
        )

        # 看门狗模型
        ctk.CTkLabel(wd_frame, text='模型:', font=CTK_FONT_MAIN, width=60, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.watchdog_model = ctk.CTkOptionMenu(
            wd_frame,
            values=['none', 'i6300esb', 'ib700', 'diag288'],
            width=120,
            font=CTK_FONT_SMALL,
        )
        self.watchdog_model.set('none')
        self.watchdog_model.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        # 看门狗动作
        ctk.CTkLabel(wd_frame, text='动作:', font=CTK_FONT_MAIN, width=50, anchor='w').grid(
            row=1, column=2, padx=10, pady=5, sticky='w'
        )
        self.watchdog_action = ctk.CTkOptionMenu(
            wd_frame,
            values=['reset', 'shutdown', 'poweroff', 'inject-nmi', 'none'],
            width=120,
            font=CTK_FONT_SMALL,
        )
        self.watchdog_action.set('reset')
        self.watchdog_action.grid(row=1, column=3, padx=5, pady=5, sticky='w')

        # 时间同步
        time_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=8)
        time_frame.grid(row=1, column=0, sticky='ew', padx=10, pady=10)
        time_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(time_frame, text='时间同步', font=CTK_FONT_BOLD, text_color='#4db6ac').grid(
            row=0, column=0, columnspan=3, padx=10, pady=5, sticky='w'
        )

        # RTC 时钟
        ctk.CTkLabel(time_frame, text='RTC:', font=CTK_FONT_MAIN, width=50, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.rtc_clock = ctk.CTkOptionMenu(
            time_frame, values=['utc', 'localtime'], width=100, font=CTK_FONT_SMALL
        )
        self.rtc_clock.set('utc')
        self.rtc_clock.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        # 启用 KVM 时钟
        self.kvm_clock_check = ctk.CTkCheckBox(
            time_frame, text='启用 KVM 时钟', font=CTK_FONT_SMALL
        )
        self.kvm_clock_check.grid(row=1, column=2, padx=10, pady=5, sticky='w')
        self.kvm_clock_check.select()

    def _trigger_change(self, *args):
        """触发变化回调."""
        if self.on_change_callback:
            self.on_change_callback()

    def get_watchdog_config(self):
        """获取看门狗配置."""
        if self.watchdog_model.get() != 'none':
            return {
                'model': self.watchdog_model.get(),
                'action': self.watchdog_action.get(),
            }
        return None

    def get_clock_config(self):
        """获取时钟配置."""
        return {
            'rtc': self.rtc_clock.get(),
            'kvm_clock': self.kvm_clock_check.get(),
        }
