"""虚拟链路状态模块 - 修改虚拟链路状态配置"""

import customtkinter as ctk

from components.base_tab import BaseConfigTab
from utils.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class NetworkLinkStateTab(BaseConfigTab):
    """修改虚拟链路状态配置"""

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
            frame, text='Modifying virtual link state', font=CTK_FONT_BOLD, text_color='#9c27b0'
        ).grid(row=0, column=0, columnspan=4, padx=10, pady=5, sticky='w')

        # Link State
        ctk.CTkLabel(frame, text='Link State:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.link_state = ctk.CTkOptionMenu(
            frame,
            values=['up', 'down'],
            width=100,
            font=CTK_FONT_SMALL,
            command=self._trigger_change,
        )
        self.link_state.set('up')
        self.link_state.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        # Auto-negotiation
        ctk.CTkLabel(
            frame, text='Auto-negotiation:', font=CTK_FONT_MAIN, width=120, anchor='w'
        ).grid(row=2, column=0, padx=10, pady=5, sticky='w')
        self.auto_negotiate = ctk.CTkCheckBox(
            frame, text='Enable', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.auto_negotiate.grid(row=2, column=1, padx=5, pady=5, sticky='w')

    def get_config(self) -> dict:
        """获取配置"""
        return {
            'type': 'network',
            'link_state': self.link_state.get(),
            'auto_negotiate': self.auto_negotiate.get(),
        }
