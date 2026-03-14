"""音频配置模块."""

import customtkinter as ctk

from utils.styles import BG_COLOR_CONTENT, CTK_FONT_MAIN, CTK_FONT_SMALL


class AudioConfig:
    """音频配置类."""

    def __init__(self, master, on_change_callback=None):
        """初始化音频配置.

        Args:
            master: 父窗口组件
            on_change_callback: 配置变更回调函数
        """
        self.master = master
        self.on_change_callback = on_change_callback
        self.audio_model = None
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化音频配置界面."""
        # 音频配置作为控制器配置的一部分，这里只创建音频模型选项
        ctk.CTkLabel(self.master, text='Audio:', font=CTK_FONT_MAIN, width=50, anchor='w').grid(
            row=1, column=2, padx=10, pady=5, sticky='w'
        )
        self.audio_model = ctk.CTkOptionMenu(
            self.master,
            values=['ich9', 'ich6', 'ac97', 'hda', 'none'],
            width=80,
            font=CTK_FONT_SMALL,
        )
        self.audio_model.set('ich9')
        self.audio_model.grid(row=1, column=3, padx=5, pady=5, sticky='w')
        self.audio_model.configure(command=self._trigger_change)

    def _trigger_change(self):
        """触发配置变更回调."""
        if self.on_change_callback:
            self.on_change_callback()

    def get_audio_config(self):
        """获取音频配置.

        Returns:
            dict or None: 音频配置信息，当模型为 'none' 时返回 None
        """
        model = self.audio_model.get()
        if model == 'none':
            return None
        return {'model': model}
