"""Domain 模型 - 整合 Config 策略模式的 libvirt domain 配置."""

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any, TypeVar

# 引入策略模式
from config.strategies.option_strategies import (
    CacheMode,
    DiskBusType,
    DiskType,
    FirmwareType,
    GraphicsType,
    MemoryUnit,
    VideoModel,
)

# 引入 NUMA 配置
from ..cpu.numa import NUMA

# ========== 类型定义 ==========

T = TypeVar('T')


class VirtType(StrEnum):
    """虚拟化类型"""

    KVM = 'kvm'
    QEMU = 'qemu'
    XEN = 'xen'
    HVF = 'hvf'
    LXC = 'lxc'
    UML = 'uml'
    OPENVZ = 'openvz'
    VZ = 'vz'


class OSType(StrEnum):
    """OS 类型"""

    HVM = 'hvm'
    LINUX = 'linux'
    EXE = 'exe'
    UML = 'uml'
    OS = 'os'
    PVM = 'pvm'


class MachineType(StrEnum):
    """机型类型"""

    Q35 = 'q35'
    PC = 'pc'
    PC_I440FX = 'pc-i440fx'
    VIRT = 'virt'
    ARM_VIRT = 'arm-virt'


class CpuMode(StrEnum):
    """CPU 模式"""

    CUSTOM = 'custom'
    HOST_MODEL = 'host-model'
    HOST_PASSTHROUGH = 'host-passthrough'
    HOST_MODEL_REQUIRED = 'host-model-required'
    MAXIMUM = 'maximum'


# ========== 基础数据类 ==========


@dataclass
class CPUTopology:
    """CPU 拓扑配置"""

    sockets: int = 1
    cores: int = 2
    threads: int = 1
    dies: int = 1
    clusters: int = 1

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'CPUTopology':
        """从字典创建"""
        return cls(
            sockets=data.get('sockets', 1),
            cores=data.get('cores', 2),
            threads=data.get('threads', 1),
            dies=data.get('dies', 1),
            clusters=data.get('clusters', 1),
        )

    def to_dict(self) -> dict[str, Any]:
        """转换为字典"""
        return {
            'sockets': self.sockets,
            'cores': self.cores,
            'threads': self.threads,
            'dies': self.dies,
            'clusters': self.clusters,
        }


@dataclass
class CPUFeature:
    """CPU 特性"""

    name: str
    policy: str | None = None  # require, optional, disable
    present: bool | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'CPUFeature':
        """从字典创建"""
        return cls(
            name=data.get('name', ''),
            policy=data.get('policy'),
            present=data.get('present'),
        )

    def to_dict(self) -> dict[str, Any]:
        """转换为字典"""
        return {
            'name': self.name,
            'policy': self.policy,
            'present': self.present,
        }


@dataclass
class CPUModel:
    """CPU 模型"""

    name: str
    fallback: str | None = None  # allow, forbid, require
    check: bool | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'CPUModel':
        """从字典创建"""
        return cls(
            name=data.get('name', ''),
            fallback=data.get('fallback'),
            check=data.get('check'),
        )

    def to_dict(self) -> dict[str, Any]:
        """转换为字典"""
        return {
            'name': self.name,
            'fallback': self.fallback,
            'check': self.check,
        }


@dataclass
class CPU:
    """CPU 配置"""

    mode: CpuMode = CpuMode.HOST_MODEL
    model: CPUModel | None = None
    topology: CPUTopology | None = None
    features: list[CPUFeature] = field(default_factory=list)
    match: str | None = None
    vendor_id: str | None = None
    placeholder: bool | None = None
    numa: NUMA | None = None
    cache: dict[str, Any] | None = None
    maxphysaddr: dict[str, Any] | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'CPU':
        """从字典创建"""
        features = data.get('features', [])
        if features and isinstance(features[0], dict):
            features = [CPUFeature.from_dict(f) for f in features]

        topology = data.get('topology')
        if topology and isinstance(topology, dict):
            topology = CPUTopology.from_dict(topology)

        model = data.get('model')
        if model and isinstance(model, dict):
            model = CPUModel.from_dict(model)

        numa = data.get('numa')
        if numa and isinstance(numa, dict):
            # 这里可以根据需要实现 NUMA 从字典创建的逻辑
            pass

        return cls(
            mode=CpuMode(data.get('mode', 'host-model')),
            model=model,
            topology=topology,
            features=features if isinstance(features, list) else [],
            match=data.get('match'),
            vendor_id=data.get('vendor_id'),
            placeholder=data.get('placeholder'),
            numa=numa,
            cache=data.get('cache'),
            maxphysaddr=data.get('maxphysaddr'),
        )

    def to_dict(self) -> dict[str, Any]:
        """转换为字典"""
        return {
            'mode': self.mode.value if isinstance(self.mode, CpuMode) else str(self.mode),
            'model': self.model.to_dict() if self.model else None,
            'topology': self.topology.to_dict() if self.topology else None,
            'features': [f.to_dict() for f in self.features],
            'match': self.match,
            'vendor_id': self.vendor_id,
            'placeholder': self.placeholder,
            'numa': self.numa,
            'cache': self.cache,
            'maxphysaddr': self.maxphysaddr,
        }


@dataclass
class VCPU:
    """VCPU 配置"""

    count: int = 2
    placement: str = 'static'
    cpuset: str | None = None
    current: int | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'VCPU':
        """从字典创建"""
        return cls(
            count=data.get('count', 2),
            placement=data.get('placement', 'static'),
            cpuset=data.get('cpuset'),
            current=data.get('current'),
        )

    def to_dict(self) -> dict[str, Any]:
        """转换为字典"""
        return {
            'count': self.count,
            'placement': self.placement,
            'cpuset': self.cpuset,
            'current': self.current,
        }


@dataclass
class Memory:
    """内存配置"""

    size: int = 2097152  # KiB
    unit: MemoryUnit = MemoryUnit.KIB
    dump_core: bool | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'Memory':
        """从字典创建"""
        unit = data.get('unit', 'KiB')
        if isinstance(unit, str):
            unit = MemoryUnit(unit)

        return cls(
            size=data.get('size', 2097152),
            unit=unit,
            dump_core=data.get('dump_core'),
        )

    def to_dict(self) -> dict[str, Any]:
        """转换为字典"""
        return {
            'size': self.size,
            'unit': self.unit.value,
            'dump_core': self.dump_core,
        }


@dataclass
class MaxMemory:
    """最大内存配置"""

    size: int = 4194304  # KiB
    unit: MemoryUnit = MemoryUnit.KIB
    slots: int | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'MaxMemory':
        """从字典创建"""
        unit = data.get('unit', 'KiB')
        if isinstance(unit, str):
            unit = MemoryUnit(unit)

        return cls(
            size=data.get('size', 4194304),
            unit=unit,
            slots=data.get('slots'),
        )

    def to_dict(self) -> dict[str, Any]:
        """转换为字典"""
        return {
            'size': self.size,
            'unit': self.unit.value,
            'slots': self.slots,
        }


@dataclass
class CurrentMemory:
    """当前内存配置"""

    size: int = 2097152  # KiB
    unit: MemoryUnit = MemoryUnit.KIB

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'CurrentMemory':
        """从字典创建"""
        unit = data.get('unit', 'KiB')
        if isinstance(unit, str):
            unit = MemoryUnit(unit)

        return cls(
            size=data.get('size', 2097152),
            unit=unit,
        )

    def to_dict(self) -> dict[str, Any]:
        """转换为字典"""
        return {
            'size': self.size,
            'unit': self.unit.value,
        }


