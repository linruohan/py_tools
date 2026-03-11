"""磁盘配置框架."""

import customtkinter as ctk

from ..styles import CTK_FONT_SMALL


class ScrollableDiskFrame(ctk.CTkScrollableFrame):
    """可滚动磁盘配置框架."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.disk_entries = []
        self.disk_count = 0
        self.on_change_callback = on_change_callback

    def add_disk(self):
        """添加磁盘配置行."""
        frame = ctk.CTkFrame(self, fg_color='transparent')
        frame.grid(row=self.disk_count, column=0, sticky='ew', pady=5)

        # 磁盘名称
        name_entry = ctk.CTkEntry(
            frame, placeholder_text='磁盘名称', width=100, font=CTK_FONT_SMALL
        )
        name_entry.grid(row=0, column=0, padx=2)
        name_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        # 磁盘路径
        path_entry = ctk.CTkEntry(
            frame, placeholder_text='/path/to/disk.qcow2', width=180, font=CTK_FONT_SMALL
        )
        path_entry.grid(row=0, column=1, padx=2)
        path_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        # 磁盘类型
        disk_type = ctk.CTkOptionMenu(
            frame, values=['qcow2', 'raw', 'vmdk', 'vdi', 'iso'], width=70, font=CTK_FONT_SMALL
        )
        disk_type.set('qcow2')
        disk_type.grid(row=0, column=2, padx=2)
        disk_type.configure(command=self._trigger_change)

        # 磁盘总线
        bus_type = ctk.CTkOptionMenu(
            frame, values=['virtio', 'sata', 'ide', 'scsi', 'usb'], width=60, font=CTK_FONT_SMALL
        )
        bus_type.set('virtio')
        bus_type.grid(row=0, column=3, padx=2)
        bus_type.configure(command=self._trigger_change)

        # 缓存模式
        cache_mode = ctk.CTkOptionMenu(
            frame, values=['none', 'writeback', 'writethrough', 'unsafe', 'directsync'], width=90, font=CTK_FONT_SMALL
        )
        cache_mode.set('none')
        cache_mode.grid(row=0, column=4, padx=2)
        cache_mode.configure(command=self._trigger_change)

        # IO 模式
        io_mode = ctk.CTkOptionMenu(
            frame, values=['native', 'native_cached', 'threads', 'directsync'], width=90, font=CTK_FONT_SMALL
        )
        io_mode.set('native')
        io_mode.grid(row=0, column=5, padx=2)
        io_mode.configure(command=self._trigger_change)

        # 丢弃/Trim 支持
        discard_check = ctk.CTkCheckBox(frame, text='Trim', width=40, font=CTK_FONT_SMALL)
        discard_check.grid(row=0, column=6, padx=2)
        discard_check.configure(command=self._trigger_change)

        # 只读
        readonly_check = ctk.CTkCheckBox(frame, text='RO', width=35, font=CTK_FONT_SMALL)
        readonly_check.grid(row=0, column=7, padx=2)
        readonly_check.configure(command=self._trigger_change)

        # 删除按钮
        del_btn = ctk.CTkButton(
            frame,
            text='X',
            width=25,
            fg_color='#f44336',
            hover_color='#d32f2f',
            font=CTK_FONT_SMALL,
            command=lambda: self.remove_disk(frame),
        )
        del_btn.grid(row=0, column=8, padx=2)

        self.disk_entries.append(
            {
                'frame': frame,
                'name': name_entry,
                'path': path_entry,
                'type': disk_type,
                'bus': bus_type,
                'cache': cache_mode,
                'io': io_mode,
                'discard': discard_check,
                'readonly': readonly_check,
            }
        )
        self.disk_count += 1

    def _trigger_change(self):
        """触发变化回调."""
        if self.on_change_callback:
            self.on_change_callback()

    def remove_disk(self, frame):
        """删除磁盘配置行."""
        for i, entry in enumerate(self.disk_entries):
            if entry['frame'] == frame:
                frame.destroy()
                self.disk_entries.pop(i)
                self.disk_count -= 1
                # 重新布局
                for j, e in enumerate(self.disk_entries):
                    e['frame'].grid(row=j, column=0, sticky='ew', pady=5)
                break

    def add_cdrom(self):
        """添加光驱配置行."""
        frame = ctk.CTkFrame(self, fg_color='transparent')
        frame.grid(row=self.disk_count, column=0, sticky='ew', pady=5)

        # 光驱名称
        name_entry = ctk.CTkEntry(
            frame, placeholder_text='光驱名称', width=100, font=CTK_FONT_SMALL
        )
        name_entry.grid(row=0, column=0, padx=2)
        name_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        # ISO 镜像路径
        path_entry = ctk.CTkEntry(
            frame, placeholder_text='/path/to/image.iso', width=180, font=CTK_FONT_SMALL
        )
        path_entry.grid(row=0, column=1, padx=2)
        path_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        # 磁盘类型 - CDROM 固定
        disk_type = ctk.CTkOptionMenu(
            frame, values=['cdrom'], width=70, font=CTK_FONT_SMALL, state='disabled'
        )
        disk_type.set('cdrom')
        disk_type.grid(row=0, column=2, padx=2)

        # 磁盘总线
        bus_type = ctk.CTkOptionMenu(
            frame, values=['sata', 'ide', 'scsi', 'virtio'], width=60, font=CTK_FONT_SMALL
        )
        bus_type.set('sata')
        bus_type.grid(row=0, column=3, padx=2)
        bus_type.configure(command=self._trigger_change)

        # 缓存模式
        cache_mode = ctk.CTkOptionMenu(
            frame, values=['none', 'writeback', 'writethrough', 'unsafe', 'directsync'], width=90, font=CTK_FONT_SMALL
        )
        cache_mode.set('none')
        cache_mode.grid(row=0, column=4, padx=2)
        cache_mode.configure(command=self._trigger_change)

        # IO 模式
        io_mode = ctk.CTkOptionMenu(
            frame, values=['native', 'native_cached', 'threads', 'directsync'], width=90, font=CTK_FONT_SMALL
        )
        io_mode.set('native')
        io_mode.grid(row=0, column=5, padx=2)
        io_mode.configure(command=self._trigger_change)

        # 只读 - CDROM 固定选中
        readonly_check = ctk.CTkCheckBox(frame, text='RO', width=35, font=CTK_FONT_SMALL, state='disabled')
        readonly_check.grid(row=0, column=6, padx=2)
        readonly_check.select()

        # 删除按钮
        del_btn = ctk.CTkButton(
            frame,
            text='X',
            width=25,
            fg_color='#f44336',
            hover_color='#d32f2f',
            font=CTK_FONT_SMALL,
            command=lambda: self.remove_disk(frame),
        )
        del_btn.grid(row=0, column=7, padx=2)

        self.disk_entries.append(
            {
                'frame': frame,
                'name': name_entry,
                'path': path_entry,
                'type': disk_type,
                'bus': bus_type,
                'cache': cache_mode,
                'io': io_mode,
                'discard': None,
                'readonly': readonly_check,
            }
        )
        self.disk_count += 1

    def get_disks(self):
        """获取所有磁盘配置."""
        disks = []
        for entry in self.disk_entries:
            name = entry['name'].get().strip()
            path = entry['path'].get().strip()
            disk_type = entry['type'].get()
            if name or path:
                disks.append(
                    {
                        'name': name or f'disk{len(disks)}',
                        'path': path,
                        'type': disk_type,
                        'bus': entry['bus'].get(),
                        'cache': entry['cache'].get() if entry.get('cache') else 'none',
                        'io': entry['io'].get() if entry.get('io') else 'native',
                        'discard': entry['discard'].get() if entry.get('discard') else False,
                        'readonly': entry['readonly'].get() if entry.get('readonly') else False,
                    }
                )
        return disks
