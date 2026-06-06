from dataclasses import dataclass, field


@dataclass
class HugePage:
    """大页内存配置"""

    size: int
    unit: str | None = None  # KiB, MiB, GiB, TiB
    nodeset: str | None = None


@dataclass
class MemoryBacking:
    """内存后端配置"""

    hugepages: list[HugePage] = field(default_factory=list)
    nosharepages: bool | None = None
    locked: bool | None = None
    source_type: str | None = None  # file, anonymous, memfd
    access_mode: str | None = None  # shared, private
    allocation_mode: str | None = None  # immediate, ondemand
    allocation_threads: int | None = None
    discard: bool | None = None
