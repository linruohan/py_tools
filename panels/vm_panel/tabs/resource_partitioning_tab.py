"""资源分区配置 Tab - Resource Partitioning."""

import customtkinter as ctk

from components.base_tab import BaseConfigTab
from utils.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class ResourcePartitioningTab(BaseConfigTab):
    """资源分区配置 Tab."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, on_change_callback, **kwargs)

        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面."""
        self.grid_columnconfigure(0, weight=1)

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

        info_frame = ctk.CTkFrame(left_frame, fg_color='transparent')
        info_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky='w')

        info_text = """说明:
• 资源分区支持嵌套,可设置绝对路径(如:/parent/child)
• 如不设置分区,domain 将放置在默认分区中
• 仅默认分区可假设已存在,其他分区需管理员预先创建
• 启动 guest 前请确保分区路径已存在
• 当前支持:QEMU 和 LXC 驱动(映射到 cgroups 目录)
• 自 libvirt 1.0.5 版本起支持"""

        ctk.CTkLabel(
            info_frame,
            text=info_text,
            font=CTK_FONT_SMALL,
            text_color='#888888',
            justify='left',
            anchor='nw',
        ).pack(side='left')

    def get_config(self) -> dict:
        """获取配置数据."""
        return {
            'partition': self.partition.get().strip(),
        }

    def to_xml(self) -> dict:
        """生成 XML 配置字典."""
        partition_value = self.partition.get().strip()

        # 如果没有设置分区路径,返回空的 resource 元素
        # 表示使用默认分区
        if not partition_value:
            return {
                'resource_partitioning': {},
            }

        # 如果设置了分区路径,包含 partition 子元素
        return {
            'resource_partitioning': {'partition': partition_value},
        }
