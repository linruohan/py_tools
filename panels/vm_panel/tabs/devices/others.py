"""其他设备模块 - 串口、TPM、控制器、音频配置."""

import customtkinter as ctk

from components.base_tab import BaseConfigTab


class OthersTab(BaseConfigTab):
    """其他设备配置 Tab - 串口、TPM、控制器."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, on_change_callback, **kwargs)
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        frame = ctk.CTkFrame(self, fg_color='transparent')
        frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            frame, 
            text='其他设备配置', 
            font=ctk.CTkFont(size=16, weight='bold')
        ).grid(row=0, column=0, padx=10, pady=10, sticky='w')

        ctk.CTkLabel(
            frame, 
            text='此模块已被拆分到各个专门的子模块中', 
            font=ctk.CTkFont(size=12)
        ).grid(row=1, column=0, padx=10, pady=5, sticky='w')

    def get_serial_config(self):
        """获取串口配置."""
        return {'type': 'pty', 'port': '0'}

    def get_tpm_config(self):
        """获取 TPM 配置."""
        return None

    def get_audio_config(self):
        """获取音频配置."""
        return {'model': 'ich9'}

    def get_controller_config(self):
        """获取控制器配置."""
        return {'disable_usb': False, 'disable_sound': False}
