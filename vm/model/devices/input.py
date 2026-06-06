from dataclasses import dataclass
from typing import Any


@dataclass
class Input:
    """输入设备配置"""

    type: str = 'keyboard'  # keyboard, mouse, tablet, joystick
    bus: str = 'ps2'  # ps2, usb, virtio
    device: str | None = None  # 设备类型
    mode: str | None = None  # 模式
    passwd: str | None = None  # 密码
    replay: bool | None = None  # 重放
    grab: str | None = None  # 抓取模式
    repeat: bool | None = None  # 重复
    wheel_emulation: bool | None = None  # 滚轮模拟
    wheel_emulation_button: int | None = None  # 滚轮模拟按钮
    wheel_emulation_x_mult: int | None = None  # X 轴滚轮倍数
    wheel_emulation_y_mult: int | None = None  # Y 轴滚轮倍数
    vendor_id: str | None = None  # 厂商 ID
    product_id: str | None = None  # 产品 ID
    address: dict[str, str] | None = None  # 设备地址

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'Input':
        """从字典创建"""
        return cls(
            type=data.get('type', 'keyboard'),
            bus=data.get('bus', 'ps2'),
            device=data.get('device'),
            mode=data.get('mode'),
            passwd=data.get('passwd'),
            replay=data.get('replay'),
            grab=data.get('grab'),
            repeat=data.get('repeat'),
            wheel_emulation=data.get('wheel_emulation'),
            wheel_emulation_button=data.get('wheel_emulation_button'),
            wheel_emulation_x_mult=data.get('wheel_emulation_x_mult'),
            wheel_emulation_y_mult=data.get('wheel_emulation_y_mult'),
            vendor_id=data.get('vendor_id'),
            product_id=data.get('product_id'),
            address=data.get('address'),
        )

    def to_dict(self) -> dict[str, Any]:
        """转换为字典"""
        return {
            'type': self.type,
            'bus': self.bus,
            'device': self.device,
            'mode': self.mode,
            'passwd': self.passwd,
            'replay': self.replay,
            'grab': self.grab,
            'repeat': self.repeat,
            'wheel_emulation': self.wheel_emulation,
            'wheel_emulation_button': self.wheel_emulation_button,
            'wheel_emulation_x_mult': self.wheel_emulation_x_mult,
            'wheel_emulation_y_mult': self.wheel_emulation_y_mult,
            'vendor_id': self.vendor_id,
            'product_id': self.product_id,
            'address': self.address,
        }
