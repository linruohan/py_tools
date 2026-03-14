"""Redirfilter 设备配置 - 整合策略模式."""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List


@dataclass
class UsbFilterRule:
    """USB 过滤规则"""

    class_id: Optional[str] = None  # 设备类
    subclass_id: Optional[str] = None  # 设备子类
    protocol_id: Optional[str] = None  # 设备协议
    vendor_id: Optional[str] = None  # 厂商 ID
    product_id: Optional[str] = None  # 产品 ID
    version: Optional[str] = None  # 设备版本
    allow: bool = True  # 允许/拒绝


@dataclass
class Redirfilter:
    """Redirfilter (USB 重定向过滤器) 配置"""

    rules: List[UsbFilterRule] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Redirfilter':
        """从字典创建"""
        rules = []
        for rule_data in data.get('rules', []):
            rules.append(UsbFilterRule(
                class_id=rule_data.get('class_id'),
                subclass_id=rule_data.get('subclass_id'),
                protocol_id=rule_data.get('protocol_id'),
                vendor_id=rule_data.get('vendor_id'),
                product_id=rule_data.get('product_id'),
                version=rule_data.get('version'),
                allow=rule_data.get('allow', True),
            ))
        return cls(rules=rules)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'rules': [
                {
                    'class_id': rule.class_id,
                    'subclass_id': rule.subclass_id,
                    'protocol_id': rule.protocol_id,
                    'vendor_id': rule.vendor_id,
                    'product_id': rule.product_id,
                    'version': rule.version,
                    'allow': rule.allow,
                }
                for rule in self.rules
            ],
        }
