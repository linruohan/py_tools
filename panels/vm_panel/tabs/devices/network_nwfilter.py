"""NWFilter流量过滤模块 - 流量过滤配置"""

import customtkinter as ctk

from components.base_tab import BaseConfigTab
from utils.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class NetworkNWFilterTab(BaseConfigTab):
    """流量过滤配置"""

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
            frame, text='Traffic filtering with NWFilter', font=CTK_FONT_BOLD, text_color='#ff9800'
        ).grid(row=0, column=0, columnspan=4, padx=10, pady=5, sticky='w')

        # Filter Name
        ctk.CTkLabel(frame, text='Filter Name:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.filter_name = ctk.CTkEntry(
            frame, placeholder_text='default', width=150, font=CTK_FONT_SMALL
        )
        self.filter_name.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.filter_name.bind('<KeyRelease>', lambda e: self._trigger_change())

        # Filter Parameters
        ctk.CTkLabel(
            frame, text='Filter Parameters:', font=CTK_FONT_MAIN, width=100, anchor='w'
        ).grid(row=2, column=0, padx=10, pady=5, sticky='w')
        self.filter_params = ctk.CTkTextbox(
            frame, placeholder_text='param1=value1\nparam2=value2', height=100, font=CTK_FONT_SMALL
        )
        self.filter_params.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.filter_params.bind('<KeyRelease>', lambda e: self._trigger_change())

    def get_config(self) -> dict:
        """获取配置"""
        return {
            'type': 'network',
            'filter_name': self.filter_name.get().strip() or 'default',
            'filter_params': self.filter_params.get('1.0', 'end').strip(),
        }
