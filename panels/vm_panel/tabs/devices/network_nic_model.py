"""NIC模型设置模块 - NIC模型配置"""

import customtkinter as ctk

from components.base_tab import BaseConfigTab
from utils.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class NICModelTab(BaseConfigTab):
    """NIC模型配置"""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, on_change_callback, **kwargs)
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面"""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            frame, text='Setting the NIC model', font=CTK_FONT_BOLD, text_color='#2196f3'
        ).grid(row=0, column=0, columnspan=4, padx=10, pady=5, sticky='w')

        # NIC Model
        ctk.CTkLabel(frame, text='NIC Model:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.nic_model = ctk.CTkOptionMenu(
            frame,
            values=['e1000', 'e1000e', 'virtio', 'rtl8139', 'pcnet', 'ne2k_pci'],
            width=150,
            font=CTK_FONT_SMALL,
            command=self._trigger_change
        )
        self.nic_model.set('virtio')
        self.nic_model.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        # VLAN Tag
        ctk.CTkLabel(frame, text='VLAN Tag:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.vlan_tag = ctk.CTkEntry(
            frame, placeholder_text='1', width=100, font=CTK_FONT_SMALL
        )
        self.vlan_tag.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.vlan_tag.bind('<KeyRelease>', lambda e: self._trigger_change())

    def get_config(self) -> dict:
        """获取配置"""
        return {
            'type': 'network',
            'nic_model': self.nic_model.get(),
            'vlan_tag': self.vlan_tag.get().strip()
        }
