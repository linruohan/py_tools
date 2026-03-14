"""VM 配置管理类 - 基于组合模式和工厂模式."""

from config import (
    ConfigComposite,
    BasicConfig,
    CPUConfig,
    MemoryConfig,
    OSConfig,
    DevicesConfig,
    FeaturesConfig,
    ClockConfig,
    TuningConfig,
    SecurityConfig,
    MemoryBackingConfig,
    PowerManagementConfig,
    EventsConfig,
    IOThreadsConfig,
)
from config.strategies import OptionStrategyManager, DiskBusStrategy


class VMConfig:
    """VM 配置管理类 - 使用组合模式统一管理配置."""

    def __init__(self):
        """初始化 VM 配置."""
        # 配置树根节点
        self.config_tree = ConfigComposite('vm_config')

        # 创建各子配置（使用工厂模式创建）
        self.basic = BasicConfig()
        self.cpu = CPUConfig()
        self.memory = MemoryConfig()
        self.os = OSConfig()
        self.devices = DevicesConfig()
        self.features = FeaturesConfig()
        self.clock = ClockConfig()
        self.tuning = TuningConfig()
        self.security = SecurityConfig()
        self.memory_backing = MemoryBackingConfig()
        self.power_management = PowerManagementConfig()
        self.events = EventsConfig()
        self.iothreads = IOThreadsConfig()

        # 其他配置项
        self.hypervisor = 'kvm'
        self.resource_partitioning = {'partition': ''}
        self.fibre_channel_vmid = {'appid': ''}

        # 策略管理器（单例）
        self.strategy_manager = OptionStrategyManager.get_instance()
        self._init_strategies()

        # 同步上下文（用于策略动态更新）
        self._sync_context()

    def _init_strategies(self) -> None:
        """初始化策略注册."""
        self.strategy_manager.register('disk_bus', DiskBusStrategy())

    def _sync_context(self) -> None:
        """同步配置上下文到策略管理器."""
        self.strategy_manager.update_context(
            machine=self.basic.machine,
            arch=self.basic.get_value('arch') or 'x86_64',
        )

    def update_from_tab(self, tab_key: str, tab_data: dict) -> None:
        """从 Tab 更新配置.

        Args:
            tab_key: Tab 的键名
            tab_data: Tab 的配置数据
        """
        if not tab_data:
            return

        # 基础配置
        if tab_key == 'general_metadata' or 'basic' in tab_data:
            self.basic.update(tab_data)
            self._sync_context()

        # 内存配置
        if tab_key == 'memory_allocation' or 'memory_allocation' in tab_data:
            data = tab_data.get('memory_allocation', tab_data)
            self.memory.update(data)

        # CPU 配置
        if tab_key == 'cpu_allocation' or 'cpu_allocation' in tab_data:
            data = tab_data.get('cpu_allocation', tab_data)
            self.cpu.update(data)

        # OS 引导配置
        if tab_key == 'os_booting' or 'os_booting' in tab_data:
            data = tab_data.get('os_booting', tab_data)
            self.os.update(data)
            self._sync_context()

        # 设备配置
        if tab_key == 'devices' or 'devices' in tab_data:
            data = tab_data.get('devices', tab_data)
            self.devices.update(data)

        # 磁盘设备
        if 'disk_devices' in tab_data:
            self.devices.set_value('disk_devices', tab_data['disk_devices'])

        # 特性配置
        if tab_key == 'hypervisor_features' or 'hypervisor_features' in tab_data:
            data = tab_data.get('hypervisor_features', tab_data)
            self.features.update(data)

        # 时钟配置
        if tab_key == 'time_keeping' or 'time_keeping' in tab_data:
            data = tab_data.get('time_keeping', tab_data)
            self.clock.update(data)

        # 电源管理配置
        if 'power_management' in tab_data:
            self.power_management.update(tab_data['power_management'])

        # 事件配置
        if 'events_configuration' in tab_data:
            self.events.update(tab_data['events_configuration'])

        # 内存后端配置
        if 'memory_backing' in tab_data:
            self.memory_backing.update(tab_data['memory_backing'])

        # 内存调优配置
        if 'memory_tuning' in tab_data:
            tuning = self.tuning.get('memory')
            if tuning:
                for key, value in tab_data['memory_tuning'].items():
                    tuning.set_value(key, value)

        # CPU 调优配置
        if 'cpu_tuning' in tab_data:
            tuning = self.tuning.get('cpu')
            if tuning:
                for key, value in tab_data['cpu_tuning'].items():
                    tuning.set_value(key, value)

        # NUMA 调优配置
        if 'numa_node_tuning' in tab_data:
            tuning = self.tuning.get('numa')
            if tuning:
                for key, value in tab_data['numa_node_tuning'].items():
                    tuning.set_value(key, value)

        # 块 IO 调优配置
        if 'block_io_tuning' in tab_data:
            tuning = self.tuning.get('blkio')
            if tuning:
                for key, value in tab_data['block_io_tuning'].items():
                    tuning.set_value(key, value)

        # IO 线程配置
        if 'iothreads_allocation' in tab_data:
            self.iothreads.update(tab_data['iothreads_allocation'])

        # 资源分区配置
        if 'resource_partitioning' in tab_data:
            self.resource_partitioning.update(tab_data['resource_partitioning'])

        # 光纤通道 VMID 配置
        if 'fibre_channel_vmid' in tab_data:
            self.fibre_channel_vmid.update(tab_data['fibre_channel_vmid'])

        # 安全标签配置
        if 'security_label' in tab_data:
            self.security.update(tab_data['security_label'])

        # 密钥包装配置
        if 'key_wrap' in tab_data:
            self.security.update(tab_data['key_wrap'])

        # 启动安全配置
        if 'launch_security' in tab_data:
            self.security.update(tab_data['launch_security'])

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
        config['memory_allocation'] = self.memory.to_dict()

        # CPU 配置
        config['cpu_allocation'] = self.cpu.to_dict()
        config['cpu_model_topology'] = {
            'model': self.cpu.model,
            'feature': self.cpu.get_value('features') or [],
            'cache': self.cpu.get('cache').to_dict() if self.cpu.get('cache') else {},
        }

        # OS 引导配置
        config['os_booting'] = self.os.to_dict()

        # 设备配置
        config['devices'] = self.devices.to_dict()
        config['disk_devices'] = self.devices.get_value('disk_devices') or []

        # 特性配置
        config['hypervisor_features'] = self.features.to_dict()

        # 时钟配置
        config['time_keeping'] = self.clock.to_dict()

        # 电源管理配置
        config['power_management'] = self.power_management.to_dict()

        # 事件配置
        config['events_configuration'] = self.events.to_dict()

        # 内存后端配置
        config['memory_backing'] = self.memory_backing.to_dict()

        # 内存调优配置
        config['memory_tuning'] = (
            self.tuning.get('memory').to_dict() if self.tuning.get('memory') else {}
        )

        # CPU 调优配置
        config['cpu_tuning'] = self.tuning.get('cpu').to_dict() if self.tuning.get('cpu') else {}

        # NUMA 调优配置
        config['numa_node_tuning'] = (
            self.tuning.get('numa').to_dict() if self.tuning.get('numa') else {}
        )

        # 块 IO 调优配置
        config['block_io_tuning'] = (
            self.tuning.get('blkio').to_dict() if self.tuning.get('blkio') else {}
        )

        # IO 线程配置
        config['iothreads_allocation'] = self.iothreads.to_dict()

        # 资源分区配置
        config['resource_partitioning'] = self.resource_partitioning

        # 光纤通道 VMID 配置
        config['fibre_channel_vmid'] = self.fibre_channel_vmid

        # 安全配置（包含 seclabel, keywrap, launch_security）
        config['security_label'] = self.security.seclabel
        config['key_wrap'] = self.security.keywrap
        config['launch_security'] = self.security.launch_security

        # 虚拟机监控程序配置
        config['hypervisor'] = self.hypervisor

        return config

    def validate(self) -> tuple[bool, str]:
        """验证配置的有效性.

        Returns:
            (是否有效，错误信息)
        """
        errors = []

        # 验证必要的配置
        if not self.basic.vm_name:
            errors.append('虚拟机名称不能为空')

        if self.memory.memory <= 0:
            errors.append('内存大小必须大于 0')

        if self.cpu.max_vcpu <= 0:
            errors.append('CPU 数量必须大于 0')

        # 验证 OS 引导配置
        if self.os.os_type == 'direct_kernel':
            if not self.os.get_value('kernel'):
                errors.append('直接内核引导模式下必须指定内核路径')

        # 验证设备配置
        gfx_type = self.devices.get_value('graphics.type') or 'vnc'
        if gfx_type != 'none':
            if not self.devices.get_value('graphics.listen'):
                errors.append('图形设备必须指定监听地址')

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
        self.features = FeaturesConfig()
        self.clock = ClockConfig()
        self.tuning = TuningConfig()
        self.security = SecurityConfig()
        self.memory_backing = MemoryBackingConfig()
        self.power_management = PowerManagementConfig()
        self.events = EventsConfig()
        self.iothreads = IOThreadsConfig()

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
            'name': self.basic.vm_name,
            'description': self.basic.get_value('description') or '',
            'memory': f'{self.memory.memory // 1024}MB',
            'vcpu': self.cpu.max_vcpu,
            'os_type': self.os.os_type,
            'arch': self.os.get_value('arch') or 'x86_64',
            'machine': self.os.machine,
            'graphics': self.devices.get_value('graphics.type') or 'vnc',
        }
