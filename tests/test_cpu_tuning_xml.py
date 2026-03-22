"""测试 CPU 调优 XML 生成功能."""

import sys

sys.path.insert(0, 'D:/codehub/py_tools')

from utils.xml_generator import LibvirtXMLGenerator


def test_full_cpu_tuning_xml():
    """测试完整的 CPU 调优 XML 生成."""

    config = {
        'hypervisor': 'kvm',
        'name': 'test-vm',
        'cpu_allocation': {'max_vcpu': 4},
        'memory_allocation': {'memory': 2097152, 'unit': 'KiB'},
        'os_booting': {'type': 'hvm'},
        'devices': {},
        'cpu_tuning': {
            'vcpupin': [
                {'vcpu': '0', 'cpuset': '1-4,^2'},
                {'vcpu': '1', 'cpuset': '0,1'},
                {'vcpu': '2', 'cpuset': '2,3'},
                {'vcpu': '3', 'cpuset': '0,4'},
            ],
            'emulatorpin': '1-3',
            'iothreadpin': [
                {'iothread': '1', 'cpuset': '5,6'},
                {'iothread': '2', 'cpuset': '7,8'},
            ],
            'shares': 2048,
            'period': 1000000,
            'quota': -1,
            'global_period': 1000000,
            'global_quota': -1,
            'emulator_period': 1000000,
            'emulator_quota': -1,
            'iothread_period': 1000000,
            'iothread_quota': -1,
            'vcpusched': {
                'vcpus': '0-4,^3',
                'scheduler': 'fifo',
                'priority': 1,
            },
            'cachetune': [
                {
                    'vcpus': '0-3',
                    'cache': {'level': 3, 'type': 'both', 'size': 3, 'unit': 'MiB'},
                    'monitor': {'level': 3, 'vcpus': '1'},
                },
            ],
            'memorytune': [
                {'vcpus': '0-3', 'node': {'id': 0, 'bandwidth': 60}},
            ],
        },
    }

    generator = LibvirtXMLGenerator()
    xml_str = generator.generate(config)

    print("=" * 60)
    print("完整 CPU 调优配置 XML:")
    print("=" * 60)

    # 只打印 cputune 部分
    for line in xml_str.split('\n'):
        if '<cputune>' in line or '</cputune>' in line or (line.strip() and 'cputune' not in line and any(x in line for x in [
            'vcpupin', 'emulatorpin', 'iothreadpin', 'shares', 'period', 'quota',
            'global_', 'emulator_', 'iothread_', 'vcpusched', 'cachetune', 'memorytune',
            'cache ', 'monitor', 'node '
        ])):
            print(line)

    # 验证
    checks = [
        ('vcpupin', '<vcpupin vcpu="0" cpuset="1-4,^2"/>' in xml_str),
        ('emulatorpin', '<emulatorpin cpuset="1-3"/>' in xml_str),
        ('iothreadpin', '<iothreadpin iothread="1" cpuset="5,6"/>' in xml_str),
        ('shares', '<shares>2048</shares>' in xml_str),
        ('period/quota', '<period>1000000</period>' in xml_str and '<quota>-1</quota>' in xml_str),
        ('global_period/quota', '<global_period>1000000</global_period>' in xml_str),
        ('emulator_period/quota', '<emulator_period>1000000</emulator_period>' in xml_str),
        ('iothread_period/quota', '<iothread_period>1000000</iothread_period>' in xml_str),
        ('vcpusched', 'scheduler="fifo"' in xml_str and 'priority="1"' in xml_str),
        ('cachetune', '<cachetune vcpus="0-3">' in xml_str),
        ('cache', 'level="3"' in xml_str and 'size="3"' in xml_str),
        ('monitor', '<monitor level=' in xml_str),
        ('memorytune', '<memorytune vcpus="0-3">' in xml_str),
        ('node bandwidth', 'bandwidth="60"' in xml_str),
    ]

    print("\n验证结果:")
    passed = failed = 0
    for name, result in checks:
        status = "PASS" if result else "FAIL"
        if result:
            passed += 1
        else:
            failed += 1
        print(f"  {status}: {name}")

    print(f"\n总计：{passed} 通过，{failed} 失败")
    return failed == 0


def test_emulatorsched_xml():
    """测试 emulatorsched XML 生成."""

    config = {
        'hypervisor': 'kvm',
        'name': 'test-vm',
        'cpu_allocation': {'max_vcpu': 2},
        'memory_allocation': {'memory': 1048576, 'unit': 'KiB'},
        'os_booting': {'type': 'hvm'},
        'devices': {},
        'cpu_tuning': {
            'emulatorsched': {
                'scheduler': 'rr',
                'priority': 50,
            },
        },
    }

    generator = LibvirtXMLGenerator()
    xml_str = generator.generate(config)

    print("\n" + "=" * 60)
    print("emulatorsched XML:")
    print("=" * 60)

    for line in xml_str.split('\n'):
        if '<cputune>' in line or '</cputune>' in line or 'emulatorsched' in line:
            print(line)

    checks = [
        ('emulatorsched', '<emulatorsched' in xml_str),
        ('scheduler="rr"', 'scheduler="rr"' in xml_str),
        ('priority="50"', 'priority="50"' in xml_str),
    ]

    print("\n验证结果:")
    passed = failed = 0
    for name, result in checks:
        status = "PASS" if result else "FAIL"
        if result:
            passed += 1
        else:
            failed += 1
        print(f"  {status}: {name}")

    return failed == 0


def test_minimal_xml():
    """测试最小配置 XML 生成（仅 vcpupin）."""

    config = {
        'hypervisor': 'kvm',
        'name': 'minimal-vm',
        'cpu_allocation': {'max_vcpu': 2},
        'memory_allocation': {'memory': 1048576, 'unit': 'KiB'},
        'os_booting': {'type': 'hvm'},
        'devices': {},
        'cpu_tuning': {
            'vcpupin': [
                {'vcpu': '0', 'cpuset': '0'},
                {'vcpu': '1', 'cpuset': '1'},
            ],
        },
    }

    generator = LibvirtXMLGenerator()
    xml_str = generator.generate(config)

    print("\n" + "=" * 60)
    print("最小配置 XML (仅 vcpupin):")
    print("=" * 60)

    for line in xml_str.split('\n'):
        if '<cputune>' in line or '</cputune>' in line or 'vcpupin' in line:
            print(line)

    checks = [
        ('vcpupin vcpu="0"', '<vcpupin vcpu="0" cpuset="0"/>' in xml_str),
        ('vcpupin vcpu="1"', '<vcpupin vcpu="1" cpuset="1"/>' in xml_str),
    ]

    print("\n验证结果:")
    passed = failed = 0
    for name, result in checks:
        status = "PASS" if result else "FAIL"
        if result:
            passed += 1
        else:
            failed += 1
        print(f"  {status}: {name}")

    return failed == 0


if __name__ == '__main__':
    print("CPU 调优 XML 生成测试\n")

    result1 = test_full_cpu_tuning_xml()
    result2 = test_emulatorsched_xml()
    result3 = test_minimal_xml()

    print("\n" + "=" * 60)
    if result1 and result2 and result3:
        print("所有测试通过!")
    else:
        print("部分测试失败!")
    print("=" * 60)
