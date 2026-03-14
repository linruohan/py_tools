"""CPU 分配配置 Tab - vCPU 分配和配置."""

from components.base_tab import BaseConfigTab, create_three_column_layout
from utils.parsers import parse_integer_value


class CPUAllocationTab(BaseConfigTab):
    """CPU 分配配置 Tab."""

    def _init_ui(self) -> None:
        """初始化界面."""
        left_frame, mid_frame, right_frame = create_three_column_layout(
            self,
            left_title='vCPU 配置',
            mid_title='CPU 拓扑',
            right_title='vCPU 状态',
            left_color='#64b5f6',
            mid_color='#4caf50',
            right_color='#ff9800',
        )

        # 左侧面板 - vCPU 配置
        self.max_vcpu = self._create_label_entry(
            left_frame, '最大 vCPU:', placeholder='2', default_value='2', width=100, row=1
        )
        self.current_vcpu = self._create_label_entry(
            left_frame, '当前 vCPU:', placeholder='2', default_value='2', width=100, row=2
        )
        self.placement = self._create_label_option(
            left_frame, '放置模式:', ['static', 'auto'], 'static', width=100, row=3
        )
        self.cpuset = self._create_label_entry(
            left_frame, 'CPU 亲和性:', placeholder='1-4,^3', width=150, row=4
        )

        # 中间面板 - CPU 拓扑
        self.sockets = self._create_label_entry(
            mid_frame,
            'Sockets:',
            placeholder='1',
            default_value='1',
            width=80,
            row=1,
            label_width=80,
        )
        self.dies = self._create_label_entry(
            mid_frame, 'Dies:', placeholder='1', default_value='1', width=80, row=2, label_width=80
        )
        self.clusters = self._create_label_entry(
            mid_frame,
            'Clusters:',
            placeholder='1',
            default_value='1',
            width=80,
            row=3,
            label_width=80,
        )
        self.cores = self._create_label_entry(
            mid_frame, 'Cores:', placeholder='2', default_value='2', width=80, row=4, label_width=80
        )
        self.threads = self._create_label_entry(
            mid_frame,
            'Threads:',
            placeholder='1',
            default_value='1',
            width=80,
            row=5,
            label_width=80,
        )

        # 右侧面板 - vCPU 状态
        self.vcpu_id = self._create_label_entry(
            right_frame, 'vCPU ID:', placeholder='0', width=80, row=1, label_width=80
        )
        self.vcpu_enabled = self._create_label_checkbox(
            right_frame, '启用:', default_checked=True, row=2, label_width=80
        )
        self.hotpluggable = self._create_label_checkbox(
            right_frame, '热插拔:', default_checked=False, row=3, label_width=80
        )
        self.vcpu_order = self._create_label_entry(
            right_frame, '顺序:', placeholder='1', width=80, row=4, label_width=80
        )

    def get_config(self) -> dict:
        """获取配置数据."""
        return {
            'max_vcpu': parse_integer_value(self.max_vcpu.get(), default=2),
            'current_vcpu': parse_integer_value(self.current_vcpu.get(), default=2),
            'placement': self.placement.get(),
            'cpuset': self.cpuset.get().strip(),
            'topology': {
                'sockets': parse_integer_value(self.sockets.get(), default=1),
                'dies': parse_integer_value(self.dies.get(), default=1),
                'clusters': parse_integer_value(self.clusters.get(), default=1),
                'cores': parse_integer_value(self.cores.get(), default=2),
                'threads': parse_integer_value(self.threads.get(), default=1),
            },
            'vcpu_state': {
                'id': parse_integer_value(self.vcpu_id.get(), default=0),
                'enabled': self.vcpu_enabled.get(),
                'hotpluggable': self.hotpluggable.get(),
                'order': parse_integer_value(self.vcpu_order.get(), default=1),
            },
        }

    def to_xml(self) -> dict:
        """生成XML配置字典."""
        return {'cpu_allocation': self.get_config()}
