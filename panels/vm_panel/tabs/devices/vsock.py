import customtkinter as ctk
from components.base_tab import BaseConfigTab


class VsockTab(BaseConfigTab):
    """Vsock设备配置标签页"""
    
    def __init__(self, parent, on_change_callback=None, **kwargs):
        """初始化Vsock设备配置标签页
        
        Args:
            parent: 父窗口
            on_change_callback: 配置变更回调函数
        """
        super().__init__(parent, on_change_callback, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        """创建Vsock设备配置界面"""
        # Vsock设备配置
        vsock_frame = ctk.CTkFrame(self, corner_radius=8)
        vsock_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(vsock_frame, text="Vsock设备配置:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=5)
        
        # 设备模型
        model_frame = ctk.CTkFrame(vsock_frame)
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
        address_frame = ctk.CTkFrame(vsock_frame)
        address_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(address_frame, text="设备地址:", width=100).pack(side="left", padx=5, pady=5)
        self.address_entry = ctk.CTkEntry(address_frame)
        self.address_entry.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        
        # Vsock设备属性
        props_frame = ctk.CTkFrame(self, corner_radius=8)
        props_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(props_frame, text="Vsock设备属性:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=5)
        
        # CID (Context ID)
        cid_frame = ctk.CTkFrame(props_frame)
        cid_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(cid_frame, text="CID:", width=100).pack(side="left", padx=5, pady=5)
        self.cid_entry = ctk.CTkEntry(cid_frame, placeholder_text="例如: 3")
        self.cid_entry.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        
        # Vsock设备 UUID
        uuid_frame = ctk.CTkFrame(props_frame)
        uuid_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(uuid_frame, text="设备UUID:", width=100).pack(side="left", padx=5, pady=5)
        self.uuid_entry = ctk.CTkEntry(uuid_frame)
        self.uuid_entry.pack(side="left", fill="x", expand=True, padx=5, pady=5)
    
    def get_config(self):
        """获取Vsock设备配置
        
        Returns:
            dict: Vsock设备配置数据
        """
        return {
            "model": self.model_var.get(),
            "address": self.address_entry.get(),
            "cid": self.cid_entry.get(),
            "uuid": self.uuid_entry.get()
        }
