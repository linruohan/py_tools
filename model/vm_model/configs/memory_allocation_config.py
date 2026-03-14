"""内存分配配置类 - 管理虚拟机内存分配配置信息."""


class MemoryAllocationConfig:
    """内存分配配置类."""

    def __init__(self):
        """初始化内存分配配置."""
        self.memory = 2097152  # KiB
        self.current_memory = 2097152  # KiB
        self.max_memory = 4194304  # KiB
        self.unit = 'KiB'
        self.memory_slots = 16

    def update(self, data: dict) -> None:
        """更新配置.

        Args:
            data: 配置数据
        """
        if 'memory' in data:
            self.memory = data['memory']
        if 'current_memory' in data:
            self.current_memory = data['current_memory']
        if 'max_memory' in data:
            self.max_memory = data['max_memory']
        if 'unit' in data:
            self.unit = data['unit']
        if 'memory_slots' in data:
            self.memory_slots = data['memory_slots']

    def to_dict(self) -> dict:
        """转换为字典格式.

        Returns:
            配置字典
        """
        return {
            'memory': self.memory,
            'current_memory': self.current_memory,
            'max_memory': self.max_memory,
            'unit': self.unit,
            'memory_slots': self.memory_slots,
        }
