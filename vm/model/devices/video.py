"""Video 设备配置 - 整合策略模式."""

from dataclasses import dataclass
from typing import Any

# 从 config 模块导入枚举类型
from config.strategies.option_strategies import VideoModel


@dataclass
class Video:
    """视频设备配置"""

    model: VideoModel = VideoModel.QXL
    vram: int = 64  # MiB
    heads: int = 1
    primary: bool | None = None
    accel: str | None = None
    rom_file: str | None = None
    resolution: dict[str, int] | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'Video':
        """从字典创建"""
        model = data.get('model', 'qxl')
        if isinstance(model, str):
            model = VideoModel(model)

        return cls(
            model=model,
            vram=data.get('vram', 64),
            heads=data.get('heads', 1),
            primary=data.get('primary'),
            accel=data.get('accel'),
            rom_file=data.get('rom_file'),
            resolution=data.get('resolution'),
        )

    def to_dict(self) -> dict[str, Any]:
        """转换为字典"""
        return {
            'model': self.model.value,
            'vram': self.vram,
            'heads': self.heads,
            'primary': self.primary,
            'accel': self.accel,
            'rom_file': self.rom_file,
            'resolution': self.resolution,
        }
