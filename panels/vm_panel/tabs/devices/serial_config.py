"""串口配置模块."""

import customtkinter as ctk

from utils.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class SerialConfig:
    """串口配置类."""

    def __init__(self, master, on_change_callback=None):
        """初始化串口配置.

        Args:
            master: 父窗口组件
            on_change_callback: 配置变更回调函数
        """
        self.master = master
        self.on_change_callback = on_change_callback
        self.serial_type = None
        self.serial_port = None
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化串口配置界面."""
        serial_frame = ctk.CTkFrame(self.master, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        serial_frame.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
        serial_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            serial_frame, text='Serial Configuration', font=CTK_FONT_BOLD, text_color='#ff9800'
        ).grid(row=0, column=0, columnspan=4, padx=10, pady=5, sticky='w')

        ctk.CTkLabel(serial_frame, text='类型:', font=CTK_FONT_MAIN, width=60, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.serial_type = ctk.CTkOptionMenu(
            serial_frame,
            values=['pty', 'tcp', 'udp', 'unix', 'spicevmc', 'none'],
            width=100,
            font=CTK_FONT_SMALL,
        )
        self.serial_type.set('pty')
        self.serial_type.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.serial_type.configure(command=self._trigger_change)

        ctk.CTkLabel(serial_frame, text='端口:', font=CTK_FONT_MAIN, width=50, anchor='w').grid(
            row=1, column=2, padx=10, pady=5, sticky='w'
        )
        self.serial_port = ctk.CTkEntry(serial_frame, width=80, font=CTK_FONT_SMALL)
        self.serial_port.grid(row=1, column=3, padx=5, pady=5, sticky='w')
        self.serial_port.insert(0, '0')
        self.serial_port.bind('<KeyRelease>', lambda e: self._trigger_change())

    def _trigger_change(self):
        """触发配置变更回调."""
        if self.on_change_callback:
            self.on_change_callback()

    def get_serial_config(self):
        """获取串口配置.

        Returns:
            dict: 串口配置信息
        """
        return {
            'type': self.serial_type.get(),
            'port': self.serial_port.get().strip() or '0',
        }
