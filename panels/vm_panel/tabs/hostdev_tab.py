"""PCI 直通设备 Tab."""

import customtkinter as ctk

from components.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD

from ..frames import ScrollableHostdevFrame


class HostdevTab(ctk.CTkFrame):
    """PCI 直通设备 Tab."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent')
        self.on_change_callback = on_change_callback
        self.hostdev_frame = None

        # 初始化 UI
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面."""
        # 配置 grid 权重
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        hostdev_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=8)
        hostdev_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        hostdev_frame.grid_rowconfigure(1, weight=1)
        hostdev_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            hostdev_frame, text='PCI 直通设备', font=CTK_FONT_BOLD, text_color='#81c784'
        ).grid(row=0, column=0, padx=10, pady=5, sticky='w')

        # 添加工具栏
        gpu_toolbar = ctk.CTkFrame(hostdev_frame, fg_color='transparent')
        gpu_toolbar.grid(row=1, column=0, sticky='ew', padx=10, pady=5)

        add_gpu_btn = ctk.CTkButton(
            gpu_toolbar,
            text='添加 PCI 设备',
            command=self.add_hostdev,
            fg_color='#ff9800',
            hover_color='#f57c00',
            width=120,
        )
        add_gpu_btn.pack(side='left', padx=5)

        # PCI 设备列表
        self.hostdev_frame = ScrollableHostdevFrame(
            hostdev_frame,
            corner_radius=0,
            fg_color=BG_COLOR_CONTENT,
            on_change_callback=self._trigger_change,
        )
        self.hostdev_frame.grid(row=2, column=0, sticky='nsew', padx=10, pady=5)

    def _trigger_change(self, *args):
        """触发变化回调."""
        if self.on_change_callback:
            self.on_change_callback()

    def add_hostdev(self):
        """添加 PCI 直通设备."""
        if self.hostdev_frame:
            self.hostdev_frame.add_hostdev()

    def get_hostdevs(self):
        """获取所有 PCI 直通设备配置."""
        if self.hostdev_frame:
            return self.hostdev_frame.get_hostdevs()
        return []
