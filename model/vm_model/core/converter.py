"""Domain 与 Config 转换器 - 连接两层配置系统."""

from typing import Any

from .domain import (
    Domain,
)


class DomainConfigConverter:
    """Domain 与 Config 配置字典之间的转换器."""

    @staticmethod
    def to_config(domain: Domain) -> dict[str, Any]:
        """将 Domain 转换为 Config 配置字典.

        Args:
            domain: Domain 实例

        Returns:
            Config 配置字典
        """
        config = {
            'name': domain.name,
            'uuid': domain.uuid,
            'title': domain.title,
            'description': domain.description,
            'hypervisor': domain.type.value if domain.type else 'kvm',
        }

        # CPU 配置
        if domain.vcpu:
            config['cpu_allocation'] = {
                'max_vcpu': domain.vcpu.count,
                'current_vcpu': domain.vcpu.current or domain.vcpu.count,
                'placement': domain.vcpu.placement,
                'cpuset': domain.vcpu.cpuset,
            }

        if domain.cpu:
            cpu_dict = (
                domain.cpu.to_dict()
                if hasattr(domain.cpu, 'to_dict')
                else {
                    'mode': domain.cpu.mode.value if domain.cpu.mode else 'host-model',
                    'model': {'name': domain.cpu.model.name} if domain.cpu.model else None,
                    'topology': domain.cpu.topology.to_dict() if domain.cpu.topology else None,
                    'features': [f.to_dict() for f in domain.cpu.features]
                    if domain.cpu.features
                    else [],
                }
            )
            config['cpu_model_topology'] = {
                'model': cpu_dict.get('model'),
                'feature': cpu_dict.get('features', []),
                'cache': cpu_dict.get('cache', {}),
            }

        # 内存配置
        if domain.memory:
            mem_dict = (
                domain.memory.to_dict()
                if hasattr(domain.memory, 'to_dict')
                else {
                    'size': domain.memory.size,
                    'unit': domain.memory.unit.value if domain.memory.unit else 'KiB',
                }
            )
            config['memory_allocation'] = {
                'memory': domain.memory.size,
                'unit': mem_dict.get('unit', 'KiB'),
                'current_memory': domain.current_memory.size
                if domain.current_memory
                else domain.memory.size,
                'max_memory': domain.max_memory.size if domain.max_memory else domain.memory.size,
                'memory_slots': domain.max_memory.slots if domain.max_memory else None,
            }

        # OS 配置
        if domain.os:
            os_dict = (
                domain.os.to_dict()
                if hasattr(domain.os, 'to_dict')
                else {
                    'type': domain.os.type.value if domain.os.type else 'hvm',
                    'arch': domain.os.arch,
                    'machine': domain.os.machine.value if domain.os.machine else 'q35',
                    'firmware': domain.os.firmware.value if domain.os.firmware else 'bios',
                    'boot': [b.to_dict() for b in domain.os.boot] if domain.os.boot else [],
                    'bootmenu': domain.os.bootmenu.to_dict() if domain.os.bootmenu else None,
                    'kernel': domain.os.kernel,
                    'initrd': domain.os.initrd,
                    'cmdline': domain.os.cmdline,
                }
            )
            config['os_booting'] = os_dict

        # 设备配置
        if domain.devices:
            devices_dict = (
                domain.devices.to_dict()
                if hasattr(domain.devices, 'to_dict')
                else {
                    'emulator': domain.devices.emulator,
                    'disks': [d.to_dict() for d in domain.devices.disks]
                    if domain.devices.disks
                    else [],
                    'graphics': [g.to_dict() for g in domain.devices.graphics]
                    if domain.devices.graphics
                    else [],
                    'videos': [v.to_dict() for v in domain.devices.videos]
                    if domain.devices.videos
                    else [],
                    'interfaces': [i.to_dict() for i in domain.devices.interfaces]
                    if domain.devices.interfaces
                    else [],
                }
            )
            config['devices'] = devices_dict
            config['disk_devices'] = devices_dict.get('disks', [])

        # 特性配置
        if domain.features:
            features_dict = (
                domain.features.to_dict()
                if hasattr(domain.features, 'to_dict')
                else {
                    'general': {
                        'acpi': domain.features.acpi,
                        'apic': domain.features.apic,
                        'pae': domain.features.pae,
                    },
                    'hyperv': domain.features.hyperv,
                    'kvm': domain.features.kvm,
                }
            )
            config['hypervisor_features'] = features_dict

        # 时钟配置
        if domain.clock:
            clock_dict = (
                domain.clock.to_dict()
                if hasattr(domain.clock, 'to_dict')
                else {
                    'offset': domain.clock.offset,
                    'timezone': domain.clock.timezone,
                    'timers': domain.clock.timers,
                }
            )
            config['time_keeping'] = clock_dict

        # 事件配置
        config['events_configuration'] = {
            'on_poweroff': domain.on_poweroff or 'destroy',
            'on_reboot': domain.on_reboot or 'restart',
            'on_crash': domain.on_crash or 'destroy',
        }

        return config

    @staticmethod
    def from_config(config: dict[str, Any]) -> Domain:
        """从 Config 配置字典创建 Domain.

        Args:
            config: Config 配置字典

        Returns:
            Domain 实例
        """
        return Domain.from_config(config)

    @staticmethod
    def to_xml(domain: Domain) -> str:
        """将 Domain 转换为 XML 字符串.

        Args:
            domain: Domain 实例

        Returns:
            XML 字符串
        """
        return domain.to_xml()

    @staticmethod
    def convert_vmconfig_to_domain(vmconfig_dict: dict[str, Any]) -> Domain:
        """从 VMConfig 的 to_dict() 输出转换为 Domain.

        Args:
            vmconfig_dict: VMConfig.to_dict() 的输出

        Returns:
            Domain 实例
        """
        return Domain.from_config(vmconfig_dict)

    @staticmethod
    def convert_domain_to_vmconfig(domain: Domain) -> dict[str, Any]:
        """将 Domain 转换为 VMConfig 兼容的字典格式.

        Args:
            domain: Domain 实例

        Returns:
            VMConfig 兼容的字典
        """
        return DomainConfigConverter.to_config(domain)
