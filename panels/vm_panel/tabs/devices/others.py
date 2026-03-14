"""其他设备模块 - 串口、TPM、控制器、音频配置."""

import customtkinter as ctk

from components.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class OthersTab(ctk.CTkFrame):
    """其他设备配置 Tab - 串口、TPM、控制器."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent')
        self.on_change_callback = on_change_callback

        self.serial_type = None
        self.serial_port = None
        self.tpm_model = None
        self.tpm_version = None
        self.disable_usb_check = None
        self.disable_sound_check = None
        self.audio_model = None

        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=1)

        # 串口配置
        serial_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        serial_frame.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
        serial_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            serial_frame, text='Serial Configuration', font=CTK_FONT_BOLD, text_color='#ff9800'
        ).grid(row=0, column=0, columnspan=4, padx=10, pady=5, sticky='w')

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

        ctk.CTkLabel(serial_frame, text='端口:', font=CTK_FONT_MAIN, width=50, anchor='w').grid(
            row=1, column=2, padx=10, pady=5, sticky='w'
        )
        self.serial_port = ctk.CTkEntry(serial_frame, width=80, font=CTK_FONT_SMALL)
        self.serial_port.grid(row=1, column=3, padx=5, pady=5, sticky='w')
        self.serial_port.insert(0, '0')
        self.serial_port.bind('<KeyRelease>', lambda e: self._trigger_change())

        # TPM 配置
        tpm_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        tpm_frame.grid(row=1, column=0, sticky='ew', padx=5, pady=5)
        tpm_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(tpm_frame, text='TPM Device', font=CTK_FONT_BOLD, text_color='#7986cb').grid(
            row=0, column=0, columnspan=4, padx=10, pady=5, sticky='w'
        )

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
        ctrl_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        ctrl_frame.grid(row=2, column=0, sticky='ew', padx=5, pady=5)
        ctrl_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(ctrl_frame, text='Controller', font=CTK_FONT_BOLD, text_color='#ff7043').grid(
            row=0, column=0, columnspan=3, padx=10, pady=5, sticky='w'
        )

        self.disable_usb_check = ctk.CTkCheckBox(
            ctrl_frame, text='Disable USB', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.disable_usb_check.grid(row=1, column=0, padx=10, pady=5, sticky='w')

        self.disable_sound_check = ctk.CTkCheckBox(
            ctrl_frame, text='Disable Sound', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.disable_sound_check.grid(row=1, column=1, padx=10, pady=5, sticky='w')

        ctk.CTkLabel(ctrl_frame, text='Audio:', font=CTK_FONT_MAIN, width=50, anchor='w').grid(
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

    def _trigger_change(self, *args):
        """触发变化回调."""
        if self.on_change_callback:
            self.on_change_callback()

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
        return {'model': model}

    def get_controller_config(self):
        """获取控制器配置."""
        return {
            'disable_usb': self.disable_usb_check.get(),
            'disable_sound': self.disable_sound_check.get(),
        }
