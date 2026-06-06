"""S390 密钥包装配置 - Key Wrap."""

from dataclasses import dataclass


@dataclass
class Cipher:
    """加密算法配置.

    Attributes:
        name: 算法名称 (aes 或 dea)
        state: 状态 (on 或 off)
    """

    name: str = 'aes'
    state: str = 'on'

    def to_dict(self) -> dict:
        """转换为字典格式."""
        return {
            'name': self.name,
            'state': self.state,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Cipher':
        """从字典创建实例.

        Args:
            data: 配置字典

        Returns:
            Cipher 实例
        """
        return cls(
            name=data.get('name', 'aes'),
            state=data.get('state', 'on'),
        )


@dataclass
class KeyWrap:
    """S390 密钥包装配置.

    用于指定 guest 是否可以执行 S390 加密密钥管理操作。
    明文密钥可以通过在唯一包装密钥下加密来保护，该密钥为每个 guest VM 生成。

    Attributes:
        aes: AES 包装密钥配置
        dea: DEA/TDEA 包装密钥配置
    """

    aes: Cipher | None = None
    dea: Cipher | None = None

    def to_dict(self) -> dict:
        """转换为字典格式."""
        result = {}
        if self.aes:
            result['aes'] = self.aes.to_dict()
        if self.dea:
            result['dea'] = self.dea.to_dict()
        return result

    @classmethod
    def from_dict(cls, data: dict) -> 'KeyWrap':
        """从字典创建实例.

        Args:
            data: 配置字典

        Returns:
            KeyWrap 实例
        """
        aes = None
        dea = None

        if 'aes' in data:
            aes_data = data['aes']
            if isinstance(aes_data, dict):
                aes = Cipher.from_dict(aes_data)
            elif isinstance(aes_data, str):
                aes = Cipher(name='aes', state=aes_data)

        if 'dea' in data:
            dea_data = data['dea']
            if isinstance(dea_data, dict):
                dea = Cipher.from_dict(dea_data)
            elif isinstance(dea_data, str):
                dea = Cipher(name='dea', state=dea_data)

        return cls(aes=aes, dea=dea)

    def is_enabled(self) -> bool:
        """检查是否启用了密钥包装."""
        return self.aes is not None or self.dea is not None
