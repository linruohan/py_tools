"""网络隔离模块 - 隔离虚拟机网络流量配置"""

import customtkinter as ctk

from components.base_tab import BaseConfigTab
from utils.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class NetworkIsolationTab(BaseConfigTab):
    """隔离虚拟机网络流量配置"""

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

        ctk.CTkLabel(
            frame,
            text="Isolating guests' network traffic from each other",
            font=CTK_FONT_BOLD,
            text_color='#ff9800',
        ).grid(row=0, column=0, columnspan=4, padx=10, pady=5, sticky='w')

        # Isolation Mode
        ctk.CTkLabel(frame, text='Isolation Mode:', font=CTK_FONT_MAIN, width=120, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.isolation_mode = ctk.CTkOptionMenu(
            frame,
            values=['none', 'vlan', 'private', 'isolated'],
            width=150,
            font=CTK_FONT_SMALL,
            command=self._trigger_change,
        )
        self.isolation_mode.set('none')
        self.isolation_mode.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        # Isolation Tag
        ctk.CTkLabel(frame, text='Isolation Tag:', font=CTK_FONT_MAIN, width=120, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.isolation_tag = ctk.CTkEntry(
            frame, placeholder_text='100', width=100, font=CTK_FONT_SMALL
        )
        self.isolation_tag.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.isolation_tag.bind('<KeyRelease>', lambda e: self._trigger_change())

    def get_config(self) -> dict:
        """获取配置"""
        return {
            'type': 'network',
            'isolation_mode': self.isolation_mode.get(),
            'isolation_tag': self.isolation_tag.get().strip(),
        }
