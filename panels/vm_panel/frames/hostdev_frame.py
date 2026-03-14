"""PCI 直通设备配置框架."""

import customtkinter as ctk

from components.styles import CTK_FONT_SMALL


class ScrollableHostdevFrame(ctk.CTkScrollableFrame):
    """可滚动 PCI 直通设备配置框架."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.hostdev_entries = []
        self.hostdev_count = 0
        self.on_change_callback = on_change_callback

    def add_hostdev(self):
        """添加 PCI 直通设备配置行."""
        frame = ctk.CTkFrame(self, fg_color='transparent')
        frame.grid(row=self.hostdev_count, column=0, sticky='ew', pady=5)

        # 设备名称
        name_entry = ctk.CTkEntry(
            frame, placeholder_text='设备名称', width=100, font=CTK_FONT_SMALL
        )
        name_entry.grid(row=0, column=0, padx=5)

        # PCI 地址 (domain:bus:slot.function)
        pci_entry = ctk.CTkEntry(
            frame, placeholder_text='0000:00:00.0', width=140, font=CTK_FONT_SMALL
        )
        pci_entry.grid(row=0, column=1, padx=5)

        # 设备类型
        dev_type = ctk.CTkOptionMenu(
            frame, values=['pci', 'usb', 'mdev'], width=70, font=CTK_FONT_SMALL
        )
        dev_type.set('pci')
        dev_type.grid(row=0, column=2, padx=5)

        # 删除按钮
        del_btn = ctk.CTkButton(
            frame,
            text='删除',
            width=50,
            fg_color='#f44336',
            hover_color='#d32f2f',
            font=CTK_FONT_SMALL,
            command=lambda: self.remove_hostdev(frame),
        )
        del_btn.grid(row=0, column=3, padx=5)

        # 绑定变化事件
        for widget in [name_entry, pci_entry]:
            widget.bind('<KeyRelease>', lambda e: self._trigger_change())
        dev_type.configure(command=self._trigger_change)

        self.hostdev_entries.append(
            {'frame': frame, 'name': name_entry, 'pci': pci_entry, 'type': dev_type}
        )
        self.hostdev_count += 1

    def _trigger_change(self):
        """触发变化回调."""
        if self.on_change_callback:
            self.on_change_callback()

    def remove_hostdev(self, frame):
        """删除 PCI 直通设备配置行."""
        for i, entry in enumerate(self.hostdev_entries):
            if entry['frame'] == frame:
                frame.destroy()
                self.hostdev_entries.pop(i)
                self.hostdev_count -= 1
                # 重新布局
                for j, e in enumerate(self.hostdev_entries):
                    e['frame'].grid(row=j, column=0, sticky='ew', pady=5)
                break

    def get_hostdevs(self):
        """获取所有 PCI 直通设备配置."""
        hostdevs = []
        for entry in self.hostdev_entries:
            name = entry['name'].get().strip()
            pci = entry['pci'].get().strip()
            if pci:
                hostdevs.append(
                    {
                        'name': name or f'hostdev{len(hostdevs)}',
                        'pci': pci,
                        'type': entry['type'].get(),
                    }
                )
        return hostdevs
