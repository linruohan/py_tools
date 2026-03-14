"""网络配置框架."""

import uuid

from tkinter import END

import customtkinter as ctk

from utils.styles import CTK_FONT_SMALL


class ScrollableNetworkFrame(ctk.CTkScrollableFrame):
    """可滚动网络配置框架."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.network_entries = []
        self.network_count = 0
        self.on_change_callback = on_change_callback

    def add_network(self):
        """添加网络配置行."""
        frame = ctk.CTkFrame(self, fg_color='transparent')
        frame.grid(row=self.network_count, column=0, sticky='ew', pady=5)

        # 网卡名称
        name_entry = ctk.CTkEntry(frame, placeholder_text='网卡名称', width=80, font=CTK_FONT_SMALL)
        name_entry.grid(row=0, column=0, padx=2)
        name_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        # 网络模式
        network_mode = ctk.CTkOptionMenu(
            frame,
            values=['NAT', 'Bridge', 'Macvtap', 'Virtual Network', 'Direct Attachment', 'User'],
            width=130,
            font=CTK_FONT_SMALL,
        )
        network_mode.set('NAT')
        network_mode.grid(row=0, column=1, padx=2)
        network_mode.configure(command=self._trigger_change)

        # 网桥/网络名称
        bridge_entry = ctk.CTkEntry(
            frame, placeholder_text='网桥名称', width=100, font=CTK_FONT_SMALL
        )
        bridge_entry.grid(row=0, column=2, padx=2)
        bridge_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        # 模型类型
        model_type = ctk.CTkOptionMenu(
            frame,
            values=[
                'virtio',
                'virtio-transitional',
                'virtio-non-transitional',
                'e1000',
                'rtl8139',
                'vmxnet3',
                'ne2k_pci',
            ],
            width=180,
            font=CTK_FONT_SMALL,
        )
        model_type.set('virtio')
        model_type.grid(row=0, column=3, padx=2)
        model_type.configure(command=self._trigger_change)

        # MAC 地址
        mac_entry = ctk.CTkEntry(frame, placeholder_text='MAC 地址', width=130, font=CTK_FONT_SMALL)
        mac_entry.grid(row=0, column=4, padx=2)
        mac_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        # 生成随机 MAC 按钮
        gen_mac_btn = ctk.CTkButton(
            frame,
            text='生成',
            width=50,
            fg_color='#2196f3',
            hover_color='#1976d2',
            font=CTK_FONT_SMALL,
            command=lambda: self.generate_mac(mac_entry),
        )
        gen_mac_btn.grid(row=0, column=5, padx=2)

        # vhost 多队列
        vhost_check = ctk.CTkCheckBox(frame, text='vhost', width=50, font=CTK_FONT_SMALL)
        vhost_check.grid(row=0, column=6, padx=2)
        vhost_check.configure(command=self._trigger_change)

        # 多队列数
        queues_entry = ctk.CTkEntry(frame, placeholder_text='队列数', width=50, font=CTK_FONT_SMALL)
        queues_entry.grid(row=0, column=7, padx=2)
        queues_entry.insert(0, '1')
        queues_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        # VLAN ID
        vlan_entry = ctk.CTkEntry(frame, placeholder_text='VLAN', width=50, font=CTK_FONT_SMALL)
        vlan_entry.grid(row=0, column=8, padx=2)
        vlan_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        # 链路状态
        link_check = ctk.CTkCheckBox(frame, text='Link Down', width=70, font=CTK_FONT_SMALL)
        link_check.grid(row=0, column=9, padx=2)
        link_check.configure(command=self._trigger_change)

        # 删除按钮
        del_btn = ctk.CTkButton(
            frame,
            text='X',
            width=25,
            fg_color='#f44336',
            hover_color='#d32f2f',
            font=CTK_FONT_SMALL,
            command=lambda: self.remove_network(frame),
        )
        del_btn.grid(row=0, column=10, padx=2)

        self.network_entries.append(
            {
                'frame': frame,
                'name': name_entry,
                'mode': network_mode,
                'bridge': bridge_entry,
                'model': model_type,
                'mac': mac_entry,
                'vhost': vhost_check,
                'queues': queues_entry,
                'vlan': vlan_entry,
                'link_down': link_check,
            }
        )
        self.network_count += 1

    def _trigger_change(self):
        """触发变化回调."""
        if self.on_change_callback:
            self.on_change_callback()

    def remove_network(self, frame):
        """删除网络配置行."""
        for i, entry in enumerate(self.network_entries):
            if entry['frame'] == frame:
                frame.destroy()
                self.network_entries.pop(i)
                self.network_count -= 1
                # 重新布局
                for j, e in enumerate(self.network_entries):
                    e['frame'].grid(row=j, column=0, sticky='ew', pady=5)
                break

    def generate_mac(self, mac_entry: ctk.CTkEntry):
        """生成随机 MAC 地址."""
        mac = ':'.join([f'{uuid.random().int % 256:02x}' for _ in range(6)])
        mac_entry.delete(0, END)
        mac_entry.insert(0, mac)

    def get_networks(self):
        """获取所有网络配置."""
        networks = []
        for entry in self.network_entries:
            name = entry['name'].get().strip()
            bridge = entry['bridge'].get().strip()
            mac = entry['mac'].get().strip()
            if name or bridge or mac:
                networks.append(
                    {
                        'name': name or f'nic{len(networks)}',
                        'mode': entry['mode'].get(),
                        'bridge': bridge,
                        'model': entry['model'].get(),
                        'mac': mac if mac else self._generate_mac(),
                        'vhost': entry['vhost'].get(),
                        'queues': int(entry['queues'].get().strip() or '1'),
                        'vlan': entry['vlan'].get().strip() or None,
                        'link_down': entry['link_down'].get(),
                    }
                )
        return networks

    def _generate_mac(self):
        """生成随机 MAC 地址."""
        return ':'.join([f'{uuid.random().int % 256:02x}' for _ in range(6)])
