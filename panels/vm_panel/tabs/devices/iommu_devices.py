"""IOMMU 设备配置模块."""

import customtkinter as ctk

from components.base_tab import BaseConfigTab


class IOMMUDevicesTab(BaseConfigTab):
    """IOMMU 设备配置标签页 - 紧凑布局."""

    def __init__(self, parent, on_change_callback=None, **kwargs):
        super().__init__(parent, on_change_callback, **kwargs)

    def _init_ui(self):
        """创建 IOMMU 设备配置界面 - 所有元素紧凑排列到一行."""
        # 单行布局,所有元素 pack 左对齐
        ctk.CTkLabel(self, text='IOMMU:', font=ctk.CTkFont(weight='bold')).pack(
            side='left', padx=5, pady=5
        )

        self.type_var = ctk.StringVar(value='intel')
        type_menu = ctk.CTkOptionMenu(
            self,
            variable=self.type_var,
            values=['intel', 'amd', 'none'],
            width=80,
            command=lambda e=None: self._trigger_change(),
        )
        type_menu.pack(side='left', padx=5, pady=5)

        ctk.CTkLabel(self, text='Address:').pack(side='left', padx=5, pady=5)
        self.address_entry = ctk.CTkEntry(self, width=150)
        self.address_entry.pack(side='left', padx=5, pady=5)
        self.address_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(self, text='Mode:').pack(side='left', padx=5, pady=5)
        self.mode_var = ctk.StringVar(value='strict')
        mode_menu = ctk.CTkOptionMenu(
            self,
            variable=self.mode_var,
            values=['strict', 'relaxed'],
            width=80,
            command=lambda e=None: self._trigger_change(),
        )
        mode_menu.pack(side='left', padx=5, pady=5)

        ctk.CTkLabel(self, text='UUID:').pack(side='left', padx=5, pady=5)
        self.uuid_entry = ctk.CTkEntry(self, width=200)
        self.uuid_entry.pack(side='left', padx=5, pady=5)
        self.uuid_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

    def get_config(self):
        """获取 IOMMU 设备配置."""
        return {
            'model': self.type_var.get(),
            'caching_mode': 'on' if self.mode_var.get() == 'strict' else None,
            'address': self.address_entry.get() or None,
            'uuid': self.uuid_entry.get() or None,
        }

    def to_xml(self) -> dict:
        """生成 XML 配置字典."""
        iommu_type = self.type_var.get()

        # 如果选择了 none,不生成 XML
        if iommu_type == 'none':
            return {}

        return {
            'iommu': [
                {
                    'model': iommu_type,
                    'caching_mode': 'on' if self.mode_var.get() == 'strict' else None,
                    'address': self.address_entry.get() or None,
                    'uuid': self.uuid_entry.get() or None,
                }
            ]
        }
