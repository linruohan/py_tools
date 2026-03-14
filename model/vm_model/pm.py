from dataclasses import dataclass
from typing import Optional


@dataclass
class PM:
    """电源管理配置"""

    suspend_to_mem: Optional[bool] = None
    suspend_to_disk: Optional[bool] = None
    graceful_shutdown: Optional[bool] = None
