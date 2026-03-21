"""密钥包装配置 Tab - Key Wrap (S390 Platform)."""

import customtkinter as ctk

from components.base_tab import BaseConfigTab
from utils.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class KeyWrapTab(BaseConfigTab):
    """密钥包装配置 Tab - S390 平台加密密钥管理.

    根据 libvirt 文档，keywrap 元素指定 guest 是否可以执行 S390 加密密钥管理操作。
    明文密钥可以通过在唯一包装密钥下加密来保护。

    支持的加密算法:
    - aes: AES 包装密钥
    - dea: DEA/TDEA 包装密钥 (DES/TDES)
    """

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, on_change_callback, **kwargs)

        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # 左侧框架 - AES 配置
        left_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        left_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        left_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(left_frame, text='AES 加密', font=CTK_FONT_BOLD, text_color='#64b5f6').grid(
            row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
        )

        ctk.CTkLabel(left_frame, text='算法:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.aes_cipher = ctk.CTkEntry(left_frame, width=100)
        self.aes_cipher.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.aes_cipher.insert(0, 'aes')
        self.aes_cipher.configure(state='disabled')  # 固定为 aes
        self.aes_cipher.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(left_frame, text='状态:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.aes_state = ctk.CTkOptionMenu(left_frame, values=['None', 'on', 'off'], width=80)
        self.aes_state.set('None')
        self.aes_state.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.aes_state.configure(command=lambda v: self._trigger_change())

        # 右侧框架 - DEA 配置
        right_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        right_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        right_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            right_frame, text='DEA/TDEA 加密', font=CTK_FONT_BOLD, text_color='#4caf50'
        ).grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w')

        ctk.CTkLabel(right_frame, text='算法:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.dea_cipher = ctk.CTkEntry(right_frame, width=100)
        self.dea_cipher.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.dea_cipher.insert(0, 'dea')
        self.dea_cipher.configure(state='disabled')  # 固定为 dea
        self.dea_cipher.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(right_frame, text='状态:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.dea_state = ctk.CTkOptionMenu(right_frame, values=['None', 'on', 'off'], width=80)
        self.dea_state.set('None')
        self.dea_state.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.dea_state.configure(command=lambda v: self._trigger_change())

        # 下方说明框架
        info_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        info_frame.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=5, pady=5)

        ctk.CTkLabel(info_frame, text='说明', font=CTK_FONT_BOLD, text_color='#ff9800').grid(
            row=0, column=0, padx=10, pady=5, sticky='w'
        )

        info_text = (
            '密钥包装 (Key Wrap) 用于 S390 平台的加密密钥管理操作。\n\n'
            '功能说明:\n'
            '• 明文密钥可以通过在唯一包装密钥下加密来保护\n'
            '• 包装密钥为每个 guest VM 生成\n'
            '• 支持两种加密算法：AES 和 DEA/TDEA\n\n'
            '算法说明:\n'
            '• AES - 高级加密标准 (Advanced Encryption Standard)\n'
            '• DEA/TDEA - 数据加密算法/三重 DEA (同 DES/TDES)\n\n'
            '注意:\n'
            '• 至少需要一个 cipher 元素\n'
            '• state 设为 on 启用该算法的密钥管理操作\n'
            '• 不配置 keywrap 元素时，默认两种算法都启用'
        )
        ctk.CTkLabel(
            info_frame,
            text=info_text,
            font=CTK_FONT_SMALL,
            text_color='#888888',
            justify='left',
        ).grid(row=1, column=0, padx=10, pady=5, sticky='w')

    def get_config(self) -> dict:
        """获取配置数据."""
        return {
            'aes_cipher': self.aes_cipher.get().strip(),
            'aes_state': self.aes_state.get(),
            'dea_cipher': self.dea_cipher.get().strip(),
            'dea_state': self.dea_state.get(),
        }

    def to_xml(self) -> dict:
        """生成 XML 配置字典."""
        config = self.get_config()

        # 构建 cipher 列表
        # 当 state='None' 时，不输出该 cipher
        cipher_list = []

        aes_state = config.get('aes_state')
        if aes_state and aes_state != 'None':
            cipher_list.append(
                {
                    'name': config.get('aes_cipher', 'aes'),
                    'state': aes_state,
                }
            )

        dea_state = config.get('dea_state')
        if dea_state and dea_state != 'None':
            cipher_list.append(
                {
                    'name': config.get('dea_cipher', 'dea'),
                    'state': dea_state,
                }
            )

        return {'key_wrap': {'cipher': cipher_list}} if cipher_list else {}

    def load_config(self, config: dict) -> None:
        """加载配置数据.

        Args:
            config: 配置字典
        """
        if 'cipher' in config:
            cipher_list = config['cipher']
            if isinstance(cipher_list, list):
                for cipher in cipher_list:
                    if isinstance(cipher, dict):
                        name = cipher.get('name', '')
                        state = cipher.get('state', 'off')
                        if name == 'aes':
                            self.aes_state.set(state)
                        elif name == 'dea':
                            self.dea_state.set(state)
