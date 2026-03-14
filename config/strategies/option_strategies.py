"""选项策略枚举类型定义"""

from enum import StrEnum


class DiskBusType(StrEnum):
    """磁盘总线类型"""

    IDE = 'ide'
    SCSI = 'scsi'
    VIRTIO = 'virtio'
    SATA = 'sata'
    USB = 'usb'
    FC = 'fc'
    ISCSI = 'iscsi'
    NVME = 'nvme'


class DiskType(StrEnum):
    """磁盘类型"""

    RAW = 'raw'
    QCOW2 = 'qcow2'
    VMDK = 'vmdk'
    VHD = 'vhd'
    VHDX = 'vhdx'
    QED = 'qed'
    LVM = 'lvm'


class CacheMode(StrEnum):
    """缓存模式"""

    NONE = 'none'
    WRITEBACK = 'writeback'
    WRITETHROUGH = 'writethrough'
    DIRECTSYNC = 'directsync'
    UNSAFE = 'unsafe'
    WRITEBACK_PARENT = 'writeback-parent'


class GraphicsType(StrEnum):
    """图形类型"""

    VNC = 'vnc'
    SPICE = 'spice'
    SDL = 'sdl'
    RDP = 'rdp'
    GTK = 'gtk'
    CURSES = 'curses'


class VideoModel(StrEnum):
    """视频模型"""

    QXL = 'qxl'
    VGA = 'vga'
    CIRRUS = 'cirrus'
    VMVGA = 'vmvga'
    VIRTIO = 'virtio'
    BOCHS = 'bochs'
    RAMFB = 'ramfb'


class FirmwareType(StrEnum):
    """固件类型"""

    BIOS = 'bios'
    EFI = 'efi'


class MemoryUnit(StrEnum):
    """内存单位"""

    B = 'b'
    BYTES = 'bytes'
    KB = 'KB'
    K = 'k'
    KIB = 'KiB'
    MB = 'MB'
    M = 'M'
    MIB = 'MiB'
    GB = 'GB'
    G = 'G'
    GIB = 'GiB'
    TB = 'TB'
    T = 'T'
    TIB = 'TiB'
