"""系统引导配置类 - 管理虚拟机系统引导配置信息."""

from dataclasses import dataclass


@dataclass
class BootDevice:
    """启动设备配置."""

    dev: str  # fd, hd, cdrom, network


@dataclass
class Bootmenu:
    """启动菜单配置."""

    enable: bool = False
    timeout: int = -1  # -1 表示禁用


@dataclass
class Bios:
    """BIOS 配置."""

    useserial: bool = False
    rebootTimeout: int = -1


@dataclass
class Smbios:
    """SMBIOS 配置."""

    mode: str = 'emulate'  # emulate, host, sysinfo


@dataclass
class Loader:
    """引导加载器配置."""

    path: str = ''
    readonly: bool = True
    secure: bool = False
    type: str = 'pflash'  # rom, pflash
    stateless: bool = False
    format: str = ''  # raw, qcow2


@dataclass
class Nvram:
    """NVRAM 配置."""

    path: str = ''
    template: str = ''
    templateFormat: str = ''
    type: str = 'file'  # file, block, network
    format: str = ''


@dataclass
class FirmwareFeature:
    """固件特性."""

    name: str
    enabled: bool


@dataclass
class AcpiTable:
    """ACPI 表配置."""

    type: str  # raw, rawset, slic, msdm
    path: str


