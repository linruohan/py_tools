"""vhost-user连接模块 - vhost-user连接配置"""

import customtkinter as ctk

from components.base_tab import BaseConfigTab
from utils.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class NetworkVhostUserTab(BaseConfigTab):
    """vhost-user连接配置"""

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
            frame, text='vhost-user connection', font=CTK_FONT_BOLD, text_color='#4caf50'
        ).grid(row=0, column=0, columnspan=4, padx=10, pady=5, sticky='w')

        # Socket Path
        ctk.CTkLabel(frame, text='Socket Path:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.socket_path = ctk.CTkEntry(
            frame, placeholder_text='/path/to/vhost-user.sock', width=200, font=CTK_FONT_SMALL
        )
        self.socket_path.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.socket_path.bind('<KeyRelease>', lambda e: self._trigger_change())

        # Mode
        ctk.CTkLabel(frame, text='Mode:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.mode = ctk.CTkOptionMenu(
            frame,
            values=['client', 'server'],
            width=100,
            font=CTK_FONT_SMALL,
            command=self._trigger_change,
        )
        self.mode.set('client')
        self.mode.grid(row=2, column=1, padx=5, pady=5, sticky='w')

    def get_config(self) -> dict:
        """获取配置"""
        return {
            'type': 'network',
            'source': 'vhostuser',
            'socket_path': self.socket_path.get().strip(),
            'mode': self.mode.get(),
        }
