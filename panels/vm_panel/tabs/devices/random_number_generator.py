import customtkinter as ctk

from components.base_tab import BaseConfigTab


class RandomNumberGeneratorTab(BaseConfigTab):
    """随机数生成器设备配置标签页"""

    def __init__(self, parent, on_change_callback=None, **kwargs):
        """初始化随机数生成器设备配置标签页

        Args:
            parent: 父窗口
            on_change_callback: 配置变更回调函数
        """
        super().__init__(parent, on_change_callback, **kwargs)
        self._create_widgets()

    def _create_widgets(self):
        """创建随机数生成器设备配置界面"""
        # 随机数生成器配置
        rng_frame = ctk.CTkFrame(self, corner_radius=8)
        rng_frame.pack(fill='x', padx=10, pady=5)

        ctk.CTkLabel(rng_frame, text='随机数生成器配置:', font=ctk.CTkFont(weight='bold')).pack(
            anchor='w', padx=10, pady=5
        )

        # 设备模型
        model_frame = ctk.CTkFrame(rng_frame)
        model_frame.pack(fill='x', padx=10, pady=5)
        ctk.CTkLabel(model_frame, text='设备模型:', width=100).pack(side='left', padx=5, pady=5)
        self.model_var = ctk.StringVar(value='virtio')
        model_options = ctk.CTkOptionMenu(
            model_frame, variable=self.model_var, values=['virtio', 'ivshmem']
        )
        model_options.pack(side='left', fill='x', expand=True, padx=5, pady=5)

        # 设备地址
        address_frame = ctk.CTkFrame(rng_frame)
        address_frame.pack(fill='x', padx=10, pady=5)
        ctk.CTkLabel(address_frame, text='设备地址:', width=100).pack(side='left', padx=5, pady=5)
        self.address_entry = ctk.CTkEntry(address_frame)
        self.address_entry.pack(side='left', fill='x', expand=True, padx=5, pady=5)

        # 随机数生成器属性
        props_frame = ctk.CTkFrame(self, corner_radius=8)
        props_frame.pack(fill='x', padx=10, pady=5)

        ctk.CTkLabel(props_frame, text='随机数生成器属性:', font=ctk.CTkFont(weight='bold')).pack(
            anchor='w', padx=10, pady=5
        )

        # 后端类型
        backend_frame = ctk.CTkFrame(props_frame)
        backend_frame.pack(fill='x', padx=10, pady=5)
        ctk.CTkLabel(backend_frame, text='后端类型:', width=100).pack(side='left', padx=5, pady=5)
        self.backend_var = ctk.StringVar(value='random')
        backend_options = ctk.CTkOptionMenu(
            backend_frame, variable=self.backend_var, values=['random', 'urandom', 'egd']
        )
        backend_options.pack(side='left', fill='x', expand=True, padx=5, pady=5)

        # EGD路径 (当后端为egd时使用)
        egd_frame = ctk.CTkFrame(props_frame)
        egd_frame.pack(fill='x', padx=10, pady=5)
        ctk.CTkLabel(egd_frame, text='EGD路径:', width=100).pack(side='left', padx=5, pady=5)
        self.egd_path_entry = ctk.CTkEntry(egd_frame)
        self.egd_path_entry.pack(side='left', fill='x', expand=True, padx=5, pady=5)

    def get_config(self):
        """获取随机数生成器设备配置

        Returns:
            dict: 随机数生成器设备配置数据
        """
        return {
            'model': self.model_var.get(),
            'address': self.address_entry.get(),
            'backend': self.backend_var.get(),
            'egd_path': self.egd_path_entry.get(),
        }
