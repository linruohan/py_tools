"""事件切换开关 - 带开关和 enabled 下拉选择框的组合组件."""

import customtkinter as ctk

from utils.styles import CTK_FONT_MAIN, CTK_FONT_SMALL


class EventToggleSwitch(ctk.CTkFrame):
    """事件切换开关组件 - 开关 + enabled 下拉框.

    用于性能监控事件配置，支持:
    - 开关关闭：不生成该事件的 XML
    - 开关开启 + enabled=yes: 生成 enabled='yes' 的事件
    - 开关开启 + enabled=no: 生成 enabled='no' 的事件
    """

    def __init__(
        self,
        master,
        event_name: str,
        event_desc: str,
        on_change_callback=None,
        default_enabled: bool = False,
        default_enabled_value: str = 'yes',
        **kwargs,
    ):
        """初始化事件切换开关.

        Args:
            master: 父组件
            event_name: 事件名称 (如 'cmt', 'cpu_cycles')
            event_desc: 事件描述
            on_change_callback: 状态改变时的回调
            default_enabled: 默认是否启用开关
            default_enabled_value: 默认 enabled 值 ('yes' 或 'no')
            **kwargs: 其他参数
        """
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent')

        self.event_name = event_name
        self.on_change_callback = on_change_callback

        # 开关状态
        self.enabled_var = ctk.BooleanVar(value=default_enabled)
        # enabled 值 (yes/no)
        self.enabled_value_var = ctk.StringVar(value=default_enabled_value)

        self._create_ui()

    def _create_ui(self) -> None:
        """创建 UI 布局."""
        # 开关复选框
        self.checkbox = ctk.CTkCheckBox(
            self,
            text=self.event_name,
            variable=self.enabled_var,
            command=self._on_change,
            font=CTK_FONT_SMALL,
            checkbox_width=14,
            checkbox_height=14,
        )
        self.checkbox.pack(side='left', padx=2, pady=2)

        # enabled 下拉框 (初始隐藏)
        self.enabled_menu = ctk.CTkOptionMenu(
            self,
            values=['yes', 'no'],
            variable=self.enabled_value_var,
            command=self._on_change,
            font=CTK_FONT_SMALL,
            width=55,
        )
        self.enabled_menu.pack(side='left', padx=2, pady=2)

        # 根据开关状态显示/隐藏下拉框
        self._update_visibility()

    def _on_change(self, *args) -> None:
        """状态改变时的回调."""
        self._update_visibility()
        if self.on_change_callback:
            self.on_change_callback(self.event_name, self.get_state())

    def _update_visibility(self) -> None:
        """根据开关状态更新下拉框可见性."""
        if self.enabled_var.get():
            self.enabled_menu.pack(side='left', padx=2, pady=2)
        else:
            self.enabled_menu.pack_forget()

    def get_state(self) -> tuple[bool, str]:
        """获取当前状态.

        Returns:
            (enabled, enabled_value) 元组
            - enabled: 开关是否开启
            - enabled_value: 'yes' 或 'no'
        """
        return (self.enabled_var.get(), self.enabled_value_var.get())

    def set_state(self, enabled: bool, enabled_value: str = 'yes') -> None:
        """设置状态.

        Args:
            enabled: 是否启用开关
            enabled_value: 'yes' 或 'no'
        """
        self.enabled_var.set(enabled)
        self.enabled_value_var.set(enabled_value)
        self._update_visibility()

    def is_enabled(self) -> bool:
        """获取开关状态.

        Returns:
            bool: 是否启用
        """
        return self.enabled_var.get()
