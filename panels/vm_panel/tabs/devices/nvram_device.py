import customtkinter as ctk
from components.base_tab import BaseConfigTab


class NVRAMDeviceTab(BaseConfigTab):
    """NVRAM设备配置标签页"""
    
    def __init__(self, parent, on_change_callback=None, **kwargs):
        """初始化NVRAM设备配置标签页
        
        Args:
            parent: 父窗口
            on_change_callback: 配置变更回调函数
        """
        super().__init__(parent, on_change_callback, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        """创建NVRAM设备配置界面"""
        # NVRAM配置
        nvram_frame = ctk.CTkFrame(self, corner_radius=8)
        nvram_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(nvram_frame, text="NVRAM配置:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=5)
        
        # 设备模型
        model_frame = ctk.CTkFrame(nvram_frame)
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
        address_frame = ctk.CTkFrame(nvram_frame)
        address_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(address_frame, text="设备地址:", width=100).pack(side="left", padx=5, pady=5)
        self.address_entry = ctk.CTkEntry(address_frame)
        self.address_entry.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        
        # NVRAM属性
        props_frame = ctk.CTkFrame(self, corner_radius=8)
        props_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(props_frame, text="NVRAM属性:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=5)
        
        # NVRAM文件路径
        file_frame = ctk.CTkFrame(props_frame)
        file_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(file_frame, text="NVRAM文件:", width=100).pack(side="left", padx=5, pady=5)
        self.file_entry = ctk.CTkEntry(file_frame)
        self.file_entry.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        
        # NVRAM模板
        template_frame = ctk.CTkFrame(props_frame)
        template_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(template_frame, text="NVRAM模板:", width=100).pack(side="left", padx=5, pady=5)
        self.template_entry = ctk.CTkEntry(template_frame)
        self.template_entry.pack(side="left", fill="x", expand=True, padx=5, pady=5)
    
    def get_config(self):
        """获取NVRAM设备配置
        
        Returns:
            dict: NVRAM设备配置数据
        """
        return {
            "model": self.model_var.get(),
            "address": self.address_entry.get(),
            "file": self.file_entry.get(),
            "template": self.template_entry.get()
        }
