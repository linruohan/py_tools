"""NUMA 节点优化配置 Tab - NUMA Node Tuning."""

import customtkinter as ctk

from ..styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class NUMANodeTuningTab(ctk.CTkFrame):
    """NUMA 节点优化配置 Tab."""

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
            left_frame, text='NUMA 内存策略', font=CTK_FONT_BOLD, text_color='#64b5f6'
        ).grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w')

        ctk.CTkLabel(left_frame, text='模式:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.mode = ctk.CTkOptionMenu(
            left_frame,
            values=['strict', 'interleave', 'preferred', 'restrictive'],
            width=120,
            font=CTK_FONT_SMALL,
        )
        self.mode.set('strict')
        self.mode.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.mode.configure(command=self._trigger_change)

        ctk.CTkLabel(left_frame, text='节点集:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.nodeset = ctk.CTkEntry(left_frame, placeholder_text='1-4,^3', width=150)
        self.nodeset.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.nodeset.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(left_frame, text='放置:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=3, column=0, padx=10, pady=5, sticky='w'
        )
        self.placement = ctk.CTkOptionMenu(
            left_frame,
            values=['static', 'auto'],
            width=80,
            font=CTK_FONT_SMALL,
        )
        self.placement.set('static')
        self.placement.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        self.placement.configure(command=self._trigger_change)

        right_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        right_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)

        ctk.CTkLabel(
            right_frame, text='NUMA 节点配置', font=CTK_FONT_BOLD, text_color='#4caf50'
        ).grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w')

        ctk.CTkLabel(right_frame, text='Cell ID:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.cellid = ctk.CTkEntry(right_frame, placeholder_text='0', width=80)
        self.cellid.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.cellid.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(right_frame, text='CPUs:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.cpus = ctk.CTkEntry(right_frame, placeholder_text='0-3', width=80)
        self.cpus.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.cpus.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(right_frame, text='内存:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=3, column=0, padx=10, pady=5, sticky='w'
        )
        self.memory = ctk.CTkEntry(right_frame, placeholder_text='512000', width=80)
        self.memory.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        self.memory.bind('<KeyRelease>', lambda e: self._trigger_change())

    def _trigger_change(self):
        """触发变化回调."""
        if self.on_change_callback:
            self.on_change_callback()

    def get_config(self) -> dict:
        """获取配置数据."""
        return {
            'mode': self.mode.get(),
            'nodeset': self.nodeset.get().strip(),
            'placement': self.placement.get(),
            'cellid': self.cellid.get().strip(),
            'cpus': self.cpus.get().strip(),
            'memory': self.memory.get().strip(),
        }

    def to_xml(self) -> dict:
        """生成XML配置字典."""
        return {'numa_node_tuning': self.get_config()}
