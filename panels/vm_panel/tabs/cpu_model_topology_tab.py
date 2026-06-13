"""CPU 模型与拓扑配置 Tab - 参考系统启动 Tab 布局重构."""

from typing import ClassVar

import customtkinter as ctk

from components.base_tab import SectionConfig, StandardConfigTab


class CPUModelTopologyTab(StandardConfigTab):
    """CPU 模型与拓扑配置 Tab - 使用紧凑布局.

    根据 libvirt 文档第 15 章实现,支持以下配置:

    CPU 元素属性:
    - mode: custom, host-model, host-passthrough, maximum
    - match: exact, minimum, strict (host-model 模式下无效)
    - check: none, partial, full
    - migratable: on, off (host-passthrough/maximum 模式常用)
    - deprecated_features: on, off (S390 专用,Since 11.0.0)

    子元素:
    - model: CPU 模型名称,支持 fallback 属性
    - vendor: 厂商名称,支持 id 属性 (vendor_id)
    - topology: sockets, dies, clusters, cores, threads
    - feature: 可配置多个,支持 policy 属性
    - cache: level, mode
    - maxphysaddr: mode, bits, limit
    """

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
        """初始化基于 Sections 的 UI,添加自定义布局."""
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

        # threads 单独一行(带说明)
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
        """创建 CPU 模型基本信息行:mode、match、check、migratable、deprecated_features."""
        frame = ctk.CTkFrame(parent, fg_color='transparent')
        frame.grid(row=row, column=0, columnspan=2, padx=10, pady=3, sticky='w')

        # mode
        ctk.CTkLabel(frame, text='mode:', font=('', 10), width=25, anchor='w').pack(
            side='left', padx=(0, 2)
        )
        self.cpu_mode = ctk.CTkOptionMenu(
            frame,
            values=['None', 'custom', 'host-model', 'host-passthrough', 'maximum'],
            width=60,
            font=('', 10),
            command=self._on_mode_change,
        )
        self.cpu_mode.set('None')
        self.cpu_mode.pack(side='left', padx=2)

        # match
        ctk.CTkLabel(frame, text='match:', font=('', 10), width=25, anchor='w').pack(
            side='left', padx=(5, 2)
        )
        self.cpu_match = ctk.CTkOptionMenu(
            frame, values=['None', 'exact', 'minimum', 'strict'], width=70, font=('', 10)
        )
        self.cpu_match.set('None')
        self.cpu_match.pack(side='left', padx=2)
        self.cpu_match.configure(command=self._trigger_change)

        # check
        ctk.CTkLabel(frame, text='check:', font=('', 10), width=25, anchor='w').pack(
            side='left', padx=(5, 2)
        )
        self.cpu_check = ctk.CTkOptionMenu(
            frame, values=['None', 'none', 'partial', 'full'], width=65, font=('', 10)
        )
        self.cpu_check.set('None')
        self.cpu_check.pack(side='left', padx=2)
        self.cpu_check.configure(command=self._trigger_change)

        # migratable
        ctk.CTkLabel(frame, text='migratable:', font=('', 10), width=60, anchor='w').pack(
            side='left', padx=(5, 2)
        )
        self.cpu_migratable = ctk.CTkOptionMenu(
            frame, values=['None', 'on', 'off'], width=50, font=('', 10)
        )
        self.cpu_migratable.set('None')
        self.cpu_migratable.pack(side='left', padx=2)
        self.cpu_migratable.configure(command=self._trigger_change)

        # deprecated_features (S390 专用)
        ctk.CTkLabel(frame, text='deprecated_features:', font=('', 9), width=90, anchor='w').pack(
            side='left', padx=(5, 2)
        )
        self.deprecated_features = ctk.CTkOptionMenu(
            frame, values=['on', 'off'], width=30, font=('', 9)
        )
        self.deprecated_features.set('on')
        self.deprecated_features.pack(side='left', padx=2)
        self.deprecated_features.configure(command=self._trigger_change)

    def _on_mode_change(self, value: str) -> None:
        """根据 mode 自动调整 match 和 migratable 默认值.

        根据 libvirt 文档:
        - host-model 模式下,match 属性无效(不应设置)
        - host-passthrough 和 maximum 模式通常搭配 migratable 属性
        - custom 模式下 match 默认为 exact

        Args:
            value: mode 值 (custom, host-model, host-passthrough, maximum)
        """
        # host-model 模式下 match 属性无效,但保持用户设置不变
        # host-passthrough 和 maximum 模式通常与 migratable 属性一起使用
        self._trigger_change(value)

    def get_mode_help_text(self) -> str:
        """获取当前 mode 的帮助文本.

        Returns:
            描述当前 mode 特性的帮助文本
        """
        mode = self.cpu_mode.get()
        help_texts = {
            'custom': '自定义 CPU 模型,guest 看到的硬件与配置一致',
            'host-model': '匹配主机 CPU 模型,match 属性无效',
            'host-passthrough': '直通主机 CPU,迁移需目标主机相同',
            'maximum': '最大 CPU 特性集,类似 host-passthrough',
        }
        return help_texts.get(mode, '')

    def _create_model_vendor_row(self, parent: ctk.CTkFrame, row: int) -> None:
        """创建 model、fallback、vendor、vendor_id 行."""
        frame = ctk.CTkFrame(parent, fg_color='transparent')
        frame.grid(row=row, column=0, columnspan=2, padx=10, pady=3, sticky='w')

        # model
        ctk.CTkLabel(frame, text='model:', font=('', 10), width=45, anchor='w').pack(
            side='left', padx=(0, 2)
        )
        self.cpu_model = ctk.CTkEntry(frame, placeholder_text='core2duo', width=100, font=('', 10))
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
        self.cpu_vendor = ctk.CTkEntry(frame, placeholder_text='Intel', width=80, font=('', 10))
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
        """创建拓扑结构第一行:sockets、dies、clusters、cores."""
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
            frame,
            text='(vCPU = sockets × dies × clusters × cores × threads)',
            font=('', 9),
            text_color='#888888',
        ).pack(side='left', padx=10)

    def _create_feature_add_row(self, parent: ctk.CTkFrame, row: int) -> None:
        """创建添加 feature 的行."""
        frame = ctk.CTkFrame(parent, fg_color='transparent')
        frame.grid(row=row, column=0, columnspan=2, padx=10, pady=3, sticky='w')

        ctk.CTkLabel(frame, text='feature:', font=('', 10), width=55, anchor='w').pack(
            side='left', padx=(0, 2)
        )
        self.feature_name = ctk.CTkEntry(
            frame, placeholder_text='lahf_lm, pcid...', width=120, font=('', 10)
        )
        self.feature_name.pack(side='left', padx=2)
        self.feature_name.bind('<KeyRelease>', lambda e: self._on_enter_key(e))

        ctk.CTkLabel(frame, text='policy:', font=('', 10), width=45, anchor='w').pack(
            side='left', padx=(10, 2)
        )
        self.feature_policy = ctk.CTkOptionMenu(
            frame,
            values=['require', 'optional', 'force', 'disable', 'forbid'],
            width=80,
            font=('', 10),
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
        """创建缓存配置行:cache_level、cache_mode."""
        frame = ctk.CTkFrame(parent, fg_color='transparent')
        frame.grid(row=row, column=0, columnspan=2, padx=10, pady=3, sticky='w')

        # cache level
        ctk.CTkLabel(frame, text='level:', font=('', 10), width=40, anchor='w').pack(
            side='left', padx=(0, 2)
        )
        self.cache_level = ctk.CTkOptionMenu(frame, values=['1', '2', '3'], width=50, font=('', 10))
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
                self.features_display_frame,
                text='暂无已添加特性',
                font=('', 10),
                text_color='#888888',
            ).grid(row=0, column=0, padx=10, pady=5, sticky='w')
            return

        # 横向排列所有特性
        for i, feat in enumerate(self.features_list):
            feat_frame = ctk.CTkFrame(
                self.features_display_frame, fg_color='#2a2a2a', corner_radius=4
            )
            feat_frame.grid(row=0, column=i, padx=3, pady=3, sticky='w')

            feat_text = f'{feat["name"]} ({feat["policy"]})'
            ctk.CTkLabel(feat_frame, text=feat_text, font=('', 9), text_color='#64b5f6').pack(
                side='left', padx=5, pady=2
            )

    def get_config(self) -> dict:
        """获取配置数据,过滤掉值为 None 的选项."""
        result = {}

        # 处理 model 字段,包含 name、fallback、vendor、vendor_id
        model_name = self.cpu_model.get().strip()
        model_dict = {}
        if model_name:
            model_dict['name'] = model_name
            fallback_value = self.model_fallback.get()
            # 只有用户明确选择了 forbid 时才添加 fallback(默认 allow 不输出)
            if fallback_value and fallback_value == 'forbid':
                model_dict['fallback'] = fallback_value
        # vendor 和 vendor_id 可以独立于 model_name 添加
        vendor_value = self.cpu_vendor.get().strip()
        if vendor_value:
            model_dict['vendor'] = vendor_value
        vendor_id_value = self.vendor_id.get().strip()
        if vendor_id_value:
            model_dict['vendor_id'] = vendor_id_value

        # mode/match/check/migratable/deprecated_features 放在顶层
        mode_value = self.cpu_mode.get()
        if mode_value != 'None':
            result['mode'] = mode_value

        match_value = self.cpu_match.get()
        if match_value != 'None':
            result['match'] = match_value

        check_value = self.cpu_check.get()
        if check_value != 'None':
            result['check'] = check_value

        migratable_value = self.cpu_migratable.get()
        if migratable_value != 'None':
            result['migratable'] = migratable_value

        deprecated_features_value = self.deprecated_features.get()
        # deprecated_features 默认值为 'on',只有用户明确选择了'off'时才添加
        if deprecated_features_value == 'off':
            result['deprecated_features'] = 'off'

        # 构建 topology,只有填写了至少一个字段的值才添加
        topology_data = {}
        for field_name, field_widget in [
            ('sockets', self.sockets),
            ('dies', self.dies),
            ('clusters', self.clusters),
            ('cores', self.cores),
            ('threads', self.threads),
        ]:
            field_value = field_widget.get().strip()
            if field_value:
                topology_data[field_name] = field_value

        # 构建 feature 列表
        feature_list = []
        for feat in self.features_list:
            feat_name = feat.get('name', '').strip()
            if feat_name:
                feat_dict = {'name': feat_name}
                policy = feat.get('policy')
                if policy and policy != 'require':
                    feat_dict['policy'] = policy
                feature_list.append(feat_dict)

        # 构建 cache,只有 mode 不是默认值 emulate 时才添加
        cache_data = {}
        cache_level = self.cache_level.get()
        cache_mode = self.cache_mode.get()
        if cache_level and cache_level != '3':
            cache_data['level'] = int(cache_level)
        if cache_mode and cache_mode != 'emulate':
            cache_data['mode'] = cache_mode

        # 构建 maxphysaddr,只有填写了值才添加
        maxphysaddr_data = {}
        physaddr_mode = self.physaddr_mode.get()
        physaddr_bits = self.physaddr_bits.get().strip()
        physaddr_limit = self.physaddr_limit.get().strip()
        if physaddr_mode and physaddr_mode != 'passthrough':
            maxphysaddr_data['mode'] = physaddr_mode
        if physaddr_bits:
            maxphysaddr_data['bits'] = physaddr_bits
        if physaddr_limit:
            maxphysaddr_data['limit'] = physaddr_limit

        # 添加 model 字典(如果有内容)
        if model_dict:
            result['model'] = model_dict
        if topology_data:
            result['topology'] = topology_data
        if feature_list:
            result['feature'] = feature_list
        if cache_data:
            result['cache'] = cache_data
        if maxphysaddr_data:
            result['maxphysaddr'] = maxphysaddr_data

        return result

    def to_xml(self) -> dict:
        """生成 XML 配置字典."""
        return {'cpu_model_topology': self.get_config()}

    def load_config(self, config: dict) -> None:
        """加载配置数据."""
        # CPU 模型
        model = config.get('model', {})
        if 'mode' in model:
            self.cpu_mode.set(model['mode'])
        else:
            self.cpu_mode.set('None')
        if 'match' in model:
            self.cpu_match.set(model['match'])
        else:
            self.cpu_match.set('None')
        if 'check' in model:
            self.cpu_check.set(model['check'])
        else:
            self.cpu_check.set('None')
        if 'migratable' in model:
            self.cpu_migratable.set(model['migratable'])
        else:
            self.cpu_migratable.set('None')
        if 'deprecated_features' in model:
            self.deprecated_features.set(model['deprecated_features'])
        # 处理model字段(现在是字典)
        if 'model' in model and isinstance(model['model'], dict):
            model_dict = model['model']
            if 'name' in model_dict:
                self.cpu_model.delete(0, 'end')
                self.cpu_model.insert(0, model_dict['name'])
            if 'fallback' in model_dict:
                self.model_fallback.set(model_dict['fallback'])
            if 'vendor' in model_dict:
                self.cpu_vendor.delete(0, 'end')
                self.cpu_vendor.insert(0, model_dict['vendor'])
            if 'vendor_id' in model_dict:
                self.vendor_id.delete(0, 'end')
                self.vendor_id.insert(0, model_dict['vendor_id'])

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
        self.features_list = config.get('feature', []).copy()
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
