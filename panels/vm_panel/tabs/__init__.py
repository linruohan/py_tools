"""Tabs - 虚拟机配置 Tab 模块."""

from .basic_tab import BasicTab
from .block_io_tuning_tab import BlockIOTuningTab
from .cpu_model_topology_tab import CPUModelTopologyTab
from .cpu_tuning_tab import CPUTuningTab
from .devices_tab import DevicesTab
from .disk_throttle_group_tab import DiskThrottleGroupTab
from .events_configuration_tab import EventsConfigurationTab
from .fibre_channel_vmid_tab import FibreChannelVMIDTab
from .hypervisor_features_tab import HypervisorFeaturesTab
from .iothreads_allocation_tab import IOThreadsAllocationTab
from .key_wrap_tab import KeyWrapTab
from .launch_security_tab import LaunchSecurityTab
from .memory_allocation_tab import MemoryAllocationTab
from .memory_backing_tab import MemoryBackingTab
from .memory_tuning_tab import MemoryTuningTab
from .numa_node_tuning_tab import NUMANodeTuningTab
from .os_tab import OSTab
from .performance_monitoring_tab import PerformanceMonitoringTab
from .power_management_tab import PowerManagementTab
from .resource_partitioning_tab import ResourcePartitioningTab
from .security_label_tab import SecurityLabelTab
from .smbios_system_tab import SMBIOSSystemTab
from .time_keeping_tab import TimeKeepingTab

__all__ = [
    'BasicTab',
    'BlockIOTuningTab',
    'CPUModelTopologyTab',
    'CPUTuningTab',
    'DevicesTab',
    'DiskThrottleGroupTab',
    'EventsConfigurationTab',
    'FibreChannelVMIDTab',
    'HypervisorFeaturesTab',
    'IOThreadsAllocationTab',
    'KeyWrapTab',
    'LaunchSecurityTab',
    'MemoryAllocationTab',
    'MemoryBackingTab',
    'MemoryTuningTab',
    'NUMANodeTuningTab',
    'OSTab',
    'PerformanceMonitoringTab',
    'PowerManagementTab',
    'ResourcePartitioningTab',
    'SMBIOSSystemTab',
    'SecurityLabelTab',
    'TimeKeepingTab',
]
