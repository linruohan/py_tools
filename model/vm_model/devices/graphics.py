"""Graphics 设备配置 - 整合策略模式."""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any

# 从 config 模块导入枚举类型
from config.strategies.option_strategies import GraphicsType


@dataclass
class Graphics:
    """图形设备配置"""

    type: GraphicsType = GraphicsType.VNC
    port: str = '-1'
    tls_port: Optional[str] = None
    listen: str = '0.0.0.0'
    passwd: Optional[str] = None
    connected: Optional[str] = None
    keymap: Optional[str] = None
    default_mode: Optional[str] = None
    image_compression: Optional[str] = None
    jpeg_compression: Optional[str] = None
    zlib_compression: Optional[str] = None
    opengl: Optional[bool] = None
    listen_addresses: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Graphics':
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

    def to_dict(self) -> Dict[str, Any]:
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
