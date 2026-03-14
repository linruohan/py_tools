"""CPU分配配置类 - 管理虚拟机CPU分配配置信息."""


class CPUAllocationConfig:
    """CPU分配配置类."""

    def __init__(self):
        """初始化CPU分配配置."""
        self.max_vcpu = 2
        self.current_vcpu = 2
        self.placement = 'static'
        self.cpuset = ''
        self.topology = {
            'sockets': 1,
            'dies': 1,
            'clusters': 1,
            'cores': 2,
            'threads': 1,
        }

    def update(self, data: dict) -> None:
        """更新配置.

        Args:
            data: 配置数据
        """
        if 'max_vcpu' in data:
            self.max_vcpu = data['max_vcpu']
        if 'current_vcpu' in data:
            self.current_vcpu = data['current_vcpu']
        if 'placement' in data:
            self.placement = data['placement']
        if 'cpuset' in data:
            self.cpuset = data['cpuset']
        if 'topology' in data:
            self.topology.update(data['topology'])

    def to_dict(self) -> dict:
        """转换为字典格式.

        Returns:
            配置字典
        """
        return {
            'max_vcpu': self.max_vcpu,
            'current_vcpu': self.current_vcpu,
            'placement': self.placement,
            'cpuset': self.cpuset,
            'topology': self.topology,
        }
