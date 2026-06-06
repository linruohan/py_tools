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
    source: dict = (
        None  # source 配置 (file/block 类型: {'file': path}, network 类型: {'protocol': xxx, ...})
    )

    def __post_init__(self):
        if self.source is None:
            self.source = {}


@dataclass
class Varstore:
    """Varstore 配置."""

    path: str = ''
    template: str = ''


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
        self.varstore = Varstore()

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
        # 基本 OS 配置
        if 'type' in data:
            self.type = data['type']
        if 'arch' in data:
            self.arch = data['arch']
        if 'machine' in data:
            self.machine = data['machine']
        if 'firmware' in data:
            self.firmware = data['firmware']

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
        if 'varstore' in data:
            varstore_data = data['varstore']
            if isinstance(varstore_data, dict):
                for key, value in varstore_data.items():
                    if hasattr(self.varstore, key):
                        setattr(self.varstore, key, value)
            else:
                self.varstore.path = varstore_data

        # 启动设备
        if 'boot_devices' in data:
            devices = data['boot_devices']
            if isinstance(devices, list):
                self.boot_devices = [
                    BootDevice(**d) if isinstance(d, dict) else BootDevice(dev=d) for d in devices
                ]
            else:
                self.boot_devices = []

        # 启动菜单
        if 'bootmenu' in data:
            bootmenu_data = data['bootmenu']
            if isinstance(bootmenu_data, dict):
                for key, value in bootmenu_data.items():
                    if hasattr(self.bootmenu, key):
                        setattr(self.bootmenu, key, value)

        # BIOS 配置
        if 'bios' in data:
            bios_data = data['bios']
            if isinstance(bios_data, dict):
                for key, value in bios_data.items():
                    if hasattr(self.bios, key):
                        setattr(self.bios, key, value)

        # SMBIOS 配置
        if 'smbios' in data:
            smbios_data = data['smbios']
            if isinstance(smbios_data, dict):
                for key, value in smbios_data.items():
                    if hasattr(self.smbios, key):
                        setattr(self.smbios, key, value)

        # 固件特性
        if 'firmware_features' in data:
            self.firmware_features = [
                FirmwareFeature(**f) if isinstance(f, dict) else f
                for f in data['firmware_features']
            ]

        # 直接内核引导 (direct_kernel)
        if 'direct_kernel' in data:
            dk_data = data['direct_kernel']
            if isinstance(dk_data, dict):
                self.kernel = dk_data.get('kernel', '')
                self.initrd = dk_data.get('initrd', '')
                self.cmdline = dk_data.get('cmdline', '')
                self.shim = dk_data.get('shim', '')
                self.dtb = dk_data.get('dtb', '')

        # 主机引导加载器 (host_bootloader)
        if 'host_bootloader' in data:
            hl_data = data['host_bootloader']
            if isinstance(hl_data, dict):
                self.bootloader = hl_data.get('path', '')
                self.bootloader_args = hl_data.get('args', '')

        # 容器启动配置 (container)
        if 'container' in data:
            container_data = data['container']
            if isinstance(container_data, dict):
                self.container_init = container_data.get('init', '')
                self.container_initargs = container_data.get('initargs', [])
                self.container_initenv = container_data.get('initenvs', [])
                self.container_initdir = container_data.get('initdir', '')
                self.container_inituser = container_data.get('inituser', '')
                self.container_initgroup = container_data.get('initgroup', '')

        # ID 映射 (idmap)
        if 'idmap' in data:
            idmap_data = data['idmap']
            if isinstance(idmap_data, dict):
                if 'uid' in idmap_data:
                    uid = idmap_data['uid']
                    self.idmap_uid_start = uid.get('start', 0)
                    self.idmap_uid_target = uid.get('target', 0)
                    self.idmap_uid_count = uid.get('count', 0)
                if 'gid' in idmap_data:
                    gid = idmap_data['gid']
                    self.idmap_gid_start = gid.get('start', 0)
                    self.idmap_gid_target = gid.get('target', 0)
                    self.idmap_gid_count = gid.get('count', 0)

        # ACPI 表配置 (acpi)
        if 'acpi' in data:
            acpi_data = data['acpi']
            if isinstance(acpi_data, dict):
                if 'tables' in acpi_data:
                    tables = acpi_data['tables']
                    if isinstance(tables, list):
                        self.acpi_tables = [
                            AcpiTable(type=t.get('type', 'raw'), path=t.get('path', ''))
                            if isinstance(t, dict)
                            else t
                            for t in tables
                        ]
                elif 'table' in acpi_data:
                    table = acpi_data['table']
                    if isinstance(table, dict):
                        self.acpi_tables = [
                            AcpiTable(type=table.get('type', 'raw'), path=table.get('path', ''))
                        ]

    def to_dict(self) -> dict:
        """转换为字典格式.

        Returns:
            配置字典
        """
        result = {
            'type': self.type,
            'arch': self.arch
            if self.arch
            else None,  # 空值返回 None，让 XML 生成器决定是否使用默认值
            'machine': self.machine if self.machine else None,
            'firmware': self.firmware if self.firmware else None,
            'boot_devices': [d.dev for d in self.boot_devices],
            'kernel': self.kernel if self.kernel else None,
            'initrd': self.initrd if self.initrd else None,
            'cmdline': self.cmdline if self.cmdline else None,
            'shim': self.shim if self.shim else None,
            'dtb': self.dtb if self.dtb else None,
            'firmware_features': [
                {'name': f.name, 'enabled': f.enabled} for f in self.firmware_features
            ],
        }

        # Loader 配置
        loader_dict = {
            'path': self.loader.path,
            'readonly': self.loader.readonly,
            'secure': self.loader.secure,
            'type': self.loader.type,
            'stateless': self.loader.stateless,
            'format': self.loader.format,
        }
        if loader_dict.get('path') or any(v for k, v in loader_dict.items() if k != 'path'):
            result['loader'] = loader_dict

        # NVRAM 配置
        nvram_dict = {
            'path': self.nvram.path,
            'template': self.nvram.template,
            'templateFormat': self.nvram.templateFormat,
            'type': self.nvram.type,
            'format': self.nvram.format,
            'source': self.nvram.source,
        }
        if nvram_dict.get('path') or nvram_dict.get('template') or nvram_dict.get('source'):
            result['nvram'] = nvram_dict

        # Varstore 配置
        varstore_dict = {
            'path': self.varstore.path,
            'template': self.varstore.template,
        }
        if varstore_dict.get('path') or varstore_dict.get('template'):
            result['varstore'] = varstore_dict

        # Bootmenu 配置
        if self.bootmenu.enable or (self.bootmenu.timeout and self.bootmenu.timeout >= 0):
            result['bootmenu'] = {
                'enable': self.bootmenu.enable,
                'timeout': self.bootmenu.timeout if self.bootmenu.timeout >= 0 else None,
            }

        # BIOS 配置
        bios_dict = {
            'useserial': self.bios.useserial,
            'rebootTimeout': self.bios.rebootTimeout,
        }
        if bios_dict.get('useserial') or (
            bios_dict.get('rebootTimeout') and bios_dict['rebootTimeout'] >= 0
        ):
            result['bios'] = bios_dict

        # SMBIOS 配置
        if self.smbios.mode and self.smbios.mode != 'emulate':
            result['smbios'] = {'mode': self.smbios.mode}

        # 直接内核引导 (direct_kernel)
        if self.kernel or self.initrd or self.cmdline:
            result['direct_kernel'] = {
                'kernel': self.kernel,
                'initrd': self.initrd,
                'cmdline': self.cmdline,
                'shim': self.shim,
                'dtb': self.dtb,
            }

        # 主机引导加载器 (host_bootloader)
        if self.bootloader:
            result['host_bootloader'] = {
                'path': self.bootloader,
                'args': self.bootloader_args,
            }

        # 容器引导
        if (
            self.container_init
            or self.container_initargs
            or self.container_initenv
            or self.container_initdir
            or self.container_inituser
            or self.container_initgroup
        ):
            result['container'] = {
                'init': self.container_init,
                'initargs': self.container_initargs,
                'initenvs': self.container_initenv,
                'initdir': self.container_initdir,
                'inituser': self.container_inituser,
                'initgroup': self.container_initgroup,
            }

        # ID 映射
        idmap_config = {}
        if self.idmap_uid_target != 0:
            idmap_config['uid'] = {
                'start': self.idmap_uid_start,
                'target': self.idmap_uid_target,
                'count': self.idmap_uid_count,
            }
        if self.idmap_gid_target != 0:
            idmap_config['gid'] = {
                'start': self.idmap_gid_start,
                'target': self.idmap_gid_target,
                'count': self.idmap_gid_count,
            }
        if idmap_config:
            result['idmap'] = idmap_config

        # ACPI 表
        if self.acpi_tables:
            result['acpi'] = {
                'tables': [{'type': t.type, 'path': t.path} for t in self.acpi_tables]
            }

        return result
