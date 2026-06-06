"""测试 XML 生成器装饰器."""

import logging

import pytest

from utils.xml_generator_decorators import (
    safe_xml_generation,
    validate_config_keys,
    xml_generation_method,
)


class TestXMLGenerationMethodDecorator:
    """测试 xml_generation_method 装饰器."""

    def test_successful_execution(self):
        """测试成功执行的情况."""

        @xml_generation_method
        def test_func():
            return "success"

        result = test_func()
        assert result == "success"

    def test_key_error_handling(self):
        """测试 KeyError 处理."""

        @xml_generation_method
        def test_func():
            config = {}
            return config["missing"]

        with pytest.raises(KeyError):
            test_func()

    def test_type_error_handling(self):
        """测试 TypeError 处理."""

        @xml_generation_method
        def test_func():
            return None + 1  # type: ignore

        with pytest.raises(TypeError):
            test_func()

    def test_value_error_handling(self):
        """测试 ValueError 处理."""

        @xml_generation_method
        def test_func():
            raise ValueError("test error")

        with pytest.raises(ValueError, match="test error"):
            test_func()

    def test_generic_exception_handling(self):
        """测试通用异常处理."""

        @xml_generation_method
        def test_func():
            raise RuntimeError("generic error")

        with pytest.raises(RuntimeError, match="generic error"):
            test_func()

    def test_logging_on_success(self, caplog):
        """测试成功时的日志记录."""

        @xml_generation_method
        def test_func():
            return "done"

        with caplog.at_level(logging.DEBUG):
            result = test_func()

        assert result == "done"
        assert "开始生成：test_func" in caplog.text
        assert "生成完成：test_func" in caplog.text

    def test_logging_on_error(self, caplog):
        """测试失败时的日志记录."""

        @xml_generation_method
        def test_func():
            raise ValueError("error for testing")

        with caplog.at_level(logging.ERROR):
            with pytest.raises(ValueError):
                test_func()

        assert "test_func" in caplog.text
        assert "值错误" in caplog.text


class TestSafeXMLGenerationDecorator:
    """测试 safe_xml_generation 装饰器."""

    def test_successful_execution(self):
        """测试成功执行的情况."""

        @safe_xml_generation(default_return=None)
        def test_func():
            return "success"

        result = test_func()
        assert result == "success"

    def test_exception_returns_default(self):
        """测试异常时返回默认值."""

        @safe_xml_generation(default_return="default")
        def test_func():
            raise RuntimeError("error")

        result = test_func()
        assert result == "default"

    def test_warning_log_on_exception(self, caplog):
        """测试异常时记录警告日志."""

        @safe_xml_generation(default_return=None)
        def test_func():
            raise ValueError("test error")

        with caplog.at_level(logging.WARNING):
            result = test_func()

        assert result is None
        assert "test_func" in caplog.text
        assert "生成失败" in caplog.text

    def test_custom_default_return(self):
        """测试自定义默认返回值."""

        @safe_xml_generation(default_return={"key": "value"})
        def test_func():
            raise RuntimeError("error")

        result = test_func()
        assert result == {"key": "value"}

    def test_with_parameters(self):
        """测试带参数的函数."""

        @safe_xml_generation(default_return=0)
        def add(a: int, b: int) -> int:
            return a + b

        result = add(2, 3)
        assert result == 5

    def test_with_kwargs(self):
        """测试带关键字参数的函数."""

        @safe_xml_generation(default_return={})
        def create_config(**kwargs):
            return kwargs

        result = create_config(name="test", value=123)
        assert result == {"name": "test", "value": 123}


class TestValidateConfigKeysDecorator:
    """测试 validate_config_keys 装饰器."""

    def test_all_keys_present(self, caplog):
        """测试所有键都存在的情况."""

        @validate_config_keys(["name", "memory"])
        def process_config(config):
            return "processed"

        with caplog.at_level(logging.WARNING):
            result = process_config({"name": "test", "memory": 2048})

        assert result == "processed"
        assert "缺少必需的键" not in caplog.text

    def test_missing_keys(self, caplog):
        """测试缺少键的情况."""

        @validate_config_keys(["name", "memory", "cpu"])
        def process_config(config):
            return "processed"

        # 获取装饰器模块的 logger
        from utils import xml_generator_decorators

        with caplog.at_level(logging.WARNING, logger=xml_generator_decorators.__name__):
            result = process_config({"name": "test"})

        assert result == "processed"
        assert "缺少必需的键" in caplog.text
        assert "memory" in caplog.text
        assert "cpu" in caplog.text

    def test_no_config_parameter(self, caplog):
        """测试没有 config 参数的情况."""

        @validate_config_keys(["name"])
        def no_config_func():
            return "no config"

        with caplog.at_level(logging.WARNING):
            result = no_config_func()

        assert result == "no config"
        assert "缺少必需的键" not in caplog.text

    def test_non_dict_config(self, caplog):
        """测试非字典配置的情况."""

        @validate_config_keys(["name"])
        def process_config(config):
            return "processed"

        with caplog.at_level(logging.WARNING):
            result = process_config("not a dict")

        assert result == "processed"
        assert "缺少必需的键" not in caplog.text

    def test_partial_keys_missing(self, caplog):
        """测试部分键缺失的情况."""

        @validate_config_keys(["name", "memory", "cpu", "disk"])
        def process_config(config):
            return "processed"

        # 获取装饰器模块的 logger
        from utils import xml_generator_decorators

        with caplog.at_level(logging.WARNING, logger=xml_generator_decorators.__name__):
            result = process_config({"name": "test", "cpu": 2})

        assert result == "processed"
        assert "缺少必需的键" in caplog.text
        assert "memory" in caplog.text
        assert "disk" in caplog.text
        assert "name" not in caplog.text
        assert "cpu" not in caplog.text


class TestDecoratorComposition:
    """测试装饰器组合使用."""

    def test_multiple_decorators(self):
        """测试多个装饰器组合."""

        @safe_xml_generation(default_return="default")
        @xml_generation_method
        def test_func():
            return "success"

        result = test_func()
        assert result == "success"

    def test_multiple_decorators_with_exception(self):
        """测试多个装饰器组合发生异常."""

        @safe_xml_generation(default_return="default")
        @xml_generation_method
        def test_func():
            raise RuntimeError("error")

        result = test_func()
        assert result == "default"

    def test_validation_and_safe_generation(self):
        """测试验证和安全生成组合."""

        @safe_xml_generation(default_return={})
        @validate_config_keys(["name"])
        def process_config(config):
            return {"processed": True}

        # 缺少 name 键，但不会抛出异常，只会记录警告
        result = process_config({})
        assert result == {"processed": True}
