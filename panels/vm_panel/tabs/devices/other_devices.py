"""其他设备模块 - 包括输入设备、集线器设备、图形设备等"""

import customtkinter as ctk

from components.base_tab import BaseConfigTab
from utils.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class InputDevicesTab(BaseConfigTab):
    """输入设备配置"""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, on_change_callback, **kwargs)
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面"""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            frame, text='Input devices', font=CTK_FONT_BOLD, text_color='#2196f3'
        ).grid(row=0, column=0, columnspan=4, padx=10, pady=5, sticky='w')

        # Input Type
        ctk.CTkLabel(frame, text='Input Type:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.input_type = ctk.CTkOptionMenu(
            frame,
            values=['keyboard', 'mouse', 'tablet'],
            width=100,
            font=CTK_FONT_SMALL,
            command=self._trigger_change
        )
        self.input_type.set('keyboard')
        self.input_type.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        # Model
        ctk.CTkLabel(frame, text='Model:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.model = ctk.CTkOptionMenu(
            frame,
            values=['ps2', 'usb', 'virtio'],
            width=100,
            font=CTK_FONT_SMALL,
            command=self._trigger_change
        )
        self.model.set('ps2')
        self.model.grid(row=2, column=1, padx=5, pady=5, sticky='w')

    def get_config(self) -> dict:
        """获取配置"""
        return {
            'type': 'input',
            'input_type': self.input_type.get(),
            'model': self.model.get()
        }


class HubDevicesTab(BaseConfigTab):
    """集线器设备配置"""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, on_change_callback, **kwargs)
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面"""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            frame, text='Hub devices', font=CTK_FONT_BOLD, text_color='#4caf50'
        ).grid(row=0, column=0, padx=10, pady=5, sticky='w')

        ctk.CTkLabel(
            frame, 
            text='集线器设备用于连接多个USB设备。\n'
                 '通常使用USB hub来扩展虚拟机的USB设备连接能力。',
            font=CTK_FONT_SMALL, 
            text_color='#666666'
        ).grid(row=1, column=0, padx=10, pady=5, sticky='w')

        # Hub Type
        ctk.CTkLabel(frame, text='Hub Type:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.hub_type = ctk.CTkOptionMenu(
            frame,
            values=['usb', 'usb3'],
            width=100,
            font=CTK_FONT_SMALL,
            command=self._trigger_change
        )
        self.hub_type.set('usb')
        self.hub_type.grid(row=2, column=1, padx=5, pady=5, sticky='w')

    def get_config(self) -> dict:
        """获取配置"""
        return {
            'type': 'hub',
            'hub_type': self.hub_type.get()
        }


class GraphicalFramebuffersTab(BaseConfigTab):
    """图形帧缓冲区配置"""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, on_change_callback, **kwargs)
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面"""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            frame, text='Graphical framebuffers', font=CTK_FONT_BOLD, text_color='#ff9800'
        ).grid(row=0, column=0, columnspan=4, padx=10, pady=5, sticky='w')

        # Framebuffer Type
        ctk.CTkLabel(frame, text='Type:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.fb_type = ctk.CTkOptionMenu(
            frame,
            values=['vga', 'cirrus', 'qxl', 'virtio'],
            width=100,
            font=CTK_FONT_SMALL,
            command=self._trigger_change
        )
        self.fb_type.set('vga')
        self.fb_type.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        # Resolution
        ctk.CTkLabel(frame, text='Resolution:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.resolution = ctk.CTkOptionMenu(
            frame,
            values=['800x600', '1024x768', '1280x720', '1920x1080'],
            width=120,
            font=CTK_FONT_SMALL,
            command=self._trigger_change
        )
        self.resolution.set('1024x768')
        self.resolution.grid(row=2, column=1, padx=5, pady=5, sticky='w')

    def get_config(self) -> dict:
        """获取配置"""
        return {
            'type': 'framebuffer',
            'fb_type': self.fb_type.get(),
            'resolution': self.resolution.get()
        }


class VideoDevicesTab(BaseConfigTab):
    """视频设备配置"""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, on_change_callback, **kwargs)
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面"""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            frame, text='Video devices', font=CTK_FONT_BOLD, text_color='#9c27b0'
        ).grid(row=0, column=0, columnspan=4, padx=10, pady=5, sticky='w')

        # Video Model
        ctk.CTkLabel(frame, text='Model:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.video_model = ctk.CTkOptionMenu(
            frame,
            values=['vga', 'cirrus', 'qxl', 'virtio', 'vmvga'],
            width=100,
            font=CTK_FONT_SMALL,
            command=self._trigger_change
        )
        self.video_model.set('vga')
        self.video_model.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        # Heads
        ctk.CTkLabel(frame, text='Heads:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.heads = ctk.CTkEntry(
            frame, placeholder_text='1', width=80, font=CTK_FONT_SMALL
        )
        self.heads.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.heads.bind('<KeyRelease>', lambda e: self._trigger_change())

    def get_config(self) -> dict:
        """获取配置"""
        return {
            'type': 'video',
            'model': self.video_model.get(),
            'heads': self.heads.get().strip() or '1'
        }


