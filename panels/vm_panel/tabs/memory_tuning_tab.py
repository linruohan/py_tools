"""内存优化配置 Tab - Memory Tuning."""

import customtkinter as ctk

from components.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class MemoryTuningTab(ctk.CTkFrame):
    """内存优化配置 Tab - 内存可调参数配置."""

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

        ctk.CTkLabel(left_frame, text='内存限制', font=CTK_FONT_BOLD, text_color='#64b5f6').grid(
            row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
        )

        ctk.CTkLabel(left_frame, text='硬限制:', font=CTK_FONT_MAIN, width=120, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.hard_limit = ctk.CTkEntry(left_frame, placeholder_text='KiB (无限制留空)', width=150)
        self.hard_limit.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.hard_limit.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(left_frame, text='软限制:', font=CTK_FONT_MAIN, width=120, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.soft_limit = ctk.CTkEntry(left_frame, placeholder_text='KiB (无限制留空)', width=150)
        self.soft_limit.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.soft_limit.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(
            left_frame, text='交换硬限制:', font=CTK_FONT_MAIN, width=120, anchor='w'
        ).grid(row=3, column=0, padx=10, pady=5, sticky='w')
        self.swap_hard_limit = ctk.CTkEntry(
            left_frame, placeholder_text='KiB (无限制留空)', width=150
        )
        self.swap_hard_limit.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        self.swap_hard_limit.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(left_frame, text='最小保证:', font=CTK_FONT_MAIN, width=120, anchor='w').grid(
            row=4, column=0, padx=10, pady=5, sticky='w'
        )
        self.min_guarantee = ctk.CTkEntry(
            left_frame, placeholder_text='KiB (仅VMware/OpenVZ)', width=150
        )
        self.min_guarantee.grid(row=4, column=1, padx=5, pady=5, sticky='w')
        self.min_guarantee.bind('<KeyRelease>', lambda e: self._trigger_change())

        right_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        right_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)

        ctk.CTkLabel(right_frame, text='说明', font=CTK_FONT_BOLD, text_color='#4caf50').grid(
            row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
        )

        info_text = (
            '硬限制 (hard_limit):\n'
            '客户机可使用的最大内存。\n\n'
            '软限制 (soft_limit):\n'
            '内存争用期间强制执行的限制。\n\n'
            '交换硬限制 (swap_hard_limit):\n'
            '内存+交换的最大值。\n\n'
            '最小保证 (min_guarantee):\n'
            '保证分配的最小内存。\n'
            '(仅VMware ESX和OpenVZ支持)'
        )
        info_label = ctk.CTkLabel(
            right_frame,
            text=info_text,
            font=CTK_FONT_SMALL,
            text_color='#888888',
            justify='left',
        )
        info_label.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky='nw')

        warning_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        warning_frame.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=5, pady=5)

        ctk.CTkLabel(warning_frame, text='⚠️ 警告', font=CTK_FONT_BOLD, text_color='#ff9800').grid(
            row=0, column=0, padx=10, pady=5, sticky='w'
        )

        warning_text = (
            '对于QEMU/KVM,建议不要设置硬限制,因为如果猜测过低,\n'
            '域可能会被内核杀死。确定进程运行所需的内存是一个不可判定的问题。\n'
            '如果启用了内存锁定,则需要根据部署情况计算合适的硬限制值。'
        )
        ctk.CTkLabel(
            warning_frame,
            text=warning_text,
            font=CTK_FONT_SMALL,
            text_color='#aaaaaa',
            justify='left',
        ).grid(row=1, column=0, padx=10, pady=5, sticky='w')

    def _trigger_change(self, *args):
        """触发变化回调."""
        if self.on_change_callback:
            self.on_change_callback()

    def get_config(self) -> dict:
        """获取配置数据."""
        return {
            'hard_limit': self.hard_limit.get().strip(),
            'soft_limit': self.soft_limit.get().strip(),
            'swap_hard_limit': self.swap_hard_limit.get().strip(),
            'min_guarantee': self.min_guarantee.get().strip(),
        }

    def to_xml(self) -> dict:
        """生成XML配置字典."""
        return {'memory_tuning': self.get_config()}
