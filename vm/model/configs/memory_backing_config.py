"""内存后端配置数据类."""

from dataclasses import dataclass, field


@dataclass
class HugepageItem:
    """Hugepage 配置项."""

    size: str | None = None  # 页面大小
    unit: str = 'GiB'  # 单位：KiB, MiB, GiB
    nodeset: str | None = None  # 节点集

    def update(self, data: dict) -> None:
        """更新配置."""
        if 'size' in data:
            self.size = data['size']
        if 'unit' in data:
            self.unit = data['unit']
        if 'nodeset' in data:
            self.nodeset = data['nodeset']

    def to_dict(self) -> dict:
        """转换为字典格式."""
        result = {}
        if self.size:
            result['size'] = self.size
            result['unit'] = self.unit
            if self.nodeset:
                result['nodeset'] = self.nodeset
        return result

    @classmethod
    def from_dict(cls, data: dict) -> 'HugepageItem':
        """从字典创建实例."""
        return cls(
            size=data.get('size'),
            unit=data.get('unit', 'GiB'),
            nodeset=data.get('nodeset'),
        )

    def is_empty(self) -> bool:
        """检查配置是否为空."""
        return not self.size


@dataclass
class MemoryBackingConfig:
    """内存后端配置类."""

    hugepages: list[HugepageItem] = field(default_factory=list)
    source_type: str = 'anonymous'  # anonymous, file, memfd
    access_mode: str = 'private'  # private, shared
    allocation_mode: str = 'ondemand'  # immediate, ondemand
    allocation_threads: str | None = None
    nosharepages: bool = False
    locked: bool = False
    discard: bool = False

    def update(self, data: dict) -> None:
        """更新配置."""
        if 'hugepages' in data and isinstance(data['hugepages'], list):
            self.hugepages = [HugepageItem.from_dict(hp) for hp in data['hugepages']]
        if data.get('source_type'):
            self.source_type = data['source_type']
        if data.get('access_mode'):
            self.access_mode = data['access_mode']
        if data.get('allocation_mode'):
            self.allocation_mode = data['allocation_mode']
        if 'allocation_threads' in data:
            self.allocation_threads = data['allocation_threads'] or None
        if 'nosharepages' in data:
            self.nosharepages = bool(data['nosharepages'])
        if 'locked' in data:
            self.locked = bool(data['locked'])
        if 'discard' in data:
            self.discard = bool(data['discard'])

    def to_dict(self) -> dict:
        """转换为字典格式."""
        result = {}

        # Hugepages - 只添加非空条目
        hugepages_list = [hp.to_dict() for hp in self.hugepages if not hp.is_empty()]
        if hugepages_list:
            result['hugepages'] = hugepages_list

        # source_type - 'anonymous' 为默认值，不生成 XML
        if self.source_type and self.source_type != 'anonymous':
            result['source_type'] = self.source_type

        # access_mode - 只有非默认值才生成
        if self.access_mode and self.access_mode != 'private':
            result['access_mode'] = self.access_mode

        # allocation_mode - 只有非默认值才生成
        if self.allocation_mode and self.allocation_mode != 'ondemand':
            result['allocation_mode'] = self.allocation_mode

        # allocation_threads - 只有有值时才生成
        if self.allocation_threads:
            result['allocation_threads'] = self.allocation_threads

        # Boolean 选项
        if self.nosharepages:
            result['nosharepages'] = True
        if self.locked:
            result['locked'] = True
        if self.discard:
            result['discard'] = True

        return result

    def is_empty(self) -> bool:
        """检查配置是否为空."""
        # 检查是否有任何非默认配置
        has_hugepages = any(not hp.is_empty() for hp in self.hugepages)
        return (
            not has_hugepages
            and self.source_type == 'anonymous'
            and self.access_mode == 'private'
            and self.allocation_mode == 'ondemand'
            and not self.allocation_threads
            and not self.nosharepages
            and not self.locked
            and not self.discard
        )
