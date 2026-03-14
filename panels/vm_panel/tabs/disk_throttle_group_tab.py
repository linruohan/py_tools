"""磁盘节流组配置 Tab - Disk Throttle Group."""

import customtkinter as ctk

from components.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class DiskThrottleGroupTab(ctk.CTkFrame):
    """磁盘节流组配置 Tab - 创建命名节流组."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent')
        self.on_change_callback = on_change_callback
        self.throttle_groups = []

        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        left_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        left_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        left_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(left_frame, text='节流组配置', font=CTK_FONT_BOLD, text_color='#64b5f6').grid(
            row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
        )

        ctk.CTkLabel(left_frame, text='组名称:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.group_name = ctk.CTkEntry(left_frame, placeholder_text='limit0', width=150)
        self.group_name.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.group_name.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(left_frame, text='总字节/秒:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.total_bytes_sec = ctk.CTkEntry(left_frame, placeholder_text='10000000', width=150)
        self.total_bytes_sec.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.total_bytes_sec.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(left_frame, text='读字节/秒:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=3, column=0, padx=10, pady=5, sticky='w'
        )
        self.read_bytes_sec = ctk.CTkEntry(left_frame, placeholder_text='字节/秒', width=150)
        self.read_bytes_sec.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        self.read_bytes_sec.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(left_frame, text='写字节/秒:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=4, column=0, padx=10, pady=5, sticky='w'
        )
        self.write_bytes_sec = ctk.CTkEntry(left_frame, placeholder_text='字节/秒', width=150)
        self.write_bytes_sec.grid(row=4, column=1, padx=5, pady=5, sticky='w')
        self.write_bytes_sec.bind('<KeyRelease>', lambda e: self._trigger_change())

        right_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        right_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        right_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(right_frame, text='IOPS 限制', font=CTK_FONT_BOLD, text_color='#4caf50').grid(
            row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
        )

        ctk.CTkLabel(right_frame, text='总 IOPS:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.total_iops_sec = ctk.CTkEntry(right_frame, placeholder_text='次/秒', width=150)
        self.total_iops_sec.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.total_iops_sec.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(right_frame, text='读 IOPS:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.read_iops_sec = ctk.CTkEntry(right_frame, placeholder_text='400000', width=150)
        self.read_iops_sec.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.read_iops_sec.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(right_frame, text='写 IOPS:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=3, column=0, padx=10, pady=5, sticky='w'
        )
        self.write_iops_sec = ctk.CTkEntry(right_frame, placeholder_text='100000', width=150)
        self.write_iops_sec.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        self.write_iops_sec.bind('<KeyRelease>', lambda e: self._trigger_change())

        add_btn = ctk.CTkButton(
            right_frame,
            text='添加节流组',
            command=self._add_throttle_group,
            fg_color='#00bcd4',
            hover_color='#0097a7',
            width=120,
            font=CTK_FONT_SMALL,
        )
        add_btn.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        groups_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        groups_frame.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=5, pady=5)

        ctk.CTkLabel(
            groups_frame, text='已添加的节流组', font=CTK_FONT_BOLD, text_color='#ff9800'
        ).grid(row=0, column=0, padx=10, pady=5, sticky='w')

        self.groups_display = ctk.CTkLabel(
            groups_frame, text='无', font=CTK_FONT_SMALL, text_color='#888888', anchor='w'
        )
        self.groups_display.grid(row=1, column=0, padx=10, pady=5, sticky='w')

    def _add_throttle_group(self):
        """添加节流组."""
        name = self.group_name.get().strip()
        if name:
            group = {
                'name': name,
                'total_bytes_sec': self.total_bytes_sec.get().strip(),
                'read_bytes_sec': self.read_bytes_sec.get().strip(),
                'write_bytes_sec': self.write_bytes_sec.get().strip(),
                'total_iops_sec': self.total_iops_sec.get().strip(),
                'read_iops_sec': self.read_iops_sec.get().strip(),
                'write_iops_sec': self.write_iops_sec.get().strip(),
            }
            self.throttle_groups.append(group)
            self.groups_display.configure(text=', '.join([g['name'] for g in self.throttle_groups]))
            self.group_name.delete(0, 'end')
            self._trigger_change()

    def _trigger_change(self, *args):
        """触发变化回调."""
        if self.on_change_callback:
            self.on_change_callback()

    def get_config(self) -> dict:
        """获取配置数据."""
        return {
            'throttle_groups': self.throttle_groups.copy(),
        }

    def to_xml(self) -> dict:
        """生成XML配置字典."""
        return {'disk_throttle_group': self.get_config()}
