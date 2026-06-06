from dataclasses import dataclass, field


@dataclass
class SMBIOSBIOS:
    """SMBIOS BIOS 信息"""

    vendor: str | None = None
    version: str | None = None
    date: str | None = None
    release: str | None = None


@dataclass
class SMBIOSSystem:
    """SMBIOS 系统信息"""

    manufacturer: str | None = None
    product: str | None = None
    version: str | None = None
    serial: str | None = None
    uuid: str | None = None
    sku: str | None = None
    family: str | None = None


@dataclass
class SMBIOSBaseBoard:
    """SMBIOS 主板信息"""

    manufacturer: str | None = None
    product: str | None = None
    version: str | None = None
    serial: str | None = None
    asset: str | None = None
    location: str | None = None


@dataclass
class SMBIOSChassis:
    """SMBIOS 机箱信息"""

    manufacturer: str | None = None
    version: str | None = None
    serial: str | None = None
    asset: str | None = None
    sku: str | None = None


@dataclass
class FWCFGEntry:
    """FWCFG 条目"""

    name: str
    value: str | None = None
    file: str | None = None


@dataclass
class SysInfo:
    """系统信息配置"""

    type: str  # smbios or fwcfg
    bios: SMBIOSBIOS | None = None
    system: SMBIOSSystem | None = None
    base_boards: list[SMBIOSBaseBoard] = field(default_factory=list)
    chassis: SMBIOSChassis | None = None
    oem_strings: list[str] = field(default_factory=list)
    fwcfg_entries: list[FWCFGEntry] = field(default_factory=list)
