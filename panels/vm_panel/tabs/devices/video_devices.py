"""视频设备模块 - Video Devices 配置 (根据 libvirt devices 文档)."""

import customtkinter as ctk

from components.base_tab import BaseConfigTab
from utils.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class VideoDevicesTab(BaseConfigTab):
    """视频设备配置 Tab - 支持多种视频模型和选项."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        # 在调用父类 __init__ 之前初始化属性 (因为 _init_ui 会被父类 __init__ 调用)
        self.video_list = []
        super().__init__(master, on_change_callback, **kwargs)

    def _init_ui(self) -> None:
        """初始化界面."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # 工具栏
        toolbar = ctk.CTkFrame(self, fg_color='transparent')
        toolbar.grid(row=0, column=0, sticky='ew', padx=5, pady=5)

        add_btn = ctk.CTkButton(
            toolbar,
            text='Add Video Device',
            command=self._add_video,
            fg_color='#4caf50',
            hover_color='#388e3c',
            width=140,
        )
        add_btn.pack(side='left', padx=5)

        # 内容区域
        self.content_frame = ctk.CTkScrollableFrame(
            self, fg_color=BG_COLOR_CONTENT, corner_radius=6
        )
        self.content_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)

        if not self.video_list:
            label = ctk.CTkLabel(
                self.content_frame,
                text='No video devices added',
                font=CTK_FONT_SMALL,
                text_color='#aaaaaa',
                anchor='w',
            )
            label.grid(row=0, column=0, sticky='w', padx=10, pady=10)

    def _add_video(self):
        """添加视频设备对话框."""
        dialog = ctk.CTkToplevel(self)
        dialog.title('Add Video Device')
        dialog.geometry('600x500')
        dialog.transient(self)
        dialog.grab_set()

        VideoConfigDialog(dialog, self._on_video_added)

    def _on_video_added(self, video_config):
        """视频设备添加完成回调."""
        self.video_list.append(video_config)
        self._update_display()
        self._trigger_change()

    def _update_display(self):
        """更新显示."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        if not self.video_list:
            label = ctk.CTkLabel(
                self.content_frame,
                text='No video devices added',
                font=CTK_FONT_SMALL,
                text_color='#aaaaaa',
                anchor='w',
            )
            label.grid(row=0, column=0, sticky='w', padx=10, pady=10)
            return

        for i, video in enumerate(self.video_list):
            video_frame = ctk.CTkFrame(self.content_frame, fg_color='transparent')
            video_frame.grid(row=i, column=0, sticky='ew', padx=10, pady=5)

            model = video.get('model', 'vga')
            vram = video.get('vram', '16384')
            heads = video.get('heads', '1')
            label_text = f'{model} - VRAM: {vram}KB, Heads: {heads}'

            label = ctk.CTkLabel(
                video_frame,
                text=label_text,
                font=CTK_FONT_MAIN,
                anchor='w',
            )
            label.grid(row=0, column=0, sticky='w')

            del_btn = ctk.CTkButton(
                video_frame,
                text='Delete',
                width=60,
                fg_color='#f44336',
                hover_color='#d32f2f',
                font=CTK_FONT_SMALL,
                command=lambda idx=i: self._remove_video(idx),
            )
            del_btn.grid(row=0, column=1, padx=10)

    def _remove_video(self, index):
        """删除视频设备."""
        self.video_list.pop(index)
        self._update_display()
        self._trigger_change()

    def get_config(self) -> dict:
        """获取配置."""
        return {
            'type': 'video_devices',
            'videos': self.video_list.copy(),
        }


class VideoConfigDialog:
    """视频设备配置对话框."""

    def __init__(self, dialog, on_confirm_callback):
        self.dialog = dialog
        self.on_confirm_callback = on_confirm_callback
        self._init_ui()

    def _init_ui(self):
        """初始化 UI."""
        # 基本信息
        info_frame = ctk.CTkFrame(self.dialog, fg_color='transparent')
        info_frame.grid(row=0, column=0, sticky='ew', padx=20, pady=10)
        info_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(info_frame, text='Video Model', font=CTK_FONT_BOLD).grid(
            row=0, column=0, columnspan=4, padx=5, pady=5, sticky='w'
        )

        # Model
        ctk.CTkLabel(info_frame, text='Model:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=5, pady=5, sticky='w'
        )
        self.model_menu = ctk.CTkOptionMenu(
            info_frame,
            values=[
                'vga',
                'cirrus',
                'vmvga',
                'xen',
                'vbox',
                'qxl',
                'virtio',
                'gop',
                'bochs',
                'ramfb',
                'none',
            ],
            width=120,
            font=CTK_FONT_SMALL,
        )
        self.model_menu.set('vga')
        self.model_menu.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        # VRAM (KiB)
        ctk.CTkLabel(
            info_frame, text='VRAM (KiB):', font=CTK_FONT_MAIN, width=100, anchor='w'
        ).grid(row=1, column=2, padx=5, pady=5, sticky='w')
        self.vram_entry = ctk.CTkEntry(
            info_frame, placeholder_text='16384', width=100, font=CTK_FONT_SMALL
        )
        self.vram_entry.insert(0, '16384')
        self.vram_entry.grid(row=1, column=3, padx=5, pady=5, sticky='w')

        # Heads
        ctk.CTkLabel(info_frame, text='Heads:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=2, column=0, padx=5, pady=5, sticky='w'
        )
        self.heads_entry = ctk.CTkEntry(
            info_frame, placeholder_text='1', width=60, font=CTK_FONT_SMALL
        )
        self.heads_entry.insert(0, '1')
        self.heads_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')

        # Primary
        ctk.CTkLabel(info_frame, text='Primary:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=2, column=2, padx=5, pady=5, sticky='w'
        )
        self.primary_check = ctk.CTkCheckBox(info_frame, text='Yes', font=CTK_FONT_SMALL)
        if False:
            self.primary_check.select()
        else:
            self.primary_check.deselect()
        self.primary_check.grid(row=2, column=3, padx=5, pady=5, sticky='w')

        # QXL specific
        qxl_frame = ctk.CTkFrame(self.dialog, fg_color='#333333', corner_radius=6)
        qxl_frame.grid(row=1, column=0, sticky='ew', padx=20, pady=10)
        qxl_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(qxl_frame, text='QXL Options', font=CTK_FONT_SMALL, text_color='#9c27b0').grid(
            row=0, column=0, columnspan=4, padx=5, pady=5, sticky='w'
        )

        # RAM (KiB)
        ctk.CTkLabel(qxl_frame, text='RAM (KiB):', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=5, pady=5, sticky='w'
        )
        self.ram_entry = ctk.CTkEntry(
            qxl_frame, placeholder_text='65536', width=100, font=CTK_FONT_SMALL
        )
        self.ram_entry.insert(0, '65536')
        self.ram_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        # VRAM64 (KiB)
        ctk.CTkLabel(
            qxl_frame, text='VRAM64 (KiB):', font=CTK_FONT_MAIN, width=100, anchor='w'
        ).grid(row=1, column=2, padx=5, pady=5, sticky='w')
        self.vram64_entry = ctk.CTkEntry(
            qxl_frame, placeholder_text='65536', width=100, font=CTK_FONT_SMALL
        )
        self.vram64_entry.insert(0, '65536')
        self.vram64_entry.grid(row=1, column=3, padx=5, pady=5, sticky='w')

        # VGAMEM (KiB)
        ctk.CTkLabel(
            qxl_frame, text='VGAMEM (KiB):', font=CTK_FONT_MAIN, width=100, anchor='w'
        ).grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.vgamem_entry = ctk.CTkEntry(
            qxl_frame, placeholder_text='16384', width=100, font=CTK_FONT_SMALL
        )
        self.vgamem_entry.insert(0, '16384')
        self.vgamem_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')

        # Resolution
        resolution_frame = ctk.CTkFrame(self.dialog, fg_color='transparent')
        resolution_frame.grid(row=2, column=0, sticky='ew', padx=20, pady=10)
        resolution_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(resolution_frame, text='Minimum Resolution', font=CTK_FONT_SMALL).grid(
            row=0, column=0, columnspan=4, padx=5, pady=5, sticky='w'
        )

        # Resolution X
        ctk.CTkLabel(
            resolution_frame, text='Width:', font=CTK_FONT_MAIN, width=80, anchor='w'
        ).grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.res_x_entry = ctk.CTkEntry(
            resolution_frame, placeholder_text='1024', width=80, font=CTK_FONT_SMALL
        )
        self.res_x_entry.insert(0, '1024')
        self.res_x_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        # Resolution Y
        ctk.CTkLabel(
            resolution_frame, text='Height:', font=CTK_FONT_MAIN, width=80, anchor='w'
        ).grid(row=1, column=2, padx=5, pady=5, sticky='w')
        self.res_y_entry = ctk.CTkEntry(
            resolution_frame, placeholder_text='768', width=80, font=CTK_FONT_SMALL
        )
        self.res_y_entry.insert(0, '768')
        self.res_y_entry.grid(row=1, column=3, padx=5, pady=5, sticky='w')

        # VirtIO specific
        virtio_frame = ctk.CTkFrame(self.dialog, fg_color='#333333', corner_radius=6)
        virtio_frame.grid(row=3, column=0, sticky='ew', padx=20, pady=10)
        virtio_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            virtio_frame, text='VirtIO Options', font=CTK_FONT_SMALL, text_color='#4caf50'
        ).grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky='w')

        # Blob
        ctk.CTkLabel(virtio_frame, text='Blob:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=5, pady=5, sticky='w'
        )
        self.blob_check = ctk.CTkCheckBox(
            virtio_frame, text='Enable blob resources', font=CTK_FONT_SMALL
        )
        if False:
            self.blob_check.select()
        else:
            self.blob_check.deselect()
        self.blob_check.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        # EDID
        ctk.CTkLabel(virtio_frame, text='EDID:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=2, padx=5, pady=5, sticky='w'
        )
        self.edid_check = ctk.CTkCheckBox(virtio_frame, text='Expose EDID', font=CTK_FONT_SMALL)
        if True:
            self.edid_check.select()
        else:
            self.edid_check.deselect()
        self.edid_check.grid(row=1, column=3, padx=5, pady=5, sticky='w')

        # 按钮
        btn_frame = ctk.CTkFrame(self.dialog, fg_color='transparent')
        btn_frame.grid(row=4, column=0, sticky='e', padx=20, pady=10)

        ctk.CTkButton(
            btn_frame,
            text='Cancel',
            command=self.dialog.destroy,
            width=80,
            fg_color='#9e9e9e',
            hover_color='#757575',
        ).pack(side='right', padx=5)

        ctk.CTkButton(
            btn_frame,
            text='OK',
            command=self._confirm,
            width=80,
            fg_color='#4caf50',
            hover_color='#388e3c',
        ).pack(side='right', padx=5)

    def _confirm(self):
        """确认添加."""
        model = self.model_menu.get()
        config = {
            'model': model,
            'vram': self.vram_entry.get().strip() or '16384',
            'heads': self.heads_entry.get().strip() or '1',
            'primary': self.primary_check.get(),
        }

        # QXL specific
        if model == 'qxl':
            config['ram'] = self.ram_entry.get().strip() or '65536'
            config['vram64'] = self.vram64_entry.get().strip() or '65536'
            config['vgamem'] = self.vgamem_entry.get().strip() or '16384'

        # Resolution
        res_x = self.res_x_entry.get().strip()
        res_y = self.res_y_entry.get().strip()
        if res_x and res_y:
            config['resolution'] = {'x': int(res_x), 'y': int(res_y)}

        # VirtIO specific
        if model == 'virtio':
            config['blob'] = self.blob_check.get()
            config['edid'] = self.edid_check.get()

        self.on_confirm_callback(config)
        self.dialog.destroy()
