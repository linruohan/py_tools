import customtkinter as ctk
from components.base_tab import BaseConfigTab


class MemoryDevicesTab(BaseConfigTab):
    """内存设备配置标签页"""

    def __init__(self, parent, on_change_callback=None, **kwargs):
        """初始化内存设备配置标签页

        Args:
            parent: 父窗口
            on_change_callback: 配置变更回调函数
        """
        super().__init__(parent, on_change_callback, **kwargs)
        self._create_widgets()

    def _create_widgets(self):
        """创建内存设备配置界面"""
        # 内存设备配置
        memory_frame = ctk.CTkFrame(self, corner_radius=8)
        memory_frame.pack(fill='x', padx=10, pady=5)

        ctk.CTkLabel(memory_frame, text='内存设备配置:', font=ctk.CTkFont(weight='bold')).pack(
            anchor='w', padx=10, pady=5
        )

        # 设备类型
        type_frame = ctk.CTkFrame(memory_frame)
        type_frame.pack(fill='x', padx=10, pady=5)
        ctk.CTkLabel(type_frame, text='设备类型:', width=100).pack(side='left', padx=5, pady=5)
        self.type_var = ctk.StringVar(value='dimm')
        type_options = ctk.CTkOptionMenu(
            type_frame, variable=self.type_var, values=['dimm', 'nvdimm']
        )
        type_options.pack(side='left', fill='x', expand=True, padx=5, pady=5)

        # 设备地址
        address_frame = ctk.CTkFrame(memory_frame)
        address_frame.pack(fill='x', padx=10, pady=5)
        ctk.CTkLabel(address_frame, text='设备地址:', width=100).pack(side='left', padx=5, pady=5)
        self.address_entry = ctk.CTkEntry(address_frame)
        self.address_entry.pack(side='left', fill='x', expand=True, padx=5, pady=5)

        # 内存设备属性
        props_frame = ctk.CTkFrame(self, corner_radius=8)
        props_frame.pack(fill='x', padx=10, pady=5)

        ctk.CTkLabel(props_frame, text='内存设备属性:', font=ctk.CTkFont(weight='bold')).pack(
            anchor='w', padx=10, pady=5
        )

        # 内存大小
        size_frame = ctk.CTkFrame(props_frame)
        size_frame.pack(fill='x', padx=10, pady=5)
        ctk.CTkLabel(size_frame, text='内存大小:', width=100).pack(side='left', padx=5, pady=5)
        self.size_entry = ctk.CTkEntry(size_frame, placeholder_text='例如: 1024M')
        self.size_entry.pack(side='left', fill='x', expand=True, padx=5, pady=5)

        # 内存标签
        label_frame = ctk.CTkFrame(props_frame)
        label_frame.pack(fill='x', padx=10, pady=5)
        ctk.CTkLabel(label_frame, text='内存标签:', width=100).pack(side='left', padx=5, pady=5)
        self.label_entry = ctk.CTkEntry(label_frame)
        self.label_entry.pack(side='left', fill='x', expand=True, padx=5, pady=5)

        # 内存设备 UUID
        uuid_frame = ctk.CTkFrame(props_frame)
        uuid_frame.pack(fill='x', padx=10, pady=5)
        ctk.CTkLabel(uuid_frame, text='设备UUID:', width=100).pack(side='left', padx=5, pady=5)
        self.uuid_entry = ctk.CTkEntry(uuid_frame)
        self.uuid_entry.pack(side='left', fill='x', expand=True, padx=5, pady=5)

    def get_config(self):
        """获取内存设备配置

        Returns:
            dict: 内存设备配置数据
        """
        return {
            'type': self.type_var.get(),
            'address': self.address_entry.get(),
            'size': self.size_entry.get(),
            'label': self.label_entry.get(),
            'uuid': self.uuid_entry.get(),
        }
