"""基础信息配置类 - 使用 dataclass 简化的配置类."""

from dataclasses import dataclass, field

from ..cpu.topology import CPUTopology


@dataclass
class BasicConfig:
    """基础信息配置类."""

    name: str = 'vm0'
    title: str = ''
    description: str = ''
    uuid: str = ''
    genid: str = ''
    arch: str = 'x86'
    machine: str = 'virt'
    virt_type: str = 'hvm'
    chipset: str = 'virtio'
    vcpu: int = 2
    cpu_mode: str = 'host-model'
    cpu_topology: CPUTopology = field(default_factory=lambda: CPUTopology.basic_topology())
    memory: int = 2048  # MB
    current_memory: int = 2048  # MB
    max_memory: int = 4096  # MB
    swap: int = 0  # MB

    def update(self, data: dict) -> None:
        """更新配置."""
        for key in [
            'name',
            'title',
            'description',
            'uuid',
            'genid',
            'arch',
            'machine',
            'virt_type',
            'chipset',
            'vcpu',
            'cpu_mode',
            'memory',
            'current_memory',
            'max_memory',
            'swap',
        ]:
            if key in data:
                setattr(self, key, data[key])
        if 'cpu_topology' in data:
            if isinstance(data['cpu_topology'], dict):
                self.cpu_topology = CPUTopology.from_dict(data['cpu_topology'])
            else:
                self.cpu_topology = data['cpu_topology']

    def to_dict(self) -> dict:
        """转换为字典格式."""
        from dataclasses import asdict

        result = asdict(self)
        result['cpu_topology'] = self.cpu_topology.to_dict()
        return result
