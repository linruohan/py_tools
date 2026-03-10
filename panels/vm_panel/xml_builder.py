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
    if data['description']:
        desc = ET.SubElement(domain, 'description')
        desc.text = data['description']

    # 内存 (KB)
    memory = ET.SubElement(domain, 'memory', unit='KiB')
    memory.text = str(data['memory'] * 1024)

    # 当前内存
    current_memory = ET.SubElement(domain, 'currentMemory', unit='KiB')
    current_memory.text = str(data['memory'] * 1024)

    # vCPU
    vcpu = ET.SubElement(domain, 'vcpu')
    vcpu.text = str(data['vcpu'])

    # 操作系统
    os_elem = ET.SubElement(domain, 'os')
    os_type = ET.SubElement(os_elem, 'type', arch='x86_64', machine=data['machine'])
    if data['virt_type'] == 'hvm':
        os_type.text = 'hvm'
    else:
        os_type.text = 'linux'

    # 引导设备
    boot = ET.SubElement(os_elem, 'boot', dev=data['boot_device'])

    # UEFI 固件
    if data['firmware'] == 'UEFI':
        loader = ET.SubElement(
            os_elem, 'loader', readonly='yes', type='pflash'
        )
        loader.text = '/usr/share/OVMF/OVMF_CODE.fd'
        nvram = ET.SubElement(os_elem, 'nvram')
        nvram.text = f'/var/lib/libvirt/qemu/nvram/{data["name"]}._VARS.fd'

    # 功能特性
    features = ET.SubElement(domain, 'features')
    if data['features']['acpi']:
        ET.SubElement(features, 'acpi')
    if data['features']['apic']:
        ET.SubElement(features, 'apic')
    if data['features']['hyperv']:
        hyperv = ET.SubElement(features, 'hyperv')
        ET.SubElement(hyperv, 'vpindex', mode='native')
        ET.SubElement(hyperv, 'synic', mode='native')

    # IOMMU
    if data['features']['iommu']:
        iommu = ET.SubElement(domain, 'iommu', type='intel')

    # 时钟
    clock = ET.SubElement(domain, 'clock', offset='utc')
    ET.SubElement(clock, 'timer', name='rtc', tickpolicy='catchup')
    ET.SubElement(clock, 'timer', name='pit', tickpolicy='delay')
    ET.SubElement(clock, 'timer', name='hpet', present='no')

    # 设备
    devices = ET.SubElement(domain, 'devices')

    # 磁盘
    for i, disk in enumerate(data['disks']):
        disk_elem = ET.SubElement(
            devices, 'disk', type='file', device='disk'
        )
        driver = ET.SubElement(
            disk_elem, 'driver', name='qemu', type=disk['type'], cache='none'
        )
        source = ET.SubElement(
            disk_elem, 'source', file=disk['path']
        )
        target = ET.SubElement(
            disk_elem, 'target', dev=f'vd{chr(ord("a") + i)}', bus=disk['bus']
        )

    # 网络
    for i, network in enumerate(data['networks']):
        interface = ET.SubElement(
            devices, 'interface', type='network' if network['mode'] == 'NAT' else 'bridge'
        )
        if network['mac']:
            ET.SubElement(interface, 'mac', address=network['mac'])
        if network['mode'] == 'NAT':
            ET.SubElement(interface, 'source', network='default')
        else:
            ET.SubElement(interface, 'source', bridge=network['bridge'] or 'br0')
        ET.SubElement(interface, 'model', type=network['model'])

    # 控制台
    console = ET.SubElement(devices, 'console', type='pty')
    ET.SubElement(console, 'target', type='serial', port='0')

    # 输入设备
    ET.SubElement(devices, 'input', type='tablet', bus='usb')
    ET.SubElement(devices, 'input', type='mouse', bus='ps2')

    # 图形 (VNC)
    graphics = ET.SubElement(
        devices, 'graphics', type='vnc', port='-1', autoport='yes', listen='0.0.0.0'
    )
    listen = ET.SubElement(graphics, 'listen', type='address')

    # 视频
    video = ET.SubElement(devices, 'video')
    ET.SubElement(video, 'model', type='qxl', ram='65536', vram='65536', vgamem='16384')

    # PCI 直通设备
    for hostdev in data['hostdevs']:
        hd = ET.SubElement(
            devices, 'hostdev', mode='subsystem', type='pci', managed='yes'
        )
        source = ET.SubElement(hd, 'source')
        # 解析 PCI 地址
        try:
            parts = hostdev['pci'].replace(',', ':').split(':')
            if len(parts) >= 4:
                addr = parts[3].split('.')
                ET.SubElement(
                    source, 'address',
                    domain=parts[0],
                    bus=parts[1],
                    slot=parts[2],
                    function=addr[1] if len(addr) > 1 else '0',
                )
        except (IndexError, ValueError):
            pass

    # USB 设备
    for usb in data['usb_devices']:
        if ':' in usb:
            vendor, product = usb.split(':')
            usb_elem = ET.SubElement(
                devices, 'hostdev', mode='subsystem', type='usb', managed='yes'
            )
            source = ET.SubElement(usb_elem, 'source')
            ET.SubElement(source, 'vendor', id=f'0x{vendor}')
            ET.SubElement(source, 'product', id=f'0x{product}')

    # 生成格式化的 XML
    xml_str = ET.tostring(domain, encoding='unicode')
    parsed = minidom.parseString(xml_str)
    return parsed.toprettyxml(indent='  ')
