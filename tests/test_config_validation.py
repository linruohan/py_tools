"""测试配置验证功能."""

from vm.model.core.vm_config import VMConfig
from vm.model.cpu.topology import CPUTopology


def test_validate_empty_name():
    """测试空名称验证."""
    config = VMConfig()
    config.basic.name = ''
    is_valid, errors = config.validate()
    assert not is_valid
    assert '虚拟机名称不能为空' in errors


def test_validate_invalid_name_chars():
    """测试无效字符验证."""
    config = VMConfig()
    config.basic.name = 'invalid@name!'
    is_valid, errors = config.validate()
    assert not is_valid
    assert any('只能包含字母' in err for err in errors)


def test_validate_valid_name():
    """测试有效名称验证."""
    config = VMConfig()
    config.basic.name = 'valid-vm_name123'
    is_valid, errors = config.validate()
    assert is_valid
    assert len(errors) == 0


def test_validate_memory_too_small():
    """测试内存过小警告."""
    config = VMConfig()
    config.basic.name = 'test-vm'
    # 设置为 256MB (注意单位是 KiB,所以 256MB = 262144 KiB)
    # 但要小于默认的 current_memory,所以需要同时设置 current_memory
    config.memory.memory = 256 * 1024  # 256MB in KiB
    config.memory.current_memory = 128 * 1024  # 128MB in KiB, less than memory
    is_valid, errors = config.validate()
    # 应该通过(只是警告,不是错误)
    assert is_valid
    # 警告不应该出现在错误列表中
    assert len(errors) == 0


def test_validate_memory_zero():
    """测试零内存验证."""
    config = VMConfig()
    config.basic.name = 'test-vm'
    config.memory.memory = 0
    is_valid, errors = config.validate()
    assert not is_valid
    assert '内存大小必须大于 0' in errors


def test_validate_cpu_too_large():
    """测试 CPU 数量过大警告."""
    config = VMConfig()
    config.basic.name = 'test-vm'
    config.cpu.max_vcpu = 300  # 超过 256
    # 需要重置 current_memory 和 topology 以避免验证失败
    config.memory.current_memory = None
    config.cpu.topology = None  # 清除拓扑以避免不匹配错误
    is_valid, errors = config.validate()
    # 应该通过(只是警告,不是错误)
    assert is_valid
    # 警告不应该出现在错误列表中
    assert len(errors) == 0


def test_validate_cpu_zero():
    """测试零 CPU 验证."""
    config = VMConfig()
    config.basic.name = 'test-vm'
    config.cpu.max_vcpu = 0
    is_valid, errors = config.validate()
    assert not is_valid
    assert 'CPU 数量必须大于 0' in errors


def test_validate_current_memory_exceeds_max():
    """测试当前内存超过最大内存验证."""
    config = VMConfig()
    config.basic.name = 'test-vm'
    config.memory.memory = 2048
    config.memory.current_memory = 4096  # 大于 memory
    is_valid, errors = config.validate()
    assert not is_valid
    assert '当前内存不能大于最大内存' in errors


def test_validate_cpu_topology_mismatch():
    """测试 CPU 拓扑不匹配验证."""
    config = VMConfig()
    config.basic.name = 'test-vm'
    config.cpu.max_vcpu = 4
    # 设置不匹配的拓扑:2 sockets * 2 cores * 2 threads = 8 != 4
    config.cpu.topology = CPUTopology(sockets=2, cores=2, threads=2)
    is_valid, errors = config.validate()
    assert not is_valid
    assert any('CPU 拓扑不匹配' in err for err in errors)


def test_validate_cpu_topology_match():
    """测试 CPU 拓扑匹配验证."""
    config = VMConfig()
    config.basic.name = 'test-vm'
    config.cpu.max_vcpu = 8
    # 设置匹配的拓扑:2 sockets * 2 cores * 2 threads = 8
    config.cpu.topology = CPUTopology(sockets=2, cores=2, threads=2)
    is_valid, errors = config.validate()
    assert is_valid
    assert len(errors) == 0


def test_validate_direct_kernel_without_kernel():
    """测试直接内核模式缺少内核路径验证."""
    config = VMConfig()
    config.basic.name = 'test-vm'
    config.os.type = 'direct_kernel'
    config.os.kernel = ''  # 空内核路径
    is_valid, errors = config.validate()
    assert not is_valid
    assert len(errors) > 0
    assert any('必须指定内核路径' in err for err in errors)


def test_validate_direct_kernel_with_kernel():
    """测试直接内核模式有内核路径验证."""
    config = VMConfig()
    config.basic.name = 'test-vm'
    config.os.type = 'direct_kernel'
    config.os.kernel = '/path/to/kernel'
    is_valid, errors = config.validate()
    assert is_valid
    assert len(errors) == 0


def test_validate_multiple_errors():
    """测试多个验证错误."""
    config = VMConfig()
    config.basic.name = ''  # 空名称
    config.memory.memory = 0  # 零内存
    config.cpu.max_vcpu = 0  # 零 CPU
    is_valid, errors = config.validate()
    assert not is_valid
    assert len(errors) >= 3
    assert '虚拟机名称不能为空' in errors
    assert '内存大小必须大于 0' in errors
    assert 'CPU 数量必须大于 0' in errors


def test_validate_valid_config():
    """测试有效配置验证."""
    config = VMConfig()
    config.basic.name = 'test-vm'
    # 使用 KiB 单位,2GB = 2097152 KiB
    config.memory.memory = 2 * 1024 * 1024  # 2GB in KiB
    config.memory.current_memory = None  # 避免验证失败
    config.cpu.max_vcpu = 2
    config.os.type = 'hvm'
    is_valid, errors = config.validate()
    assert is_valid
    assert len(errors) == 0
