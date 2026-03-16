"""驱动域网络后端模块 - 在驱动域中设置网络后端配置"""

import customtkinter as ctk

from components.base_tab import BaseConfigTab
from utils.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class NetworkDriverDomainTab(BaseConfigTab):
    """在驱动域中设置网络后端配置"""

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
            frame, text='Setting up a network backend in a driver domain', font=CTK_FONT_BOLD, text_color='#4caf50'
        ).grid(row=0, column=0, columnspan=4, padx=10, pady=5, sticky='w')

        # Driver Domain Name
        ctk.CTkLabel(frame, text='Driver Domain:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.driver_domain = ctk.CTkEntry(
            frame, placeholder_text='driver-dom', width=150, font=CTK_FONT_SMALL
        )
        self.driver_domain.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.driver_domain.bind('<KeyRelease>', lambda e: self._trigger_change())

        # Interface Name
        ctk.CTkLabel(frame, text='Interface:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.interface = ctk.CTkEntry(
            frame, placeholder_text='vnet0', width=150, font=CTK_FONT_SMALL
        )
        self.interface.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.interface.bind('<KeyRelease>', lambda e: self._trigger_change())

    def get_config(self) -> dict:
        """获取配置"""
        return {
            'type': 'network',
            'driver_domain': self.driver_domain.get().strip(),
            'interface': self.interface.get().strip()
        }
