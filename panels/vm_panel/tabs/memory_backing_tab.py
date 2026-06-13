"""内存后端配置 Tab - Memory Backing."""

import customtkinter as ctk

from components.base_tab import BaseConfigTab
from utils.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class MemoryBackingTab(BaseConfigTab):
    """内存后端配置 Tab - 虚拟内存页的后端配置."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, on_change_callback, **kwargs)

    def _init_ui(self) -> None:
        """初始化界面 - 所有 section 合并为一个,每个组中所有元素放到一行,pack 布局,左对齐."""
        # 初始化 hugepage 列表
        self.hugepage_entries = []

        # 主容器
        main_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        main_frame.pack(fill='both', expand=True, padx=5, pady=5)

        # 标题
        ctk.CTkLabel(
            main_frame, text='内存后端配置', font=CTK_FONT_BOLD, text_color='#64b5f6'
        ).pack(anchor='w', padx=10, pady=(10, 10))

        # ===== Hugepages 配置行 =====
        hugepage_frame = ctk.CTkFrame(main_frame, fg_color='transparent')
        hugepage_frame.pack(fill='x', padx=10, pady=3)

        ctk.CTkLabel(
            hugepage_frame, text='Hugepages:', font=CTK_FONT_BOLD, width=80, anchor='w'
        ).pack(side='left')

        # 添加按钮
        add_btn = ctk.CTkButton(
            hugepage_frame,
            text='+ 添加',
            width=60,
            font=CTK_FONT_SMALL,
            command=self._add_hugepage_entry,
        )
        add_btn.pack(side='left', padx=(0, 10))

        # Hugepages 列表容器
        self.hugepage_list_frame = ctk.CTkFrame(hugepage_frame, fg_color='transparent')
        self.hugepage_list_frame.pack(side='left', fill='x', expand=True)
        self.hugepage_list_frame.pack_propagate(False)
        self.hugepage_list_frame.configure(height=40)

        # 初始添加一个条目
        self._add_hugepage_entry()

        # ===== 后端设置行 =====
        backend_frame = ctk.CTkFrame(main_frame, fg_color='transparent')
        backend_frame.pack(fill='x', padx=10, pady=3)

        ctk.CTkLabel(
            backend_frame, text='后端设置:', font=CTK_FONT_BOLD, width=80, anchor='w'
        ).pack(side='left')

        # 源类型
        ctk.CTkLabel(backend_frame, text='源:', font=CTK_FONT_MAIN, width=30, anchor='w').pack(
            side='left', padx=(5, 0)
        )
        self.source_type = ctk.CTkOptionMenu(
            backend_frame,
            values=['None', 'anonymous', 'file', 'memfd'],
            width=90,
            font=CTK_FONT_SMALL,
            command=self._trigger_change,
        )
        self.source_type.set('None')
        self.source_type.pack(side='left', padx=(0, 5))

        # 访问模式
        ctk.CTkLabel(backend_frame, text='访问:', font=CTK_FONT_MAIN, width=40, anchor='w').pack(
            side='left', padx=(5, 0)
        )
        self.access_mode = ctk.CTkOptionMenu(
            backend_frame,
            values=['None', 'private', 'shared'],
            width=80,
            font=CTK_FONT_SMALL,
            command=self._trigger_change,
        )
        self.access_mode.set('None')
        self.access_mode.pack(side='left', padx=(0, 5))

        # 分配模式
        ctk.CTkLabel(backend_frame, text='分配:', font=CTK_FONT_MAIN, width=40, anchor='w').pack(
            side='left', padx=(5, 0)
        )
        self.allocation_mode = ctk.CTkOptionMenu(
            backend_frame,
            values=['None', 'immediate', 'ondemand'],
            width=90,
            font=CTK_FONT_SMALL,
            command=self._trigger_change,
        )
        self.allocation_mode.set('None')
        self.allocation_mode.pack(side='left', padx=(0, 5))

        # 分配线程
        ctk.CTkLabel(backend_frame, text='线程:', font=CTK_FONT_MAIN, width=40, anchor='w').pack(
            side='left', padx=(5, 0)
        )
        self.allocation_threads = ctk.CTkEntry(backend_frame, placeholder_text='8', width=60)
        self.allocation_threads.pack(side='left', padx=(0, 5))
        self.allocation_threads.bind('<KeyRelease>', lambda e: self._trigger_change())

        # ===== 其他选项行 =====
        options_frame = ctk.CTkFrame(main_frame, fg_color='transparent')
        options_frame.pack(fill='x', padx=10, pady=3)

        ctk.CTkLabel(
            options_frame, text='其他选项:', font=CTK_FONT_BOLD, width=80, anchor='w'
        ).pack(side='left')

        self.nosharepages = ctk.CTkCheckBox(
            options_frame,
            text='禁用共享页',
            font=CTK_FONT_SMALL,
            command=self._trigger_change,
        )
        self.nosharepages.pack(side='left', padx=(5, 10))

        self.locked = ctk.CTkCheckBox(
            options_frame, text='锁定内存', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.locked.pack(side='left', padx=(0, 10))

        self.discard = ctk.CTkCheckBox(
            options_frame, text='丢弃内存', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.discard.pack(side='left', padx=(0, 10))

        # 说明区域
        info_frame = ctk.CTkFrame(main_frame, fg_color='transparent')
        info_frame.pack(fill='x', padx=10, pady=(15, 5))

        info_text = (
            '说明:选择 "None" 或不填值将不生成对应的 XML 元素\n'
            'Hugepages: 大页面配置,可指定大小和单位 (GiB/MiB/KiB)\n'
            '源类型:anonymous(匿名), file(文件), memfd(内存文件描述符)\n'
            '访问模式:private(私有), shared(共享)\n'
            '分配模式:immediate(立即), ondemand(按需)'
        )
        ctk.CTkLabel(
            info_frame,
            text=info_text,
            font=CTK_FONT_SMALL,
            text_color='#888888',
            justify='left',
        ).pack(anchor='w')

    def _add_hugepage_entry(self):
        """添加一个 hugepage 配置条目."""
        _ = len(self.hugepage_entries)  # 保留用于将来的行号计算

        entry_frame = ctk.CTkFrame(self.hugepage_list_frame, fg_color='transparent')
        entry_frame.pack(side='left', padx=2, pady=2)

        # 页面大小
        size_entry = ctk.CTkEntry(entry_frame, placeholder_text='大小', width=50)
        size_entry.pack(side='left')
        size_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        # 单位
        unit_menu = ctk.CTkOptionMenu(
            entry_frame, values=['KiB', 'MiB', 'GiB'], width=60, font=CTK_FONT_SMALL
        )
        unit_menu.set('GiB')
        unit_menu.pack(side='left', padx=2)
        unit_menu.configure(command=self._trigger_change)

        # 节点集
        nodeset_entry = ctk.CTkEntry(entry_frame, placeholder_text='nodeset', width=80)
        nodeset_entry.pack(side='left', padx=2)
        nodeset_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        # 删除按钮
        del_btn = ctk.CTkButton(
            entry_frame,
            text='X',
            width=30,
            font=CTK_FONT_SMALL,
            command=lambda: self._remove_hugepage_entry(entry_frame),
        )
        del_btn.pack(side='left', padx=2)

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

        self._update_delete_buttons()
        self._trigger_change()

    def _update_delete_buttons(self):
        """更新删除按钮的可见性."""
        for entry in self.hugepage_entries:
            for widget in entry['frame'].winfo_children():
                if isinstance(widget, ctk.CTkButton):
                    if len(self.hugepage_entries) == 1:
                        widget.configure(state='disabled')
                    else:
                        widget.configure(state='normal')

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

        # 处理源类型 - 'None' 转换为 'anonymous' (默认值,不生成 XML)
        source_type = self.source_type.get()
        if source_type == 'None':
            source_type = 'anonymous'

        # 处理访问模式 - 'None' 转换为 'private' (默认值,不生成 XML)
        access_mode = self.access_mode.get()
        if access_mode == 'None':
            access_mode = 'private'

        # 处理分配模式 - 'None' 转换为 'ondemand' (默认值,不生成 XML)
        allocation_mode = self.allocation_mode.get()
        if allocation_mode == 'None':
            allocation_mode = 'ondemand'

        return {
            'hugepages': hugepage_list,
            'source_type': source_type,
            'access_mode': access_mode,
            'allocation_mode': allocation_mode,
            'allocation_threads': self.allocation_threads.get().strip(),
            'nosharepages': self.nosharepages.get(),
            'locked': self.locked.get(),
            'discard': self.discard.get(),
        }

    def to_xml(self) -> dict:
        """生成 XML 配置字典."""
        return {'memory_backing': self.get_config()}
