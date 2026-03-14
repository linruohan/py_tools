"""可折叠面板组件 - 用于组织模块内部的配置组."""

import customtkinter as ctk

from .styles import CTK_FONT_BOLD


class AccordionFrame(ctk.CTkFrame):
    """可折叠面板组件."""

    def __init__(
        self,
        master,
        title: str = '',
        default_expanded: bool = True,
        on_toggle_callback=None,
        **kwargs,
    ):
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent')

        self.title = title
        self.default_expanded = default_expanded
        self.on_toggle_callback = on_toggle_callback
        self.expanded = default_expanded

        # 配置 grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # 标题栏
        self.grid_rowconfigure(1, weight=1)  # 内容区

        # 标题栏
        self.header_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.header_frame.grid(row=0, column=0, sticky='ew')
        self.header_frame.grid_columnconfigure(1, weight=1)

        # 展开/收起图标
        self.toggle_icon = ctk.CTkLabel(
            self.header_frame,
            text='▼',
            width=20,
            font=ctk.CTkFont(size=12),
        )
        self.toggle_icon.grid(row=0, column=0, padx=(0, 5), sticky='w')

        # 标题
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text=title,
            font=CTK_FONT_BOLD,
            text_color='#64b5f6',
        )
        self.title_label.grid(row=0, column=1, sticky='w')

        # 绑定点击事件
        self.header_frame.bind('<Button-1>', self._on_toggle)
        self.toggle_icon.bind('<Button-1>', self._on_toggle)
        self.title_label.bind('<Button-1>', self._on_toggle)

        # 内容区
        self.content_frame = ctk.CTkFrame(self, fg_color='transparent')
        if self.expanded:
            self.content_frame.grid(row=1, column=0, sticky='nsew', pady=(5, 0))
        else:
            self.content_frame.grid_remove()

        # 内容区 grid 配置 - 由外部设置
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

    def _on_toggle(self, event=None):
        """切换展开/收起状态."""
        self.expanded = not self.expanded
        if self.expanded:
            self.content_frame.grid()
            self.toggle_icon.configure(text='▼')
        else:
            self.content_frame.grid_remove()
            self.toggle_icon.configure(text='▶')

        if self.on_toggle_callback:
            self.on_toggle_callback(self.expanded)

    def expand(self):
        """展开面板."""
        if not self.expanded:
            self._on_toggle()

    def collapse(self):
        """收起面板."""
        if self.expanded:
            self._on_toggle()

    def get_content_frame(self):
        """获取内容区 Frame, 用于添加子控件."""
        return self.content_frame


class AccordionPanel(ctk.CTkScrollableFrame):
    """可折叠面板容器 - 用于管理多个 AccordionFrame."""

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent')
        self.grid_columnconfigure(0, weight=1)
        self._row_counter = 0

        self.accordions = {}

    def add_accordion(
        self,
        key: str,
        title: str,
        default_expanded: bool = True,
        on_toggle_callback=None,
    ) -> AccordionFrame:
        """添加一个可折叠面板."""
        accordion = AccordionFrame(
            self,
            title=title,
            default_expanded=default_expanded,
            on_toggle_callback=on_toggle_callback,
        )
        accordion.grid(row=self._row_counter, column=0, sticky='nsew', pady=(5, 0))
        self._row_counter += 1

        self.accordions[key] = accordion
        return accordion

    def get_accordion(self, key: str) -> AccordionFrame | None:
        """获取指定 key 的面板."""
        return self.accordions.get(key)

    def expand_all(self):
        """展开所有面板."""
        for accordion in self.accordions.values():
            accordion.expand()

    def collapse_all(self):
        """收起所有面板."""
        for accordion in self.accordions.values():
            accordion.collapse()
