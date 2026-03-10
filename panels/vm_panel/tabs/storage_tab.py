"""存储配置 Tab."""

import customtkinter as ctk

from ..styles import BG_COLOR_CONTENT
from ..frames import ScrollableDiskFrame


class StorageTab(ctk.CTkFrame):
    """存储配置 Tab."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent')
        self.on_change_callback = on_change_callback
        self.disk_frame = None

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

        add_disk_btn = ctk.CTkButton(
            toolbar,
            text='添加磁盘',
            command=lambda: (self.add_disk(), self._trigger_change()),
            fg_color='#4caf50',
            hover_color='#388e3c',
            width=100,
        )
        add_disk_btn.pack(side='left', padx=5)

        # 添加 CDROM 按钮
        add_cdrom_btn = ctk.CTkButton(
            toolbar,
            text='添加光驱',
            command=lambda: (self.add_cdrom(), self._trigger_change()),
            fg_color='#ff9800',
            hover_color='#f57c00',
            width=100,
        )
        add_cdrom_btn.pack(side='left', padx=5)

        # 磁盘列表
        self.disk_frame = ScrollableDiskFrame(
            self, corner_radius=0, fg_color=BG_COLOR_CONTENT, on_change_callback=self._trigger_change
        )
        self.disk_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=5)
        self.grid_rowconfigure(1, weight=1)

        # 默认添加一个磁盘
        self.add_disk()

    def _trigger_change(self):
        """触发变化回调."""
        if self.on_change_callback:
            self.on_change_callback()

    def add_disk(self):
        """添加磁盘配置行."""
        if self.disk_frame:
            self.disk_frame.add_disk()

    def add_cdrom(self):
        """添加光驱配置行."""
        if self.disk_frame:
            self.disk_frame.add_cdrom()

    def get_disks(self):
        """获取所有磁盘配置."""
        if self.disk_frame:
            return self.disk_frame.get_disks()
        return []
