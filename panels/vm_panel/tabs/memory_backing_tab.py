"""内存后端配置 Tab - Memory Backing."""

import customtkinter as ctk

from ..styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class MemoryBackingTab(ctk.CTkFrame):
    """内存后端配置 Tab - 虚拟内存页的后端配置."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent')
        self.on_change_callback = on_change_callback

        self.hugepage_entries = []

        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # 左侧 - Hugepages 配置
        left_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        left_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        left_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            left_frame, text='Hugepages 配置', font=CTK_FONT_BOLD, text_color='#64b5f6'
        ).grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky='w')

        # Hugepages 列表容器
        self.hugepage_list_frame = ctk.CTkFrame(left_frame, fg_color='transparent')
        self.hugepage_list_frame.grid(row=1, column=0, columnspan=3, sticky='ew', padx=10, pady=5)
        self.hugepage_list_frame.grid_columnconfigure(0, weight=0)

        # 添加按钮
        add_btn = ctk.CTkButton(
            left_frame,
            text='+ 添加页面',
            width=100,
            font=CTK_FONT_SMALL,
            command=self._add_hugepage_entry,
        )
        add_btn.grid(row=2, column=0, padx=10, pady=5, sticky='w')

        # 初始添加一个条目
        self._add_hugepage_entry()

        # 右侧 - 后端设置
        right_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        right_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        right_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(right_frame, text='后端设置', font=CTK_FONT_BOLD, text_color='#4caf50').grid(
            row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
        )

        ctk.CTkLabel(right_frame, text='源类型:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.source_type = ctk.CTkOptionMenu(
            right_frame,
            values=['anonymous', 'file', 'memfd'],
            width=100,
            font=CTK_FONT_SMALL,
        )
        self.source_type.set('anonymous')
        self.source_type.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.source_type.configure(command=self._trigger_change)

        ctk.CTkLabel(right_frame, text='访问模式:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.access_mode = ctk.CTkOptionMenu(
            right_frame,
            values=['private', 'shared'],
            width=100,
            font=CTK_FONT_SMALL,
        )
        self.access_mode.set('private')
        self.access_mode.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.access_mode.configure(command=self._trigger_change)

        ctk.CTkLabel(right_frame, text='分配模式:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=3, column=0, padx=10, pady=5, sticky='w'
        )
        self.allocation_mode = ctk.CTkOptionMenu(
            right_frame,
            values=['immediate', 'ondemand'],
            width=100,
            font=CTK_FONT_SMALL,
        )
        self.allocation_mode.set('ondemand')
        self.allocation_mode.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        self.allocation_mode.configure(command=self._trigger_change)

        ctk.CTkLabel(right_frame, text='分配线程:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=4, column=0, padx=10, pady=5, sticky='w'
        )
        self.allocation_threads = ctk.CTkEntry(right_frame, placeholder_text='8', width=80)
        self.allocation_threads.grid(row=4, column=1, padx=5, pady=5, sticky='w')
        self.allocation_threads.bind('<KeyRelease>', lambda e: self._trigger_change())

        # 底部 - 其他选项
        options_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        options_frame.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=5, pady=5)

        ctk.CTkLabel(options_frame, text='其他选项', font=CTK_FONT_BOLD, text_color='#ff9800').grid(
            row=0, column=0, columnspan=4, padx=10, pady=5, sticky='w'
        )

        self.nosharepages = ctk.CTkCheckBox(
            options_frame,
            text='禁用共享页 (nosharepages)',
            font=CTK_FONT_SMALL,
            command=self._trigger_change,
        )
        self.nosharepages.grid(row=1, column=0, padx=10, pady=5, sticky='w')

        self.locked = ctk.CTkCheckBox(
            options_frame, text='锁定内存', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.locked.grid(row=1, column=1, padx=10, pady=5, sticky='w')

        self.discard = ctk.CTkCheckBox(
            options_frame, text='丢弃内存', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.discard.grid(row=1, column=2, padx=10, pady=5, sticky='w')

    def _add_hugepage_entry(self):
        """添加一个 hugepage 配置条目."""
        row = len(self.hugepage_entries)

        entry_frame = ctk.CTkFrame(self.hugepage_list_frame, fg_color='transparent')
        entry_frame.grid(row=row, column=0, sticky='ew', pady=2)
        entry_frame.grid_columnconfigure(1, weight=1)

        # 页面大小
        size_entry = ctk.CTkEntry(entry_frame, placeholder_text='1', width=60)
        size_entry.grid(row=0, column=0, padx=2, pady=2, sticky='w')
        size_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        # 单位
        unit_menu = ctk.CTkOptionMenu(
            entry_frame, values=['KiB', 'MiB', 'GiB'], width=70, font=CTK_FONT_SMALL
        )
        unit_menu.set('GiB')
        unit_menu.grid(row=0, column=1, padx=2, pady=2, sticky='w')
        unit_menu.configure(command=self._trigger_change)

        # 节点集
        nodeset_entry = ctk.CTkEntry(entry_frame, placeholder_text='0-3,5', width=100)
        nodeset_entry.grid(row=0, column=2, padx=2, pady=2, sticky='w')
        nodeset_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        # 删除按钮
        del_btn = ctk.CTkButton(
            entry_frame,
            text='删除',
            width=50,
            font=CTK_FONT_SMALL,
            command=lambda: self._remove_hugepage_entry(entry_frame),
        )
        del_btn.grid(row=0, column=3, padx=2, pady=2, sticky='w')

        self.hugepage_entries.append(
            {
                'frame': entry_frame,
                'size': size_entry,
                'unit': unit_menu,
                'nodeset': nodeset_entry,
            }
        )

        # 更新删除按钮状态
        self._update_delete_buttons()
        self._trigger_change()

    def _remove_hugepage_entry(self, entry_frame):
        """删除一个 hugepage 配置条目."""
        for i, entry in enumerate(self.hugepage_entries):
            if entry['frame'] == entry_frame:
                entry['frame'].destroy()
                self.hugepage_entries.pop(i)
                break

        # 重新排列剩余条目
        for i, entry in enumerate(self.hugepage_entries):
            entry['frame'].grid(row=i, column=0, sticky='ew', pady=2)

        self._update_delete_buttons()
        self._trigger_change()

    def _update_delete_buttons(self):
        """更新删除按钮的可见性."""
        for i, entry in enumerate(self.hugepage_entries):
            for widget in entry['frame'].winfo_children():
                if isinstance(widget, ctk.CTkButton):
                    if len(self.hugepage_entries) == 1:
                        widget.configure(state='disabled')
                    else:
                        widget.configure(state='normal')

    def _trigger_change(self, *args):
        """触发变化回调."""
        if self.on_change_callback:
            self.on_change_callback()

    def get_config(self) -> dict:
        """获取配置数据."""
        hugepage_list = []
        for entry in self.hugepage_entries:
            size = entry['size'].get().strip()
            unit = entry['unit'].get()
            nodeset = entry['nodeset'].get().strip()
            if size:
                hugepage_list.append(
                    {
                        'size': size,
                        'unit': unit,
                        'nodeset': nodeset,
                    }
                )

        return {
            'hugepages': hugepage_list,
            'source_type': self.source_type.get(),
            'access_mode': self.access_mode.get(),
            'allocation_mode': self.allocation_mode.get(),
            'allocation_threads': self.allocation_threads.get().strip(),
            'nosharepages': self.nosharepages.get(),
            'locked': self.locked.get(),
            'discard': self.discard.get(),
        }

    def to_xml(self) -> dict:
        """生成XML配置字典."""
        return {'memory_backing': self.get_config()}
