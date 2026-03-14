"""VM Panel 模块包 - 6 个主要功能模块."""

from .advanced_tuning_module import AdvancedTuningModule
from .basic_info_module import BasicInfoModule
from .combined_devices_module import CombinedDevicesModule
from .cpu_memory_module import CPUMemoryModule
from .metadata_module import MetadataModule
from .os_boot_module import OSBootModule

__all__ = [
    "AdvancedTuningModule",
    "BasicInfoModule",
    "CombinedDevicesModule",
    "CPUMemoryModule",
    "MetadataModule",
    "OSBootModule",
]
