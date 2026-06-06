"""密钥包装配置类 - Key Wrap Configuration."""

from dataclasses import dataclass


@dataclass
class KeyWrapConfig:
    """密钥包装配置管理类.

    用于 S390 平台的加密密钥管理操作配置。
    """

    aes_cipher: str = 'aes'
    aes_state: str = 'None'  # 默认不输出
    dea_cipher: str = 'dea'
    dea_state: str = 'None'  # 默认不输出

    def to_dict(self) -> dict:
        """转换为字典格式.

        Returns:
            配置字典
        """
        result = {}

        # 输出所有 cipher 配置，包括 state='off'
        # 当 state='None' 或 None 时，不输出该 cipher
        ciphers = []
        # AES - state='None' 或 None 时不输出
        if self.aes_state not in ('None', None, ''):
            ciphers.append(
                {
                    'name': self.aes_cipher,
                    'state': self.aes_state,
                }
            )
        # DEA - state='None' 或 None 时不输出
        if self.dea_state not in ('None', None, ''):
            ciphers.append(
                {
                    'name': self.dea_cipher,
                    'state': self.dea_state,
                }
            )

        if ciphers:
            result['cipher'] = ciphers

        return result

    def from_dict(self, data: dict) -> None:
        """从字典加载配置.

        Args:
            data: 配置字典
        """
        if 'cipher' in data:
            cipher_list = data['cipher']
            if isinstance(cipher_list, list):
                for cipher in cipher_list:
                    if isinstance(cipher, dict):
                        name = cipher.get('name', '')
                        state = cipher.get('state', 'on')
                        if name == 'aes':
                            self.aes_cipher = 'aes'
                            self.aes_state = state
                        elif name == 'dea':
                            self.dea_cipher = 'dea'
                            self.dea_state = state
            elif isinstance(cipher_list, dict):
                # 单个 cipher 配置
                cipher = cipher_list
                name = cipher.get('name', '')
                state = cipher.get('state', 'on')
                if name == 'aes':
                    self.aes_cipher = 'aes'
                    self.aes_state = state
                elif name == 'dea':
                    self.dea_cipher = 'dea'
                    self.dea_state = state

    def is_enabled(self) -> bool:
        """检查是否启用了密钥包装."""
        return self.aes_state in ('on', 'off') or self.dea_state in ('on', 'off')

    def has_cipher_config(self) -> bool:
        """检查是否有 cipher 配置（排除 'None' 和 None）。"""
        # 当 state 不是 'None'、None 或空字符串时，认为有配置
        return self.aes_state not in ('None', None, '') or self.dea_state not in ('None', None, '')
