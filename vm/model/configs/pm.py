from dataclasses import dataclass


@dataclass
class PM:
    """电源管理配置"""

    suspend_to_mem: bool | None = None
    suspend_to_disk: bool | None = None
    graceful_shutdown: bool | None = None
