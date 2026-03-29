"""表单构建器 - 减少重复代码"""

from collections.abc import Callable
from typing import Any

import customtkinter as ctk


class FormBuilder:
    """表单构建器 - 提供常用表单组件的快速创建方法"""

    @staticmethod
    def create_label_entry(
        parent: ctk.CTkFrame,
        label_text: str,
        default_value: str = '',
        row: int = 0,
        column: int = 0,
        width: int = 200,
        on_change: Callable[[str], None] | None = None,
        **kwargs: Any,
    ) -> ctk.CTkEntry:
        """创建标签+输入框组合

        Args:
            parent: 父容器
            label_text: 标签文本
            default_value: 默认值
            row: 行号
            column: 列号
            width: 输入框宽度
            on_change: 值变化回调函数
            **kwargs: 传递给 CTkEntry 的其他参数

        Returns:
            创建的输入框组件
        """
        label = ctk.CTkLabel(parent, text=label_text)
        label.grid(row=row, column=column, padx=5, pady=5, sticky='w')

        entry = ctk.CTkEntry(parent, width=width, **kwargs)
        entry.insert(0, default_value)
        entry.grid(row=row, column=column + 1, padx=5, pady=5, sticky='ew')

        if on_change:
            entry.bind('<KeyRelease>', lambda e: on_change(entry.get()))

        return entry

    @staticmethod
    def create_label_combobox(
        parent: ctk.CTkFrame,
        label_text: str,
        values: list[str],
        default_value: str = '',
        row: int = 0,
        column: int = 0,
        width: int = 200,
        on_change: Callable[[str], None] | None = None,
        **kwargs: Any,
    ) -> ctk.CTkComboBox:
        """创建标签+下拉框组合

        Args:
            parent: 父容器
            label_text: 标签文本
            values: 下拉选项列表
            default_value: 默认值
            row: 行号
            column: 列号
            width: 下拉框宽度
            on_change: 值变化回调函数
            **kwargs: 传递给 CTkComboBox 的其他参数

        Returns:
            创建的下拉框组件
        """
        label = ctk.CTkLabel(parent, text=label_text)
        label.grid(row=row, column=column, padx=5, pady=5, sticky='w')

        combobox = ctk.CTkComboBox(parent, values=values, width=width, **kwargs)
        if default_value:
            combobox.set(default_value)
        combobox.grid(row=row, column=column + 1, padx=5, pady=5, sticky='ew')

        if on_change:
            combobox.configure(command=on_change)

        return combobox

    @staticmethod
    def create_label_switch(
        parent: ctk.CTkFrame,
        label_text: str,
        default_value: bool = False,
        row: int = 0,
        column: int = 0,
        on_change: Callable[[bool], None] | None = None,
        **kwargs: Any,
    ) -> ctk.CTkSwitch:
        """创建标签+开关组合

        Args:
            parent: 父容器
            label_text: 标签文本
            default_value: 默认值
            row: 行号
            column: 列号
            on_change: 值变化回调函数
            **kwargs: 传递给 CTkSwitch 的其他参数

        Returns:
            创建的开关组件
        """
        label = ctk.CTkLabel(parent, text=label_text)
        label.grid(row=row, column=column, padx=5, pady=5, sticky='w')

        switch = ctk.CTkSwitch(parent, text='', **kwargs)
        if default_value:
            switch.select()
        switch.grid(row=row, column=column + 1, padx=5, pady=5, sticky='w')

        if on_change:
            switch.configure(command=lambda: on_change(switch.get() == 1))

        return switch

    @staticmethod
    def create_label_textbox(
        parent: ctk.CTkFrame,
        label_text: str,
        default_value: str = '',
        row: int = 0,
        column: int = 0,
        width: int = 200,
        height: int = 100,
        **kwargs: Any,
    ) -> ctk.CTkTextbox:
        """创建标签+文本框组合

        Args:
            parent: 父容器
            label_text: 标签文本
            default_value: 默认值
            row: 行号
            column: 列号
            width: 文本框宽度
            height: 文本框高度
            **kwargs: 传递给 CTkTextbox 的其他参数

        Returns:
            创建的文本框组件
        """
        label = ctk.CTkLabel(parent, text=label_text)
        label.grid(row=row, column=column, padx=5, pady=5, sticky='nw')

        textbox = ctk.CTkTextbox(parent, width=width, height=height, **kwargs)
        textbox.insert('1.0', default_value)
        textbox.grid(row=row, column=column + 1, padx=5, pady=5, sticky='nsew')

        return textbox
