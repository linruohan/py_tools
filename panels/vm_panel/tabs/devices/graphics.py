"""图形显示模块 - VNC/SPICE 图形配置."""

import customtkinter as ctk

from utils.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class GraphicsTab(ctk.CTkFrame):
    """图形显示配置 Tab."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent')
        self.on_change_callback = on_change_callback

        self.graphics_type = None
        self.graphics_listen = None
        self.graphics_port = None
        self.video_model = None
        self.vram_entry = None

        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(frame, text='Graphics', font=CTK_FONT_BOLD, text_color='#ba68c8').grid(
            row=0, column=0, columnspan=6, padx=10, pady=5, sticky='w'
        )

        ctk.CTkLabel(frame, text='Graphics:', font=CTK_FONT_MAIN, width=70, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.graphics_type = ctk.CTkOptionMenu(
            frame, values=['vnc', 'spice', 'none'], width=90, font=CTK_FONT_SMALL
        )
        self.graphics_type.set('vnc')
        self.graphics_type.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.graphics_type.configure(command=self._trigger_change)

        ctk.CTkLabel(frame, text='Listen:', font=CTK_FONT_MAIN, width=50, anchor='w').grid(
            row=1, column=2, padx=5, pady=5, sticky='w'
        )
        self.graphics_listen = ctk.CTkEntry(frame, width=100, font=CTK_FONT_SMALL)
        self.graphics_listen.grid(row=1, column=3, padx=5, pady=5, sticky='w')
        self.graphics_listen.insert(0, '0.0.0.0')
        self.graphics_listen.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(frame, text='Port:', font=CTK_FONT_MAIN, width=40, anchor='w').grid(
            row=1, column=4, padx=5, pady=5, sticky='w'
        )
        self.graphics_port = ctk.CTkEntry(frame, width=60, font=CTK_FONT_SMALL)
        self.graphics_port.grid(row=1, column=5, padx=5, pady=5, sticky='w')
        self.graphics_port.insert(0, '-1')
        self.graphics_port.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(frame, text='Video:', font=CTK_FONT_MAIN, width=50, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.video_model = ctk.CTkOptionMenu(
            frame,
            values=['qxl', 'virtio', 'vmvga', 'bochs', 'ramfb', 'virtio-vga', 'virtio-vga-gl'],
            width=120,
            font=CTK_FONT_SMALL,
        )
        self.video_model.set('qxl')
        self.video_model.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.video_model.configure(command=self._trigger_change)

        ctk.CTkLabel(frame, text='VRAM (MB):', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=2, column=2, padx=5, pady=5, sticky='w'
        )
        self.vram_entry = ctk.CTkEntry(frame, width=60, font=CTK_FONT_SMALL)
        self.vram_entry.grid(row=2, column=3, padx=5, pady=5, sticky='w')
        self.vram_entry.insert(0, '64')
        self.vram_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

    def _trigger_change(self, *args):
        """触发变化回调."""
        if self.on_change_callback:
            self.on_change_callback()

    def get_config(self) -> dict:
        """获取图形配置."""
        return {
            'type': self.graphics_type.get(),
            'listen': self.graphics_listen.get().strip() or '0.0.0.0',
            'port': self.graphics_port.get().strip() or '-1',
            'video_model': self.video_model.get(),
            'vram': int(self.vram_entry.get().strip() or '64'),
        }
