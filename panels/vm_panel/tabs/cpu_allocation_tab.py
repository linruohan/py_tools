"""CPU 分配配置 Tab - vCPU 分配和配置."""

import customtkinter as ctk

from components.base_tab import BaseConfigTab
from utils.parsers import parse_integer_value


class CPUAllocationTab(BaseConfigTab):
    """CPU 分配配置 Tab."""

    def _init_ui(self) -> None:
        """初始化界面."""
        # 使用三列布局
        for i in range(3):
            self.grid_columnconfigure(i, weight=1)

        # 添加标题
        self._create_section_title(self, 'CPU 模型和拓扑配置', row=0, column=0, columnspan=3)

        # 创建checkbox容器
        self.checkbox_frame = ctk.CTkFrame(self)
        self.checkbox_frame.grid(row=1, column=0, padx=10, pady=5, sticky='ew', columnspan=3)

        # 设置checkbox容器的布局为单行
        for i in range(10):
            self.checkbox_frame.grid_columnconfigure(i, weight=1)

        # 所有checkbox一行显示
        self.mode_checkbox = ctk.CTkCheckBox(
            self.checkbox_frame, text='Mode', command=self._toggle_mode
        )
        self.mode_checkbox.grid(row=0, column=0, padx=5, pady=2, sticky='w')

        self.match_checkbox = ctk.CTkCheckBox(
            self.checkbox_frame, text='Match', command=self._toggle_match
        )
        self.match_checkbox.grid(row=0, column=1, padx=5, pady=2, sticky='w')

        self.migratable_checkbox = ctk.CTkCheckBox(
            self.checkbox_frame, text='Migratable', command=self._toggle_migratable
        )
        self.migratable_checkbox.grid(row=0, column=2, padx=5, pady=2, sticky='w')

        self.check_checkbox = ctk.CTkCheckBox(
            self.checkbox_frame, text='Check', command=self._toggle_check
        )
        self.check_checkbox.grid(row=0, column=3, padx=5, pady=2, sticky='w')

        self.model_checkbox = ctk.CTkCheckBox(
            self.checkbox_frame, text='Model', command=self._toggle_model
        )
        self.model_checkbox.grid(row=0, column=4, padx=5, pady=2, sticky='w')

        self.vendor_checkbox = ctk.CTkCheckBox(
            self.checkbox_frame, text='Vendor', command=self._toggle_vendor
        )
        self.vendor_checkbox.grid(row=0, column=5, padx=5, pady=2, sticky='w')

        self.topology_checkbox = ctk.CTkCheckBox(
            self.checkbox_frame, text='Topology', command=self._toggle_topology
        )
        self.topology_checkbox.grid(row=0, column=6, padx=5, pady=2, sticky='w')

        self.cache_checkbox = ctk.CTkCheckBox(
            self.checkbox_frame, text='Cache', command=self._toggle_cache
        )
        self.cache_checkbox.grid(row=0, column=7, padx=5, pady=2, sticky='w')

        self.maxphysaddr_checkbox = ctk.CTkCheckBox(
            self.checkbox_frame, text='Maxphysaddr', command=self._toggle_maxphysaddr
        )
        self.maxphysaddr_checkbox.grid(row=0, column=8, padx=5, pady=2, sticky='w')

        self.feature_checkbox = ctk.CTkCheckBox(
            self.checkbox_frame, text='Feature', command=self._toggle_feature
        )
        self.feature_checkbox.grid(row=0, column=9, padx=5, pady=2, sticky='w')

        # 创建UI配置容器（不使用section frames，直接放置元素）
        self.ui_container = ctk.CTkFrame(self)
        self.ui_container.grid(row=2, column=0, padx=10, pady=5, sticky='nsew', columnspan=3)

        # 设置UI容器的布局 - 每行3个元素
        for i in range(3):
            self.ui_container.grid_columnconfigure(i, weight=1)

        # 初始化所有UI元素
        # Mode配置
        self.mode_label = ctk.CTkLabel(self.ui_container, text='Mode:', font=('Arial', 10, 'bold'))
        self.mode_label.grid(row=0, column=0, padx=5, pady=2, sticky='w')
        self.mode_value_label = ctk.CTkLabel(
            self.ui_container, text='Value:', font=('Arial', 10), width=60, anchor='e'
        )
        self.mode_value_label.grid(row=1, column=0, padx=5, pady=2, sticky='e')
        self.cpu_mode = ctk.CTkComboBox(
            self.ui_container,
            values=['custom', 'host-model', 'host-passthrough', 'maximum'],
            width=180,
        )
        self.cpu_mode.grid(row=1, column=0, padx=70, pady=2, sticky='w')
        self.cpu_mode.set('custom')
        self.cpu_mode.bind('<<ComboboxSelected>>', lambda e: self._trigger_change())

        # Match配置
        self.match_label = ctk.CTkLabel(
            self.ui_container, text='Match:', font=('Arial', 10, 'bold')
        )
        self.match_label.grid(row=0, column=1, padx=5, pady=2, sticky='w')
        self.match_value_label = ctk.CTkLabel(
            self.ui_container, text='Value:', font=('Arial', 10), width=60, anchor='e'
        )
        self.match_value_label.grid(row=1, column=1, padx=5, pady=2, sticky='e')
        self.cpu_match = ctk.CTkComboBox(
            self.ui_container, values=['minimum', 'exact', 'strict'], width=180
        )
        self.cpu_match.grid(row=1, column=1, padx=70, pady=2, sticky='w')
        self.cpu_match.set('exact')
        self.cpu_match.bind('<<ComboboxSelected>>', lambda e: self._trigger_change())

        # Migratable配置
        self.migratable_label = ctk.CTkLabel(
            self.ui_container, text='Migratable:', font=('Arial', 10, 'bold')
        )
        self.migratable_label.grid(row=0, column=2, padx=5, pady=2, sticky='w')
        self.migratable_value_label = ctk.CTkLabel(
            self.ui_container, text='Value:', font=('Arial', 10), width=60, anchor='e'
        )
        self.migratable_value_label.grid(row=1, column=2, padx=5, pady=2, sticky='e')
        self.cpu_migratable = ctk.CTkComboBox(self.ui_container, values=['on', 'off'], width=180)
        self.cpu_migratable.grid(row=1, column=2, padx=70, pady=2, sticky='w')
        self.cpu_migratable.set('off')
        self.cpu_migratable.bind('<<ComboboxSelected>>', lambda e: self._trigger_change())

        # Check配置
        self.check_label = ctk.CTkLabel(
            self.ui_container, text='Check:', font=('Arial', 10, 'bold')
        )
        self.check_label.grid(row=2, column=0, padx=5, pady=2, sticky='w')
        self.check_value_label = ctk.CTkLabel(
            self.ui_container, text='Value:', font=('Arial', 10), width=60, anchor='e'
        )
        self.check_value_label.grid(row=3, column=0, padx=5, pady=2, sticky='e')
        self.cpu_check = ctk.CTkComboBox(
            self.ui_container, values=['none', 'partial', 'full'], width=180
        )
        self.cpu_check.grid(row=3, column=0, padx=70, pady=2, sticky='w')
        self.cpu_check.bind('<<ComboboxSelected>>', lambda e: self._trigger_change())

        # Model配置
        self.model_label = ctk.CTkLabel(
            self.ui_container, text='Model:', font=('Arial', 10, 'bold')
        )
        self.model_label.grid(row=2, column=1, padx=5, pady=2, sticky='w')
        self.model_name_label = ctk.CTkLabel(
            self.ui_container, text='Name:', font=('Arial', 10), width=60, anchor='e'
        )
        self.model_name_label.grid(row=3, column=1, padx=5, pady=2, sticky='e')
        self.cpu_model = ctk.CTkEntry(self.ui_container, placeholder_text='core2duo', width=180)
        self.cpu_model.grid(row=3, column=1, padx=70, pady=2, sticky='w')
        self.cpu_model.bind('<KeyRelease>', lambda e: self._trigger_change())

        self.model_fallback_label = ctk.CTkLabel(
            self.ui_container, text='Fallback:', font=('Arial', 10), width=60, anchor='e'
        )
        self.model_fallback_label.grid(row=4, column=1, padx=5, pady=2, sticky='e')
        self.cpu_fallback = ctk.CTkComboBox(
            self.ui_container, values=['allow', 'forbid'], width=180
        )
        self.cpu_fallback.grid(row=4, column=1, padx=70, pady=2, sticky='w')
        self.cpu_fallback.set('allow')
        self.cpu_fallback.bind('<<ComboboxSelected>>', lambda e: self._trigger_change())

        # Vendor配置
        self.vendor_label = ctk.CTkLabel(
            self.ui_container, text='Vendor:', font=('Arial', 10, 'bold')
        )
        self.vendor_label.grid(row=2, column=2, padx=5, pady=2, sticky='w')
        self.vendor_name_label = ctk.CTkLabel(
            self.ui_container, text='Name:', font=('Arial', 10), width=60, anchor='e'
        )
        self.vendor_name_label.grid(row=3, column=2, padx=5, pady=2, sticky='e')
        self.cpu_vendor = ctk.CTkEntry(self.ui_container, placeholder_text='Intel', width=180)
        self.cpu_vendor.grid(row=3, column=2, padx=70, pady=2, sticky='w')
        self.cpu_vendor.bind('<KeyRelease>', lambda e: self._trigger_change())

        # Topology配置
        self.topology_label = ctk.CTkLabel(
            self.ui_container, text='Topology:', font=('Arial', 10, 'bold')
        )
        self.topology_label.grid(row=5, column=0, padx=5, pady=2, sticky='w')
        self.topology_sockets_label = ctk.CTkLabel(
            self.ui_container, text='Sockets:', font=('Arial', 10), width=60, anchor='e'
        )
        self.topology_sockets_label.grid(row=6, column=0, padx=5, pady=2, sticky='e')
        self.sockets = ctk.CTkEntry(self.ui_container, placeholder_text='1', width=80)
        self.sockets.grid(row=6, column=0, padx=70, pady=2, sticky='w')
        self.sockets.bind('<KeyRelease>', lambda e: self._trigger_change())

        self.topology_dies_label = ctk.CTkLabel(
            self.ui_container, text='Dies:', font=('Arial', 10), width=60, anchor='e'
        )
        self.topology_dies_label.grid(row=7, column=0, padx=5, pady=2, sticky='e')
        self.dies = ctk.CTkEntry(self.ui_container, placeholder_text='1', width=80)
        self.dies.grid(row=7, column=0, padx=70, pady=2, sticky='w')
        self.dies.bind('<KeyRelease>', lambda e: self._trigger_change())

        self.topology_clusters_label = ctk.CTkLabel(
            self.ui_container, text='Clusters:', font=('Arial', 10), width=60, anchor='e'
        )
        self.topology_clusters_label.grid(row=8, column=0, padx=5, pady=2, sticky='e')
        self.clusters = ctk.CTkEntry(self.ui_container, placeholder_text='1', width=80)
        self.clusters.grid(row=8, column=0, padx=70, pady=2, sticky='w')
        self.clusters.bind('<KeyRelease>', lambda e: self._trigger_change())

        self.topology_cores_label = ctk.CTkLabel(
            self.ui_container, text='Cores:', font=('Arial', 10), width=60, anchor='e'
        )
        self.topology_cores_label.grid(row=9, column=0, padx=5, pady=2, sticky='e')
        self.cores = ctk.CTkEntry(self.ui_container, placeholder_text='2', width=80)
        self.cores.grid(row=9, column=0, padx=70, pady=2, sticky='w')
        self.cores.bind('<KeyRelease>', lambda e: self._trigger_change())

        self.topology_threads_label = ctk.CTkLabel(
            self.ui_container, text='Threads:', font=('Arial', 10), width=60, anchor='e'
        )
        self.topology_threads_label.grid(row=10, column=0, padx=5, pady=2, sticky='e')
        self.threads = ctk.CTkEntry(self.ui_container, placeholder_text='1', width=80)
        self.threads.grid(row=10, column=0, padx=70, pady=2, sticky='w')
        self.threads.bind('<KeyRelease>', lambda e: self._trigger_change())

        # Cache配置
        self.cache_label = ctk.CTkLabel(
            self.ui_container, text='Cache:', font=('Arial', 10, 'bold')
        )
        self.cache_label.grid(row=5, column=1, padx=5, pady=2, sticky='w')
        self.cache_mode_label = ctk.CTkLabel(
            self.ui_container, text='Mode:', font=('Arial', 10), width=60, anchor='e'
        )
        self.cache_mode_label.grid(row=6, column=1, padx=5, pady=2, sticky='e')
        self.cache_mode = ctk.CTkComboBox(
            self.ui_container, values=['emulate', 'passthrough', 'disable'], width=180
        )
        self.cache_mode.grid(row=6, column=1, padx=70, pady=2, sticky='w')
        self.cache_mode.bind('<<ComboboxSelected>>', lambda e: self._trigger_change())

        self.cache_level_label = ctk.CTkLabel(
            self.ui_container, text='Level:', font=('Arial', 10), width=60, anchor='e'
        )
        self.cache_level_label.grid(row=7, column=1, padx=5, pady=2, sticky='e')
        self.cache_level = ctk.CTkEntry(self.ui_container, placeholder_text='3', width=80)
        self.cache_level.grid(row=7, column=1, padx=70, pady=2, sticky='w')
        self.cache_level.bind('<KeyRelease>', lambda e: self._trigger_change())

        # Maxphysaddr配置
        self.maxphysaddr_label = ctk.CTkLabel(
            self.ui_container, text='Maxphysaddr:', font=('Arial', 10, 'bold')
        )
        self.maxphysaddr_label.grid(row=5, column=2, padx=5, pady=2, sticky='w')
        self.maxphysaddr_mode_label = ctk.CTkLabel(
            self.ui_container, text='Mode:', font=('Arial', 10), width=60, anchor='e'
        )
        self.maxphysaddr_mode_label.grid(row=6, column=2, padx=5, pady=2, sticky='e')
        self.maxphysaddr_mode = ctk.CTkComboBox(
            self.ui_container, values=['emulate', 'passthrough'], width=180
        )
        self.maxphysaddr_mode.grid(row=6, column=2, padx=70, pady=2, sticky='w')
        self.maxphysaddr_mode.set('emulate')
        self.maxphysaddr_mode.bind('<<ComboboxSelected>>', lambda e: self._trigger_change())

        self.maxphysaddr_bits_label = ctk.CTkLabel(
            self.ui_container, text='Bits:', font=('Arial', 10), width=60, anchor='e'
        )
        self.maxphysaddr_bits_label.grid(row=7, column=2, padx=5, pady=2, sticky='e')
        self.maxphysaddr_bits = ctk.CTkEntry(self.ui_container, placeholder_text='42', width=80)
        self.maxphysaddr_bits.grid(row=7, column=2, padx=70, pady=2, sticky='w')
        self.maxphysaddr_bits.bind('<KeyRelease>', lambda e: self._trigger_change())

        # Feature配置
        self.feature_label = ctk.CTkLabel(
            self.ui_container, text='Feature:', font=('Arial', 10, 'bold')
        )
        self.feature_label.grid(row=8, column=1, padx=5, pady=2, sticky='w')
        self.feature_name_label = ctk.CTkLabel(
            self.ui_container, text='Name:', font=('Arial', 10), width=60, anchor='e'
        )
        self.feature_name_label.grid(row=9, column=1, padx=5, pady=2, sticky='e')
        self.feature_name = ctk.CTkEntry(self.ui_container, placeholder_text='lahf_lm', width=180)
        self.feature_name.grid(row=9, column=1, padx=70, pady=2, sticky='w')
        self.feature_name.bind('<KeyRelease>', lambda e: self._trigger_change())

        self.feature_policy_label = ctk.CTkLabel(
            self.ui_container, text='Policy:', font=('Arial', 10), width=60, anchor='e'
        )
        self.feature_policy_label.grid(row=10, column=1, padx=5, pady=2, sticky='e')
        self.feature_policy = ctk.CTkComboBox(
            self.ui_container,
            values=['force', 'require', 'optional', 'disable', 'forbid'],
            width=180,
        )
        self.feature_policy.grid(row=10, column=1, padx=70, pady=2, sticky='w')
        self.feature_policy.set('disable')
        self.feature_policy.bind('<<ComboboxSelected>>', lambda e: self._trigger_change())

        # 添加说明文本
        info_text = (
            'CPU 配置说明:\n'
            '- Mode: CPU 模式 (custom/host-model/host-passthrough/maximum)\n'
            '- Match: 匹配策略 (minimum/exact/strict)\n'
            '- Check: 检查策略 (none/partial/full)\n'
            '- Migratable: 迁移性 (on/off)\n'
            '- Model: CPU 模型名称\n'
            '- Fallback: 当模型不可用时的行为 (allow/forbid)\n'
            '- Vendor: CPU 厂商\n'
            '- Topology: CPU 拓扑结构\n'
            '- Cache: 缓存配置\n'
            '- Maxphysaddr: 物理地址大小\n'
            '- Feature: CPU 特性配置'
        )
        self.info_label = self._create_info_label(self, info_text, row=3, column=0, columnspan=3)

        # 初始化所有UI元素为隐藏状态
        self._hide_all_elements()

    def _hide_all_elements(self) -> None:
        """隐藏所有UI元素."""
        for widget in self.ui_container.winfo_children():
            widget.grid_forget()

    def _toggle_mode(self) -> None:
        """切换Mode配置状态."""
        if self.mode_checkbox.get():
            self.mode_label.grid(row=0, column=0, padx=5, pady=2, sticky='w')
            self.mode_value_label.grid(row=1, column=0, padx=5, pady=2, sticky='e')
            self.cpu_mode.grid(row=1, column=0, padx=70, pady=2, sticky='w')
        else:
            self.mode_label.grid_forget()
            self.mode_value_label.grid_forget()
            self.cpu_mode.grid_forget()
        # 触发配置变更
        self._trigger_change()

    def _toggle_match(self) -> None:
        """切换Match配置状态."""
        if self.match_checkbox.get():
            self.match_label.grid(row=0, column=1, padx=5, pady=2, sticky='w')
            self.match_value_label.grid(row=1, column=1, padx=5, pady=2, sticky='e')
            self.cpu_match.grid(row=1, column=1, padx=70, pady=2, sticky='w')
        else:
            self.match_label.grid_forget()
            self.match_value_label.grid_forget()
            self.cpu_match.grid_forget()
        # 触发配置变更
        self._trigger_change()

    def _toggle_migratable(self) -> None:
        """切换Migratable配置状态."""
        if self.migratable_checkbox.get():
            self.migratable_label.grid(row=0, column=2, padx=5, pady=2, sticky='w')
            self.migratable_value_label.grid(row=1, column=2, padx=5, pady=2, sticky='e')
            self.cpu_migratable.grid(row=1, column=2, padx=70, pady=2, sticky='w')
        else:
            self.migratable_label.grid_forget()
            self.migratable_value_label.grid_forget()
            self.cpu_migratable.grid_forget()
        # 触发配置变更
        self._trigger_change()

    def _toggle_check(self) -> None:
        """切换Check配置状态."""
        if self.check_checkbox.get():
            self.check_label.grid(row=2, column=0, padx=5, pady=2, sticky='w')
            self.check_value_label.grid(row=3, column=0, padx=5, pady=2, sticky='e')
            self.cpu_check.grid(row=3, column=0, padx=70, pady=2, sticky='w')
        else:
            self.check_label.grid_forget()
            self.check_value_label.grid_forget()
            self.cpu_check.grid_forget()
        # 触发配置变更
        self._trigger_change()

    def _toggle_model(self) -> None:
        """切换Model配置状态."""
        if self.model_checkbox.get():
            self.model_label.grid(row=2, column=1, padx=5, pady=2, sticky='w')
            self.model_name_label.grid(row=3, column=1, padx=5, pady=2, sticky='e')
            self.cpu_model.grid(row=3, column=1, padx=70, pady=2, sticky='w')
            self.model_fallback_label.grid(row=4, column=1, padx=5, pady=2, sticky='e')
            self.cpu_fallback.grid(row=4, column=1, padx=70, pady=2, sticky='w')
        else:
            self.model_label.grid_forget()
            self.model_name_label.grid_forget()
            self.cpu_model.grid_forget()
            self.model_fallback_label.grid_forget()
            self.cpu_fallback.grid_forget()
            # 清空输入字段
            self.cpu_model.delete(0, 'end')
        # 触发配置变更
        self._trigger_change()

    def _toggle_vendor(self) -> None:
        """切换Vendor配置状态."""
        if self.vendor_checkbox.get():
            self.vendor_label.grid(row=2, column=2, padx=5, pady=2, sticky='w')
            self.vendor_name_label.grid(row=3, column=2, padx=5, pady=2, sticky='e')
            self.cpu_vendor.grid(row=3, column=2, padx=70, pady=2, sticky='w')
        else:
            self.vendor_label.grid_forget()
            self.vendor_name_label.grid_forget()
            self.cpu_vendor.grid_forget()
            # 清空输入字段
            self.cpu_vendor.delete(0, 'end')
        # 触发配置变更
        self._trigger_change()

    def _toggle_topology(self) -> None:
        """切换Topology配置状态."""
        if self.topology_checkbox.get():
            self.topology_label.grid(row=5, column=0, padx=5, pady=2, sticky='w')
            self.topology_sockets_label.grid(row=6, column=0, padx=5, pady=2, sticky='e')
            self.sockets.grid(row=6, column=0, padx=70, pady=2, sticky='w')
            self.topology_dies_label.grid(row=7, column=0, padx=5, pady=2, sticky='e')
            self.dies.grid(row=7, column=0, padx=70, pady=2, sticky='w')
            self.topology_clusters_label.grid(row=8, column=0, padx=5, pady=2, sticky='e')
            self.clusters.grid(row=8, column=0, padx=70, pady=2, sticky='w')
            self.topology_cores_label.grid(row=9, column=0, padx=5, pady=2, sticky='e')
            self.cores.grid(row=9, column=0, padx=70, pady=2, sticky='w')
            self.topology_threads_label.grid(row=10, column=0, padx=5, pady=2, sticky='e')
            self.threads.grid(row=10, column=0, padx=70, pady=2, sticky='w')
        else:
            self.topology_label.grid_forget()
            self.topology_sockets_label.grid_forget()
            self.sockets.grid_forget()
            self.topology_dies_label.grid_forget()
            self.dies.grid_forget()
            self.topology_clusters_label.grid_forget()
            self.clusters.grid_forget()
            self.topology_cores_label.grid_forget()
            self.cores.grid_forget()
            self.topology_threads_label.grid_forget()
            self.threads.grid_forget()
            # 清空输入字段
            self.sockets.delete(0, 'end')
            self.dies.delete(0, 'end')
            self.clusters.delete(0, 'end')
            self.cores.delete(0, 'end')
            self.threads.delete(0, 'end')
        # 触发配置变更
        self._trigger_change()

    def _toggle_cache(self) -> None:
        """切换Cache配置状态."""
        if self.cache_checkbox.get():
            self.cache_label.grid(row=5, column=1, padx=5, pady=2, sticky='w')
            self.cache_mode_label.grid(row=6, column=1, padx=5, pady=2, sticky='e')
            self.cache_mode.grid(row=6, column=1, padx=70, pady=2, sticky='w')
            self.cache_level_label.grid(row=7, column=1, padx=5, pady=2, sticky='e')
            self.cache_level.grid(row=7, column=1, padx=70, pady=2, sticky='w')
        else:
            self.cache_label.grid_forget()
            self.cache_mode_label.grid_forget()
            self.cache_mode.grid_forget()
            self.cache_level_label.grid_forget()
            self.cache_level.grid_forget()
            # 清空输入字段
            self.cache_level.delete(0, 'end')
        # 触发配置变更
        self._trigger_change()

    def _toggle_maxphysaddr(self) -> None:
        """切换Maxphysaddr配置状态."""
        if self.maxphysaddr_checkbox.get():
            self.maxphysaddr_label.grid(row=5, column=2, padx=5, pady=2, sticky='w')
            self.maxphysaddr_mode_label.grid(row=6, column=2, padx=5, pady=2, sticky='e')
            self.maxphysaddr_mode.grid(row=6, column=2, padx=70, pady=2, sticky='w')
            self.maxphysaddr_bits_label.grid(row=7, column=2, padx=5, pady=2, sticky='e')
            self.maxphysaddr_bits.grid(row=7, column=2, padx=70, pady=2, sticky='w')
        else:
            self.maxphysaddr_label.grid_forget()
            self.maxphysaddr_mode_label.grid_forget()
            self.maxphysaddr_mode.grid_forget()
            self.maxphysaddr_bits_label.grid_forget()
            self.maxphysaddr_bits.grid_forget()
            # 清空输入字段
            self.maxphysaddr_bits.delete(0, 'end')
        # 触发配置变更
        self._trigger_change()

    def _toggle_feature(self) -> None:
        """切换Feature配置状态."""
        if self.feature_checkbox.get():
            self.feature_label.grid(row=8, column=1, padx=5, pady=2, sticky='w')
            self.feature_name_label.grid(row=9, column=1, padx=5, pady=2, sticky='e')
            self.feature_name.grid(row=9, column=1, padx=70, pady=2, sticky='w')
            self.feature_policy_label.grid(row=10, column=1, padx=5, pady=2, sticky='e')
            self.feature_policy.grid(row=10, column=1, padx=70, pady=2, sticky='w')
        else:
            self.feature_label.grid_forget()
            self.feature_name_label.grid_forget()
            self.feature_name.grid_forget()
            self.feature_policy_label.grid_forget()
            self.feature_policy.grid_forget()
            # 清空输入字段
            self.feature_name.delete(0, 'end')
        # 触发配置变更
        self._trigger_change()

    def get_config(self) -> dict:
        """获取配置数据."""
        config = {}

        # Mode配置
        if self.mode_checkbox.get():
            config['mode'] = self.cpu_mode.get()

        # Match配置
        if self.match_checkbox.get():
            config['match'] = self.cpu_match.get()

        # Check配置
        if self.check_checkbox.get():
            config['check'] = self.cpu_check.get() if self.cpu_check.get() else None

        # Migratable配置
        if self.migratable_checkbox.get():
            config['migratable'] = self.cpu_migratable.get()

        # Model配置
        if self.model_checkbox.get():
            config['model'] = self.cpu_model.get() if self.cpu_model.get() else None
            config['fallback'] = self.cpu_fallback.get()

        # Vendor配置
        if self.vendor_checkbox.get():
            config['vendor'] = self.cpu_vendor.get() if self.cpu_vendor.get() else None

        # Topology配置
        if self.topology_checkbox.get():
            config['topology'] = {
                'sockets': parse_integer_value(self.sockets.get(), default=1),
                'dies': parse_integer_value(self.dies.get(), default=1),
                'clusters': parse_integer_value(self.clusters.get(), default=1),
                'cores': parse_integer_value(self.cores.get(), default=2),
                'threads': parse_integer_value(self.threads.get(), default=1),
            }

        # Cache配置
        if self.cache_checkbox.get():
            config['cache'] = {
                'mode': self.cache_mode.get() if self.cache_mode.get() else None,
                'level': parse_integer_value(self.cache_level.get())
                if self.cache_level.get()
                else None,
            }

        # Maxphysaddr配置
        if self.maxphysaddr_checkbox.get():
            config['maxphysaddr'] = {
                'mode': self.maxphysaddr_mode.get(),
                'bits': parse_integer_value(self.maxphysaddr_bits.get())
                if self.maxphysaddr_bits.get()
                else None,
            }

        # Feature配置
        if self.feature_checkbox.get():
            config['feature'] = {
                'name': self.feature_name.get() if self.feature_name.get() else None,
                'policy': self.feature_policy.get(),
            }

        return config

    def to_xml(self) -> dict:
        """生成XML配置字典."""
        config = self.get_config()

        # 构建XML格式的配置
        cpu_config = {}

        # 添加属性
        if config.get('match'):
            cpu_config['match'] = config['match']
        if config.get('check'):
            cpu_config['check'] = config['check']
        if config.get('mode'):
            cpu_config['mode'] = config['mode']
        if config.get('migratable'):
            cpu_config['migratable'] = config['migratable']

        # 添加子元素
        children = []

        # Model元素
        if config.get('model'):
            model_elem = {'model': config['model']}
            if config.get('fallback'):
                model_elem['fallback'] = config['fallback']
            children.append(model_elem)

        # Vendor元素
        if config.get('vendor'):
            children.append({'vendor': config['vendor']})

        # Topology元素
        if config.get('topology'):
            topology = config['topology']
            topology_elem = {
                'topology': {
                    'sockets': str(topology['sockets']),
                    'dies': str(topology['dies']),
                    'clusters': str(topology['clusters']),
                    'cores': str(topology['cores']),
                    'threads': str(topology['threads']),
                }
            }
            children.append(topology_elem)

        # Cache元素
        if config.get('cache') and config['cache'].get('mode'):
            cache = config['cache']
            cache_elem = {'cache': {'mode': cache['mode']}}
            if cache.get('level'):
                cache_elem['cache']['level'] = str(cache['level'])
            children.append(cache_elem)

        # Maxphysaddr元素
        if config.get('maxphysaddr'):
            maxphysaddr = config['maxphysaddr']
            maxphysaddr_elem = {'maxphysaddr': {'mode': maxphysaddr['mode']}}
            if maxphysaddr.get('bits'):
                maxphysaddr_elem['maxphysaddr']['bits'] = str(maxphysaddr['bits'])
            if maxphysaddr.get('limit'):
                maxphysaddr_elem['maxphysaddr']['limit'] = str(maxphysaddr['limit'])
            children.append(maxphysaddr_elem)

        # Feature元素
        if config.get('feature') and config['feature'].get('name'):
            feature = config['feature']
            feature_elem = {'feature': {'name': feature['name'], 'policy': feature['policy']}}
            children.append(feature_elem)

        # 添加子元素到cpu配置
        if children:
            cpu_config['children'] = children

        # 始终返回 cpu_allocation 键，即使 cpu 为空
        return {'cpu_allocation': {'cpu': cpu_config}}