class ConsolesDevicesTab(BaseConfigTab):
    """控制台、串口、并口和通道设备配置"""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, on_change_callback, **kwargs)
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面"""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            frame, text='Consoles, serial, parallel & channel devices', font=CTK_FONT_BOLD, text_color='#ff5722'
        ).grid(row=0, column=0, padx=10, pady=5, sticky='w')

        ctk.CTkLabel(
            frame, 
            text='配置虚拟机的控制台、串口、并口和通道设备。',
            font=CTK_FONT_SMALL, 
            text_color='#666666'
        ).grid(row=1, column=0, padx=10, pady=5, sticky='w')


class SoundDevicesTab(BaseConfigTab):
    """声音设备配置"""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, on_change_callback, **kwargs)
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面"""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            frame, text='Sound devices', font=CTK_FONT_BOLD, text_color='#795548'
        ).grid(row=0, column=0, columnspan=4, padx=10, pady=5, sticky='w')

        # Sound Model
        ctk.CTkLabel(frame, text='Model:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.sound_model = ctk.CTkOptionMenu(
            frame,
            values=['ac97', 'es1370', 'hda', 'sb16', 'pcspk'],
            width=100,
            font=CTK_FONT_SMALL,
            command=self._trigger_change
        )
        self.sound_model.set('ac97')
        self.sound_model.grid(row=1, column=1, padx=5, pady=5, sticky='w')

    def get_config(self) -> dict:
        """获取配置"""
        return {
            'type': 'sound',
            'model': self.sound_model.get()
        }


class WatchdogDevicesTab(BaseConfigTab):
    """看门狗设备配置"""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, on_change_callback, **kwargs)
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面"""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            frame, text='Watchdog devices', font=CTK_FONT_BOLD, text_color='#607d8b'
        ).grid(row=0, column=0, columnspan=4, padx=10, pady=5, sticky='w')

        # Watchdog Model
        ctk.CTkLabel(frame, text='Model:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.watchdog_model = ctk.CTkOptionMenu(
            frame,
            values=['i6300esb', 'ib700', 'wdt_i6300esb'],
            width=120,
            font=CTK_FONT_SMALL,
            command=self._trigger_change
        )
        self.watchdog_model.set('i6300esb')
        self.watchdog_model.grid(row=1, column=1, padx=5, pady=5, sticky='w')

    def get_config(self) -> dict:
        """获取配置"""
        return {
            'type': 'watchdog',
            'model': self.watchdog_model.get()
        }


class MemoryBalloonTab(BaseConfigTab):
    """内存气球设备配置"""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, on_change_callback, **kwargs)
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面"""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            frame, text='Memory balloon device', font=CTK_FONT_BOLD, text_color='#4caf50'
        ).grid(row=0, column=0, columnspan=4, padx=10, pady=5, sticky='w')

        # Model
        ctk.CTkLabel(frame, text='Model:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.balloon_model = ctk.CTkOptionMenu(
            frame,
            values=['virtio', 'none'],
            width=100,
            font=CTK_FONT_SMALL,
            command=self._trigger_change
        )
        self.balloon_model.set('virtio')
        self.balloon_model.grid(row=1, column=1, padx=5, pady=5, sticky='w')

    def get_config(self) -> dict:
        """获取配置"""
        return {
            'type': 'balloon',
            'model': self.balloon_model.get()
        }


class TPMDeviceTab(BaseConfigTab):
    """TPM设备配置"""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, on_change_callback, **kwargs)
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面"""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            frame, text='TPM device', font=CTK_FONT_BOLD, text_color='#2196f3'
        ).grid(row=0, column=0, columnspan=4, padx=10, pady=5, sticky='w')

        # TPM Version
        ctk.CTkLabel(frame, text='Version:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.tpm_version = ctk.CTkOptionMenu(
            frame,
            values=['tpm1.2', 'tpm2.0'],
            width=100,
            font=CTK_FONT_SMALL,
            command=self._trigger_change
        )
        self.tpm_version.set('tpm2.0')
        self.tpm_version.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        # Model
        ctk.CTkLabel(frame, text='Model:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.tpm_model = ctk.CTkOptionMenu(
            frame,
            values=['tpm-tis', 'tpm-crb'],
            width=100,
            font=CTK_FONT_SMALL,
            command=self._trigger_change
        )
        self.tpm_model.set('tpm-tis')
        self.tpm_model.grid(row=2, column=1, padx=5, pady=5, sticky='w')

    def get_config(self) -> dict:
        """获取配置"""
        return {
            'type': 'tpm',
            'version': self.tpm_version.get(),
            'model': self.tpm_model.get()
        }
