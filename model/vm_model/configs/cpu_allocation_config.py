"""CPU 分配配置类 - 使用 dataclass 简化的配置类."""

from dataclasses import dataclass, field

from model.vm_model.cpu.topology import CPUTopology


@dataclass
class CPUAllocationConfig:
    """CPU 分配配置类."""

    max_vcpu: int = 2
    current_vcpu: int = 2
    placement: str = 'static'
    cpuset: str = ''
    topology: CPUTopology = field(default_factory=lambda: CPUTopology.full_topology())
    vcpu_instances: list = field(default_factory=list)

    def update(self, data: dict) -> None:
        """更新配置."""
        for key in ['max_vcpu', 'current_vcpu', 'placement', 'cpuset']:
            if key in data:
                setattr(self, key, data[key])
        if 'topology' in data:
            if isinstance(data['topology'], dict):
                self.topology = CPUTopology.from_dict(data['topology'])
            else:
                self.topology = data['topology']
        if 'vcpu_instances' in data:
            self.vcpu_instances = data['vcpu_instances']

    def to_dict(self) -> dict:
        """转换为字典格式."""
        from dataclasses import asdict

        result = asdict(self)
        result['topology'] = self.topology.to_dict()
        return result
