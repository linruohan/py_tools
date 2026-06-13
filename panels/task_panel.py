"""Task Panel - 任务管理面板."""

from __future__ import annotations

import uuid

from typing import Any

import customtkinter as ctk

from components.date_picker import DatePicker
from components.search_filter import SearchFilter
from task.task_db import TaskDatabase

# 全局字体配置
CTK_FONT_MAIN = ('Microsoft YaHei UI', 12)
CTK_FONT_BOLD = ('Microsoft YaHei UI', 12, 'bold')
CTK_FONT_SMALL = ('Microsoft YaHei UI', 10)

# 全局背景色常量
BG_COLOR_MAIN = '#242424'
BG_COLOR_CONTENT = '#1e1e1e'

# 默认标签颜色列表
DEFAULT_LABEL_COLORS = [
    '#ef5350',
    '#ec407a',
    '#ab47bc',
    '#7e57c2',
    '#5c6bc0',
    '#42a5f5',
    '#29b6f6',
    '#26c6da',
    '#26a69a',
    '#66bb6a',
    '#9ccc65',
    '#d4e157',
    '#ffca28',
    '#ffa726',
    '#ff7043',
]


class AddTaskDialog(ctk.CTkToplevel):
    """添加/编辑任务对话框."""

    def __init__(self, parent, callback, existing_labels=None, task_data=None) -> None:
        """初始化添加/编辑任务对话框.

        Args:
            parent: 父窗口
            callback: 保存成功后的回调函数
            existing_labels: 已有的标签列表
            task_data: 任务数据(编辑模式时传入)
        """
        super().__init__(parent)
        self.parent = parent
        self.callback = callback
        self.existing_labels = existing_labels or []
        self.task_data = task_data  # 编辑模式时的任务数据
        self.selected_labels: list[str] = []
        self.title('编辑任务' if task_data else '添加新任务')
        self.geometry('450x500')
        self.resizable(False, False)
        self.attributes('-topmost', True)

        # 设置窗口位置在父窗口中心
        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        dialog_width = 450
        dialog_height = 500
        x = parent_x + (parent_width - dialog_width) // 2
        y = parent_y + (parent_height - dialog_height) // 2
        self.geometry(f'{dialog_width}x{dialog_height}+{x}+{y}')

        # 设置背景色
        self.fg_color = BG_COLOR_MAIN

        # 配置布局
        self.grid_rowconfigure(7, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.init_widgets()

    def init_widgets(self) -> None:
        """初始化对话框组件."""
        # 任务内容
        content_label = ctk.CTkLabel(
            self, text='任务内容 *', font=CTK_FONT_MAIN, text_color='#f0f0f0'
        )
        content_label.grid(row=0, column=0, padx=20, pady=(20, 5), sticky='w')
        self.content_entry = ctk.CTkEntry(
            self,
            placeholder_text='请输入任务内容',
            font=CTK_FONT_MAIN,
            fg_color=BG_COLOR_CONTENT,
            border_width=1,
        )
        self.content_entry.grid(row=1, column=0, padx=20, pady=(0, 10), sticky='ew')

        # 任务描述
        desc_label = ctk.CTkLabel(self, text='任务描述', font=CTK_FONT_MAIN, text_color='#f0f0f0')
        desc_label.grid(row=2, column=0, padx=20, pady=(0, 5), sticky='w')
        self.desc_entry = ctk.CTkTextbox(
            self,
            font=CTK_FONT_MAIN,
            fg_color=BG_COLOR_CONTENT,
            border_width=1,
            height=80,
        )
        self.desc_entry.grid(row=3, column=0, padx=20, pady=(0, 10), sticky='ew')

        # 截止日期和优先级
        info_frame = ctk.CTkFrame(self, fg_color='transparent')
        info_frame.grid(row=4, column=0, padx=20, pady=(0, 10), sticky='ew')
        info_frame.grid_columnconfigure(0, weight=1)
        info_frame.grid_columnconfigure(1, weight=1)

        # 截止日期
        due_label = ctk.CTkLabel(
            info_frame, text='截止日期', font=CTK_FONT_MAIN, text_color='#f0f0f0'
        )
        due_label.grid(row=0, column=0, padx=(0, 10), pady=(0, 5), sticky='w')
        self.due_picker = DatePicker(info_frame)
        self.due_picker.grid(row=1, column=0, padx=(0, 10), sticky='ew')

        # 优先级
        priority_label = ctk.CTkLabel(
            info_frame, text='优先级', font=CTK_FONT_MAIN, text_color='#f0f0f0'
        )
        priority_label.grid(row=0, column=1, pady=(0, 5), sticky='w')
        self.priority_combobox = ctk.CTkOptionMenu(
            info_frame,
            values=['普通', '低', '中', '高'],
            font=CTK_FONT_MAIN,
            fg_color=BG_COLOR_CONTENT,
            button_color='#64b5f6',
            button_hover_color='#42a5f5',
            dropdown_hover_color='#373737',
        )
        self.priority_combobox.grid(row=1, column=1, sticky='ew')
        self.priority_combobox.set('普通')

        # 标签
        labels_label = ctk.CTkLabel(self, text='标签', font=CTK_FONT_MAIN, text_color='#f0f0f0')
        labels_label.grid(row=5, column=0, padx=20, pady=(0, 5), sticky='w')
        self.label_filter = SearchFilter(
            self,
            items=self.existing_labels,
            placeholder_text='选择或输入标签...',
        )
        self.label_filter.grid(row=6, column=0, padx=20, pady=(0, 5), sticky='ew')

        # 已选标签显示区域
        self.selected_labels_frame = ctk.CTkFrame(
            self,
            fg_color=BG_COLOR_CONTENT,
            corner_radius=4,
            border_width=1,
        )
        self.selected_labels_frame.grid(row=7, column=0, padx=20, pady=(0, 15), sticky='ew')
        self.selected_labels_frame.grid_columnconfigure(0, weight=1)

        # 按钮区域
        button_frame = ctk.CTkFrame(self, fg_color='transparent')
        button_frame.grid(row=8, column=0, padx=20, pady=(0, 20), sticky='ew')
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        # 取消按钮
        cancel_btn = ctk.CTkButton(
            button_frame,
            text='取消',
            command=self.destroy,
            font=CTK_FONT_MAIN,
            fg_color='#666666',
            hover_color='#555555',
            corner_radius=6,
        )
        cancel_btn.grid(row=0, column=0, padx=(0, 10), sticky='ew')

        # 保存按钮
        save_btn = ctk.CTkButton(
            button_frame,
            text='保存',
            command=self.on_save,
            font=CTK_FONT_MAIN,
            fg_color='#4caf50',
            hover_color='#388e3c',
            corner_radius=6,
        )
        save_btn.grid(row=0, column=1, padx=(10, 0), sticky='ew')

        # 绑定标签选择回调
        self.label_filter.on_select_callback = self.on_label_selected

        # 如果是编辑模式,填充已有数据
        if self.task_data:
            self._populate_task_data()

    def _populate_task_data(self) -> None:
        """填充编辑模式的任务数据."""
        # 填充任务内容
        self.content_entry.insert(0, self.task_data['content'])

        # 填充任务描述
        self.desc_entry.insert('1.0', self.task_data.get('description', ''))

        # 填充截止日期
        if self.task_data.get('due'):
            self.due_picker.set_date(self.task_data['due'])

        # 填充优先级
        priority_map_inv = {0: '普通', 1: '低', 2: '中', 3: '高'}
        priority = priority_map_inv.get(self.task_data.get('priority', 0), '普通')
        self.priority_combobox.set(priority)

        # 填充已选标签
        if self.task_data.get('labels'):
            self.selected_labels = self.task_data['labels'].split(',')
            self.update_selected_labels_display()

    def on_label_selected(self, label) -> None:
        """标签被选择时的回调.

        Args:
            label: 被选择的标签
        """
        if label and label not in self.selected_labels:
            self.selected_labels.append(label)
            self.update_selected_labels_display()
            self.label_filter.clear_search()

    def update_selected_labels_display(self) -> None:
        """更新已选标签的显示(同一行显示)."""
        # 清空已有显示
        for widget in self.selected_labels_frame.winfo_children():
            widget.destroy()

        # 标签容器框架(使用pack横向排列)
        tags_container = ctk.CTkFrame(self.selected_labels_frame, fg_color='transparent')
        tags_container.pack(fill='x', padx=2, pady=2)

        # 显示每个标签(同一行横向排列)
        for _, label in enumerate(self.selected_labels):
            # 标签框架
            tag_frame = ctk.CTkFrame(
                tags_container,
                fg_color='#404040',
                corner_radius=4,
            )
            tag_frame.pack(side='left', padx=2, pady=2)

            # 标签文字
            tag_label = ctk.CTkLabel(
                tag_frame,
                text=label,
                font=CTK_FONT_SMALL,
                text_color='white',
                anchor='w',
            )
            tag_label.pack(side='left', padx=6, pady=2)

            # 删除按钮
            remove_btn = ctk.CTkButton(
                tag_frame,
                text='×',
                width=20,
                height=20,
                font=('Microsoft YaHei UI', 12),
                fg_color='#5a5a5a',
                hover_color='#ff5252',
                corner_radius=4,
                command=lambda lbl=label: self.remove_label(lbl),
            )
            remove_btn.pack(side='left', padx=2, pady=2)

    def remove_label(self, label) -> None:
        """移除已选标签.

        Args:
            label: 要移除的标签
        """
        if label in self.selected_labels:
            self.selected_labels.remove(label)
            self.update_selected_labels_display()

    def on_save(self) -> None:
        """保存任务(添加或更新)."""
        content = self.content_entry.get().strip()
        if not content:
            return

        description = self.desc_entry.get('1.0', 'end').strip()
        due = self.due_picker.get_date()

        priority_map = {'普通': 0, '低': 1, '中': 2, '高': 3}
        priority = priority_map.get(self.priority_combobox.get(), 0)

        # 组合标签
        labels = ','.join(self.selected_labels)

        # 调用回调函数保存任务(编辑模式时传递任务ID)
        if self.task_data:
            self.callback(self.task_data['id'], content, description, due, priority, labels)
        else:
            self.callback(content, description, due, priority, labels)
        self.destroy()


class AddLabelDialog(ctk.CTkToplevel):
    """添加/编辑标签对话框."""

    def __init__(self, parent, callback, existing_label=None) -> None:
        """初始化标签对话框.

        Args:
            parent: 父窗口
            callback: 保存成功后的回调函数
            existing_label: 现有标签(编辑模式)
        """
        super().__init__(parent)
        self.parent = parent
        self.callback = callback
        self.existing_label = existing_label
        self.title('编辑标签' if existing_label else '添加新标签')
        self.geometry('350x280')
        self.resizable(False, False)
        self.attributes('-topmost', True)

        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        dialog_width = 350
        dialog_height = 280
        x = parent_x + (parent_width - dialog_width) // 2
        y = parent_y + (parent_height - dialog_height) // 2
        self.geometry(f'{dialog_width}x{dialog_height}+{x}+{y}')

        self.fg_color = BG_COLOR_MAIN
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.init_widgets()

    def init_widgets(self) -> None:
        """初始化对话框组件."""
        name_label = ctk.CTkLabel(self, text='标签名称 *', font=CTK_FONT_MAIN, text_color='#f0f0f0')
        name_label.grid(row=0, column=0, padx=20, pady=(20, 5), sticky='w')
        self.name_entry = ctk.CTkEntry(
            self,
            placeholder_text='请输入标签名称',
            font=CTK_FONT_MAIN,
            fg_color=BG_COLOR_CONTENT,
            border_width=1,
        )
        self.name_entry.grid(row=1, column=0, padx=20, pady=(0, 10), sticky='ew')

        color_label = ctk.CTkLabel(self, text='标签颜色', font=CTK_FONT_MAIN, text_color='#f0f0f0')
        color_label.grid(row=2, column=0, padx=20, pady=(0, 5), sticky='w')

        self.color_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.color_frame.grid(row=3, column=0, padx=20, pady=(0, 15), sticky='ew')
        self.selected_color = DEFAULT_LABEL_COLORS[0]

        for i, color in enumerate(DEFAULT_LABEL_COLORS):
            is_selected = self.existing_label and self.existing_label.get('color') == color
            color_btn = ctk.CTkButton(
                self.color_frame,
                text='',
                width=28,
                height=28,
                fg_color=color,
                hover_color=color,
                corner_radius=4,
                command=lambda c=color: self.select_color(c),
                border_width=2 if is_selected else 0,
                border_color='#ffffff',
            )
            color_btn.grid(row=0, column=i, padx=3)

        button_frame = ctk.CTkFrame(self, fg_color='transparent')
        button_frame.grid(row=4, column=0, padx=20, pady=(0, 20), sticky='ew')
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        cancel_btn = ctk.CTkButton(
            button_frame,
            text='取消',
            command=self.destroy,
            font=CTK_FONT_MAIN,
            fg_color='#666666',
            hover_color='#555555',
            corner_radius=6,
        )
        cancel_btn.grid(row=0, column=0, padx=(0, 10), sticky='ew')

        save_btn = ctk.CTkButton(
            button_frame,
            text='保存',
            command=self.on_save,
            font=CTK_FONT_MAIN,
            fg_color='#4caf50',
            hover_color='#388e3c',
            corner_radius=6,
        )
        save_btn.grid(row=0, column=1, padx=(10, 0), sticky='ew')

        if self.existing_label:
            self.name_entry.insert(0, self.existing_label['name'])
            self.selected_color = self.existing_label.get('color', DEFAULT_LABEL_COLORS[0])
            self.update_color_selection()

    def select_color(self, color) -> None:
        """选择颜色.

        Args:
            color: 选中的颜色值
        """
        self.selected_color = color
        self.update_color_selection()

    def update_color_selection(self) -> None:
        """更新颜色选择的视觉反馈."""
        for widget in self.color_frame.winfo_children():
            if widget.cget('fg_color') == self.selected_color:
                widget.configure(border_width=2, border_color='#ffffff')
            else:
                widget.configure(border_width=0)

    def on_save(self) -> None:
        """保存标签."""
        name = self.name_entry.get().strip()
        if not name:
            return

        if self.existing_label:
            label_id = self.existing_label['id']
        else:
            label_id = str(uuid.uuid4())

        self.callback(label_id, name, self.selected_color)
        self.destroy()


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
        self.tasks: list[dict[str, Any]] = []

        # 标签列表数据
        self.labels: list[dict[str, Any]] = []

        # 搜索和筛选状态
        self.search_keyword = ''
        self.filter_status = 'all'  # 'all', 'completed', 'pending'

        # 配置主布局
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.init_ui()
        self.load_labels_from_db()
        self.load_tasks_from_db()

    def init_ui(self) -> None:
        """初始化 UI 组件."""
        # 顶部区域:搜索筛选 + 添加按钮
        self.init_top_panel()
        # 中间区域:TabView(任务列表 + 标签管理)
        self.init_tabview()
        # 底部区域:统计信息
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

        # 搜索和筛选区域
        filter_frame = ctk.CTkFrame(top_frame, fg_color='transparent')
        filter_frame.grid(row=1, column=0, padx=15, pady=(0, 10), sticky='ew')
        filter_frame.grid_columnconfigure(0, weight=1)
        filter_frame.grid_columnconfigure(1, weight=0)

        # 搜索框
        self.search_entry = ctk.CTkEntry(
            filter_frame,
            placeholder_text='🔍 搜索任务...',
            font=CTK_FONT_MAIN,
            fg_color=BG_COLOR_CONTENT,
            border_width=1,
        )
        self.search_entry.grid(row=0, column=0, sticky='ew', padx=(0, 10))
        self.search_entry.bind('<KeyRelease>', lambda e: self.apply_filter())

        # 状态筛选下拉框
        self.filter_combobox = ctk.CTkOptionMenu(
            filter_frame,
            values=['全部', '已完成', '未完成'],
            font=CTK_FONT_MAIN,
            fg_color=BG_COLOR_CONTENT,
            button_color='#64b5f6',
            button_hover_color='#42a5f5',
            dropdown_hover_color='#373737',
            width=120,
            command=self.on_filter_changed,
        )
        self.filter_combobox.grid(row=0, column=1)
        self.filter_combobox.set('全部')

        # 添加任务按钮
        add_btn = ctk.CTkButton(
            top_frame,
            text='➕ 添加任务',
            command=self.open_add_task_dialog,
            font=CTK_FONT_MAIN,
            fg_color='#4caf50',
            hover_color='#388e3c',
            corner_radius=6,
            width=120,
        )
        add_btn.grid(row=2, column=0, padx=15, pady=(0, 10), sticky='w')

    def get_all_labels(self) -> list:
        """获取所有已有的标签.

        Returns:
            标签名称列表
        """
        if self.labels:
            return [label['name'] for label in self.labels]
        return []

    def open_add_task_dialog(self) -> None:
        """打开添加任务对话框."""
        existing_labels = self.get_all_labels()
        AddTaskDialog(self.master, self.add_task, existing_labels)

    def open_edit_task_dialog(self, task: dict) -> None:
        """打开编辑任务对话框.

        Args:
            task: 要编辑的任务数据
        """
        existing_labels = self.get_all_labels()
        AddTaskDialog(self.master, self.update_task, existing_labels, task)

    def init_tabview(self) -> None:
        """初始化 TabView,包含任务列表和标签管理."""
        tab_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_MAIN, corner_radius=8)
        tab_frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky='nsew')
        tab_frame.grid_rowconfigure(0, weight=1)
        tab_frame.grid_columnconfigure(0, weight=1)

        self.tabview = ctk.CTkTabview(tab_frame, fg_color=BG_COLOR_CONTENT)
        self.tabview.grid(row=0, column=0, padx=15, pady=15, sticky='nsew')

        self.task_tab = self.tabview.add('任务列表')
        self.task_tab.grid_rowconfigure(0, weight=1)
        self.task_tab.grid_columnconfigure(0, weight=1)

        self.label_tab = self.tabview.add('标签管理')
        self.label_tab.grid_rowconfigure(0, weight=1)
        self.label_tab.grid_columnconfigure(0, weight=1)

        self.init_task_list()
        self.init_label_list()

    def init_task_list(self) -> None:
        """初始化任务列表区域."""
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self.task_tab,
            fg_color='transparent',
            label_text='待办任务',
            label_font=CTK_FONT_BOLD,
        )
        self.scrollable_frame.grid(row=0, column=0, padx=15, pady=15, sticky='nsew')
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

    def init_label_list(self) -> None:
        """初始化标签管理区域."""
        label_list_frame = ctk.CTkFrame(self.label_tab, fg_color='transparent')
        label_list_frame.grid(row=0, column=0, padx=15, pady=15, sticky='nsew')
        label_list_frame.grid_rowconfigure(1, weight=1)
        label_list_frame.grid_columnconfigure(0, weight=1)

        add_label_btn = ctk.CTkButton(
            label_list_frame,
            text='➕ 添加标签',
            command=self.open_add_label_dialog,
            font=CTK_FONT_MAIN,
            fg_color='#4caf50',
            hover_color='#388e3c',
            corner_radius=6,
            width=120,
        )
        add_label_btn.grid(row=0, column=0, pady=(0, 10), sticky='w')

        self.label_scrollable_frame = ctk.CTkScrollableFrame(
            label_list_frame,
            fg_color='transparent',
            label_text='标签列表',
            label_font=CTK_FONT_BOLD,
        )
        self.label_scrollable_frame.grid(row=1, column=0, sticky='nsew')
        self.label_scrollable_frame.grid_columnconfigure(0, weight=1)

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
                'content': db_task['content'],
                'description': db_task.get('description', ''),
                'due': db_task.get('due', ''),
                'priority': db_task.get('priority', 0),
                'labels': db_task.get('labels', ''),
                'completed': bool(db_task['completed']),
            }
            self.tasks.append(task_data)
            self.create_task_row(task_data)
        self.update_stats()

    def add_task(
        self,
        content: str,
        description: str = '',
        due: str = '',
        priority: int = 0,
        labels: str = '',
    ) -> None:
        """添加新任务.

        Args:
            content: 任务内容
            description: 任务描述
            due: 截止日期
            priority: 优先级 (0-3)
            labels: 标签
        """
        # 保存到数据库
        task_id = self.db.add_task(content, description, due, priority, labels)

        # 创建任务项
        task_data = {
            'id': task_id,
            'content': content,
            'description': description,
            'due': due,
            'priority': priority,
            'labels': labels,
            'completed': False,
        }
        self.tasks.append(task_data)

        # 创建任务行
        self.create_task_row(task_data)

        # 重新排列任务行(考虑筛选条件)
        self.redisplay_tasks()

        # 更新统计
        self.update_stats()

    def update_task(
        self,
        task_id: int,
        content: str,
        description: str = '',
        due: str = '',
        priority: int = 0,
        labels: str = '',
    ) -> None:
        """更新任务.

        Args:
            task_id: 任务ID
            content: 任务内容
            description: 任务描述
            due: 截止日期
            priority: 优先级 (0-3)
            labels: 标签
        """
        # 更新数据库
        self.db.update_task(
            task_id,
            content=content,
            description=description,
            due=due,
            priority=priority,
            labels=labels,
        )

        # 找到并更新任务数据
        task = next(t for t in self.tasks if t['id'] == task_id)
        task['content'] = content
        task['description'] = description
        task['due'] = due
        task['priority'] = priority
        task['labels'] = labels

        # 更新任务行显示
        self.update_task_row(task)

        # 重新排列任务行(考虑筛选条件)
        self.redisplay_tasks()

        # 更新统计
        self.update_stats()

    def update_task_row(self, task: dict) -> None:
        """更新任务行的显示.

        Args:
            task: 更新后的任务数据
        """
        # 更新任务内容
        if 'label' in task:
            task['label'].configure(text=task['content'])

        # 更新截止日期
        if 'due_label' in task:
            if task['due']:
                task['due_label'].configure(text=f'截止: {task["due"]}')
                task['due_label'].grid()
            else:
                task['due_label'].grid_remove()

        # 更新标签
        if 'labels_frame' in task:
            # 清除现有标签
            for widget in task['labels_frame'].winfo_children():
                widget.destroy()

            if task['labels']:
                label_names = task['labels'].split(',')
                for label_name in label_names:
                    label_info = next(
                        (label for label in self.labels if label['name'] == label_name.strip()),
                        None,
                    )
                    bg_color = label_info['color'] if label_info else '#666666'

                    tag_label = ctk.CTkLabel(
                        task['labels_frame'],
                        text=label_name.strip(),
                        font=CTK_FONT_SMALL,
                        text_color='white',
                        fg_color=bg_color,
                        corner_radius=4,
                        padx=6,
                        pady=2,
                    )
                    tag_label.pack(side='left', padx=2)
                task['labels_frame'].grid()
            else:
                task['labels_frame'].grid_remove()

    def create_task_row(self, task: dict) -> None:
        """创建任务行 UI(美化版).

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
        checkbox: ctk.CTkCheckBox = ctk.CTkCheckBox(
            row_frame,
            text='',
            command=lambda: self.toggle_task(task['id'], checkbox, task_label),
        )
        if task['completed']:
            checkbox.select()
        checkbox.grid(row=0, column=0, padx=10, pady=8)

        # 任务内容
        task_label: ctk.CTkLabel = ctk.CTkLabel(
            row_frame,
            text=task['content'],
            font=CTK_FONT_MAIN,
            text_color='#888888' if task['completed'] else '#f0f0f0',
            anchor='w',
        )
        task_label.grid(row=0, column=1, padx=(5, 10), pady=8, sticky='ew')

        # 截止日期
        due_label = ctk.CTkLabel(
            row_frame,
            text=f'截止: {task["due"]}' if task['due'] else '',
            font=CTK_FONT_SMALL,
            text_color='#ffa726',
            anchor='w',
        )
        due_label.grid(row=0, column=2, padx=(0, 10), pady=8, sticky='w')
        due_label.grid_remove() if not task['due'] else None

        # 标签(带背景颜色)
        labels_frame = ctk.CTkFrame(row_frame, fg_color='transparent')
        labels_frame.grid(row=0, column=3, padx=(0, 10), pady=8, sticky='w')

        if task['labels']:
            label_names = task['labels'].split(',')
            for _, label_name in enumerate(label_names):
                # 查找标签颜色
                label_info = next(
                    (label for label in self.labels if label['name'] == label_name.strip()),
                    None,
                )
                bg_color = label_info['color'] if label_info else '#666666'

                tag_label = ctk.CTkLabel(
                    labels_frame,
                    text=label_name.strip(),
                    font=CTK_FONT_SMALL,
                    text_color='white',
                    fg_color=bg_color,
                    corner_radius=4,
                    padx=6,
                    pady=2,
                )
                tag_label.pack(side='left', padx=2)
        else:
            labels_frame.grid_remove()

        # 编辑按钮
        edit_btn = ctk.CTkButton(
            row_frame,
            text='编辑',
            width=55,
            height=26,
            font=CTK_FONT_SMALL,
            fg_color='#64b5f6',
            hover_color='#42a5f5',
            corner_radius=4,
            command=lambda: self.open_edit_task_dialog(task),
        )
        edit_btn.grid(row=0, column=4, padx=(0, 5), pady=8)

        # 删除按钮
        delete_btn = ctk.CTkButton(
            row_frame,
            text='删除',
            width=55,
            height=26,
            font=CTK_FONT_SMALL,
            fg_color='#f44336',
            hover_color='#d32f2f',
            corner_radius=4,
            command=lambda: self.delete_task(task['id'], row_frame),
        )
        delete_btn.grid(row=0, column=5, padx=(0, 10), pady=8)

        # 保存 UI 引用
        task['row_frame'] = row_frame
        task['checkbox'] = checkbox
        task['label'] = task_label
        task['due_label'] = due_label
        task['labels_frame'] = labels_frame
        task['edit_btn'] = edit_btn
        task['delete_btn'] = delete_btn

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
        self.redisplay_tasks()

        # 更新统计
        self.update_stats()

    def update_stats(self) -> None:
        """更新任务统计信息."""
        # 根据当前筛选条件计算统计
        filtered_tasks = self.get_filtered_tasks()
        total = len(filtered_tasks)
        completed = sum(1 for t in filtered_tasks if t['completed'])
        pending = total - completed
        self.stats_label.configure(text=f'显示: {total} | 已完成: {completed} | 未完成: {pending}')

    def get_filtered_tasks(self) -> list:
        """获取筛选后的任务列表.

        Returns:
            符合搜索关键词和状态筛选条件的任务列表
        """
        filtered = []
        for task in self.tasks:
            # 状态筛选
            if self.filter_status == 'completed' and not task['completed']:
                continue
            if self.filter_status == 'pending' and task['completed']:
                continue
            # 关键词搜索
            if self.search_keyword:
                keyword = self.search_keyword.lower()
                if keyword not in task['content'].lower():
                    # 也搜索描述和标签
                    if task.get('description') and keyword in task['description'].lower():
                        pass
                    elif task.get('labels') and keyword in task['labels'].lower():
                        pass
                    else:
                        continue
            filtered.append(task)
        return filtered

    def on_filter_changed(self, value: str) -> None:
        """处理筛选下拉框变化.

        Args:
            value: 选中的筛选值
        """
        status_map = {'全部': 'all', '已完成': 'completed', '未完成': 'pending'}
        self.filter_status = status_map.get(value, 'all')
        self.apply_filter()

    def apply_filter(self) -> None:
        """应用搜索和筛选条件到任务列表."""
        self.search_keyword = self.search_entry.get().strip()
        self.redisplay_tasks()
        self.update_stats()

    def redisplay_tasks(self) -> None:
        """根据筛选条件重新显示任务行."""
        filtered_tasks = self.get_filtered_tasks()
        filtered_ids = {t['id'] for t in filtered_tasks}

        for task in self.tasks:
            if 'row_frame' not in task:
                continue
            if task['id'] in filtered_ids:
                task['row_frame'].grid()
            else:
                task['row_frame'].grid_remove()

        # 重新排列可见的任务行
        visible_index = 0
        for task in self.tasks:
            if 'row_frame' in task and task['id'] in filtered_ids:
                task['row_frame'].grid(row=visible_index, column=0, pady=5, sticky='ew')
                visible_index += 1

    def load_labels_from_db(self) -> None:
        """从数据库加载标签."""
        self.labels = self.db.get_all_labels()
        for i, label in enumerate(self.labels):
            self.create_label_row(label, i)

    def create_label_row(self, label: dict, row_index: int | None = None) -> None:
        """创建标签行 UI.

        Args:
            label: 标签数据字典
            row_index: 行索引,用于设置grid位置
        """
        row_frame = ctk.CTkFrame(
            self.label_scrollable_frame,
            fg_color=BG_COLOR_CONTENT,
            corner_radius=6,
        )
        if row_index is not None:
            row_frame.grid(row=row_index, column=0, pady=5, sticky='ew')
        else:
            row_frame.grid(row=len(self.labels) - 1, column=0, pady=5, sticky='ew')
        row_frame.grid_columnconfigure(1, weight=1)

        color_box = ctk.CTkFrame(
            row_frame,
            fg_color=label.get('color', '#666666'),
            width=24,
            height=24,
            corner_radius=4,
        )
        color_box.grid(row=0, column=0, padx=10, pady=8)

        label_name = ctk.CTkLabel(
            row_frame,
            text=label['name'],
            font=CTK_FONT_MAIN,
            text_color='#f0f0f0',
            anchor='w',
        )
        label_name.grid(row=0, column=1, padx=5, pady=8, sticky='ew')

        edit_btn = ctk.CTkButton(
            row_frame,
            text='编辑',
            width=50,
            height=28,
            font=CTK_FONT_SMALL,
            fg_color='#64b5f6',
            hover_color='#42a5f5',
            command=lambda lbl=label: self.open_edit_label_dialog(lbl),
        )
        edit_btn.grid(row=0, column=2, padx=5, pady=8)

        delete_btn = ctk.CTkButton(
            row_frame,
            text='删除',
            width=50,
            height=28,
            font=CTK_FONT_SMALL,
            fg_color='#f44336',
            hover_color='#d32f2f',
            command=lambda lbl=label: self.delete_label(lbl['id'], row_frame),
        )
        delete_btn.grid(row=0, column=3, padx=(5, 10), pady=8)

        label['row_frame'] = row_frame
        label['color_box'] = color_box
        label['label_name'] = label_name

    def open_add_label_dialog(self) -> None:
        """打开添加标签对话框."""
        AddLabelDialog(self.master, self.save_label)

    def open_edit_label_dialog(self, label: dict) -> None:
        """打开编辑标签对话框.

        Args:
            label: 要编辑的标签数据
        """
        AddLabelDialog(self.master, self.save_label, label)

    def save_label(self, label_id: str, name: str, color: str) -> None:
        """保存标签(添加或更新).

        Args:
            label_id: 标签ID
            name: 标签名称
            color: 标签颜色
        """
        existing_label = next((label for label in self.labels if label['id'] == label_id), None)

        if existing_label:
            self.db.update_label(label_id, name=name, color=color)
            existing_label['name'] = name
            existing_label['color'] = color
            self.update_label_row(existing_label)
        else:
            self.db.add_label(label_id, name, color, item_order=len(self.labels))
            new_label = {
                'id': label_id,
                'name': name,
                'color': color,
                'item_order': len(self.labels),
                'is_deleted': 0,
                'is_favorite': 0,
                'backend_type': '',
                'source_id': '',
            }
            self.labels.append(new_label)
            self.create_label_row(new_label)

    def update_label_row(self, label: dict) -> None:
        """更新标签行的显示.

        Args:
            label: 更新后的标签数据
        """
        if 'color_box' in label:
            label['color_box'].configure(fg_color=label['color'])
        if 'label_name' in label:
            label['label_name'].configure(text=label['name'])

    def delete_label(self, label_id: str, row_frame: ctk.CTkFrame) -> None:
        """删除标签.

        Args:
            label_id: 标签ID
            row_frame: 标签行框架
        """
        self.db.delete_label(label_id)
        self.labels = [label for label in self.labels if label['id'] != label_id]
        row_frame.destroy()

        visible_index = 0
        for label in self.labels:
            if 'row_frame' in label:
                label['row_frame'].grid(row=visible_index, column=0, pady=5, sticky='ew')
                visible_index += 1

    def destroy(self) -> None:
        """销毁面板时关闭数据库连接."""
        self.db.close()
        super().destroy()
