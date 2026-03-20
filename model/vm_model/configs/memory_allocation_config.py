"""内存分配配置类 - 使用 dataclass 简化的配置类."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class MemoryAllocationConfig:
    """内存分配配置类."""

    memory: int = 2097152  # KiB
    current_memory: Optional[int] = 2097152  # KiB
    max_memory: Optional[int] = 4194304  # KiB
    unit: str = 'KiB'
    memory_slots: int = 16
    dump_core: Optional[bool] = None

    def update(self, data: dict) -> None:
        """更新配置."""
        for key in ['memory', 'current_memory', 'max_memory', 'unit', 'memory_slots', 'dump_core']:
            if key in data:
                setattr(self, key, data[key])

    def to_dict(self) -> dict:
        """转换为字典格式."""
        from dataclasses import asdict

        return asdict(self)
