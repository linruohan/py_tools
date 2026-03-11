"""内存后端配置 Tab - Memory Backing."""

import customtkinter as ctk

from ..styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class MemoryBackingTab(ctk.CTkFrame):
    """内存后端配置 Tab - 虚拟内存页的后端配置."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent')
        self.on_change_callback = on_change_callback

        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        left_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        left_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        left_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            left_frame, text='Hugepages 配置', font=CTK_FONT_BOLD, text_color='#64b5f6'
        ).grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w')

        self.hugepages = ctk.CTkCheckBox(
            left_frame, text='启用 Hugepages', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.hugepages.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky='w')

        ctk.CTkLabel(left_frame, text='页面大小:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.page_size = ctk.CTkEntry(left_frame, placeholder_text='2', width=80)
        self.page_size.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.page_size.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(left_frame, text='页面单位:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=3, column=0, padx=10, pady=5, sticky='w'
        )
        self.page_unit = ctk.CTkOptionMenu(
            left_frame,
            values=['KiB', 'MiB', 'GiB'],
            width=80,
            font=CTK_FONT_SMALL,
        )
        self.page_unit.set('MiB')
        self.page_unit.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        self.page_unit.configure(command=self._trigger_change)

        ctk.CTkLabel(left_frame, text='节点集:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=4, column=0, padx=10, pady=5, sticky='w'
        )
        self.nodeset = ctk.CTkEntry(left_frame, placeholder_text='0-3,5', width=120)
        self.nodeset.grid(row=4, column=1, padx=5, pady=5, sticky='w')
        self.nodeset.bind('<KeyRelease>', lambda e: self._trigger_change())

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

    def _trigger_change(self):
        """触发变化回调."""
        if self.on_change_callback:
            self.on_change_callback()

    def get_config(self) -> dict:
        """获取配置数据."""
        return {
            'hugepages': self.hugepages.get(),
            'page_size': self.page_size.get().strip(),
            'page_unit': self.page_unit.get(),
            'nodeset': self.nodeset.get().strip(),
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
