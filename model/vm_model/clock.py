"""Clock 设备配置 - 整合策略模式."""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


@dataclass
class Catchup:
    """Catchup 模式配置"""

    threshold: Optional[int] = None
    slew: Optional[int] = None
    limit: Optional[int] = None


@dataclass
class Timer:
    """定时器配置"""

    name: str  # platform, hpet, kvmclock, pit, rtc, tsc, hypervclock, armvtimer
    present: Optional[bool] = None
    tickpolicy: Optional[str] = None  # delay, catchup, merge, discard
    track: Optional[str] = None  # boot, guest, wall, realtime
    frequency: Optional[int] = None
    mode: Optional[str] = None  # auto, native, emulate, paravirt, smpsafe, host, guest
    args: Optional[str] = None
    catchup: Optional[Catchup] = None
    pit: Optional[Dict[str, Any]] = None
    hpet: Optional[Dict[str, Any]] = None
    rtc: Optional[Dict[str, Any]] = None
    kvmclock: Optional[Dict[str, Any]] = None
    hypervclock: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Timer':
        """从字典创建"""
        catchup_data = data.get('catchup')
        catchup = Catchup(
            threshold=catchup_data.get('threshold'),
            slew=catchup_data.get('slew'),
            limit=catchup_data.get('limit'),
        ) if catchup_data else None

        return cls(
            name=data.get('name', 'rtc'),
            present=data.get('present'),
            tickpolicy=data.get('tickpolicy'),
            track=data.get('track'),
            frequency=data.get('frequency'),
            mode=data.get('mode'),
            args=data.get('args'),
            catchup=catchup,
            pit=data.get('pit'),
            hpet=data.get('hpet'),
            rtc=data.get('rtc'),
            kvmclock=data.get('kvmclock'),
            hypervclock=data.get('hypervclock'),
        )

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        result = {
            'name': self.name,
            'present': self.present,
            'tickpolicy': self.tickpolicy,
            'track': self.track,
            'frequency': self.frequency,
            'mode': self.mode,
            'args': self.args,
        }
        if self.catchup:
            result['catchup'] = {
                'threshold': self.catchup.threshold,
                'slew': self.catchup.slew,
                'limit': self.catchup.limit,
            }
        if self.pit:
            result['pit'] = self.pit
        if self.hpet:
            result['hpet'] = self.hpet
        if self.rtc:
            result['rtc'] = self.rtc
        if self.kvmclock:
            result['kvmclock'] = self.kvmclock
        if self.hypervclock:
            result['hypervclock'] = self.hypervclock
        return result


@dataclass
class Clock:
    """时钟配置"""

    offset: str = 'utc'  # utc, localtime, timezone, variable
    timezone: Optional[str] = None
    adjustment: Optional[str] = None  # none, acpi, apic
    timers: List[Timer] = field(default_factory=list)
    bpm: Optional[str] = None  # boot monotonic

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Clock':
        """从字典创建"""
        timers_data = data.get('timers', [])
        timers = [Timer.from_dict(t) for t in timers_data]

        return cls(
            offset=data.get('offset', 'utc'),
            timezone=data.get('timezone'),
            adjustment=data.get('adjustment'),
            timers=timers,
            bpm=data.get('bpm'),
        )

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'offset': self.offset,
            'timezone': self.timezone,
            'adjustment': self.adjustment,
            'timers': [t.to_dict() for t in self.timers],
            'bpm': self.bpm,
        }
