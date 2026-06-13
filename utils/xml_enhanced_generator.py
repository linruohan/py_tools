"""XML 生成器增强模块 - 添加异常处理和类型注解."""

from __future__ import annotations

import logging
import xml.etree.ElementTree as ET

from typing import Any

logger = logging.getLogger(__name__)

# 类型别名
ElementDict = dict[str, Any]
ConfigDict = dict[str, Any]


class XMLEnhancedGenerator:
    """XML 增强生成器 - 提供更安全和类型安全的 XML 生成方法."""

    def __init__(self, domain_element: ET.Element):
        """初始化增强生成器.

        Args:
            domain_element: Domain 根元素
        """
        self.domain = domain_element
        self._errors: list[str] = []

    def safe_add_element(
        self,
        parent: ET.Element,
        tag: str,
        text: str | None = None,
        attribs: dict[str, str] | None = None,
    ) -> ET.Element | None:
        """安全地添加 XML 元素,包含异常处理.

        Args:
            parent: 父元素
            tag: 元素标签名
            text: 元素文本内容
            attribs: 属性字典

        Returns:
            创建的元素,失败返回 None
        """
        try:
            element = ET.SubElement(parent, tag)
            if text is not None:
                element.text = str(text)
            if attribs:
                for key, value in attribs.items():
                    element.set(key, str(value))
            return element
        except Exception as e:
            logger.error(f'添加 XML 元素失败:tag={tag}, error={e}')
            self._errors.append(f'添加元素 {tag} 失败:{e}')
            return None

    def get_value(
        self,
        config: ConfigDict,
        key: str,
        default: Any = None,
        expected_type: type | tuple[type, ...] | None = None,
    ) -> Any:
        """安全地从配置字典获取值,进行类型检查.

        Args:
            config: 配置字典
            key: 键名
            default: 默认值
            expected_type: 期望的类型(可以是类型元组)

        Returns:
            获取到的值,类型不匹配或不存在时返回默认值
        """
        try:
            value = config.get(key, default)
            if expected_type is not None and value is not None:
                if not isinstance(value, expected_type):
                    logger.warning(
                        f'配置项 {key} 类型不匹配:期望 {expected_type}, 得到 {type(value)}'
                    )
                    return default
            return value
        except Exception as e:
            logger.error(f'获取配置项 {key} 失败:{e}')
            return default

    def get_nested_config(self, config: ConfigDict, key: str, required: bool = False) -> ConfigDict:
        """安全地获取嵌套配置.

        Args:
            config: 父配置字典
            key: 嵌套配置的键
            required: 是否为必需配置

        Returns:
            嵌套配置字典,不存在时返回空字典

        Raises:
            ValueError: 当配置为必需但不存在时
        """
        try:
            nested = config.get(key, {})
            if required and not nested:
                raise ValueError(f'缺少必需的嵌套配置:{key}')
            return nested if isinstance(nested, dict) else {}
        except Exception as e:
            logger.error(f'获取嵌套配置 {key} 失败:{e}')
            if required:
                raise
            return {}

    def validate_positive_int(
        self, value: Any, field_name: str, allow_zero: bool = False
    ) -> int | None:
        """验证正整数值.

        Args:
            value: 要验证的值
            field_name: 字段名称
            allow_zero: 是否允许零值

        Returns:
            验证后的整数值,无效时返回 None
        """
        try:
            if value is None:
                return None
            int_value = int(value)
            if allow_zero:
                if int_value < 0:
                    logger.warning(f'{field_name} 不能为负数:{int_value}')
                    return None
            else:
                if int_value <= 0:
                    logger.warning(f'{field_name} 必须为正数:{int_value}')
                    return None
            return int_value
        except (TypeError, ValueError) as e:
            logger.warning(f'{field_name} 不是有效的整数:{value}, error={e}')
            return None

    def validate_string(self, value: Any, field_name: str, allow_empty: bool = False) -> str | None:
        """验证字符串值.

        Args:
            value: 要验证的值
            field_name: 字段名称
            allow_empty: 是否允许空字符串

        Returns:
            验证后的字符串,无效时返回 None
        """
        try:
            if value is None:
                return None
            str_value = str(value).strip()
            if not allow_empty and not str_value:
                logger.warning(f'{field_name} 不能为空字符串')
                return None
            return str_value
        except Exception as e:
            logger.warning(f'{field_name} 转换字符串失败:{value}, error={e}')
            return None

    def add_metadata(self, config: ConfigDict) -> None:
        """添加元数据配置(带异常处理).

        Args:
            config: 配置字典
        """
        try:
            metadata_config = self.get_nested_config(config, 'name')
            if metadata_config:
                # 注意:这里的逻辑可能需要调整,因为原代码直接从 config 获取
                pass

            # 使用安全方法添加元素
            if name := self.get_value(config, 'name', expected_type=str):
                self.safe_add_element(self.domain, 'name', text=name)

            if title := self.get_value(config, 'title', expected_type=str):
                self.safe_add_element(self.domain, 'title', text=title)

            if description := self.get_value(config, 'description', expected_type=str):
                self.safe_add_element(self.domain, 'description', text=description)

            if uuid := self.get_value(config, 'uuid', expected_type=str):
                self.safe_add_element(self.domain, 'uuid', text=uuid)

            if genid := self.get_value(config, 'genid', expected_type=str):
                self.safe_add_element(self.domain, 'genid', text=genid)

        except Exception as e:
            logger.exception(f'添加元数据失败:{e}')
            self._errors.append(f'元数据添加失败:{e}')

    def add_memory(self, config: ConfigDict) -> None:
        """添加内存配置(带异常处理).

        Args:
            config: 配置字典
        """
        try:
            memory_config = self.get_nested_config(config, 'memory_allocation')
            if not memory_config:
                return

            # 获取内存值并验证
            memory = self.validate_positive_int(
                self.get_value(memory_config, 'memory', default=2097152),
                'memory.memory',
            )
            if memory is None:
                memory = 2097152  # 默认值

            unit = self.get_value(memory_config, 'unit', default='KiB', expected_type=str)
            dump_core = self.get_value(memory_config, 'dump_core')

            # 创建 memory 元素
            mem_elem = self.safe_add_element(
                self.domain, 'memory', text=str(memory), attribs={'unit': unit}
            )
            if mem_elem is not None and dump_core is not None:
                mem_elem.set('dumpCore', 'on' if dump_core else 'off')

            # 添加 currentMemory
            if 'current_memory' in memory_config:
                current_memory = self.validate_positive_int(
                    self.get_value(memory_config, 'current_memory', default=memory),
                    'memory.current_memory',
                )
                if current_memory is not None:
                    self.safe_add_element(
                        self.domain,
                        'currentMemory',
                        text=str(current_memory),
                        attribs={'unit': unit},
                    )

            # 添加 maxMemory
            if 'max_memory' in memory_config:
                max_memory = self.get_value(memory_config, 'max_memory')
                if max_memory and max_memory > memory:
                    slots = self.validate_positive_int(
                        self.get_value(memory_config, 'memory_slots', default=16),
                        'memory.memory_slots',
                        allow_zero=True,
                    )
                    if slots is None:
                        slots = 16
                    self.safe_add_element(
                        self.domain,
                        'maxMemory',
                        text=str(max_memory),
                        attribs={'slots': str(slots), 'unit': unit},
                    )

        except Exception as e:
            logger.exception(f'添加内存配置失败:{e}')
            self._errors.append(f'内存配置添加失败:{e}')

    def get_errors(self) -> list[str]:
        """获取所有收集的错误.

        Returns:
            错误列表
        """
        return self._errors.copy()

    def clear_errors(self) -> None:
        """清除错误列表."""
        self._errors.clear()
