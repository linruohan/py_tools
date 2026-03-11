"""设备配置 Tab - 图形、USB、控制器、串口、TPM 等."""

import customtkinter as ctk

from ..styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class DevicesTab(ctk.CTkFrame):
    """设备配置 Tab."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent')
        self.on_change_callback = on_change_callback
        self.usb_list = []

        # 控件引用
        self.graphics_type = None
        self.graphics_listen = None
        self.graphics_port = None
        self.video_model = None
        self.vram_entry = None
        self.usb_controller = None
        self.usb_entry = None
        self.usb_display = None
        self.disable_usb_check = None
        self.disable_sound_check = None
        # 串口配置
        self.serial_type = None
        self.serial_port = None
        # TPM 配置
        self.tpm_model = None
        self.tpm_version = None
        # 音频配置
        self.audio_model = None

        # 初始化 UI
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面."""
        # 配置 grid 权重
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=0)
        self.grid_rowconfigure(4, weight=1)  # 填充剩余垂直空间

        # 图形配置
        graphics_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=8)
        graphics_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=10)
        graphics_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            graphics_frame, text='图形显示', font=CTK_FONT_BOLD, text_color='#ba68c8'
        ).grid(row=0, column=0, columnspan=6, padx=10, pady=5, sticky='w')

        # 图形类型
        ctk.CTkLabel(graphics_frame, text='图形:', font=CTK_FONT_MAIN, width=70, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.graphics_type = ctk.CTkOptionMenu(
            graphics_frame, values=['vnc', 'spice', 'none'], width=90, font=CTK_FONT_SMALL
        )
        self.graphics_type.set('vnc')
        self.graphics_type.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.graphics_type.configure(command=self._trigger_change)

        # 监听地址
        ctk.CTkLabel(graphics_frame, text='监听:', font=CTK_FONT_MAIN, width=50, anchor='w').grid(
            row=1, column=2, padx=5, pady=5, sticky='w'
        )
        self.graphics_listen = ctk.CTkEntry(graphics_frame, width=100, font=CTK_FONT_SMALL)
        self.graphics_listen.grid(row=1, column=3, padx=5, pady=5, sticky='w')
        self.graphics_listen.insert(0, '0.0.0.0')
        self.graphics_listen.bind('<KeyRelease>', lambda e: self._trigger_change())

        # 端口
        ctk.CTkLabel(graphics_frame, text='端口:', font=CTK_FONT_MAIN, width=40, anchor='w').grid(
            row=1, column=4, padx=5, pady=5, sticky='w'
        )
        self.graphics_port = ctk.CTkEntry(graphics_frame, width=60, font=CTK_FONT_SMALL)
        self.graphics_port.grid(row=1, column=5, padx=5, pady=5, sticky='w')
        self.graphics_port.insert(0, '-1')
        self.graphics_port.bind('<KeyRelease>', lambda e: self._trigger_change())

        # 视频模型
        ctk.CTkLabel(graphics_frame, text='视频:', font=CTK_FONT_MAIN, width=50, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.video_model = ctk.CTkOptionMenu(
            graphics_frame,
            values=['qxl', 'virtio', 'vmvga', 'bochs', 'ramfb', 'virtio-vga', 'virtio-vga-gl'],
            width=120,
            font=CTK_FONT_SMALL,
        )
        self.video_model.set('qxl')
        self.video_model.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.video_model.configure(command=self._trigger_change)

        # VRAM 大小
        ctk.CTkLabel(
            graphics_frame, text='VRAM (MB):', font=CTK_FONT_MAIN, width=80, anchor='w'
        ).grid(row=2, column=2, padx=5, pady=5, sticky='w')
        self.vram_entry = ctk.CTkEntry(graphics_frame, width=60, font=CTK_FONT_SMALL)
        self.vram_entry.grid(row=2, column=3, padx=5, pady=5, sticky='w')
        self.vram_entry.insert(0, '64')
        self.vram_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        # USB 控制器
        usb_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=8)
        usb_frame.grid(row=1, column=0, sticky='ew', padx=10, pady=10)
        usb_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(usb_frame, text='USB 控制器', font=CTK_FONT_BOLD, text_color='#2196f3').grid(
            row=0, column=0, columnspan=3, padx=10, pady=5, sticky='w'
        )

        # USB 控制器模型
        ctk.CTkLabel(usb_frame, text='控制器:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.usb_controller = ctk.CTkOptionMenu(
            usb_frame,
            values=[
                'qemu-xhci',
                'piix3-uhci',
                'piix4-uhci',
                'nec-xhci',
                'vt82c686b-uhci',
                'ich9-ehci1',
                'none',
            ],
            width=150,
            font=CTK_FONT_SMALL,
        )
        self.usb_controller.set('qemu-xhci')
        self.usb_controller.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.usb_controller.configure(command=self._trigger_change)

        # USB 直通设备
        ctk.CTkLabel(usb_frame, text='USB 设备:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=1, column=2, padx=10, pady=5, sticky='w'
        )
        self.usb_entry = ctk.CTkEntry(
            usb_frame,
            placeholder_text='Vendor:Product (如 8087:8008)',
            width=180,
            font=CTK_FONT_SMALL,
        )
        self.usb_entry.grid(row=1, column=3, padx=5, pady=5, sticky='w')
        self.usb_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        # 添加 USB 按钮
        add_usb_btn = ctk.CTkButton(
            usb_frame,
            text='添加',
            command=self.add_usb,
            fg_color='#00bcd4',
            hover_color='#0097a7',
            width=70,
            font=CTK_FONT_SMALL,
        )
        add_usb_btn.grid(row=1, column=4, padx=5)

        self.usb_display = ctk.CTkLabel(
            usb_frame, text='', font=CTK_FONT_SMALL, text_color='#aaaaaa', anchor='w'
        )
        self.usb_display.grid(row=2, column=0, columnspan=5, padx=10, pady=5, sticky='w')

        # 串口配置
        serial_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=8)
        serial_frame.grid(row=3, column=0, sticky='ew', padx=10, pady=10)
        serial_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(serial_frame, text='串口配置', font=CTK_FONT_BOLD, text_color='#ff9800').grid(
            row=0, column=0, columnspan=4, padx=10, pady=5, sticky='w'
        )

        # 串口类型
        ctk.CTkLabel(serial_frame, text='类型:', font=CTK_FONT_MAIN, width=60, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.serial_type = ctk.CTkOptionMenu(
            serial_frame,
            values=['pty', 'tcp', 'udp', 'unix', 'spicevmc', 'none'],
            width=100,
            font=CTK_FONT_SMALL,
        )
        self.serial_type.set('pty')
        self.serial_type.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.serial_type.configure(command=self._trigger_change)

        # 端口号
        ctk.CTkLabel(serial_frame, text='端口:', font=CTK_FONT_MAIN, width=50, anchor='w').grid(
            row=1, column=2, padx=10, pady=5, sticky='w'
        )
        self.serial_port = ctk.CTkEntry(serial_frame, width=80, font=CTK_FONT_SMALL)
        self.serial_port.grid(row=1, column=3, padx=5, pady=5, sticky='w')
        self.serial_port.insert(0, '0')
        self.serial_port.bind('<KeyRelease>', lambda e: self._trigger_change())

        # TPM 配置
        tpm_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=8)
        tpm_frame.grid(row=2, column=0, sticky='ew', padx=10, pady=10)
        tpm_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(tpm_frame, text='TPM 设备', font=CTK_FONT_BOLD, text_color='#7986cb').grid(
            row=0, column=0, columnspan=4, padx=10, pady=5, sticky='w'
        )

        # TPM 模型
        ctk.CTkLabel(tpm_frame, text='模型:', font=CTK_FONT_MAIN, width=60, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.tpm_model = ctk.CTkOptionMenu(
            tpm_frame,
            values=['none', 'tpm-crb', 'tpm-tis', 'tpm-spapr'],
            width=100,
            font=CTK_FONT_SMALL,
        )
        self.tpm_model.set('none')
        self.tpm_model.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.tpm_model.configure(command=self._trigger_change)

        # TPM 版本
        ctk.CTkLabel(tpm_frame, text='版本:', font=CTK_FONT_MAIN, width=50, anchor='w').grid(
            row=1, column=2, padx=10, pady=5, sticky='w'
        )
        self.tpm_version = ctk.CTkOptionMenu(
            tpm_frame, values=['1.2', '2.0'], width=60, font=CTK_FONT_SMALL
        )
        self.tpm_version.set('2.0')
        self.tpm_version.grid(row=1, column=3, padx=5, pady=5, sticky='w')
        self.tpm_version.configure(command=self._trigger_change)

        # 控制器配置
        ctrl_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=8)
        ctrl_frame.grid(row=4, column=0, sticky='ew', padx=10, pady=10)
        ctrl_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(ctrl_frame, text='控制器', font=CTK_FONT_BOLD, text_color='#ff7043').grid(
            row=0, column=0, columnspan=3, padx=10, pady=5, sticky='w'
        )

        # 禁用 USB
        self.disable_usb_check = ctk.CTkCheckBox(
            ctrl_frame, text='禁用 USB', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.disable_usb_check.grid(row=1, column=0, padx=10, pady=5, sticky='w')

        # 禁用声卡
        self.disable_sound_check = ctk.CTkCheckBox(
            ctrl_frame, text='禁用声卡', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.disable_sound_check.grid(row=1, column=1, padx=10, pady=5, sticky='w')

        # 音频模型
        ctk.CTkLabel(ctrl_frame, text='音频:', font=CTK_FONT_MAIN, width=50, anchor='w').grid(
            row=1, column=2, padx=10, pady=5, sticky='w'
        )
        self.audio_model = ctk.CTkOptionMenu(
            ctrl_frame,
            values=['ich9', 'ich6', 'ac97', 'hda', 'none'],
            width=80,
            font=CTK_FONT_SMALL,
        )
        self.audio_model.set('ich9')
        self.audio_model.grid(row=1, column=3, padx=5, pady=5, sticky='w')
        self.audio_model.configure(command=self._trigger_change)

    def _trigger_change(self):
        """触发变化回调."""
        if self.on_change_callback:
            self.on_change_callback()

    def add_usb(self) -> None:
        """添加 USB 设备."""
        from tkinter import messagebox

        usb_id = self.usb_entry.get().strip()
        if not usb_id or ':' not in usb_id:
            messagebox.showwarning('警告', '请输入有效的 USB 设备 ID (格式：Vendor:Product)!')
            return
        self.usb_list.append(usb_id)
        self.usb_display.configure(text=f'已添加 USB: {", ".join(self.usb_list)}')
        self.usb_entry.delete(0, 'end')
        self._trigger_change()

    def get_graphics_config(self):
        """获取图形配置."""
        return {
            'type': self.graphics_type.get(),
            'listen': self.graphics_listen.get().strip() or '0.0.0.0',
            'port': self.graphics_port.get().strip() or '-1',
            'video_model': self.video_model.get(),
            'vram': int(self.vram_entry.get().strip() or '64'),
        }

    def get_usb_config(self):
        """获取 USB 配置."""
        return {
            'controller': self.usb_controller.get(),
            'disabled': self.disable_usb_check.get(),
            'sound_disabled': self.disable_sound_check.get(),
            'devices': self.usb_list.copy(),
        }

    def get_serial_config(self):
        """获取串口配置."""
        return {
            'type': self.serial_type.get(),
            'port': self.serial_port.get().strip() or '0',
        }

    def get_tpm_config(self):
        """获取 TPM 配置."""
        model = self.tpm_model.get()
        if model == 'none':
            return None
        return {
            'model': model,
            'version': self.tpm_version.get(),
        }

    def get_audio_config(self):
        """获取音频配置."""
        model = self.audio_model.get()
        if model == 'none':
            return None
        return {
            'model': model,
        }

    def get_devices_config(self):
        """获取所有设备配置."""
        return {
            'graphics': self.get_graphics_config(),
            'usb': self.get_usb_config(),
            'serial': self.get_serial_config(),
            'tpm': self.get_tpm_config(),
            'audio': self.get_audio_config(),
        }

    def to_xml(self) -> dict:
        """生成XML配置字典.

        Returns:
            包含XML配置的字典，用于XML生成器
        """
        devices_config = self.get_devices_config()
        devices = {
            'emulator': '/usr/bin/qemu-system-x86_64',
            'graphics': devices_config.get('graphics'),
            'videos': [{
                'model': devices_config.get('graphics', {}).get('video_model', 'qxl'),
                'vram': devices_config.get('graphics', {}).get('vram', 64),
            }],
            'controllers': [],
            'serials': [],
            'sounds': [],
        }

        # 添加 USB 控制器
        usb_config = devices_config.get('usb', {})
        if usb_config.get('controller') and usb_config.get('controller') != 'none':
            devices['controllers'].append({
                'type': 'usb',
                'model': usb_config['controller'],
            })

        # 添加串口
        serial_config = devices_config.get('serial', {})
        if serial_config.get('type') and serial_config.get('type') != 'none':
            devices['serials'].append({
                'type': serial_config['type'],
                'port': serial_config.get('port', '0'),
            })

        # 添加音频
        audio_config = devices_config.get('audio', {})
        if audio_config and audio_config.get('model') != 'none':
            devices['sounds'].append({
                'model': audio_config['model'],
            })

        return {'devices': devices}