@dataclass
class Boot:
    """引导设备配置"""

    dev: str  # fd, hd, cdrom, network

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'Boot':
        """从字典创建"""
        return cls(dev=data.get('dev', 'hd'))

    def to_dict(self) -> dict[str, Any]:
        """转换为字典"""
        return {'dev': self.dev}


@dataclass
class Bootmenu:
    """引导菜单配置"""

    enable: bool = False
    timeout: int | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'Bootmenu':
        """从字典创建"""
        return cls(
            enable=data.get('enable', False),
            timeout=data.get('timeout'),
        )

    def to_dict(self) -> dict[str, Any]:
        """转换为字典"""
        return {
            'enable': self.enable,
            'timeout': self.timeout,
        }


@dataclass
class Loader:
    """引导加载器配置"""

    path: str | None = None
    readonly: bool | None = None
    secure: bool | None = None
    type: str | None = None  # rom or pflash
    stateless: bool | None = None
    format: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'Loader':
        """从字典创建"""
        return cls(
            path=data.get('path'),
            readonly=data.get('readonly'),
            secure=data.get('secure'),
            type=data.get('type'),
            stateless=data.get('stateless'),
            format=data.get('format'),
        )

    def to_dict(self) -> dict[str, Any]:
        """转换为字典"""
        return {
            'path': self.path,
            'readonly': self.readonly,
            'secure': self.secure,
            'type': self.type,
            'stateless': self.stateless,
            'format': self.format,
        }


@dataclass
class Nvram:
    """NVRAM 配置"""

    path: str | None = None
    template: str | None = None
    template_format: str | None = None
    type: str | None = None
    source: dict[str, Any] | None = None
    format: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'Nvram':
        """从字典创建"""
        return cls(
            path=data.get('path'),
            template=data.get('template'),
            template_format=data.get('template_format'),
            type=data.get('type'),
            source=data.get('source'),
            format=data.get('format'),
        )

    def to_dict(self) -> dict[str, Any]:
        """转换为字典"""
        return {
            'path': self.path,
            'template': self.template,
            'template_format': self.template_format,
            'type': self.type,
            'source': self.source,
            'format': self.format,
        }


@dataclass
class OS:
    """操作系统配置"""

    type: OSType = OSType.HVM
    arch: str = 'x86_64'
    machine: MachineType = MachineType.Q35
    firmware: FirmwareType = FirmwareType.BIOS
    firmware_features: list[dict[str, Any]] = field(default_factory=list)
    loader: Loader | None = None
    nvram: Nvram | None = None
    varstore: dict[str, Any] | None = None
    boot: list[Boot] = field(default_factory=list)
    bootmenu: Bootmenu | None = None
    smbios: dict[str, Any] | None = None
    bios: dict[str, Any] | None = None
    kernel: str | None = None
    initrd: str | None = None
    cmdline: str | None = None
    shim: str | None = None
    dtb: str | None = None
    init: str | None = None
    initargs: list[str] = field(default_factory=list)
    initenv: list[dict[str, Any]] = field(default_factory=list)
    initdir: str | None = None
    inituser: str | None = None
    initgroup: str | None = None
    idmap: dict[str, Any] | None = None
    acpi: dict[str, Any] | None = None
    bootloader: str | None = None
    bootloader_args: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'OS':
        """从字典创建"""
        boot = data.get('boot', [])
        if boot and isinstance(boot[0], dict):
            boot = [Boot.from_dict(b) for b in boot]

        loader = data.get('loader')
        if loader and isinstance(loader, dict):
            loader = Loader.from_dict(loader)

        nvram = data.get('nvram')
        if nvram and isinstance(nvram, dict):
            nvram = Nvram.from_dict(nvram)

        bootmenu = data.get('bootmenu')
        if bootmenu and isinstance(bootmenu, dict):
            bootmenu = Bootmenu.from_dict(bootmenu)

        firmware = data.get('firmware', 'bios')
        if isinstance(firmware, str):
            firmware = FirmwareType(firmware)

        os_type = data.get('type', 'hvm')
        if isinstance(os_type, str):
            os_type = OSType(os_type)

        machine = data.get('machine', 'q35')
        if isinstance(machine, str):
            machine = MachineType(machine)

        return cls(
            type=os_type,
            arch=data.get('arch', 'x86_64'),
            machine=machine,
            firmware=firmware,
            firmware_features=data.get('firmware_features', []),
            loader=loader,
            nvram=nvram,
            varstore=data.get('varstore'),
            boot=boot,
            bootmenu=bootmenu,
            smbios=data.get('smbios'),
            bios=data.get('bios'),
            kernel=data.get('kernel'),
            initrd=data.get('initrd'),
            cmdline=data.get('cmdline'),
            shim=data.get('shim'),
            dtb=data.get('dtb'),
            init=data.get('init'),
            initargs=data.get('initargs', []),
            initenv=data.get('initenv', []),
            initdir=data.get('initdir'),
            inituser=data.get('inituser'),
            initgroup=data.get('initgroup'),
            idmap=data.get('idmap'),
            acpi=data.get('acpi'),
            bootloader=data.get('bootloader'),
            bootloader_args=data.get('bootloader_args'),
        )

    def to_dict(self) -> dict[str, Any]:
        """转换为字典"""
        return {
            'type': self.type.value,
            'arch': self.arch,
            'machine': self.machine.value,
            'firmware': self.firmware.value,
            'firmware_features': self.firmware_features,
            'loader': self.loader.to_dict() if self.loader else None,
            'nvram': self.nvram.to_dict() if self.nvram else None,
            'varstore': self.varstore,
            'boot': [b.to_dict() for b in self.boot],
            'bootmenu': self.bootmenu.to_dict() if self.bootmenu else None,
            'smbios': self.smbios,
            'bios': self.bios,
            'kernel': self.kernel,
            'initrd': self.initrd,
            'cmdline': self.cmdline,
            'shim': self.shim,
            'dtb': self.dtb,
            'init': self.init,
            'initargs': self.initargs,
            'initenv': self.initenv,
            'initdir': self.initdir,
            'inituser': self.inituser,
            'initgroup': self.initgroup,
            'idmap': self.idmap,
            'acpi': self.acpi,
            'bootloader': self.bootloader,
            'bootloader_args': self.bootloader_args,
        }


@dataclass
class Disk:
    """磁盘设备配置"""

    type: DiskType = DiskType.QCOW2
    device: str = 'disk'  # disk, cdrom, floppy, lun
    bus: DiskBusType = DiskBusType.VIRTIO
    target: str = 'vda'
    driver: str | None = None
    cache: CacheMode = CacheMode.NONE
    io: str | None = None
    discard: str | None = None
    detect_zeroes: bool | None = None
    source_file: str | None = None
    source_protocol: str | None = None
    source_dev: str | None = None
    snapshot: str | None = None  # on, off
    readonly: bool = False
    shareable: bool = False
    transient: bool = False
    capacity: int | None = None
    allocation: int | None = None
    physical: int | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'Disk':
        """从字典创建"""
        disk_type = data.get('type', 'qcow2')
        if isinstance(disk_type, str):
            disk_type = DiskType(disk_type)

        bus = data.get('bus', 'virtio')
        if isinstance(bus, str):
            bus = DiskBusType(bus)

        cache = data.get('cache', 'none')
        if isinstance(cache, str):
            cache = CacheMode(cache)

        return cls(
            type=disk_type,
            device=data.get('device', 'disk'),
            bus=bus,
            target=data.get('target', 'vda'),
            driver=data.get('driver'),
            cache=cache,
            io=data.get('io'),
            discard=data.get('discard'),
            detect_zeroes=data.get('detect_zeroes'),
            source_file=data.get('source_file'),
            source_protocol=data.get('source_protocol'),
            source_dev=data.get('source_dev'),
            snapshot=data.get('snapshot'),
            readonly=data.get('readonly', False),
            shareable=data.get('shareable', False),
            transient=data.get('transient', False),
            capacity=data.get('capacity'),
            allocation=data.get('allocation'),
            physical=data.get('physical'),
        )

    def to_dict(self) -> dict[str, Any]:
        """转换为字典"""
        return {
            'type': self.type.value,
            'device': self.device,
            'bus': self.bus.value,
            'target': self.target,
            'driver': self.driver,
            'cache': self.cache.value,
            'io': self.io,
            'discard': self.discard,
            'detect_zeroes': self.detect_zeroes,
            'source_file': self.source_file,
            'source_protocol': self.source_protocol,
            'source_dev': self.source_dev,
            'snapshot': self.snapshot,
            'readonly': self.readonly,
            'shareable': self.shareable,
            'transient': self.transient,
            'capacity': self.capacity,
            'allocation': self.allocation,
            'physical': self.physical,
        }


