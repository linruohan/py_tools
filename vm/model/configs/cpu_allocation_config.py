"""CPU 分配配置类 - 使用 dataclass 简化的配置类."""

from dataclasses import dataclass, field

from ..cpu.topology import CPUTopology


@dataclass
class CPUAllocationConfig:
    """CPU 分配配置类."""

    max_vcpu: int = 2
    current_vcpu: int = 2
    placement: str = 'static'
    cpuset: str = ''
    topology: CPUTopology = field(default_factory=lambda: CPUTopology.full_topology())
    vcpu_instances: list = field(default_factory=list)
    # CPU 模型和拓扑相关配置
    mode: str = 'host-model'  # custom, host-model, host-passthrough, maximum
    match: str = 'exact'  # exact, minimum, strict
    check: str = 'none'  # none, partial, full
    migratable: str = 'on'  # on, off
    deprecated_features: str = 'on'  # on, off (S390 专用,Since 11.0.0)
    model: str = ''  # CPU 模型名称
    fallback: str = 'allow'  # allow, forbid
    vendor: str = ''  # 厂商名称
    vendor_id: str = ''  # 厂商标识符 (12 字符)
    cache: dict = field(default_factory=dict)
    maxphysaddr: dict = field(default_factory=dict)
    feature: dict = field(default_factory=dict)

    def update(self, data: dict) -> None:
        """更新配置."""
        # 重置 CPU 模型和拓扑相关配置
        self.mode = 'host-model'
        self.match = 'exact'
        self.check = 'none'
        self.migratable = 'on'
        self.deprecated_features = 'on'
        self.model = ''
        self.fallback = 'allow'
        self.vendor = ''
        self.vendor_id = ''
        self.cache = {}
        self.maxphysaddr = {}
        self.feature = {}

        # 处理来自 cpu_allocation_tab 的数据格式
        if 'cpu' in data:
            cpu_data = data['cpu']
            # 处理 CPU 属性
            for key in ['mode', 'match', 'check', 'migratable', 'deprecated_features']:
                if key in cpu_data:
                    setattr(self, key, cpu_data[key])
            # 处理 CPU 子元素
            if 'children' in cpu_data:
                for child in cpu_data['children']:
                    if 'topology' in child:
                        topology_data = child['topology']
                        if isinstance(topology_data, dict):
                            self.topology = CPUTopology.from_dict(topology_data)
                    elif 'model' in child:
                        self.model = child['model']
                        if 'fallback' in child:
                            self.fallback = child['fallback']
                    elif 'vendor' in child:
                        self.vendor = child['vendor']
                        if 'id' in child:
                            self.vendor_id = child['id']
                    elif 'vendor_id' in child:
                        self.vendor_id = child['vendor_id']
                    elif 'cache' in child:
                        self.cache = child['cache']
                    elif 'maxphysaddr' in child:
                        self.maxphysaddr = child['maxphysaddr']
                    elif 'feature' in child:
                        self.feature = child['feature']

        # 处理直接的配置项
        for key in ['max_vcpu', 'current_vcpu', 'placement', 'cpuset']:
            if key in data:
                setattr(self, key, data[key])

        # 处理 CPU 模型和拓扑相关配置
        for key in [
            'mode',
            'match',
            'check',
            'migratable',
            'deprecated_features',
            'model',
            'fallback',
            'vendor',
            'vendor_id',
        ]:
            if key in data:
                setattr(self, key, data[key])
        if 'topology' in data:
            if isinstance(data['topology'], dict):
                self.topology = CPUTopology.from_dict(data['topology'])
            else:
                self.topology = data['topology']
        if 'cache' in data:
            self.cache = data['cache']
        if 'maxphysaddr' in data:
            self.maxphysaddr = data['maxphysaddr']
        if 'feature' in data:
            self.feature = data['feature']
        if 'vcpu_instances' in data:
            self.vcpu_instances = data['vcpu_instances']

    def to_dict(self) -> dict:
        """转换为字典格式."""
        from dataclasses import asdict

        result = asdict(self)
        result['topology'] = self.topology.to_dict()
        # 只返回非空值
        return {k: v for k, v in result.items() if v not in (None, '', [], {})}
