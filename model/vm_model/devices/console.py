"""Console 设备配置 - 整合策略模式."""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List


@dataclass
class Console:
    """Console 设备配置"""

    target_type: Optional[str] = None  # 目标类型
    target_port: Optional[str] = None  # 目标端口
    source_path: Optional[str] = None  # 源路径
    source_mode: Optional[str] = None  # 源模式
    source_host: Optional[str] = None  # 源主机
    source_service: Optional[str] = None  # 源服务
    type: str = 'pty'  # pty, file, dev, null, udp, tcp, unix, spicevmc, nmdm
    log_file: Optional[str] = None  # 日志文件
    protocol: Optional[str] = None  # 协议类型
    tty: Optional[str] = None  # TTY 设备
    prefix: Optional[str] = None  # 前缀
    address: Optional[Dict[str, str]] = None  # 设备地址

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Console':
        """从字典创建"""
        return cls(
            target_type=data.get('target_type'),
            target_port=data.get('target_port'),
            source_path=data.get('source_path'),
            source_mode=data.get('source_mode'),
            source_host=data.get('source_host'),
            source_service=data.get('source_service'),
            type=data.get('type', 'pty'),
            log_file=data.get('log_file'),
            protocol=data.get('protocol'),
            tty=data.get('tty'),
            prefix=data.get('prefix'),
            address=data.get('address'),
        )

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'target_type': self.target_type,
            'target_port': self.target_port,
            'source_path': self.source_path,
            'source_mode': self.source_mode,
            'source_host': self.source_host,
            'source_service': self.source_service,
            'type': self.type,
            'log_file': self.log_file,
            'protocol': self.protocol,
            'tty': self.tty,
            'prefix': self.prefix,
            'address': self.address,
        }
