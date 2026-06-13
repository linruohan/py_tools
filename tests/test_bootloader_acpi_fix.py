"""测试 bootloader 和 ACPI 表修复."""

import sys
sys.path.insert(0, 'D:\\codehub\\py_tools')

from panels.vm_panel.tabs.os_tab import OSTab
import customtkinter as ctk


def test_bootloader_config_generation():
    """测试 bootloader 和 bootloader_args 配置生成."""
    print("\n=== 测试 bootloader 配置生成 ===")

    # 创建虚拟的 master 组件
    root = ctk.CTk()
    root.withdraw()  # 隐藏窗口

    os_tab = OSTab(root)

    # 模拟用户输入
    os_tab.bootloader_entry.insert(0, '/usr/bin/pygrub')
    os_tab.bootloader_args_entry.insert(0, '--append single')

    # 获取配置
    config = os_tab.get_config()

    # 验证 bootloader 和 bootloader_args 是否在配置中
    assert 'bootloader' in config, "配置中应该包含 bootloader 字段"
    assert 'bootloader_args' in config, "配置中应该包含 bootloader_args 字段"
    assert config['bootloader'] == '/usr/bin/pygrub', f"bootloader 值不正确:{config['bootloader']}"
    assert config['bootloader_args'] == '--append single', f"bootloader_args 值不正确:{config['bootloader_args']}"

    print(f"✓ bootloader: {config['bootloader']}")
    print(f"✓ bootloader_args: {config['bootloader_args']}")

    # 测试 to_xml() 方法
    xml_config = os_tab.to_xml()
    os_booting = xml_config.get('os_booting', {})

    # 验证 XML 配置中包含 host_bootloader
    assert 'host_bootloader' in os_booting, "XML 配置中应该包含 host_bootloader 字段"
    assert os_booting['host_bootloader']['path'] == '/usr/bin/pygrub', f"XML bootloader path 值不正确:{os_booting['host_bootloader']['path']}"
    assert os_booting['host_bootloader']['args'] == '--append single', f"XML bootloader args 值不正确:{os_booting['host_bootloader']['args']}"

    print(f"✓ XML host_bootloader: {os_booting['host_bootloader']}")

    root.destroy()
    print("[PASS] bootloader 配置生成测试通过!\n")


def test_acpi_tables_generation():
    """测试多个 ACPI 表配置生成."""
    print("=== 测试 ACPI 表配置生成 ===")

    # 创建虚拟的 master 组件
    root = ctk.CTk()
    root.withdraw()  # 隐藏窗口

    os_tab = OSTab(root)

    # 清除默认的 ACPI 表
    if hasattr(os_tab, 'acpi_tables'):
        for table in os_tab.acpi_tables:
            table['type'].destroy()
            table['path'].destroy()
            table['type_label'].destroy()
            table['path_label'].destroy()
            table['frame'].destroy()
        os_tab.acpi_tables = []

    # 添加第一个 ACPI 表
    os_tab._add_acpi_table()
    os_tab.acpi_tables[0]['type'].set('slic')
    os_tab.acpi_tables[0]['path'].insert(0, '/path/to/slic.dat')

    # 添加第二个 ACPI 表
    os_tab._add_acpi_table()
    os_tab.acpi_tables[1]['type'].set('msdm')
    os_tab.acpi_tables[1]['path'].insert(0, '/path/to/msdm.dat')

    # 添加第三个 ACPI 表
    os_tab._add_acpi_table()
    os_tab.acpi_tables[2]['type'].set('raw')
    os_tab.acpi_tables[2]['path'].insert(0, '/path/to/raw.dat')

    # 获取配置
    config = os_tab.get_config()

    # 验证 acpi_tables 字段
    assert 'acpi_tables' in config, "配置中应该包含 acpi_tables 字段"
    assert len(config['acpi_tables']) == 3, f"应该有 3 个 ACPI 表,实际有 {len(config['acpi_tables'])} 个"

    print(f"✓ ACPI 表数量:{len(config['acpi_tables'])}")
    for i, table in enumerate(config['acpi_tables']):
        print(f"  表{i+1}: type={table['type']}, path={table['path']}")

    # 验证每个表的值
    assert config['acpi_tables'][0]['type'] == 'slic', f"第一个表 type 不正确"
    assert config['acpi_tables'][0]['path'] == '/path/to/slic.dat', f"第一个表 path 不正确"
    assert config['acpi_tables'][1]['type'] == 'msdm', f"第二个表 type 不正确"
    assert config['acpi_tables'][1]['path'] == '/path/to/msdm.dat', f"第二个表 path 不正确"
    assert config['acpi_tables'][2]['type'] == 'raw', f"第三个表 type 不正确"
    assert config['acpi_tables'][2]['path'] == '/path/to/raw.dat', f"第三个表 path 不正确"

    # 测试 to_xml() 方法
    xml_config = os_tab.to_xml()
    os_booting = xml_config.get('os_booting', {})

    # 验证 XML 配置中包含 tables 数组
    assert 'acpi' in os_booting, "XML 配置中应该包含 acpi 字段"
    assert 'tables' in os_booting['acpi'], "XML acpi 中应该包含 tables 字段"
    assert len(os_booting['acpi']['tables']) == 3, f"XML 中应该有 3 个 ACPI 表"

    print(f"✓ XML ACPI tables 数量:{len(os_booting['acpi']['tables'])}")
    for i, table in enumerate(os_booting['acpi']['tables']):
        print(f"  表{i+1}: type={table['type']}, path={table['path']}")

    root.destroy()
    print("[PASS] ACPI 表配置生成测试通过!\n")