@dataclass
class Graphics:
    """图形设备配置"""

    type: GraphicsType = GraphicsType.VNC
    port: str = '-1'
    tls_port: str | None = None
    listen: str = '0.0.0.0'
    passwd: str | None = None
    connected: str | None = None
    keymap: str | None = None
    default_mode: str | None = None
    image_compression: str | None = None
    jpeg_compression: str | None = None
    zlib_compression: str | None = None
    opengl: bool | None = None
    listen_addresses: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'Graphics':
        """从字典创建"""
        gfx_type = data.get('type', 'vnc')
        if isinstance(gfx_type, str):
            gfx_type = GraphicsType(gfx_type)

        return cls(
            type=gfx_type,
            port=data.get('port', '-1'),
            tls_port=data.get('tls_port'),
            listen=data.get('listen', '0.0.0.0'),
            passwd=data.get('passwd'),
            connected=data.get('connected'),
            keymap=data.get('keymap'),
            default_mode=data.get('default_mode'),
            image_compression=data.get('image_compression'),
            jpeg_compression=data.get('jpeg_compression'),
            zlib_compression=data.get('zlib_compression'),
            opengl=data.get('opengl'),
            listen_addresses=data.get('listen_addresses', []),
        )

    def to_dict(self) -> dict[str, Any]:
        """转换为字典"""
        return {
            'type': self.type.value,
            'port': self.port,
            'tls_port': self.tls_port,
            'listen': self.listen,
            'passwd': self.passwd,
            'connected': self.connected,
            'keymap': self.keymap,
            'default_mode': self.default_mode,
            'image_compression': self.image_compression,
            'jpeg_compression': self.jpeg_compression,
            'zlib_compression': self.zlib_compression,
            'opengl': self.opengl,
            'listen_addresses': self.listen_addresses,
        }


@dataclass
class Video:
    """视频设备配置"""

    model: VideoModel = VideoModel.QXL
    vram: int = 64  # MiB
    heads: int = 1
    primary: bool | None = None
    accel: str | None = None
    rom_file: str | None = None
    resolution: dict[str, int] | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'Video':
        """从字典创建"""
        model = data.get('model', 'qxl')
        if isinstance(model, str):
            model = VideoModel(model)

        return cls(
            model=model,
            vram=data.get('vram', 64),
            heads=data.get('heads', 1),
            primary=data.get('primary'),
            accel=data.get('accel'),
            rom_file=data.get('rom_file'),
            resolution=data.get('resolution'),
        )

    def to_dict(self) -> dict[str, Any]:
        """转换为字典"""
        return {
            'model': self.model.value,
            'vram': self.vram,
            'heads': self.heads,
            'primary': self.primary,
            'accel': self.accel,
            'rom_file': self.rom_file,
            'resolution': self.resolution,
        }


@dataclass
class NetworkInterface:
    """网络设备配置"""

    type: str = 'network'  # network, bridge, user, internal, direct
    source: str | None = None
    target: str | None = None
    mac: str | None = None
    model: str = 'virtio'
    driver: dict[str, str] | None = None
    address: dict[str, str] | None = None
    mtu: int | None = None
    virtualport_type: str | None = None
    virtualport_params: dict[str, str] | None = None
    port: str | None = None
    portgroup: str | None = None
    inbound: dict[str, str] | None = None
    outbound: dict[str, str] | None = None
    link_state: str = 'up'

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'NetworkInterface':
        """从字典创建"""
        return cls(
            type=data.get('type', 'network'),
            source=data.get('source'),
            target=data.get('target'),
            mac=data.get('mac'),
            model=data.get('model', 'virtio'),
            driver=data.get('driver'),
            address=data.get('address'),
            mtu=data.get('mtu'),
            virtualport_type=data.get('virtualport_type'),
            virtualport_params=data.get('virtualport_params'),
            port=data.get('port'),
            portgroup=data.get('portgroup'),
            inbound=data.get('inbound'),
            outbound=data.get('outbound'),
            link_state=data.get('link_state', 'up'),
        )

    def to_dict(self) -> dict[str, Any]:
        """转换为字典"""
        return {
            'type': self.type,
            'source': self.source,
            'target': self.target,
            'mac': self.mac,
            'model': self.model,
            'driver': self.driver,
            'address': self.address,
            'mtu': self.mtu,
            'virtualport_type': self.virtualport_type,
            'virtualport_params': self.virtualport_params,
            'port': self.port,
            'portgroup': self.portgroup,
            'inbound': self.inbound,
            'outbound': self.outbound,
            'link_state': self.link_state,
        }


