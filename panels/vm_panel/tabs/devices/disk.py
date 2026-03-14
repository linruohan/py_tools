"""磁盘设备模块 - 磁盘设备配置和对话框."""

import customtkinter as ctk

from components.inner_tab_panel import InnerTabPanel
from components.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class DiskDevicesTab(ctk.CTkFrame):
    """磁盘设备配置 Tab - 支持 file, block, network, volume, dir, nvme, vhostuser, vhostvdpa, ctl 类型."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent')
        self.on_change_callback = on_change_callback
        self.disk_list = []

        self._init_ui()

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
            text='Add Disk Device',
            command=self._add_disk,
            fg_color='#4caf50',
            hover_color='#388e3c',
            width=120,
        )
        add_btn.pack(side='left', padx=5)

        clear_btn = ctk.CTkButton(
            toolbar,
            text='Clear List',
            command=self._clear_list,
            fg_color='#f44336',
            hover_color='#d32f2f',
            width=100,
        )
        clear_btn.pack(side='left', padx=5)

        # 内容区域
        self.content_frame = ctk.CTkScrollableFrame(
            self, fg_color=BG_COLOR_CONTENT, corner_radius=6
        )
        self.content_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)

        # 设备列表显示
        self.disk_display = ctk.CTkLabel(
            self.content_frame,
            text='暂无设备',
            font=CTK_FONT_SMALL,
            text_color='#aaaaaa',
            anchor='w',
        )
        self.disk_display.grid(row=0, column=0, sticky='w', padx=10, pady=10)

    def _add_disk(self):
        """Add disk device configuration dialog."""
        dialog = ctk.CTkToplevel(self)
        dialog.title('Add Disk Device')
        dialog.geometry('700x600')
        dialog.transient(self)
        dialog.grab_set()

        DiskConfigDialog(dialog, self._on_disk_added)

    def _on_disk_added(self, disk_config):
        """磁盘设备添加完成回调."""
        self.disk_list.append(disk_config)
        self._update_display()
        self._trigger_change()

    def _clear_list(self):
        """清空磁盘设备列表."""
        self.disk_list.clear()
        self._update_display()
        self._trigger_change()

    def _update_display(self):
        """更新显示."""
        # 清除旧的显示
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        if not self.disk_list:
            label = ctk.CTkLabel(
                self.content_frame,
                text='暂无设备',
                font=CTK_FONT_SMALL,
                text_color='#aaaaaa',
                anchor='w',
            )
            label.grid(row=0, column=0, sticky='w', padx=10, pady=10)
            return

        # 显示所有磁盘设备
        for i, disk in enumerate(self.disk_list):
            disk_frame = ctk.CTkFrame(self.content_frame, fg_color='transparent')
            disk_frame.grid(row=i, column=0, sticky='ew', padx=10, pady=5)

            # 设备类型标签
            type_label = f'[{disk.get("type", "file")}] {disk.get("device", "disk")}'
            source_label = disk.get('source', '')
            if disk.get('protocol'):
                source_label = f'{disk["protocol"]}:{source_label}'

            label = ctk.CTkLabel(
                disk_frame,
                text=f'{type_label}: {source_label} -> {disk.get("target_dev", "N/A")} ({disk.get("bus", "N/A")})',
                font=CTK_FONT_MAIN,
                anchor='w',
            )
            label.grid(row=0, column=0, sticky='w')

            # 删除按钮
            del_btn = ctk.CTkButton(
                disk_frame,
                text='删除',
                width=60,
                fg_color='#f44336',
                hover_color='#d32f2f',
                font=CTK_FONT_SMALL,
                command=lambda idx=i: self._remove_disk(idx),
            )
            del_btn.grid(row=0, column=1, padx=10)

    def _remove_disk(self, index):
        """删除指定索引的磁盘设备."""
        self.disk_list.pop(index)
        self._update_display()
        self._trigger_change()

    def _trigger_change(self, *args):
        """触发变化回调."""
        if self.on_change_callback:
            self.on_change_callback()

    def get_config(self) -> dict:
        """获取配置."""
        return {
            'type': 'disk_devices',
            'devices': self.disk_list.copy(),
        }


class DiskConfigDialog:
    """磁盘设备配置对话框."""

    def __init__(self, dialog, on_confirm_callback):
        self.dialog = dialog
        self.on_confirm_callback = on_confirm_callback
        self.config = {}
        self._init_ui()

    def _init_ui(self):
        """初始化 UI."""
        # 基本信息
        info_frame = ctk.CTkFrame(self.dialog, fg_color='transparent')
        info_frame.grid(row=0, column=0, sticky='ew', padx=20, pady=10)
        info_frame.grid_columnconfigure(1, weight=1)

        # Disk Type
        ctk.CTkLabel(info_frame, text='Type:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=0, column=0, padx=5, pady=5, sticky='w'
        )
        self.type_menu = ctk.CTkOptionMenu(
            info_frame,
            values=[
                'file',
                'block',
                'network',
                'volume',
                'dir',
                'nvme',
                'vhostuser',
                'vhostvdpa',
                'ctl',
            ],
            width=120,
            font=CTK_FONT_SMALL,
            command=self._on_type_changed,
        )
        self.type_menu.set('file')
        self.type_menu.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        # Device Type
        ctk.CTkLabel(
            info_frame, text='Device Type:', font=CTK_FONT_MAIN, width=80, anchor='w'
        ).grid(row=0, column=2, padx=5, pady=5, sticky='w')
        self.device_menu = ctk.CTkOptionMenu(
            info_frame,
            values=['disk', 'cdrom', 'lun', 'floppy'],
            width=100,
            font=CTK_FONT_SMALL,
        )
        self.device_menu.set('disk')
        self.device_menu.grid(row=0, column=3, padx=5, pady=5, sticky='w')

        # Target Device
        ctk.CTkLabel(
            info_frame, text='Target Device:', font=CTK_FONT_MAIN, width=80, anchor='w'
        ).grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.target_entry = ctk.CTkEntry(
            info_frame, placeholder_text='vda', width=100, font=CTK_FONT_SMALL
        )
        self.target_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        # Bus Type
        ctk.CTkLabel(info_frame, text='Bus:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=1, column=2, padx=5, pady=5, sticky='w'
        )
        self.bus_menu = ctk.CTkOptionMenu(
            info_frame,
            values=['virtio', 'sata', 'ide', 'scsi', 'usb', 'nvme'],
            width=80,
            font=CTK_FONT_SMALL,
        )
        self.bus_menu.set('virtio')
        self.bus_menu.grid(row=1, column=3, padx=5, pady=5, sticky='w')

        # 动态内容区域
        self.dynamic_frame = ctk.CTkFrame(self.dialog, fg_color='transparent')
        self.dynamic_frame.grid(row=1, column=0, sticky='nsew', padx=20, pady=10)
        self.dynamic_frame.grid_columnconfigure(1, weight=1)

        self._init_dynamic_ui()

        # Other Options
        options_frame = ctk.CTkFrame(self.dialog, fg_color='transparent')
        options_frame.grid(row=2, column=0, sticky='ew', padx=20, pady=10)
        options_frame.grid_columnconfigure(1, weight=1)

        # Read-only
        self.readonly_check = ctk.CTkCheckBox(options_frame, text='Read-only', font=CTK_FONT_SMALL)
        self.readonly_check.grid(row=0, column=0, padx=5, pady=5, sticky='w')

        # Boot Order
        ctk.CTkLabel(
            options_frame, text='Boot Order:', font=CTK_FONT_MAIN, width=80, anchor='w'
        ).grid(row=0, column=1, padx=5, pady=5, sticky='w')
        self.boot_order_entry = ctk.CTkEntry(options_frame, width=60, font=CTK_FONT_SMALL)
        self.boot_order_entry.grid(row=0, column=2, padx=5, pady=5, sticky='w')
        self.boot_order_entry.insert(0, '')

        # Startup Policy
        ctk.CTkLabel(
            options_frame, text='Startup Policy:', font=CTK_FONT_MAIN, width=80, anchor='w'
        ).grid(row=0, column=3, padx=5, pady=5, sticky='w')
        self.startup_menu = ctk.CTkOptionMenu(
            options_frame, values=['required', 'optional'], width=100, font=CTK_FONT_SMALL
        )
        self.startup_menu.set('optional')
        self.startup_menu.grid(row=0, column=4, padx=5, pady=5, sticky='w')

        # 按钮
        btn_frame = ctk.CTkFrame(self.dialog, fg_color='transparent')
        btn_frame.grid(row=3, column=0, sticky='e', padx=20, pady=10)

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

    def _init_dynamic_ui(self):
        """初始化动态内容 UI."""
        # 清除现有内容
        for widget in self.dynamic_frame.winfo_children():
            widget.destroy()

        disk_type = self.type_menu.get()

        row = 0

        # file type
        if disk_type == 'file':
            ctk.CTkLabel(
                self.dynamic_frame, text='File Path:', font=CTK_FONT_MAIN, width=80, anchor='w'
            ).grid(row=row, column=0, padx=5, pady=5, sticky='w')
            self.source_entry = ctk.CTkEntry(
                self.dynamic_frame,
                placeholder_text='/var/lib/libvirt/images/disk.qcow2',
                width=400,
                font=CTK_FONT_SMALL,
            )
            self.source_entry.grid(row=row, column=1, padx=5, pady=5, sticky='ew')

            ctk.CTkLabel(
                self.dynamic_frame, text='Driver Format:', font=CTK_FONT_MAIN, width=80, anchor='w'
            ).grid(row=row + 1, column=0, padx=5, pady=5, sticky='w')
            self.driver_menu = ctk.CTkOptionMenu(
                self.dynamic_frame,
                values=['qcow2', 'raw', 'vmdk', 'vdi', 'vpc', 'parallels'],
                width=100,
                font=CTK_FONT_SMALL,
            )
            self.driver_menu.set('qcow2')
            self.driver_menu.grid(row=row + 1, column=1, padx=5, pady=5, sticky='w')

        # block type
        elif disk_type == 'block':
            ctk.CTkLabel(
                self.dynamic_frame, text='Block Device:', font=CTK_FONT_MAIN, width=80, anchor='w'
            ).grid(row=row, column=0, padx=5, pady=5, sticky='w')
            self.source_entry = ctk.CTkEntry(
                self.dynamic_frame, placeholder_text='/dev/sda', width=300, font=CTK_FONT_SMALL
            )
            self.source_entry.grid(row=row, column=1, padx=5, pady=5, sticky='w')

        # network type
        elif disk_type == 'network':
            ctk.CTkLabel(
                self.dynamic_frame, text='Protocol:', font=CTK_FONT_MAIN, width=80, anchor='w'
            ).grid(row=row, column=0, padx=5, pady=5, sticky='w')
            self.protocol_menu = ctk.CTkOptionMenu(
                self.dynamic_frame,
                values=['sheepdog', 'rbd', 'iscsi', 'nfs', 'http', 'https', 'ftp', 'ftps', 'tftp'],
                width=100,
                font=CTK_FONT_SMALL,
                command=self._on_protocol_changed,
            )
            self.protocol_menu.set('rbd')
            self.protocol_menu.grid(row=row, column=1, padx=5, pady=5, sticky='w')

            ctk.CTkLabel(
                self.dynamic_frame, text='Image Name:', font=CTK_FONT_MAIN, width=80, anchor='w'
            ).grid(row=row + 1, column=0, padx=5, pady=5, sticky='w')
            self.source_entry = ctk.CTkEntry(
                self.dynamic_frame, placeholder_text='pool/image', width=300, font=CTK_FONT_SMALL
            )
            self.source_entry.grid(row=row + 1, column=1, padx=5, pady=5, sticky='ew')

            ctk.CTkLabel(
                self.dynamic_frame, text='Host:', font=CTK_FONT_MAIN, width=80, anchor='w'
            ).grid(row=row + 2, column=0, padx=5, pady=5, sticky='w')
            self.host_entry = ctk.CTkEntry(
                self.dynamic_frame, placeholder_text='hostname', width=150, font=CTK_FONT_SMALL
            )
            self.host_entry.grid(row=row + 2, column=1, padx=5, pady=5, sticky='w')

            ctk.CTkLabel(
                self.dynamic_frame, text='Port:', font=CTK_FONT_MAIN, width=50, anchor='w'
            ).grid(row=row + 2, column=2, padx=5, pady=5, sticky='w')
            self.port_entry = ctk.CTkEntry(
                self.dynamic_frame, placeholder_text='7000', width=60, font=CTK_FONT_SMALL
            )
            self.port_entry.grid(row=row + 2, column=3, padx=5, pady=5, sticky='w')

            # Authentication
            self.auth_check = ctk.CTkCheckBox(
                self.dynamic_frame, text='Enable Authentication', font=CTK_FONT_SMALL
            )
            self.auth_check.grid(row=row + 3, column=0, padx=5, pady=5, sticky='w')

            ctk.CTkLabel(
                self.dynamic_frame, text='Username:', font=CTK_FONT_MAIN, width=80, anchor='w'
            ).grid(row=row + 3, column=1, padx=5, pady=5, sticky='w')
            self.username_entry = ctk.CTkEntry(
                self.dynamic_frame, placeholder_text='myuser', width=100, font=CTK_FONT_SMALL
            )
            self.username_entry.grid(row=row + 3, column=2, padx=5, pady=5, sticky='w')

            ctk.CTkLabel(
                self.dynamic_frame, text='Secret:', font=CTK_FONT_MAIN, width=60, anchor='w'
            ).grid(row=row + 3, column=3, padx=5, pady=5, sticky='w')
            self.secret_entry = ctk.CTkEntry(
                self.dynamic_frame, placeholder_text='libvirtiscsi', width=120, font=CTK_FONT_SMALL
            )
            self.secret_entry.grid(row=row + 3, column=4, padx=5, pady=5, sticky='w')

        # volume type
        elif disk_type == 'volume':
            ctk.CTkLabel(
                self.dynamic_frame, text='Storage Pool:', font=CTK_FONT_MAIN, width=80, anchor='w'
            ).grid(row=row, column=0, padx=5, pady=5, sticky='w')
            self.pool_entry = ctk.CTkEntry(
                self.dynamic_frame, placeholder_text='blk-pool0', width=200, font=CTK_FONT_SMALL
            )
            self.pool_entry.grid(row=row, column=1, padx=5, pady=5, sticky='w')

            ctk.CTkLabel(
                self.dynamic_frame, text='Volume:', font=CTK_FONT_MAIN, width=80, anchor='w'
            ).grid(row=row + 1, column=0, padx=5, pady=5, sticky='w')
            self.volume_entry = ctk.CTkEntry(
                self.dynamic_frame, placeholder_text='vol0', width=200, font=CTK_FONT_SMALL
            )
            self.volume_entry.grid(row=row + 1, column=1, padx=5, pady=5, sticky='w')

        # dir type
        elif disk_type == 'dir':
            ctk.CTkLabel(
                self.dynamic_frame, text='Directory:', font=CTK_FONT_MAIN, width=80, anchor='w'
            ).grid(row=row, column=0, padx=5, pady=5, sticky='w')
            self.source_entry = ctk.CTkEntry(
                self.dynamic_frame,
                placeholder_text='/var/somefiles',
                width=300,
                font=CTK_FONT_SMALL,
            )
            self.source_entry.grid(row=row, column=1, padx=5, pady=5, sticky='ew')

        # nvme type
        elif disk_type == 'nvme':
            ctk.CTkLabel(
                self.dynamic_frame, text='Namespace:', font=CTK_FONT_MAIN, width=80, anchor='w'
            ).grid(row=row, column=0, padx=5, pady=5, sticky='w')
            self.ns_entry = ctk.CTkEntry(
                self.dynamic_frame, placeholder_text='1', width=60, font=CTK_FONT_SMALL
            )
            self.ns_entry.grid(row=row, column=1, padx=5, pady=5, sticky='w')

            ctk.CTkLabel(
                self.dynamic_frame, text='PCI Address:', font=CTK_FONT_MAIN, width=80, anchor='w'
            ).grid(row=row + 1, column=0, padx=5, pady=5, sticky='w')
            self.pci_entry = ctk.CTkEntry(
                self.dynamic_frame, placeholder_text='0000:01:00.0', width=150, font=CTK_FONT_SMALL
            )
            self.pci_entry.grid(row=row + 1, column=1, padx=5, pady=5, sticky='w')

        # vhostuser type
        elif disk_type == 'vhostuser':
            ctk.CTkLabel(
                self.dynamic_frame, text='Socket:', font=CTK_FONT_MAIN, width=80, anchor='w'
            ).grid(row=row, column=0, padx=5, pady=5, sticky='w')
            self.source_entry = ctk.CTkEntry(
                self.dynamic_frame,
                placeholder_text='/tmp/vhost-blk.sock',
                width=300,
                font=CTK_FONT_SMALL,
            )
            self.source_entry.grid(row=row, column=1, padx=5, pady=5, sticky='ew')

        # vhostvdpa type
        elif disk_type == 'vhostvdpa':
            ctk.CTkLabel(
                self.dynamic_frame, text='Device:', font=CTK_FONT_MAIN, width=80, anchor='w'
            ).grid(row=row, column=0, padx=5, pady=5, sticky='w')
            self.source_entry = ctk.CTkEntry(
                self.dynamic_frame,
                placeholder_text='/dev/vhost-vdpa-0',
                width=200,
                font=CTK_FONT_SMALL,
            )
            self.source_entry.grid(row=row, column=1, padx=5, pady=5, sticky='w')

        # ctl type
        elif disk_type == 'ctl':
            ctk.CTkLabel(
                self.dynamic_frame, text='Device:', font=CTK_FONT_MAIN, width=80, anchor='w'
            ).grid(row=row, column=0, padx=5, pady=5, sticky='w')
            self.source_entry = ctk.CTkEntry(
                self.dynamic_frame, placeholder_text='/dev/cam/ctl', width=200, font=CTK_FONT_SMALL
            )
            self.source_entry.grid(row=row, column=1, padx=5, pady=5, sticky='w')

    def _on_type_changed(self, new_type):
        """类型改变."""
        self._init_dynamic_ui()

    def _on_protocol_changed(self, new_protocol):
        """协议改变."""
        # 根据协议设置默认端口
        default_ports = {
            'sheepdog': '7000',
            'rbd': '6789',
            'iscsi': '3260',
            'nfs': '2049',
            'http': '80',
            'https': '443',
            'ftp': '21',
            'ftps': '990',
            'tftp': '69',
        }
        if hasattr(self, 'port_entry'):
            self.port_entry.delete(0, 'end')
            self.port_entry.insert(0, default_ports.get(new_protocol, ''))

    def _confirm(self):
        """确认添加."""
        disk_type = self.type_menu.get()
        device_type = self.device_menu.get()

        config = {
            'type': disk_type,
            'device': device_type,
            'target_dev': self.target_entry.get().strip(),
            'bus': self.bus_menu.get(),
            'readonly': self.readonly_check.get(),
            'boot_order': self.boot_order_entry.get().strip() or None,
            'startup_policy': self.startup_menu.get(),
        }

        # 收集不同类型的配置
        if disk_type == 'file':
            config['source'] = self.source_entry.get().strip()
            config['driver'] = self.driver_menu.get()
        elif disk_type == 'block':
            config['source'] = self.source_entry.get().strip()
        elif disk_type == 'network':
            config['protocol'] = self.protocol_menu.get()
            config['source'] = self.source_entry.get().strip()
            config['host'] = self.host_entry.get().strip()
            config['port'] = self.port_entry.get().strip()
            if self.auth_check.get():
                config['username'] = self.username_entry.get().strip()
                config['secret'] = self.secret_entry.get().strip()
        elif disk_type == 'volume':
            config['pool'] = self.pool_entry.get().strip()
            config['volume'] = self.volume_entry.get().strip()
        elif disk_type == 'dir':
            config['source'] = self.source_entry.get().strip()
        elif disk_type == 'nvme':
            config['namespace'] = self.ns_entry.get().strip() or '1'
            config['pci'] = self.pci_entry.get().strip()
        elif disk_type == 'vhostuser':
            config['source'] = self.source_entry.get().strip()
        elif disk_type == 'vhostvdpa':
            config['source'] = self.source_entry.get().strip()
        elif disk_type == 'ctl':
            config['source'] = self.source_entry.get().strip()

        self.on_confirm_callback(config)
        self.dialog.destroy()