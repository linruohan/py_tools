"""基础 Tab 组件 - 提供所有配置 Tab 的基类.

这个模块提供了基础类来减少重复代码, 让所有 Tab 类都能继承这些公共功能.
"""

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, ClassVar, Literal

import customtkinter as ctk

from utils.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL

FieldType = Literal['entry', 'option', 'checkbox', 'info']


@dataclass
class FieldConfig:
    """字段配置."""

    label: str
    field_type: FieldType = 'entry'
    default: Any = ''
    values: list[str] | None = None  # 用于 option 类型
    width: int = 100
    label_width: int = 100
    placeholder: str = ''
    tooltip: str = ''


@dataclass
class SectionConfig:
    """区域配置."""

    title: str
    fields: list[FieldConfig] = field(default_factory=list)
    color: str = '#64b5f6'


class BaseConfigTab(ctk.CTkFrame):
    """所有配置 Tab 的基类.

    提供了通用的初始化、变化触发和配置获取功能.
    子类只需要实现 _init_ui() 和 get_config() 方法即可.

    Attributes:
        on_change_callback: 当配置发生变化时的回调函数
    """

    def __init__(self, master: Any, on_change_callback: Callable | None = None, **kwargs) -> None:
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

        当任何配置项发生变化时调用此方法, 会通知父组件配置已更改.

        Args:
            *args: 接受任何参数, 方便绑定到各种事件
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

        默认实现使用类名 (去除 'Tab' 后缀并小写) 作为键.
        子类可以重写此方法以自定义 XML 结构.

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
        column: int = 0,
        columnspan: int = 1,
        label_width: int = 100,
    ) -> ctk.CTkEntry:
        """创建 Label + Entry 组合控件.

        这是一个便捷方法, 用于快速创建标签和输入框的组合.

        Args:
            parent: 父级容器
            label_text: 标签文本
            placeholder: 输入框占位文本
            default_value: 默认值
            width: 输入框宽度
            row: 网格行号
            column: 网格列号
            columnspan: 列跨度
            label_width: 标签宽度

        Returns:
            创建的 CTkEntry 控件
        """
        ctk.CTkLabel(
            parent, text=label_text, font=CTK_FONT_MAIN, width=label_width, anchor='w'
        ).grid(row=row, column=column, padx=10, pady=5, sticky='w')

        entry = ctk.CTkEntry(parent, placeholder_text=placeholder, width=width)
        entry.grid(row=row, column=column + 1, padx=5, pady=5, sticky='w')
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
        column: int = 0,
        columnspan: int = 1,
        label_width: int = 100,
    ) -> ctk.CTkOptionMenu:
        """创建 Label + OptionMenu 组合控件.

        这是一个便捷方法, 用于快速创建标签和下拉菜单的组合.

        Args:
            parent: 父级容器
            label_text: 标签文本
            values: 选项列表
            default_value: 默认值
            width: 下拉菜单宽度
            row: 网格行号
            column: 网格列号
            columnspan: 列跨度
            label_width: 标签宽度

        Returns:
            创建的 CTkOptionMenu 控件
        """
        ctk.CTkLabel(
            parent, text=label_text, font=CTK_FONT_MAIN, width=label_width, anchor='w'
        ).grid(row=row, column=column, padx=10, pady=5, sticky='w')

        option = ctk.CTkOptionMenu(parent, values=values, width=width, font=CTK_FONT_SMALL)
        option.set(default_value)
        option.grid(row=row, column=column + 1, padx=5, pady=5, sticky='w')
        option.configure(command=self._trigger_change)

        return option

    def _create_label_checkbox(
        self,
        parent: ctk.CTkFrame,
        label_text: str,
        default_checked: bool = False,
        row: int = 0,
        column: int = 0,
        label_width: int = 100,
    ) -> ctk.CTkCheckBox:
        """创建 Label + CheckBox 组合控件.

        Args:
            parent: 父级容器
            label_text: 标签文本
            default_checked: 默认是否选中
            row: 网格行号
            column: 网格列号
            label_width: 标签宽度

        Returns:
            创建的 CTkCheckBox 控件
        """
        ctk.CTkLabel(
            parent, text=label_text, font=CTK_FONT_MAIN, width=label_width, anchor='w'
        ).grid(row=row, column=column, padx=10, pady=5, sticky='w')

        checkbox = ctk.CTkCheckBox(
            parent, text='', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        if default_checked:
            checkbox.select()
        checkbox.grid(row=row, column=column + 1, padx=5, pady=5, sticky='w')

        return checkbox

    def _create_section_title(
        self,
        parent: ctk.CTkFrame,
        title: str,
        text_color: str = '#64b5f6',
        row: int = 0,
        column: int = 0,
        columnspan: int = 2,
    ) -> None:
        """创建章节标题.

        Args:
            parent: 父级容器
            title: 标题文本
            text_color: 标题颜色
            row: 网格行号
            column: 网格列号
            columnspan: 列跨度
        """
        ctk.CTkLabel(parent, text=title, font=CTK_FONT_BOLD, text_color=text_color).grid(
            row=row, column=column, columnspan=columnspan, padx=10, pady=5, sticky='w'
        )

    def _create_info_label(
        self,
        parent: ctk.CTkFrame,
        info_text: str,
        row: int = 0,
        column: int = 0,
        columnspan: int = 2,
        text_color: str = '#888888',
    ) -> None:
        """创建说明文本标签.

        Args:
            parent: 父级容器
            info_text: 说明文本
            row: 网格行号
            column: 网格列号
            columnspan: 列跨度
            text_color: 文本颜色
        """
        ctk.CTkLabel(
            parent,
            text=info_text,
            font=CTK_FONT_SMALL,
            text_color=text_color,
            justify='left',
        ).grid(row=row, column=column, columnspan=columnspan, padx=10, pady=5, sticky='nw')


class BaseInnerTab(BaseConfigTab):
    """用于 InnerTabPanel 的子 Tab 基类.

    继承自 BaseConfigTab, 专门用于作为 InnerTabPanel 的子标签页.
    提供了相同的接口, 但语义上更清晰.
    """

    pass


class StandardConfigTab(BaseConfigTab):
    """标准配置 Tab 基类 - 使用声明式配置自动生成 UI.

    适用于简单的配置场景,只需定义字段配置即可自动生成界面.

    Example:
        class PowerManagementTab(StandardConfigTab):
            SECTIONS = {
                'left': SectionConfig(
                    title='电源管理',
                    fields=[
                        FieldConfig('S3 (挂起到内存):', 'option', 'yes', ['yes', 'no']),
                        FieldConfig('S4 (挂起到磁盘):', 'option', 'yes', ['yes', 'no']),
                    ],
                    color='#64b5f6'
                ),
                'right': SectionConfig(
                    title='说明',
                    fields=[
                        FieldConfig('说明文本', 'info', 'S3: 系统状态保存到内存...'),
                    ],
                    color='#4caf50'
                )
            }
    """

    SECTIONS: ClassVar[dict[str, SectionConfig]] = {}  # 子类定义
    LEFT_TITLE: str = ''  # 兼容旧的命名方式
    RIGHT_TITLE: str = ''
    LEFT_COLOR: str = '#64b5f6'
    RIGHT_COLOR: str = '#4caf50'
    FIELDS: ClassVar[list[FieldConfig]] = []  # 兼容旧的命名方式 (仅左侧)

    def _init_ui(self) -> None:
        """初始化界面."""
        # 兼容旧的使用 LEFT_TITLE/RIGHT_TITLE 的方式
        if self.LEFT_TITLE and not self.SECTIONS:
            self._init_legacy_ui()
        else:
            self._init_sections_ui()

    def _init_legacy_ui(self) -> None:
        """初始化传统双栏 UI (兼容旧代码)."""
        self.left_frame, self.right_frame = create_two_column_layout(
            self, self.LEFT_TITLE, self.RIGHT_TITLE, self.LEFT_COLOR, self.RIGHT_COLOR
        )
        self._create_fields(self.left_frame, self.FIELDS, start_row=1)
        self._current_row_right = 1

    def _init_sections_ui(self) -> None:
        """初始化基于 Sections 的 UI."""
        num_sections = len(self.SECTIONS)
        if num_sections == 0:
            return

        # 配置列权重
        for i in range(num_sections):
            self.grid_columnconfigure(i, weight=1)

        self.section_frames = {}
        self.section_rows = {}

        # 创建每个区域
        for idx, (section_key, section) in enumerate(self.SECTIONS.items()):
            frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
            frame.grid(row=0, column=idx, sticky='nsew', padx=5, pady=5)
            frame.grid_columnconfigure(1, weight=1)

            ctk.CTkLabel(
                frame, text=section.title, font=CTK_FONT_BOLD, text_color=section.color
            ).grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w')

            self._create_fields(frame, section.fields, start_row=1)
            self.section_frames[section_key] = frame
            self.section_rows[section_key] = 1

    def _create_fields(
        self, parent: ctk.CTkFrame, fields: list[FieldConfig], start_row: int = 1
    ) -> dict:
        """创建一组字段.

        Args:
            parent: 父容器
            fields: 字段配置列表
            start_row: 起始行号

        Returns:
            创建的控件字典
        """
        widgets = {}
        for i, field_config in enumerate(fields):
            row = start_row + i
            widget = self._create_field(parent, field_config, row)
            widgets[field_config.label] = widget
        return widgets

    def _create_field(
        self, parent: ctk.CTkFrame, field_config: FieldConfig, row: int
    ) -> ctk.CTkEntry | ctk.CTkOptionMenu | ctk.CTkCheckBox | ctk.CTkLabel:
        """创建单个字段.

        Args:
            parent: 父容器
            field_config: 字段配置
            row: 行号

        Returns:
            创建的控件
        """
        if field_config.field_type == 'entry':
            return self._create_entry_field(parent, field_config, row)
        elif field_config.field_type == 'option':
            return self._create_option_field(parent, field_config, row)
        elif field_config.field_type == 'checkbox':
            return self._create_checkbox_field(parent, field_config, row)
        elif field_config.field_type == 'info':
            return self._create_info_field(parent, field_config, row)
        else:
            raise ValueError(f'未知的字段类型:{field_config.field_type}')

    def _create_entry_field(
        self, parent: ctk.CTkFrame, field_config: FieldConfig, row: int
    ) -> ctk.CTkEntry:
        """创建 Entry 字段."""
        ctk.CTkLabel(
            parent,
            text=field_config.label,
            font=CTK_FONT_MAIN,
            width=field_config.label_width,
            anchor='w',
        ).grid(row=row, column=0, padx=10, pady=5, sticky='w')

        entry = ctk.CTkEntry(
            parent,
            placeholder_text=field_config.placeholder,
            width=field_config.width,
        )
        entry.grid(row=row, column=1, padx=5, pady=5, sticky='w')
        if field_config.default:
            entry.insert(0, str(field_config.default))
        entry.bind('<KeyRelease>', lambda e: self._trigger_change())
        return entry

    def _create_option_field(
        self, parent: ctk.CTkFrame, field_config: FieldConfig, row: int
    ) -> ctk.CTkOptionMenu:
        """创建 Option 字段."""
        ctk.CTkLabel(
            parent,
            text=field_config.label,
            font=CTK_FONT_MAIN,
            width=field_config.label_width,
            anchor='w',
        ).grid(row=row, column=0, padx=10, pady=5, sticky='w')

        option = ctk.CTkOptionMenu(
            parent,
            values=field_config.values or [],
            width=field_config.width,
            font=CTK_FONT_SMALL,
        )
        option.set(field_config.default)
        option.grid(row=row, column=1, padx=5, pady=5, sticky='w')
        option.configure(command=self._trigger_change)
        return option

    def _create_checkbox_field(
        self, parent: ctk.CTkFrame, field_config: FieldConfig, row: int
    ) -> ctk.CTkCheckBox:
        """创建 Checkbox 字段."""
        ctk.CTkLabel(
            parent,
            text=field_config.label,
            font=CTK_FONT_MAIN,
            width=field_config.label_width,
            anchor='w',
        ).grid(row=row, column=0, padx=10, pady=5, sticky='w')

        checkbox = ctk.CTkCheckBox(
            parent, text='', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        if field_config.default:
            checkbox.select()
        checkbox.grid(row=row, column=1, padx=5, pady=5, sticky='w')
        return checkbox

    def _create_info_field(
        self, parent: ctk.CTkFrame, field_config: FieldConfig, row: int
    ) -> ctk.CTkLabel:
        """创建 Info 字段 (多行说明文本)."""
        label = ctk.CTkLabel(
            parent,
            text=field_config.default,
            font=CTK_FONT_SMALL,
            text_color='#888888',
            justify='left',
        )
        label.grid(row=row, column=0, columnspan=2, padx=10, pady=5, sticky='nw')
        return label

    def get_config(self) -> dict:
        """获取配置数据.

        默认实现会从所有 section 中收集配置.
        子类可以重写此方法以自定义配置收集逻辑.
        """
        config = {}
        # 收集所有 section 的字段值
        for _section_key, section in self.SECTIONS.items():
            for field_config in section.fields:
                if field_config.field_type == 'info':
                    continue  # 跳过 info 类型
                widget = getattr(self, f'_{self._sanitize_name(field_config.label)}', None)
                if widget:
                    key = self._sanitize_name(field_config.label, prefix='')
                    if isinstance(widget, ctk.CTkEntry):
                        config[key] = widget.get().strip()
                    elif isinstance(widget, ctk.CTkOptionMenu):
                        config[key] = widget.get()
                    elif isinstance(widget, ctk.CTkCheckBox):
                        config[key] = bool(widget.get())
        return config

    @staticmethod
    def _sanitize_name(label: str, prefix: str = '_') -> str:
        """将标签文本转换为合法的属性名.

        Args:
            label: 标签文本
            prefix: 前缀

        Returns:
            合法的 Python 属性名
        """
        name = label.lower()
        name = name.replace('(', '').replace(')', '').replace(':', '')
        name = name.replace(' ', '_').replace('-', '_')
        name = name.replace('/', '_').replace('.', '')
        return prefix + name if prefix else name


def create_two_column_layout(
    parent: ctk.CTkFrame,
    left_title: str = '左侧面板',
    right_title: str = '右侧面板',
    left_color: str = '#64b5f6',
    right_color: str = '#4caf50',
) -> tuple[ctk.CTkFrame, ctk.CTkFrame]:
    """创建标准的双列布局.

    这是一个工具函数, 用于快速创建左右两栏的标准布局.

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

    这是一个工具函数, 用于快速创建左中右三栏的标准布局.

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


def create_four_column_layout(
    parent: ctk.CTkFrame,
    left_title: str = '左侧面板',
    mid1_title: str = '中间面板 1',
    mid2_title: str = '中间面板 2',
    right_title: str = '右侧面板',
    left_color: str = '#64b5f6',
    mid1_color: str = '#9c27b0',
    mid2_color: str = '#4caf50',
    right_color: str = '#ff9800',
) -> tuple[ctk.CTkFrame, ctk.CTkFrame, ctk.CTkFrame, ctk.CTkFrame]:
    """创建标准的四列布局.

    这是一个工具函数, 用于快速创建左中1中2右四栏的标准布局.

    Args:
        parent: 父级容器
        left_title: 左侧面板标题
        mid1_title: 中间面板 1 标题
        mid2_title: 中间面板 2 标题
        right_title: 右侧面板标题
        left_color: 左侧标题颜色
        mid1_color: 中间面板 1 标题颜色
        mid2_color: 中间面板 2 标题颜色
        right_color: 右侧标题颜色

    Returns:
        (左侧面板, 中间面板 1, 中间面板 2, 右侧面板) 的元组
    """
    parent.grid_columnconfigure(0, weight=1)
    parent.grid_columnconfigure(1, weight=1)
    parent.grid_columnconfigure(2, weight=1)
    parent.grid_columnconfigure(3, weight=1)

    # 左侧面板
    left_frame = ctk.CTkFrame(parent, fg_color=BG_COLOR_CONTENT, corner_radius=6)
    left_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
    left_frame.grid_columnconfigure(1, weight=1)

    ctk.CTkLabel(left_frame, text=left_title, font=CTK_FONT_BOLD, text_color=left_color).grid(
        row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
    )

    # 中间面板 1
    mid1_frame = ctk.CTkFrame(parent, fg_color=BG_COLOR_CONTENT, corner_radius=6)
    mid1_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
    mid1_frame.grid_columnconfigure(1, weight=1)

    ctk.CTkLabel(mid1_frame, text=mid1_title, font=CTK_FONT_BOLD, text_color=mid1_color).grid(
        row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
    )

    # 中间面板 2
    mid2_frame = ctk.CTkFrame(parent, fg_color=BG_COLOR_CONTENT, corner_radius=6)
    mid2_frame.grid(row=0, column=2, sticky='nsew', padx=5, pady=5)
    mid2_frame.grid_columnconfigure(1, weight=1)

    ctk.CTkLabel(mid2_frame, text=mid2_title, font=CTK_FONT_BOLD, text_color=mid2_color).grid(
        row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
    )

    # 右侧面板
    right_frame = ctk.CTkFrame(parent, fg_color=BG_COLOR_CONTENT, corner_radius=6)
    right_frame.grid(row=0, column=3, sticky='nsew', padx=5, pady=5)
    right_frame.grid_columnconfigure(1, weight=1)

    ctk.CTkLabel(right_frame, text=right_title, font=CTK_FONT_BOLD, text_color=right_color).grid(
        row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
    )

    return left_frame, mid1_frame, mid2_frame, right_frame
