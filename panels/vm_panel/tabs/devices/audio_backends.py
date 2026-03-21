import customtkinter as ctk
from components.base_tab import BaseConfigTab


class AudioBackendsTab(BaseConfigTab):
    """音频后端配置标签页"""

    def __init__(self, parent, on_change_callback=None, **kwargs):
        """初始化音频后端配置标签页

        Args:
            parent: 父窗口
            on_change_callback: 配置变更回调函数
        """
        super().__init__(parent, on_change_callback, **kwargs)
        self._create_widgets()

    def _create_widgets(self):
        """创建音频后端配置界面"""
        # 音频后端配置
        backend_frame = ctk.CTkFrame(self, corner_radius=8)
        backend_frame.pack(fill='x', padx=10, pady=5)

        ctk.CTkLabel(backend_frame, text='音频后端类型:', font=ctk.CTkFont(weight='bold')).pack(
            anchor='w', padx=10, pady=5
        )

        self.backend_types = ctk.CTkOptionMenu(
            backend_frame, values=['默认', 'ALSA', 'PulseAudio', 'SPICE', 'Dummy']
        )
        self.backend_types.pack(fill='x', padx=10, pady=5)

        # 音频后端属性
        backend_props_frame = ctk.CTkFrame(self, corner_radius=8)
        backend_props_frame.pack(fill='x', padx=10, pady=5)

        ctk.CTkLabel(
            backend_props_frame, text='音频后端属性:', font=ctk.CTkFont(weight='bold')
        ).pack(anchor='w', padx=10, pady=5)

        # 设备名称
        name_frame = ctk.CTkFrame(backend_props_frame)
        name_frame.pack(fill='x', padx=10, pady=5)
        ctk.CTkLabel(name_frame, text='设备名称:', width=100).pack(side='left', padx=5, pady=5)
        self.name_entry = ctk.CTkEntry(name_frame)
        self.name_entry.pack(side='left', fill='x', expand=True, padx=5, pady=5)

        # 音频后端选项
        options_frame = ctk.CTkFrame(backend_props_frame)
        options_frame.pack(fill='x', padx=10, pady=5)
        ctk.CTkLabel(options_frame, text='后端选项:', width=100).pack(side='left', padx=5, pady=5)
        self.options_entry = ctk.CTkEntry(options_frame)
        self.options_entry.pack(side='left', fill='x', expand=True, padx=5, pady=5)

    def get_config(self):
        """获取音频后端配置

        Returns:
            dict: 音频后端配置数据
        """
        return {
            'backend_type': self.backend_types.get(),
            'name': self.name_entry.get(),
            'options': self.options_entry.get(),
        }
