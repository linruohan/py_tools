"""基础 Tab 组件 - 提供所有配置 Tab 的基类.

这个模块提供了基础类来减少重复代码，让所有 Tab 类都能继承这些公共功能。
"""

from typing import Any, Callable, Optional
import customtkinter as ctk

from utils.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class BaseConfigTab(ctk.CTkFrame):
    """所有配置 Tab 的基类.

    提供了通用的初始化、变化触发和配置获取功能。
    子类只需要实现 _init_ui() 和 get_config() 方法即可。

    Attributes:
        on_change_callback: 当配置发生变化时的回调函数
    """

    def __init__(
        self, master: Any, on_change_callback: Optional[Callable] = None, **kwargs
    ) -> None:
        """初始化基础 Tab.

        Args:
            master: 父级容器
            on_change_callback: 配置变化时的回调函数
            **kwargs: 传递给 CTkFrame 的其他参数
        """
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent')
        self.on_change_callback = on_change_callback
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面 - 子类必须实现此方法.

        Raises:
            NotImplementedError: 如果子类没有实现此方法
        """
        raise NotImplementedError(f'{self.__class__.__name__} 必须实现 _init_ui() 方法')

    def _trigger_change(self, *args: Any) -> None:
        """触发配置变化回调.

        当任何配置项发生变化时调用此方法，会通知父组件配置已更改。

        Args:
            *args: 接受任何参数，方便绑定到各种事件
        """
        if self.on_change_callback:
            self.on_change_callback()

    def get_config(self) -> dict:
        """获取配置数据 - 子类必须实现此方法.

        Returns:
            包含当前配置的字典

        Raises:
            NotImplementedError: 如果子类没有实现此方法
        """
        raise NotImplementedError(f'{self.__class__.__name__} 必须实现 get_config() 方法')

    def to_xml(self) -> dict:
        """生成 XML 配置字典.

        默认实现使用类名（去除 'Tab' 后缀并小写）作为键。
        子类可以重写此方法以自定义 XML 结构。

        Returns:
            XML 配置字典
        """
        key = self.__class__.__name__.lower().replace('tab', '')
        return {key: self.get_config()}

    def _create_label_entry(
        self,
        parent: ctk.CTkFrame,
        label_text: str,
        placeholder: str = '',
        default_value: str = '',
        width: int = 100,
        row: int = 0,
        label_width: int = 100,
    ) -> ctk.CTkEntry:
        """创建 Label + Entry 组合控件.

        这是一个便捷方法，用于快速创建标签和输入框的组合。

        Args:
            parent: 父级容器
            label_text: 标签文本
            placeholder: 输入框占位文本
            default_value: 默认值
            width: 输入框宽度
            row: 网格行号
            label_width: 标签宽度

        Returns:
            创建的 CTkEntry 控件
        """
        ctk.CTkLabel(
            parent, text=label_text, font=CTK_FONT_MAIN, width=label_width, anchor='w'
        ).grid(row=row, column=0, padx=10, pady=5, sticky='w')

        entry = ctk.CTkEntry(parent, placeholder_text=placeholder, width=width)
        entry.grid(row=row, column=1, padx=5, pady=5, sticky='w')
        if default_value:
            entry.insert(0, default_value)
        entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        return entry

    def _create_label_option(
        self,
        parent: ctk.CTkFrame,
        label_text: str,
        values: list[str],
        default_value: str,
        width: int = 120,
        row: int = 0,
        label_width: int = 100,
    ) -> ctk.CTkOptionMenu:
        """创建 Label + OptionMenu 组合控件.

        这是一个便捷方法，用于快速创建标签和下拉菜单的组合。

        Args:
            parent: 父级容器
            label_text: 标签文本
            values: 选项列表
            default_value: 默认值
            width: 下拉菜单宽度
            row: 网格行号
            label_width: 标签宽度

        Returns:
            创建的 CTkOptionMenu 控件
        """
        ctk.CTkLabel(
            parent, text=label_text, font=CTK_FONT_MAIN, width=label_width, anchor='w'
        ).grid(row=row, column=0, padx=10, pady=5, sticky='w')

        option = ctk.CTkOptionMenu(parent, values=values, width=width, font=CTK_FONT_SMALL)
        option.set(default_value)
        option.grid(row=row, column=1, padx=5, pady=5, sticky='w')
        option.configure(command=self._trigger_change)

        return option

    def _create_label_checkbox(
        self,
        parent: ctk.CTkFrame,
        label_text: str,
        default_checked: bool = False,
        row: int = 0,
        label_width: int = 100,
    ) -> ctk.CTkCheckBox:
        """创建 Label + CheckBox 组合控件.

        Args:
            parent: 父级容器
            label_text: 标签文本
            default_checked: 默认是否选中
            row: 网格行号
            label_width: 标签宽度

        Returns:
            创建的 CTkCheckBox 控件
        """
        ctk.CTkLabel(
            parent, text=label_text, font=CTK_FONT_MAIN, width=label_width, anchor='w'
        ).grid(row=row, column=0, padx=10, pady=5, sticky='w')

        checkbox = ctk.CTkCheckBox(
            parent, text='', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        if default_checked:
            checkbox.select()
        checkbox.grid(row=row, column=1, padx=5, pady=5, sticky='w')

        return checkbox

    def _create_section_title(
        self,
        parent: ctk.CTkFrame,
        title: str,
        text_color: str = '#64b5f6',
        row: int = 0,
    ) -> None:
        """创建章节标题.

        Args:
            parent: 父级容器
            title: 标题文本
            text_color: 标题颜色
            row: 网格行号
        """
        ctk.CTkLabel(parent, text=title, font=CTK_FONT_BOLD, text_color=text_color).grid(
            row=row, column=0, columnspan=2, padx=10, pady=5, sticky='w'
        )

    def _create_info_label(
        self,
        parent: ctk.CTkFrame,
        info_text: str,
        row: int = 0,
        text_color: str = '#888888',
    ) -> None:
        """创建说明文本标签.

        Args:
            parent: 父级容器
            info_text: 说明文本
            row: 网格行号
            text_color: 文本颜色
        """
        ctk.CTkLabel(
            parent,
            text=info_text,
            font=CTK_FONT_SMALL,
            text_color=text_color,
            justify='left',
        ).grid(row=row, column=0, columnspan=2, padx=10, pady=5, sticky='nw')


class BaseInnerTab(BaseConfigTab):
    """用于 InnerTabPanel 的子 Tab 基类.

    继承自 BaseConfigTab，专门用于作为 InnerTabPanel 的子标签页。
    提供了相同的接口，但语义上更清晰。
    """

    pass


def create_two_column_layout(
    parent: ctk.CTkFrame,
    left_title: str = '左侧面板',
    right_title: str = '右侧面板',
    left_color: str = '#64b5f6',
    right_color: str = '#4caf50',
) -> tuple[ctk.CTkFrame, ctk.CTkFrame]:
    """创建标准的双列布局.

    这是一个工具函数，用于快速创建左右两栏的标准布局。

    Args:
        parent: 父级容器
        left_title: 左侧面板标题
        right_title: 右侧面板标题
        left_color: 左侧标题颜色
        right_color: 右侧标题颜色

    Returns:
        (左侧面板, 右侧面板) 的元组
    """
    parent.grid_columnconfigure(0, weight=1)
    parent.grid_columnconfigure(1, weight=1)

    # 左侧面板
    left_frame = ctk.CTkFrame(parent, fg_color=BG_COLOR_CONTENT, corner_radius=6)
    left_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
    left_frame.grid_columnconfigure(1, weight=1)

    ctk.CTkLabel(left_frame, text=left_title, font=CTK_FONT_BOLD, text_color=left_color).grid(
        row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
    )

    # 右侧面板
    right_frame = ctk.CTkFrame(parent, fg_color=BG_COLOR_CONTENT, corner_radius=6)
    right_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
    right_frame.grid_columnconfigure(1, weight=1)

    ctk.CTkLabel(right_frame, text=right_title, font=CTK_FONT_BOLD, text_color=right_color).grid(
        row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
    )

    return left_frame, right_frame


def create_three_column_layout(
    parent: ctk.CTkFrame,
    left_title: str = '左侧面板',
    mid_title: str = '中间面板',
    right_title: str = '右侧面板',
    left_color: str = '#64b5f6',
    mid_color: str = '#4caf50',
    right_color: str = '#ff9800',
) -> tuple[ctk.CTkFrame, ctk.CTkFrame, ctk.CTkFrame]:
    """创建标准的三列布局.

    这是一个工具函数，用于快速创建左中右三栏的标准布局。

    Args:
        parent: 父级容器
        left_title: 左侧面板标题
        mid_title: 中间面板标题
        right_title: 右侧面板标题
        left_color: 左侧标题颜色
        mid_color: 中间标题颜色
        right_color: 右侧标题颜色

    Returns:
        (左侧面板, 中间面板, 右侧面板) 的元组
    """
    parent.grid_columnconfigure(0, weight=1)
    parent.grid_columnconfigure(1, weight=1)
    parent.grid_columnconfigure(2, weight=1)

    # 左侧面板
    left_frame = ctk.CTkFrame(parent, fg_color=BG_COLOR_CONTENT, corner_radius=6)
    left_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
    left_frame.grid_columnconfigure(1, weight=1)

    ctk.CTkLabel(left_frame, text=left_title, font=CTK_FONT_BOLD, text_color=left_color).grid(
        row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
    )

    # 中间面板
    mid_frame = ctk.CTkFrame(parent, fg_color=BG_COLOR_CONTENT, corner_radius=6)
    mid_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
    mid_frame.grid_columnconfigure(1, weight=1)

    ctk.CTkLabel(mid_frame, text=mid_title, font=CTK_FONT_BOLD, text_color=mid_color).grid(
        row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
    )

    # 右侧面板
    right_frame = ctk.CTkFrame(parent, fg_color=BG_COLOR_CONTENT, corner_radius=6)
    right_frame.grid(row=0, column=2, sticky='nsew', padx=5, pady=5)
    right_frame.grid_columnconfigure(1, weight=1)

    ctk.CTkLabel(right_frame, text=right_title, font=CTK_FONT_BOLD, text_color=right_color).grid(
        row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
    )

    return left_frame, mid_frame, right_frame
