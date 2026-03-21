"""TCP隧道模块 - TCP隧道配置"""

import customtkinter as ctk

from components.base_tab import BaseConfigTab
from utils.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class TCPTunnelTab(BaseConfigTab):
    """TCP隧道配置"""

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

        ctk.CTkLabel(frame, text='TCP tunnel', font=CTK_FONT_BOLD, text_color='#ff5722').grid(
            row=0, column=0, columnspan=4, padx=10, pady=5, sticky='w'
        )

        # Host
        ctk.CTkLabel(frame, text='Host:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.host = ctk.CTkEntry(
            frame, placeholder_text='127.0.0.1', width=150, font=CTK_FONT_SMALL
        )
        self.host.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.host.bind('<KeyRelease>', lambda e: self._trigger_change())

        # Port
        ctk.CTkLabel(frame, text='Port:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.port = ctk.CTkEntry(frame, placeholder_text='1234', width=100, font=CTK_FONT_SMALL)
        self.port.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.port.bind('<KeyRelease>', lambda e: self._trigger_change())

    def get_config(self) -> dict:
        """获取配置"""
        return {
            'type': 'network',
            'source': 'tcp',
            'host': self.host.get().strip(),
            'port': self.port.get().strip() or '1234',
        }
