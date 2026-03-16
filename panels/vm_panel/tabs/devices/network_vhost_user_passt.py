"""vhost-user连接与passt后端模块 - vhost-user连接与passt后端配置"""

import customtkinter as ctk

from components.base_tab import BaseConfigTab
from utils.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class NetworkVhostUserPasstTab(BaseConfigTab):
    """vhost-user连接与passt后端配置"""

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
            frame, text='vhost-user connection with passt backend', font=CTK_FONT_BOLD, text_color='#2196f3'
        ).grid(row=0, column=0, columnspan=4, padx=10, pady=5, sticky='w')

        # Socket Path
        ctk.CTkLabel(frame, text='Socket Path:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.socket_path = ctk.CTkEntry(
            frame, placeholder_text='/path/to/vhost-user-passt.sock', width=200, font=CTK_FONT_SMALL
        )
        self.socket_path.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.socket_path.bind('<KeyRelease>', lambda e: self._trigger_change())

        # Passt Arguments
        ctk.CTkLabel(frame, text='Passt Args:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.passt_args = ctk.CTkEntry(
            frame, placeholder_text='--mtu=1500', width=200, font=CTK_FONT_SMALL
        )
        self.passt_args.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.passt_args.bind('<KeyRelease>', lambda e: self._trigger_change())

    def get_config(self) -> dict:
        """获取配置"""
        return {
            'type': 'network',
            'source': 'vhostuser',
            'socket_path': self.socket_path.get().strip(),
            'passt_args': self.passt_args.get().strip()
        }
