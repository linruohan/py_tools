"""搜索筛选组件 - 参考customtkinter下拉框实现."""

import customtkinter as ctk

from utils.styles import BG_COLOR_CONTENT, CTK_FONT_MAIN, CTK_FONT_SMALL


class SearchFilter(ctk.CTkFrame):
    """搜索筛选组件 - 参考customtkinter下拉框实现."""

    def __init__(
        self,
        master,
        items: list | None = None,
        on_select_callback=None,
        placeholder_text='请输入关键词...',
        **kwargs,
    ):
        """初始化搜索筛选组件.

        Args:
            master: 父容器
            items: 初始列表项
            on_select_callback: 选中回调函数
            placeholder_text: 输入框占位文本
        """
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent')

        self.items = items or []
        self.filtered_items = self.items.copy()
        self.on_select_callback = on_select_callback
        self.placeholder_text = placeholder_text
        self.current_selection = -1
        self.dropdown_frame = None

        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)

        # 计算并设置最大宽度(在创建输入框之前)
        self._max_width = self._calculate_max_width()

        # 输入框
        self.search_entry = ctk.CTkEntry(
            self,
            placeholder_text=self.placeholder_text,
            font=CTK_FONT_MAIN,
            fg_color=BG_COLOR_CONTENT,
            border_width=1,
            width=self._max_width,
        )
        self.search_entry.grid(row=0, column=0, sticky='ew', padx=0, pady=0)
        self.search_entry.bind('<KeyRelease>', self._on_search)
        self.search_entry.bind('<FocusIn>', self._on_focus_in)
        self.search_entry.bind('<Down>', self._on_arrow_down)
        self.search_entry.bind('<Up>', self._on_arrow_up)
        self.search_entry.bind('<Return>', self._on_enter)
        self.search_entry.bind('<FocusOut>', self._on_focus_out)

    def _calculate_max_width(self) -> int:
        """计算最大宽度(基于最长列表项)."""
        if not self.items:
            return 200  # 默认宽度

        # 创建一个临时标签来测量文本宽度
        temp_label = ctk.CTkLabel(self, font=CTK_FONT_MAIN)
        max_width = 0
        for item in self.items:
            temp_label.configure(text=str(item))
            width = temp_label.winfo_reqwidth()
            if width > max_width:
                max_width = width
        temp_label.destroy()

        # 添加一些额外的空间(边距和滚动条空间)
        max_width += 60
        return max_width

    def _update_max_width(self) -> None:
        """更新最大宽度(当列表项变化时)."""
        self._max_width = self._calculate_max_width()
        # 设置输入框的最小宽度
        self.search_entry.configure(width=self._max_width)

    def _on_focus_in(self, event) -> None:
        """获得焦点处理."""
        # 当输入框获得焦点时,显示所有列表项
        self.filtered_items = self.items.copy()
        self.current_selection = -1 if not self.filtered_items else 0
        self._show_dropdown()

    def _on_search(self, event) -> None:
        """搜索输入处理."""
        keyword = self.search_entry.get().lower()
        if not keyword:
            self.filtered_items = self.items.copy()
        else:
            self.filtered_items = [item for item in self.items if keyword in str(item).lower()]
        self.current_selection = -1 if not self.filtered_items else 0
        self._show_dropdown()

    def _on_arrow_down(self, event) -> None:
        """向下箭头处理."""
        if self.filtered_items:
            self.current_selection = (self.current_selection + 1) % len(self.filtered_items)
            self._update_dropdown()

    def _on_arrow_up(self, event) -> None:
        """向上箭头处理."""
        if self.filtered_items:
            self.current_selection = (self.current_selection - 1) % len(self.filtered_items)
            self._update_dropdown()

    def _on_enter(self, event) -> None:
        """回车键处理."""
        if self.filtered_items and self.current_selection >= 0:
            selected_item = self.filtered_items[self.current_selection]
            self._select_item(selected_item)

    def _on_focus_out(self, event) -> None:
        """失去焦点处理."""
        # 延迟隐藏,以便点击下拉项时能触发选择
        self.after(200, self._hide_dropdown)

    def _on_item_click(self, item) -> None:
        """列表项点击处理."""
        self._select_item(item)

    def _show_dropdown(self) -> None:
        """显示下拉列表."""
        # 隐藏现有下拉框
        self._hide_dropdown()

        if not self.filtered_items:
            return

        # 获取输入框的宽度
        entry_width = self.search_entry.winfo_width()

        # 创建下拉框架,显示在输入框下方
        # width 和 height 必须在构造函数中设置(customtkinter 要求)
        self.dropdown_frame = ctk.CTkFrame(
            self,
            fg_color=BG_COLOR_CONTENT,
            corner_radius=0,
            border_width=1,
            border_color='#555555',
            height=150,  # 固定高度
            width=entry_width,  # 使用输入框的宽度
        )
        # 使用grid布局将下拉框显示在输入框下方
        assert self.dropdown_frame is not None
        self.dropdown_frame.grid(row=1, column=0, sticky='ew', padx=0, pady=0)
        self.dropdown_frame.grid_columnconfigure(0, weight=1)

        # 可滚动列表
        from customtkinter import CTkScrollableFrame

        scrollable_frame = CTkScrollableFrame(
            self.dropdown_frame, fg_color=BG_COLOR_CONTENT, corner_radius=0, border_width=0
        )
        scrollable_frame.pack(fill='both', expand=True, padx=0, pady=0)
        scrollable_frame.grid_columnconfigure(0, weight=1)

        # 添加列表项
        for i, item in enumerate(self.filtered_items):  # 显示所有匹配的条目
            is_selected = i == self.current_selection
            label = ctk.CTkLabel(
                scrollable_frame,
                text=str(item),
                font=CTK_FONT_SMALL,
                fg_color='#404040' if is_selected else 'transparent',
                corner_radius=4,
                cursor='hand2',
                anchor='w',  # 左对齐
            )
            label.pack(fill='x', padx=5, pady=2)
            label.bind('<Button-1>', lambda e, item=item: self._on_item_click(item))

    def _update_dropdown(self) -> None:
        """更新下拉列表."""
        if self.dropdown_frame:
            self._hide_dropdown()
            self._show_dropdown()

    def _hide_dropdown(self) -> None:
        """隐藏下拉列表."""
        if self.dropdown_frame:
            self.dropdown_frame.destroy()
            self.dropdown_frame = None

    def _select_item(self, item) -> None:
        """选择列表项."""
        # 先隐藏下拉框
        self._hide_dropdown()

        # 更新输入框
        self.search_entry.delete(0, 'end')
        self.search_entry.insert(0, str(item))

        # 让输入框失去焦点,防止下拉列表再次出现
        self.master.focus_set()

        # 调用回调函数
        if self.on_select_callback:
            self.on_select_callback(item)

    def set_items(self, items: list) -> None:
        """设置列表项.

        Args:
            items: 新的列表项
        """
        self.items = items
        self.filtered_items = self.items.copy()
        self.current_selection = -1 if not self.filtered_items else 0
        # 更新最大宽度
        self._update_max_width()

    def get_selected_item(self):
        """获取当前选中的项.

        Returns:
            当前选中的项,如果没有选中则返回 None
        """
        current_text = self.search_entry.get()
        if current_text in [str(item) for item in self.items]:
            return current_text
        return None

    def clear_selection(self) -> None:
        """清除选中状态."""
        self.search_entry.delete(0, 'end')
        self._hide_dropdown()

    def clear_search(self) -> None:
        """清除搜索输入."""
        self.search_entry.delete(0, 'end')
        self.filtered_items = self.items.copy()
        self.current_selection = -1 if not self.filtered_items else 0
        self._hide_dropdown()

    def set_selected_item(self, item) -> None:
        """设置选中的项.

        Args:
            item: 要选中的项
        """
        if item in self.items:
            self.search_entry.delete(0, 'end')
            self.search_entry.insert(0, str(item))
            self._hide_dropdown()
