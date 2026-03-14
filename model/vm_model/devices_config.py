"""设备配置类 - 管理虚拟机设备配置信息."""


class DevicesConfig:
    """设备配置类."""

    def __init__(self):
        """初始化设备配置."""
        self.emulator = ''
        self.disks = []
        self.disk_devices = []
        self.interfaces = []
        self.graphics = {
            'type': 'vnc',
            'port': '-1',
            'listen': '0.0.0.0',
            'passwd': '',
        }
        self.videos = []
        self.controllers = []
        self.serials = []
        self.inputs = []
        self.sounds = []
        self.hostdevs = []

    def update(self, data: dict) -> None:
        """更新配置.

        Args:
            data: 配置数据
        """
        if 'emulator' in data:
            self.emulator = data['emulator']
        if 'disks' in data:
            self.disks = data['disks']
        if 'disk_devices' in data:
            self.disk_devices = data['disk_devices']
        if 'interfaces' in data:
            self.interfaces = data['interfaces']
        if 'graphics' in data:
            self.graphics.update(data['graphics'])
        if 'videos' in data:
            self.videos = data['videos']
        if 'controllers' in data:
            self.controllers = data['controllers']
        if 'serials' in data:
            self.serials = data['serials']
        if 'inputs' in data:
            self.inputs = data['inputs']
        if 'sounds' in data:
            self.sounds = data['sounds']
        if 'hostdevs' in data:
            self.hostdevs = data['hostdevs']

    def to_dict(self) -> dict:
        """转换为字典格式.

        Returns:
            配置字典
        """
        return {
            'emulator': self.emulator,
            'disks': self.disks,
            'disk_devices': self.disk_devices,
            'interfaces': self.interfaces,
            'graphics': self.graphics,
            'videos': self.videos,
            'controllers': self.controllers,
            'serials': self.serials,
            'inputs': self.inputs,
            'sounds': self.sounds,
            'hostdevs': self.hostdevs,
        }
