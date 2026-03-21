"""测试 XML 生成器."""

import sys
sys.path.insert(0, 'D:\\codehub\\py_tools')

from utils.xml_generator import LibvirtXMLGenerator


def test_xml_generation():
    """测试从配置生成 XML."""

    # 模拟从 VMConfig.to_dict() 返回的数据
    vm_config = {
        'os_booting': {
            'type': 'hvm',
            'arch': 'x86_64',
            'machine': 'q35',
            'firmware': 'efi',
            'boot_devices': ['hd', 'cdrom'],
            'bootmenu': {
                'enable': True,
                'timeout': 3000,
            },
            'loader': {
                'path': '/path/to/loader',
                'readonly': True,
                'secure': False,
            },
            'nvram': {
                'path': '/path/to/nvram',
                'type': 'file',
            },
            'bios': {
                'useserial': True,
                'rebootTimeout': 1000,
            },
        }
    }

    generator = LibvirtXMLGenerator()
    xml_str = generator.generate(vm_config)

    print("生成的 XML:")
    print(xml_str)
    print()

    # 验证 XML 内容
    assert '<os' in xml_str, "Expected <os> element in XML"
    assert 'arch="x86_64"' in xml_str, 'Expected arch="x86_64" in XML'
    assert 'machine="q35"' in xml_str, 'Expected machine="q35" in XML'
    assert '<boot' in xml_str, "Expected <boot> elements in XML"
    assert 'hd' in xml_str, "Expected hd boot device in XML"
    assert 'cdrom' in xml_str, "Expected cdrom boot device in XML"
    assert '<bootmenu' in xml_str, "Expected <bootmenu> element in XML"
    assert 'enable="yes"' in xml_str, 'Expected bootmenu enable="yes" in XML'
    assert 'timeout="3000"' in xml_str, 'Expected timeout="3000" in XML'
    assert '<loader' in xml_str, "Expected <loader> element in XML"
    assert 'readonly="yes"' in xml_str, 'Expected loader readonly="yes" in XML'
    assert '<nvram' in xml_str, "Expected <nvram> element in XML"
    assert '<bios' in xml_str, "Expected <bios> element in XML"
    assert 'useserial="yes"' in xml_str, 'Expected bios useserial="yes" in XML'
    assert 'rebootTimeout="1000"' in xml_str, 'Expected rebootTimeout="1000" in XML'

    print("[PASS] XML generation test passed!")


def test_empty_arch_machine():
    """测试空 arch/machine 值不生成属性."""

    vm_config = {
        'os_booting': {
            'type': 'hvm',
            'arch': None,  # 空值
            'machine': None,  # 空值
            'boot_devices': ['hd'],
        }
    }

    generator = LibvirtXMLGenerator()
    xml_str = generator.generate(vm_config)

    print("\n空 arch/machine 的 XML:")
    print(xml_str)
    print()

    # 验证不包含 arch 和 machine 属性
    assert 'arch=' not in xml_str, "Expected no arch attribute in XML when arch is None"
    assert 'machine=' not in xml_str, "Expected no machine attribute in XML when machine is None"
    # 但应该有 <type>hvm</type>
    assert '<type>hvm</type>' in xml_str, "Expected <type>hvm</type> in XML"

    print("[PASS] Empty arch/machine test passed!")


if __name__ == '__main__':
    test_xml_generation()
    test_empty_arch_machine()
    print("\n[SUCCESS] All XML generation tests passed!")
