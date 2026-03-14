"""CPU 拓扑配置类."""

from dataclasses import dataclass


@dataclass
class CPUTopology:
    """CPU 拓扑配置.

    Attributes:
        sockets: socket 数量
        dies: die 数量 (仅 cpu_allocation 使用)
        clusters: cluster 数量 (仅 cpu_allocation 使用)
        cores: 每 socket 核心数
        threads: 每核心线程数
    """

    sockets: int = 1
    dies: int = 1
    clusters: int = 1
    cores: int = 2
    threads: int = 1

    @classmethod
    def from_dict(cls, data: dict, fields: list[str] | None = None) -> 'CPUTopology':
        """从字典创建 CPU 拓扑.

        Args:
            data: 包含配置数据的字典
            fields: 要使用的字段列表,如果为 None 则使用所有定义的字段

        Returns:
            CPUTopology 实例
        """
        if fields is None:
            fields = list(cls.__dataclass_fields__.keys())
        return cls(**{k: v for k, v in data.items() if k in fields})

    def to_dict(self, fields: list[str] | None = None) -> dict:
        """转换为字典.

        Args:
            fields: 要导出的字段列表,如果为 None 则导出所有字段

        Returns:
            包含配置数据的字典
        """
        if fields is None:
            fields = list(self.__dataclass_fields__.keys())
        return {k: getattr(self, k) for k in fields}

    @classmethod
    def basic_topology(cls, sockets: int = 1, cores: int = 2, threads: int = 1) -> 'CPUTopology':
        """创建基础 CPU 拓扑 (仅 sockets/cores/threads).

        Args:
            sockets: socket 数量
            cores: 每 socket 核心数
            threads: 每核心线程数

        Returns:
            CPUTopology 实例
        """
        return cls(sockets=sockets, cores=cores, threads=threads)

    @classmethod
    def full_topology(
        cls,
        sockets: int = 1,
        dies: int = 1,
        clusters: int = 1,
        cores: int = 2,
        threads: int = 1,
    ) -> 'CPUTopology':
        """创建完整 CPU 拓扑 (包含所有字段).

        Args:
            sockets: socket 数量
            dies: die 数量
            clusters: cluster 数量
            cores: 每 socket 核心数
            threads: 每核心线程数

        Returns:
            CPUTopology 实例
        """
        return cls(
            sockets=sockets,
            dies=dies,
            clusters=clusters,
            cores=cores,
            threads=threads,
        )
