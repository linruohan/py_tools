"""CPU 模型与拓扑配置 Tab - 参考系统启动 Tab 布局重构."""

from typing import ClassVar

import customtkinter as ctk

from components.base_tab import SectionConfig, StandardConfigTab


class CPUModelTopologyTab(StandardConfigTab):
    """CPU 模型与拓扑配置 Tab - 使用紧凑布局."""

    SECTIONS: ClassVar[dict] = {
        'cpu_model': SectionConfig(
            title='CPU 模型',
            fields=[],  # 通过自定义代码创建 UI
            color='#64b5f6',
        ),
        'topology': SectionConfig(
            title='CPU 拓扑',
            fields=[],  # 通过自定义代码创建 UI
            color='#4caf50',
        ),
        'features': SectionConfig(
            title='CPU 特性',
            fields=[],  # 通过自定义代码创建 UI
            color='#ff9800',
        ),
        'cache': SectionConfig(
            title='CPU 缓存',
            fields=[],  # 通过自定义代码创建 UI
            color='#9c27b0',
        ),
    }

    def __init__(self, master, on_change_callback=None, **kwargs):
        self.features_list = []
        super().__init__(master, on_change_callback, **kwargs)

    def _init_sections_ui(self) -> None:
        """初始化基于 Sections 的 UI，添加自定义布局."""
        super()._init_sections_ui()

        # === CPU 模型部分 ===
        model_frame = self.section_frames['cpu_model']
        model_row = 1

        # 基本信息行
        ctk.CTkLabel(model_frame, text='基本信息', font=('', 11), text_color='#FFD93D').grid(
            row=model_row, column=0, columnspan=2, padx=10, pady=3, sticky='w'
        )
        model_row += 1

        # mode、match、check、migratable 放一行
        self._create_cpu_model_basic_row(model_frame, model_row)
        model_row += 1

        # model、fallback、vendor、vendor_id 放一行
        self._create_model_vendor_row(model_frame, model_row)
        model_row += 1

        self.section_rows['cpu_model'] = model_row

        # === CPU 拓扑部分 ===
        topology_frame = self.section_frames['topology']
        topology_row = 1

        ctk.CTkLabel(topology_frame, text='拓扑结构', font=('', 11), text_color='#FFD93D').grid(
            row=topology_row, column=0, columnspan=2, padx=10, pady=3, sticky='w'
        )
        topology_row += 1

        # sockets、dies、clusters、cores 放一行
        self._create_topology_row1(topology_frame, topology_row)
        topology_row += 1

        # threads 单独一行（带说明）
        self._create_threads_row(topology_frame, topology_row)
        topology_row += 1

        self.section_rows['topology'] = topology_row

        # === CPU 特性部分 ===
        features_frame = self.section_frames['features']
        features_row = 1

        # 添加新 feature 的行
        self._create_feature_add_row(features_frame, features_row)
        features_row += 1

        # feature 列表显示区域
        self.features_display_frame = ctk.CTkFrame(features_frame, fg_color='transparent')
        self.features_display_frame.grid(
            row=features_row, column=0, columnspan=2, padx=10, pady=3, sticky='ew'
        )
        features_row += 1

        self.section_rows['features'] = features_row

        # === CPU 缓存部分 ===
        cache_frame = self.section_frames['cache']
        cache_row = 1

        ctk.CTkLabel(cache_frame, text='缓存配置', font=('', 11), text_color='#FFD93D').grid(
            row=cache_row, column=0, columnspan=2, padx=10, pady=3, sticky='w'
        )
        cache_row += 1

        # cache_level、cache_mode 放一行
        self._create_cache_basic_row(cache_frame, cache_row)
        cache_row += 1

        ctk.CTkLabel(cache_frame, text='物理地址', font=('', 11), text_color='#FFD93D').grid(
            row=cache_row, column=0, columnspan=2, padx=10, pady=3, sticky='w'
        )
        cache_row += 1

        # physaddr_mode、physaddr_bits、physaddr_limit 放一行
        self._create_physaddr_row(cache_frame, cache_row)
        cache_row += 1

        self.section_rows['cache'] = cache_row

    def _create_cpu_model_basic_row(self, parent: ctk.CTkFrame, row: int) -> None:
        """创建 CPU 模型基本信息行：mode、match、check、migratable."""
        frame = ctk.CTkFrame(parent, fg_color='transparent')
        frame.grid(row=row, column=0, columnspan=2, padx=10, pady=3, sticky='w')

        # mode
        ctk.CTkLabel(frame, text='mode:', font=('', 10), width=45, anchor='w').pack(
            side='left', padx=(0, 2)
        )
        self.cpu_mode = ctk.CTkOptionMenu(
            frame,
            values=['custom', 'host-model', 'host-passthrough', 'maximum'],
            width=110,
            font=('', 10),
            command=self._on_mode_change,
        )
        self.cpu_mode.set('host-model')
        self.cpu_mode.pack(side='left', padx=2)

        # match
        ctk.CTkLabel(frame, text='match:', font=('', 10), width=45, anchor='w').pack(
            side='left', padx=(10, 2)
        )
        self.cpu_match = ctk.CTkOptionMenu(
            frame, values=['exact', 'minimum', 'strict'], width=70, font=('', 10)
        )
        self.cpu_match.set('exact')
        self.cpu_match.pack(side='left', padx=2)
        self.cpu_match.configure(command=self._trigger_change)

        # check
        ctk.CTkLabel(frame, text='check:', font=('', 10), width=40, anchor='w').pack(
            side='left', padx=(10, 2)
        )
        self.cpu_check = ctk.CTkOptionMenu(
            frame, values=['none', 'partial', 'full'], width=65, font=('', 10)
        )
        self.cpu_check.set('none')
        self.cpu_check.pack(side='left', padx=2)
        self.cpu_check.configure(command=self._trigger_change)

        # migratable
        ctk.CTkLabel(frame, text='migratable:', font=('', 10), width=60, anchor='w').pack(
            side='left', padx=(10, 2)
        )
        self.cpu_migratable = ctk.CTkOptionMenu(
            frame, values=['on', 'off'], width=50, font=('', 10)
        )
        self.cpu_migratable.set('on')
        self.cpu_migratable.pack(side='left', padx=2)
        self.cpu_migratable.configure(command=self._trigger_change)

    def _on_mode_change(self, value: str) -> None:
        """根据 mode 自动调整 match 和 migratable 默认值.

        根据 libvirt 文档:
        - host-model 模式下，match 属性无效（不应设置）
        - host-passthrough 和 maximum 模式通常搭配 migratable 属性
        - custom 模式下 match 默认为 exact
        """
        # 可以在这里根据 mode 自动调整其他设置
        # 但目前保持用户设置不变
        self._trigger_change(value)

    def _create_model_vendor_row(self, parent: ctk.CTkFrame, row: int) -> None:
        """创建 model、fallback、vendor、vendor_id 行."""
        frame = ctk.CTkFrame(parent, fg_color='transparent')
        frame.grid(row=row, column=0, columnspan=2, padx=10, pady=3, sticky='w')

        # model
        ctk.CTkLabel(frame, text='model:', font=('', 10), width=45, anchor='w').pack(
            side='left', padx=(0, 2)
        )
        self.cpu_model = ctk.CTkEntry(
            frame, placeholder_text='core2duo', width=100, font=('', 10)
        )
        self.cpu_model.pack(side='left', padx=2)
        self.cpu_model.bind('<KeyRelease>', lambda e: self._trigger_change())

        # fallback
        ctk.CTkLabel(frame, text='fallback:', font=('', 10), width=55, anchor='w').pack(
            side='left', padx=(10, 2)
        )
        self.model_fallback = ctk.CTkOptionMenu(
            frame, values=['allow', 'forbid'], width=70, font=('', 10)
        )
        self.model_fallback.set('allow')
        self.model_fallback.pack(side='left', padx=2)
        self.model_fallback.configure(command=self._trigger_change)

        # vendor
        ctk.CTkLabel(frame, text='vendor:', font=('', 10), width=50, anchor='w').pack(
            side='left', padx=(10, 2)
        )
        self.cpu_vendor = ctk.CTkEntry(
            frame, placeholder_text='Intel', width=80, font=('', 10)
        )
        self.cpu_vendor.pack(side='left', padx=2)
        self.cpu_vendor.bind('<KeyRelease>', lambda e: self._trigger_change())

        # vendor_id
        ctk.CTkLabel(frame, text='vendor_id:', font=('', 10), width=55, anchor='w').pack(
            side='left', padx=(10, 2)
        )
        self.vendor_id = ctk.CTkEntry(
            frame, placeholder_text='AuthenticAMD', width=120, font=('', 10)
        )
        self.vendor_id.pack(side='left', padx=2)
        self.vendor_id.bind('<KeyRelease>', lambda e: self._trigger_change())


    def _create_topology_row1(self, parent: ctk.CTkFrame, row: int) -> None:
        """创建拓扑结构第一行：sockets、dies、clusters、cores."""
        frame = ctk.CTkFrame(parent, fg_color='transparent')
        frame.grid(row=row, column=0, columnspan=2, padx=10, pady=3, sticky='w')

        # sockets
        ctk.CTkLabel(frame, text='sockets:', font=('', 10), width=50, anchor='w').pack(
            side='left', padx=(0, 2)
        )
        self.sockets = ctk.CTkEntry(frame, placeholder_text='1', width=50, font=('', 10))
        self.sockets.pack(side='left', padx=2)
        self.sockets.bind('<KeyRelease>', lambda e: self._trigger_change())

        # dies
        ctk.CTkLabel(frame, text='dies:', font=('', 10), width=35, anchor='w').pack(
            side='left', padx=(10, 2)
        )
        self.dies = ctk.CTkEntry(frame, placeholder_text='1', width=40, font=('', 10))
        self.dies.pack(side='left', padx=2)
        self.dies.bind('<KeyRelease>', lambda e: self._trigger_change())

        # clusters
        ctk.CTkLabel(frame, text='clusters:', font=('', 10), width=50, anchor='w').pack(
            side='left', padx=(10, 2)
        )
        self.clusters = ctk.CTkEntry(frame, placeholder_text='1', width=40, font=('', 10))
        self.clusters.pack(side='left', padx=2)
        self.clusters.bind('<KeyRelease>', lambda e: self._trigger_change())

        # cores
        ctk.CTkLabel(frame, text='cores:', font=('', 10), width=45, anchor='w').pack(
            side='left', padx=(10, 2)
        )
        self.cores = ctk.CTkEntry(frame, placeholder_text='2', width=50, font=('', 10))
        self.cores.pack(side='left', padx=2)
        self.cores.bind('<KeyRelease>', lambda e: self._trigger_change())

    def _create_threads_row(self, parent: ctk.CTkFrame, row: int) -> None:
        """创建 threads 行."""
        frame = ctk.CTkFrame(parent, fg_color='transparent')
        frame.grid(row=row, column=0, columnspan=2, padx=10, pady=3, sticky='w')

        ctk.CTkLabel(frame, text='threads:', font=('', 10), width=50, anchor='w').pack(
            side='left', padx=(0, 2)
        )
        self.threads = ctk.CTkEntry(frame, placeholder_text='1', width=50, font=('', 10))
        self.threads.pack(side='left', padx=2)
        self.threads.bind('<KeyRelease>', lambda e: self._trigger_change())

        # 说明文本
        ctk.CTkLabel(
            frame, text='(vCPU = sockets × dies × clusters × cores × threads)', font=('', 9), text_color='#888888'
        ).pack(side='left', padx=10)

    def _create_feature_add_row(self, parent: ctk.CTkFrame, row: int) -> None:
        """创建添加 feature 的行."""
        frame = ctk.CTkFrame(parent, fg_color='transparent')
        frame.grid(row=row, column=0, columnspan=2, padx=10, pady=3, sticky='w')

        ctk.CTkLabel(frame, text='feature:', font=('', 10), width=55, anchor='w').pack(
            side='left', padx=(0, 2)
        )
        self.feature_name = ctk.CTkEntry(frame, placeholder_text='lahf_lm, pcid...', width=120, font=('', 10))
        self.feature_name.pack(side='left', padx=2)
        self.feature_name.bind('<KeyRelease>', lambda e: self._on_enter_key(e))

        ctk.CTkLabel(frame, text='policy:', font=('', 10), width=45, anchor='w').pack(
            side='left', padx=(10, 2)
        )
        self.feature_policy = ctk.CTkOptionMenu(
            frame, values=['require', 'optional', 'force', 'disable', 'forbid'], width=80, font=('', 10)
        )
        self.feature_policy.set('require')
        self.feature_policy.pack(side='left', padx=2)

        add_btn = ctk.CTkButton(
            frame, text='+', width=25, height=20, command=self._add_feature, font=('', 10)
        )
        add_btn.pack(side='left', padx=5)

        remove_btn = ctk.CTkButton(
            frame, text='-', width=25, height=20, command=self._remove_feature, font=('', 10)
        )
        remove_btn.pack(side='left', padx=2)

    def _create_cache_basic_row(self, parent: ctk.CTkFrame, row: int) -> None:
        """创建缓存配置行：cache_level、cache_mode."""
        frame = ctk.CTkFrame(parent, fg_color='transparent')
        frame.grid(row=row, column=0, columnspan=2, padx=10, pady=3, sticky='w')

        # cache level
        ctk.CTkLabel(frame, text='level:', font=('', 10), width=40, anchor='w').pack(
            side='left', padx=(0, 2)
        )
        self.cache_level = ctk.CTkOptionMenu(
            frame, values=['1', '2', '3'], width=50, font=('', 10)
        )
        self.cache_level.set('3')
        self.cache_level.pack(side='left', padx=2)
        self.cache_level.configure(command=self._trigger_change)

        # cache mode
        ctk.CTkLabel(frame, text='mode:', font=('', 10), width=40, anchor='w').pack(
            side='left', padx=(10, 2)
        )
        self.cache_mode = ctk.CTkOptionMenu(
            frame, values=['emulate', 'passthrough', 'disable'], width=80, font=('', 10)
        )
        self.cache_mode.set('emulate')
        self.cache_mode.pack(side='left', padx=2)
        self.cache_mode.configure(command=self._trigger_change)

    def _create_physaddr_row(self, parent: ctk.CTkFrame, row: int) -> None:
        """创建物理地址配置行."""
        frame = ctk.CTkFrame(parent, fg_color='transparent')
        frame.grid(row=row, column=0, columnspan=2, padx=10, pady=3, sticky='w')

        # physaddr mode
        ctk.CTkLabel(frame, text='mode:', font=('', 10), width=40, anchor='w').pack(
            side='left', padx=(0, 2)
        )
        self.physaddr_mode = ctk.CTkOptionMenu(
            frame, values=['passthrough', 'emulate'], width=80, font=('', 10)
        )
        self.physaddr_mode.set('passthrough')
        self.physaddr_mode.pack(side='left', padx=2)
        self.physaddr_mode.configure(command=self._trigger_change)

        # physaddr bits
        ctk.CTkLabel(frame, text='bits:', font=('', 10), width=35, anchor='w').pack(
            side='left', padx=(10, 2)
        )
        self.physaddr_bits = ctk.CTkEntry(frame, placeholder_text='42', width=50, font=('', 10))
        self.physaddr_bits.pack(side='left', padx=2)
        self.physaddr_bits.bind('<KeyRelease>', lambda e: self._trigger_change())

        # physaddr limit
        ctk.CTkLabel(frame, text='limit:', font=('', 10), width=35, anchor='w').pack(
            side='left', padx=(10, 2)
        )
        self.physaddr_limit = ctk.CTkEntry(frame, placeholder_text='39', width=50, font=('', 10))
        self.physaddr_limit.pack(side='left', padx=2)
        self.physaddr_limit.bind('<KeyRelease>', lambda e: self._trigger_change())

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
        self._refresh_feature_display()
        self._trigger_change()

    def _remove_feature(self):
        """删除最后一个 CPU 特性."""
        if self.features_list:
            self.features_list.pop()
            self._refresh_feature_display()
            self._trigger_change()

    def _refresh_feature_display(self):
        """刷新 feature 显示."""
        # 清除所有现有控件
        for widget in self.features_display_frame.winfo_children():
            widget.destroy()

        if not self.features_list:
            ctk.CTkLabel(
                self.features_display_frame, text='暂无已添加特性', font=('', 10), text_color='#888888'
            ).grid(row=0, column=0, padx=10, pady=5, sticky='w')
            return

        # 横向排列所有特性
        for i, feat in enumerate(self.features_list):
            feat_frame = ctk.CTkFrame(self.features_display_frame, fg_color='#2a2a2a', corner_radius=4)
            feat_frame.grid(row=0, column=i, padx=3, pady=3, sticky='w')

            feat_text = f'{feat["name"]} ({feat["policy"]})'
            ctk.CTkLabel(
                feat_frame, text=feat_text, font=('', 9), text_color='#64b5f6'
            ).pack(side='left', padx=5, pady=2)

    def get_config(self) -> dict:
        """获取配置数据."""
        return {
            'model': {
                'mode': self.cpu_mode.get(),
                'match': self.cpu_match.get(),
                'check': self.cpu_check.get(),
                'migratable': self.cpu_migratable.get(),
                'model': self.cpu_model.get().strip(),
                'fallback': self.model_fallback.get(),
                'vendor': self.cpu_vendor.get().strip(),
                'vendor_id': self.vendor_id.get().strip(),
            },
            'topology': {
                'sockets': self.sockets.get().strip(),
                'dies': self.dies.get().strip(),
                'clusters': self.clusters.get().strip(),
                'cores': self.cores.get().strip(),
                'threads': self.threads.get().strip(),
            },
            'features': self.features_list.copy(),
            'cache': {
                'level': int(self.cache_level.get()) if self.cache_level.get() else 3,
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
        # CPU 模型
        model = config.get('model', {})
        if 'mode' in model:
            self.cpu_mode.set(model['mode'])
        if 'match' in model:
            self.cpu_match.set(model['match'])
        if 'check' in model:
            self.cpu_check.set(model['check'])
        if 'migratable' in model:
            self.cpu_migratable.set(model['migratable'])
        if 'model' in model:
            self.cpu_model.delete(0, 'end')
            self.cpu_model.insert(0, model['model'])
        if 'fallback' in model:
            self.model_fallback.set(model['fallback'])
        if 'vendor' in model:
            self.cpu_vendor.delete(0, 'end')
            self.cpu_vendor.insert(0, model['vendor'])
        if 'vendor_id' in model:
            self.vendor_id.delete(0, 'end')
            self.vendor_id.insert(0, model['vendor_id'])

        # 拓扑
        topology = config.get('topology', {})
        if 'sockets' in topology:
            self.sockets.delete(0, 'end')
            self.sockets.insert(0, topology['sockets'])
        if 'dies' in topology:
            self.dies.delete(0, 'end')
            self.dies.insert(0, topology['dies'])
        if 'clusters' in topology:
            self.clusters.delete(0, 'end')
            self.clusters.insert(0, topology['clusters'])
        if 'cores' in topology:
            self.cores.delete(0, 'end')
            self.cores.insert(0, topology['cores'])
        if 'threads' in topology:
            self.threads.delete(0, 'end')
            self.threads.insert(0, topology['threads'])

        # 特性
        self.features_list = config.get('features', []).copy()
        self._refresh_feature_display()

        # 缓存
        cache = config.get('cache', {})
        if 'level' in cache:
            self.cache_level.set(str(cache['level']))
        if 'mode' in cache:
            self.cache_mode.set(cache['mode'])

        # 物理地址
        maxphysaddr = config.get('maxphysaddr', {})
        if 'mode' in maxphysaddr:
            self.physaddr_mode.set(maxphysaddr['mode'])
        if 'bits' in maxphysaddr:
            self.physaddr_bits.delete(0, 'end')
            self.physaddr_bits.insert(0, maxphysaddr['bits'])
        if 'limit' in maxphysaddr:
            self.physaddr_limit.delete(0, 'end')
            self.physaddr_limit.insert(0, maxphysaddr['limit'])
