"""测试 OS Booting Tab 数据流."""

import sys
sys.path.insert(0, 'D:\\codehub\\py_tools')

from model.vm_model.configs.os_booting_config import OSBootingConfig


def test_os_booting_config_update():
    """测试 OSBootingConfig.update() 方法."""
    config = OSBootingConfig()

    # 模拟从 UI 传来的配置数据
    test_data = {
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

    config.update(test_data)

    # 验证配置是否正确更新
    assert config.arch == 'x86_64', f"Expected arch='x86_64', got '{config.arch}'"
    assert config.machine == 'q35', f"Expected machine='q35', got '{config.machine}'"
    assert config.firmware == 'efi', f"Expected firmware='efi', got '{config.firmware}'"
    assert len(config.boot_devices) == 2, f"Expected 2 boot devices, got {len(config.boot_devices)}"
    assert config.bootmenu.enable == True, f"Expected bootmenu.enable=True, got {config.bootmenu.enable}"
    assert config.bootmenu.timeout == 3000, f"Expected bootmenu.timeout=3000, got {config.bootmenu.timeout}"
    assert config.loader.path == '/path/to/loader', f"Expected loader.path='/path/to/loader', got '{config.loader.path}'"
    assert config.nvram.path == '/path/to/nvram', f"Expected nvram.path='/path/to/nvram', got '{config.nvram.path}'"
    assert config.bios.useserial == True, f"Expected bios.useserial=True, got {config.bios.useserial}"
    assert config.bios.rebootTimeout == 1000, f"Expected bios.rebootTimeout=1000, got {config.bios.rebootTimeout}"

    print("[PASS] OSBootingConfig.update() test passed!")

    # 测试 to_dict() 方法
    result = config.to_dict()

    assert result['arch'] == 'x86_64', f"Expected arch='x86_64' in to_dict, got '{result.get('arch')}'"
    assert result['machine'] == 'q35', f"Expected machine='q35' in to_dict, got '{result.get('machine')}'"
    assert result['firmware'] == 'efi', f"Expected firmware='efi' in to_dict, got '{result.get('firmware')}'"
    assert 'bootmenu' in result, "Expected 'bootmenu' in to_dict"
    assert result['bootmenu']['enable'] == True, f"Expected bootmenu.enable=True in to_dict, got {result['bootmenu']['enable']}"
    assert result['bootmenu']['timeout'] == 3000, f"Expected bootmenu.timeout=3000 in to_dict, got {result['bootmenu']['timeout']}"

    print("[PASS] OSBootingConfig.to_dict() test passed!")

    # 测试空 arch/machine 值
    config2 = OSBootingConfig()
    config2.arch = ''
    config2.machine = ''
    result2 = config2.to_dict()

    assert result2['arch'] is None, f"Expected arch=None for empty string, got '{result2.get('arch')}'"
    assert result2['machine'] is None, f"Expected machine=None for empty string, got '{result2.get('machine')}'"

    print("[PASS] Empty arch/machine test passed!")

    print("\n[SUCCESS] All OS Booting Config tests passed!")


def test_vm_config_integration():
    """测试 VMConfig 与 OSBootingConfig 的集成."""
    from model.vm_model.core.vm_config import VMConfig

    vm_config = VMConfig()

    # 模拟从 OS Tab 传来的数据
    os_tab_data = {
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
            },
            'nvram': {
                'path': '/path/to/nvram',
                'type': 'file',
            },
        }
    }

    vm_config.update_from_tab('os_booting', os_tab_data['os_booting'])

    # 验证配置是否正确传递
    assert vm_config.os.arch == 'x86_64', f"Expected vm_config.os.arch='x86_64', got '{vm_config.os.arch}'"
    assert vm_config.os.machine == 'q35', f"Expected vm_config.os.machine='q35', got '{vm_config.os.machine}'"
    assert vm_config.os.firmware == 'efi', f"Expected vm_config.os.firmware='efi', got '{vm_config.os.firmware}'"
    assert vm_config.os.bootmenu.enable == True, f"Expected bootmenu.enable=True, got {vm_config.os.bootmenu.enable}"

    # 验证 to_dict() 输出
    result = vm_config.to_dict()
    os_booting = result.get('os_booting', {})

    assert os_booting.get('arch') == 'x86_64', f"Expected arch='x86_64' in vm_config.to_dict, got '{os_booting.get('arch')}'"
    assert os_booting.get('machine') == 'q35', f"Expected machine='q35' in vm_config.to_dict, got '{os_booting.get('machine')}'"
    assert os_booting.get('firmware') == 'efi', f"Expected firmware='efi' in vm_config.to_dict, got '{os_booting.get('firmware')}'"
    assert 'bootmenu' in os_booting, "Expected 'bootmenu' in vm_config.to_dict"

    print("[PASS] VMConfig integration test passed!")
    print("\n[SUCCESS] All integration tests passed!")


if __name__ == '__main__':
    test_os_booting_config_update()
    test_vm_config_integration()