@dataclass
class Devices:
    """设备集合"""

    emulator: str | None = None
    disks: list[Disk] = field(default_factory=list)
    graphics: list[Graphics] = field(default_factory=list)
    videos: list[Video] = field(default_factory=list)
    interfaces: list[NetworkInterface] = field(default_factory=list)
    serials: list[dict[str, Any]] = field(default_factory=list)
    consoles: list[dict[str, Any]] = field(default_factory=list)
    channels: list[dict[str, Any]] = field(default_factory=list)
    inputs: list[dict[str, Any]] = field(default_factory=list)
    audio: list[dict[str, Any]] = field(default_factory=list)
    sounds: list[dict[str, Any]] = field(default_factory=list)
    hostdevs: list[dict[str, Any]] = field(default_factory=list)
    controllers: list[dict[str, Any]] = field(default_factory=list)
    tpms: list[dict[str, Any]] = field(default_factory=list)
    rngs: list[dict[str, Any]] = field(default_factory=list)
    watchdogs: list[dict[str, Any]] = field(default_factory=list)
    balloons: list[dict[str, Any]] = field(default_factory=list)
    filesystems: list[dict[str, Any]] = field(default_factory=list)
    parallel: list[dict[str, Any]] = field(default_factory=list)
    smartcard: list[dict[str, Any]] = field(default_factory=list)
    shmem: list[dict[str, Any]] = field(default_factory=list)
    vsock: list[dict[str, Any]] = field(default_factory=list)
    crypto: list[dict[str, Any]] = field(default_factory=list)
    iommu: list[dict[str, Any]] = field(default_factory=list)
    panic: list[dict[str, Any]] = field(default_factory=list)
    pstore: list[dict[str, Any]] = field(default_factory=list)
    memory: list[dict[str, Any]] = field(default_factory=list)
    nvram: list[dict[str, Any]] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'Devices':
        """从字典创建"""
        disks = data.get('disks', [])
        if disks and isinstance(disks[0], dict):
            disks = [Disk.from_dict(d) for d in disks]

        graphics = data.get('graphics', [])
        if graphics and isinstance(graphics[0], dict):
            graphics = [Graphics.from_dict(g) for g in graphics]

        videos = data.get('videos', [])
        if videos and isinstance(videos[0], dict):
            videos = [Video.from_dict(v) for v in videos]

        interfaces = data.get('interfaces', [])
        if interfaces and isinstance(interfaces[0], dict):
            interfaces = [NetworkInterface.from_dict(i) for i in interfaces]

        return cls(
            emulator=data.get('emulator'),
            disks=disks,
            graphics=graphics,
            videos=videos,
            interfaces=interfaces,
            serials=data.get('serials', []),
            consoles=data.get('consoles', []),
            channels=data.get('channels', []),
            inputs=data.get('inputs', []),
            audio=data.get('audio', []),
            sounds=data.get('sounds', []),
            hostdevs=data.get('hostdevs', []),
            controllers=data.get('controllers', []),
            tpms=data.get('tpms', []),
            rngs=data.get('rngs', []),
            watchdogs=data.get('watchdogs', []),
            balloons=data.get('balloons', []),
            filesystems=data.get('filesystems', []),
            parallel=data.get('parallel', []),
            smartcard=data.get('smartcard', []),
            shmem=data.get('shmem', []),
            vsock=data.get('vsock', []),
            crypto=data.get('crypto', []),
            iommu=data.get('iommu', []),
            panic=data.get('panic', []),
            pstore=data.get('pstore', []),
            memory=data.get('memory', []),
            nvram=data.get('nvram', []),
        )

    def to_dict(self) -> dict[str, Any]:
        """转换为字典"""
        return {
            'emulator': self.emulator,
            'disks': [d.to_dict() for d in self.disks],
            'graphics': [g.to_dict() for g in self.graphics],
            'videos': [v.to_dict() for v in self.videos],
            'interfaces': [i.to_dict() for i in self.interfaces],
            'serials': self.serials,
            'consoles': self.consoles,
            'channels': self.channels,
            'inputs': self.inputs,
            'audio': self.audio,
            'sounds': self.sounds,
            'hostdevs': self.hostdevs,
            'controllers': self.controllers,
            'tpms': self.tpms,
            'rngs': self.rngs,
            'watchdogs': self.watchdogs,
            'balloons': self.balloons,
            'filesystems': self.filesystems,
            'parallel': self.parallel,
            'smartcard': self.smartcard,
            'shmem': self.shmem,
            'vsock': self.vsock,
            'crypto': self.crypto,
            'iommu': self.iommu,
            'panic': self.panic,
            'pstore': self.pstore,
            'memory': self.memory,
            'nvram': self.nvram,
        }


@dataclass
class Features:
    """特性配置"""

    acpi: bool = True
    apic: bool = True
    pae: bool | None = None
    hap: bool | None = None
    viridian: bool | None = None
    privnet: bool | None = None
    pvspinlock: bool | None = None
    pmu: bool | None = None
    vmport: bool | None = None
    smm: dict[str, Any] | None = None
    hyperv: dict[str, Any] | None = None
    kvm: dict[str, Any] | None = None
    xen: dict[str, Any] | None = None
    gic: dict[str, Any] | None = None
    ioapic: dict[str, Any] | None = None
    hpt: dict[str, Any] | None = None
    tcg: dict[str, Any] | None = None
    vmcoreinfo: bool | None = None
    ras: bool | None = None
    async_teardown: bool | None = None
    ps2: bool | None = None
    aia: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'Features':
        """从字典创建"""
        general = data.get('general', data)
        hyperv = data.get('hyperv')
        kvm = data.get('kvm')
        xen = data.get('xen')
        gic = data.get('gic')
        ioapic = data.get('ioapic')
        hpt = data.get('hpt')
        tcg = data.get('tcg')

        return cls(
            acpi=general.get('acpi', True),
            apic=general.get('apic', True),
            pae=general.get('pae'),
            hap=general.get('hap'),
            viridian=general.get('viridian'),
            privnet=general.get('privnet'),
            pvspinlock=general.get('pvspinlock'),
            pmu=general.get('pmu'),
            vmport=general.get('vmport'),
            smm=general.get('smm'),
            hyperv=hyperv,
            kvm=kvm,
            xen=xen,
            gic=gic,
            ioapic=ioapic,
            hpt=hpt,
            tcg=tcg,
            vmcoreinfo=general.get('vmcoreinfo'),
            ras=general.get('ras'),
            async_teardown=general.get('async_teardown'),
            ps2=general.get('ps2'),
            aia=general.get('aia'),
        )

    def to_dict(self) -> dict[str, Any]:
        """转换为字典"""
        return {
            'general': {
                'acpi': self.acpi,
                'apic': self.apic,
                'pae': self.pae,
                'hap': self.hap,
                'viridian': self.viridian,
                'privnet': self.privnet,
                'pvspinlock': self.pvspinlock,
                'pmu': self.pmu,
                'vmport': self.vmport,
                'smm': self.smm,
                'vmcoreinfo': self.vmcoreinfo,
                'ras': self.ras,
                'async_teardown': self.async_teardown,
                'ps2': self.ps2,
                'aia': self.aia,
            },
            'hyperv': self.hyperv,
            'kvm': self.kvm,
            'xen': self.xen,
            'gic': self.gic,
            'ioapic': self.ioapic,
            'hpt': self.hpt,
            'tcg': self.tcg,
        }


@dataclass
class Clock:
    """时钟配置"""

    offset: str = 'utc'
    timezone: str | None = None
    adjustment: str | None = None
    basis: str | None = None
    start: str | None = None
    timers: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'Clock':
        """从字典创建"""
        return cls(
            offset=data.get('offset', 'utc'),
            timezone=data.get('timezone'),
            adjustment=data.get('adjustment'),
            basis=data.get('basis'),
            start=data.get('start'),
            timers=data.get('timers', {}),
        )

    def to_dict(self) -> dict[str, Any]:
        """转换为字典"""
        return {
            'offset': self.offset,
            'timezone': self.timezone,
            'adjustment': self.adjustment,
            'basis': self.basis,
            'start': self.start,
            'timers': self.timers,
        }


