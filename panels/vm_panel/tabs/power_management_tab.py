"""电源管理配置 Tab - Power Management."""

import customtkinter as ctk

from utils.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class PowerManagementTab(ctk.CTkFrame):
    """电源管理配置 Tab."""

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

        ctk.CTkLabel(left_frame, text='电源管理', font=CTK_FONT_BOLD, text_color='#64b5f6').grid(
            row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
        )

        ctk.CTkLabel(
            left_frame, text='S3 (挂起到内存):', font=CTK_FONT_MAIN, width=130, anchor='w'
        ).grid(row=1, column=0, padx=10, pady=5, sticky='w')
        self.suspend_to_mem = ctk.CTkOptionMenu(
            left_frame,
            values=['yes', 'no'],
            width=80,
            font=CTK_FONT_SMALL,
        )
        self.suspend_to_mem.set('yes')
        self.suspend_to_mem.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.suspend_to_mem.configure(command=self._trigger_change)

        ctk.CTkLabel(
            left_frame, text='S4 (挂起到磁盘):', font=CTK_FONT_MAIN, width=130, anchor='w'
        ).grid(row=2, column=0, padx=10, pady=5, sticky='w')
        self.suspend_to_disk = ctk.CTkOptionMenu(
            left_frame,
            values=['yes', 'no'],
            width=80,
            font=CTK_FONT_SMALL,
        )
        self.suspend_to_disk.set('yes')
        self.suspend_to_disk.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.suspend_to_disk.configure(command=self._trigger_change)

        right_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        right_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)

        ctk.CTkLabel(right_frame, text='说明', font=CTK_FONT_BOLD, text_color='#4caf50').grid(
            row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
        )

        info_text = (
            'S3 (挂起到内存):\n'
            '系统状态保存到内存,\n'
            '功耗较低,唤醒较快。\n\n'
            'S4 (挂起到磁盘):\n'
            '系统状态保存到磁盘,\n'
            '功耗最低,唤醒较慢。\n\n'
            '注意: 此设置无法阻止\n'
            '客户机自行执行挂起操作。'
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
            'suspend_to_mem': self.suspend_to_mem.get(),
            'suspend_to_disk': self.suspend_to_disk.get(),
        }

    def to_xml(self) -> dict:
        """生成XML配置字典."""
        return {'power_management': self.get_config()}
