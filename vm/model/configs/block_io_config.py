"""块 I/O 优化配置数据类."""

from dataclasses import dataclass, field


@dataclass
class BlockIODevice:
    """块 IO 设备配置类."""

    path: str = ''
    weight: int | None = None  # 100-1000
    read_bytes_sec: int | None = None
    write_bytes_sec: int | None = None
    read_iops_sec: int | None = None
    write_iops_sec: int | None = None

    def update(self, data: dict) -> None:
        """更新配置."""
        for key in [
            'path',
            'weight',
            'read_bytes_sec',
            'write_bytes_sec',
            'read_iops_sec',
            'write_iops_sec',
        ]:
            if key in data:
                setattr(self, key, data[key])

    def to_dict(self) -> dict:
        """转换为字典格式,只包含有值的字段."""
        result = {}
        if self.path:
            result['path'] = self.path
        if self.weight is not None:
            result['weight'] = self.weight
        if self.read_bytes_sec is not None:
            result['read_bytes_sec'] = self.read_bytes_sec
        if self.write_bytes_sec is not None:
            result['write_bytes_sec'] = self.write_bytes_sec
        if self.read_iops_sec is not None:
            result['read_iops_sec'] = self.read_iops_sec
        if self.write_iops_sec is not None:
            result['write_iops_sec'] = self.write_iops_sec
        return result

    @classmethod
    def from_dict(cls, data: dict) -> 'BlockIODevice':
        """从字典创建实例."""
        return cls(
            path=data.get('path', ''),
            weight=data.get('weight'),
            read_bytes_sec=data.get('read_bytes_sec'),
            write_bytes_sec=data.get('write_bytes_sec'),
            read_iops_sec=data.get('read_iops_sec'),
            write_iops_sec=data.get('write_iops_sec'),
        )


@dataclass
class BlockIOConfig:
    """块 IO 优化配置类."""

    weight: int | None = None  # 全局权重 100-1000
    devices: list[BlockIODevice] = field(default_factory=list)

    def update(self, data: dict) -> None:
        """更新配置."""
        if 'weight' in data:
            self.weight = data['weight']
        if 'devices' in data:
            self.devices = [
                BlockIODevice.from_dict(d) if isinstance(d, dict) else d for d in data['devices']
            ]

    def to_dict(self) -> dict:
        """转换为字典格式."""
        result = {}
        if self.weight is not None:
            result['weight'] = self.weight
        if self.devices:
            result['devices'] = [d.to_dict() for d in self.devices]
        return result

    def is_empty(self) -> bool:
        """检查配置是否为空."""
        return self.weight is None and not self.devices