class OSBootingConfig:
    """系统引导配置类."""

    def __init__(self):
        """初始化系统引导配置."""
        # OS 类型
        self.type = 'hvm'
        self.arch = 'x86_64'
        self.machine = 'q35'

        # 固件配置
        self.firmware = ''  # bios, efi (自动选择)
        self.firmware_features: list[FirmwareFeature] = []
        self.loader = Loader()
        self.nvram = Nvram()

        # 启动设备顺序
        self.boot_devices: list[BootDevice] = []

        # 启动菜单
        self.bootmenu = Bootmenu()
        self.bios = Bios()

        # SMBIOS
        self.smbios = Smbios()

        # 直接内核引导
        self.kernel = ''
        self.initrd = ''
        self.cmdline = ''
        self.shim = ''
        self.dtb = ''

        # 主机引导加载器
        self.bootloader = ''
        self.bootloader_args = ''

        # 容器引导
        self.container_init = ''
        self.container_initargs: list[str] = []
        self.container_initenv: list[dict] = []
        self.container_initdir = ''
        self.container_inituser = ''
        self.container_initgroup = ''

        # ID 映射 (容器)
        self.idmap_uid_start = 0
        self.idmap_uid_target = 0
        self.idmap_uid_count = 0
        self.idmap_gid_start = 0
        self.idmap_gid_target = 0
        self.idmap_gid_count = 0

        # ACPI 表
        self.acpi_tables: list[AcpiTable] = []

    def update(self, data: dict) -> None:
        """更新配置.

        Args:
            data: 配置数据
        """
        if 'type' in data:
            self.type = data['type']
        if 'arch' in data:
            self.arch = data['arch']
        if 'machine' in data:
            self.machine = data['machine']
        if 'firmware' in data:
            self.firmware = data['firmware']
        if 'kernel' in data:
            self.kernel = data['kernel']
        if 'initrd' in data:
            self.initrd = data['initrd']
        if 'cmdline' in data:
            self.cmdline = data['cmdline']
        if 'shim' in data:
            self.shim = data['shim']
        if 'dtb' in data:
            self.dtb = data['dtb']
        if 'bootloader' in data:
            self.bootloader = data['bootloader']
        if 'bootloader_args' in data:
            self.bootloader_args = data['bootloader_args']
        if 'container_init' in data:
            self.container_init = data['container_init']
        if 'container_initargs' in data:
            self.container_initargs = data['container_initargs']
        if 'container_initenv' in data:
            self.container_initenv = data['container_initenv']
        if 'container_initdir' in data:
            self.container_initdir = data['container_initdir']
        if 'container_inituser' in data:
            self.container_inituser = data['container_inituser']
        if 'container_initgroup' in data:
            self.container_initgroup = data['container_initgroup']
        if 'idmap_uid_start' in data:
            self.idmap_uid_start = data['idmap_uid_start']
        if 'idmap_uid_target' in data:
            self.idmap_uid_target = data['idmap_uid_target']
        if 'idmap_uid_count' in data:
            self.idmap_uid_count = data['idmap_uid_count']
        if 'idmap_gid_start' in data:
            self.idmap_gid_start = data['idmap_gid_start']
        if 'idmap_gid_target' in data:
            self.idmap_gid_target = data['idmap_gid_target']
        if 'idmap_gid_count' in data:
            self.idmap_gid_count = data['idmap_gid_count']
        if 'acpi_tables' in data:
            self.acpi_tables = [
                AcpiTable(**t) if isinstance(t, dict) else t for t in data['acpi_tables']
            ]

        # Loader 配置
        if 'loader' in data:
            loader_data = data['loader']
            if isinstance(loader_data, dict):
                for key, value in loader_data.items():
                    if hasattr(self.loader, key):
                        setattr(self.loader, key, value)
            else:
                self.loader.path = loader_data
        if 'nvram' in data:
            nvram_data = data['nvram']
            if isinstance(nvram_data, dict):
                for key, value in nvram_data.items():
                    if hasattr(self.nvram, key):
                        setattr(self.nvram, key, value)
            else:
                self.nvram.path = nvram_data
        if 'boot_devices' in data:
            devices = data['boot_devices']
            if isinstance(devices, list):
                self.boot_devices = [
                    BootDevice(**d) if isinstance(d, dict) else BootDevice(dev=d) for d in devices
                ]
            else:
                self.boot_devices = []
        if 'bootmenu' in data:
            bootmenu_data = data['bootmenu']
            if isinstance(bootmenu_data, dict):
                for key, value in bootmenu_data.items():
                    if hasattr(self.bootmenu, key):
                        setattr(self.bootmenu, key, value)
        if 'bios' in data:
            bios_data = data['bios']
            if isinstance(bios_data, dict):
                for key, value in bios_data.items():
                    if hasattr(self.bios, key):
                        setattr(self.bios, key, value)
        if 'smbios' in data:
            smbios_data = data['smbios']
            if isinstance(smbios_data, dict):
                for key, value in smbios_data.items():
                    if hasattr(self.smbios, key):
                        setattr(self.smbios, key, value)
        if 'firmware_features' in data:
            self.firmware_features = [
                FirmwareFeature(**f) if isinstance(f, dict) else f
                for f in data['firmware_features']
            ]

    def to_dict(self) -> dict:
        """转换为字典格式.

        Returns:
            配置字典
        """
        return {
            'type': self.type,
            'arch': self.arch,
            'machine': self.machine,
            'firmware': self.firmware,
            'loader': {
                'path': self.loader.path,
                'readonly': self.loader.readonly,
                'secure': self.loader.secure,
                'type': self.loader.type,
                'stateless': self.loader.stateless,
                'format': self.loader.format,
            },
            'nvram': {
                'path': self.nvram.path,
                'template': self.nvram.template,
                'templateFormat': self.nvram.templateFormat,
                'type': self.nvram.type,
                'format': self.nvram.format,
            },
            'boot_devices': [d.dev for d in self.boot_devices],
            'bootmenu': {
                'enable': self.bootmenu.enable,
                'timeout': self.bootmenu.timeout,
            },
            'bios': {
                'useserial': self.bios.useserial,
                'rebootTimeout': self.bios.rebootTimeout,
            },
            'smbios': {
                'mode': self.smbios.mode,
            },
            'kernel': self.kernel,
            'initrd': self.initrd,
            'cmdline': self.cmdline,
            'shim': self.shim,
            'dtb': self.dtb,
            'bootloader': self.bootloader,
            'bootloader_args': self.bootloader_args,
            'container_init': self.container_init,
            'container_initargs': self.container_initargs,
            'container_initenv': self.container_initenv,
            'container_initdir': self.container_initdir,
            'container_inituser': self.container_inituser,
            'container_initgroup': self.container_initgroup,
            'idmap_uid_start': self.idmap_uid_start,
            'idmap_uid_target': self.idmap_uid_target,
            'idmap_uid_count': self.idmap_uid_count,
            'idmap_gid_start': self.idmap_gid_start,
            'idmap_gid_target': self.idmap_gid_target,
            'idmap_gid_count': self.idmap_gid_count,
            'acpi_tables': [{'type': t.type, 'path': t.path} for t in self.acpi_tables],
            'firmware_features': [
                {'name': f.name, 'enabled': f.enabled} for f in self.firmware_features
            ],
        }
