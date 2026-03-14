"""其他设备模块 - 串口、TPM、控制器、音频配置."""

import customtkinter as ctk

from components.base_tab import BaseConfigTab
from .serial_config import SerialConfig
from .tpm_config import TPMConfig
from .controller_config import ControllerConfig


class OthersTab(BaseConfigTab):
    """其他设备配置 Tab - 串口、TPM、控制器."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, on_change_callback, **kwargs)

        self.serial_config = None
        self.tpm_config = None
        self.controller_config = None

        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=1)

        # 初始化各个配置模块
        self.serial_config = SerialConfig(self, self._trigger_change)
        self.tpm_config = TPMConfig(self, self._trigger_change)
        self.controller_config = ControllerConfig(self, self._trigger_change)

    def get_serial_config(self):
        """获取串口配置."""
        return self.serial_config.get_serial_config()

    def get_tpm_config(self):
        """获取 TPM 配置."""
        return self.tpm_config.get_tpm_config()

    def get_audio_config(self):
        """获取音频配置."""
        return self.controller_config.get_audio_config()

    def get_controller_config(self):
        """获取控制器配置."""
        return self.controller_config.get_controller_config()
