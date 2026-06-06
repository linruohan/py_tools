"""Task Panel - 任务管理面板."""

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


class AddTaskDialog(ctk.CTkToplevel):
    """添加任务对话框."""

    def __init__(self, parent, callback, existing_labels=None) -> None:
        """初始化添加任务对话框.

        Args:
            parent: 父窗口
            callback: 保存成功后的回调函数
            existing_labels: 已有的标签列表
        """
        super().__init__(parent)
        self.parent = parent
        self.callback = callback
        self.existing_labels = existing_labels or []
        self.selected_labels = []
        self.title('添加新任务')
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

        # 已选标签显示
        self.selected_labels_frame = ctk.CTkScrollableFrame(
            self,
            fg_color='transparent',
            height=50,
            label_text='已选标签',
            label_font=CTK_FONT_SMALL,
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
        """更新已选标签的显示."""
        # 清空已有显示
        for widget in self.selected_labels_frame.winfo_children():
            widget.destroy()

        # 显示每个标签
        for i, label in enumerate(self.selected_labels):
            tag_frame = ctk.CTkFrame(
                self.selected_labels_frame,
                fg_color=BG_COLOR_CONTENT,
                corner_radius=4,
            )
            tag_frame.grid(row=i, column=0, pady=2, sticky='ew')
            tag_frame.grid_columnconfigure(0, weight=1)

            tag_label = ctk.CTkLabel(
                tag_frame,
                text=label,
                font=CTK_FONT_SMALL,
                text_color='#f0f0f0',
            )
            tag_label.grid(row=0, column=0, padx=8, pady=4, sticky='w')

            remove_btn = ctk.CTkButton(
                tag_frame,
                text='×',
                width=24,
                height=24,
                font=CTK_FONT_SMALL,
                fg_color='transparent',
                hover_color='#555555',
                command=lambda lbl=label: self.remove_label(lbl),
            )
            remove_btn.grid(row=0, column=1, padx=4, pady=4)

    def remove_label(self, label) -> None:
        """移除已选标签.

        Args:
            label: 要移除的标签
        """
        if label in self.selected_labels:
            self.selected_labels.remove(label)
            self.update_selected_labels_display()

    def on_save(self) -> None:
        """保存任务."""
        content = self.content_entry.get().strip()
        if not content:
            return

        description = self.desc_entry.get('1.0', 'end').strip()
        due = self.due_picker.get_date()

        priority_map = {'普通': 0, '低': 1, '中': 2, '高': 3}
        priority = priority_map.get(self.priority_combobox.get(), 0)

        # 组合标签
        labels = ','.join(self.selected_labels)

        # 调用回调函数保存任务
        self.callback(content, description, due, priority, labels)
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
        self.tasks = []

        # 搜索和筛选状态
        self.search_keyword = ''
        self.filter_status = 'all'  # 'all', 'completed', 'pending'

        # 配置主布局
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.init_ui()
        self.load_tasks_from_db()

    def init_ui(self) -> None:
        """初始化 UI 组件."""
        # 顶部区域：搜索筛选 + 添加按钮
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
            标签列表
        """
        all_labels = set()
        for task in self.tasks:
            if task.get('labels'):
                labels = task['labels'].split(',')
                for label in labels:
                    if label.strip():
                        all_labels.add(label.strip())
        return sorted(list(all_labels))

    def open_add_task_dialog(self) -> None:
        """打开添加任务对话框."""
        existing_labels = self.get_all_labels()
        AddTaskDialog(self.master, self.add_task, existing_labels)

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

        # 重新排列任务行（考虑筛选条件）
        self.redisplay_tasks()

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

        # 任务内容标签
        content_text = task['content']
        if task['due']:
            content_text += f' (截止: {task["due"]})'
        if task['labels']:
            content_text += f' [{task["labels"]}]'

        task_label = ctk.CTkLabel(
            row_frame,
            text=content_text,
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

    def destroy(self) -> None:
        """销毁面板时关闭数据库连接."""
        self.db.close()
        super().destroy()
