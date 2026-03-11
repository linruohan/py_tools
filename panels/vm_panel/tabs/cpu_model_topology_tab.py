"""CPU 模型与拓扑配置 Tab - CPU 模型、特性、缓存配置."""

import customtkinter as ctk

from ..inner_tab_panel import InnerTabPanel
from ..styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class CPUModelSubTab(ctk.CTkFrame):
    """CPU 模型子 Tab."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent')
        self.on_change_callback = on_change_callback

        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        left_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        left_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        left_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(left_frame, text='CPU 模型', font=CTK_FONT_BOLD, text_color='#64b5f6').grid(
            row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
        )

        ctk.CTkLabel(left_frame, text='模式:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.cpu_mode = ctk.CTkOptionMenu(
            left_frame,
            values=['custom', 'host-model', 'host-passthrough', 'maximum'],
            width=140,
            font=CTK_FONT_SMALL,
        )
        self.cpu_mode.set('host-model')
        self.cpu_mode.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.cpu_mode.configure(command=self._trigger_change)

        ctk.CTkLabel(left_frame, text='匹配:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.cpu_match = ctk.CTkOptionMenu(
            left_frame,
            values=['exact', 'minimum', 'strict'],
            width=100,
            font=CTK_FONT_SMALL,
        )
        self.cpu_match.set('exact')
        self.cpu_match.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.cpu_match.configure(command=self._trigger_change)

        ctk.CTkLabel(left_frame, text='模型:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=3, column=0, padx=10, pady=5, sticky='w'
        )
        self.cpu_model = ctk.CTkEntry(left_frame, placeholder_text='core2duo, qemu64...', width=150)
        self.cpu_model.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        self.cpu_model.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(left_frame, text='厂商:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=4, column=0, padx=10, pady=5, sticky='w'
        )
        self.cpu_vendor = ctk.CTkEntry(left_frame, placeholder_text='Intel, AMD...', width=150)
        self.cpu_vendor.grid(row=4, column=1, padx=5, pady=5, sticky='w')
        self.cpu_vendor.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(left_frame, text='Vendor ID:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=5, column=0, padx=10, pady=5, sticky='w'
        )
        self.vendor_id = ctk.CTkEntry(left_frame, placeholder_text='12字符', width=150)
        self.vendor_id.grid(row=5, column=1, padx=5, pady=5, sticky='w')
        self.vendor_id.bind('<KeyRelease>', lambda e: self._trigger_change())

        right_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        right_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        right_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(right_frame, text='迁移选项', font=CTK_FONT_BOLD, text_color='#4caf50').grid(
            row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
        )

        ctk.CTkLabel(right_frame, text='Fallback:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.fallback = ctk.CTkOptionMenu(
            right_frame,
            values=['allow', 'forbid'],
            width=100,
            font=CTK_FONT_SMALL,
        )
        self.fallback.set('allow')
        self.fallback.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.fallback.configure(command=self._trigger_change)

        ctk.CTkLabel(
            right_frame, text='Migratable:', font=CTK_FONT_MAIN, width=100, anchor='w'
        ).grid(row=2, column=0, padx=10, pady=5, sticky='w')
        self.migratable = ctk.CTkOptionMenu(
            right_frame,
            values=['on', 'off'],
            width=80,
            font=CTK_FONT_SMALL,
        )
        self.migratable.set('on')
        self.migratable.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.migratable.configure(command=self._trigger_change)

        ctk.CTkLabel(right_frame, text='检查:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=3, column=0, padx=10, pady=5, sticky='w'
        )
        self.check = ctk.CTkOptionMenu(
            right_frame,
            values=['none', 'partial', 'full'],
            width=100,
            font=CTK_FONT_SMALL,
        )
        self.check.set('partial')
        self.check.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        self.check.configure(command=self._trigger_change)

    def _trigger_change(self):
        """触发变化回调."""
        if self.on_change_callback:
            self.on_change_callback()

    def get_config(self) -> dict:
        """获取配置数据."""
        return {
            'mode': self.cpu_mode.get(),
            'match': self.cpu_match.get(),
            'model': self.cpu_model.get().strip(),
            'vendor': self.cpu_vendor.get().strip(),
            'vendor_id': self.vendor_id.get().strip(),
            'fallback': self.fallback.get(),
            'migratable': self.migratable.get(),
            'check': self.check.get(),
        }


class CPUFeatureSubTab(ctk.CTkFrame):
    """CPU 特性子 Tab."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent')
        self.on_change_callback = on_change_callback
        self.features_list = []

        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面."""
        self.grid_columnconfigure(0, weight=1)

        frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(frame, text='CPU 特性', font=CTK_FONT_BOLD, text_color='#ff9800').grid(
            row=0, column=0, columnspan=4, padx=10, pady=5, sticky='w'
        )

        ctk.CTkLabel(frame, text='特性名:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.feature_name = ctk.CTkEntry(frame, placeholder_text='lahf_lm, pcid...', width=150)
        self.feature_name.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.feature_name.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(frame, text='策略:', font=CTK_FONT_MAIN, width=60, anchor='w').grid(
            row=1, column=2, padx=10, pady=5, sticky='w'
        )
        self.feature_policy = ctk.CTkOptionMenu(
            frame,
            values=['require', 'optional', 'force', 'disable', 'forbid'],
            width=100,
            font=CTK_FONT_SMALL,
        )
        self.feature_policy.set('require')
        self.feature_policy.grid(row=1, column=3, padx=5, pady=5, sticky='w')
        self.feature_policy.configure(command=self._trigger_change)

        add_btn = ctk.CTkButton(
            frame,
            text='添加',
            command=self._add_feature,
            fg_color='#00bcd4',
            hover_color='#0097a7',
            width=70,
            font=CTK_FONT_SMALL,
        )
        add_btn.grid(row=1, column=4, padx=5, pady=5)

        self.features_display = ctk.CTkLabel(
            frame, text='', font=CTK_FONT_SMALL, text_color='#aaaaaa', anchor='w'
        )
        self.features_display.grid(row=2, column=0, columnspan=5, padx=10, pady=5, sticky='w')

    def _add_feature(self):
        """添加 CPU 特性."""
        name = self.feature_name.get().strip()
        if name:
            self.features_list.append(
                {
                    'name': name,
                    'policy': self.feature_policy.get(),
                }
            )
            self.features_display.configure(
                text=f'已添加: {", ".join([f["name"] for f in self.features_list])}'
            )
            self.feature_name.delete(0, 'end')
            self._trigger_change()

    def _trigger_change(self):
        """触发变化回调."""
        if self.on_change_callback:
            self.on_change_callback()

    def get_config(self) -> dict:
        """获取配置数据."""
        return {
            'features': self.features_list.copy(),
        }


class CPUCacheSubTab(ctk.CTkFrame):
    """CPU 缓存子 Tab."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent')
        self.on_change_callback = on_change_callback

        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        left_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        left_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        left_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(left_frame, text='CPU 缓存', font=CTK_FONT_BOLD, text_color='#9c27b0').grid(
            row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
        )

        ctk.CTkLabel(left_frame, text='缓存级别:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.cache_level = ctk.CTkOptionMenu(
            left_frame,
            values=['1', '2', '3'],
            width=80,
            font=CTK_FONT_SMALL,
        )
        self.cache_level.set('3')
        self.cache_level.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.cache_level.configure(command=self._trigger_change)

        ctk.CTkLabel(left_frame, text='模式:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.cache_mode = ctk.CTkOptionMenu(
            left_frame,
            values=['emulate', 'passthrough', 'disable'],
            width=120,
            font=CTK_FONT_SMALL,
        )
        self.cache_mode.set('emulate')
        self.cache_mode.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.cache_mode.configure(command=self._trigger_change)

        right_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        right_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        right_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(right_frame, text='物理地址', font=CTK_FONT_BOLD, text_color='#7986cb').grid(
            row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
        )

        ctk.CTkLabel(right_frame, text='模式:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.physaddr_mode = ctk.CTkOptionMenu(
            right_frame,
            values=['passthrough', 'emulate'],
            width=120,
            font=CTK_FONT_SMALL,
        )
        self.physaddr_mode.set('passthrough')
        self.physaddr_mode.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.physaddr_mode.configure(command=self._trigger_change)

        ctk.CTkLabel(right_frame, text='位数:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.physaddr_bits = ctk.CTkEntry(right_frame, placeholder_text='42', width=80)
        self.physaddr_bits.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.physaddr_bits.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(right_frame, text='限制:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=3, column=0, padx=10, pady=5, sticky='w'
        )
        self.physaddr_limit = ctk.CTkEntry(right_frame, placeholder_text='39', width=80)
        self.physaddr_limit.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        self.physaddr_limit.bind('<KeyRelease>', lambda e: self._trigger_change())

    def _trigger_change(self):
        """触发变化回调."""
        if self.on_change_callback:
            self.on_change_callback()

    def get_config(self) -> dict:
        """获取配置数据."""
        return {
            'cache': {
                'level': int(self.cache_level.get()),
                'mode': self.cache_mode.get(),
            },
            'maxphysaddr': {
                'mode': self.physaddr_mode.get(),
                'bits': self.physaddr_bits.get().strip(),
                'limit': self.physaddr_limit.get().strip(),
            },
        }


class CPUModelTopologyTab(ctk.CTkFrame):
    """CPU 模型与拓扑配置 Tab."""

    SUB_TABS_CONFIG = {
        'model': {
            'name': 'CPU 模型',
            'class': CPUModelSubTab,
            'default': True,
        },
        'feature': {
            'name': 'CPU 特性',
            'class': CPUFeatureSubTab,
            'default': False,
        },
        'cache': {
            'name': 'CPU 缓存',
            'class': CPUCacheSubTab,
            'default': False,
        },
    }

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent')
        self.on_change_callback = on_change_callback

        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.inner_panel = InnerTabPanel(
            self,
            tabs_config=self.SUB_TABS_CONFIG,
            on_change_callback=self.on_change_callback,
        )
        self.inner_panel.grid(row=0, column=0, sticky='nsew')

    def get_config(self) -> dict:
        """获取配置数据."""
        return self.inner_panel.collect_data()

    def to_xml(self) -> dict:
        """生成XML配置字典."""
        return {'cpu_model_topology': self.get_config()}
