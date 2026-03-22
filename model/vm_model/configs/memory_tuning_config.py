"""内存调优配置数据类."""

from dataclasses import dataclass


@dataclass
class MemoryTuningItem:
    """内存调优单项配置类."""

    value: str | None = None  # 值 (字符串，允许空字符串表示 None)
    unit: str = 'KiB'  # 单位：KiB, MiB, GiB, bytes

    def update(self, data: dict) -> None:
        """更新配置."""
        if 'value' in data:
            self.value = data['value']
        if 'unit' in data:
            self.unit = data['unit']

    def to_dict(self) -> dict:
        """转换为字典格式."""
        return {'value': self.value, 'unit': self.unit}

    @classmethod
    def from_dict(cls, data: dict) -> 'MemoryTuningItem':
        """从字典创建实例."""
        return cls(
            value=data.get('value'),
            unit=data.get('unit', 'KiB'),
        )

    def is_empty(self) -> bool:
        """检查配置是否为空."""
        return self.value is None or self.value == ''


@dataclass
class MemoryTuningConfig:
    """内存调优配置类."""

    hard_limit: MemoryTuningItem = None  # type: ignore
    soft_limit: MemoryTuningItem = None  # type: ignore
    swap_hard_limit: MemoryTuningItem = None  # type: ignore
    min_guarantee: MemoryTuningItem = None  # type: ignore

    def __post_init__(self):
        """初始化默认值."""
        if self.hard_limit is None:
            self.hard_limit = MemoryTuningItem()
        if self.soft_limit is None:
            self.soft_limit = MemoryTuningItem()
        if self.swap_hard_limit is None:
            self.swap_hard_limit = MemoryTuningItem()
        if self.min_guarantee is None:
            self.min_guarantee = MemoryTuningItem()

    def update(self, data: dict) -> None:
        """更新配置."""
        if 'hard_limit' in data and isinstance(data['hard_limit'], dict):
            self.hard_limit.update(data['hard_limit'])
        elif 'hard_limit' in data:
            self.hard_limit = (
                MemoryTuningItem.from_dict(data['hard_limit'])
                if data['hard_limit']
                else MemoryTuningItem()
            )

        if 'soft_limit' in data and isinstance(data['soft_limit'], dict):
            self.soft_limit.update(data['soft_limit'])
        elif 'soft_limit' in data:
            self.soft_limit = (
                MemoryTuningItem.from_dict(data['soft_limit'])
                if data['soft_limit']
                else MemoryTuningItem()
            )

        if 'swap_hard_limit' in data and isinstance(data['swap_hard_limit'], dict):
            self.swap_hard_limit.update(data['swap_hard_limit'])
        elif 'swap_hard_limit' in data:
            self.swap_hard_limit = (
                MemoryTuningItem.from_dict(data['swap_hard_limit'])
                if data['swap_hard_limit']
                else MemoryTuningItem()
            )

        if 'min_guarantee' in data and isinstance(data['min_guarantee'], dict):
            self.min_guarantee.update(data['min_guarantee'])
        elif 'min_guarantee' in data:
            self.min_guarantee = (
                MemoryTuningItem.from_dict(data['min_guarantee'])
                if data['min_guarantee']
                else MemoryTuningItem()
            )

    def to_dict(self) -> dict:
        """转换为字典格式."""
        result = {}
        if not self.hard_limit.is_empty():
            result['hard_limit'] = self.hard_limit.to_dict()
        if not self.soft_limit.is_empty():
            result['soft_limit'] = self.soft_limit.to_dict()
        if not self.swap_hard_limit.is_empty():
            result['swap_hard_limit'] = self.swap_hard_limit.to_dict()
        if not self.min_guarantee.is_empty():
            result['min_guarantee'] = self.min_guarantee.to_dict()
        return result

    def is_empty(self) -> bool:
        """检查配置是否为空."""
        return (
            self.hard_limit.is_empty()
            and self.soft_limit.is_empty()
            and self.swap_hard_limit.is_empty()
            and self.min_guarantee.is_empty()
        )
