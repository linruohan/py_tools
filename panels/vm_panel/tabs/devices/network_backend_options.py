"""网络后端选项模块 - 网络后端特定选项配置"""

import customtkinter as ctk

from components.base_tab import BaseConfigTab
from utils.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class NetworkBackendOptionsTab(BaseConfigTab):
    """网络后端特定选项配置"""

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
            frame, text='Setting network backend-specific options', font=CTK_FONT_BOLD, text_color='#9c27b0'
        ).grid(row=0, column=0, columnspan=4, padx=10, pady=5, sticky='w')

        # Backend Type
        ctk.CTkLabel(frame, text='Backend Type:', font=CTK_FONT_MAIN, width=120, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.backend_type = ctk.CTkOptionMenu(
            frame,
            values=['bridge', 'network', 'user', 'direct'],
            width=150,
            font=CTK_FONT_SMALL,
            command=self._trigger_change
        )
        self.backend_type.set('bridge')
        self.backend_type.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        # Backend Options
        ctk.CTkLabel(frame, text='Backend Options:', font=CTK_FONT_MAIN, width=120, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.backend_options = ctk.CTkTextbox(
            frame, placeholder_text='hello=world', height=100, font=CTK_FONT_SMALL
        )
        self.backend_options.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.backend_options.bind('<KeyRelease>', lambda e: self._trigger_change())

    def get_config(self) -> dict:
        """获取配置"""
        return {
            'type': 'network',
            'backend_type': self.backend_type.get(),
            'backend_options': self.backend_options.get('1.0', 'end').strip()
        }
