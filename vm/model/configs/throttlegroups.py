from dataclasses import dataclass, field


@dataclass
class ThrottleGroup:
    """节流组配置"""

    name: str
    total_bytes_sec: int | None = None
    read_bytes_sec: int | None = None
    write_bytes_sec: int | None = None
    read_iops_sec: int | None = None
    write_iops_sec: int | None = None
    total_iops_sec: int | None = None


@dataclass
class ThrottleGroups:
    """节流组集合配置"""

    throttlegroups: list[ThrottleGroup] = field(default_factory=list)
