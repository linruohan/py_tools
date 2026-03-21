"""网络组队模块 - virtio/hostdev NIC配对组队配置"""

import customtkinter as ctk

from components.base_tab import BaseConfigTab
from utils.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class NetworkTeamingTab(BaseConfigTab):
    """virtio/hostdev NIC配对组队配置"""

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
            frame,
            text='Teaming a virtio/hostdev NIC pair',
            font=CTK_FONT_BOLD,
            text_color='#ff9800',
        ).grid(row=0, column=0, columnspan=4, padx=10, pady=5, sticky='w')

        # Team Name
        ctk.CTkLabel(frame, text='Team Name:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.team_name = ctk.CTkEntry(
            frame, placeholder_text='team0', width=150, font=CTK_FONT_SMALL
        )
        self.team_name.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.team_name.bind('<KeyRelease>', lambda e: self._trigger_change())

        # Mode
        ctk.CTkLabel(frame, text='Mode:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.team_mode = ctk.CTkOptionMenu(
            frame,
            values=['active-backup', 'round-robin', 'broadcast', 'loadbalance'],
            width=150,
            font=CTK_FONT_SMALL,
            command=self._trigger_change,
        )
        self.team_mode.set('active-backup')
        self.team_mode.grid(row=2, column=1, padx=5, pady=5, sticky='w')

    def get_config(self) -> dict:
        """获取配置"""
        return {
            'type': 'network',
            'source': 'team',
            'team_name': self.team_name.get().strip() or 'team0',
            'mode': self.team_mode.get(),
        }
