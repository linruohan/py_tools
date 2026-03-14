"""IO 线程分配配置 Tab - IOThreads Allocation."""

from typing import ClassVar

from components.base_tab import FieldConfig, SectionConfig, StandardConfigTab


class IOThreadsAllocationTab(StandardConfigTab):
    """IO 线程分配配置 Tab."""

    SECTIONS: ClassVar[dict] = {
        'left': SectionConfig(
            title='IO 线程配置',
            fields=[
                FieldConfig(
                    'IO 线程数:', 'entry', '0', placeholder='0-禁用', label_width=110, width=80
                ),
                FieldConfig(
                    '线程池最小:', 'entry', '0', placeholder='0', label_width=110, width=80
                ),
                FieldConfig(
                    '线程池最大:', 'entry', '0', placeholder='0', label_width=110, width=80
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
                    'IOThreads 是专用事件循环线程,\n'
                    '用于支持磁盘设备的块 I/O 请求,\n'
                    '可提高 SMP 主机/客户机的可扩展性.\n\n'
                    '建议:\n'
                    '• 每个 IOThread 对应 1-2 个主机 CPU\n'
                    '• 多个设备可分配到同一 IOThread\n'
                    '• 仅 QEMU/KVM 支持',
                )
            ],
            color='#4caf50',
        ),
    }

    def get_config(self) -> dict:
        """获取配置数据."""
        children = self.section_frames['left'].winfo_children()
        return {
            'iothreads': int(children[1].get().strip() or '0'),
            'thread_pool_min': int(children[2].get().strip() or '0'),
            'thread_pool_max': int(children[3].get().strip() or '0'),
        }

    def to_xml(self) -> dict:
        """生成 XML 配置字典."""
        return {'iothreads_allocation': self.get_config()}
