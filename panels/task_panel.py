"""Task Panel - 任务管理面板."""

from tkinter import END

import customtkinter as ctk

from task.task_db import TaskDatabase

# 全局字体配置
CTK_FONT_MAIN = ('Microsoft YaHei UI', 12)
CTK_FONT_BOLD = ('Microsoft YaHei UI', 12, 'bold')
CTK_FONT_SMALL = ('Microsoft YaHei UI', 10)

# 全局背景色常量
BG_COLOR_MAIN = '#242424'
BG_COLOR_CONTENT = '#1e1e1e'


class TaskPanel(ctk.CTkFrame):
    """任务管理面板."""

    def __init__(self, parent: ctk.CTk) -> None:
        """初始化 Task Panel."""
        super().__init__(parent)
        self.corner_radius = 0
        self.fg_color = 'transparent'

        # 初始化数据库
        self.db = TaskDatabase()

        # 任务列表数据
        self.tasks = []

        # 配置主布局
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.init_ui()
        self.load_tasks_from_db()

    def init_ui(self) -> None:
        """初始化 UI 组件."""
        # 顶部区域：输入框 + 添加按钮
        self.init_top_panel()
        # 中间区域：任务列表
        self.init_task_list()
        # 底部区域：统计信息
        self.init_bottom_panel()

    def init_top_panel(self) -> None:
        """初始化顶部输入区域."""
        top_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_MAIN, corner_radius=8)
        top_frame.grid(row=0, column=0, padx=10, pady=10, sticky='ew')
        top_frame.grid_columnconfigure(0, weight=1)

        # 标题
        title_label = ctk.CTkLabel(
            top_frame,
            text='📋 Task Manager',
            font=CTK_FONT_BOLD,
            text_color='#64b5f6',
        )
        title_label.grid(row=0, column=0, padx=15, pady=(10, 5), sticky='w')

        # 输入框区域
        input_frame = ctk.CTkFrame(top_frame, fg_color='transparent')
        input_frame.grid(row=1, column=0, padx=15, pady=(0, 10), sticky='ew')
        input_frame.grid_columnconfigure(0, weight=1)

        # 任务输入框
        self.task_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text='输入新任务...',
            font=CTK_FONT_MAIN,
            fg_color=BG_COLOR_CONTENT,
            border_width=1,
        )
        self.task_entry.grid(row=0, column=0, sticky='ew', padx=(0, 10))
        self.task_entry.bind('<Return>', lambda e: self.add_task())

        # 添加按钮
        add_btn = ctk.CTkButton(
            input_frame,
            text='添加',
            command=self.add_task,
            font=CTK_FONT_MAIN,
            fg_color='#4caf50',
            hover_color='#388e3c',
            corner_radius=6,
            width=80,
        )
        add_btn.grid(row=0, column=1)

    def init_task_list(self) -> None:
        """初始化任务列表区域."""
        list_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_MAIN, corner_radius=8)
        list_frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky='nsew')
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)

        # 可滚动的任务列表容器
        self.scrollable_frame = ctk.CTkScrollableFrame(
            list_frame,
            fg_color='transparent',
            label_text='待办任务',
            label_font=CTK_FONT_BOLD,
        )
        self.scrollable_frame.grid(row=0, column=0, padx=15, pady=15, sticky='nsew')
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

    def init_bottom_panel(self) -> None:
        """初始化底部统计区域."""
        bottom_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=8)
        bottom_frame.grid(row=2, column=0, padx=10, pady=(0, 10), sticky='ew')

        # 统计标签
        self.stats_label = ctk.CTkLabel(
            bottom_frame,
            text='总计: 0 | 已完成: 0 | 未完成: 0',
            font=CTK_FONT_SMALL,
            text_color='#aaaaaa',
        )
        self.stats_label.pack(padx=20, pady=8)

    def load_tasks_from_db(self) -> None:
        """从数据库加载任务."""
        db_tasks = self.db.get_all_tasks()
        for db_task in db_tasks:
            task_data = {
                'id': db_task['id'],
                'text': db_task['text'],
                'completed': bool(db_task['completed'])
            }
            self.tasks.append(task_data)
            self.create_task_row(task_data)
        self.update_stats()

    def add_task(self) -> None:
        """添加新任务."""
        task_text = self.task_entry.get().strip()
        if not task_text:
            return

        # 保存到数据库
        task_id = self.db.add_task(task_text)

        # 创建任务项
        task_data = {'id': task_id, 'text': task_text, 'completed': False}
        self.tasks.append(task_data)

        # 创建任务行
        self.create_task_row(task_data)

        # 清空输入框
        self.task_entry.delete(0, END)

        # 更新统计
        self.update_stats()

    def create_task_row(self, task: dict) -> None:
        """创建任务行 UI.

        Args:
            task: 任务数据字典
        """
        row_frame = ctk.CTkFrame(
            self.scrollable_frame,
            fg_color=BG_COLOR_CONTENT,
            corner_radius=6,
        )
        row_frame.grid(row=len(self.tasks) - 1, column=0, pady=5, sticky='ew')
        row_frame.grid_columnconfigure(1, weight=1)

        # 复选框
        checkbox = ctk.CTkCheckBox(
            row_frame,
            text='',
            command=lambda: self.toggle_task(task['id'], checkbox, task_label),
        )
        if task['completed']:
            checkbox.select()
        checkbox.grid(row=0, column=0, padx=10, pady=10)

        # 任务文本标签
        task_label = ctk.CTkLabel(
            row_frame,
            text=task['text'],
            font=CTK_FONT_MAIN,
            text_color='#888888' if task['completed'] else '#f0f0f0',
            anchor='w',
        )
        task_label.grid(row=0, column=1, padx=5, pady=10, sticky='ew')

        # 删除按钮
        delete_btn = ctk.CTkButton(
            row_frame,
            text='删除',
            width=60,
            height=28,
            font=CTK_FONT_SMALL,
            fg_color='#f44336',
            hover_color='#d32f2f',
            command=lambda: self.delete_task(task['id'], row_frame),
        )
        delete_btn.grid(row=0, column=2, padx=10, pady=10)

        # 保存 UI 引用
        task['row_frame'] = row_frame
        task['checkbox'] = checkbox
        task['label'] = task_label

    def toggle_task(self, task_id: int, checkbox: ctk.CTkCheckBox, label: ctk.CTkLabel) -> None:
        """切换任务完成状态.

        Args:
            task_id: 任务 ID
            checkbox: 复选框组件
            label: 任务标签组件
        """
        task = next(t for t in self.tasks if t['id'] == task_id)
        task['completed'] = checkbox.get() == 1

        # 更新到数据库
        self.db.update_task(task_id, completed=task['completed'])

        # 更新文本样式
        if task['completed']:
            label.configure(text_color='#888888')
        else:
            label.configure(text_color='#f0f0f0')

        # 更新统计
        self.update_stats()

    def delete_task(self, task_id: int, row_frame: ctk.CTkFrame) -> None:
        """删除任务.

        Args:
            task_id: 任务 ID
            row_frame: 任务行框架
        """
        # 从数据库删除
        self.db.delete_task(task_id)

        # 从列表中移除
        self.tasks = [t for t in self.tasks if t['id'] != task_id]

        # 销毁 UI
        row_frame.destroy()

        # 重新排列任务行
        for i, task in enumerate(self.tasks):
            if 'row_frame' in task:
                task['row_frame'].grid(row=i, column=0, pady=5, sticky='ew')

        # 更新统计
        self.update_stats()

    def update_stats(self) -> None:
        """更新任务统计信息."""
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t['completed'])
        pending = total - completed
        self.stats_label.configure(
            text=f'总计: {total} | 已完成: {completed} | 未完成: {pending}'
        )

    def destroy(self) -> None:
        """销毁面板时关闭数据库连接."""
        self.db.close()
        super().destroy()
