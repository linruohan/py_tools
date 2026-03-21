"""目标元素覆盖模块 - 覆盖网络接口目标元素配置"""

import customtkinter as ctk

from components.base_tab import BaseConfigTab
from utils.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class NetworkTargetOverrideTab(BaseConfigTab):
    """覆盖网络接口目标元素配置"""

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
            frame, text='Overriding the target element', font=CTK_FONT_BOLD, text_color='#ff5722'
        ).grid(row=0, column=0, columnspan=4, padx=10, pady=5, sticky='w')

        # Target Device
        ctk.CTkLabel(frame, text='Target Device:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.target_dev = ctk.CTkEntry(
            frame, placeholder_text='eth0', width=100, font=CTK_FONT_SMALL
        )
        self.target_dev.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.target_dev.bind('<KeyRelease>', lambda e: self._trigger_change())

        # Target Bus
        ctk.CTkLabel(frame, text='Target Bus:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.target_bus = ctk.CTkOptionMenu(
            frame,
            values=['virtio', 'e1000', 'pcnet', 'rtl8139'],
            width=100,
            font=CTK_FONT_SMALL,
            command=self._trigger_change,
        )
        self.target_bus.set('virtio')
        self.target_bus.grid(row=2, column=1, padx=5, pady=5, sticky='w')

    def get_config(self) -> dict:
        """获取配置"""
        return {
            'type': 'network',
            'target_dev': self.target_dev.get().strip() or 'eth0',
            'target_bus': self.target_bus.get(),
        }
