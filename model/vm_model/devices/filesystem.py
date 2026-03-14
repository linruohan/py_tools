from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


@dataclass
class AccessMode:
    """访问模式配置"""

    type: str  # passthrough, mapped, squashed


@dataclass
class Source:
    """文件系统源配置"""

    dir: Optional[str] = None  # 本地目录
    name: Optional[str] = None  # 共享名称
    protocol: Optional[str] = None  # 协议
    host: Optional[str] = None  # 主机
    port: Optional[int] = None  # 端口
    socket: Optional[str] = None  # 套接字


@dataclass
class Filesystem:
    """Filesystem 设备配置"""

    type: str = 'mount'  # mount, template, trans
    access_mode: Optional[AccessMode] = None
    source: Optional[Source] = None
    target: str = 'mount_tag'  # 挂载标签
    readonly: Optional[bool] = None  # 只读
    driver: Optional[Dict[str, Any]] = None  # 驱动配置
    qemu_security_model: Optional[str] = None  # QEMU 安全模型
    selinux_relabel: Optional[bool] = None  # SELinux 重标签
    mdev: Optional[str] = None  # 设备名称
    pool: Optional[str] = None  # 存储池
    volume: Optional[str] = None  # 卷
    format: Optional[str] = None  # 格式
    snapshots: Optional[bool] = None  # 快照
    shared: Optional[bool] = None  # 共享
    copy_on_read: Optional[bool] = None  # 读时复制
    address: Optional[Dict[str, Any]] = None  # 设备地址

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Filesystem':
        """从字典创建"""
        access_mode = data.get('access_mode')
        if access_mode and isinstance(access_mode, dict):
            access_mode = AccessMode(**access_mode)

        source = data.get('source')
        if source and isinstance(source, dict):
            source = Source(**source)

        return cls(
            type=data.get('type', 'mount'),
            access_mode=access_mode,
            source=source,
            target=data.get('target', 'mount_tag'),
            readonly=data.get('readonly'),
            driver=data.get('driver'),
            qemu_security_model=data.get('qemu_security_model'),
            selinux_relabel=data.get('selinux_relabel'),
            mdev=data.get('mdev'),
            pool=data.get('pool'),
            volume=data.get('volume'),
            format=data.get('format'),
            snapshots=data.get('snapshots'),
            shared=data.get('shared'),
            copy_on_read=data.get('copy_on_read'),
            address=data.get('address'),
        )

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'type': self.type,
            'access_mode': self.access_mode.__dict__ if self.access_mode else None,
            'source': self.source.__dict__ if self.source else None,
            'target': self.target,
            'readonly': self.readonly,
            'driver': self.driver,
            'qemu_security_model': self.qemu_security_model,
            'selinux_relabel': self.selinux_relabel,
            'mdev': self.mdev,
            'pool': self.pool,
            'volume': self.volume,
            'format': self.format,
            'snapshots': self.snapshots,
            'shared': self.shared,
            'copy_on_read': self.copy_on_read,
            'address': self.address,
        }

