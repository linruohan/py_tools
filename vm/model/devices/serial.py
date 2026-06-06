"""Serial 设备配置 - 整合策略模式."""

from dataclasses import dataclass
from typing import Any


@dataclass
class Serial:
    """Serial (串口) 设备配置"""

    type: str = 'pty'  # pty, file, dev, null, udp, tcp, unix, pipe, nmdm, spicevmc
    source_path: str | None = None  # 源路径
    source_mode: str | None = None  # 源模式 (bind, connect)
    source_host: str | None = None  # 源主机
    source_service: str | None = None  # 源服务
    source_tty: str | None = None  # TTY 设备
    target_type: str | None = None  # 目标类型
    target_port: str | None = None  # 目标端口
    target_path: str | None = None  # 目标路径
    log_file: str | None = None  # 日志文件
    protocol: str | None = None  # 协议 (raw, telnet)
    telnet_interface: str | None = None  # Telnet 接口
    address: dict[str, str] | None = None  # 设备地址

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'Serial':
        """从字典创建"""
        return cls(
            type=data.get('type', 'pty'),
            source_path=data.get('source_path'),
            source_mode=data.get('source_mode'),
            source_host=data.get('source_host'),
            source_service=data.get('source_service'),
            source_tty=data.get('source_tty'),
            target_type=data.get('target_type'),
            target_port=data.get('target_port'),
            target_path=data.get('target_path'),
            log_file=data.get('log_file'),
            protocol=data.get('protocol'),
            telnet_interface=data.get('telnet_interface'),
            address=data.get('address'),
        )

    def to_dict(self) -> dict[str, Any]:
        """转换为字典"""
        return {
            'type': self.type,
            'source_path': self.source_path,
            'source_mode': self.source_mode,
            'source_host': self.source_host,
            'source_service': self.source_service,
            'source_tty': self.source_tty,
            'target_type': self.target_type,
            'target_port': self.target_port,
            'target_path': self.target_path,
            'log_file': self.log_file,
            'protocol': self.protocol,
            'telnet_interface': self.telnet_interface,
            'address': self.address,
        }
