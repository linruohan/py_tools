"""通用以太网连接模块 - 通用以太网连接配置"""

import customtkinter as ctk

from components.base_tab import BaseConfigTab
from utils.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class GenericEthernetTab(BaseConfigTab):
    """通用以太网连接配置"""

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
            frame, text='Generic ethernet connection', font=CTK_FONT_BOLD, text_color='#2196f3'
        ).grid(row=0, column=0, columnspan=4, padx=10, pady=5, sticky='w')

        # MAC Address
        ctk.CTkLabel(frame, text='MAC Address:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.mac_address = ctk.CTkEntry(
            frame, placeholder_text='52:54:00:12:34:56', width=150, font=CTK_FONT_SMALL
        )
        self.mac_address.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.mac_address.bind('<KeyRelease>', lambda e: self._trigger_change())

        # MTU
        ctk.CTkLabel(frame, text='MTU:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.mtu = ctk.CTkEntry(frame, placeholder_text='1500', width=100, font=CTK_FONT_SMALL)
        self.mtu.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.mtu.bind('<KeyRelease>', lambda e: self._trigger_change())

    def get_config(self) -> dict:
        """获取配置"""
        return {
            'type': 'network',
            'source': 'ethernet',
            'mac': self.mac_address.get().strip(),
            'mtu': self.mtu.get().strip() or '1500',
        }
