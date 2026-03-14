from dataclasses import dataclass
from typing import Optional


@dataclass
class LaunchSecurity:
    """启动安全配置"""

    type: str  # selinux, apparmor, smack, windows, tpm
    model: Optional[str] = None
    profile: Optional[str] = None
    policy: Optional[str] = None
