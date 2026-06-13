"""磁盘节流组配置 Tab - Disk Throttle Group."""

import customtkinter as ctk

from components.base_tab import BaseConfigTab
from utils.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class DiskThrottleGroupTab(BaseConfigTab):
    """磁盘节流组配置 Tab - 创建命名节流组."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, on_change_callback, **kwargs)
        self.throttle_groups = []
        self.selected_group_index = None

    def _init_ui(self) -> None:
        """初始化界面."""
        # 上方:输入区域
        input_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        input_frame.pack(fill='x', padx=5, pady=5, anchor='w')

        # None 选项
        self.use_none_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            input_frame,
            text='不使用节流组 (None)',
            variable=self.use_none_var,
            command=self._on_use_none_changed,
            font=CTK_FONT_SMALL,
        ).pack(side='left', padx=5)

        ctk.CTkLabel(input_frame, text='名称:', font=CTK_FONT_MAIN).pack(side='left', padx=2)
        self.group_name = ctk.CTkEntry(input_frame, placeholder_text='limit0', width=80)
        self.group_name.pack(side='left', padx=2)
        self.group_name.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(input_frame, text='总 B/s:', font=CTK_FONT_MAIN).pack(side='left', padx=2)
        self.total_bytes_sec = ctk.CTkEntry(input_frame, placeholder_text='10M', width=70)
        self.total_bytes_sec.pack(side='left', padx=2)
        self.total_bytes_sec.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(input_frame, text='读 B/s:', font=CTK_FONT_MAIN).pack(side='left', padx=2)
        self.read_bytes_sec = ctk.CTkEntry(input_frame, placeholder_text='B/s', width=70)
        self.read_bytes_sec.pack(side='left', padx=2)
        self.read_bytes_sec.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(input_frame, text='写 B/s:', font=CTK_FONT_MAIN).pack(side='left', padx=2)
        self.write_bytes_sec = ctk.CTkEntry(input_frame, placeholder_text='B/s', width=70)
        self.write_bytes_sec.pack(side='left', padx=2)
        self.write_bytes_sec.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(input_frame, text='总 IOPS:', font=CTK_FONT_MAIN).pack(side='left', padx=2)
        self.total_iops_sec = ctk.CTkEntry(input_frame, placeholder_text='/s', width=60)
        self.total_iops_sec.pack(side='left', padx=2)
        self.total_iops_sec.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(input_frame, text='读 IOPS:', font=CTK_FONT_MAIN).pack(side='left', padx=2)
        self.read_iops_sec = ctk.CTkEntry(input_frame, placeholder_text='400k', width=60)
        self.read_iops_sec.pack(side='left', padx=2)
        self.read_iops_sec.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(input_frame, text='写 IOPS:', font=CTK_FONT_MAIN).pack(side='left', padx=2)
        self.write_iops_sec = ctk.CTkEntry(input_frame, placeholder_text='100k', width=60)
        self.write_iops_sec.pack(side='left', padx=2)
        self.write_iops_sec.bind('<KeyRelease>', lambda e: self._trigger_change())

        # 按钮组
        add_btn = ctk.CTkButton(
            input_frame,
            text='添加/更新',
            command=self._add_throttle_group,
            fg_color='#00bcd4',
            hover_color='#0097a7',
            width=70,
            font=CTK_FONT_SMALL,
        )
        add_btn.pack(side='left', padx=5)

        clear_btn = ctk.CTkButton(
            input_frame,
            text='清空',
            command=self._clear_input,
            fg_color='#757575',
            hover_color='#616161',
            width=50,
            font=CTK_FONT_SMALL,
        )
        clear_btn.pack(side='left', padx=2)

        # 下方:节流组列表
        groups_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        groups_frame.pack(fill='both', expand=True, padx=5, pady=5, anchor='w')

        ctk.CTkLabel(
            groups_frame, text='已添加的节流组', font=CTK_FONT_BOLD, text_color='#ff9800'
        ).pack(anchor='w', padx=10, pady=5)

        # 节流组列表框
        self.groups_listbox_frame = ctk.CTkScrollableFrame(
            groups_frame, fg_color='transparent', height=150
        )
        self.groups_listbox_frame.pack(fill='both', expand=True, padx=10, pady=5)

        self.groups_label = ctk.CTkLabel(
            groups_frame, text='无', font=CTK_FONT_SMALL, text_color='#888888', anchor='w'
        )
        self.groups_label.pack(anchor='w', padx=10, pady=5)

    def _on_use_none_changed(self) -> None:
        """None 选项改变时的回调."""
        self._trigger_change()

    def _clear_input(self) -> None:
        """清空输入框."""
        self.group_name.delete(0, 'end')
        self.total_bytes_sec.delete(0, 'end')
        self.read_bytes_sec.delete(0, 'end')
        self.write_bytes_sec.delete(0, 'end')
        self.total_iops_sec.delete(0, 'end')
        self.read_iops_sec.delete(0, 'end')
        self.write_iops_sec.delete(0, 'end')
        self.selected_group_index = None

    def _add_throttle_group(self) -> None:
        """添加或更新节流组."""
        name = self.group_name.get().strip()
        if not name:
            return

        group = {
            'name': name,
            'total_bytes_sec': self._parse_int(self.total_bytes_sec.get()),
            'read_bytes_sec': self._parse_int(self.read_bytes_sec.get()),
            'write_bytes_sec': self._parse_int(self.write_bytes_sec.get()),
            'total_iops_sec': self._parse_int(self.total_iops_sec.get()),
            'read_iops_sec': self._parse_int(self.read_iops_sec.get()),
            'write_iops_sec': self._parse_int(self.write_iops_sec.get()),
        }

        # 检查是否已存在同名组
        for i, existing in enumerate(self.throttle_groups):
            if existing['name'] == name:
                self.throttle_groups[i] = group
                self.selected_group_index = i
                self._refresh_groups_listbox()
                self._trigger_change()
                return

        self.throttle_groups.append(group)
        self._refresh_groups_listbox()
        self._trigger_change()

    def _parse_int(self, value: str) -> int | None:
        """将字符串转换为整数,空字符串返回 None."""
        value = value.strip()
        if not value:
            return None
        try:
            return int(value)
        except ValueError:
            return None

    def _refresh_groups_listbox(self) -> None:
        """刷新节流组列表显示."""
        # 清空列表
        for widget in self.groups_listbox_frame.winfo_children():
            widget.destroy()

        if not self.throttle_groups:
            self.groups_label.configure(text='无')
            return

        self.groups_label.configure(text=f'共 {len(self.throttle_groups)} 个节流组')

        # 添加列表项
        for i, group in enumerate(self.throttle_groups):
            row_frame = ctk.CTkFrame(self.groups_listbox_frame, fg_color='transparent')
            row_frame.pack(fill='x', pady=2)

            # 组名和限值摘要
            limits = []
            if group.get('total_bytes_sec'):
                limits.append(f'B:{group["total_bytes_sec"]}')
            if group.get('read_iops_sec'):
                limits.append(f'RI:{group["read_iops_sec"]}')
            if group.get('write_iops_sec'):
                limits.append(f'WI:{group["write_iops_sec"]}')
            limits_str = ', '.join(limits) if limits else '无限值'

            ctk.CTkLabel(
                row_frame,
                text=f'{i + 1}. {group["name"]} ({limits_str})',
                font=CTK_FONT_SMALL,
                anchor='w',
            ).pack(side='left', fill='x', expand=True)

            # 选择按钮
            select_btn = ctk.CTkButton(
                row_frame,
                text='编辑',
                width=50,
                font=CTK_FONT_SMALL,
                command=lambda idx=i: self._select_group(idx),
            )
            select_btn.pack(side='right', padx=2)

            # 删除按钮
            delete_btn = ctk.CTkButton(
                row_frame,
                text='删除',
                width=50,
                font=CTK_FONT_SMALL,
                fg_color='#d32f2f',
                hover_color='#b71c1c',
                command=lambda idx=i: self._delete_group(idx),
            )
            delete_btn.pack(side='right', padx=2)

    def _select_group(self, index: int) -> None:
        """选择节流组进行编辑."""
        if 0 <= index < len(self.throttle_groups):
            group = self.throttle_groups[index]
            self.selected_group_index = index

            self.group_name.delete(0, 'end')
            self.group_name.insert(0, group.get('name', ''))

            self._set_entry_text(self.total_bytes_sec, group.get('total_bytes_sec'))
            self._set_entry_text(self.read_bytes_sec, group.get('read_bytes_sec'))
            self._set_entry_text(self.write_bytes_sec, group.get('write_bytes_sec'))
            self._set_entry_text(self.total_iops_sec, group.get('total_iops_sec'))
            self._set_entry_text(self.read_iops_sec, group.get('read_iops_sec'))
            self._set_entry_text(self.write_iops_sec, group.get('write_iops_sec'))

    def _delete_group(self, index: int) -> None:
        """删除节流组."""
        if 0 <= index < len(self.throttle_groups):
            self.throttle_groups.pop(index)
            if self.selected_group_index == index:
                self._clear_input()
            elif self.selected_group_index is not None and self.selected_group_index > index:
                self.selected_group_index -= 1
            self._refresh_groups_listbox()
            self._trigger_change()

    def _set_entry_text(self, entry: ctk.CTkEntry, value: int | None) -> None:
        """设置 Entry 的文本."""
        entry.delete(0, 'end')
        if value is not None:
            entry.insert(0, str(value))

    def get_config(self) -> dict:
        """获取配置数据."""
        # 如果选中了 None 选项,返回空配置
        if self.use_none_var.get():
            return {'throttle_groups': [], 'use_none': True}
        return {'throttle_groups': self.throttle_groups.copy(), 'use_none': False}

    def load_config(self, config: dict) -> None:
        """加载配置."""
        self._clear_input()
        self.throttle_groups = []
        self.use_none_var.set(False)

        if config:
            groups = config.get('throttle_groups', [])
            if isinstance(groups, list):
                self.throttle_groups = groups.copy()
            use_none = config.get('use_none', False)
            self.use_none_var.set(use_none)

        self._refresh_groups_listbox()

    def to_xml(self) -> dict:
        """生成 XML 配置字典."""
        config = self.get_config()
        # 如果选中 None,不生成 throttlegroups 元素
        if config.get('use_none'):
            return {'disk_throttle_group': {'throttle_groups': []}}
        return {'disk_throttle_group': config}
