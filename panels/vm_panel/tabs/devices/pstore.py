import customtkinter as ctk
from components.base_tab import BaseConfigTab


class PstoreTab(BaseConfigTab):
    """Pstore设备配置标签页"""
    
    def __init__(self, parent, on_change_callback=None, **kwargs):
        """初始化Pstore设备配置标签页
        
        Args:
            parent: 父窗口
            on_change_callback: 配置变更回调函数
        """
        super().__init__(parent, on_change_callback, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        """创建Pstore设备配置界面"""
        # Pstore设备配置
        pstore_frame = ctk.CTkFrame(self, corner_radius=8)
        pstore_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(pstore_frame, text="Pstore设备配置:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=5)
        
        # 设备模型
        model_frame = ctk.CTkFrame(pstore_frame)
        model_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(model_frame, text="设备模型:", width=100).pack(side="left", padx=5, pady=5)
        self.model_var = ctk.StringVar(value="virtio")
        model_options = ctk.CTkOptionMenu(
            model_frame,
            variable=self.model_var,
            values=["virtio"]
        )
        model_options.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        
        # 设备地址
        address_frame = ctk.CTkFrame(pstore_frame)
        address_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(address_frame, text="设备地址:", width=100).pack(side="left", padx=5, pady=5)
        self.address_entry = ctk.CTkEntry(address_frame)
        self.address_entry.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        
        # Pstore设备属性
        props_frame = ctk.CTkFrame(self, corner_radius=8)
        props_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(props_frame, text="Pstore设备属性:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=5)
        
        # Pstore类型
        type_frame = ctk.CTkFrame(props_frame)
        type_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(type_frame, text="Pstore类型:", width=100).pack(side="left", padx=5, pady=5)
        self.type_var = ctk.StringVar(value="ramoops")
        type_options = ctk.CTkOptionMenu(
            type_frame,
            variable=self.type_var,
            values=["ramoops", "pstore"]
        )
        type_options.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        
        # Pstore大小
        size_frame = ctk.CTkFrame(props_frame)
        size_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(size_frame, text="Pstore大小:", width=100).pack(side="left", padx=5, pady=5)
        self.size_entry = ctk.CTkEntry(size_frame, placeholder_text="例如: 64k")
        self.size_entry.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        
        # Pstore设备 UUID
        uuid_frame = ctk.CTkFrame(props_frame)
        uuid_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(uuid_frame, text="设备UUID:", width=100).pack(side="left", padx=5, pady=5)
        self.uuid_entry = ctk.CTkEntry(uuid_frame)
        self.uuid_entry.pack(side="left", fill="x", expand=True, padx=5, pady=5)
    
    def get_config(self):
        """获取Pstore设备配置
        
        Returns:
            dict: Pstore设备配置数据
        """
        return {
            "model": self.model_var.get(),
            "address": self.address_entry.get(),
            "type": self.type_var.get(),
            "size": self.size_entry.get(),
            "uuid": self.uuid_entry.get()
        }
