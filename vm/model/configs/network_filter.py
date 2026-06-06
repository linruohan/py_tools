from dataclasses import dataclass, field
from typing import Any


@dataclass
class Rule:
    """网络过滤规则"""

    action: str  # allow, drop, reject, log, audit
    direction: str  # in, out
    protocol: str | None = None  # tcp, udp, icmp, etc.
    source: dict[str, Any] | None = None  # 源地址配置
    destination: dict[str, Any] | None = None  # 目标地址配置
    port: dict[str, Any] | None = None  # 端口配置
    icmp: dict[str, Any] | None = None  # ICMP 配置
    state: dict[str, Any] | None = None  # 状态配置


@dataclass
class Chain:
    """规则链"""

    name: str
    priority: int | None = None
    rules: list[Rule] = field(default_factory=list)


@dataclass
class NetworkFilter:
    """网络过滤规则配置"""

    name: str
    chain: list[Chain] = field(default_factory=list)
    priority: int | None = None
    target: str | None = None  # ACCEPT, DROP, REJECT

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'NetworkFilter':
        """从字典创建"""
        chains = []
        if 'chain' in data:
            for chain_data in data['chain']:
                rules = []
                if 'rules' in chain_data:
                    for rule_data in chain_data['rules']:
                        rules.append(Rule(**rule_data))
                chains.append(
                    Chain(name=chain_data['name'], priority=chain_data.get('priority'), rules=rules)
                )

        return cls(
            name=data.get('name'),
            chain=chains,
            priority=data.get('priority'),
            target=data.get('target'),
        )

    def to_dict(self) -> dict[str, Any]:
        """转换为字典"""
        return {
            'name': self.name,
            'chain': [
                {
                    'name': chain.name,
                    'priority': chain.priority,
                    'rules': [rule.__dict__ for rule in chain.rules],
                }
                for chain in self.chain
            ],
            'priority': self.priority,
            'target': self.target,
        }
