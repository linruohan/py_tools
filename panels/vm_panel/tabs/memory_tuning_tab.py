"""内存调优配置 Tab - Memory Tuning."""

import customtkinter as ctk

from components.base_tab import BaseConfigTab
from utils.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class MemoryTuningTab(BaseConfigTab):
    """内存优化配置 Tab - 内存可调参数配置."""

    def _init_ui(self) -> None:
        """初始化界面."""
        # 主容器
        main_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        main_frame.pack(fill='both', expand=True, padx=5, pady=5)

        # 标题
        ctk.CTkLabel(
            main_frame, text='内存调优参数', font=CTK_FONT_BOLD, text_color='#64b5f6'
        ).pack(anchor='w', padx=10, pady=(10, 10))

        # 单位选项
        unit_options = ['None', 'KiB', 'MiB', 'GiB', 'bytes']

        # 所有参数放在一行：硬限制 | 软限制 | 交换硬限制 | 最小保证
        row = ctk.CTkFrame(main_frame, fg_color='transparent')
        row.pack(fill='x', padx=10, pady=3)

        # 硬限制
        ctk.CTkLabel(row, text='硬限制:', font=CTK_FONT_MAIN, width=60, anchor='w').pack(
            side='left'
        )
        self.hard_limit_unit = ctk.CTkOptionMenu(
            row, values=unit_options, width=65, command=self._trigger_change
        )
        self.hard_limit_unit.set('None')
        self.hard_limit_unit.pack(side='left', padx=(0, 2))
        self.hard_limit_value = ctk.CTkEntry(row, placeholder_text='数值', width=100)
        self.hard_limit_value.pack(side='left', padx=(0, 10))
        self.hard_limit_value.bind('<KeyRelease>', lambda e: self._trigger_change())

        # 软限制
        ctk.CTkLabel(row, text='软限制:', font=CTK_FONT_MAIN, width=60, anchor='w').pack(
            side='left'
        )
        self.soft_limit_unit = ctk.CTkOptionMenu(
            row, values=unit_options, width=65, command=self._trigger_change
        )
        self.soft_limit_unit.set('None')
        self.soft_limit_unit.pack(side='left', padx=(0, 2))
        self.soft_limit_value = ctk.CTkEntry(row, placeholder_text='数值', width=100)
        self.soft_limit_value.pack(side='left', padx=(0, 10))
        self.soft_limit_value.bind('<KeyRelease>', lambda e: self._trigger_change())

        # 交换硬限制
        ctk.CTkLabel(row, text='交换硬限制:', font=CTK_FONT_MAIN, width=70, anchor='w').pack(
            side='left'
        )
        self.swap_hard_limit_unit = ctk.CTkOptionMenu(
            row, values=unit_options, width=65, command=self._trigger_change
        )
        self.swap_hard_limit_unit.set('None')
        self.swap_hard_limit_unit.pack(side='left', padx=(0, 2))
        self.swap_hard_limit_value = ctk.CTkEntry(row, placeholder_text='数值', width=100)
        self.swap_hard_limit_value.pack(side='left', padx=(0, 10))
        self.swap_hard_limit_value.bind('<KeyRelease>', lambda e: self._trigger_change())

        # 最小保证
        ctk.CTkLabel(row, text='最小保证:', font=CTK_FONT_MAIN, width=60, anchor='w').pack(
            side='left'
        )
        self.min_guarantee_unit = ctk.CTkOptionMenu(
            row, values=unit_options, width=65, command=self._trigger_change
        )
        self.min_guarantee_unit.set('None')
        self.min_guarantee_unit.pack(side='left', padx=(0, 2))
        self.min_guarantee_value = ctk.CTkEntry(row, placeholder_text='数值', width=100)
        self.min_guarantee_value.pack(side='left')
        self.min_guarantee_value.bind('<KeyRelease>', lambda e: self._trigger_change())

        # 说明区域
        info_frame = ctk.CTkFrame(main_frame, fg_color='transparent')
        info_frame.pack(fill='x', padx=10, pady=(15, 5))

        info_text = (
            '单位说明：选择 "None" 或不填值将不生成对应的 XML 元素\n'
            '硬限制 (hard_limit): 客户机可使用的最大内存\n'
            '软限制 (soft_limit): 内存争用期间强制执行的限制\n'
            '交换硬限制 (swap_hard_limit): 内存 + 交换的最大值\n'
            '最小保证 (min_guarantee): 保证分配的最小内存 (仅 VMware ESX 和 OpenVZ 支持)'
        )
        ctk.CTkLabel(
            info_frame,
            text=info_text,
            font=CTK_FONT_SMALL,
            text_color='#888888',
            justify='left',
        ).pack(anchor='w')

        # 警告区域
        warning_frame = ctk.CTkFrame(main_frame, fg_color='#fff3e0', corner_radius=6)
        warning_frame.pack(fill='x', padx=10, pady=10)

        ctk.CTkLabel(warning_frame, text='警告', font=CTK_FONT_BOLD, text_color='#ff9800').pack(
            anchor='w', padx=10, pady=(5, 0)
        )

        warning_text = (
            '对于 QEMU/KVM，建议不要设置硬限制，因为如果猜测过低，\n'
            '域可能会被内核杀死。确定进程运行所需的内存是一个不可判定的问题。\n'
            '如果启用了内存锁定，则需要根据部署情况计算合适的硬限制值。'
        )
        ctk.CTkLabel(
            warning_frame,
            text=warning_text,
            font=CTK_FONT_SMALL,
            text_color='#aaaaaa',
            justify='left',
        ).pack(anchor='w', padx=10, pady=(0, 5))

    def get_config(self) -> dict:
        """获取配置数据."""

        def get_item(unit_widget, value_widget) -> dict:
            unit = unit_widget.get()
            value = value_widget.get().strip()
            if unit == 'None' or value == '':
                return {'value': None, 'unit': 'KiB'}
            return {'value': value, 'unit': unit}

        return {
            'hard_limit': get_item(self.hard_limit_unit, self.hard_limit_value),
            'soft_limit': get_item(self.soft_limit_unit, self.soft_limit_value),
            'swap_hard_limit': get_item(self.swap_hard_limit_unit, self.swap_hard_limit_value),
            'min_guarantee': get_item(self.min_guarantee_unit, self.min_guarantee_value),
        }

    def to_xml(self) -> dict:
        """生成 XML 配置字典."""
        return {'memory_tuning': self.get_config()}
