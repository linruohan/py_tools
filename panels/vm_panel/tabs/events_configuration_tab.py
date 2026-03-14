"""事件配置 Tab - 生命周期事件配置."""

import customtkinter as ctk

from utils.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class EventsConfigurationTab(ctk.CTkFrame):
    """事件配置 Tab."""

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

        ctk.CTkLabel(
            left_frame, text='生命周期事件', font=CTK_FONT_BOLD, text_color='#64b5f6'
        ).grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w')

        ctk.CTkLabel(left_frame, text='关机时:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.on_poweroff = ctk.CTkOptionMenu(
            left_frame,
            values=['destroy', 'restart', 'preserve', 'rename-restart'],
            width=140,
            font=CTK_FONT_SMALL,
        )
        self.on_poweroff.set('destroy')
        self.on_poweroff.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.on_poweroff.configure(command=self._trigger_change)

        ctk.CTkLabel(left_frame, text='重启时:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.on_reboot = ctk.CTkOptionMenu(
            left_frame,
            values=['destroy', 'restart', 'preserve', 'rename-restart'],
            width=140,
            font=CTK_FONT_SMALL,
        )
        self.on_reboot.set('restart')
        self.on_reboot.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.on_reboot.configure(command=self._trigger_change)

        ctk.CTkLabel(left_frame, text='崩溃时:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=3, column=0, padx=10, pady=5, sticky='w'
        )
        self.on_crash = ctk.CTkOptionMenu(
            left_frame,
            values=[
                'destroy',
                'restart',
                'preserve',
                'rename-restart',
                'coredump-destroy',
                'coredump-restart',
            ],
            width=140,
            font=CTK_FONT_SMALL,
        )
        self.on_crash.set('destroy')
        self.on_crash.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        self.on_crash.configure(command=self._trigger_change)

        right_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        right_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        right_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(right_frame, text='锁失败事件', font=CTK_FONT_BOLD, text_color='#ff9800').grid(
            row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
        )

        ctk.CTkLabel(right_frame, text='锁失败时:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.on_lockfailure = ctk.CTkOptionMenu(
            right_frame,
            values=['poweroff', 'restart', 'pause', 'ignore'],
            width=100,
            font=CTK_FONT_SMALL,
        )
        self.on_lockfailure.set('poweroff')
        self.on_lockfailure.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.on_lockfailure.configure(command=self._trigger_change)

        info_label = ctk.CTkLabel(
            right_frame,
            text='说明:\n'
            'destroy: 终止并释放资源\n'
            'restart: 重启虚拟机\n'
            'preserve: 保留资源供分析\n'
            'coredump: 生成核心转储',
            font=CTK_FONT_SMALL,
            text_color='#888888',
            justify='left',
        )
        info_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky='w')

    def _trigger_change(self, *args):
        """触发变化回调."""
        if self.on_change_callback:
            self.on_change_callback()

    def get_config(self) -> dict:
        """获取配置数据."""
        return {
            'on_poweroff': self.on_poweroff.get(),
            'on_reboot': self.on_reboot.get(),
            'on_crash': self.on_crash.get(),
            'on_lockfailure': self.on_lockfailure.get(),
        }

    def to_xml(self) -> dict:
        """生成XML配置字典."""
        return {'events_configuration': self.get_config()}
