"""控制台模块 - 控制台配置"""

import customtkinter as ctk

from components.base_tab import BaseConfigTab
from utils.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class ConsoleTab(BaseConfigTab):
    """控制台配置"""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, on_change_callback, **kwargs)
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面"""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(frame, text='Console', font=CTK_FONT_BOLD, text_color='#ff9800').grid(
            row=0, column=0, columnspan=4, padx=10, pady=5, sticky='w'
        )

        # Console Type
        ctk.CTkLabel(frame, text='Type:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.console_type = ctk.CTkOptionMenu(
            frame,
            values=['pty', 'tty', 'file', 'null', 'tcp', 'udp', 'unix'],
            width=100,
            font=CTK_FONT_SMALL,
            command=self._trigger_change,
        )
        self.console_type.set('pty')
        self.console_type.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        # Target
        ctk.CTkLabel(frame, text='Target:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.target = ctk.CTkEntry(
            frame, placeholder_text='/dev/console', width=200, font=CTK_FONT_SMALL
        )
        self.target.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.target.bind('<KeyRelease>', lambda e: self._trigger_change())

    def get_config(self) -> dict:
        """获取配置"""
        return {
            'type': 'console',
            'console_type': self.console_type.get(),
            'target': self.target.get().strip(),
        }
