"""Libvirt XML 构建器."""

import xml.etree.ElementTree as ET
from xml.dom import minidom


def build_libvirt_xml(data: dict) -> str:
    """构建 libvirt domain XML.

    Args:
        data: 虚拟机配置数据字典

    Returns:
        格式化后的 XML 字符串
    """
    # 根元素
    domain = ET.Element('domain', type='kvm')

    # 名称
    name = ET.SubElement(domain, 'name')
    name.text = data['name']

    # 描述
    if data.get('description'):
        desc = ET.SubElement(domain, 'description')
        desc.text = data['description']

    # UUID
    if data.get('uuid'):
        uuid_elem = ET.SubElement(domain, 'uuid')
        uuid_elem.text = data['uuid']

    # 内存 (KiB)
    memory = ET.SubElement(domain, 'memory', unit='KiB')
    memory.text = str(data['memory'] * 1024)

    # 当前内存（动态内存）
    current_memory = ET.SubElement(domain, 'currentMemory', unit='KiB')
    current_memory.text = str(data.get('current_memory', data['memory']) * 1024)

    # 最大内存（动态内存）
    max_memory = data.get('max_memory')
    if max_memory and max_memory != data['memory']:
        max_memory_elem = ET.SubElement(domain, 'maxMemory', unit='KiB')
        max_memory_elem.text = str(max_memory * 1024)

    # 交换内存
    swap = data.get('swap', 0)
    if swap and swap > 0:
        swap_elem = ET.SubElement(domain, 'memtune')
        ET.SubElement(swap_elem, 'hard_limit', unit='KiB').text = str(swap)

    # vCPU
    vcpu = ET.SubElement(domain, 'vcpu')
    vcpu.text = str(data['vcpu'])

    # CPU 模式
    cpu_mode = data.get('cpu_mode')
    if cpu_mode and cpu_mode != 'custom':
        cpu_elem = ET.SubElement(domain, 'cpu', mode=cpu_mode)
    elif cpu_mode == 'custom':
        cpu_elem = ET.SubElement(domain, 'cpu')

    # 操作系统
    os_elem = ET.SubElement(domain, 'os')

    # 引导设备（支持多个）
    boot_devices = data.get('boot_devices', ['hd'])
    for dev in boot_devices:
        ET.SubElement(os_elem, 'boot', dev=dev)

    # 引导超时
    boot_timeout = data.get('boot_timeout', -1)
    if boot_timeout > 0:
        ET.SubElement(os_elem, 'bootmenu', timeout=str(boot_timeout))

    # 机型
    os_type = ET.SubElement(os_elem, 'type', arch='x86_64', machine=data.get('machine', 'q35'))
    os_type.text = 'hvm' if data.get('virt_type', 'hvm') == 'hvm' else 'linux'

    # 芯片组
    chipset = data.get('chipset')
    if chipset:
        ET.SubElement(os_elem, 'chipset', model=chipset)

    # UEFI 固件
    firmware = data.get('firmware', 'BIOS')
    if firmware == 'UEFI':
        loader = ET.SubElement(
            os_elem, 'loader', readonly='yes', type='pflash'
        )
        loader.text = '/usr/share/OVMF/OVMF_CODE.fd'
        nvram = ET.SubElement(os_elem, 'nvram')
        nvram.text = f'/var/lib/libvirt/qemu/nvram/{data["name"]}_VARS.fd'
    elif firmware == 'EFIVARS':
        loader = ET.SubElement(
            os_elem, 'loader', readonly='yes', type='pflash'
        )
        loader.text = '/usr/share/OVMF/OVMF_CODE.fd'
        nvram = ET.SubElement(os_elem, 'nvram')
        nvram.text = f'/var/lib/libvirt/qemu/nvram/{data["name"]}_VARS.fd'

    # 安全启动
    if data.get('secure_boot'):
        features_elem = ET.SubElement(os_elem, 'features')
        ET.SubElement(features_elem, 'secure-boot', enabled='yes')

    # 功能特性
    features = ET.SubElement(domain, 'features')
    if data.get('features', {}).get('acpi', True):
        ET.SubElement(features, 'acpi')
    if data.get('features', {}).get('apic', True):
        ET.SubElement(features, 'apic')
    if data.get('features', {}).get('hyperv'):
        hyperv = ET.SubElement(features, 'hyperv')
        ET.SubElement(hyperv, 'vpindex', mode='native')
        ET.SubElement(hyperv, 'synic', mode='native')
        ET.SubElement(hyperv, 'vapic', mode='on')
        ET.SubElement(hyperv, 'spinlocks', retries='8191')
    if data.get('features', {}).get('iommu'):
        iommu = ET.SubElement(domain, 'iommu', type='intel')
        ET.SubElement(iommu, 'interrupt_remapping', enabled='yes')

    # 时钟
    clock_offset = data.get('clock', {}).get('rtc', 'utc')
    clock = ET.SubElement(domain, 'clock', offset=clock_offset)
    ET.SubElement(clock, 'timer', name='rtc', tickpolicy='catchup')
    ET.SubElement(clock, 'timer', name='pit', tickpolicy='delay')
    ET.SubElement(clock, 'timer', name='hpet', present='no')

    # KVM 时钟
    if data.get('clock', {}).get('kvm_clock', True):
        ET.SubElement(clock, 'timer', name='kvmclock', present='yes')

    # 看门狗
    watchdog = data.get('watchdog')
    if watchdog and watchdog.get('model') != 'none':
        watchdog_elem = ET.SubElement(domain, 'watchdog', model=watchdog['model'])
        ET.SubElement(watchdog_elem, 'action', name=watchdog.get('action', 'reset'))

    # 设备
    devices = ET.SubElement(domain, 'devices')

    # 磁盘（包括 CDROM）
    for i, disk in enumerate(data.get('disks', [])):
        disk_type = 'cdrom' if disk.get('type') == 'cdrom' else 'disk'
        disk_elem = ET.SubElement(
            devices, 'disk', type='file' if disk.get('path') else 'block', device=disk_type
        )

        # 驱动（CDROM 不需要 driver）
        if disk_type != 'cdrom' and disk.get('type'):
            driver = ET.SubElement(
                disk_elem, 'driver', name='qemu', type=disk['type'], cache='none'
            )

        # 源文件
        if disk.get('path'):
            ET.SubElement(
                disk_elem, 'source', file=disk['path']
            )

        # 目标设备
        if disk_type == 'cdrom':
            # CDROM 使用固定的设备命名
            ET.SubElement(
                disk_elem, 'target', dev=f'sd{chr(ord("a") + i)}', bus=disk.get('bus', 'sata')
            )
            # CDROM 需要 readonly
            ET.SubElement(disk_elem, 'readonly')
        else:
            ET.SubElement(
                disk_elem, 'target', dev=f'vd{chr(ord("a") + i)}', bus=disk.get('bus', 'virtio')
            )

        # 磁盘名称
        if disk.get('name'):
            ET.SubElement(disk_elem, 'alias', name=disk['name'])

    # 网络
    for network in data.get('networks', []):
        iface_type = 'network' if network.get('mode') == 'NAT' else 'bridge'
        interface = ET.SubElement(
            devices, 'interface', type=iface_type
        )
        if network.get('mac'):
            ET.SubElement(interface, 'mac', address=network['mac'])
        if network.get('mode') == 'NAT':
            ET.SubElement(interface, 'source', network='default')
        else:
            bridge = network.get('bridge') or 'br0'
            ET.SubElement(interface, 'source', bridge=bridge)
        ET.SubElement(interface, 'model', type=network.get('model', 'virtio'))
        if network.get('name'):
            ET.SubElement(interface, 'alias', name=network['name'])

    # 图形配置
    graphics = data.get('graphics', {})
    if graphics and graphics.get('type') and graphics['type'] != 'none':
        graphics_elem = ET.SubElement(
            devices, 'graphics',
            type=graphics['type'],
            port='-1',
            autoport='yes',
            listen=graphics.get('listen', '0.0.0.0')
        )
        ET.SubElement(graphics_elem, 'listen', type='address', address=graphics.get('listen', '0.0.0.0'))

    # 视频
    video_model = graphics.get('video_model', 'qxl') if graphics else 'qxl'
    vram = graphics.get('vram', 64) if graphics else 64
    video = ET.SubElement(devices, 'video')
    ET.SubElement(video, 'model', type=video_model, ram='65536', vram=str(vram * 1024), vgamem='16384')

    # USB 控制器
    usb_config = data.get('usb', {})
    if usb_config.get('controller') and usb_config.get('controller') != 'none':
        if not usb_config.get('disabled'):
            ET.SubElement(devices, 'controller', type='usb', model=usb_config['controller'])

    # USB 设备
    for usb in data.get('usb', {}).get('devices', []):
        if ':' in usb:
            vendor, product = usb.split(':')
            usb_elem = ET.SubElement(
                devices, 'hostdev', mode='subsystem', type='usb', managed='yes'
            )
            source = ET.SubElement(usb_elem, 'source')
            ET.SubElement(source, 'vendor', id=f'0x{vendor}')
            ET.SubElement(source, 'product', id=f'0x{product}')

    # 内存平衡
    balloon = data.get('balloon')
    if balloon:
        balloon_elem = ET.SubElement(devices, 'memballoon', model='virtio')
        if balloon.get('target'):
            ET.SubElement(balloon_elem, 'size', unit='MiB').text = str(balloon['target'])

    # 控制台
    console = ET.SubElement(devices, 'console', type='pty')
    ET.SubElement(console, 'target', type='serial', port='0')

    # 输入设备
    ET.SubElement(devices, 'input', type='tablet', bus='usb')
    ET.SubElement(devices, 'input', type='mouse', bus='ps2')

    # PCI 直通设备
    for hostdev in data.get('hostdevs', []):
        hd = ET.SubElement(
            devices, 'hostdev', mode='subsystem', type='pci', managed='yes'
        )
        source = ET.SubElement(hd, 'source')
        # 解析 PCI 地址
        try:
            pci_addr = hostdev.get('pci', '')
            if pci_addr:
                parts = pci_addr.replace(',', ':').split(':')
                if len(parts) >= 4:
                    domain_bus = parts[0]
                    bus = parts[1]
                    slot = parts[2]
                    func_parts = parts[3].split('.')
                    function = func_parts[1] if len(func_parts) > 1 else func_parts[0]
                    ET.SubElement(
                        source, 'address',
                        domain=domain_bus,
                        bus=bus,
                        slot=slot,
                        function=function,
                    )
        except (IndexError, ValueError):
            pass
        if hostdev.get('name'):
            ET.SubElement(hd, 'alias', name=hostdev['name'])

    # 生成格式化的 XML
    xml_str = ET.tostring(domain, encoding='unicode')
    parsed = minidom.parseString(xml_str)
    return parsed.toprettyxml(indent='  ')
