import customtkinter as ctk
from components.base_tab import BaseConfigTab


class SharedMemoryDeviceTab(BaseConfigTab):
    """共享内存设备配置标签页"""

    def __init__(self, parent, on_change_callback=None, **kwargs):
        """初始化共享内存设备配置标签页

        Args:
            parent: 父窗口
            on_change_callback: 配置变更回调函数
        """
        super().__init__(parent, on_change_callback, **kwargs)
        self._create_widgets()

    def _create_widgets(self):
        """创建共享内存设备配置界面"""
        # 共享内存设备配置
        shmem_frame = ctk.CTkFrame(self, corner_radius=8)
        shmem_frame.pack(fill='x', padx=10, pady=5)

        ctk.CTkLabel(shmem_frame, text='共享内存设备配置:', font=ctk.CTkFont(weight='bold')).pack(
            anchor='w', padx=10, pady=5
        )

        # 设备模型
        model_frame = ctk.CTkFrame(shmem_frame)
        model_frame.pack(fill='x', padx=10, pady=5)
        ctk.CTkLabel(model_frame, text='设备模型:', width=100).pack(side='left', padx=5, pady=5)
        self.model_var = ctk.StringVar(value='ivshmem')
        model_options = ctk.CTkOptionMenu(
            model_frame, variable=self.model_var, values=['ivshmem', 'virtio']
        )
        model_options.pack(side='left', fill='x', expand=True, padx=5, pady=5)

        # 设备地址
        address_frame = ctk.CTkFrame(shmem_frame)
        address_frame.pack(fill='x', padx=10, pady=5)
        ctk.CTkLabel(address_frame, text='设备地址:', width=100).pack(side='left', padx=5, pady=5)
        self.address_entry = ctk.CTkEntry(address_frame)
        self.address_entry.pack(side='left', fill='x', expand=True, padx=5, pady=5)

        # 共享内存属性
        props_frame = ctk.CTkFrame(self, corner_radius=8)
        props_frame.pack(fill='x', padx=10, pady=5)

        ctk.CTkLabel(props_frame, text='共享内存属性:', font=ctk.CTkFont(weight='bold')).pack(
            anchor='w', padx=10, pady=5
        )

        # 共享内存大小
        size_frame = ctk.CTkFrame(props_frame)
        size_frame.pack(fill='x', padx=10, pady=5)
        ctk.CTkLabel(size_frame, text='内存大小:', width=100).pack(side='left', padx=5, pady=5)
        self.size_entry = ctk.CTkEntry(size_frame, placeholder_text='例如: 1024M')
        self.size_entry.pack(side='left', fill='x', expand=True, padx=5, pady=5)

        # 共享内存文件
        file_frame = ctk.CTkFrame(props_frame)
        file_frame.pack(fill='x', padx=10, pady=5)
        ctk.CTkLabel(file_frame, text='共享文件:', width=100).pack(side='left', padx=5, pady=5)
        self.file_entry = ctk.CTkEntry(file_frame)
        self.file_entry.pack(side='left', fill='x', expand=True, padx=5, pady=5)

        # 共享内存服务器
        server_frame = ctk.CTkFrame(props_frame)
        server_frame.pack(fill='x', padx=10, pady=5)
        ctk.CTkLabel(server_frame, text='服务器:', width=100).pack(side='left', padx=5, pady=5)
        self.server_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(server_frame, text='作为服务器', variable=self.server_var).pack(
            side='left', padx=5, pady=5
        )

    def get_config(self):
        """获取共享内存设备配置

        Returns:
            dict: 共享内存设备配置数据
        """
        return {
            'model': self.model_var.get(),
            'address': self.address_entry.get(),
            'size': self.size_entry.get(),
            'file': self.file_entry.get(),
            'server': self.server_var.get(),
        }
