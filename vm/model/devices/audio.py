"""Audio 设备配置 - 整合策略模式."""

from dataclasses import dataclass
from typing import Any


@dataclass
class AudioSettings:
    """音频设置配置"""

    frequency: int = 44100
    channels: int = 2
    format: str = 's16'  # s8, u8, s16, u16, s32, u32, f32

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'AudioSettings':
        """从字典创建"""
        return cls(
            frequency=data.get('frequency', 44100),
            channels=data.get('channels', 2),
            format=data.get('format', 's16'),
        )

    def to_dict(self) -> dict[str, Any]:
        """转换为字典"""
        return {
            'frequency': self.frequency,
            'channels': self.channels,
            'format': self.format,
        }


@dataclass
class AudioIO:
    """音频输入/输出配置"""

    mixing_engine: bool = True
    fixed_settings: bool = False
    voices: int = 1
    buffer_length: int = 100
    dev: str | None = None  # ALSA/OSS 设备路径
    server_name: str | None = None  # Jack 服务器名称
    client_name: str | None = None  # Jack 客户端名称
    connect_ports: str | None = None  # Jack 端口正则表达式
    exact_name: bool = False  # Jack 精确名称
    buffer_count: int | None = None  # 缓冲区数量
    settings: AudioSettings | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'AudioIO':
        """从字典创建"""
        settings_data = data.get('settings')
        settings = AudioSettings.from_dict(settings_data) if settings_data else None

        return cls(
            mixing_engine=data.get('mixing_engine', True),
            fixed_settings=data.get('fixed_settings', False),
            voices=data.get('voices', 1),
            buffer_length=data.get('buffer_length', 100),
            dev=data.get('dev'),
            server_name=data.get('server_name'),
            client_name=data.get('client_name'),
            connect_ports=data.get('connect_ports'),
            exact_name=data.get('exact_name', False),
            buffer_count=data.get('buffer_count'),
            settings=settings,
        )

    def to_dict(self) -> dict[str, Any]:
        """转换为字典"""
        result = {
            'mixing_engine': self.mixing_engine,
            'fixed_settings': self.fixed_settings,
            'voices': self.voices,
            'buffer_length': self.buffer_length,
            'dev': self.dev,
            'server_name': self.server_name,
            'client_name': self.client_name,
            'connect_ports': self.connect_ports,
            'exact_name': self.exact_name,
            'buffer_count': self.buffer_count,
        }
        if self.settings:
            result['settings'] = self.settings.to_dict()
        return result


@dataclass
class Audio:
    """音频设备配置"""

    id: int = 1
    type: str = 'pulseaudio'  # none, alsa, coreaudio, dbus, jack, oss, pipewire, pulseaudio, sdl, spice, file
    timer_period: int = 40  # 微秒
    input: AudioIO | None = None
    output: AudioIO | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'Audio':
        """从字典创建"""
        input_data = data.get('input')
        output_data = data.get('output')

        return cls(
            id=data.get('id', 1),
            type=data.get('type', 'pulseaudio'),
            timer_period=data.get('timer_period', 40),
            input=AudioIO.from_dict(input_data) if input_data else None,
            output=AudioIO.from_dict(output_data) if output_data else None,
        )

    def to_dict(self) -> dict[str, Any]:
        """转换为字典"""
        result = {
            'id': self.id,
            'type': self.type,
            'timer_period': self.timer_period,
        }
        if self.input:
            result['input'] = self.input.to_dict()
        if self.output:
            result['output'] = self.output.to_dict()
        return result
