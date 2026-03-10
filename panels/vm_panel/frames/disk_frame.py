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
            frame, placeholder_text='磁盘名称', width=120, font=CTK_FONT_SMALL
        )
        name_entry.grid(row=0, column=0, padx=5)

        # 磁盘路径
        path_entry = ctk.CTkEntry(
            frame, placeholder_text='/path/to/disk.qcow2', width=200, font=CTK_FONT_SMALL
        )
        path_entry.grid(row=0, column=1, padx=5)

        # 磁盘类型
        disk_type = ctk.CTkOptionMenu(
            frame, values=['qcow2', 'raw', 'vmdk', 'vdi'], width=80, font=CTK_FONT_SMALL
        )
        disk_type.set('qcow2')
        disk_type.grid(row=0, column=2, padx=5)

        # 磁盘总线
        bus_type = ctk.CTkOptionMenu(
            frame, values=['virtio', 'sata', 'ide', 'scsi'], width=70, font=CTK_FONT_SMALL
        )
        bus_type.set('virtio')
        bus_type.grid(row=0, column=3, padx=5)

        # 删除按钮
        del_btn = ctk.CTkButton(
            frame,
            text='删除',
            width=50,
            fg_color='#f44336',
            hover_color='#d32f2f',
            font=CTK_FONT_SMALL,
            command=lambda: self.remove_disk(frame),
        )
        del_btn.grid(row=0, column=4, padx=5)

        # 绑定变化事件
        for widget in [name_entry, path_entry]:
            widget.bind('<KeyRelease>', lambda e: self._trigger_change())
        for widget in [disk_type, bus_type]:
            widget.configure(command=self._trigger_change)

        self.disk_entries.append(
            {'frame': frame, 'name': name_entry, 'path': path_entry, 'type': disk_type, 'bus': bus_type}
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
            frame, placeholder_text='光驱名称', width=120, font=CTK_FONT_SMALL
        )
        name_entry.grid(row=0, column=0, padx=5)

        # ISO 镜像路径
        path_entry = ctk.CTkEntry(
            frame, placeholder_text='/path/to/image.iso', width=200, font=CTK_FONT_SMALL
        )
        path_entry.grid(row=0, column=1, padx=5)

        # 磁盘类型 - CDROM 固定
        disk_type = ctk.CTkOptionMenu(
            frame, values=['cdrom'], width=80, font=CTK_FONT_SMALL, state='disabled'
        )
        disk_type.set('cdrom')
        disk_type.grid(row=0, column=2, padx=5)

        # 磁盘总线
        bus_type = ctk.CTkOptionMenu(
            frame, values=['sata', 'ide', 'scsi', 'virtio'], width=70, font=CTK_FONT_SMALL
        )
        bus_type.set('sata')
        bus_type.grid(row=0, column=3, padx=5)

        # 删除按钮
        del_btn = ctk.CTkButton(
            frame,
            text='删除',
            width=50,
            fg_color='#f44336',
            hover_color='#d32f2f',
            font=CTK_FONT_SMALL,
            command=lambda: self.remove_disk(frame),
        )
        del_btn.grid(row=0, column=4, padx=5)

        # 绑定变化事件
        for widget in [name_entry, path_entry]:
            widget.bind('<KeyRelease>', lambda e: self._trigger_change())
        bus_type.configure(command=self._trigger_change)

        self.disk_entries.append(
            {'frame': frame, 'name': name_entry, 'path': path_entry, 'type': disk_type, 'bus': bus_type}
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
                    }
                )
        return disks
