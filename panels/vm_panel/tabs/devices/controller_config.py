"""控制器配置模块."""

import customtkinter as ctk

from utils.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_SMALL
from .audio_config import AudioConfig


class ControllerConfig:
    """控制器配置类."""

    def __init__(self, master, on_change_callback=None):
        """初始化控制器配置.

        Args:
            master: 父窗口组件
            on_change_callback: 配置变更回调函数
        """
        self.master = master
        self.on_change_callback = on_change_callback
        self.disable_usb_check = None
        self.disable_sound_check = None
        self.audio_config = None
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化控制器配置界面."""
        ctrl_frame = ctk.CTkFrame(self.master, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        ctrl_frame.grid(row=2, column=0, sticky='ew', padx=5, pady=5)
        ctrl_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(ctrl_frame, text='Controller', font=CTK_FONT_BOLD, text_color='#ff7043').grid(
            row=0, column=0, columnspan=3, padx=10, pady=5, sticky='w'
        )

        self.disable_usb_check = ctk.CTkCheckBox(
            ctrl_frame, text='Disable USB', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.disable_usb_check.grid(row=1, column=0, padx=10, pady=5, sticky='w')

        self.disable_sound_check = ctk.CTkCheckBox(
            ctrl_frame, text='Disable Sound', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.disable_sound_check.grid(row=1, column=1, padx=10, pady=5, sticky='w')

        # 集成音频配置
        self.audio_config = AudioConfig(ctrl_frame, self._trigger_change)

    def _trigger_change(self):
        """触发配置变更回调."""
        if self.on_change_callback:
            self.on_change_callback()

    def get_controller_config(self):
        """获取控制器配置.

        Returns:
            dict: 控制器配置信息
        """
        return {
            'disable_usb': self.disable_usb_check.get(),
            'disable_sound': self.disable_sound_check.get(),
        }

    def get_audio_config(self):
        """获取音频配置.

        Returns:
            dict or None: 音频配置信息
        """
        return self.audio_config.get_audio_config()
