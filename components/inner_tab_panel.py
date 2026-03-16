"""内部 Tab 切换面板 - 用于 Tab 内部的子选项切换."""

import customtkinter as ctk

from utils.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_SMALL


class InnerTabPanel(ctk.CTkFrame):
    """内部 Tab 切换面板 - 使用按钮组实现子选项切换."""

    def __init__(
        self,
        master,
        tabs_config: dict,
        on_change_callback=None,
        **kwargs,
    ):
        """初始化内部 Tab 面板.

        Args:
            master: 父容器
            tabs_config: Tab 配置字典,格式为:
                {
                    'tab_key': {
                        'name': '显示名称',
                        'class': TabClass,  # 可选,如果没有则为空
                        'default': False,  # 是否默认显示
                    }
                }
            on_change_callback: 变化回调函数
        """
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent')

        self.tabs_config = tabs_config
        self.on_change_callback = on_change_callback
        self.tab_instances = {}
        self.current_tab = None
        self.tab_buttons = {}

        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        button_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        button_frame.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
        # 允许按钮框架水平扩展
        button_frame.grid_columnconfigure(0, weight=1)

        content_frame = ctk.CTkFrame(self, fg_color='transparent')
        content_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)

        self.content_frame = content_frame

        # 使用CTKScrollableFrame来实现可滚动的按钮面板
        from customtkinter import CTkScrollableFrame

        scrollable_frame = CTkScrollableFrame(button_frame)
        scrollable_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

        col = 0
        row = 0
        max_cols = 11  # 每行最多显示6个按钮
        first_tab = None
        for tab_key, config in self.tabs_config.items():
            is_default = config.get('default', False)
            if first_tab is None or is_default:
                first_tab = tab_key

            btn = ctk.CTkButton(
                scrollable_frame,
                text=config['name'],
                width=140,
                height=28,
                fg_color='#3B8ED0' if is_default else '#555555',
                hover_color='#1F6AA5' if is_default else '#444444',
                font=CTK_FONT_SMALL,
                command=lambda k=tab_key: self._switch_tab(k),
            )
            btn.grid(row=row, column=col, padx=3, pady=3, sticky='w')
            self.tab_buttons[tab_key] = btn

            col += 1
            if col >= max_cols:
                col = 0
                row += 1

        if first_tab:
            self._switch_tab(first_tab, initial=True)

    def _switch_tab(self, tab_key: str, initial: bool = False) -> None:
        """切换到指定的 Tab.

        Args:
            tab_key: Tab 键名
            initial: 是否是初始化切换
        """
        if tab_key == self.current_tab and not initial:
            return

        for key, btn in self.tab_buttons.items():
            if key == tab_key:
                btn.configure(fg_color='#3B8ED0', hover_color='#1F6AA5')
            else:
                btn.configure(fg_color='#555555', hover_color='#444444')

        if self.current_tab and self.current_tab in self.tab_instances:
            self.tab_instances[self.current_tab].grid_remove()

        self.current_tab = tab_key

        if tab_key not in self.tab_instances:
            config = self.tabs_config.get(tab_key, {})
            tab_class = config.get('class')

            if tab_class:
                tab_instance = tab_class(
                    self.content_frame,
                    on_change_callback=self.on_change_callback,
                )
            else:
                tab_instance = ctk.CTkFrame(
                    self.content_frame, fg_color=BG_COLOR_CONTENT, corner_radius=6
                )
                ctk.CTkLabel(
                    tab_instance,
                    text=f'{config.get("name", tab_key)} - 配置项',
                    font=CTK_FONT_BOLD,
                    text_color='#888888',
                ).pack(padx=20, pady=20)

            tab_instance.grid(row=0, column=0, sticky='nsew')
            self.tab_instances[tab_key] = tab_instance
        else:
            self.tab_instances[tab_key].grid()

        if self.on_change_callback and not initial:
            self.on_change_callback()

    def get_current_tab(self) -> str:
        """获取当前显示的 Tab 键名."""
        return self.current_tab

    def get_tab_instance(self, tab_key: str):
        """获取指定 Tab 的实例."""
        return self.tab_instances.get(tab_key)

    def collect_data(self) -> dict:
        """收集所有 Tab 的数据."""
        data = {}
        for tab_key, tab_instance in self.tab_instances.items():
            if hasattr(tab_instance, 'get_config'):
                data[tab_key] = tab_instance.get_config()
        return data
