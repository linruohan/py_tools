"""完整的 OS Tab 集成测试."""

import sys
sys.path.insert(0, 'D:\\codehub\\py_tools')

from utils.xml_generator import LibvirtXMLGenerator


def test_complete_os_tab_flow():
    """测试完整的 OS Tab 数据流：UI -> to_xml() -> VMConfig -> XML."""

    from model.vm_model.configs.os_booting_config import OSBootingConfig

    # 使用 OSBootingConfig 来正确生成配置
    os_config = OSBootingConfig()

    # 模拟从 UI 更新配置
    os_config.update({
        'type': 'hvm',
        'arch': 'x86_64',
        'machine': 'q35',
        'firmware': 'efi',
        'boot_devices': ['hd', 'cdrom', 'network'],
        'loader': {
            'path': '/path/to/loader',
            'readonly': True,
        },
        'nvram': {
            'type': 'file',
            'source': {'file': '/path/to/nvram'},
        },
        'varstore': {
            'path': '/path/to/varstore',
        },
        'bootmenu': {
            'enable': True,
            'timeout': 3000,
        },
        'bios': {
            'useserial': True,
            'rebootTimeout': 1000,
        },
        'smbios': {
            'mode': 'emulate',
        },
        'direct_kernel': {
            'kernel': '/boot/vmlinuz',
            'initrd': '/boot/initrd.img',
            'cmdline': 'quiet splash',
        },
    })

    # 转换为字典格式
    os_tab_xml_config = os_config.to_dict()

    # 构建完整的 VM 配置（模拟 vm_panel.py 的 collect_vm_data）
    vm_config = {
        'name': 'TestVM',
        'description': 'Test VM for OS Booting',
        'memory_allocation': {
            'memory': 4194304,  # 4GB
            'unit': 'KiB',
        },
        'cpu_allocation': {
            'vcpu': 4,
        },
        'os_booting': os_tab_xml_config,  # 使用 OSBootingConfig.to_dict() 的输出
    }

    # 生成 XML
    generator = LibvirtXMLGenerator()
    xml_str = generator.generate(vm_config)

    print("完整的 XML 输出:")
    print(xml_str)
    print()

    # 验证所有关键元素都存在
    checks = [
        ('<domain type="kvm">', 'domain 元素'),
        ('<name>TestVM</name>', 'VM 名称'),
        ('<description>Test VM for OS Booting</description>', '描述'),
        ('<memory unit="KiB">4194304</memory>', '内存配置'),
        ('<os firmware="efi">', 'OS 固件'),
        ('arch="x86_64"', 'arch 属性'),
        ('machine="q35"', 'machine 属性'),
        ('readonly="yes"', 'loader readonly 属性'),
        ('/path/to/loader', 'loader 路径'),
        ('<nvram type="file"', 'nvram 配置'),
        ('<source file="/path/to/nvram"/>', 'nvram source 文件'),
        ('<varstore path="/path/to/varstore"/>', 'varstore 配置'),
        ('<boot dev="hd"/>', 'hd 启动设备'),
        ('<boot dev="cdrom"/>', 'cdrom 启动设备'),
        ('<boot dev="network"/>', 'network 启动设备'),
        ('<bootmenu enable="yes" timeout="3000"/>', 'bootmenu 配置'),
        ('<bios useserial="yes" rebootTimeout="1000"/>', 'bios 配置'),
        # smbios mode='emulate' 是默认值，不会生成 XML
        ('<kernel>/boot/vmlinuz</kernel>', '内核路径'),
        ('<initrd>/boot/initrd.img</initrd>', 'initrd 路径'),
        ('<cmdline>quiet splash</cmdline>', '命令行参数'),
    ]

    for check_str, description in checks:
        if check_str in xml_str:
            print(f"[PASS] {description}: {check_str}")
        else:
            print(f"[FAIL] {description}: {check_str}")
            raise AssertionError(f"Missing {description} in XML")

    print("\n[PASS] Complete OS Tab flow test passed!")


def test_bootmenu_only_change():
    """测试仅点击 bootmenu 时，其他配置不丢失."""

    from model.vm_model.configs.os_booting_config import OSBootingConfig

    # 模拟用户先配置了 arch/machine/firmware 等
    # 然后点击 bootmenu 复选框
    os_config_before = OSBootingConfig()
    os_config_before.update({
        'type': 'hvm',
        'arch': 'x86_64',
        'machine': 'q35',
        'firmware': 'efi',
        'boot_devices': ['hd'],
        'loader': {'path': '/path/to/loader'},
        'nvram': {'source': {'file': '/path/to/nvram'}},
        'bootmenu': {
            'enable': False,  # 未勾选
        },
    })

    os_config_after = OSBootingConfig()
    os_config_after.update({
        'type': 'hvm',
        'arch': 'x86_64',
        'machine': 'q35',
        'firmware': 'efi',
        'boot_devices': ['hd'],
        'loader': {'path': '/path/to/loader'},
        'nvram': {'source': {'file': '/path/to/nvram'}},
        'bootmenu': {
            'enable': True,  # 勾选了
            'timeout': 3000,  # 使用默认超时值
        },
    })

    vm_config_before = {
        'name': 'TestVM',
        'os_booting': os_config_before.to_dict(),
    }

    vm_config_after = {
        'name': 'TestVM',
        'os_booting': os_config_after.to_dict(),
    }

    generator = LibvirtXMLGenerator()

    xml_before = generator.generate(vm_config_before)
    xml_after = generator.generate(vm_config_after)

    print("\nBootmenu 之前的 XML:")
    print(xml_before)
    print("\nBootmenu 之后的 XML:")
    print(xml_after)
    print()

    # 验证之前的配置包含基本元素
    assert 'arch="x86_64"' in xml_before, "Before: arch should be in XML"
    assert 'machine="q35"' in xml_before, "Before: machine should be in XML"
    assert 'firmware="efi"' in xml_before, "Before: firmware should be in XML"
    assert '/path/to/loader' in xml_before, "Before: loader should be in XML"
    assert '/path/to/nvram' in xml_before, "Before: nvram should be in XML"

    # 验证之后的配置保留所有之前的元素，并添加 bootmenu
    assert 'arch="x86_64"' in xml_after, "After: arch should still be in XML"
    assert 'machine="q35"' in xml_after, "After: machine should still be in XML"
    assert 'firmware="efi"' in xml_after, "After: firmware should still be in XML"
    assert '/path/to/loader' in xml_after, "After: loader should still be in XML"
    assert '/path/to/nvram' in xml_after, "After: nvram should still be in XML"
    assert '<bootmenu enable="yes"' in xml_after, "After: bootmenu should be added"

    print("[PASS] Bootmenu-only change test passed!")


if __name__ == '__main__':
    test_complete_os_tab_flow()
    test_bootmenu_only_change()
    print("\n[SUCCESS] All integration tests passed!")
