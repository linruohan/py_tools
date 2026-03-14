from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class Metadata:
    """元数据配置"""

    name: Optional[str] = None
    uuid: Optional[str] = None
    description: Optional[str] = None
    title: Optional[str] = None
    os_type: Optional[str] = None
    os_variant: Optional[str] = None
    annotations: List[dict] = field(default_factory=list)
