from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


@dataclass
class Rule:
    """网络过滤规则"""

    action: str  # allow, drop, reject, log, audit
    direction: str  # in, out
    protocol: Optional[str] = None  # tcp, udp, icmp, etc.
    source: Optional[Dict[str, Any]] = None  # 源地址配置
    destination: Optional[Dict[str, Any]] = None  # 目标地址配置
    port: Optional[Dict[str, Any]] = None  # 端口配置
    icmp: Optional[Dict[str, Any]] = None  # ICMP 配置
    state: Optional[Dict[str, Any]] = None  # 状态配置


@dataclass
class Chain:
    """规则链"""

    name: str
    priority: Optional[int] = None
    rules: List[Rule] = field(default_factory=list)


@dataclass
class NetworkFilter:
    """网络过滤规则配置"""

    name: str
    chain: List[Chain] = field(default_factory=list)
    priority: Optional[int] = None
    target: Optional[str] = None  # ACCEPT, DROP, REJECT

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'NetworkFilter':
        """从字典创建"""
        chains = []
        if 'chain' in data:
            for chain_data in data['chain']:
                rules = []
                if 'rules' in chain_data:
                    for rule_data in chain_data['rules']:
                        rules.append(Rule(**rule_data))
                chains.append(Chain(
                    name=chain_data['name'],
                    priority=chain_data.get('priority'),
                    rules=rules
                ))

        return cls(
            name=data.get('name'),
            chain=chains,
            priority=data.get('priority'),
            target=data.get('target'),
        )

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'name': self.name,
            'chain': [
                {
                    'name': chain.name,
                    'priority': chain.priority,
                    'rules': [rule.__dict__ for rule in chain.rules]
                }
                for chain in self.chain
            ],
            'priority': self.priority,
            'target': self.target,
        }
