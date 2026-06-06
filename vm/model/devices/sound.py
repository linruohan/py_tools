"""Sound 设备配置 - 整合策略模式."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Sound:
    """Sound 设备配置"""

    model: str = 'ich6'  # ich6, ich9, es1370, sb16, cs4231a, ac97, hda
    codec: str | None = None  # 编解码器
    outputs: list[dict[str, str]] = field(default_factory=list)  # 输出列表

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'Sound':
        """从字典创建"""
        return cls(
            model=data.get('model', 'ich6'),
            codec=data.get('codec'),
            outputs=data.get('outputs', []),
        )

    def to_dict(self) -> dict[str, Any]:
        """转换为字典"""
        return {
            'model': self.model,
            'codec': self.codec,
            'outputs': self.outputs,
        }
