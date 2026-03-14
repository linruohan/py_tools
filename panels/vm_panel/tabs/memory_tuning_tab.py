"""内存优化配置 Tab - Memory Tuning."""

from typing import ClassVar

import customtkinter as ctk

from components.base_tab import (
    BG_COLOR_CONTENT,
    CTK_FONT_BOLD,
    CTK_FONT_SMALL,
    FieldConfig,
    SectionConfig,
    StandardConfigTab,
)


class MemoryTuningTab(StandardConfigTab):
    """内存优化配置 Tab - 内存可调参数配置."""

    SECTIONS: ClassVar[dict] = {
        'left': SectionConfig(
            title='内存限制',
            fields=[
                FieldConfig(
                    '硬限制:',
                    'entry',
                    '',
                    placeholder='KiB (无限制留空)',
                    label_width=120,
                    width=150,
                ),
                FieldConfig(
                    '软限制:',
                    'entry',
                    '',
                    placeholder='KiB (无限制留空)',
                    label_width=120,
                    width=150,
                ),
                FieldConfig(
                    '交换硬限制:',
                    'entry',
                    '',
                    placeholder='KiB (无限制留空)',
                    label_width=120,
                    width=150,
                ),
                FieldConfig(
                    '最小保证:',
                    'entry',
                    '',
                    placeholder='KiB (仅 VMware/OpenVZ)',
                    label_width=120,
                    width=150,
                ),
            ],
            color='#64b5f6',
        ),
        'right': SectionConfig(
            title='说明',
            fields=[
                FieldConfig(
                    'info',
                    'info',
                    '硬限制 (hard_limit):\n客户机可使用的最大内存.\n\n'
                    '软限制 (soft_limit):\n内存争用期间强制执行的限制.\n\n'
                    '交换硬限制 (swap_hard_limit):\n内存 + 交换的最大值.\n\n'
                    '最小保证 (min_guarantee):\n保证分配的最小内存.\n(仅 VMware ESX 和 OpenVZ 支持)',
                )
            ],
            color='#4caf50',
        ),
    }

    def _init_ui(self) -> None:
        """初始化界面 - 添加警告区域."""
        super()._init_ui()

        # 添加警告区域
        warning_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        warning_frame.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=5, pady=5)

        ctk.CTkLabel(warning_frame, text='警告', font=CTK_FONT_BOLD, text_color='#ff9800').grid(
            row=0, column=0, padx=10, pady=5, sticky='w'
        )

        warning_text = (
            '对于 QEMU/KVM,建议不要设置硬限制,因为如果猜测过低,\n'
            '域可能会被内核杀死.确定进程运行所需的内存是一个不可判定的问题.\n'
            '如果启用了内存锁定,则需要根据部署情况计算合适的硬限制值.'
        )
        ctk.CTkLabel(
            warning_frame,
            text=warning_text,
            font=CTK_FONT_SMALL,
            text_color='#aaaaaa',
            justify='left',
        ).grid(row=1, column=0, padx=10, pady=5, sticky='w')

    def get_config(self) -> dict:
        """获取配置数据."""
        children = self.section_frames['left'].winfo_children()
        return {
            'hard_limit': children[1].get().strip(),
            'soft_limit': children[2].get().strip(),
            'swap_hard_limit': children[3].get().strip(),
            'min_guarantee': children[4].get().strip(),
        }

    def to_xml(self) -> dict:
        """生成 XML 配置字典."""
        return {'memory_tuning': self.get_config()}
