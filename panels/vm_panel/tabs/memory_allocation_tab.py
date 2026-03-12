"""内存分配配置 Tab - Memory Allocation."""

import customtkinter as ctk

from ..styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class MemoryAllocationTab(ctk.CTkFrame):
    """内存分配配置 Tab - 基础内存分配设置."""

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

        ctk.CTkLabel(left_frame, text='内存配置', font=CTK_FONT_BOLD, text_color='#64b5f6').grid(
            row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
        )

        memory_options = [
            '256M',
            '512M',
            '1G',
            '2G',
            '4G',
            '8G',
            '16G',
            '32G',
            '64G',
            '128G',
            '256G',
        ]

        ctk.CTkLabel(left_frame, text='内存:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.memory = ctk.CTkOptionMenu(
            left_frame,
            values=memory_options,
            width=120,
            font=CTK_FONT_SMALL,
        )
        self.memory.set('2G')
        self.memory.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.memory.configure(command=self._trigger_change)

        ctk.CTkLabel(left_frame, text='当前内存:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.current_memory = ctk.CTkOptionMenu(
            left_frame,
            values=memory_options,
            width=120,
            font=CTK_FONT_SMALL,
        )
        self.current_memory.set('2G')
        self.current_memory.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.current_memory.configure(command=self._trigger_change)

        ctk.CTkLabel(left_frame, text='最大内存:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=3, column=0, padx=10, pady=5, sticky='w'
        )
        self.max_memory = ctk.CTkOptionMenu(
            left_frame,
            values=memory_options,
            width=120,
            font=CTK_FONT_SMALL,
        )
        self.max_memory.set('4G')
        self.max_memory.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        self.max_memory.configure(command=self._trigger_change)

        ctk.CTkLabel(left_frame, text='内存槽位:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=4, column=0, padx=10, pady=5, sticky='w'
        )
        self.memory_slots = ctk.CTkEntry(left_frame, placeholder_text='16', width=80)
        self.memory_slots.grid(row=4, column=1, padx=5, pady=5, sticky='w')
        self.memory_slots.insert(0, '16')
        self.memory_slots.bind('<KeyRelease>', lambda e: self._trigger_change())

        right_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        right_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        right_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(right_frame, text='单位设置', font=CTK_FONT_BOLD, text_color='#4caf50').grid(
            row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
        )

        ctk.CTkLabel(right_frame, text='单位:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.memory_unit = ctk.CTkOptionMenu(
            right_frame,
            values=['KiB', 'MiB', 'GiB', 'TiB', 'KB', 'MB', 'GB', 'TB', 'b', 'bytes'],
            width=80,
            font=CTK_FONT_SMALL,
        )
        self.memory_unit.set('KiB')
        self.memory_unit.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.memory_unit.configure(command=self._trigger_change)

        ctk.CTkLabel(
            right_frame, text='Dump Core:', font=CTK_FONT_MAIN, width=100, anchor='w'
        ).grid(row=2, column=0, padx=10, pady=5, sticky='w')
        self.dump_core = ctk.CTkOptionMenu(
            right_frame,
            values=['on', 'off'],
            width=80,
            font=CTK_FONT_SMALL,
        )
        self.dump_core.set('on')
        self.dump_core.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.dump_core.configure(command=self._trigger_change)

        ctk.CTkLabel(right_frame, text='说明', font=CTK_FONT_BOLD, text_color='#ff9800').grid(
            row=3, column=0, columnspan=2, padx=10, pady=10, sticky='w'
        )

        info_text = (
            '内存 (memory):\n'
            '启动时分配的最大内存。\n\n'
            '当前内存 (currentMemory):\n'
            '实际分配的内存，可以小于\n'
            '最大值以支持内存气球。\n\n'
            '最大内存 (maxMemory):\n'
            '运行时可通过热插拔增加\n'
            '到的最大内存限制。'
        )
        ctk.CTkLabel(
            right_frame,
            text=info_text,
            font=CTK_FONT_SMALL,
            text_color='#888888',
            justify='left',
        ).grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky='nw')

    def _trigger_change(self, *args):
        """触发变化回调."""
        if self.on_change_callback:
            self.on_change_callback()

    def _parse_memory(self, value: str) -> int:
        """解析内存值为 KiB."""
        if not value:
            return 2097152
        value = value.strip().upper()
        if value.endswith('G'):
            return int(value[:-1]) * 1024 * 1024
        elif value.endswith('M'):
            return int(value[:-1]) * 1024
        elif value.endswith('T'):
            return int(value[:-1]) * 1024 * 1024 * 1024
        else:
            try:
                return int(value)
            except ValueError:
                return 2097152

    def get_config(self) -> dict:
        """获取配置数据."""
        return {
            'memory': self._parse_memory(self.memory.get()),
            'current_memory': self._parse_memory(self.current_memory.get()),
            'max_memory': self._parse_memory(self.max_memory.get()),
            'memory_slots': int(self.memory_slots.get().strip() or '16'),
            'unit': self.memory_unit.get(),
            'dump_core': self.dump_core.get(),
        }

    def to_xml(self) -> dict:
        """生成XML配置字典."""
        return {'memory_allocation': self.get_config()}
