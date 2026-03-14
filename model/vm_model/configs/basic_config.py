"""基础信息配置类 - 管理虚拟机基础配置信息."""


class BasicConfig:
    """基础信息配置类."""

    def __init__(self):
        """初始化基础配置."""
        self.name = 'vm0'
        self.title = ''
        self.description = ''
        self.uuid = ''
        self.genid = ''
        self.arch = 'x86'
        self.machine = 'virt'
        self.virt_type = 'hvm'
        self.chipset = 'virtio'
        self.vcpu = 2
        self.cpu_mode = 'host-model'
        self.cpu_topology = {
            'sockets': 1,
            'cores': 2,
            'threads': 1,
        }
        self.memory = 2048  # MB
        self.current_memory = 2048  # MB
        self.max_memory = 4096  # MB
        self.swap = 0  # MB

    def update(self, data: dict) -> None:
        """更新配置.

        Args:
            data: 配置数据
        """
        if 'name' in data:
            self.name = data['name']
        if 'title' in data:
            self.title = data['title']
        if 'description' in data:
            self.description = data['description']
        if 'uuid' in data:
            self.uuid = data['uuid']
        if 'genid' in data:
            self.genid = data['genid']
        if 'arch' in data:
            self.arch = data['arch']
        if 'machine' in data:
            self.machine = data['machine']
        if 'virt_type' in data:
            self.virt_type = data['virt_type']
        if 'chipset' in data:
            self.chipset = data['chipset']
        if 'vcpu' in data:
            self.vcpu = data['vcpu']
        if 'cpu_mode' in data:
            self.cpu_mode = data['cpu_mode']
        if 'cpu_topology' in data:
            self.cpu_topology.update(data['cpu_topology'])
        if 'memory' in data:
            self.memory = data['memory']
        if 'current_memory' in data:
            self.current_memory = data['current_memory']
        if 'max_memory' in data:
            self.max_memory = data['max_memory']
        if 'swap' in data:
            self.swap = data['swap']

    def to_dict(self) -> dict:
        """转换为字典格式.

        Returns:
            配置字典
        """
        return {
            'name': self.name,
            'title': self.title,
            'description': self.description,
            'uuid': self.uuid,
            'genid': self.genid,
            'arch': self.arch,
            'machine': self.machine,
            'virt_type': self.virt_type,
            'chipset': self.chipset,
            'vcpu': self.vcpu,
            'cpu_mode': self.cpu_mode,
            'cpu_topology': self.cpu_topology,
            'memory': self.memory,
            'current_memory': self.current_memory,
            'max_memory': self.max_memory,
            'swap': self.swap,
        }
