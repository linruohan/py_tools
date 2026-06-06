from dataclasses import dataclass
from typing import Any


@dataclass
class AccessMode:
    """访问模式配置"""

    type: str  # passthrough, mapped, squashed


@dataclass
class Source:
    """文件系统源配置"""

    dir: str | None = None  # 本地目录
    name: str | None = None  # 共享名称
    protocol: str | None = None  # 协议
    host: str | None = None  # 主机
    port: int | None = None  # 端口
    socket: str | None = None  # 套接字


@dataclass
class Filesystem:
    """Filesystem 设备配置"""

    type: str = 'mount'  # mount, template, trans
    access_mode: AccessMode | None = None
    source: Source | None = None
    target: str = 'mount_tag'  # 挂载标签
    readonly: bool | None = None  # 只读
    driver: dict[str, Any] | None = None  # 驱动配置
    qemu_security_model: str | None = None  # QEMU 安全模型
    selinux_relabel: bool | None = None  # SELinux 重标签
    mdev: str | None = None  # 设备名称
    pool: str | None = None  # 存储池
    volume: str | None = None  # 卷
    format: str | None = None  # 格式
    snapshots: bool | None = None  # 快照
    shared: bool | None = None  # 共享
    copy_on_read: bool | None = None  # 读时复制
    address: dict[str, Any] | None = None  # 设备地址

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'Filesystem':
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

    def to_dict(self) -> dict[str, Any]:
        """转换为字典"""
        # 处理 source 可能是字符串或 Source 对象
        source_val = self.source
        if isinstance(source_val, str):
            # 字符串格式，直接作为 dir
            source_dict = {'dir': source_val}
        elif source_val:
            # Source 对象格式
            source_dict = source_val.__dict__
        else:
            source_dict = None

        # 处理 access_mode 可能是字符串或 AccessMode 对象
        access_mode_val = self.access_mode
        if isinstance(access_mode_val, str):
            # 字符串格式，直接作为 type
            access_mode_dict = {'type': access_mode_val}
        elif access_mode_val:
            # AccessMode 对象格式
            access_mode_dict = access_mode_val.__dict__
        else:
            access_mode_dict = None

        return {
            'type': self.type,
            'access_mode': access_mode_dict,
            'source': source_dict,
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
