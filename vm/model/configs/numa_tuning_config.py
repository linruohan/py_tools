"""NUMA 节点调优配置数据模型."""

from dataclasses import dataclass, field


@dataclass
class MemNode:
    """内存节点配置"""

    cellid: str = ''
    mode: str | None = None  # strict, preferred, interleave, restrictive
    nodeset: str | None = None


@dataclass
class NumaTuneConfig:
    """NUMA 节点调优配置"""

    memory_mode: str | None = None  # strict, preferred, interleave, restrictive, None
    memory_nodeset: str | None = None
    memory_placement: str | None = None  # static, auto, None
    memnodes: list[MemNode] = field(default_factory=list)

    def is_empty(self) -> bool:
        """检查是否为空配置."""
        if self.memory_mode and self.memory_mode != 'None':
            return False
        if self.memory_nodeset:
            return False
        if self.memory_placement and self.memory_placement != 'None':
            return False
        if self.memnodes:
            return False
        return True

    def to_dict(self) -> dict:
        """转换为字典格式."""
        result = {}

        if self.memory_mode and self.memory_mode != 'None':
            result['memory_mode'] = self.memory_mode
        if self.memory_nodeset:
            result['memory_nodeset'] = self.memory_nodeset
        if self.memory_placement and self.memory_placement != 'None':
            result['memory_placement'] = self.memory_placement

        if self.memnodes:
            result['memnodes'] = [
                {
                    'cellid': node.cellid,
                    'mode': node.mode,
                    'nodeset': node.nodeset,
                }
                for node in self.memnodes
                if node.cellid  # 只包含有 cellid 的节点
            ]

        return result

    @classmethod
    def from_dict(cls, data: dict) -> 'NumaTuneConfig':
        """从字典创建配置."""
        config = cls()

        config.memory_mode = data.get('memory_mode')
        config.memory_nodeset = data.get('memory_nodeset')
        config.memory_placement = data.get('memory_placement')

        memnodes_data = data.get('memnodes', [])
        for node_data in memnodes_data:
            node = MemNode(
                cellid=str(node_data.get('cellid', '')),
                mode=node_data.get('mode'),
                nodeset=node_data.get('nodeset'),
            )
            config.memnodes.append(node)

        return config
