"""Memory 设备配置 - 整合策略模式."""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List

# 从 config 模块导入枚举类型
from config.strategies.option_strategies import MemoryUnit


@dataclass
class Memory:
    """内存设备配置"""

    size: int = 0
    unit: MemoryUnit = MemoryUnit.MIB
    nodemask: Optional[str] = None
    access: Optional[str] = None
    align: Optional[str] = None
    labels: Optional[List[str]] = field(default_factory=list)
    slots: Optional[int] = None
    use: Optional[str] = None
    replace: Optional[str] = None
    alias: Optional[str] = None
    address: Optional[Dict[str, str]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Memory':
        """从字典创建"""
        unit = data.get('unit', 'MiB')
        if isinstance(unit, str):
            unit = MemoryUnit(unit)

        return cls(
            size=data.get('size', 0),
            unit=unit,
            nodemask=data.get('nodemask'),
            access=data.get('access'),
            align=data.get('align'),
            labels=data.get('labels', []),
            slots=data.get('slots'),
            use=data.get('use'),
            replace=data.get('replace'),
            alias=data.get('alias'),
            address=data.get('address'),
        )

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'size': self.size,
            'unit': self.unit.value,
            'nodemask': self.nodemask,
            'access': self.access,
            'align': self.align,
            'labels': self.labels,
            'slots': self.slots,
            'use': self.use,
            'replace': self.replace,
            'alias': self.alias,
            'address': self.address,
        }
