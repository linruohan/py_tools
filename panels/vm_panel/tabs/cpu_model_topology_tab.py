"""CPU 模型与拓扑配置 Tab - CPU 模型、特性、缓存配置."""

from typing import ClassVar

import customtkinter as ctk

from components.base_tab import BaseConfigTab
from components.inner_tab_panel import InnerTabPanel
from utils.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class CPUModelSubTab(BaseConfigTab):
    """CPU 模型子 Tab."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, on_change_callback, **kwargs)
        self._pending_config = {}  # 保存尚未加载的配置

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

    def load_config(self, config: dict) -> None:
        """加载配置数据."""
        if 'mode' in config:
            self.cpu_mode.set(config['mode'])
        if 'match' in config:
            self.cpu_match.set(config['match'])
        if 'model' in config:
            self.cpu_model.delete(0, 'end')
            self.cpu_model.insert(0, config['model'])
        if 'vendor' in config:
            self.cpu_vendor.delete(0, 'end')
            self.cpu_vendor.insert(0, config['vendor'])
        if 'vendor_id' in config:
            self.vendor_id.delete(0, 'end')
            self.vendor_id.insert(0, config['vendor_id'])
        if 'fallback' in config:
            self.fallback.set(config['fallback'])
        if 'migratable' in config:
            self.migratable.set(config['migratable'])
        if 'check' in config:
            self.check.set(config['check'])


class CPUFeatureSubTab(BaseConfigTab):
    """CPU 特性子 Tab."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        self.features_list = []
        self.feature_widgets = {}
        super().__init__(master, on_change_callback, **kwargs)

    def _init_ui(self) -> None:
        """初始化界面."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # 顶部框架:添加新 feature
        top_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        top_frame.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
        top_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(top_frame, text='CPU 特性', font=CTK_FONT_BOLD, text_color='#ff9800').grid(
            row=0, column=0, columnspan=5, padx=10, pady=5, sticky='w'
        )

        ctk.CTkLabel(top_frame, text='特性名:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.feature_name = ctk.CTkEntry(top_frame, placeholder_text='lahf_lm, pcid...', width=150)
        self.feature_name.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.feature_name.bind('<KeyRelease>', lambda e: self._on_enter_key(e))

        ctk.CTkLabel(top_frame, text='策略:', font=CTK_FONT_MAIN, width=60, anchor='w').grid(
            row=1, column=2, padx=10, pady=5, sticky='w'
        )
        self.feature_policy = ctk.CTkOptionMenu(
            top_frame,
            values=['require', 'optional', 'force', 'disable', 'forbid'],
            width=100,
            font=CTK_FONT_SMALL,
        )
        self.feature_policy.set('require')
        self.feature_policy.grid(row=1, column=3, padx=5, pady=5, sticky='w')

        add_btn = ctk.CTkButton(
            top_frame,
            text='添加',
            command=self._add_feature,
            fg_color='#00bcd4',
            hover_color='#0097a7',
            width=70,
            font=CTK_FONT_SMALL,
        )
        add_btn.grid(row=1, column=4, padx=5, pady=5)

        # 底部框架:显示已添加的 feature 列表
        bottom_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        bottom_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
        bottom_frame.grid_columnconfigure(0, weight=1)
        bottom_frame.grid_rowconfigure(0, weight=1)

        self.list_frame = ctk.CTkScrollableFrame(bottom_frame, fg_color='transparent')
        self.list_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        self.list_frame.grid_columnconfigure(0, weight=1)

        self._refresh_feature_list()

    def _on_enter_key(self, event):
        """按回车键添加 feature."""
        if event.keysym == 'Return':
            self._add_feature()

    def _add_feature(self):
        """添加 CPU 特性."""
        name = self.feature_name.get().strip()
        if not name:
            return

        # 检查是否已存在
        for feat in self.features_list:
            if feat['name'] == name:
                self.feature_name.delete(0, 'end')
                return

        self.features_list.append(
            {
                'name': name,
                'policy': self.feature_policy.get(),
            }
        )
        self.feature_name.delete(0, 'end')
        self._refresh_feature_list()
        self._trigger_change()

    def _remove_feature(self, index: int):
        """删除指定索引的 CPU 特性."""
        if 0 <= index < len(self.features_list):
            del self.features_list[index]
            self._refresh_feature_list()
            self._trigger_change()

    def _refresh_feature_list(self):
        """刷新 feature 列表显示."""
        # 清除所有现有控件
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        if not self.features_list:
            ctk.CTkLabel(
                self.list_frame,
                text='暂无已添加的特性',
                font=CTK_FONT_SMALL,
                text_color='#888888'
            ).grid(row=0, column=0, padx=10, pady=10, sticky='w')
            return

        # 显示每个 feature 及其删除按钮
        for i, feat in enumerate(self.features_list):
            row = i // 3  # 每行 3 个
            col = (i % 3) * 3  # 每个 feature 占 3 列

            # 创建 frame 包裹单个 feature
            feat_frame = ctk.CTkFrame(self.list_frame, fg_color='#2a2a2a', corner_radius=4)
            feat_frame.grid(row=row, column=col, padx=5, pady=5, sticky='ew')
            self.list_frame.grid_columnconfigure(col, weight=1)

            # 显示 feature 名和策略
            feat_text = f"{feat['name']} ({feat['policy']})"
            ctk.CTkLabel(
                feat_frame,
                text=feat_text,
                font=CTK_FONT_SMALL,
                text_color='#64b5f6'
            ).pack(side='left', padx=5, pady=2)

            # 删除按钮
            def make_remove_handler(idx):
                return lambda idx=idx: self._remove_feature(idx)

            del_btn = ctk.CTkButton(
                feat_frame,
                text='X',
                width=24,
                height=20,
                fg_color='#f44336',
                hover_color='#d32f2f',
                font=CTK_FONT_SMALL,
                command=make_remove_handler(i)
            )
            del_btn.pack(side='right', padx=2, pady=2)

    def get_config(self) -> dict:
        """获取配置数据."""
        return {
            'features': self.features_list.copy(),
        }

    def load_config(self, config: dict) -> None:
        """加载配置数据."""
        self.features_list = config.get('features', []).copy()
        self._refresh_feature_list()

class CPUCacheSubTab(BaseConfigTab):
    """CPU 缓存子 Tab."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, on_change_callback, **kwargs)

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

    def load_config(self, config: dict) -> None:
        """加载配置数据."""
        cache = config.get('cache', {})
        if 'level' in cache:
            self.cache_level.set(str(cache['level']))
        if 'mode' in cache:
            self.cache_mode.set(cache['mode'])

        maxphysaddr = config.get('maxphysaddr', {})
        if 'mode' in maxphysaddr:
            self.physaddr_mode.set(maxphysaddr['mode'])
        if 'bits' in maxphysaddr:
            self.physaddr_bits.delete(0, 'end')
            self.physaddr_bits.insert(0, maxphysaddr['bits'])
        if 'limit' in maxphysaddr:
            self.physaddr_limit.delete(0, 'end')
            self.physaddr_limit.insert(0, maxphysaddr['limit'])


class CPUModelTopologyTab(BaseConfigTab):
    """CPU 模型与拓扑配置 Tab."""

    SUB_TABS_CONFIG: ClassVar[dict] = {
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
        super().__init__(master, on_change_callback, **kwargs)

        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 包装 InnerTabPanel 的_switch_tab 方法
        original_switch = InnerTabPanel._switch_tab
        def wrapped_switch(self_inner, *args, **kwargs):
            original_switch(self_inner, *args, **kwargs)
            # Tab 切换后尝试加载配置
            if hasattr(self, '_pending_config') and args[0] in self._pending_config:
                tab_instance = self_inner.get_tab_instance(args[0])
                if tab_instance and hasattr(tab_instance, 'load_config'):
                    tab_instance.load_config(self._pending_config[args[0]])

        InnerTabPanel._switch_tab = wrapped_switch

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
    def load_config(self, config: dict) -> None:
        """加载配置数据到各个子 Tab."""
        # config 格式:{'model': {...}, 'feature': {...}, 'cache': {...}}
        self._pending_config = config
        for tab_key, tab_data in config.items():
            tab_instance = self.inner_panel.get_tab_instance(tab_key)
            if tab_instance and hasattr(tab_instance, 'load_config'):
                tab_instance.load_config(tab_data)

