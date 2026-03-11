
from dataclasses import dataclass, field


@dataclass
class GraphicsConfig:
    """图形协议配置"""

    type: str = 'vnc'  # vnc, spice
    port: str = '5900'
    listen: str = '127.0.0.1'
    password: str | None = None
    keymap: str = 'en-us'


@dataclass
class DiskDevice:
    """磁盘设备"""

    device_type: str = 'file'  # file, block, network
    device: str = 'disk'  # disk, cdrom, floppy
    driver_name: str = 'qemu'
    driver_type: str = 'qcow2'  # raw, qcow2, ...
    source_file: str = ''
    bus: str = 'virtio'  # virtio, ide, sata, scsi
    target_dev: str = ''  # 自动生成 vda, vdb...
    readonly: bool = False


@dataclass
class NetDevice:
    """网络设备"""

    model: str = 'virtio'
    network_type: str = 'bridge'  # bridge, network, user
    source_bridge: str = 'br0'  # 桥接模式
    source_network: str = 'default'  # 虚拟网络模式
    mac_addr: str = ''  # 自动生成


@dataclass
class VmConfig:
    """虚拟机主配置"""

    name: str = 'guest'
    uuid: str = ''  # 留空自动生成
    memory_mb: int = 1024
    vcpu: int = 1
    cpu_mode: str = 'host-passthrough'  # host-passthrough, host-model, custom
    firmware: str = 'bios'  # bios, uefi
    boot_order: list[str] = field(default_factory=lambda: ['hd', 'cdrom'])
    disks: list[DiskDevice] = field(default_factory=list)
    networks: list[NetDevice] = field(default_factory=list)
    graphics: GraphicsConfig | None = None
    # 可扩展更多设备：控制器、USB、串口等