def test_acpi_table_load():
    """测试加载多个 ACPI 表配置."""
    print("=== 测试加载 ACPI 表配置 ===")

    # 创建虚拟的 master 组件
    root = ctk.CTk()
    root.withdraw()  # 隐藏窗口

    os_tab = OSTab(root)

    # 模拟从 XML 加载的配置
    config = {
        'acpi': {
            'tables': [
                {'type': 'slic', 'path': '/path/to/slic.dat'},
                {'type': 'msdm', 'path': '/path/to/msdm.dat'},
                {'type': 'raw', 'path': '/path/to/raw.dat'},
            ]
        }
    }

    # 加载配置
    os_tab.load_config(config)

    # 验证加载后的表数量
    assert hasattr(os_tab, 'acpi_tables'), "应该有 acpi_tables 属性"
    assert len(os_tab.acpi_tables) == 3, f"应该有 3 个 ACPI 表,实际有 {len(os_tab.acpi_tables)} 个"

    print(f"✓ 加载的 ACPI 表数量:{len(os_tab.acpi_tables)}")

    # 验证每个表的值
    assert os_tab.acpi_tables[0]['type'].get() == 'slic', f"第一个表 type 不正确"
    assert os_tab.acpi_tables[0]['path'].get() == '/path/to/slic.dat', f"第一个表 path 不正确"
    assert os_tab.acpi_tables[1]['type'].get() == 'msdm', f"第二个表 type 不正确"
    assert os_tab.acpi_tables[1]['path'].get() == '/path/to/msdm.dat', f"第二个表 path 不正确"
    assert os_tab.acpi_tables[2]['type'].get() == 'raw', f"第三个表 type 不正确"
    assert os_tab.acpi_tables[2]['path'].get() == '/path/to/raw.dat', f"第三个表 path 不正确"

    for i, table in enumerate(os_tab.acpi_tables):
        print(f"  表{i+1}: type={table['type'].get()}, path={table['path'].get()}")

    root.destroy()
    print("[PASS] 加载 ACPI 表配置测试通过!\n")


if __name__ == '__main__':
    test_bootloader_config_generation()
    test_acpi_tables_generation()
    test_acpi_table_load()

    print("\n" + "="*50)
    print("[SUCCESS] 所有 bootloader 和 ACPI 表修复测试通过!")
    print("="*50)
