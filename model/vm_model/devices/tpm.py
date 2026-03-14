"""TPM 设备配置 - 整合策略模式."""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List


@dataclass
class TPM:
    """TPM 设备配置"""

    model: str = 'tpm-tis'  # tpm-tis, tpm-crb, tpm-spapr
    type: str = 'passthrough'  # passthrough, emulator
    device_path: Optional[str] = None  # /dev/tpm0
    version: Optional[str] = None  # 1.2, 2.0
    persistent_state: Optional[bool] = None  # 持久化状态
    source_remove: Optional[bool] = None  # 源移除

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TPM':
        """从字典创建"""
        return cls(
            model=data.get('model', 'tpm-tis'),
            type=data.get('type', 'passthrough'),
            device_path=data.get('device_path'),
            version=data.get('version'),
            persistent_state=data.get('persistent_state'),
            source_remove=data.get('source_remove'),
        )

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'model': self.model,
            'type': self.type,
            'device_path': self.device_path,
            'version': self.version,
            'persistent_state': self.persistent_state,
            'source_remove': self.source_remove,
        }
