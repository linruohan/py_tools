"""密钥包装配置 Tab - Key Wrap."""

import customtkinter as ctk

from ..styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class KeyWrapTab(ctk.CTkFrame):
    """密钥包装配置 Tab - 加密密钥包装."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent')
        self.on_change_callback = on_change_callback

        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        left_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        left_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        left_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            left_frame, text='密钥包装配置', font=CTK_FONT_BOLD, text_color='#64b5f6'
        ).grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w')

        ctk.CTkLabel(left_frame, text='密钥名称:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.key_name = ctk.CTkEntry(left_frame, placeholder_text='密钥标识', width=200)
        self.key_name.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.key_name.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(left_frame, text='UUID:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.uuid = ctk.CTkEntry(left_frame, placeholder_text='密钥UUID', width=200)
        self.uuid.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.uuid.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(left_frame, text='用法:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=3, column=0, padx=10, pady=5, sticky='w'
        )
        self.usage = ctk.CTkEntry(left_frame, placeholder_text='密钥用法标识', width=200)
        self.usage.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        self.usage.bind('<KeyRelease>', lambda e: self._trigger_change())

        right_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        right_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)

        ctk.CTkLabel(right_frame, text='包装设置', font=CTK_FONT_BOLD, text_color='#4caf50').grid(
            row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
        )

        ctk.CTkLabel(right_frame, text='密码:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.cipher = ctk.CTkEntry(right_frame, placeholder_text='aes', width=150)
        self.cipher.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.cipher.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(right_frame, text='密钥大小:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.key_size = ctk.CTkEntry(right_frame, placeholder_text='256', width=80)
        self.key_size.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.key_size.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(right_frame, text='模式:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=3, column=0, padx=10, pady=5, sticky='w'
        )
        self.mode = ctk.CTkEntry(right_frame, placeholder_text='cbc-essiv', width=150)
        self.mode.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        self.mode.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(right_frame, text='哈希:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=4, column=0, padx=10, pady=5, sticky='w'
        )
        self.hash_alg = ctk.CTkEntry(right_frame, placeholder_text='sha256', width=150)
        self.hash_alg.grid(row=4, column=1, padx=5, pady=5, sticky='w')
        self.hash_alg.bind('<KeyRelease>', lambda e: self._trigger_change())

        info_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        info_frame.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=5, pady=5)

        ctk.CTkLabel(info_frame, text='说明', font=CTK_FONT_BOLD, text_color='#ff9800').grid(
            row=0, column=0, padx=10, pady=5, sticky='w'
        )

        info_text = (
            '密钥包装用于加密虚拟机磁盘镜像。\n\n'
            '支持的加密格式:\n'
            '• qcow2 - QEMU Copy On Write\n'
            '• luks - Linux Unified Key Setup\n\n'
            '常用密码算法:\n'
            '• aes - 高级加密标准\n'
            '• serpent - Serpent 密码\n'
            '• twofish - Twofish 密码'
        )
        ctk.CTkLabel(
            info_frame,
            text=info_text,
            font=CTK_FONT_SMALL,
            text_color='#888888',
            justify='left',
        ).grid(row=1, column=0, padx=10, pady=5, sticky='w')

    def _trigger_change(self):
        """触发变化回调."""
        if self.on_change_callback:
            self.on_change_callback()

    def get_config(self) -> dict:
        """获取配置数据."""
        return {
            'key_name': self.key_name.get().strip(),
            'uuid': self.uuid.get().strip(),
            'usage': self.usage.get().strip(),
            'cipher': self.cipher.get().strip(),
            'key_size': self.key_size.get().strip(),
            'mode': self.mode.get().strip(),
            'hash': self.hash_alg.get().strip(),
        }
