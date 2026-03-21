"""域日志文件模块 - 域日志文件配置"""

import customtkinter as ctk

from components.base_tab import BaseConfigTab
from utils.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class DomainLogfileTab(BaseConfigTab):
    """域日志文件配置"""

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

        ctk.CTkLabel(frame, text='Domain logfile', font=CTK_FONT_BOLD, text_color='#ff5722').grid(
            row=0, column=0, columnspan=4, padx=10, pady=5, sticky='w'
        )

        # Log Path
        ctk.CTkLabel(frame, text='Log Path:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.log_path = ctk.CTkEntry(
            frame,
            placeholder_text='/var/log/libvirt/qemu/domain.log',
            width=200,
            font=CTK_FONT_SMALL,
        )
        self.log_path.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.log_path.bind('<KeyRelease>', lambda e: self._trigger_change())

        # Log Level
        ctk.CTkLabel(frame, text='Log Level:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.log_level = ctk.CTkOptionMenu(
            frame,
            values=['debug', 'info', 'warning', 'error'],
            width=100,
            font=CTK_FONT_SMALL,
            command=self._trigger_change,
        )
        self.log_level.set('info')
        self.log_level.grid(row=2, column=1, padx=5, pady=5, sticky='w')

    def get_config(self) -> dict:
        """获取配置"""
        return {
            'type': 'logfile',
            'path': self.log_path.get().strip(),
            'level': self.log_level.get(),
        }
