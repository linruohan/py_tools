"""Serial 设备配置 - 整合策略模式."""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List


@dataclass
class Serial:
    """Serial (串口) 设备配置"""

    type: str = 'pty'  # pty, file, dev, null, udp, tcp, unix, pipe, nmdm, spicevmc
    source_path: Optional[str] = None  # 源路径
    source_mode: Optional[str] = None  # 源模式 (bind, connect)
    source_host: Optional[str] = None  # 源主机
    source_service: Optional[str] = None  # 源服务
    source_tty: Optional[str] = None  # TTY 设备
    target_type: Optional[str] = None  # 目标类型
    target_port: Optional[str] = None  # 目标端口
    target_path: Optional[str] = None  # 目标路径
    log_file: Optional[str] = None  # 日志文件
    protocol: Optional[str] = None  # 协议 (raw, telnet)
    telnet_interface: Optional[str] = None  # Telnet 接口
    address: Optional[Dict[str, str]] = None  # 设备地址

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Serial':
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

    def to_dict(self) -> Dict[str, Any]:
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
