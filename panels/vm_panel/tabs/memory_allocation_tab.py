"""内存分配配置 Tab - Memory Allocation."""

from components.base_tab import BaseConfigTab, create_two_column_layout
from utils.parsers import MEMORY_OPTIONS, parse_integer_value


class MemoryAllocationTab(BaseConfigTab):
    """内存分配配置 Tab - 基础内存分配设置."""

    def _init_ui(self) -> None:
        """初始化界面."""
        left_frame, right_frame = create_two_column_layout(
            self,
            left_title='内存配置',
            right_title='单位设置',
            left_color='#64b5f6',
            right_color='#4caf50',
        )

        memory_options_with_none = ['None', *MEMORY_OPTIONS]

        # 左侧面板 - 内存配置
        self.memory = self._create_label_option(left_frame, '内存:', MEMORY_OPTIONS, '2G', row=1)
        self.current_memory = self._create_label_option(
            left_frame, '当前内存:', memory_options_with_none, '2G', row=2
        )
        self.max_memory = self._create_label_option(
            left_frame, '最大内存:', memory_options_with_none, '4G', row=3
        )
        self.memory_slots = self._create_label_entry(
            left_frame, '内存槽位:', placeholder='16', default_value='16', width=80, row=4
        )

        # 右侧面板 - 单位设置
        self.memory_unit = self._create_label_option(
            right_frame,
            '单位:',
            ['KiB', 'MiB', 'GiB', 'TiB', 'KB', 'MB', 'GB', 'TB', 'b', 'bytes'],
            'KiB',
            width=80,
            row=1,
        )
        self.dump_core = self._create_label_option(
            right_frame, 'Dump Core:', ['None', 'on', 'off'], 'on', width=80, row=2
        )

        # 说明信息
        self._create_section_title(right_frame, '说明', text_color='#ff9800', row=3)
        info_text = (
            '内存 (memory):启动时分配的最大内存.\n'
            '当前内存 (currentMemory):实际分配的内存,可以小于最大值以支持内存气球.\n'
            '最大内存 (maxMemory):运行时可通过热插拔增加到的最大内存限制.'
        )
        self._create_info_label(right_frame, info_text, row=4)

    def get_config(self) -> dict:
        """获取配置数据."""
        from utils.parsers import parse_memory_value

        target_unit = self.memory_unit.get()
        memory = parse_memory_value(self.memory.get(), target_unit=target_unit)

        current_memory_raw = self.current_memory.get()
        current_memory = (
            None
            if current_memory_raw == 'None'
            else parse_memory_value(current_memory_raw, target_unit=target_unit)
        )

        max_memory_raw = self.max_memory.get()
        max_memory = (
            None
            if max_memory_raw == 'None'
            else parse_memory_value(max_memory_raw, target_unit=target_unit)
        )

        memory_config = {
            'memory': memory,
            'unit': self.memory_unit.get(),
        }
        dump_core_value = self.dump_core.get()
        if dump_core_value != 'None':
            memory_config['dump_core'] = dump_core_value == 'on'
        if current_memory is not None:
            memory_config['current_memory'] = current_memory
        if max_memory is not None:
            memory_config['max_memory'] = max_memory
            memory_config['memory_slots'] = parse_integer_value(self.memory_slots.get(), default=16)

        return memory_config

    def to_xml(self) -> dict:
        """生成XML配置字典."""
        return {'memory_allocation': self.get_config()}
