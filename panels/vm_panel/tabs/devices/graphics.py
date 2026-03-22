"""图形显示模块 - VNC/SPICE 图形配置 (根据 libvirt devices 文档)."""

import customtkinter as ctk

from components.base_tab import BaseConfigTab
from utils.styles import CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class GraphicsTab(BaseConfigTab):
    """图形显示配置 Tab - 支持 VNC, SPICE, RDP, SDL, Desktop, EGL-headless, D-Bus."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, on_change_callback, **kwargs)

        self.graphics_type = None
        self.autoport = None
        self.port = None
        self.tls_port = None
        self.listen = None
        self.passwd = None
        self.keymap = None
        self.share_policy = None
        self.power_control = None
        self.wait = None

        # SPICE specific
        self.spice_default_mode = None
        self.spice_image_compression = None
        self.spice_streaming_mode = None
        self.spice_clipboard = None
        self.spice_mouse_mode = None
        self.spice_filetransfer = None

        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面 - 所有 section 合并，每行紧凑排列。"""
        # 滚动框架
        scroll_frame = ctk.CTkScrollableFrame(self, fg_color='transparent', corner_radius=6)
        scroll_frame.pack(fill='both', expand=True, padx=5, pady=5)

        # 标题
        ctk.CTkLabel(scroll_frame, text='Graphics', font=CTK_FONT_BOLD, text_color='#ba68c8', width=100).pack(side='left', padx=2, pady=2)

        # 第一行：Type, Autoport, Port, Listen
        ctk.CTkLabel(scroll_frame, text='Type:', font=CTK_FONT_MAIN, width=40).pack(side='left', padx=5, pady=2)
        self.graphics_type = ctk.CTkOptionMenu(
            scroll_frame,
            values=['vnc', 'spice', 'rdp', 'sdl', 'desktop', 'egl-headless', 'dbus', 'none'],
            width=100,
            font=CTK_FONT_SMALL,
            command=self._on_type_changed,
        )
        self.graphics_type.set('vnc')
        self.graphics_type.pack(side='left', padx=2, pady=2)

        ctk.CTkLabel(scroll_frame, text='Autoport:', font=CTK_FONT_MAIN, width=60).pack(side='left', padx=5, pady=2)
        self.autoport = ctk.CTkCheckBox(scroll_frame, text='On', font=CTK_FONT_SMALL, width=50)
        self.autoport.select()
        self.autoport.pack(side='left', padx=2, pady=2)
        self.autoport.configure(command=self._trigger_change)

        ctk.CTkLabel(scroll_frame, text='Port:', font=CTK_FONT_MAIN, width=35).pack(side='left', padx=3, pady=2)
        self.port = ctk.CTkEntry(scroll_frame, placeholder_text='-1', width=50, font=CTK_FONT_SMALL)
        self.port.insert(0, '-1')
        self.port.pack(side='left', padx=2, pady=2)
        self.port.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(scroll_frame, text='Listen:', font=CTK_FONT_MAIN, width=45).pack(side='left', padx=3, pady=2)
        self.listen = ctk.CTkEntry(scroll_frame, placeholder_text='0.0.0.0', width=90, font=CTK_FONT_SMALL)
        self.listen.insert(0, '0.0.0.0')
        self.listen.pack(side='left', padx=2, pady=2)
        self.listen.bind('<KeyRelease>', lambda e: self._trigger_change())

        # 第二行：TLS Port, Password, Keymap
        ctk.CTkLabel(scroll_frame, text='TLS:', font=CTK_FONT_MAIN, width=30).pack(side='left', padx=3, pady=2)
        self.tls_port = ctk.CTkEntry(scroll_frame, placeholder_text='-1', width=50, font=CTK_FONT_SMALL)
        self.tls_port.insert(0, '-1')
        self.tls_port.pack(side='left', padx=2, pady=2)
        self.tls_port.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(scroll_frame, text='Passwd:', font=CTK_FONT_MAIN, width=50).pack(side='left', padx=3, pady=2)
        self.passwd = ctk.CTkEntry(scroll_frame, placeholder_text='', width=100, font=CTK_FONT_SMALL, show='*')
        self.passwd.pack(side='left', padx=2, pady=2)
        self.passwd.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(scroll_frame, text='Keymap:', font=CTK_FONT_MAIN, width=55).pack(side='left', padx=3, pady=2)
        self.keymap = ctk.CTkEntry(scroll_frame, placeholder_text='en-us', width=70, font=CTK_FONT_SMALL)
        self.keymap.insert(0, 'en-us')
        self.keymap.pack(side='left', padx=2, pady=2)
        self.keymap.bind('<KeyRelease>', lambda e: self._trigger_change())

        # 第三行：VNC 选项
        ctk.CTkLabel(scroll_frame, text='VNC:', font=CTK_FONT_MAIN, width=35).pack(side='left', padx=3, pady=2)
        ctk.CTkLabel(scroll_frame, text='Share:', font=CTK_FONT_MAIN, width=40).pack(side='left', padx=3, pady=2)
        self.share_policy = ctk.CTkOptionMenu(
            scroll_frame,
            values=['allow-exclusive', 'force-shared', 'ignore'],
            width=110,
            font=CTK_FONT_SMALL,
            command=self._trigger_change,
        )
        self.share_policy.set('allow-exclusive')
        self.share_policy.pack(side='left', padx=2, pady=2)

        ctk.CTkLabel(scroll_frame, text='Power:', font=CTK_FONT_MAIN, width=40).pack(side='left', padx=3, pady=2)
        self.power_control = ctk.CTkCheckBox(scroll_frame, text='On', font=CTK_FONT_SMALL, width=45)
        self.power_control.deselect()
        self.power_control.pack(side='left', padx=2, pady=2)
        self.power_control.configure(command=self._trigger_change)

        ctk.CTkLabel(scroll_frame, text='Wait:', font=CTK_FONT_MAIN, width=35).pack(side='left', padx=3, pady=2)
        self.wait = ctk.CTkCheckBox(scroll_frame, text='Wait', font=CTK_FONT_SMALL, width=50)
        self.wait.deselect()
        self.wait.pack(side='left', padx=2, pady=2)
        self.wait.configure(command=self._trigger_change)

        # SPICE 选项分隔线
        ctk.CTkLabel(scroll_frame, text='|', text_color='#666666').pack(side='left', padx=10, pady=2)
        ctk.CTkLabel(scroll_frame, text='SPICE:', font=CTK_FONT_BOLD, text_color='#ff9800', width=50).pack(side='left', padx=3, pady=2)

        # SPICE 选项行
        ctk.CTkLabel(scroll_frame, text='Mode:', font=CTK_FONT_MAIN, width=40).pack(side='left', padx=3, pady=2)
        self.spice_default_mode = ctk.CTkOptionMenu(
            scroll_frame,
            values=['any', 'secure', 'insecure'],
            width=80,
            font=CTK_FONT_SMALL,
            command=self._trigger_change,
        )
        self.spice_default_mode.set('any')
        self.spice_default_mode.pack(side='left', padx=2, pady=2)

        ctk.CTkLabel(scroll_frame, text='Compression:', font=CTK_FONT_MAIN, width=75).pack(side='left', padx=3, pady=2)
        self.spice_image_compression = ctk.CTkOptionMenu(
            scroll_frame,
            values=['auto_glz', 'auto_lz', 'quic', 'glz', 'lz', 'off'],
            width=90,
            font=CTK_FONT_SMALL,
            command=self._trigger_change,
        )
        self.spice_image_compression.set('auto_glz')
        self.spice_image_compression.pack(side='left', padx=2, pady=2)

        ctk.CTkLabel(scroll_frame, text='Stream:', font=CTK_FONT_MAIN, width=50).pack(side='left', padx=3, pady=2)
        self.spice_streaming_mode = ctk.CTkOptionMenu(
            scroll_frame,
            values=['filter', 'all', 'off'],
            width=70,
            font=CTK_FONT_SMALL,
            command=self._trigger_change,
        )
        self.spice_streaming_mode.set('filter')
        self.spice_streaming_mode.pack(side='left', padx=2, pady=2)

        # SPICE 选项第二行
        ctk.CTkLabel(scroll_frame, text='Clipboard:', font=CTK_FONT_MAIN, width=60).pack(side='left', padx=3, pady=2)
        self.spice_clipboard = ctk.CTkOptionMenu(
            scroll_frame,
            values=['yes', 'no'],
            width=60,
            font=CTK_FONT_SMALL,
            command=self._trigger_change,
        )
        self.spice_clipboard.set('yes')
        self.spice_clipboard.pack(side='left', padx=2, pady=2)

        ctk.CTkLabel(scroll_frame, text='Mouse:', font=CTK_FONT_MAIN, width=45).pack(side='left', padx=3, pady=2)
        self.spice_mouse_mode = ctk.CTkOptionMenu(
            scroll_frame,
            values=['client', 'server'],
            width=70,
            font=CTK_FONT_SMALL,
            command=self._trigger_change,
        )
        self.spice_mouse_mode.set('client')
        self.spice_mouse_mode.pack(side='left', padx=2, pady=2)

        ctk.CTkLabel(scroll_frame, text='FileTransfer:', font=CTK_FONT_MAIN, width=75).pack(side='left', padx=3, pady=2)
        self.spice_filetransfer = ctk.CTkOptionMenu(
            scroll_frame,
            values=['yes', 'no'],
            width=60,
            font=CTK_FONT_SMALL,
            command=self._trigger_change,
        )
        self.spice_filetransfer.set('yes')
        self.spice_filetransfer.pack(side='left', padx=2, pady=2)

    def _on_type_changed(self, new_type: str) -> None:
        """Graphics 类型改变时的处理."""
        self._trigger_change()

    def get_config(self) -> dict:
        """获取图形配置."""
        config = {
            'type': self.graphics_type.get(),
            'autoport': self.autoport.get(),
            'port': self.port.get().strip() or '-1',
            'listen': self.listen.get().strip() or '0.0.0.0',
            'passwd': self.passwd.get().strip() or None,
            'keymap': self.keymap.get().strip() or 'en-us',
            'share_policy': self.share_policy.get() if self.graphics_type.get() == 'vnc' else None,
            'power_control': self.power_control.get() if self.graphics_type.get() == 'vnc' else None,
            'wait': self.wait.get() if self.graphics_type.get() == 'vnc' else None,
        }

        # SPICE specific
        if self.graphics_type.get() == 'spice':
            config.update({
                'tls_port': self.tls_port.get().strip() or '-1',
                'spice_default_mode': self.spice_default_mode.get(),
                'spice_image_compression': self.spice_image_compression.get(),
                'spice_streaming_mode': self.spice_streaming_mode.get(),
                'spice_clipboard': self.spice_clipboard.get(),
                'spice_mouse_mode': self.spice_mouse_mode.get(),
                'spice_filetransfer': self.spice_filetransfer.get(),
            })

        return config

    def to_xml(self) -> dict:
        """生成 XML 配置字典."""
        gfx_type = self.graphics_type.get()

        # 如果选择了 none，不生成 XML
        if gfx_type == 'none':
            return {}

        config = self.get_config()
        return {'graphics': config}
