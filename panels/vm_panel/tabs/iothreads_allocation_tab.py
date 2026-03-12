"""IO 线程分配配置 Tab - IOThreads Allocation."""

import customtkinter as ctk

from ..styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class IOThreadsAllocationTab(ctk.CTkFrame):
    """IO 线程分配配置 Tab."""

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

        ctk.CTkLabel(left_frame, text='IO 线程配置', font=CTK_FONT_BOLD, text_color='#64b5f6').grid(
            row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
        )

        ctk.CTkLabel(left_frame, text='IO 线程数:', font=CTK_FONT_MAIN, width=110, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.iothreads = ctk.CTkEntry(left_frame, placeholder_text='0-禁用', width=80)
        self.iothreads.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.iothreads.insert(0, '0')
        self.iothreads.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(
            left_frame, text='线程池最小:', font=CTK_FONT_MAIN, width=110, anchor='w'
        ).grid(row=2, column=0, padx=10, pady=5, sticky='w')
        self.thread_pool_min = ctk.CTkEntry(left_frame, placeholder_text='0', width=80)
        self.thread_pool_min.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.thread_pool_min.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(
            left_frame, text='线程池最大:', font=CTK_FONT_MAIN, width=110, anchor='w'
        ).grid(row=3, column=0, padx=10, pady=5, sticky='w')
        self.thread_pool_max = ctk.CTkEntry(left_frame, placeholder_text='0', width=80)
        self.thread_pool_max.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        self.thread_pool_max.bind('<KeyRelease>', lambda e: self._trigger_change())

        right_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        right_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)

        ctk.CTkLabel(right_frame, text='说明', font=CTK_FONT_BOLD, text_color='#4caf50').grid(
            row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
        )

        info_text = (
            'IOThreads 是专用事件循环线程,\n'
            '用于支持磁盘设备的块 I/O 请求,\n'
            '可提高 SMP 主机/客户机的可扩展性。\n\n'
            '建议:\n'
            '• 每个 IOThread 对应 1-2 个主机 CPU\n'
            '• 多个设备可分配到同一 IOThread\n'
            '• 仅 QEMU/KVM 支持'
        )
        info_label = ctk.CTkLabel(
            right_frame,
            text=info_text,
            font=CTK_FONT_SMALL,
            text_color='#888888',
            justify='left',
        )
        info_label.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky='w')

    def _trigger_change(self, *args):
        """触发变化回调."""
        if self.on_change_callback:
            self.on_change_callback()

    def get_config(self) -> dict:
        """获取配置数据."""
        return {
            'iothreads': int(self.iothreads.get().strip() or '0'),
            'thread_pool_min': int(self.thread_pool_min.get().strip() or '0'),
            'thread_pool_max': int(self.thread_pool_max.get().strip() or '0'),
        }

    def to_xml(self) -> dict:
        """生成XML配置字典."""
        return {'iothreads_allocation': self.get_config()}
