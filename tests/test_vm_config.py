"""测试虚拟机配置类 - 使用当前模型结构."""

from model.vm_model.core.vm_config import VMConfig
from model.vm_model.configs.basic_config import BasicConfig
from model.vm_model.configs.memory_allocation_config import MemoryAllocationConfig
from model.vm_model.configs.throttlegroups import ThrottleGroups, ThrottleGroup
from utils.xml_generator import LibvirtXMLGenerator, XMLGenerationError


def test_vmconfig_init():
    """测试 VMConfig 初始化."""
    config = VMConfig()
    assert config.basic is not None
    assert config.cpu is not None
    assert config.memory is not None
    assert config.os is not None
    assert config.devices is not None
    assert config.hypervisor == 'kvm'


def test_vmconfig_validate_valid():
    """测试有效配置的验证."""
    config = VMConfig()
    config.basic.name = 'test-vm'
    is_valid, msg = config.validate()
    assert is_valid, f'应该有效，但得到: {msg}'


def test_vmconfig_validate_empty_name():
    """测试空名称的验证."""
    config = VMConfig()
    config.basic.name = ''
    is_valid, msg = config.validate()
    assert not is_valid
    assert '名称' in msg


def test_vmconfig_to_dict():
    """测试配置转换为字典."""
    config = VMConfig()
    config.basic.name = 'test-vm'
    d = config.to_dict()
    assert isinstance(d, dict)
    assert d.get('name') == 'test-vm'


def test_vmconfig_update_from_tab_basic():
    """测试从 Tab 更新基础配置."""
    config = VMConfig()
    config.update_from_tab('general_metadata', {'name': 'my-vm'})
    assert config.basic.name == 'my-vm'


def test_vmconfig_update_from_tab_memory():
    """测试从 Tab 更新内存配置."""
    config = VMConfig()
    config.update_from_tab('memory_allocation', {
        'memory_allocation': {'memory': 4096, 'unit': 'MiB'}
    })
    assert config.memory.memory == 4096


def test_vmconfig_reset():
    """测试配置重置."""
    config = VMConfig()
    config.basic.name = 'changed-name'
    config.reset()
    assert config.basic.name == 'vm0'


def test_vmconfig_get_summary():
    """测试获取配置摘要."""
    config = VMConfig()
    config.basic.name = 'summary-vm'
    summary = config.get_summary()
    assert isinstance(summary, dict)
    assert summary['name'] == 'summary-vm'


def test_throttlegroup_config():
    """测试节流组配置."""
    groups = ThrottleGroups()
    group = ThrottleGroup(
        name='limit0',
        total_bytes_sec=10_000_000,
        read_iops_sec=400_000,
        write_iops_sec=100_000,
    )
    groups.throttlegroups.append(group)
    assert len(groups.throttlegroups) == 1
    assert groups.throttlegroups[0].name == 'limit0'


def test_xml_generator_basic():
    """测试 XML 生成器基础功能."""
    gen = LibvirtXMLGenerator()
    config = VMConfig()
    config.basic.name = 'xml-test-vm'
    xml = gen.generate(config.to_dict())
    assert '<domain' in xml
    assert 'xml-test-vm' in xml


def test_xml_generator_error_handling():
    """测试 XML 生成器异常处理."""
    gen = LibvirtXMLGenerator()
    # 传入非字典类型应该触发异常处理
    try:
        gen.generate(None)  # type: ignore
        assert False, '应该抛出异常'
    except (XMLGenerationError, TypeError, AttributeError):
        pass  # 预期的异常


def test_basic_config_update():
    """测试 BasicConfig 更新."""
    cfg = BasicConfig()
    cfg.update({'name': 'updated-vm', 'arch': 'arm'})
    assert cfg.name == 'updated-vm'
    assert cfg.arch == 'arm'


def test_memory_config():
    """测试内存配置."""
    mem = MemoryAllocationConfig()
    assert mem.memory > 0
    d = mem.to_dict()
    assert 'memory' in d
