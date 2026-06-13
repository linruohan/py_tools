"""存储配置 Tab."""

from typing import Any

import customtkinter as ctk

from components.base_tab import BaseConfigTab
from utils.styles import BG_COLOR_CONTENT

from ..frames import ScrollableDiskFrame


class StorageTab(BaseConfigTab):
    """存储配置 Tab."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, on_change_callback, **kwargs)
        self.disk_frame: ScrollableDiskFrame | None = None

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
            command=self._on_add_disk,
            fg_color='#4caf50',
            hover_color='#388e3c',
            width=100,
        )
        add_disk_btn.pack(side='left', padx=5)

        # 添加 CDROM 按钮
        add_cdrom_btn = ctk.CTkButton(
            toolbar,
            text='添加光驱',
            command=self._on_add_cdrom,
            fg_color='#ff9800',
            hover_color='#f57c00',
            width=100,
        )
        add_cdrom_btn.pack(side='left', padx=5)

        # 磁盘列表
        self.disk_frame = ScrollableDiskFrame(
            self,
            corner_radius=0,
            fg_color=BG_COLOR_CONTENT,
            on_change_callback=self._trigger_change,
        )
        self.disk_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=5)
        self.grid_rowconfigure(1, weight=1)

        # 默认添加一个磁盘
        self.add_disk()

    def _on_add_disk(self) -> None:
        """添加磁盘并触发变更."""
        self.add_disk()
        self._trigger_change()

    def _on_add_cdrom(self) -> None:
        """添加光驱并触发变更."""
        self.add_cdrom()
        self._trigger_change()

    def add_disk(self) -> None:
        """添加磁盘配置行."""
        if self.disk_frame:
            self.disk_frame.add_disk()

    def add_cdrom(self) -> None:
        """添加光驱配置行."""
        if self.disk_frame:
            self.disk_frame.add_cdrom()

    def get_disks(self) -> list[Any]:
        """获取所有磁盘配置."""
        if self.disk_frame:
            return self.disk_frame.get_disks()
        return []
