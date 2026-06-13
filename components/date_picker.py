"""日期选择组件."""

from datetime import datetime

import customtkinter as ctk

from utils.styles import BG_COLOR_CONTENT, CTK_FONT_MAIN


class DatePicker(ctk.CTkFrame):
    """日期选择组件."""

    def __init__(
        self,
        master,
        on_select_callback=None,
        placeholder_text='选择日期',
        **kwargs,
    ):
        """初始化日期选择组件.

        Args:
            master: 父容器
            on_select_callback: 选中回调函数
            placeholder_text: 输入框占位文本
        """
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent')

        self.on_select_callback = on_select_callback
        self.placeholder_text = placeholder_text
        self.date_window = None

        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)

        # 输入框 - 通过阻止键盘输入来禁止编辑，同时让 placeholder 能正常显示
        self.date_entry = ctk.CTkEntry(
            self,
            placeholder_text=self.placeholder_text,
            font=CTK_FONT_MAIN,
            fg_color=BG_COLOR_CONTENT,
            border_width=1,
        )
        self.date_entry.grid(row=0, column=0, sticky='ew', padx=0, pady=0)

        # 阻止键盘输入
        self.date_entry.bind('<Key>', lambda e: 'break')

        # 点击整个组件都弹出日历
        self.bind('<Button-1>', lambda e: self._show_calendar())
        self.date_entry.bind('<Button-1>', lambda e: self._show_calendar())

    def _show_calendar(self) -> None:
        """显示日历窗口."""
        # 如果日历窗口已经显示，关闭它
        if self.date_window is not None:
            try:
                self.date_window.destroy()
                self.date_window = None
            except Exception:
                self.date_window = None
            return

        # 创建日历窗口
        self.date_window = ctk.CTkToplevel(self)
        self.date_window.overrideredirect(True)  # 去掉标题栏
        self.date_window.geometry('230x220')  # 调整尺寸消除空白
        self.date_window.resizable(False, False)
        self.date_window.attributes('-topmost', True)

        # 位置（显示在输入框下方，左对齐）
        entry_x = self.date_entry.winfo_rootx()
        entry_y = self.date_entry.winfo_rooty()
        entry_height = self.date_entry.winfo_height()
        self.date_window.geometry(f'230x220+{entry_x}+{entry_y + entry_height}')

        # 初始化日历
        self.current_year = datetime.now().year
        self.current_month = datetime.now().month

        self._init_calendar_ui()

    def _init_calendar_ui(self) -> None:
        """初始化日历界面."""
        # 主框架 - 更紧凑布局
        main_frame = ctk.CTkFrame(self.date_window, fg_color='#242424', corner_radius=4)
        main_frame.pack(fill='both', expand=True, padx=2, pady=2)

        # 标题框架
        header_frame = ctk.CTkFrame(main_frame, fg_color='transparent')
        header_frame.pack(fill='x', pady=(2, 1))

        # 上一个月按钮 - 更紧凑
        prev_btn = ctk.CTkButton(
            header_frame,
            text='◀',
            width=24,
            height=22,
            font=CTK_FONT_MAIN,
            fg_color='#64b5f6',
            hover_color='#42a5f5',
            corner_radius=4,
            command=self._prev_month,
        )
        prev_btn.pack(side='left', padx=(1, 1))

        # 月份年份显示
        self.month_year_label = ctk.CTkLabel(
            header_frame, text='', font=CTK_FONT_MAIN, text_color='#f0f0f0'
        )
        self.month_year_label.pack(side='left', expand=True)

        # 下一个月按钮 - 更紧凑
        next_btn = ctk.CTkButton(
            header_frame,
            text='▶',
            width=24,
            height=22,
            font=CTK_FONT_MAIN,
            fg_color='#64b5f6',
            hover_color='#42a5f5',
            corner_radius=4,
            command=self._next_month,
        )
        next_btn.pack(side='left', padx=(1, 1))

        # 星期标题 - 使用grid布局更紧凑
        week_frame = ctk.CTkFrame(main_frame, fg_color='transparent')
        week_frame.pack(fill='x', pady=(1, 1))
        week_frame.grid_columnconfigure(list(range(7)), weight=1)

        weekdays = ['日', '一', '二', '三', '四', '五', '六']
        for i, day in enumerate(weekdays):
            label = ctk.CTkLabel(
                week_frame,
                text=day,
                font=CTK_FONT_MAIN,
                text_color='#aaaaaa',
            )
            label.grid(row=0, column=i, sticky='nsew', padx=0)

        # 日期按钮框架
        self.days_frame = ctk.CTkFrame(main_frame, fg_color='transparent')
        self.days_frame.pack(fill='both', expand=True, pady=1)

        # 底部按钮框架
        bottom_frame = ctk.CTkFrame(main_frame, fg_color='transparent')
        bottom_frame.pack(fill='x', pady=(1, 2))
        bottom_frame.grid_columnconfigure(0, weight=1)
        bottom_frame.grid_columnconfigure(1, weight=1)

        # 清空按钮
        clear_btn = ctk.CTkButton(
            bottom_frame,
            text='清空',
            font=CTK_FONT_MAIN,
            fg_color='#666666',
            hover_color='#555555',
            corner_radius=4,
            height=22,
            command=self._clear_date,
        )
        clear_btn.grid(row=0, column=0, padx=1, sticky='ew')

        # 今天按钮
        today_btn = ctk.CTkButton(
            bottom_frame,
            text='今天',
            font=CTK_FONT_MAIN,
            fg_color='#64b5f6',
            hover_color='#42a5f5',
            corner_radius=4,
            height=22,
            command=self._select_today,
        )
        today_btn.grid(row=0, column=1, padx=1, sticky='ew')

        # 初始更新
        self._update_calendar()

    def _update_calendar(self) -> None:
        """更新日历显示."""
        # 更新月份年份标签
        months = [
            '一月',
            '二月',
            '三月',
            '四月',
            '五月',
            '六月',
            '七月',
            '八月',
            '九月',
            '十月',
            '十一月',
            '十二月',
        ]
        self.month_year_label.configure(
            text=f'{self.current_year}年 {months[self.current_month - 1]}'
        )

        # 清空日期按钮
        for widget in self.days_frame.winfo_children():
            widget.destroy()

        # 使用grid布局，设置7列
        for col in range(7):
            self.days_frame.grid_columnconfigure(col, weight=1, uniform='day_col')

        # 获取当前月份第一天的星期几（0是周一，6是周日）
        import calendar

        first_day_weekday = calendar.monthrange(self.current_year, self.current_month)[0]
        days_in_month = calendar.monthrange(self.current_year, self.current_month)[1]

        # 今天
        today = datetime.now()
        today_day = (
            today.day
            if (today.year == self.current_year and today.month == self.current_month)
            else -1
        )

        # 填充上个月的天数（以周日为第一列）
        adjusted_first_day = (first_day_weekday + 1) % 7

        # 当前位置
        current_row = 0
        current_col = adjusted_first_day

        # 填充当前月份的天数
        for day in range(1, days_in_month + 1):
            is_today = day == today_day
            btn = ctk.CTkButton(
                self.days_frame,
                text=str(day),
                font=CTK_FONT_MAIN,
                fg_color='#4caf50' if is_today else BG_COLOR_CONTENT,
                hover_color='#555555',
                height=22,
                command=lambda d=day: self._select_date(d),
            )
            btn.grid(row=current_row, column=current_col, padx=1, pady=1, sticky='nsew')

            current_col += 1
            if current_col >= 7:
                current_col = 0
                current_row += 1

    def _prev_month(self) -> None:
        """上个月."""
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self._update_calendar()

    def _next_month(self) -> None:
        """下个月."""
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self._update_calendar()

    def _select_date(self, day: int) -> None:
        """选择日期.

        Args:
            day: 日期
        """
        date_str = f'{self.current_year}-{self.current_month:02d}-{day:02d}'
        self.date_entry.delete(0, 'end')
        self.date_entry.insert(0, date_str)

        if self.date_window:
            self.date_window.destroy()
            self.date_window = None

        if self.on_select_callback:
            self.on_select_callback(date_str)

    def _select_today(self) -> None:
        """选择今天."""
        today = datetime.now()
        self._select_date(today.day)

    def _clear_date(self) -> None:
        """清空日期."""
        self.date_entry.delete(0, 'end')

        if self.date_window:
            self.date_window.destroy()
            self.date_window = None

        if self.on_select_callback:
            self.on_select_callback('')

    def get_date(self) -> str:
        """获取选中的日期.

        Returns:
            日期字符串 'YYYY-MM-DD'
        """
        return str(self.date_entry.get()).strip()

    def set_date(self, date_str: str) -> None:
        """设置日期.

        Args:
            date_str: 日期字符串 'YYYY-MM-DD'
        """
        self.date_entry.delete(0, 'end')
        self.date_entry.insert(0, date_str)
