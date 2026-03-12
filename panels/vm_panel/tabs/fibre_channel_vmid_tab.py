"""光纤通道 VMID 配置 Tab - Fibre Channel VMID."""

import customtkinter as ctk

from ..styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class FibreChannelVMIDTab(ctk.CTkFrame):
    """光纤通道 VMID 配置 Tab - FC SAN QoS 和访问控制."""

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
            left_frame, text='FC VMID 配置', font=CTK_FONT_BOLD, text_color='#64b5f6'
        ).grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w')

        ctk.CTkLabel(left_frame, text='App ID:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.appid = ctk.CTkEntry(left_frame, placeholder_text='最大128字节', width=200)
        self.appid.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.appid.bind('<KeyRelease>', lambda e: self._trigger_change())

        right_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        right_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)

        ctk.CTkLabel(right_frame, text='功能说明', font=CTK_FONT_BOLD, text_color='#4caf50').grid(
            row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
        )

        info_text = (
            'FC SAN 可以根据 VMID 提供:\n\n'
            '• 不同的 QoS 级别\n'
            '• 访问控制\n'
            '• 收集遥测数据\n'
            '• 增强 IO 性能\n\n'
            '使用此功能需要:\n'
            '• 支持 Fibre Channel 的硬件\n'
            '• 内核编译选项 CONFIG_BLK_CGROUP_FC_APPID\n'
            '• 加载 nvme_fc 内核模块'
        )
        info_label = ctk.CTkLabel(
            right_frame,
            text=info_text,
            font=CTK_FONT_SMALL,
            text_color='#888888',
            justify='left',
        )
        info_label.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky='nw')

        example_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        example_frame.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=5, pady=5)

        ctk.CTkLabel(example_frame, text='XML 示例', font=CTK_FONT_BOLD, text_color='#9c27b0').grid(
            row=0, column=0, padx=10, pady=5, sticky='w'
        )

        example_text = "<resource>\n  <fibrechannel appid='userProvidedID'/>\n</resource>"
        ctk.CTkLabel(
            example_frame,
            text=example_text,
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
            'appid': self.appid.get().strip(),
        }

    def to_xml(self) -> dict:
        """生成XML配置字典."""
        return {'fibre_channel_vmid': self.get_config()}
