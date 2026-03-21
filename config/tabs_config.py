"""Tab 配置文件."""

# Tab 配置 - 统一的配置
TABS_CONFIG: dict = {
    # 基础 Tab (默认启用)
    'general_metadata': {
        'name': '通用元数据',
        'class': 'BasicTab',
        'default_on': True,
    },  # cpu分配+内存分配
    'os_booting': {'name': '系统启动', 'class': 'OSTab', 'default_on': True},
    'devices': {'name': 'Devices', 'class': 'DevicesTab', 'default_on': True},
    # 高级调优 Tab (默认禁用)
    'smbios_system': {
        'name': 'SMBIOS系统信息',
        'class': 'SMBIOSSystemTab',
        'default_on': False,
    },
    'iothreads_allocation': {
        'name': 'IOThreads分配',
        'class': 'IOThreadsAllocationTab',
        'default_on': False,
    },
    'cpu_tuning': {'name': 'CPU调优', 'class': 'CPUTuningTab', 'default_on': False},
    'memory_backing': {'name': 'Memory支持', 'class': 'MemoryBackingTab', 'default_on': False},
    'memory_tuning': {'name': 'Memory调优', 'class': 'MemoryTuningTab', 'default_on': False},
    'numa_node_tuning': {
        'name': 'NUMA Node调优',
        'class': 'NUMANodeTuningTab',
        'default_on': False,
    },
    'block_io_tuning': {
        'name': 'Block I/O调优',
        'class': 'BlockIOTuningTab',
        'default_on': False,
    },
    'resource_partitioning': {
        'name': '资源分区',
        'class': 'ResourcePartitioningTab',
        'default_on': False,
    },
    'fibre_channel_vmid': {
        'name': '光纤通道VMID',
        'class': 'FibreChannelVMIDTab',
        'default_on': False,
    },
    'cpu_model_topology': {
        'name': 'CPU模型和拓扑',
        'class': 'CPUModelTopologyTab',
        'default_on': True,
    },
    'events_configuration': {
        'name': '事件配置',
        'class': 'EventsConfigurationTab',
        'default_on': False,
    },
    'power_management': {
        'name': '电源管理',
        'class': 'PowerManagementTab',
        'default_on': False,
    },
    'disk_throttle_group': {
        'name': '磁盘限流组',
        'class': 'DiskThrottleGroupTab',
        'default_on': False,
    },
    'hypervisor_features': {
        'name': '虚拟机特性',
        'class': 'HypervisorFeaturesTab',
        'default_on': False,
    },
    'time_keeping': {'name': '时间管理', 'class': 'TimeKeepingTab', 'default_on': False},
    'performance_monitoring': {
        'name': '性能监测',
        'class': 'PerformanceMonitoringTab',
        'default_on': False,
    },
    'security_label': {'name': '安全标签', 'class': 'SecurityLabelTab', 'default_on': False},
    'key_wrap': {'name': '密钥封装', 'class': 'KeyWrapTab', 'default_on': False},
    'launch_security': {
        'name': '启动安全',
        'class': 'LaunchSecurityTab',
        'default_on': False,
    },
}
