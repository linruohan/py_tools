from dataclasses import dataclass


@dataclass
class KeyWrap:
    """密钥包装配置"""

    type: str
    uuid: str | None = None
    masterkeyid: str | None = None
