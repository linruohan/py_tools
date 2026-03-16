"""ROM BIOS配置模块 - 网络接口ROM BIOS配置"""

import customtkinter as ctk

from components.base_tab import BaseConfigTab
from utils.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class NetworkROMBIOSConfigTab(BaseConfigTab):
    """网络接口ROM BIOS配置"""

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
            frame, text='Interface ROM BIOS configuration', font=CTK_FONT_BOLD, text_color='#607d8b'
        ).grid(row=0, column=0, columnspan=4, padx=10, pady=5, sticky='w')

        # ROM Bar
        ctk.CTkLabel(frame, text='ROM Bar:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.rom_bar = ctk.CTkOptionMenu(
            frame,
            values=['on', 'off'],
            width=100,
            font=CTK_FONT_SMALL,
            command=self._trigger_change
        )
        self.rom_bar.set('off')
        self.rom_bar.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        # ROM File
        ctk.CTkLabel(frame, text='ROM File:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.rom_file = ctk.CTkEntry(
            frame, placeholder_text='/path/to/boot.bin', width=200, font=CTK_FONT_SMALL
        )
        self.rom_file.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.rom_file.bind('<KeyRelease>', lambda e: self._trigger_change())

    def get_config(self) -> dict:
        """获取配置"""
        return {
            'type': 'network',
            'rom_bar': self.rom_bar.get(),
            'rom_file': self.rom_file.get().strip()
        }
