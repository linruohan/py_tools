from dataclasses import dataclass
from typing import Optional


@dataclass
class KeyWrap:
    """密钥包装配置"""

    type: str
    uuid: Optional[str] = None
    masterkeyid: Optional[str] = None
