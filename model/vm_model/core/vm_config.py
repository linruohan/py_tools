"""VM 配置管理类 - 基于组合模式和工厂模式."""

from ..configs.basic_config import BasicConfig
from ..configs.cpu_allocation_config import CPUAllocationConfig as CPUConfig
from ..configs.devices_config import DevicesConfig
from ..configs.memory_allocation_config import MemoryAllocationConfig as MemoryConfig
from ..configs.os_booting_config import OSBootingConfig as OSConfig
from ..cpu.topology import CPUTopology


class VMConfig:
    """VM 配置管理类 - 使用组合模式统一管理配置."""

    def __init__(self):
        """初始化 VM 配置."""
        # 创建各子配置
        self.basic = BasicConfig()
        self.cpu = CPUConfig()
        self.memory = MemoryConfig()
        self.os = OSConfig()
        self.devices = DevicesConfig()

        # 其他配置项
        self.hypervisor = 'kvm'
        self.resource_partitioning = {'partition': ''}
        self.fibre_channel_vmid = {'appid': ''}

        # 简化版本,移除策略管理器
        self._sync_context()

    def _sync_context(self) -> None:
        """同步配置上下文."""
        # 简化版本,移除策略管理器
        pass

    def update_from_tab(self, tab_key: str, tab_data: dict) -> None:
        """从 Tab 更新配置.

        Args:
            tab_key: Tab 的键名
            tab_data: Tab 的配置数据
        """
        if not tab_data:
            return

        # 基础配置
        if (
            tab_key == 'general_metadata'
            or tab_key == 'basic_info'
            or 'basic' in tab_data
            or 'name' in tab_data
        ):
            self.basic.update(tab_data)
            self._sync_context()

        # 内存配置
        if tab_key == 'memory_allocation' or 'memory_allocation' in tab_data:
            data = tab_data.get('memory_allocation', tab_data)
            self.memory.update(data)
            if 'current_memory' not in data:
                self.memory.current_memory = None
            if 'max_memory' not in data:
                self.memory.max_memory = None
            if 'dump_core' not in data:
                self.memory.dump_core = None

        # CPU 配置
        if tab_key == 'cpu_allocation' or 'cpu_allocation' in tab_data:
            data = tab_data.get('cpu_allocation', tab_data)
            self.cpu.update(data)

        # CPU 模型和拓扑配置
        if tab_key == 'cpu_model_topology' or 'cpu_model_topology' in tab_data:
            data = tab_data.get('cpu_model_topology', tab_data)
            # 更新 topology
            if 'topology' in data:
                if isinstance(data['topology'], dict):
                    self.cpu.topology = CPUTopology.from_dict(data['topology'])
                else:
                    self.cpu.topology = data['topology']
            # 更新 CPU 模型相关配置
            model_data = data.get('model', {})
            if model_data:
                for key in [
                    'mode',
                    'match',
                    'check',
                    'migratable',
                    'model',
                    'vendor',
                    'vendor_id',
                    'fallback',
                ]:
                    if model_data.get(key):
                        setattr(self.cpu, key, model_data[key])
            # 更新 cache 配置
            if data.get('cache'):
                self.cpu.cache = data['cache']
            # 更新 maxphysaddr 配置
            if data.get('maxphysaddr'):
                self.cpu.maxphysaddr = data['maxphysaddr']
            # 更新 feature 配置
            if data.get('feature'):
                self.cpu.feature = data['feature']

        # OS 引导配置
        if tab_key == 'os_booting' or 'os_booting' in tab_data:
            data = tab_data.get('os_booting', tab_data)
            self.os.update(data)
            self._sync_context()

        # 设备配置
        if tab_key == 'devices' or 'devices' in tab_data:
            data = tab_data.get('devices', tab_data)
            self.devices.update(data)

        # 资源分区配置
        if 'resource_partitioning' in tab_data:
            self.resource_partitioning.update(tab_data['resource_partitioning'])

        # 光纤通道 VMID 配置
        if 'fibre_channel_vmid' in tab_data:
            self.fibre_channel_vmid.update(tab_data['fibre_channel_vmid'])

        # 虚拟机监控程序配置
        if 'hypervisor' in tab_data:
            self.hypervisor = tab_data['hypervisor']

    def to_dict(self) -> dict:
        """将配置转换为字典格式.

        Returns:
            包含所有配置的字典
        """
        config = {}

        # 基础配置
        config.update(self.basic.to_dict())

        # 内存配置
        memory_dict = self.memory.to_dict()
        if memory_dict.get('current_memory') is None:
            del memory_dict['current_memory']
        if memory_dict.get('max_memory') is None:
            del memory_dict['max_memory']
        if memory_dict.get('dump_core') is None:
            del memory_dict['dump_core']
        config['memory_allocation'] = memory_dict

        # CPU 配置
        config['cpu_allocation'] = self.cpu.to_dict()

        # OS 引导配置
        config['os_booting'] = self.os.to_dict()

        # 设备配置
        config['devices'] = self.devices.to_dict()

        # 资源分区配置
        config['resource_partitioning'] = self.resource_partitioning

        # 光纤通道 VMID 配置
        config['fibre_channel_vmid'] = self.fibre_channel_vmid

        # 虚拟机监控程序配置
        config['hypervisor'] = self.hypervisor

        # CPU 模型和拓扑配置 (从 cpu 配置中提取)
        cpu_model_topology = {}
        # 提取 CPU 模型相关配置
        model_config = {}
        for key in [
            'mode',
            'match',
            'check',
            'migratable',
            'model',
            'vendor',
            'vendor_id',
            'fallback',
        ]:
            if hasattr(self.cpu, key) and getattr(self.cpu, key):
                model_config[key] = getattr(self.cpu, key)
        if model_config:
            cpu_model_topology['model'] = model_config
        # 提取 cache 配置
        if hasattr(self.cpu, 'cache') and self.cpu.cache:
            cpu_model_topology['cache'] = self.cpu.cache
        # 提取 maxphysaddr 配置
        if hasattr(self.cpu, 'maxphysaddr') and self.cpu.maxphysaddr:
            cpu_model_topology['maxphysaddr'] = self.cpu.maxphysaddr
        # 提取 feature 配置
        if hasattr(self.cpu, 'feature') and self.cpu.feature:
            cpu_model_topology['feature'] = self.cpu.feature

        if cpu_model_topology:
            config['cpu_model_topology'] = cpu_model_topology

        return config

    def validate(self) -> tuple[bool, str]:
        """验证配置的有效性.

        Returns:
            (是否有效,错误信息)
        """
        errors = []

        # 验证必要的配置
        if not self.basic.name:
            errors.append('虚拟机名称不能为空')

        if hasattr(self.memory, 'memory') and self.memory.memory <= 0:
            errors.append('内存大小必须大于 0')

        if hasattr(self.cpu, 'vcpu') and self.cpu.vcpu <= 0:
            errors.append('CPU 数量必须大于 0')

        # 验证 OS 引导配置
        if hasattr(self.os, 'os_type') and self.os.os_type == 'direct_kernel':
            if not hasattr(self.os, 'kernel') or not self.os.kernel:
                errors.append('直接内核引导模式下必须指定内核路径')

        if errors:
            return False, '; '.join(errors)
        return True, '配置有效'

    def reset(self) -> None:
        """重置配置为默认值."""
        # 重新初始化各配置对象
        self.basic = BasicConfig()
        self.cpu = CPUConfig()
        self.memory = MemoryConfig()
        self.os = OSConfig()
        self.devices = DevicesConfig()

        # 重置其他配置
        self.hypervisor = 'kvm'
        self.resource_partitioning = {'partition': ''}
        self.fibre_channel_vmid = {'appid': ''}

        # 重新同步上下文
        self._sync_context()

    def get_summary(self) -> dict:
        """获取配置摘要.

        Returns:
            配置摘要字典
        """
        return {
            'name': self.basic.name,
            'description': self.basic.description or '',
            'memory': f'{self.memory.memory // 1024}MB'
            if hasattr(self.memory, 'memory')
            else '0MB',
            'vcpu': self.cpu.vcpu if hasattr(self.cpu, 'vcpu') else 0,
            'os_type': self.os.os_type if hasattr(self.os, 'os_type') else 'hvm',
            'arch': self.os.arch if hasattr(self.os, 'arch') else 'x86_64',
            'machine': self.os.machine if hasattr(self.os, 'machine') else 'virt',
        }
