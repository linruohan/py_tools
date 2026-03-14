from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class Timer:
    """定时器配置"""

    name: str
    present: Optional[bool] = None
    tickpolicy: Optional[str] = None  # delay, catchup, merge, discard
    track: Optional[str] = None  # boot, system, wall, hypervisor
    frequency: Optional[int] = None
    mode: Optional[str] = None  # auto, host, guest
    args: Optional[str] = None
    pit: Optional[dict] = None
    hpet: Optional[dict] = None
    rtc: Optional[dict] = None


@dataclass
class Clock:
    """时钟配置"""

    offset: str  # utc, localtime, timezone
    timezone: Optional[str] = None
    timers: List[Timer] = field(default_factory=list)
    adjustment: Optional[str] = None  # none, acpi, apic
