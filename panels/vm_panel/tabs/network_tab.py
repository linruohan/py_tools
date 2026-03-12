"""网络配置 Tab."""

import customtkinter as ctk

from ..frames import ScrollableNetworkFrame
from ..styles import BG_COLOR_CONTENT


class NetworkTab(ctk.CTkFrame):
    """网络配置 Tab."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent')
        self.on_change_callback = on_change_callback
        self.network_frame = None

        # 初始化 UI
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面."""
        # 配置 grid 权重
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # 工具栏
        toolbar = ctk.CTkFrame(self, fg_color='transparent')
        toolbar.grid(row=0, column=0, sticky='ew', padx=10, pady=5)

        add_net_btn = ctk.CTkButton(
            toolbar,
            text='添加网卡',
            command=lambda: (self.add_network(), self._trigger_change()),
            fg_color='#4caf50',
            hover_color='#388e3c',
            width=100,
        )
        add_net_btn.pack(side='left', padx=5)

        # 网络列表
        self.network_frame = ScrollableNetworkFrame(
            self,
            corner_radius=0,
            fg_color=BG_COLOR_CONTENT,
            on_change_callback=self._trigger_change,
        )
        self.network_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=5)
        self.grid_rowconfigure(1, weight=1)

        # 默认添加一个网卡
        self.add_network()

    def _trigger_change(self, *args):
        """触发变化回调."""
        if self.on_change_callback:
            self.on_change_callback()

    def add_network(self):
        """添加网络配置行."""
        if self.network_frame:
            self.network_frame.add_network()

    def get_networks(self):
        """获取所有网络配置."""
        if self.network_frame:
            return self.network_frame.get_networks()
        return []
