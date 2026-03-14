"""Tab 切换开关 - 管理 24 个 Tab 的显示/隐藏."""

from collections.abc import Callable
from typing import ClassVar

import customtkinter as ctk

from config.tabs_config import TABS_CONFIG
from utils.color import get_random_color
from utils.styles import CTK_FONT_BOLD, CTK_FONT_MAIN


class TabToggleSwitch(ctk.CTkFrame):
    """Tab 切换开关组件."""

    def __init__(
        self,
        master,
        tab_key: str,
        tab_display_name: str,
        on_change_callback: Callable[[str, bool], None] | None = None,
        default_on: bool = True,
        text_color: str | None = None,
        **kwargs,
    ):
        """初始化 Tab 切换开关组件.

        Args:
            master: 父组件
            tab_key: Tab 的唯一标识符
            tab_display_name: Tab 的显示名称
            on_change_callback: 状态改变时的回调函数
            default_on: 默认是否启用
            text_color: 文本颜色, None 则随机选择
            **kwargs: 其他参数
        """
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent')

        self.tab_key = tab_key
        self.tab_display_name = tab_display_name
        self.on_change_callback = on_change_callback

        self.toggle_var = ctk.BooleanVar(value=default_on)

        # 如果没有指定颜色, 随机选择一个
        self.text_color = text_color if text_color else get_random_color()

        self.toggle_switch = ctk.CTkCheckBox(
            self,
            text=tab_display_name,
            variable=self.toggle_var,
            command=self._on_toggle,
            font=CTK_FONT_MAIN,
            checkbox_width=14,
            checkbox_height=14,
            text_color=self.text_color,
        )
        self.toggle_switch.pack(side='left', padx=2, pady=0)

    def _on_toggle(self) -> None:
        """开关状态改变时的回调."""
        if self.on_change_callback:
            self.on_change_callback(self.tab_key, self.toggle_var.get())

    def set_state(self, enabled: bool) -> None:
        """设置开关状态.

        Args:
            enabled: 是否启用
        """
        self.toggle_var.set(enabled)

    def is_enabled(self) -> bool:
        """获取开关状态.

        Returns:
            bool: 是否启用
        """
        return self.toggle_var.get()


class TabTogglePanel(ctk.CTkFrame):
    """Tab 切换开关面板 - 管理 24 个 Tab 的开关."""

    # 面板配置
    PANEL_CONFIG: ClassVar[dict] = {
        'label_text': 'vm cfgs:',
        'label_color': '#64b5f6',
        'max_columns': 12,
        'grid_padx': 1,
        'grid_pady': 0,
    }

    def __init__(
        self, master, on_tab_toggle_callback: Callable[[str, bool], None] | None = None, **kwargs
    ):
        """初始化 Tab 切换开关面板.

        Args:
            master: 父组件
            on_tab_toggle_callback: Tab 状态改变时的回调函数
            **kwargs: 其他参数
        """
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent')

        self.on_tab_toggle_callback = on_tab_toggle_callback
        self.toggle_switches: dict[str, TabToggleSwitch] = {}
        self.expanded = True

        self._create_ui()

    def _create_ui(self) -> None:
        """创建完整的 UI 布局."""
        # 主面板配置 - 紧凑布局
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 内容框架
        content_frame = ctk.CTkFrame(self, fg_color='transparent')
        content_frame.grid(row=0, column=0, sticky='ew', pady=5)

        # 标签
        self._create_label(content_frame)

        # 创建开关框架 - 用于网格布局
        switch_frame = ctk.CTkFrame(content_frame, fg_color='transparent')
        switch_frame.pack(side='left', fill='x', expand=True)

        # 创建开关网格
        self._create_switch_grid(switch_frame)

    def _create_label(self, parent_frame: ctk.CTkFrame) -> None:
        """创建面板标签.

        Args:
            parent_frame: 父框架
        """
        ctk.CTkLabel(
            parent_frame,
            text=self.PANEL_CONFIG['label_text'],
            font=CTK_FONT_BOLD,
            text_color=self.PANEL_CONFIG['label_color'],
        ).pack(side='left', padx=(3, 5), pady=0)

    def _create_switch_grid(self, parent_frame: ctk.CTkFrame) -> None:
        """创建开关网格布局.

        Args:
            parent_frame: 父框架
        """
        max_cols = self.PANEL_CONFIG['max_columns']
        grid_padx = self.PANEL_CONFIG['grid_padx']
        grid_pady = self.PANEL_CONFIG['grid_pady']

        for i, (tab_key, config) in enumerate(TABS_CONFIG.items()):
            row = i // max_cols
            col = i % max_cols

            switch = TabToggleSwitch(
                parent_frame,
                tab_key=tab_key,
                tab_display_name=config['name'],
                on_change_callback=self._on_toggle,
                default_on=config.get('default_on', True),
            )
            switch.grid(row=row, column=col, padx=grid_padx, pady=grid_pady, sticky='w')
            self.toggle_switches[tab_key] = switch

    def _on_toggle(self, tab_key: str, enabled: bool) -> None:
        """Tab 开关改变时的回调.

        Args:
            tab_key: Tab 的唯一标识符
            enabled: 是否启用
        """
        if self.on_tab_toggle_callback:
            self.on_tab_toggle_callback(tab_key, enabled)

    def set_tab_state(self, tab_key: str, enabled: bool) -> bool:
        """设置指定 Tab 的开关状态.

        Args:
            tab_key: Tab 的唯一标识符
            enabled: 是否启用

        Returns:
            bool: 操作是否成功
        """
        if tab_key in self.toggle_switches:
            self.toggle_switches[tab_key].set_state(enabled)
            return True
        return False

    def get_tab_state(self, tab_key: str) -> bool:
        """获取指定 Tab 的开关状态.

        Args:
            tab_key: Tab 的唯一标识符

        Returns:
            bool: 是否启用
        """
        return (
            self.toggle_switches.get(tab_key, TabToggleSwitch).is_enabled()
            if hasattr(TabToggleSwitch, 'is_enabled')
            else False
        )

    def get_all_states(self) -> dict[str, bool]:
        """获取所有 Tab 的开关状态.

        Returns:
            dict: 所有 Tab 的状态字典
        """
        return {tab_key: switch.is_enabled() for tab_key, switch in self.toggle_switches.items()}

    def toggle_all(self, enabled: bool) -> None:
        """批量设置所有 Tab 的开关状态.

        Args:
            enabled: 是否启用所有 Tab
        """
        for switch in self.toggle_switches.values():
            switch.set_state(enabled)

    def get_enabled_tabs(self) -> list[str]:
        """获取所有启用的 Tab 列表.

        Returns:
            list: 启用的 Tab 键列表
        """
        return [tab_key for tab_key, enabled in self.get_all_states().items() if enabled]

    def get_disabled_tabs(self) -> list[str]:
        """获取所有禁用的 Tab 列表.

        Returns:
            list: 禁用的 Tab 键列表
        """
        return [tab_key for tab_key, enabled in self.get_all_states().items() if not enabled]
