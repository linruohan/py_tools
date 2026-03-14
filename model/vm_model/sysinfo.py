from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class SMBIOSBIOS:
    """SMBIOS BIOS 信息"""

    vendor: Optional[str] = None
    version: Optional[str] = None
    date: Optional[str] = None
    release: Optional[str] = None


@dataclass
class SMBIOSSystem:
    """SMBIOS 系统信息"""

    manufacturer: Optional[str] = None
    product: Optional[str] = None
    version: Optional[str] = None
    serial: Optional[str] = None
    uuid: Optional[str] = None
    sku: Optional[str] = None
    family: Optional[str] = None


@dataclass
class SMBIOSBaseBoard:
    """SMBIOS 主板信息"""

    manufacturer: Optional[str] = None
    product: Optional[str] = None
    version: Optional[str] = None
    serial: Optional[str] = None
    asset: Optional[str] = None
    location: Optional[str] = None


@dataclass
class SMBIOSChassis:
    """SMBIOS 机箱信息"""

    manufacturer: Optional[str] = None
    version: Optional[str] = None
    serial: Optional[str] = None
    asset: Optional[str] = None
    sku: Optional[str] = None


@dataclass
class FWCFGEntry:
    """FWCFG 条目"""

    name: str
    value: Optional[str] = None
    file: Optional[str] = None


@dataclass
class SysInfo:
    """系统信息配置"""

    type: str  # smbios or fwcfg
    bios: Optional[SMBIOSBIOS] = None
    system: Optional[SMBIOSSystem] = None
    base_boards: List[SMBIOSBaseBoard] = field(default_factory=list)
    chassis: Optional[SMBIOSChassis] = None
    oem_strings: List[str] = field(default_factory=list)
    fwcfg_entries: List[FWCFGEntry] = field(default_factory=list)
