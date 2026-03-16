import customtkinter as ctk
from components.base_tab import BaseConfigTab


class CryptoTab(BaseConfigTab):
    """Crypto设备配置标签页"""
    
    def __init__(self, parent, on_change_callback=None, **kwargs):
        """初始化Crypto设备配置标签页
        
        Args:
            parent: 父窗口
            on_change_callback: 配置变更回调函数
        """
        super().__init__(parent, on_change_callback, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        """创建Crypto设备配置界面"""
        # Crypto设备配置
        crypto_frame = ctk.CTkFrame(self, corner_radius=8)
        crypto_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(crypto_frame, text="Crypto设备配置:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=5)
        
        # 设备模型
        model_frame = ctk.CTkFrame(crypto_frame)
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
        address_frame = ctk.CTkFrame(crypto_frame)
        address_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(address_frame, text="设备地址:", width=100).pack(side="left", padx=5, pady=5)
        self.address_entry = ctk.CTkEntry(address_frame)
        self.address_entry.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        
        # Crypto设备属性
        props_frame = ctk.CTkFrame(self, corner_radius=8)
        props_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(props_frame, text="Crypto设备属性:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=5)
        
        # 后端类型
        backend_frame = ctk.CTkFrame(props_frame)
        backend_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(backend_frame, text="后端类型:", width=100).pack(side="left", padx=5, pady=5)
        self.backend_var = ctk.StringVar(value="passthrough")
        backend_options = ctk.CTkOptionMenu(
            backend_frame,
            variable=self.backend_var,
            values=["passthrough", "emulated"]
        )
        backend_options.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        
        # 后端设备
        backend_dev_frame = ctk.CTkFrame(props_frame)
        backend_dev_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(backend_dev_frame, text="后端设备:", width=100).pack(side="left", padx=5, pady=5)
        self.backend_dev_entry = ctk.CTkEntry(backend_dev_frame, placeholder_text="例如: /dev/crypto")
        self.backend_dev_entry.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        
        # Crypto设备 UUID
        uuid_frame = ctk.CTkFrame(props_frame)
        uuid_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(uuid_frame, text="设备UUID:", width=100).pack(side="left", padx=5, pady=5)
        self.uuid_entry = ctk.CTkEntry(uuid_frame)
        self.uuid_entry.pack(side="left", fill="x", expand=True, padx=5, pady=5)
    
    def get_config(self):
        """获取Crypto设备配置
        
        Returns:
            dict: Crypto设备配置数据
        """
        return {
            "model": self.model_var.get(),
            "address": self.address_entry.get(),
            "backend": self.backend_var.get(),
            "backend_device": self.backend_dev_entry.get(),
            "uuid": self.uuid_entry.get()
        }
