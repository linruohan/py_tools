"""TPM 配置模块."""

import customtkinter as ctk

from utils.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class TPMConfig:
    """TPM 配置类."""

    def __init__(self, master, on_change_callback=None):
        """初始化 TPM 配置.

        Args:
            master: 父窗口组件
            on_change_callback: 配置变更回调函数
        """
        self.master = master
        self.on_change_callback = on_change_callback
        self.tpm_model = None
        self.tpm_version = None
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化 TPM 配置界面."""
        tpm_frame = ctk.CTkFrame(self.master, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        tpm_frame.grid(row=1, column=0, sticky='ew', padx=5, pady=5)
        tpm_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(tpm_frame, text='TPM Device', font=CTK_FONT_BOLD, text_color='#7986cb').grid(
            row=0, column=0, columnspan=4, padx=10, pady=5, sticky='w'
        )

        ctk.CTkLabel(tpm_frame, text='模型:', font=CTK_FONT_MAIN, width=60, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.tpm_model = ctk.CTkOptionMenu(
            tpm_frame,
            values=['none', 'tpm-crb', 'tpm-tis', 'tpm-spapr'],
            width=100,
            font=CTK_FONT_SMALL,
        )
        self.tpm_model.set('none')
        self.tpm_model.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.tpm_model.configure(command=self._trigger_change)

        ctk.CTkLabel(tpm_frame, text='版本:', font=CTK_FONT_MAIN, width=50, anchor='w').grid(
            row=1, column=2, padx=10, pady=5, sticky='w'
        )
        self.tpm_version = ctk.CTkOptionMenu(
            tpm_frame, values=['1.2', '2.0'], width=60, font=CTK_FONT_SMALL
        )
        self.tpm_version.set('2.0')
        self.tpm_version.grid(row=1, column=3, padx=5, pady=5, sticky='w')
        self.tpm_version.configure(command=self._trigger_change)

    def _trigger_change(self):
        """触发配置变更回调."""
        if self.on_change_callback:
            self.on_change_callback()

    def get_tpm_config(self):
        """获取 TPM 配置.

        Returns:
            dict or None: TPM 配置信息，当模型为 'none' 时返回 None
        """
        model = self.tpm_model.get()
        if model == 'none':
            return None
        return {
            'model': model,
            'version': self.tpm_version.get(),
        }
