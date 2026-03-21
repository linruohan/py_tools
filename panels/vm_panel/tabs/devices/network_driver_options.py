"""NIC驱动选项模块 - NIC驱动特定选项配置"""

import customtkinter as ctk

from components.base_tab import BaseConfigTab
from utils.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class NICDriverOptionsTab(BaseConfigTab):
    """NIC驱动特定选项配置"""

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
            text='Setting NIC driver-specific options',
            font=CTK_FONT_BOLD,
            text_color='#ff9800',
        ).grid(row=0, column=0, columnspan=4, padx=10, pady=5, sticky='w')

        # Driver Name
        ctk.CTkLabel(frame, text='Driver Name:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.driver_name = ctk.CTkEntry(
            frame, placeholder_text='virtio-net', width=150, font=CTK_FONT_SMALL
        )
        self.driver_name.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.driver_name.bind('<KeyRelease>', lambda e: self._trigger_change())

        # Driver Options
        ctk.CTkLabel(frame, text='Driver Options:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.driver_options = ctk.CTkTextbox(
            frame, placeholder_text='tx_queue_size=1024', height=100, font=CTK_FONT_SMALL
        )
        self.driver_options.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.driver_options.bind('<KeyRelease>', lambda e: self._trigger_change())

    def get_config(self) -> dict:
        """获取配置"""
        return {
            'type': 'network',
            'driver_name': self.driver_name.get().strip(),
            'driver_options': self.driver_options.get('1.0', 'end').strip(),
        }
