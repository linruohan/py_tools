"""设备配置 Tab - 图形、USB、控制器等."""

import customtkinter as ctk

from ..styles import CTK_FONT_MAIN, CTK_FONT_BOLD, CTK_FONT_SMALL, BG_COLOR_CONTENT


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
        self.video_model = None
        self.vram_entry = None
        self.usb_controller = None
        self.usb_entry = None
        self.usb_display = None
        self.disable_usb_check = None
        self.disable_sound_check = None

        # 初始化 UI
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面."""
        # 配置 grid 权重
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)

        # 图形配置
        graphics_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=8)
        graphics_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=10)
        graphics_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            graphics_frame, text='图形显示', font=CTK_FONT_BOLD, text_color='#ba68c8'
        ).grid(row=0, column=0, columnspan=4, padx=10, pady=5, sticky='w')

        # 图形类型
        ctk.CTkLabel(
            graphics_frame, text='图形:', font=CTK_FONT_MAIN, width=80, anchor='w'
        ).grid(row=1, column=0, padx=10, pady=5, sticky='w')
        self.graphics_type = ctk.CTkOptionMenu(
            graphics_frame, values=['vnc', 'spice', 'none'], width=100, font=CTK_FONT_SMALL
        )
        self.graphics_type.set('vnc')
        self.graphics_type.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        # 监听地址
        ctk.CTkLabel(
            graphics_frame, text='监听:', font=CTK_FONT_MAIN, width=60, anchor='w'
        ).grid(row=1, column=2, padx=10, pady=5, sticky='w')
        self.graphics_listen = ctk.CTkEntry(graphics_frame, width=120, font=CTK_FONT_SMALL)
        self.graphics_listen.grid(row=1, column=3, padx=5, pady=5, sticky='w')
        self.graphics_listen.insert(0, '0.0.0.0')

        # 视频模型
        ctk.CTkLabel(
            graphics_frame, text='视频:', font=CTK_FONT_MAIN, width=60, anchor='w'
        ).grid(row=2, column=0, padx=10, pady=5, sticky='w')
        self.video_model = ctk.CTkOptionMenu(
            graphics_frame, values=['qxl', 'virtio', 'vmvga', 'bochs', 'ramfb'], width=100, font=CTK_FONT_SMALL
        )
        self.video_model.set('qxl')
        self.video_model.grid(row=2, column=1, padx=5, pady=5, sticky='w')

        # VRAM 大小
        ctk.CTkLabel(
            graphics_frame, text='VRAM (MB):', font=CTK_FONT_MAIN, width=80, anchor='w'
        ).grid(row=2, column=2, padx=10, pady=5, sticky='w')
        self.vram_entry = ctk.CTkEntry(graphics_frame, width=80, font=CTK_FONT_SMALL)
        self.vram_entry.grid(row=2, column=3, padx=5, pady=5, sticky='w')
        self.vram_entry.insert(0, '64')

        # USB 控制器
        usb_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=8)
        usb_frame.grid(row=1, column=0, sticky='ew', padx=10, pady=10)
        usb_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            usb_frame, text='USB 控制器', font=CTK_FONT_BOLD, text_color='#2196f3'
        ).grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky='w')

        # USB 控制器模型
        ctk.CTkLabel(
            usb_frame, text='控制器:', font=CTK_FONT_MAIN, width=80, anchor='w'
        ).grid(row=1, column=0, padx=10, pady=5, sticky='w')
        self.usb_controller = ctk.CTkOptionMenu(
            usb_frame, values=['qemu-xhci', 'piix3-uhci', 'piix4-uhci', 'nec-xhci', 'vt82c686b-uhci', 'none'],
            width=150, font=CTK_FONT_SMALL
        )
        self.usb_controller.set('qemu-xhci')
        self.usb_controller.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        # USB 直通设备
        ctk.CTkLabel(
            usb_frame, text='USB 设备:', font=CTK_FONT_MAIN, width=80, anchor='w'
        ).grid(row=1, column=2, padx=10, pady=5, sticky='w')
        self.usb_entry = ctk.CTkEntry(usb_frame, placeholder_text='Vendor:Product (如 8087:8008)', width=200, font=CTK_FONT_SMALL)
        self.usb_entry.grid(row=1, column=3, padx=5, pady=5, sticky='w')
        self.usb_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        # 添加 USB 按钮
        add_usb_btn = ctk.CTkButton(
            usb_frame,
            text='添加',
            command=self.add_usb,
            fg_color='#00bcd4',
            hover_color='#0097a7',
            width=80,
            font=CTK_FONT_SMALL,
        )
        add_usb_btn.grid(row=1, column=4, padx=5)

        self.usb_display = ctk.CTkLabel(
            usb_frame, text='', font=CTK_FONT_SMALL, text_color='#aaaaaa', anchor='w'
        )
        self.usb_display.grid(row=2, column=0, columnspan=5, padx=10, pady=5, sticky='w')

        # 控制器配置
        ctrl_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=8)
        ctrl_frame.grid(row=2, column=0, sticky='ew', padx=10, pady=10)
        ctrl_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            ctrl_frame, text='控制器', font=CTK_FONT_BOLD, text_color='#ff7043'
        ).grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky='w')

        # 禁用 USB
        self.disable_usb_check = ctk.CTkCheckBox(
            ctrl_frame, text='禁用 USB', font=CTK_FONT_SMALL
        )
        self.disable_usb_check.grid(row=1, column=0, padx=10, pady=5, sticky='w')

        # 禁用声卡
        self.disable_sound_check = ctk.CTkCheckBox(
            ctrl_frame, text='禁用声卡', font=CTK_FONT_SMALL
        )
        self.disable_sound_check.grid(row=1, column=1, padx=10, pady=5, sticky='w')

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
