"""Tab 切换开关 - 根据开关状态动态添加/删除 Tab."""

import customtkinter as ctk

from .styles import CTK_FONT_MAIN, CTK_FONT_BOLD, CTK_FONT_SMALL, BG_COLOR_CONTENT


class TabToggleSwitch(ctk.CTkFrame):
    """Tab 切换开关组件."""

    def __init__(
        self,
        master,
        tab_name: str,
        tab_display_name: str,
        on_change_callback=None,
        disabled: bool = False,
        default_on: bool = True,
        **kwargs
    ):
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent')

        self.tab_name = tab_name
        self.tab_display_name = tab_display_name
        self.on_change_callback = on_change_callback
        self.disabled = disabled

        # 创建开关变量和控件
        self.toggle_var = ctk.BooleanVar(value=default_on and not disabled)

        self.toggle_switch = ctk.CTkCheckBox(
            self,
            text=tab_display_name,
            variable=self.toggle_var,
            command=self._on_toggle,
            state='disabled' if disabled else 'normal',
            font=CTK_FONT_SMALL,
        )
        self.toggle_switch.pack(side='left', padx=5, pady=2)

    def _on_toggle(self) -> None:
        """开关状态改变时的回调."""
        if self.on_change_callback:
            self.on_change_callback(self.tab_name, self.toggle_var.get())

    def set_state(self, enabled: bool) -> None:
        """设置开关状态."""
        self.toggle_var.set(enabled)

    def is_enabled(self) -> bool:
        """获取开关状态."""
        return self.toggle_var.get()


class TabTogglePanel(ctk.CTkFrame):
    """Tab 切换开关面板 - 管理所有 Tab 的开关."""

    # 定义所有 Tab 的配置
    TABS_CONFIG = {
        'basic': {'name': '基础配置', 'disabled': False, 'default_on': True},
        'os': {'name': '引导/OS', 'disabled': False, 'default_on': True},
        'storage': {'name': '存储', 'disabled': False, 'default_on': True},
        'network': {'name': '网络', 'disabled': False, 'default_on': True},
        'devices': {'name': '设备', 'disabled': False, 'default_on': True},
        'features': {'name': '功能特性', 'disabled': False, 'default_on': False},
        'hostdev': {'name': 'PCI 直通', 'disabled': False, 'default_on': False},
        'memory': {'name': '内存管理', 'disabled': False, 'default_on': False},
        'clock': {'name': '时钟/看门狗', 'disabled': False, 'default_on': False},
    }

    def __init__(self, master, on_tab_toggle_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color=BG_COLOR_CONTENT, corner_radius=6)

        self.on_tab_toggle_callback = on_tab_toggle_callback
        self.toggle_switches = {}
        self.expanded = True

        # 创建开关面板
        self._create_switches()

    def _create_switches(self) -> None:
        """创建所有 Tab 的开关."""
        # 标题
        ctk.CTkLabel(
            self,
            text='Tab 显示控制:',
            font=CTK_FONT_BOLD,
            text_color='#64b5f6',
        ).grid(row=0, column=0, padx=10, pady=5, sticky='w')

        # 创建开关 - 两行布局
        tab_keys = list(self.TABS_CONFIG.keys())
        mid_point = len(tab_keys) // 2

        # 第一行
        for i, tab_key in enumerate(tab_keys[:mid_point]):
            tab_config = self.TABS_CONFIG[tab_key]
            switch = TabToggleSwitch(
                self,
                tab_name=tab_key,
                tab_display_name=tab_config['name'],
                on_change_callback=self._on_tab_toggle,
                disabled=tab_config['disabled'],
                default_on=tab_config.get('default_on', True),
            )
            switch.grid(row=1, column=i+1, padx=8, pady=2, sticky='w')
            self.toggle_switches[tab_key] = switch

        # 第二行
        for i, tab_key in enumerate(tab_keys[mid_point:]):
            tab_config = self.TABS_CONFIG[tab_key]
            switch = TabToggleSwitch(
                self,
                tab_name=tab_key,
                tab_display_name=tab_config['name'],
                on_change_callback=self._on_tab_toggle,
                disabled=tab_config['disabled'],
                default_on=tab_config.get('default_on', True),
            )
            switch.grid(row=2, column=i+1, padx=8, pady=2, sticky='w')
            self.toggle_switches[tab_key] = switch

        # 展开/收起按钮
        self.toggle_btn = ctk.CTkButton(
            self,
            text='▼',
            width=30,
            fg_color='transparent',
            border_width=1,
            hover_color='#e0e0e0',
            font=CTK_FONT_SMALL,
            command=self._toggle_panel,
        )
        btn_col = max(mid_point, len(tab_keys) - mid_point) + 2
        self.toggle_btn.grid(row=1, column=btn_col, rowspan=2, padx=5, pady=2, sticky='e')

    def _on_tab_toggle(self, tab_name: str, enabled: bool) -> None:
        """Tab 开关改变时的回调."""
        if self.on_tab_toggle_callback:
            self.on_tab_toggle_callback(tab_name, enabled)

    def _toggle_panel(self) -> None:
        """展开/收起面板."""
        if self.expanded:
            # 收起 - 隐藏第二行
            mid_point = len(self.TABS_CONFIG) // 2
            for i, (tab_key, switch) in enumerate(self.toggle_switches.items()):
                if i >= mid_point:
                    switch.grid_remove()
            self.toggle_btn.configure(text='▲')
            self.expanded = False
        else:
            # 展开 - 显示所有
            mid_point = len(self.TABS_CONFIG) // 2
            for i, (tab_key, switch) in enumerate(self.toggle_switches.items()):
                if i < mid_point:
                    switch.grid(row=1, column=i+1, padx=8, pady=2, sticky='w')
                else:
                    switch.grid(row=2, column=(i-mid_point)+1, padx=8, pady=2, sticky='w')
            self.toggle_btn.configure(text='▼')
            self.expanded = True

    def set_tab_state(self, tab_name: str, enabled: bool) -> None:
        """设置指定 Tab 的开关状态."""
        if tab_name in self.toggle_switches:
            self.toggle_switches[tab_name].set_state(enabled)

    def get_tab_state(self, tab_name: str) -> bool:
        """获取指定 Tab 的开关状态."""
        if tab_name in self.toggle_switches:
            return self.toggle_switches[tab_name].is_enabled()
        return False

    def get_all_states(self) -> dict:
        """获取所有 Tab 的开关状态."""
        return {
            tab_name: switch.is_enabled()
            for tab_name, switch in self.toggle_switches.items()
        }
