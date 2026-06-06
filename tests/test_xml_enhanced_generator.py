"""测试 XML 增强生成器."""

import pytest

from utils.xml_enhanced_generator import XMLEnhancedGenerator, ConfigDict

import xml.etree.ElementTree as ET


class TestXMLEnhancedGenerator:
    """测试 XML 增强生成器."""

    def test_init(self):
        """测试初始化."""
        domain = ET.Element('domain')
        generator = XMLEnhancedGenerator(domain)
        assert generator.domain is domain
        assert generator.get_errors() == []

    def test_safe_add_element_basic(self):
        """测试安全添加基础元素."""
        parent = ET.Element('parent')
        generator = XMLEnhancedGenerator(parent)

        elem = generator.safe_add_element(parent, 'child', text='test')
        assert elem is not None
        assert elem.tag == 'child'
        assert elem.text == 'test'

    def test_safe_add_element_with_attribs(self):
        """测试带属性添加元素."""
        parent = ET.Element('parent')
        generator = XMLEnhancedGenerator(parent)

        attribs = {'id': '123', 'name': 'test'}
        elem = generator.safe_add_element(parent, 'child', text='content', attribs=attribs)

        assert elem is not None
        assert elem.get('id') == '123'
        assert elem.get('name') == 'test'
        assert elem.text == 'content'

    def test_safe_add_element_none_text(self):
        """测试添加 None 文本的元素."""
        parent = ET.Element('parent')
        generator = XMLEnhancedGenerator(parent)

        elem = generator.safe_add_element(parent, 'child', text=None)
        assert elem is not None
        assert elem.text is None

    def test_get_value_exists(self):
        """测试获取存在的值."""
        config: ConfigDict = {'name': 'test-vm', 'memory': 2048}
        generator = XMLEnhancedGenerator(ET.Element('domain'))

        assert generator.get_value(config, 'name') == 'test-vm'
        assert generator.get_value(config, 'memory') == 2048

    def test_get_value_default(self):
        """测试获取默认值."""
        config: ConfigDict = {'name': 'test-vm'}
        generator = XMLEnhancedGenerator(ET.Element('domain'))

        assert generator.get_value(config, 'memory', default=1024) == 1024

    def test_get_value_with_type_check(self):
        """测试类型检查获取值."""
        config: ConfigDict = {'name': 'test-vm', 'count': 'not-a-number'}
        generator = XMLEnhancedGenerator(ET.Element('domain'))

        # 类型正确
        assert generator.get_value(config, 'name', expected_type=str) == 'test-vm'

        # 类型错误，返回默认值
        assert generator.get_value(config, 'count', default=0, expected_type=int) == 0

    def test_get_nested_config_exists(self):
        """测试获取存在的嵌套配置."""
        config: ConfigDict = {
            'name': 'test',
            'memory_allocation': {'memory': 2048, 'unit': 'KiB'}
        }
        generator = XMLEnhancedGenerator(ET.Element('domain'))

        nested = generator.get_nested_config(config, 'memory_allocation')
        assert nested == {'memory': 2048, 'unit': 'KiB'}

    def test_get_nested_config_not_exists(self):
        """测试获取不存在的嵌套配置."""
        config: ConfigDict = {'name': 'test'}
        generator = XMLEnhancedGenerator(ET.Element('domain'))

        nested = generator.get_nested_config(config, 'nonexistent')
        assert nested == {}

    def test_get_nested_config_required(self):
        """测试获取必需的嵌套配置."""
        config: ConfigDict = {'name': 'test'}
        generator = XMLEnhancedGenerator(ET.Element('domain'))

        with pytest.raises(ValueError, match='缺少必需的嵌套配置'):
            generator.get_nested_config(config, 'nonexistent', required=True)

    def test_validate_positive_int_valid(self):
        """测试验证有效的正整数."""
        generator = XMLEnhancedGenerator(ET.Element('domain'))

        assert generator.validate_positive_int(100, 'test') == 100
        assert generator.validate_positive_int(0, 'test', allow_zero=True) == 0

    def test_validate_positive_int_invalid(self):
        """测试验证无效的正整数."""
        generator = XMLEnhancedGenerator(ET.Element('domain'))

        assert generator.validate_positive_int(-5, 'test') is None
        assert generator.validate_positive_int(0, 'test') is None
        assert generator.validate_positive_int('not-int', 'test') is None
        assert generator.validate_positive_int(None, 'test') is None

    def test_validate_string_valid(self):
        """测试验证有效的字符串."""
        generator = XMLEnhancedGenerator(ET.Element('domain'))

        assert generator.validate_string('hello', 'test') == 'hello'
        assert generator.validate_string('  world  ', 'test') == 'world'

    def test_validate_string_invalid(self):
        """测试验证无效的字符串."""
        generator = XMLEnhancedGenerator(ET.Element('domain'))

        assert generator.validate_string('', 'test', allow_empty=False) is None
        assert generator.validate_string('   ', 'test', allow_empty=False) is None
        assert generator.validate_string(None, 'test') is None

    def test_validate_string_allow_empty(self):
        """测试允许空字符串."""
        generator = XMLEnhancedGenerator(ET.Element('domain'))

        assert generator.validate_string('', 'test', allow_empty=True) == ''

    def test_add_metadata(self):
        """测试添加元数据."""
        domain = ET.Element('domain')
        generator = XMLEnhancedGenerator(domain)

        config: ConfigDict = {
            'name': 'test-vm',
            'title': 'Test VM',
            'description': 'A test virtual machine',
            'uuid': '12345678-1234-1234-1234-123456789abc',
        }

        generator.add_metadata(config)

        # 验证生成的 XML
        name_elem = domain.find('name')
        title_elem = domain.find('title')
        desc_elem = domain.find('description')

        assert name_elem is not None
        assert name_elem.text == 'test-vm'
        assert title_elem is not None
        assert title_elem.text == 'Test VM'
        assert desc_elem is not None
        assert desc_elem.text == 'A test virtual machine'

    def test_add_memory_basic(self):
        """测试添加基础内存配置."""
        domain = ET.Element('domain')
        generator = XMLEnhancedGenerator(domain)

        config: ConfigDict = {
            'memory_allocation': {
                'memory': 2097152,
                'unit': 'KiB',
            }
        }

        generator.add_memory(config)

        memory_elem = domain.find('memory')
        assert memory_elem is not None
        assert memory_elem.text == '2097152'
        assert memory_elem.get('unit') == 'KiB'

    def test_add_memory_with_current(self):
        """测试添加带当前内存的配置."""
        domain = ET.Element('domain')
        generator = XMLEnhancedGenerator(domain)

        config: ConfigDict = {
            'memory_allocation': {
                'memory': 2097152,
                'current_memory': 1048576,
                'unit': 'KiB',
            }
        }

        generator.add_memory(config)

        memory_elem = domain.find('memory')
        current_elem = domain.find('currentMemory')

        assert memory_elem is not None
        assert memory_elem.text == '2097152'
        assert current_elem is not None
        assert current_elem.text == '1048576'

    def test_add_memory_with_max(self):
        """测试添加带最大内存的配置."""
        domain = ET.Element('domain')
        generator = XMLEnhancedGenerator(domain)

        config: ConfigDict = {
            'memory_allocation': {
                'memory': 2097152,
                'max_memory': 4194304,
                'memory_slots': 8,
                'unit': 'KiB',
            }
        }

        generator.add_memory(config)

        memory_elem = domain.find('memory')
        max_elem = domain.find('maxMemory')

        assert memory_elem is not None
        assert max_elem is not None
        assert max_elem.text == '4194304'
        assert max_elem.get('slots') == '8'

    def test_add_memory_invalid_values(self):
        """测试添加无效内存值（应使用默认值）."""
        domain = ET.Element('domain')
        generator = XMLEnhancedGenerator(domain)

        config: ConfigDict = {
            'memory_allocation': {
                'memory': -100,  # 无效值
                'unit': 'KiB',
            }
        }

        generator.add_memory(config)

        memory_elem = domain.find('memory')
        assert memory_elem is not None
        # 应该使用默认值 2097152
        assert memory_elem.text == '2097152'

    def test_get_errors(self):
        """测试获取错误列表."""
        domain = ET.Element('domain')
        generator = XMLEnhancedGenerator(domain)

        errors = generator.get_errors()
        assert errors == []

        # 模拟添加错误
        generator._errors.append('Test error 1')
        generator._errors.append('Test error 2')

        errors = generator.get_errors()
        assert len(errors) == 2
        assert 'Test error 1' in errors
        assert 'Test error 2' in errors

    def test_clear_errors(self):
        """测试清除错误列表."""
        domain = ET.Element('domain')
        generator = XMLEnhancedGenerator(domain)

        generator._errors.append('Test error')
        assert len(generator.get_errors()) == 1

        generator.clear_errors()
        assert len(generator.get_errors()) == 0
