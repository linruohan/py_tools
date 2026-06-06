"""测试 utils/xml_generator.py 的 XML 生成功能."""

import xml.etree.ElementTree as ET

import pytest

from utils.xml_generator import LibvirtXMLGenerator, XMLGenerationError


def _gen(config: dict) -> str:
    """快捷生成 XML."""
    return LibvirtXMLGenerator().generate(config)


def _base(overrides: dict | None = None) -> dict:
    """构建最小有效配置."""
    cfg = {
        'hypervisor': 'kvm',
        'name': 'test-vm',
        'cpu_allocation': {'max_vcpu': 2},
        'memory_allocation': {'memory': 2097152, 'unit': 'KiB'},
        'os_booting': {'type': 'hvm'},
        'devices': {},
    }
    if overrides:
        cfg.update(overrides)
    return cfg


# ── 基础结构 ──────────────────────────────────────────────────────────────────

class TestBasicStructure:
    def test_domain_element(self):
        xml = _gen(_base())
        assert '<domain type="kvm"' in xml

    def test_name_element(self):
        xml = _gen(_base({'name': 'my-vm'}))
        assert '<name>my-vm</name>' in xml

    def test_valid_xml(self):
        xml = _gen(_base())
        # 应该能被 ET 解析
        root = ET.fromstring(xml)
        assert root.tag == 'domain'

    def test_hypervisor_type(self):
        xml = _gen(_base({'hypervisor': 'qemu'}))
        assert 'type="qemu"' in xml

    def test_default_hypervisor_kvm(self):
        cfg = _base()
        del cfg['hypervisor']
        xml = _gen(cfg)
        assert 'type="kvm"' in xml


# ── 内存配置 ──────────────────────────────────────────────────────────────────

class TestMemoryGeneration:
    def test_memory_element_present(self):
        xml = _gen(_base())
        assert '<memory' in xml

    def test_memory_unit_attribute(self):
        xml = _gen(_base({'memory_allocation': {'memory': 2097152, 'unit': 'KiB'}}))
        assert 'unit="KiB"' in xml

    def test_current_memory(self):
        xml = _gen(_base({'memory_allocation': {
            'memory': 2097152,
            'unit': 'KiB',
            'current_memory': 1048576,
        }}))
        assert '<currentMemory' in xml


# ── CPU 配置 ──────────────────────────────────────────────────────────────────

class TestCPUGeneration:
    def test_vcpu_element(self):
        xml = _gen(_base({'cpu_allocation': {'max_vcpu': 4}}))
        assert '<vcpu' in xml
        assert '>4<' in xml

    def test_vcpu_placement(self):
        xml = _gen(_base({'cpu_allocation': {'max_vcpu': 2, 'placement': 'static'}}))
        assert 'placement="static"' in xml


# ── OS 配置 ───────────────────────────────────────────────────────────────────

class TestOSGeneration:
    def test_os_element(self):
        xml = _gen(_base())
        assert '<os>' in xml or '<os ' in xml

    def test_boot_device(self):
        xml = _gen(_base({'os_booting': {'type': 'hvm', 'boot_devices': ['hd']}}))
        assert '<boot dev="hd"' in xml


# ── 设备配置 ──────────────────────────────────────────────────────────────────

class TestDevicesGeneration:
    def test_devices_element(self):
        # devices 需要有内容才会生成 <devices> 元素
        xml = _gen(_base({'devices': {'emulator': '/usr/bin/qemu-system-x86_64'}}))
        assert '<devices>' in xml

    def test_disk_device(self):
        xml = _gen(_base({'devices': {
            'disks': [{
                'type': 'file',
                'device': 'disk',
                'source_file': '/var/lib/libvirt/images/test.qcow2',
                'target_dev': 'vda',
                'target_bus': 'virtio',
                'driver_name': 'qemu',
                'driver_type': 'qcow2',
            }]
        }}))
        assert '<disk' in xml
        assert 'vda' in xml

    def test_graphics_vnc(self):
        xml = _gen(_base({'devices': {
            'graphics': [{'type': 'vnc', 'port': -1, 'listen': '0.0.0.0'}]
        }}))
        assert 'type="vnc"' in xml


# ── 内存调优 ──────────────────────────────────────────────────────────────────

class TestMemoryTuningGeneration:
    def test_memtune_hard_limit(self):
        # memory_tuning 的值需要嵌套 {value, unit} 格式
        xml = _gen(_base({'memory_tuning': {
            'hard_limit': {'value': '1048576', 'unit': 'KiB'}
        }}))
        assert '<hard_limit' in xml

    def test_memtune_soft_limit(self):
        xml = _gen(_base({'memory_tuning': {
            'soft_limit': {'value': '524288', 'unit': 'KiB'}
        }}))
        assert '<soft_limit' in xml


# ── 安全标签 ──────────────────────────────────────────────────────────────────

class TestSecurityLabel:
    def test_seclabel_none_type(self):
        xml = _gen(_base({'security_label': {'type': 'none'}}))
        assert 'type="none"' in xml

    def test_seclabel_dynamic(self):
        xml = _gen(_base({'security_label': {
            'type': 'dynamic',
            'model': 'selinux',
            'relabel': True,
        }}))
        assert 'type="dynamic"' in xml
        assert 'model="selinux"' in xml


# ── 异常处理 ──────────────────────────────────────────────────────────────────

class TestErrorHandling:
    def test_none_config_raises(self):
        with pytest.raises((XMLGenerationError, TypeError, AttributeError)):
            LibvirtXMLGenerator().generate(None)  # type: ignore

    def test_empty_dict_generates_valid_xml(self):
        # 空字典应该生成最小有效 XML，不应崩溃
        xml = _gen({})
        assert '<domain' in xml

    def test_xml_generation_error_is_exception(self):
        assert issubclass(XMLGenerationError, Exception)


# ── 完整配置集成 ──────────────────────────────────────────────────────────────

class TestFullConfig:
    def test_full_config_from_vmconfig(self):
        from vm.model.core.vm_config import VMConfig
        cfg = VMConfig()
        cfg.basic.name = 'full-test'
        xml = _gen(cfg.to_dict())
        root = ET.fromstring(xml)
        assert root.find('name').text == 'full-test'

    def test_power_management(self):
        xml = _gen(_base({'power_management': {
            'suspend_to_mem': 'yes',
            'suspend_to_disk': 'no',
        }}))
        assert '<pm>' in xml

    def test_clock_utc(self):
        xml = _gen(_base({'time_keeping': {'offset': 'utc'}}))
        assert 'offset="utc"' in xml
