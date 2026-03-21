"""VM 配置管理类 - 基于组合模式和工厂模式."""

from ..configs.basic_config import BasicConfig
from ..configs.block_io_config import BlockIOConfig
from ..configs.cpu_allocation_config import CPUAllocationConfig as CPUConfig
from ..configs.devices_config import DevicesConfig
from ..configs.key_wrap_config import KeyWrapConfig
from ..configs.launch_security_config import LaunchSecurityConfig
from ..configs.memory_allocation_config import MemoryAllocationConfig as MemoryConfig
from ..configs.memory_backing_config import MemoryBackingConfig
from ..configs.memory_tuning_config import MemoryTuningConfig
from ..configs.numa_tuning_config import NumaTuneConfig
from ..configs.os_booting_config import OSBootingConfig as OSConfig
from ..configs.throttlegroups import ThrottleGroup, ThrottleGroups
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
        self.launch_security = LaunchSecurityConfig()
        self.key_wrap = KeyWrapConfig()
        self.power_management = {}  # 电源管理配置
        self.events_configuration = {}  # 事件配置
        self.security_label = {}  # 安全标签配置
        self.performance_monitoring = {'enabled': False, 'events': {}}  # 性能监控配置
        self.hypervisor_features = {}  # 虚拟化特性配置
        self.time_keeping = {}  # 时间管理配置
        self.block_io_tuning = BlockIOConfig()  # 块 IO 优化配置
        self.throttlegroups = ThrottleGroups()  # 节流组配置
        self.memory_tuning = MemoryTuningConfig()  # 内存调优配置
        self.memory_backing = MemoryBackingConfig()  # 内存后端配置
        self.numa_tuning = NumaTuneConfig()  # NUMA 节点调优配置

        # 简化版本，移除策略管理器
        self._sync_context()

    def _sync_context(self) -> None:
        """同步配置上下文."""
        # 简化版本，移除策略管理器
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
            # 更新 CPU 模型相关配置 (mode, match, check, migratable 在 data 顶层)
            for key in ['mode', 'match', 'check', 'migratable', 'deprecated_features']:
                if key in data:
                    setattr(self.cpu, key, data[key])
            # 更新 model 字典中的配置 (name, fallback, vendor, vendor_id)
            model_data = data.get('model', {})
            if model_data:
                if 'name' in model_data:
                    self.cpu.model = model_data['name']
                if 'fallback' in model_data:
                    self.cpu.fallback = model_data['fallback']
                if 'vendor' in model_data:
                    self.cpu.vendor = model_data['vendor']
                if 'vendor_id' in model_data:
                    self.cpu.vendor_id = model_data['vendor_id']
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

        # 启动安全配置
        if 'launch_security' in tab_data:
            self.launch_security = LaunchSecurityConfig.from_dict(tab_data['launch_security'])

        # 密钥包装配置
        if tab_key == 'key_wrap' or 'key_wrap' in tab_data:
            key_wrap_data = tab_data.get('key_wrap', tab_data)
            if isinstance(key_wrap_data, dict):
                # 支持 cipher 列表格式
                if 'cipher' in key_wrap_data:
                    cipher_list = key_wrap_data['cipher']
                    if isinstance(cipher_list, list):
                        for cipher in cipher_list:
                            if isinstance(cipher, dict):
                                name = cipher.get('name', '')
                                state = cipher.get('state', 'off')
                                if name == 'aes':
                                    self.key_wrap.aes_state = state
                                elif name == 'dea':
                                    self.key_wrap.dea_state = state
                # 支持直接格式（来自 KeyWrapTab.get_config()）
                elif 'aes_state' in key_wrap_data:
                    self.key_wrap.aes_state = key_wrap_data.get('aes_state', 'off')
                    self.key_wrap.dea_state = key_wrap_data.get('dea_state', 'off')

        # 电源管理配置
        if 'power_management' in tab_data:
            self.power_management = tab_data['power_management']

        # 事件配置
        if 'events_configuration' in tab_data:
            self.events_configuration = tab_data['events_configuration']

        # 安全标签配置（支持 security_label 和 seclabel 两种键名）
        if 'security_label' in tab_data:
            self.security_label = tab_data['security_label']
        elif 'seclabel' in tab_data:
            self.security_label = tab_data['seclabel']

        # 性能监控配置
        if 'performance_monitoring' in tab_data:
            self.performance_monitoring = tab_data['performance_monitoring']

        # 时间管理配置（支持 tab_key 和 tab_data 两种格式）
        if tab_key == 'time_keeping' and 'time_keeping' not in tab_data:
            # tab_key 指定且 tab_data 中没有 time_keeping 键，直接使用 tab_data
            self.time_keeping = tab_data
        elif 'time_keeping' in tab_data:
            # tab_data 中 time_keeping 键，使用其值
            self.time_keeping = tab_data['time_keeping']

        # 虚拟化特性配置（支持 tab_key 和 tab_data 两种格式）
        if tab_key == 'hypervisor_features' and 'hypervisor_features' not in tab_data:
            # tab_key 指定且 tab_data 中没有 hypervisor_features 键，直接使用 tab_data
            self.hypervisor_features = tab_data
        elif 'hypervisor_features' in tab_data:
            # tab_data 中有 hypervisor_features 键，使用其值
            self.hypervisor_features = tab_data['hypervisor_features']

        # 块 IO 优化配置（支持 tab_key 和 tab_data 两种格式）
        if tab_key == 'block_io_tuning' and 'block_io_tuning' not in tab_data:
            # tab_key 指定且 tab_data 中没有 block_io_tuning 键，直接使用 tab_data
            block_io_data = tab_data
        elif 'block_io_tuning' in tab_data:
            # tab_data 中有 block_io_tuning 键，使用其值
            block_io_data = tab_data['block_io_tuning']
        else:
            block_io_data = None

        if block_io_data and isinstance(block_io_data, dict):
            self.block_io_tuning.update(block_io_data)

        # 节流组配置（支持 tab_key 和 tab_data 两种格式）
        if tab_key == 'disk_throttle_group' and 'disk_throttle_group' not in tab_data:
            # tab_key 指定且 tab_data 中没有 disk_throttle_group 键，直接使用 tab_data
            throttle_data = tab_data
        elif 'disk_throttle_group' in tab_data:
            # tab_data 中有 disk_throttle_group 键，使用其值
            throttle_data = tab_data['disk_throttle_group']
        else:
            throttle_data = None

        if throttle_data and isinstance(throttle_data, dict):
            groups_data = throttle_data.get('throttle_groups', [])
            # 清空现有节流组
            self.throttlegroups.throttlegroups = []
            # 添加新的节流组
            for group_data in groups_data:
                if isinstance(group_data, dict):
                    throttle_group = ThrottleGroup(
                        name=group_data.get('name', ''),
                        total_bytes_sec=group_data.get('total_bytes_sec'),
                        read_bytes_sec=group_data.get('read_bytes_sec'),
                        write_bytes_sec=group_data.get('write_bytes_sec'),
                        total_iops_sec=group_data.get('total_iops_sec'),
                        read_iops_sec=group_data.get('read_iops_sec'),
                        write_iops_sec=group_data.get('write_iops_sec'),
                    )
                    self.throttlegroups.throttlegroups.append(throttle_group)

        # 内存调优配置（支持 tab_key 和 tab_data 两种格式）
        if tab_key == 'memory_tuning' and 'memory_tuning' not in tab_data:
            # tab_key 指定且 tab_data 中没有 memory_tuning 键，直接使用 tab_data
            memory_tuning_data = tab_data
        elif 'memory_tuning' in tab_data:
            # tab_data 中有 memory_tuning 键，使用其值
            memory_tuning_data = tab_data['memory_tuning']
        else:
            memory_tuning_data = None

        if memory_tuning_data and isinstance(memory_tuning_data, dict):
            self.memory_tuning.update(memory_tuning_data)

        # 内存后端配置（支持 tab_key 和 tab_data 两种格式）
        if tab_key == 'memory_backing' and 'memory_backing' not in tab_data:
            # tab_key 指定且 tab_data 中没有 memory_backing 键，直接使用 tab_data
            memory_backing_data = tab_data
        elif 'memory_backing' in tab_data:
            # tab_data 中有 memory_backing 键，使用其值
            memory_backing_data = tab_data['memory_backing']
        else:
            memory_backing_data = None

        if memory_backing_data and isinstance(memory_backing_data, dict):
            self.memory_backing.update(memory_backing_data)

        # NUMA 调优配置（支持 tab_key 和 tab_data 两种格式）
        if tab_key == 'numa_node_tuning' and 'numa_node_tuning' not in tab_data:
            # tab_key 指定且 tab_data 中没有 numa_node_tuning 键，直接使用 tab_data
            numa_tuning_data = tab_data
        elif 'numa_node_tuning' in tab_data:
            # tab_data 中有 numa_node_tuning 键，使用其值
            numa_tuning_data = tab_data['numa_node_tuning']
        else:
            numa_tuning_data = None

        if numa_tuning_data and isinstance(numa_tuning_data, dict):
            self.numa_tuning = NumaTuneConfig.from_dict(numa_tuning_data)

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

        # 启动安全配置
        if self.launch_security and self.launch_security.is_enabled():
            config['launch_security'] = self.launch_security.to_dict()

        # 密钥包装配置
        if self.key_wrap.has_cipher_config():
            config['key_wrap'] = self.key_wrap.to_dict()

        # 电源管理配置
        if self.power_management:
            config['power_management'] = self.power_management

        # 事件配置
        if self.events_configuration:
            config['events_configuration'] = self.events_configuration

        # 安全标签配置
        if self.security_label:
            sec_type = self.security_label.get('type')
            # none 类型：只生成 type='none'
            if sec_type == 'none':
                config['security_label'] = {'type': 'none'}
            elif sec_type and sec_type not in ('none', 'None'):
                # 构建 security_label 字典，只包含有值的字段
                sec_config = {}
                sec_config['type'] = sec_type

                model = self.security_label.get('model')
                if model:
                    sec_config['model'] = model

                relabel = self.security_label.get('relabel')
                if relabel is not None:
                    sec_config['relabel'] = relabel

                # dynamic 类型的 baselabel
                if sec_type == 'dynamic':
                    # 支持 baselabel（复选框）和 baselabel_value（值）两种格式
                    # 也支持直接使用 baselabel 存储值
                    baselabel_check = self.security_label.get('baselabel')
                    baselabel_value = self.security_label.get('baselabel_value')

                    # 如果 baselabel 是字符串（值），直接使用
                    if isinstance(baselabel_check, str) and baselabel_check:
                        sec_config['baselabel'] = baselabel_check
                    # 否则使用 baselabel 复选框 + baselabel_value 的组合
                    elif baselabel_check and baselabel_value:
                        sec_config['baselabel'] = baselabel_value

                # static 类型的 label
                if sec_type == 'static':
                    label = self.security_label.get('label')
                    if label:
                        sec_config['label'] = label

                config['security_label'] = sec_config

        # 性能监控配置
        if self.performance_monitoring and self.performance_monitoring.get('enabled'):
            config['performance_monitoring'] = self.performance_monitoring

        # 虚拟化特性配置
        if self.hypervisor_features:
            config['hypervisor_features'] = self.hypervisor_features

        # 时间管理配置
        if self.time_keeping:
            config['time_keeping'] = self.time_keeping

        # 块 IO 优化配置
        if not self.block_io_tuning.is_empty():
            config['block_io_tuning'] = self.block_io_tuning.to_dict()

        # 节流组配置
        if self.throttlegroups and self.throttlegroups.throttlegroups:
            config['throttlegroups'] = {
                'throttlegroups': [
                    {
                        'name': group.name,
                        'total_bytes_sec': group.total_bytes_sec,
                        'read_bytes_sec': group.read_bytes_sec,
                        'write_bytes_sec': group.write_bytes_sec,
                        'total_iops_sec': group.total_iops_sec,
                        'read_iops_sec': group.read_iops_sec,
                        'write_iops_sec': group.write_iops_sec,
                    }
                    for group in self.throttlegroups.throttlegroups
                ]
            }

        # 内存调优配置
        if not self.memory_tuning.is_empty():
            config['memory_tuning'] = self.memory_tuning.to_dict()

        # 内存后端配置
        if not self.memory_backing.is_empty():
            config['memory_backing'] = self.memory_backing.to_dict()

        # NUMA 节点调优配置
        if not self.numa_tuning.is_empty():
            config['numa_node_tuning'] = self.numa_tuning.to_dict()

        # CPU 模型和拓扑配置 (从 cpu 配置中提取)
        cpu_model_topology = {}

        # 提取 CPU 模型属性 (放在顶层)
        for key in ['mode', 'match', 'check', 'migratable', 'deprecated_features']:
            if hasattr(self.cpu, key):
                value = getattr(self.cpu, key)
                if value:
                    cpu_model_topology[key] = value

        # 提取 model 字典 (包含 name, fallback, vendor, vendor_id)
        model_dict = {}
        if hasattr(self.cpu, 'model') and self.cpu.model:
            model_dict['name'] = self.cpu.model
            # fallback 只有在有 model name 时才有意义
            if hasattr(self.cpu, 'fallback') and self.cpu.fallback:
                model_dict['fallback'] = self.cpu.fallback
        # vendor 和 vendor_id 可以独立于 model name
        if hasattr(self.cpu, 'vendor') and self.cpu.vendor:
            model_dict['vendor'] = self.cpu.vendor
        if hasattr(self.cpu, 'vendor_id') and self.cpu.vendor_id:
            model_dict['vendor_id'] = self.cpu.vendor_id

        if model_dict:
            cpu_model_topology['model'] = model_dict

        # 提取 topology (从 self.cpu.topology 对象转换)
        if hasattr(self.cpu, 'topology') and self.cpu.topology:
            topology_dict = self.cpu.topology.to_dict()
            if topology_dict:
                cpu_model_topology['topology'] = topology_dict

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
            (是否有效，错误信息)
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
        self.launch_security = LaunchSecurityConfig()
        self.key_wrap = KeyWrapConfig()
        self.power_management = {}  # 电源管理配置
        self.events_configuration = {}  # 事件配置
        self.security_label = {}  # 安全标签配置
        self.performance_monitoring = {'enabled': False, 'events': {}}  # 性能监控配置
        self.hypervisor_features = {}  # 虚拟化特性配置
        self.time_keeping = {}  # 时间管理配置
        self.block_io_tuning = BlockIOConfig()  # 块 IO 优化配置
        self.throttlegroups = ThrottleGroups()  # 节流组配置
        self.memory_tuning = MemoryTuningConfig()  # 内存调优配置
        self.memory_backing = MemoryBackingConfig()  # 内存后端配置
        self.numa_tuning = NumaTuneConfig()  # NUMA 节点调优配置

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
