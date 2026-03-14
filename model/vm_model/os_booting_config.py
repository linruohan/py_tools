"""系统引导配置类 - 管理虚拟机系统引导配置信息."""


class OSBootingConfig:
    """系统引导配置类."""

    def __init__(self):
        """初始化系统引导配置."""
        self.type = 'guest_firmware'
        self.os_type = 'hvm'
        self.arch = 'x86_64'
        self.machine = 'virt'
        self.firmware = 'bios'
        self.loader_path = ''
        self.nvram_path = ''
        self.boot_dev = 'hd'
        self.boot_menu = False
        self.boot_timeout = 3000
        self.smbios_mode = ''
        self.kernel = ''
        self.initrd = ''
        self.cmdline = ''
        self.dtb = ''
        self.init = ''
        self.init_args = ''
        self.bootloader = ''
        self.bootloader_args = ''

    def update(self, data: dict) -> None:
        """更新配置.

        Args:
            data: 配置数据
        """
        if 'type' in data:
            self.type = data['type']
        if 'os_type' in data:
            self.os_type = data['os_type']
        if 'arch' in data:
            self.arch = data['arch']
        if 'machine' in data:
            self.machine = data['machine']
        if 'firmware' in data:
            self.firmware = data['firmware']
        if 'loader_path' in data:
            self.loader_path = data['loader_path']
        if 'nvram_path' in data:
            self.nvram_path = data['nvram_path']
        if 'boot_dev' in data:
            self.boot_dev = data['boot_dev']
        if 'boot_menu' in data:
            self.boot_menu = data['boot_menu']
        if 'boot_timeout' in data:
            self.boot_timeout = data['boot_timeout']
        if 'smbios_mode' in data:
            self.smbios_mode = data['smbios_mode']
        if 'kernel' in data:
            self.kernel = data['kernel']
        if 'initrd' in data:
            self.initrd = data['initrd']
        if 'cmdline' in data:
            self.cmdline = data['cmdline']
        if 'dtb' in data:
            self.dtb = data['dtb']
        if 'init' in data:
            self.init = data['init']
        if 'init_args' in data:
            self.init_args = data['init_args']
        if 'bootloader' in data:
            self.bootloader = data['bootloader']
        if 'bootloader_args' in data:
            self.bootloader_args = data['bootloader_args']

    def to_dict(self) -> dict:
        """转换为字典格式.

        Returns:
            配置字典
        """
        return {
            'type': self.type,
            'os_type': self.os_type,
            'arch': self.arch,
            'machine': self.machine,
            'firmware': self.firmware,
            'loader_path': self.loader_path,
            'nvram_path': self.nvram_path,
            'boot_dev': self.boot_dev,
            'boot_menu': self.boot_menu,
            'boot_timeout': self.boot_timeout,
            'smbios_mode': self.smbios_mode,
            'kernel': self.kernel,
            'initrd': self.initrd,
            'cmdline': self.cmdline,
            'dtb': self.dtb,
            'init': self.init,
            'init_args': self.init_args,
            'bootloader': self.bootloader,
            'bootloader_args': self.bootloader_args,
        }
