import customtkinter as ctk
from components.base_tab import BaseConfigTab


class IOMMUDevicesTab(BaseConfigTab):
    """IOMMU设备配置标签页"""
    
    def __init__(self, parent, on_change_callback=None, **kwargs):
        """初始化IOMMU设备配置标签页
        
        Args:
            parent: 父窗口
            on_change_callback: 配置变更回调函数
        """
        super().__init__(parent, on_change_callback, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        """创建IOMMU设备配置界面"""
        # IOMMU设备配置
        iommu_frame = ctk.CTkFrame(self, corner_radius=8)
        iommu_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(iommu_frame, text="IOMMU设备配置:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=5)
        
        # 设备类型
        type_frame = ctk.CTkFrame(iommu_frame)
        type_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(type_frame, text="设备类型:", width=100).pack(side="left", padx=5, pady=5)
        self.type_var = ctk.StringVar(value="intel")
        type_options = ctk.CTkOptionMenu(
            type_frame,
            variable=self.type_var,
            values=["intel", "amd"]
        )
        type_options.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        
        # 设备地址
        address_frame = ctk.CTkFrame(iommu_frame)
        address_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(address_frame, text="设备地址:", width=100).pack(side="left", padx=5, pady=5)
        self.address_entry = ctk.CTkEntry(address_frame)
        self.address_entry.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        
        # IOMMU设备属性
        props_frame = ctk.CTkFrame(self, corner_radius=8)
        props_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(props_frame, text="IOMMU设备属性:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=5)
        
        # IOMMU模式
        mode_frame = ctk.CTkFrame(props_frame)
        mode_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(mode_frame, text="IOMMU模式:", width=100).pack(side="left", padx=5, pady=5)
        self.mode_var = ctk.StringVar(value="strict")
        mode_options = ctk.CTkOptionMenu(
            mode_frame,
            variable=self.mode_var,
            values=["strict", "relaxed"]
        )
        mode_options.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        
        # IOMMU设备 UUID
        uuid_frame = ctk.CTkFrame(props_frame)
        uuid_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(uuid_frame, text="设备UUID:", width=100).pack(side="left", padx=5, pady=5)
        self.uuid_entry = ctk.CTkEntry(uuid_frame)
        self.uuid_entry.pack(side="left", fill="x", expand=True, padx=5, pady=5)
    
    def get_config(self):
        """获取IOMMU设备配置
        
        Returns:
            dict: IOMMU设备配置数据
        """
        return {
            "type": self.type_var.get(),
            "address": self.address_entry.get(),
            "mode": self.mode_var.get(),
            "uuid": self.uuid_entry.get()
        }
