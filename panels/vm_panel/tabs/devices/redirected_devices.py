"""重定向设备模块 - 重定向设备配置"""

import customtkinter as ctk

from components.base_tab import BaseConfigTab
from utils.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class RedirectedDevicesTab(BaseConfigTab):
    """重定向设备配置"""

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
            frame, text='Redirected devices', font=CTK_FONT_BOLD, text_color='#ff9800'
        ).grid(row=0, column=0, columnspan=4, padx=10, pady=5, sticky='w')

        # 重定向设备类型
        ctk.CTkLabel(frame, text='Device Type:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.device_type = ctk.CTkOptionMenu(
            frame,
            values=['smartcard', 'usb', 'serial'],
            width=100,
            font=CTK_FONT_SMALL,
            command=self._trigger_change
        )
        self.device_type.set('smartcard')
        self.device_type.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        # 重定向方法
        ctk.CTkLabel(frame, text='Redirect Method:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.redirect_method = ctk.CTkOptionMenu(
            frame,
            values=['spice', 'usb-redir', 'tcpserial'],
            width=100,
            font=CTK_FONT_SMALL,
            command=self._trigger_change
        )
        self.redirect_method.set('spice')
        self.redirect_method.grid(row=2, column=1, padx=5, pady=5, sticky='w')

    def get_config(self) -> dict:
        """获取配置"""
        return {
            'type': 'redirected',
            'device_type': self.device_type.get(),
            'redirect_method': self.redirect_method.get()
        }
