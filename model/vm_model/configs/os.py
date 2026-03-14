from dataclasses import dataclass, field
from typing import List, Optional, Union


@dataclass
class FirmwareFeature:
    """固件特性"""

    name: str
    enabled: bool


@dataclass
class Loader:
    """引导加载器配置"""

    path: Optional[str] = None
    readonly: Optional[bool] = None
    secure: Optional[bool] = None
    type: Optional[str] = None  # rom or pflash
    stateless: Optional[bool] = None
    format: Optional[str] = None


@dataclass
class NvramSource:
    """NVRAM 源配置"""

    file: Optional[str] = None
    protocol: Optional[str] = None
    name: Optional[str] = None
    hosts: List[dict] = field(default_factory=list)
    auth: Optional[dict] = None


@dataclass
class Nvram:
    """NVRAM 配置"""

    path: Optional[str] = None
    template: Optional[str] = None
    templateFormat: Optional[str] = None
    type: Optional[str] = None  # file, block, network
    source: Optional[NvramSource] = None
    format: Optional[str] = None


@dataclass
class Varstore:
    """变量存储配置"""

    path: str
    template: Optional[str] = None


@dataclass
class Boot:
    """启动设备配置"""

    dev: str  # fd, hd, cdrom, network


@dataclass
class Smbios:
    """SMBIOS 配置"""

    mode: str  # emulate, host, sysinfo


@dataclass
class Bootmenu:
    """启动菜单配置"""

    enable: bool
    timeout: Optional[int] = None


@dataclass
class Bios:
    """BIOS 配置"""

    useserial: Optional[bool] = None
    rebootTimeout: Optional[int] = None


@dataclass
class AcpiTable:
    """ACPI 表配置"""

    type: str  # raw, rawset, slic, msdm
    path: str


@dataclass
class Acpi:
    """ACPI 配置"""

    tables: List[AcpiTable] = field(default_factory=list)


@dataclass
class IdmapEntry:
    """ID 映射条目"""

    start: int
    target: int
    count: int


@dataclass
class Idmap:
    """ID 映射配置"""

    uid: IdmapEntry
    gid: IdmapEntry


@dataclass
class OS:
    """操作系统配置"""

    type: str
    arch: Optional[str] = None
    machine: Optional[str] = None
    firmware: Optional[str] = None  # bios, efi
    firmware_features: List[FirmwareFeature] = field(default_factory=list)
    loader: Optional[Loader] = None
    nvram: Optional[Nvram] = None
    varstore: Optional[Varstore] = None
    boot: List[Boot] = field(default_factory=list)
    smbios: Optional[Smbios] = None
    bootmenu: Optional[Bootmenu] = None
    bios: Optional[Bios] = None
    bootloader: Optional[str] = None
    bootloader_args: Optional[str] = None
    kernel: Optional[str] = None
    initrd: Optional[str] = None
    cmdline: Optional[str] = None
    shim: Optional[str] = None
    dtb: Optional[str] = None
    init: Optional[str] = None
    initargs: List[str] = field(default_factory=list)
    initenv: List[dict] = field(default_factory=list)
    initdir: Optional[str] = None
    inituser: Optional[str] = None
    initgroup: Optional[str] = None
    idmap: Optional[Idmap] = None
    acpi: Optional[Acpi] = None
