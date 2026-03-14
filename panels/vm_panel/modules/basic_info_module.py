"""模块 1: 基础信息 - 虚拟机名称、UUID、机型、虚拟化类型等."""

import customtkinter as ctk

from ..tabs import BasicTab


class BasicInfoModule(ctk.CTkFrame):
    """基础信息模块."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent')
        self.on_change_callback = on_change_callback

        # 使用 BasicTab
        self.basic_tab = BasicTab(self, on_change_callback=on_change_callback)
        self.basic_tab.grid(row=0, column=0, sticky='nsew')
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def get_config(self) -> dict:
        """获取配置数据."""
        return self.basic_tab.get_config()

    def to_xml(self) -> dict:
        """生成 XML 配置字典."""
        return self.basic_tab.to_xml()

    def load_config(self, config: dict):
        """加载配置数据到 UI."""
        if hasattr(self.basic_tab, 'load_config'):
            self.basic_tab.load_config(config)
