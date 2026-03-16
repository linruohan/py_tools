"""启动顺序指定模块 - 网络接口启动顺序配置"""

import customtkinter as ctk

from components.base_tab import BaseConfigTab
from utils.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class NetworkBootOrderTab(BaseConfigTab):
    """网络接口启动顺序配置"""

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
            frame, text='Specifying boot order', font=CTK_FONT_BOLD, text_color='#795548'
        ).grid(row=0, column=0, columnspan=4, padx=10, pady=5, sticky='w')

        # Boot Order
        ctk.CTkLabel(frame, text='Boot Order:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.boot_order = ctk.CTkEntry(
            frame, placeholder_text='1', width=100, font=CTK_FONT_SMALL
        )
        self.boot_order.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.boot_order.bind('<KeyRelease>', lambda e: self._trigger_change())

        # Boot Protocol
        ctk.CTkLabel(frame, text='Boot Protocol:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.boot_protocol = ctk.CTkOptionMenu(
            frame,
            values=['none', 'pXE', 'ipv4', 'ipv6'],
            width=100,
            font=CTK_FONT_SMALL,
            command=self._trigger_change
        )
        self.boot_protocol.set('none')
        self.boot_protocol.grid(row=2, column=1, padx=5, pady=5, sticky='w')

    def get_config(self) -> dict:
        """获取配置"""
        return {
            'type': 'network',
            'boot_order': self.boot_order.get().strip() or '1',
            'boot_protocol': self.boot_protocol.get()
        }
