"""资源分区配置 Tab - Resource Partitioning."""

import customtkinter as ctk

from components.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class ResourcePartitioningTab(ctk.CTkFrame):
    """资源分区配置 Tab."""

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

        ctk.CTkLabel(left_frame, text='资源分区', font=CTK_FONT_BOLD, text_color='#64b5f6').grid(
            row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
        )

        ctk.CTkLabel(left_frame, text='分区路径:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.partition = ctk.CTkEntry(
            left_frame, placeholder_text='/virtualmachines/production', width=220
        )
        self.partition.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.partition.bind('<KeyRelease>', lambda e: self._trigger_change())

        right_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        right_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)

        ctk.CTkLabel(
            right_frame, text='光纤通道 VMID', font=CTK_FONT_BOLD, text_color='#4caf50'
        ).grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w')

        ctk.CTkLabel(right_frame, text='App ID:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.fibrechannel_appid = ctk.CTkEntry(
            right_frame, placeholder_text='最大128字节', width=150
        )
        self.fibrechannel_appid.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.fibrechannel_appid.bind('<KeyRelease>', lambda e: self._trigger_change())

        info_label = ctk.CTkLabel(
            right_frame,
            text='FC SAN 可根据 VMID 提供\n不同 QoS 级别和访问控制,\n也可收集遥测数据。',
            font=CTK_FONT_SMALL,
            text_color='#888888',
            justify='left',
        )
        info_label.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky='w')

    def _trigger_change(self, *args):
        """触发变化回调."""
        if self.on_change_callback:
            self.on_change_callback()

    def get_config(self) -> dict:
        """获取配置数据."""
        return {
            'partition': self.partition.get().strip(),
            'fibrechannel_appid': self.fibrechannel_appid.get().strip(),
        }

    def to_xml(self) -> dict:
        """生成XML配置字典."""
        return {
            'resource_partitioning': {'partition': self.partition.get().strip()},
            'fibre_channel_vmid': {'appid': self.fibrechannel_appid.get().strip()},
        }