@dataclass
class Domain:
    """虚拟机域配置 - 整合 Config 策略模式"""

    type: VirtType = VirtType.KVM
    name: str = 'vm0'
    uuid: str | None = None
    hwuuid: str | None = None
    genid: str | None = None
    title: str | None = None
    description: str | None = None
    vcpu: VCPU | None = None
    cpu: CPU | None = None
    memory: Memory | None = None
    current_memory: CurrentMemory | None = None
    max_memory: MaxMemory | None = None
    os: OS | None = None
    devices: Devices | None = None
    features: Features | None = None
    clock: Clock | None = None
    on_poweroff: str = 'destroy'
    on_reboot: str = 'restart'
    on_crash: str = 'destroy'
    on_lockfailure: str | None = None
    metadata: dict[str, Any] | None = None
    seclabel: dict[str, Any] | None = None
    numatune: dict[str, Any] | None = None
    memtune: dict[str, Any] | None = None
    blkiotune: dict[str, Any] | None = None
    cputune: dict[str, Any] | None = None
    iothreads: dict[str, Any] | None = None
    launch_security: dict[str, Any] | None = None
    sysinfo: dict[str, Any] | None = None
    memory_backing: dict[str, Any] | None = None
    perf: dict[str, Any] | None = None
    throttlegroups: dict[str, Any] | None = None
    keywrap: dict[str, Any] | None = None
    resource: dict[str, Any] | None = None

    @classmethod
    def from_config(cls, config: dict[str, Any]) -> 'Domain':
        """从 Config 配置字典创建 Domain.

        Args:
            config: Config 层输出的配置字典

        Returns:
            Domain 实例
        """
        # 基础配置
        name = config.get('name', 'vm0')
        uuid = config.get('uuid')
        hwuuid = config.get('hwuuid')
        genid = config.get('genid')
        title = config.get('title')
        description = config.get('description')

        # CPU 配置
        vcpu_data = config.get('cpu_allocation', {})
        vcpu = VCPU(
            count=vcpu_data.get('max_vcpu', 2),
            placement=vcpu_data.get('placement', 'static'),
            cpuset=vcpu_data.get('cpuset'),
            current=vcpu_data.get('current_vcpu'),
        )

        cpu_model_data = config.get('cpu_model_topology', {})
        cpu = CPU.from_dict(cpu_model_data) if cpu_model_data else CPU()

        # 内存配置
        mem_data = config.get('memory_allocation', {})
        memory = Memory(
            size=mem_data.get('memory', 2097152),
            unit=mem_data.get('unit', 'KiB'),
        )
        current_memory = CurrentMemory(
            size=mem_data.get('current_memory', 2097152),
            unit=mem_data.get('unit', 'KiB'),
        )
        max_memory = MaxMemory(
            size=mem_data.get('max_memory', 4194304),
            unit=mem_data.get('unit', 'KiB'),
            slots=mem_data.get('memory_slots'),
        )

        # OS 配置
        os_data = config.get('os_booting', {})
        os = OS.from_dict(os_data) if os_data else OS()

        # 设备配置
        devices_data = config.get('devices', {})
        devices = Devices.from_dict(devices_data) if devices_data else Devices()

        # 特性配置
        features_data = config.get('hypervisor_features', {})
        features = Features.from_dict(features_data) if features_data else Features()

        # 时钟配置
        clock_data = config.get('time_keeping', {})
        clock = Clock.from_dict(clock_data) if clock_data else Clock()

        # 事件配置
        on_poweroff = config.get('events_configuration', {}).get('on_poweroff', 'destroy')
        on_reboot = config.get('events_configuration', {}).get('on_reboot', 'restart')
        on_crash = config.get('events_configuration', {}).get('on_crash', 'destroy')
        on_lockfailure = config.get('events_configuration', {}).get('on_lockfailure')

        # 其他配置
        seclabel = config.get('seclabel')
        numatune = config.get('numatune')
        memtune = config.get('memtune')
        blkiotune = config.get('blkiotune')
        cputune = config.get('cputune')
        iothreads = config.get('iothreads')
        launch_security = config.get('launch_security')
        sysinfo = config.get('sysinfo')
        memory_backing = config.get('memory_backing')
        perf = config.get('perf')
        throttlegroups = config.get('throttlegroups')
        keywrap = config.get('keywrap')
        resource = config.get('resource')

        return cls(
            type=VirtType(config.get('hypervisor', 'kvm')),
            name=name,
            uuid=uuid,
            hwuuid=hwuuid,
            genid=genid,
            title=title,
            description=description,
            vcpu=vcpu,
            cpu=cpu,
            memory=memory,
            current_memory=current_memory,
            max_memory=max_memory,
            os=os,
            devices=devices,
            features=features,
            clock=clock,
            on_poweroff=on_poweroff,
            on_reboot=on_reboot,
            on_crash=on_crash,
            on_lockfailure=on_lockfailure,
            metadata=config.get('metadata'),
            seclabel=seclabel,
            numatune=numatune,
            memtune=memtune,
            blkiotune=blkiotune,
            cputune=cputune,
            iothreads=iothreads,
            launch_security=launch_security,
            sysinfo=sysinfo,
            memory_backing=memory_backing,
            perf=perf,
            throttlegroups=throttlegroups,
            keywrap=keywrap,
            resource=resource,
        )

    def to_config(self) -> dict[str, Any]:
        """转换为 Config 配置字典.

        Returns:
            配置字典
        """
        config = {
            'name': self.name,
            'uuid': self.uuid,
            'hwuuid': self.hwuuid,
            'genid': self.genid,
            'title': self.title,
            'description': self.description,
            'hypervisor': self.type.value,
        }

        # CPU 配置
        if self.vcpu:
            config['cpu_allocation'] = self.vcpu.to_dict()
        if self.cpu:
            cpu_dict = self.cpu.to_dict()
            config['cpu_model_topology'] = {
                'model': cpu_dict.get('model'),
                'feature': cpu_dict.get('features'),
                'cache': cpu_dict.get('cache'),
            }

        # 内存配置
        if self.memory:
            config['memory_allocation'] = {
                'memory': self.memory.size,
                'unit': self.memory.unit.value,
                'current_memory': self.current_memory.size
                if self.current_memory
                else self.memory.size,
                'max_memory': self.max_memory.size if self.max_memory else self.memory.size,
                'memory_slots': self.max_memory.slots if self.max_memory else None,
            }

        # OS 配置
        if self.os:
            config['os_booting'] = self.os.to_dict()

        # 设备配置
        if self.devices:
            config['devices'] = self.devices.to_dict()

        # 特性配置
        if self.features:
            config['hypervisor_features'] = self.features.to_dict()

        # 时钟配置
        if self.clock:
            config['time_keeping'] = self.clock.to_dict()

        # 事件配置
        config['events_configuration'] = {
            'on_poweroff': self.on_poweroff,
            'on_reboot': self.on_reboot,
            'on_crash': self.on_crash,
        }
        if self.on_lockfailure:
            config['events_configuration']['on_lockfailure'] = self.on_lockfailure

        # 其他配置
        if self.seclabel:
            config['seclabel'] = self.seclabel
        if self.numatune:
            config['numatune'] = self.numatune
        if self.memtune:
            config['memtune'] = self.memtune
        if self.blkiotune:
            config['blkiotune'] = self.blkiotune
        if self.cputune:
            config['cputune'] = self.cputune
        if self.iothreads:
            config['iothreads'] = self.iothreads
        if self.launch_security:
            config['launch_security'] = self.launch_security
        if self.sysinfo:
            config['sysinfo'] = self.sysinfo
        if self.memory_backing:
            config['memory_backing'] = self.memory_backing
        if self.perf:
            config['perf'] = self.perf
        if self.throttlegroups:
            config['throttlegroups'] = self.throttlegroups
        if self.keywrap:
            config['keywrap'] = self.keywrap
        if self.resource:
            config['resource'] = self.resource

        return config

    def to_xml_element(self) -> Any:
        """转换为 XML Element(用于生成 libvirt XML).

        Returns:
            XML Element
        """
        import xml.etree.ElementTree as ET

        domain = ET.Element('domain')
        domain.set('type', self.type.value)

        # 基本元素
        if self.name:
            name_elem = ET.SubElement(domain, 'name')
            name_elem.text = self.name

        if self.uuid:
            uuid_elem = ET.SubElement(domain, 'uuid')
            uuid_elem.text = self.uuid

        if self.hwuuid:
            hwuuid_elem = ET.SubElement(domain, 'hwuuid')
            hwuuid_elem.text = self.hwuuid

        if self.genid:
            genid_elem = ET.SubElement(domain, 'genid')
            genid_elem.text = self.genid

        if self.title:
            title_elem = ET.SubElement(domain, 'title')
            title_elem.text = self.title

        if self.description:
            desc_elem = ET.SubElement(domain, 'description')
            desc_elem.text = self.description

        # VCPU
        if self.vcpu:
            vcpu_elem = ET.SubElement(domain, 'vcpu')
            vcpu_elem.text = str(self.vcpu.count)
            if self.vcpu.placement:
                vcpu_elem.set('placement', self.vcpu.placement)
            if self.vcpu.cpuset:
                vcpu_elem.set('cpuset', self.vcpu.cpuset)
            if self.vcpu.current:
                vcpu_elem.set('current', str(self.vcpu.current))

        # CPU
        if self.cpu:
            cpu_elem = ET.SubElement(domain, 'cpu')
            if self.cpu.mode:
                cpu_elem.set(
                    'mode',
                    self.cpu.mode.value
                    if isinstance(self.cpu.mode, CpuMode)
                    else str(self.cpu.mode),
                )
            if self.cpu.model:
                model_elem = ET.SubElement(cpu_elem, 'model')
                model_elem.text = self.cpu.model.name
                if self.cpu.model.fallback:
                    model_elem.set('fallback', self.cpu.model.fallback)
            if self.cpu.topology:
                ET.SubElement(
                    cpu_elem,
                    'topology',
                    attrib={
                        'sockets': str(self.cpu.topology.sockets),
                        'cores': str(self.cpu.topology.cores),
                        'threads': str(self.cpu.topology.threads),
                    },
                )
            for feature in self.cpu.features:
                feat_elem = ET.SubElement(cpu_elem, 'feature')
                feat_elem.set('name', feature.name)
                if feature.policy:
                    feat_elem.set('policy', feature.policy)

            if self.cpu.cache:
                cache_elem = ET.SubElement(cpu_elem, 'cache')
                if 'level' in self.cpu.cache:
                    cache_elem.set('level', str(self.cpu.cache['level']))
                if 'mode' in self.cpu.cache:
                    cache_elem.set('mode', self.cpu.cache['mode'])

            if self.cpu.maxphysaddr:
                maxphysaddr_elem = ET.SubElement(cpu_elem, 'maxphysaddr')
                if 'mode' in self.cpu.maxphysaddr:
                    maxphysaddr_elem.set('mode', self.cpu.maxphysaddr['mode'])
                if 'bits' in self.cpu.maxphysaddr:
                    maxphysaddr_elem.set('bits', str(self.cpu.maxphysaddr['bits']))
                if 'limit' in self.cpu.maxphysaddr:
                    maxphysaddr_elem.set('limit', str(self.cpu.maxphysaddr['limit']))

            if self.cpu.numa:
                numa_elem = ET.SubElement(cpu_elem, 'numa')
                if self.cpu.numa.nodes:
                    for node in self.cpu.numa.nodes:
                        node_elem = ET.SubElement(numa_elem, 'cell')
                        node_elem.set('id', str(node.id))
                        if node.cpus:
                            node_elem.set('cpus', node.cpus)
                        if node.memory:
                            node_elem.set('memory', str(node.memory))
                        if node.unit:
                            node_elem.set('unit', node.unit)
                        if node.memAccess:
                            node_elem.set('memAccess', node.memAccess)
                        if node.discard is not None:
                            node_elem.set('discard', 'yes' if node.discard else 'no')
                        if node.distances:
                            distances_elem = ET.SubElement(node_elem, 'distances')
                            for sibling in node.distances:
                                sibling_elem = ET.SubElement(distances_elem, 'sibling')
                                sibling_elem.set('id', str(sibling.id))
                                sibling_elem.set('value', str(sibling.value))

        # 内存
        if self.memory:
            mem_elem = ET.SubElement(domain, 'memory')
            mem_elem.text = str(self.memory.size)
            mem_elem.set('unit', self.memory.unit.value)
            if self.memory.dump_core is not None:
                mem_elem.set('dumpCore', 'yes' if self.memory.dump_core else 'no')

        if self.current_memory:
            curr_mem_elem = ET.SubElement(domain, 'currentMemory')
            curr_mem_elem.text = str(self.current_memory.size)
            curr_mem_elem.set('unit', self.current_memory.unit.value)

        if self.max_memory:
            max_mem_elem = ET.SubElement(domain, 'maxMemory')
            max_mem_elem.text = str(self.max_memory.size)
            max_mem_elem.set('unit', self.max_memory.unit.value)
            if self.max_memory.slots:
                max_mem_elem.set('slots', str(self.max_memory.slots))

        # OS
        if self.os:
            os_elem = ET.SubElement(domain, 'os')
            type_elem = ET.SubElement(os_elem, 'type')
            type_elem.text = self.os.type.value
            type_elem.set('arch', self.os.arch)
            type_elem.set('machine', self.os.machine.value)
            if self.os.firmware:
                type_elem.set('firmware', self.os.firmware.value)

            if self.os.boot:
                for boot in self.os.boot:
                    boot_elem = ET.SubElement(os_elem, 'boot')
                    boot_elem.set('dev', boot.dev)

            if self.os.bootmenu:
                bootmenu_elem = ET.SubElement(os_elem, 'bootmenu')
                bootmenu_elem.set('enable', 'yes' if self.os.bootmenu.enable else 'no')
                if self.os.bootmenu.timeout:
                    bootmenu_elem.set('timeout', str(self.os.bootmenu.timeout))

            if self.os.loader:
                loader_elem = ET.SubElement(os_elem, 'loader')
                loader_elem.text = self.os.loader.path
                if self.os.loader.readonly is not None:
                    loader_elem.set('readonly', 'yes' if self.os.loader.readonly else 'no')
                if self.os.loader.secure is not None:
                    loader_elem.set('secure', 'yes' if self.os.loader.secure else 'no')
                if self.os.loader.type:
                    loader_elem.set('type', self.os.loader.type)

            if self.os.nvram:
                nvram_elem = ET.SubElement(os_elem, 'nvram')
                if self.os.nvram.path:
                    nvram_elem.text = self.os.nvram.path
                if self.os.nvram.template:
                    nvram_elem.set('template', self.os.nvram.template)

            if self.os.varstore:
                varstore_elem = ET.SubElement(os_elem, 'varstore')
                if 'path' in self.os.varstore:
                    varstore_elem.set('path', self.os.varstore['path'])
                if 'template' in self.os.varstore:
                    varstore_elem.set('template', self.os.varstore['template'])

            if self.os.smbios:
                smbios_elem = ET.SubElement(os_elem, 'smbios')
                if 'mode' in self.os.smbios:
                    smbios_elem.set('mode', self.os.smbios['mode'])

            if self.os.bios:
                bios_elem = ET.SubElement(os_elem, 'bios')
                if 'useserial' in self.os.bios:
                    bios_elem.set('useserial', 'yes' if self.os.bios['useserial'] else 'no')
                if 'rebootTimeout' in self.os.bios:
                    bios_elem.set('rebootTimeout', str(self.os.bios['rebootTimeout']))

            if self.os.kernel:
                ET.SubElement(os_elem, 'kernel').text = self.os.kernel

            if self.os.initrd:
                ET.SubElement(os_elem, 'initrd').text = self.os.initrd

            if self.os.cmdline:
                ET.SubElement(os_elem, 'cmdline').text = self.os.cmdline

            if self.os.shim:
                ET.SubElement(os_elem, 'shim').text = self.os.shim

            if self.os.dtb:
                ET.SubElement(os_elem, 'dtb').text = self.os.dtb

            if self.os.init:
                ET.SubElement(os_elem, 'init').text = self.os.init

            for arg in self.os.initargs:
                ET.SubElement(os_elem, 'initarg').text = arg

            for env in self.os.initenv:
                if 'name' in env and 'value' in env:
                    env_elem = ET.SubElement(os_elem, 'initenv')
                    env_elem.set('name', env['name'])
                    env_elem.text = env['value']

            if self.os.initdir:
                ET.SubElement(os_elem, 'initdir').text = self.os.initdir

            if self.os.inituser:
                ET.SubElement(os_elem, 'inituser').text = self.os.inituser

            if self.os.initgroup:
                ET.SubElement(os_elem, 'initgroup').text = self.os.initgroup

            if self.os.idmap:
                idmap_elem = ET.SubElement(os_elem, 'idmap')
                if 'uid' in self.os.idmap:
                    uid = self.os.idmap['uid']
                    uid_elem = ET.SubElement(idmap_elem, 'uid')
                    if 'start' in uid:
                        uid_elem.set('start', str(uid['start']))
                    if 'target' in uid:
                        uid_elem.set('target', str(uid['target']))
                    if 'count' in uid:
                        uid_elem.set('count', str(uid['count']))
                if 'gid' in self.os.idmap:
                    gid = self.os.idmap['gid']
                    gid_elem = ET.SubElement(idmap_elem, 'gid')
                    if 'start' in gid:
                        gid_elem.set('start', str(gid['start']))
                    if 'target' in gid:
                        gid_elem.set('target', str(gid['target']))
                    if 'count' in gid:
                        gid_elem.set('count', str(gid['count']))

            if self.os.acpi:
                acpi_elem = ET.SubElement(os_elem, 'acpi')
                if 'tables' in self.os.acpi:
                    for table in self.os.acpi['tables']:
                        table_elem = ET.SubElement(acpi_elem, 'table')
                        if 'type' in table:
                            table_elem.set('type', table['type'])
                        if 'path' in table:
                            table_elem.text = table['path']

        # 电源管理
        pm_elem = ET.SubElement(domain, 'pm')
        suspend_mem = ET.SubElement(pm_elem, 'suspend-to-mem')
        suspend_mem.set('enabled', 'yes')
        suspend_disk = ET.SubElement(pm_elem, 'suspend-to-disk')
        suspend_disk.set('enabled', 'yes')

        # 事件
        if self.on_poweroff:
            ET.SubElement(domain, 'on_poweroff').text = self.on_poweroff
        if self.on_reboot:
            ET.SubElement(domain, 'on_reboot').text = self.on_reboot
        if self.on_crash:
            ET.SubElement(domain, 'on_crash').text = self.on_crash
        if self.on_lockfailure:
            ET.SubElement(domain, 'on_lockfailure').text = self.on_lockfailure

        # 特性
        if self.features:
            features_elem = ET.SubElement(domain, 'features')
            if self.features.acpi:
                ET.SubElement(features_elem, 'acpi')
            if self.features.apic:
                ET.SubElement(features_elem, 'apic')
                # 可以添加 eoi 属性
            if self.features.pae:
                ET.SubElement(features_elem, 'pae')
            if self.features.hap is not None:
                hap_elem = ET.SubElement(features_elem, 'hap')
                hap_elem.set('state', 'on' if self.features.hap else 'off')
            if self.features.viridian:
                ET.SubElement(features_elem, 'viridian')
            if self.features.privnet:
                ET.SubElement(features_elem, 'privnet')
            if self.features.pvspinlock is not None:
                pvspinlock_elem = ET.SubElement(features_elem, 'pvspinlock')
                pvspinlock_elem.set('state', 'on' if self.features.pvspinlock else 'off')
            if self.features.pmu is not None:
                pmu_elem = ET.SubElement(features_elem, 'pmu')
                pmu_elem.set('state', 'on' if self.features.pmu else 'off')
            if self.features.vmport is not None:
                vmport_elem = ET.SubElement(features_elem, 'vmport')
                vmport_elem.set('state', 'on' if self.features.vmport else 'off')
            if self.features.smm:
                smm_elem = ET.SubElement(features_elem, 'smm')
                smm_elem.set('state', 'on' if self.features.smm.get('state', True) else 'off')
                if 'tseg' in self.features.smm:
                    tseg_elem = ET.SubElement(smm_elem, 'tseg')
                    tseg_elem.text = str(self.features.smm['tseg'])
                    if 'unit' in self.features.smm:
                        tseg_elem.set('unit', self.features.smm['unit'])
            if self.features.hyperv:
                hyperv_elem = ET.SubElement(features_elem, 'hyperv')
                if 'mode' in self.features.hyperv:
                    hyperv_elem.set('mode', self.features.hyperv['mode'])
                for key, value in self.features.hyperv.items():
                    if key != 'mode':
                        if isinstance(value, bool):
                            ET.SubElement(hyperv_elem, key).set('state', 'on' if value else 'off')
                        elif isinstance(value, dict):
                            elem = ET.SubElement(hyperv_elem, key)
                            for k, v in value.items():
                                if isinstance(v, bool):
                                    elem.set(k, 'on' if v else 'off')
                                else:
                                    elem.set(k, str(v))
            if self.features.kvm:
                kvm_elem = ET.SubElement(features_elem, 'kvm')
                for key, value in self.features.kvm.items():
                    if isinstance(value, bool):
                        ET.SubElement(kvm_elem, key).set('state', 'on' if value else 'off')
                    elif isinstance(value, dict):
                        elem = ET.SubElement(kvm_elem, key)
                        for k, v in value.items():
                            elem.set(k, str(v))
            if self.features.xen:
                xen_elem = ET.SubElement(features_elem, 'xen')
                for key, value in self.features.xen.items():
                    if isinstance(value, bool):
                        ET.SubElement(xen_elem, key).set('state', 'on' if value else 'off')
                    elif isinstance(value, dict):
                        elem = ET.SubElement(xen_elem, key)
                        for k, v in value.items():
                            elem.set(k, str(v))
            if self.features.gic:
                gic_elem = ET.SubElement(features_elem, 'gic')
                if 'version' in self.features.gic:
                    gic_elem.set('version', str(self.features.gic['version']))
            if self.features.ioapic:
                ioapic_elem = ET.SubElement(features_elem, 'ioapic')
                if 'driver' in self.features.ioapic:
                    ioapic_elem.set('driver', self.features.ioapic['driver'])
            if self.features.hpt:
                hpt_elem = ET.SubElement(features_elem, 'hpt')
                if 'resizing' in self.features.hpt:
                    hpt_elem.set('resizing', self.features.hpt['resizing'])
                if 'maxpagesize' in self.features.hpt:
                    maxpagesize_elem = ET.SubElement(hpt_elem, 'maxpagesize')
                    maxpagesize_elem.text = str(self.features.hpt['maxpagesize'])
                    if 'unit' in self.features.hpt:
                        maxpagesize_elem.set('unit', self.features.hpt['unit'])
            if self.features.tcg:
                tcg_elem = ET.SubElement(features_elem, 'tcg')
                if 'tb-cache' in self.features.tcg:
                    tbcache_elem = ET.SubElement(tcg_elem, 'tb-cache')
                    tbcache_elem.text = str(self.features.tcg['tb-cache'])
                    if 'unit' in self.features.tcg:
                        tbcache_elem.set('unit', self.features.tcg['unit'])
            if self.features.vmcoreinfo:
                ET.SubElement(features_elem, 'vmcoreinfo').set('state', 'on')
            if self.features.ras:
                ET.SubElement(features_elem, 'ras').set('state', 'on')
            if self.features.async_teardown:
                async_elem = ET.SubElement(features_elem, 'async-teardown')
                async_elem.set('enabled', 'yes')
            if self.features.ps2:
                ET.SubElement(features_elem, 'ps2').set('state', 'on')
            if self.features.aia:
                aia_elem = ET.SubElement(features_elem, 'aia')
                aia_elem.set('value', self.features.aia)

        # 时钟
        if self.clock:
            clock_elem = ET.SubElement(domain, 'clock')
            clock_elem.set('offset', self.clock.offset)
            if self.clock.timezone:
                clock_elem.set('timezone', self.clock.timezone)
            if self.clock.timers:
                for timer_name, timer_config in self.clock.timers.items():
                    if isinstance(timer_config, dict):
                        ET.SubElement(clock_elem, f'{timer_name}-timer', attrib=timer_config)

        # 设备
        if self.devices:
            devices_elem = ET.SubElement(domain, 'devices')

            # 模拟器
            if self.devices.emulator:
                ET.SubElement(devices_elem, 'emulator').text = self.devices.emulator

            # 磁盘
            for disk in self.devices.disks:
                disk_elem = ET.SubElement(devices_elem, 'disk')
                disk_elem.set('type', disk.type.value)
                disk_elem.set('device', disk.device)

                driver_elem = ET.SubElement(disk_elem, 'driver')
                driver_elem.set('name', 'qemu')
                driver_elem.set('type', disk.type.value)
                if disk.cache:
                    driver_elem.set('cache', disk.cache.value)

                if disk.source_file:
                    ET.SubElement(disk_elem, 'source', file=disk.source_file)
                elif disk.source_dev:
                    ET.SubElement(disk_elem, 'source', dev=disk.source_dev)

                target_elem = ET.SubElement(disk_elem, 'target')
                target_elem.set('dev', disk.target)
                target_elem.set('bus', disk.bus.value)

            # 图形
            for gfx in self.devices.graphics:
                gfx_elem = ET.SubElement(devices_elem, 'graphics')
                gfx_elem.set('type', gfx.type.value)
                if gfx.port:
                    gfx_elem.set('port', gfx.port)
                if gfx.listen:
                    gfx_elem.set('listen', gfx.listen)
                if gfx.passwd:
                    gfx_elem.set('passwd', gfx.passwd)
                if gfx.keymap:
                    gfx_elem.set('keymap', gfx.keymap)

                if gfx.listen_addresses:
                    listen_elem = ET.SubElement(gfx_elem, 'listen')
                    listen_elem.set('type', 'address')

            # 视频
            for video in self.devices.videos:
                video_elem = ET.SubElement(devices_elem, 'video')
                model_elem = ET.SubElement(video_elem, 'model')
                model_elem.set('type', video.model.value)
                model_elem.set('vram', str(video.vram))
                model_elem.set('heads', str(video.heads))

            # 网络接口
            for iface in self.devices.interfaces:
                iface_elem = ET.SubElement(devices_elem, 'interface')
                iface_elem.set('type', iface.type)

                if iface.source:
                    if iface.type == 'network':
                        ET.SubElement(iface_elem, 'source', network=iface.source)
                    elif iface.type == 'bridge':
                        ET.SubElement(iface_elem, 'source', bridge=iface.source)

                if iface.mac:
                    ET.SubElement(iface_elem, 'mac', address=iface.mac)

                model_elem = ET.SubElement(iface_elem, 'model')
                model_elem.set('type', iface.model)

        # 安全标签
        if self.seclabel:
            seclabel_elem = ET.SubElement(domain, 'seclabel')
            for key, value in self.seclabel.items():
                if value is not None:
                    seclabel_elem.set(key, str(value))

        # NUMA 调优
        if self.numatune:
            numatune_elem = ET.SubElement(domain, 'numatune')
            if 'memory_mode' in self.numatune:
                numatune_elem.set('memoryMode', self.numatune['memory_mode'])
            if 'memory_nodeset' in self.numatune:
                numatune_elem.set('memoryNodeset', self.numatune['memory_nodeset'])
            if 'memory_placement' in self.numatune:
                numatune_elem.set('memoryPlacement', self.numatune['memory_placement'])

        # 内存调优
        if self.memtune:
            memtune_elem = ET.SubElement(domain, 'memtune')
            if 'hard_limit' in self.memtune:
                hard_limit = ET.SubElement(memtune_elem, 'hard_limit')
                hard_limit.text = str(self.memtune['hard_limit'])
                if 'hard_limit_unit' in self.memtune:
                    hard_limit.set('unit', self.memtune['hard_limit_unit'])

        # 块 IO 调优
        if self.blkiotune:
            blkiotune_elem = ET.SubElement(domain, 'blkiotune')
            if 'weight' in self.blkiotune:
                ET.SubElement(blkiotune_elem, 'weight').text = str(self.blkiotune['weight'])

        # CPU 调优
        if self.cputune:
            cputune_elem = ET.SubElement(domain, 'cputune')
            if 'shares' in self.cputune:
                ET.SubElement(cputune_elem, 'shares').text = str(self.cputune['shares'])

        # IO 线程
        if self.iothreads:
            if 'count' in self.iothreads:
                ET.SubElement(domain, 'iothreads').text = str(self.iothreads['count'])

        # 启动安全
        if self.launch_security:
            launch_security_elem = ET.SubElement(domain, 'launchSecurity')
            for key, value in self.launch_security.items():
                if value is not None:
                    launch_security_elem.set(key, str(value))

        # 系统信息
        if self.sysinfo:
            sysinfo_elem = ET.SubElement(domain, 'sysinfo')
            sysinfo_elem.set('type', self.sysinfo.get('type', 'smbios'))

        # 内存后端
        if self.memory_backing:
            memory_backing_elem = ET.SubElement(domain, 'memoryBacking')
            if self.memory_backing.get('locked'):
                ET.SubElement(memory_backing_elem, 'locked')

        # 性能配置
        if self.perf:
            perf_elem = ET.SubElement(domain, 'perf')
            if 'events' in self.perf:
                for event in self.perf['events']:
                    event_elem = ET.SubElement(perf_elem, 'event')
                    event_elem.set('name', event.get('name'))
                    event_elem.set('enabled', str(event.get('enabled')))

        # 节流组
        if self.throttlegroups:
            throttlegroups_elem = ET.SubElement(domain, 'throttlegroups')
            if 'throttlegroups' in self.throttlegroups:
                for group in self.throttlegroups['throttlegroups']:
                    group_elem = ET.SubElement(throttlegroups_elem, 'throttlegroup')
                    group_elem.set('name', group.get('name'))

        # 密钥包装
        if self.keywrap:
            keywrap_elem = ET.SubElement(domain, 'keywrap')
            for key, value in self.keywrap.items():
                if value is not None:
                    keywrap_elem.set(key, str(value))

        # 资源配置
        if self.resource:
            resource_elem = ET.SubElement(domain, 'resource')
            if 'partition' in self.resource:
                ET.SubElement(resource_elem, 'partition').text = self.resource['partition']
            if 'fibrechannel' in self.resource:
                fc = self.resource['fibrechannel']
                fc_elem = ET.SubElement(resource_elem, 'fibrechannel')
                if 'appid' in fc:
                    fc_elem.set('appid', fc['appid'])
            if 'resources' in self.resource:
                for res in self.resource['resources']:
                    res_elem = ET.SubElement(resource_elem, 'resource')
                    res_elem.set('name', res.get('name'))
                    res_elem.text = str(res.get('value'))
                    if 'unit' in res:
                        res_elem.set('unit', res.get('unit'))

        return domain

    def to_xml(self, indent: int = 2) -> str:
        """转换为 XML 字符串.

        Args:
            indent: 缩进空格数

        Returns:
            XML 字符串
        """
        import xml.etree.ElementTree as ET

        from xml.dom import minidom

        root = self.to_xml_element()

        # 格式化 XML
        rough_string = ET.tostring(root, encoding='unicode')
        reparsed = minidom.parseString(rough_string)
        pretty = reparsed.toprettyxml(indent=' ' * indent)

        # 移除多余的声明和空行
        lines = pretty.split('\n')
        if lines[0].startswith('<?xml'):
            lines = lines[1:]
        while lines and not lines[0].strip():
            lines = lines[1:]

        return '\n'.join(lines).strip()
