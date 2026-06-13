"""测试 CPU 调优 XML 生成功能."""

from utils.xml_generator import LibvirtXMLGenerator


def _make_config(cpu_tuning: dict, vcpu: int = 4, name: str = 'test-vm') -> dict:
    """构建测试用配置字典."""
    return {
        'hypervisor': 'kvm',
        'name': name,
        'cpu_allocation': {'max_vcpu': vcpu},
        'memory_allocation': {'memory': 2097152, 'unit': 'KiB'},
        'os_booting': {'type': 'hvm'},
        'devices': {},
        'cpu_tuning': cpu_tuning,
    }


def test_full_cpu_tuning_xml():
    """测试完整的 CPU 调优 XML 生成."""
    config = _make_config({
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
        'vcpusched': {'vcpus': '0-4,^3', 'scheduler': 'fifo', 'priority': 1},
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
    })

    xml = LibvirtXMLGenerator().generate(config)

    assert '<vcpupin vcpu="0" cpuset="1-4,^2"/>' in xml
    assert '<emulatorpin cpuset="1-3"/>' in xml
    assert '<iothreadpin iothread="1" cpuset="5,6"/>' in xml
    assert '<shares>2048</shares>' in xml
    assert '<period>1000000</period>' in xml
    assert '<quota>-1</quota>' in xml
    assert '<global_period>1000000</global_period>' in xml
    assert '<emulator_period>1000000</emulator_period>' in xml
    assert '<iothread_period>1000000</iothread_period>' in xml
    assert 'scheduler="fifo"' in xml
    assert 'priority="1"' in xml
    assert '<cachetune vcpus="0-3">' in xml
    assert 'level="3"' in xml
    assert 'size="3"' in xml
    assert '<monitor level=' in xml
    assert '<memorytune vcpus="0-3">' in xml
    assert 'bandwidth="60"' in xml


def test_emulatorsched_xml():
    """测试 emulatorsched XML 生成."""
    config = _make_config(
        {'emulatorsched': {'scheduler': 'rr', 'priority': 50}},
        vcpu=2,
    )
    xml = LibvirtXMLGenerator().generate(config)

    assert '<emulatorsched' in xml
    assert 'scheduler="rr"' in xml
    assert 'priority="50"' in xml


def test_minimal_xml():
    """测试最小配置 XML 生成(仅 vcpupin)."""
    config = _make_config(
        {'vcpupin': [{'vcpu': '0', 'cpuset': '0'}, {'vcpu': '1', 'cpuset': '1'}]},
        vcpu=2,
        name='minimal-vm',
    )
    xml = LibvirtXMLGenerator().generate(config)

    assert '<vcpupin vcpu="0" cpuset="0"/>' in xml
    assert '<vcpupin vcpu="1" cpuset="1"/>' in xml
