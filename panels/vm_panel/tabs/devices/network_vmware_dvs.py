"""VMWare分布式交换机模块 - VMWare分布式交换机配置"""

import customtkinter as ctk

from components.base_tab import BaseConfigTab
from utils.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class VMwareDVSTab(BaseConfigTab):
    """VMWare分布式交换机配置"""

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
            frame, text='VMWare Distributed Switch', font=CTK_FONT_BOLD, text_color='#4caf50'
        ).grid(row=0, column=0, columnspan=4, padx=10, pady=5, sticky='w')

        # Switch Name
        ctk.CTkLabel(frame, text='Switch Name:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.switch_name = ctk.CTkEntry(
            frame, placeholder_text='dvSwitch0', width=150, font=CTK_FONT_SMALL
        )
        self.switch_name.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.switch_name.bind('<KeyRelease>', lambda e: self._trigger_change())

        # Port Group
        ctk.CTkLabel(frame, text='Port Group:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.port_group = ctk.CTkEntry(
            frame, placeholder_text='VM Network', width=150, font=CTK_FONT_SMALL
        )
        self.port_group.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.port_group.bind('<KeyRelease>', lambda e: self._trigger_change())

    def get_config(self) -> dict:
        """获取配置"""
        return {
            'type': 'network',
            'source': 'vmware',
            'switch_name': self.switch_name.get().strip(),
            'port_group': self.port_group.get().strip(),
        }
