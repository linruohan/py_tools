"""VM 配置管理类 - 基于组合模式和工厂模式."""

from __future__ import annotations

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
        self.iothreads_allocation = {}  # IO 线程分配配置
        self.cpu_tuning = {}  # CPU 调优配置
        self.sysinfo = {}  # SMBIOS/FwCfg 系统信息配置

        # 简化版本，移除策略管理器
        self._sync_context()

    def _sync_context(self) -> None:
        """同步配置上下文."""
        # 简化版本，移除策略管理器
        pass

    def _resolve_tab_data(self, tab_key: str, data_key: str, tab_data: dict) -> dict | None:
        """从 tab_data 中提取指定键的数据，支持 tab_key 直接匹配和 data_key 嵌套两种格式.

        Args:
            tab_key: Tab 的键名
            data_key: tab_data 中的数据键名
            tab_data: Tab 的配置数据

        Returns:
            提取到的数据字典，或 None
        """
        if tab_key == data_key and data_key not in tab_data:
            return tab_data
        return tab_data.get(data_key)

    def _update_basic(self, tab_data: dict) -> None:
        self.basic.update(tab_data)
        self._sync_context()

    def _update_memory(self, tab_data: dict) -> None:
        data = tab_data.get('memory_allocation', tab_data)
        self.memory.update(data)
        for field in ('current_memory', 'max_memory', 'dump_core'):
            if field not in data:
                setattr(self.memory, field, None)

    def _update_cpu(self, tab_data: dict) -> None:
        self.cpu.update(tab_data.get('cpu_allocation', tab_data))

    def _update_cpu_model_topology(self, tab_data: dict) -> None:
        data = tab_data.get('cpu_model_topology', tab_data)
        if 'topology' in data:
            topo = data['topology']
            self.cpu.topology = CPUTopology.from_dict(topo) if isinstance(topo, dict) else topo
        for key in ('mode', 'match', 'check', 'migratable', 'deprecated_features'):
            if key in data:
                setattr(self.cpu, key, data[key])
        model_data = data.get('model', {})
        for attr in ('name', 'fallback', 'vendor', 'vendor_id'):
            if attr in model_data:
                setattr(self.cpu, 'model' if attr == 'name' else attr, model_data[attr])
        for attr in ('cache', 'maxphysaddr', 'feature'):
            if data.get(attr):
                setattr(self.cpu, attr, data[attr])

    def _update_os(self, tab_data: dict) -> None:
        self.os.update(tab_data.get('os_booting', tab_data))
        self._sync_context()

    def _update_devices(self, tab_data: dict) -> None:
        self.devices.update(tab_data.get('devices', tab_data))

    def _update_key_wrap(self, tab_data: dict) -> None:
        kw = tab_data.get('key_wrap', tab_data)
        if not isinstance(kw, dict):
            return
        if 'cipher' in kw:
            for cipher in kw['cipher']:
                if isinstance(cipher, dict):
                    name, state = cipher.get('name', ''), cipher.get('state', 'off')
                    if name == 'aes':
                        self.key_wrap.aes_state = state
                    elif name == 'dea':
                        self.key_wrap.dea_state = state
        elif 'aes_state' in kw:
            self.key_wrap.aes_state = kw.get('aes_state', 'off')
            self.key_wrap.dea_state = kw.get('dea_state', 'off')

    def _update_throttlegroups(self, tab_data: dict) -> None:
        throttle_data = tab_data.get('disk_throttle_group', tab_data)
        if not isinstance(throttle_data, dict):
            return
        self.throttlegroups.throttlegroups = [
            ThrottleGroup(
                name=g.get('name', ''),
                total_bytes_sec=g.get('total_bytes_sec'),
                read_bytes_sec=g.get('read_bytes_sec'),
                write_bytes_sec=g.get('write_bytes_sec'),
                total_iops_sec=g.get('total_iops_sec'),
                read_iops_sec=g.get('read_iops_sec'),
                write_iops_sec=g.get('write_iops_sec'),
            )
            for g in throttle_data.get('throttle_groups', [])
            if isinstance(g, dict)
        ]

    def _update_sysinfo(self, tab_data: dict) -> None:
        sysinfo_data = tab_data.get('sysinfo', tab_data)
        if isinstance(sysinfo_data, dict):
            self.sysinfo = sysinfo_data
        if 'smbios_mode' in tab_data:
            self.os.smbios.mode = tab_data['smbios_mode']

    def update_from_tab(self, tab_key: str, tab_data: dict) -> None:
        """从 Tab 更新配置.

        使用分发表替代 if-elif 链，每个 tab_key 对应一个处理方法。

        Args:
            tab_key: Tab 的键名
            tab_data: Tab 的配置数据
        """
        if not tab_data:
            return

        # ── 直接键名匹配的分发表 ──────────────────────────────────────────────
        _direct: dict = {
            'general_metadata': self._update_basic,
            'basic_info': self._update_basic,
            'memory_allocation': self._update_memory,
            'cpu_allocation': self._update_cpu,
            'cpu_model_topology': self._update_cpu_model_topology,
            'os_booting': self._update_os,
            'devices': self._update_devices,
            'key_wrap': self._update_key_wrap,
            'disk_throttle_group': self._update_throttlegroups,
            'memory_tuning': lambda d: self.memory_tuning.update(d),
            'memory_backing': lambda d: self.memory_backing.update(d),
            'numa_node_tuning': lambda d: setattr(self, 'numa_tuning', NumaTuneConfig.from_dict(d)),
            'iothreads_allocation': lambda d: setattr(self, 'iothreads_allocation', d),
            'cpu_tuning': lambda d: setattr(self, 'cpu_tuning', d),
            'block_io_tuning': lambda d: self.block_io_tuning.update(d),
            'time_keeping': lambda d: setattr(self, 'time_keeping', d),
            'hypervisor_features': lambda d: setattr(self, 'hypervisor_features', d),
            'smbios_system': self._update_sysinfo,
        }

        if tab_key in _direct:
            _direct[tab_key](tab_data)

        # ── 通过 tab_data 键名匹配的补充更新 ─────────────────────────────────
        # 处理 tab_data 中直接包含配置键的情况（如 {'name': 'vm0', ...}）
        if 'basic' in tab_data or 'name' in tab_data:
            if tab_key not in ('general_metadata', 'basic_info'):
                self._update_basic(tab_data)

        _data_key_map: dict = {
            'memory_allocation': self._update_memory,
            'cpu_allocation': self._update_cpu,
            'cpu_model_topology': self._update_cpu_model_topology,
            'os_booting': self._update_os,
            'devices': self._update_devices,
            'resource_partitioning': lambda d: self.resource_partitioning.update(d),
            'fibre_channel_vmid': lambda d: self.fibre_channel_vmid.update(d),
            'hypervisor': lambda d: setattr(self, 'hypervisor', d),
            'launch_security': lambda d: setattr(
                self, 'launch_security', LaunchSecurityConfig.from_dict(d)
            ),
            'key_wrap': self._update_key_wrap,
            'power_management': lambda d: setattr(self, 'power_management', d),
            'events_configuration': lambda d: setattr(self, 'events_configuration', d),
            'security_label': lambda d: setattr(self, 'security_label', d),
            'seclabel': lambda d: setattr(self, 'security_label', d),
            'performance_monitoring': lambda d: setattr(self, 'performance_monitoring', d),
            'time_keeping': lambda d: setattr(self, 'time_keeping', d),
            'hypervisor_features': lambda d: setattr(self, 'hypervisor_features', d),
            'block_io_tuning': lambda d: self.block_io_tuning.update(d),
            'disk_throttle_group': self._update_throttlegroups,
            'memory_tuning': lambda d: self.memory_tuning.update(d),
            'memory_backing': lambda d: self.memory_backing.update(d),
            'numa_node_tuning': lambda d: setattr(self, 'numa_tuning', NumaTuneConfig.from_dict(d)),
            'iothreads_allocation': lambda d: setattr(self, 'iothreads_allocation', d),
            'cpu_tuning': lambda d: setattr(self, 'cpu_tuning', d),
            'sysinfo': self._update_sysinfo,
        }

        for key, handler in _data_key_map.items():
            if key in tab_data and tab_key != key:
                value = tab_data[key]
                handler(
                    value
                    if not callable(getattr(value, 'items', None))
                    or key not in ('resource_partitioning', 'fibre_channel_vmid')
                    else {key: value}
                )

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

        # IO 线程分配配置
        if self.iothreads_allocation:
            config['iothreads_allocation'] = self.iothreads_allocation

        # CPU 调优配置
        if self.cpu_tuning:
            config['cpu_tuning'] = self.cpu_tuning

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

        # SMBIOS/FwCfg 系统信息配置
        if self.sysinfo:
            config['sysinfo'] = self.sysinfo

        return config

    def validate(self) -> tuple[bool, list[str]]:
        """验证配置的有效性.

        Returns:
            (是否有效，错误信息列表)
        """
        errors = []
        warnings = []

        # 必填项验证
        if not self.basic.name:
            errors.append('虚拟机名称不能为空')
        elif not self.basic.name.replace('_', '').replace('-', '').isalnum():
            errors.append('虚拟机名称只能包含字母、数字、下划线和连字符')

        # 数值范围验证
        if hasattr(self.memory, 'memory') and self.memory.memory <= 0:
            errors.append('内存大小必须大于 0')
        elif hasattr(self.memory, 'memory') and 0 < self.memory.memory < 512:
            warnings.append('警告：内存大小建议不小于 512MB')

        if hasattr(self.cpu, 'vcpu') and self.cpu.vcpu <= 0:
            errors.append('CPU 数量必须大于 0')
        elif hasattr(self.cpu, 'vcpu') and self.cpu.vcpu > 256:
            warnings.append('警告：CPU 数量不建议超过 256')

        # 逻辑验证
        if hasattr(self.memory, 'current_memory') and self.memory.current_memory is not None:
            if hasattr(self.memory, 'memory') and self.memory.memory > 0:
                if self.memory.current_memory > self.memory.memory:
                    errors.append('当前内存不能大于最大内存')

        # CPU 拓扑验证
        if hasattr(self.cpu, 'topology') and self.cpu.topology:
            topo = self.cpu.topology
            total = topo.sockets * topo.cores * topo.threads
            if hasattr(self.cpu, 'vcpu') and self.cpu.vcpu > 0 and total != self.cpu.vcpu:
                errors.append(
                    f'CPU 拓扑不匹配：{topo.sockets}×{topo.cores}×{topo.threads} '
                    f'!= {self.cpu.vcpu}'
                )

        # OS 引导配置验证
        if hasattr(self.os, 'os_type') and self.os.os_type == 'direct_kernel':
            if not hasattr(self.os, 'kernel') or not self.os.kernel:
                errors.append('直接内核引导模式下必须指定内核路径')

        # 只返回错误，不返回警告（警告仅用于提示）
        return len(errors) == 0, errors

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
        self.iothreads_allocation = {}  # IO 线程分配配置
        self.cpu_tuning = {}  # CPU 调优配置
        self.sysinfo = {}  # SMBIOS/FwCfg 系统信息配置

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
