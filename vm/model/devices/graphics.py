"""Graphics 设备配置 - 整合策略模式."""

from dataclasses import dataclass, field
from typing import Any

# 从 config 模块导入枚举类型
from config.strategies.option_strategies import GraphicsType


@dataclass
class Graphics:
    """图形设备配置"""

    type: GraphicsType = GraphicsType.VNC
    port: str = '-1'
    tls_port: str | None = None
    listen: str = '0.0.0.0'
    passwd: str | None = None
    connected: str | None = None
    keymap: str | None = None
    default_mode: str | None = None
    image_compression: str | None = None
    jpeg_compression: str | None = None
    zlib_compression: str | None = None
    opengl: bool | None = None
    listen_addresses: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'Graphics':
        """从字典创建"""
        gfx_type = data.get('type', 'vnc')
        if isinstance(gfx_type, str):
            gfx_type = GraphicsType(gfx_type)

        return cls(
            type=gfx_type,
            port=data.get('port', '-1'),
            tls_port=data.get('tls_port'),
            listen=data.get('listen', '0.0.0.0'),
            passwd=data.get('passwd'),
            connected=data.get('connected'),
            keymap=data.get('keymap'),
            default_mode=data.get('default_mode'),
            image_compression=data.get('image_compression'),
            jpeg_compression=data.get('jpeg_compression'),
            zlib_compression=data.get('zlib_compression'),
            opengl=data.get('opengl'),
            listen_addresses=data.get('listen_addresses', []),
        )

    def to_dict(self) -> dict[str, Any]:
        """转换为字典"""
        return {
            'type': self.type.value,
            'port': self.port,
            'tls_port': self.tls_port,
            'listen': self.listen,
            'passwd': self.passwd,
            'connected': self.connected,
            'keymap': self.keymap,
            'default_mode': self.default_mode,
            'image_compression': self.image_compression,
            'jpeg_compression': self.jpeg_compression,
            'zlib_compression': self.zlib_compression,
            'opengl': self.opengl,
            'listen_addresses': self.listen_addresses,
        }
