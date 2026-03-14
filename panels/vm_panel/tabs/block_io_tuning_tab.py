"""块 I/O 优化配置 Tab - Block I/O Tuning."""

import customtkinter as ctk

from utils.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN


class BlockIOTuningTab(ctk.CTkFrame):
    """块 I/O 优化配置 Tab."""

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
            left_frame, text='全局 I/O 权重', font=CTK_FONT_BOLD, text_color='#64b5f6'
        ).grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w')

        ctk.CTkLabel(left_frame, text='权重:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.weight = ctk.CTkEntry(left_frame, placeholder_text='100-1000', width=100)
        self.weight.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.weight.insert(0, '500')
        self.weight.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(
            left_frame, text='设备 I/O 限制', font=CTK_FONT_BOLD, text_color='#4caf50'
        ).grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky='w')

        ctk.CTkLabel(left_frame, text='设备路径:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=3, column=0, padx=10, pady=5, sticky='w'
        )
        self.device_path = ctk.CTkEntry(left_frame, placeholder_text='/dev/sda', width=150)
        self.device_path.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        self.device_path.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(left_frame, text='设备权重:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=4, column=0, padx=10, pady=5, sticky='w'
        )
        self.device_weight = ctk.CTkEntry(left_frame, placeholder_text='100-1000', width=100)
        self.device_weight.grid(row=4, column=1, padx=5, pady=5, sticky='w')
        self.device_weight.bind('<KeyRelease>', lambda e: self._trigger_change())

        right_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        right_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        right_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(right_frame, text='吞吐量限制', font=CTK_FONT_BOLD, text_color='#ff9800').grid(
            row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
        )

        ctk.CTkLabel(right_frame, text='读 (B/s):', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.read_bytes_sec = ctk.CTkEntry(right_frame, placeholder_text='字节/秒', width=120)
        self.read_bytes_sec.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.read_bytes_sec.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(right_frame, text='写 (B/s):', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.write_bytes_sec = ctk.CTkEntry(right_frame, placeholder_text='字节/秒', width=120)
        self.write_bytes_sec.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.write_bytes_sec.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(right_frame, text='IOPS 限制', font=CTK_FONT_BOLD, text_color='#9c27b0').grid(
            row=3, column=0, columnspan=2, padx=10, pady=10, sticky='w'
        )

        ctk.CTkLabel(right_frame, text='读 IOPS:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=4, column=0, padx=10, pady=5, sticky='w'
        )
        self.read_iops_sec = ctk.CTkEntry(right_frame, placeholder_text='次/秒', width=120)
        self.read_iops_sec.grid(row=4, column=1, padx=5, pady=5, sticky='w')
        self.read_iops_sec.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(right_frame, text='写 IOPS:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=5, column=0, padx=10, pady=5, sticky='w'
        )
        self.write_iops_sec = ctk.CTkEntry(right_frame, placeholder_text='次/秒', width=120)
        self.write_iops_sec.grid(row=5, column=1, padx=5, pady=5, sticky='w')
        self.write_iops_sec.bind('<KeyRelease>', lambda e: self._trigger_change())

    def _trigger_change(self, *args):
        """触发变化回调."""
        if self.on_change_callback:
            self.on_change_callback()

    def get_config(self) -> dict:
        """获取配置数据."""
        return {
            'weight': self.weight.get().strip(),
            'device_path': self.device_path.get().strip(),
            'device_weight': self.device_weight.get().strip(),
            'read_bytes_sec': self.read_bytes_sec.get().strip(),
            'write_bytes_sec': self.write_bytes_sec.get().strip(),
            'read_iops_sec': self.read_iops_sec.get().strip(),
            'write_iops_sec': self.write_iops_sec.get().strip(),
        }

    def to_xml(self) -> dict:
        """生成XML配置字典."""
        return {'block_io_tuning': self.get_config()}
