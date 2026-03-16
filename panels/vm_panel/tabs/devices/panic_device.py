import customtkinter as ctk
from components.base_tab import BaseConfigTab


class PanicDeviceTab(BaseConfigTab):
    """Panic设备配置标签页"""
    
    def __init__(self, parent, on_change_callback=None, **kwargs):
        """初始化Panic设备配置标签页
        
        Args:
            parent: 父窗口
            on_change_callback: 配置变更回调函数
        """
        super().__init__(parent, on_change_callback, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        """创建Panic设备配置界面"""
        # Panic设备配置
        panic_frame = ctk.CTkFrame(self, corner_radius=8)
        panic_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(panic_frame, text="Panic设备配置:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=5)
        
        # 设备模型
        model_frame = ctk.CTkFrame(panic_frame)
        model_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(model_frame, text="设备模型:", width=100).pack(side="left", padx=5, pady=5)
        self.model_var = ctk.StringVar(value="virtio")
        model_options = ctk.CTkOptionMenu(
            model_frame,
            variable=self.model_var,
            values=["virtio", "ivshmem"]
        )
        model_options.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        
        # 设备地址
        address_frame = ctk.CTkFrame(panic_frame)
        address_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(address_frame, text="设备地址:", width=100).pack(side="left", padx=5, pady=5)
        self.address_entry = ctk.CTkEntry(address_frame)
        self.address_entry.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        
        # Panic设备属性
        props_frame = ctk.CTkFrame(self, corner_radius=8)
        props_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(props_frame, text="Panic设备属性:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=5)
        
        # Panic动作
        action_frame = ctk.CTkFrame(props_frame)
        action_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(action_frame, text="Panic动作:", width=100).pack(side="left", padx=5, pady=5)
        self.action_var = ctk.StringVar(value="pause")
        action_options = ctk.CTkOptionMenu(
            action_frame,
            variable=self.action_var,
            values=["pause", "reset", "shutdown", "none"]
        )
        action_options.pack(side="left", fill="x", expand=True, padx=5, pady=5)
    
    def get_config(self):
        """获取Panic设备配置
        
        Returns:
            dict: Panic设备配置数据
        """
        return {
            "model": self.model_var.get(),
            "address": self.address_entry.get(),
            "action": self.action_var.get()
        }
