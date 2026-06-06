from dataclasses import dataclass


@dataclass
class LaunchSecurity:
    """启动安全配置"""

    type: str  # selinux, apparmor, smack, windows, tpm
    model: str | None = None
    profile: str | None = None
    policy: str | None = None
