from dataclasses import dataclass, field


@dataclass
class FirmwareFeature:
    """固件特性"""

    name: str
    enabled: bool


@dataclass
class Loader:
    """引导加载器配置"""

    path: str | None = None
    readonly: bool | None = None
    secure: bool | None = None
    type: str | None = None  # rom or pflash
    stateless: bool | None = None
    format: str | None = None


@dataclass
class NvramSource:
    """NVRAM 源配置"""

    file: str | None = None
    protocol: str | None = None
    name: str | None = None
    hosts: list[dict] = field(default_factory=list)
    auth: dict | None = None


@dataclass
class Nvram:
    """NVRAM 配置"""

    path: str | None = None
    template: str | None = None
    templateFormat: str | None = None
    type: str | None = None  # file, block, network
    source: NvramSource | None = None
    format: str | None = None


@dataclass
class Varstore:
    """变量存储配置"""

    path: str
    template: str | None = None


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
    timeout: int | None = None


@dataclass
class Bios:
    """BIOS 配置"""

    useserial: bool | None = None
    rebootTimeout: int | None = None


@dataclass
class AcpiTable:
    """ACPI 表配置"""

    type: str  # raw, rawset, slic, msdm
    path: str


@dataclass
class Acpi:
    """ACPI 配置"""

    tables: list[AcpiTable] = field(default_factory=list)


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
    arch: str | None = None
    machine: str | None = None
    firmware: str | None = None  # bios, efi
    firmware_features: list[FirmwareFeature] = field(default_factory=list)
    loader: Loader | None = None
    nvram: Nvram | None = None
    varstore: Varstore | None = None
    boot: list[Boot] = field(default_factory=list)
    smbios: Smbios | None = None
    bootmenu: Bootmenu | None = None
    bios: Bios | None = None
    bootloader: str | None = None
    bootloader_args: str | None = None
    kernel: str | None = None
    initrd: str | None = None
    cmdline: str | None = None
    shim: str | None = None
    dtb: str | None = None
    init: str | None = None
    initargs: list[str] = field(default_factory=list)
    initenv: list[dict] = field(default_factory=list)
    initdir: str | None = None
    inituser: str | None = None
    initgroup: str | None = None
    idmap: Idmap | None = None
    acpi: Acpi | None = None
