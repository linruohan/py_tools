"""电源管理配置 Tab - Power Management."""

from typing import ClassVar

from components.base_tab import FieldConfig, SectionConfig, StandardConfigTab


class PowerManagementTab(StandardConfigTab):
    """电源管理配置 Tab."""

    SECTIONS: ClassVar[dict] = {
        'left': SectionConfig(
            title='电源管理',
            fields=[
                FieldConfig('S3 (挂起到内存):', 'option', 'yes', ['yes', 'no'], label_width=130),
                FieldConfig('S4 (挂起到磁盘):', 'option', 'yes', ['yes', 'no'], label_width=130),
            ],
            color='#64b5f6',
        ),
        'right': SectionConfig(
            title='说明',
            fields=[
                FieldConfig(
                    'info',
                    'info',
                    'S3 (挂起到内存):\n系统状态保存到内存,\n功耗较低,唤醒较快.\n\n'
                    'S4 (挂起到磁盘):\n系统状态保存到磁盘,\n功耗最低,唤醒较慢.\n\n'
                    '注意:此设置无法阻止\n客户机自行执行挂起操作.',
                )
            ],
            color='#4caf50',
        ),
    }

    def get_config(self) -> dict:
        """获取配置数据."""
        # 从 left_frame 中获取 OptionMenu 控件 (第 1、2 个子控件,索引从 1 开始跳过标题)
        children = self.section_frames['left'].winfo_children()
        return {
            'suspend_to_mem': children[1].get(),
            'suspend_to_disk': children[2].get(),
        }

    def to_xml(self) -> dict:
        """生成 XML 配置字典."""
        return {'power_management': self.get_config()}
