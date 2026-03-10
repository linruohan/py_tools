"""VmPanel - 虚拟机 XML 配置生成面板."""

import json
import uuid
import xml.etree.ElementTree as ET
from xml.dom import minidom
from tkinter import END, filedialog, messagebox

import customtkinter as ctk

# 全局样式常量
CTK_FONT_MAIN = ('Microsoft YaHei UI', 12)
CTK_FONT_BOLD = ('Microsoft YaHei UI', 12, 'bold')
CTK_FONT_MONO = ('Consolas', 11)
CTK_FONT_SMALL = ('Microsoft YaHei UI', 10)

BG_COLOR_MAIN = '#242424'
BG_COLOR_CONTENT = '#1e1e1e'
BG_COLOR_SELECT = '#404040'


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

    def get_disks(self):
        """获取所有磁盘配置."""
        disks = []
        for entry in self.disk_entries:
            name = entry['name'].get().strip()
            path = entry['path'].get().strip()
            if name and path:
                disks.append(
                    {
                        'name': name,
                        'path': path,
                        'type': entry['type'].get(),
                        'bus': entry['bus'].get(),
                    }
                )
        return disks


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
        name_entry = ctk.CTkEntry(
            frame, placeholder_text='网卡名称', width=100, font=CTK_FONT_SMALL
        )
        name_entry.grid(row=0, column=0, padx=5)

        # 网络模式
        network_mode = ctk.CTkOptionMenu(
            frame,
            values=['NAT', 'Bridge', 'Macvtap', 'Virtual Network'],
            width=130,
            font=CTK_FONT_SMALL,
        )
        network_mode.set('NAT')
        network_mode.grid(row=0, column=1, padx=5)

        # 网桥/网络名称
        bridge_entry = ctk.CTkEntry(
            frame, placeholder_text='网桥名称', width=120, font=CTK_FONT_SMALL
        )
        bridge_entry.grid(row=0, column=2, padx=5)

        # 模型类型
        model_type = ctk.CTkOptionMenu(
            frame, values=['virtio', 'e1000', 'rtl8139', 'vmxnet3'], width=80, font=CTK_FONT_SMALL
        )
        model_type.set('virtio')
        model_type.grid(row=0, column=3, padx=5)

        # MAC 地址
        mac_entry = ctk.CTkEntry(
            frame, placeholder_text='MAC 地址', width=140, font=CTK_FONT_SMALL
        )
        mac_entry.grid(row=0, column=4, padx=5)

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
        gen_mac_btn.grid(row=0, column=5, padx=5)

        # 删除按钮
        del_btn = ctk.CTkButton(
            frame,
            text='删除',
            width=50,
            fg_color='#f44336',
            hover_color='#d32f2f',
            font=CTK_FONT_SMALL,
            command=lambda: self.remove_network(frame),
        )
        del_btn.grid(row=0, column=6, padx=5)

        # 绑定变化事件
        for widget in [name_entry, bridge_entry, mac_entry]:
            widget.bind('<KeyRelease>', lambda e: self._trigger_change())
        for widget in [network_mode, model_type]:
            widget.configure(command=self._trigger_change)

        self.network_entries.append(
            {
                'frame': frame,
                'name': name_entry,
                'mode': network_mode,
                'bridge': bridge_entry,
                'model': model_type,
                'mac': mac_entry,
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
        mac = ':'.join(['{:02x}'.format(uuid.random().int % 256) for _ in range(6)])
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
                    }
                )
        return networks

    def _generate_mac(self):
        """生成随机 MAC 地址."""
        return ':'.join(['{:02x}'.format(uuid.random().int % 256) for _ in range(6)])


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


class VmPanel(ctk.CTkFrame):
    """虚拟机 XML 配置生成面板."""

    def __init__(self, parent: ctk.CTk) -> None:
        """初始化 VmPanel."""
        super().__init__(parent)
        self.corner_radius = 10
        self.fg_color = 'transparent'

        # 主布局：1 行 1 列
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.vm_data = {}
        self._updating_xml = False  # 防止递归更新

        # 初始化 UI
        self.init_ui()

    def init_ui(self) -> None:
        """初始化界面."""
        # 主框架
        main_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_MAIN, corner_radius=8)
        main_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # 配置内部网格
        main_frame.grid_rowconfigure(2, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # 顶部工具栏
        self._create_toolbar(main_frame)

        # Tab 配置区
        self.tabview = ctk.CTkTabview(
            main_frame,
            segmented_button_selected_color=('#3B8ED0', '#1F6AA5'),
            segmented_button_unselected_color=('#DCE4EE', '#2B2B2B'),
            text_color=('gray10', '#DCE4EE'),
        )
        self.tabview.grid(row=1, column=0, padx=15, pady=10, sticky='nsew')

        # 添加配置 Tab
        self.tab_basic = self.tabview.add('基础配置')
        self.tab_disk = self.tabview.add('磁盘配置')
        self.tab_network = self.tabview.add('网络配置')
        self.tab_advanced = self.tabview.add('高级配置')

        # 配置每个 Tab 的网格
        for tab_name in ['基础配置', '磁盘配置', '网络配置', '高级配置']:
            self.tabview.tab(tab_name).grid_columnconfigure(0, weight=1)
            self.tabview.tab(tab_name).grid_rowconfigure(0, weight=0)

        # 初始化各个 Tab
        self._init_basic_tab()
        self._init_disk_tab()
        self._init_network_tab()
        self._init_advanced_tab()

        # 底部 XML 预览区
        self._create_xml_preview(main_frame)

        # 底部信息栏
        self._create_info_bar(main_frame)

        # 绑定所有基础配置的变化事件，实现动态 XML 预览
        self._bind_basic_events()

        # 初始生成 XML
        self._update_xml_preview()

    def _create_toolbar(self, parent) -> None:
        """创建顶部工具栏."""
        toolbar = ctk.CTkFrame(parent, fg_color='transparent')
        toolbar.grid(row=0, column=0, padx=15, pady=10, sticky='ew')
        toolbar.grid_columnconfigure(0, weight=1)

        # 标题
        title_label = ctk.CTkLabel(
            toolbar,
            text='虚拟机 XML 配置生成器',
            font=CTK_FONT_BOLD,
            text_color='#64b5f6',
        )
        title_label.grid(row=0, column=0, sticky='w')

        # 按钮组
        btn_frame = ctk.CTkFrame(toolbar, fg_color='transparent')
        btn_frame.grid(row=0, column=1, sticky='e')

        # 清空按钮
        clear_btn = ctk.CTkButton(
            btn_frame,
            text='清空',
            command=self.clear_all,
            fg_color='#757575',
            hover_color='#616161',
            width=80,
            font=CTK_FONT_SMALL,
        )
        clear_btn.pack(side='left', padx=5)

        # 生成 XML 按钮
        generate_btn = ctk.CTkButton(
            btn_frame,
            text='生成 XML',
            command=self.generate_xml,
            fg_color='#2196f3',
            hover_color='#1976d2',
            width=100,
            font=CTK_FONT_SMALL,
        )
        generate_btn.pack(side='left', padx=5)

        # 保存按钮
        save_btn = ctk.CTkButton(
            btn_frame,
            text='保存 XML',
            command=self.save_xml,
            fg_color='#4caf50',
            hover_color='#388e3c',
            width=100,
            font=CTK_FONT_SMALL,
        )
        save_btn.pack(side='left', padx=5)

        # 创建虚拟机按钮
        create_btn = ctk.CTkButton(
            btn_frame,
            text='创建虚拟机',
            command=self.create_vm,
            fg_color='#9c27b0',
            hover_color='#7b1fa2',
            width=100,
            font=CTK_FONT_SMALL,
        )
        create_btn.pack(side='left', padx=5)

    def _init_basic_tab(self) -> None:
        """初始化基础配置 Tab."""
        tab = self.tabview.tab('基础配置')

        # 第一行：虚拟机名称和描述
        row1 = ctk.CTkFrame(tab, fg_color='transparent')
        row1.grid(row=0, column=0, sticky='ew', padx=10, pady=5)
        row1.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            row1, text='虚拟机名称:', font=CTK_FONT_MAIN, width=100, anchor='w'
        ).grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.vm_name_entry = ctk.CTkEntry(row1, placeholder_text='vm-name', width=200)
        self.vm_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        ctk.CTkLabel(
            row1, text='描述:', font=CTK_FONT_MAIN, width=60, anchor='w'
        ).grid(row=0, column=2, padx=5, pady=5, sticky='w')
        self.vm_desc_entry = ctk.CTkEntry(row1, placeholder_text='虚拟机描述', width=200)
        self.vm_desc_entry.grid(row=0, column=3, padx=5, pady=5, sticky='w')

        # 第二行：CPU 和内存
        row2 = ctk.CTkFrame(tab, fg_color='transparent')
        row2.grid(row=1, column=0, sticky='ew', padx=10, pady=5)
        row2.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(row1, text='vCPU:', font=CTK_FONT_MAIN, width=60, anchor='w').grid(
            row=1, column=0, padx=5, pady=5, sticky='w'
        )
        self.vcpu_entry = ctk.CTkEntry(row2, placeholder_text='2', width=100)
        self.vcpu_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        self.vcpu_entry.insert(0, '2')

        ctk.CTkLabel(
            row2, text='内存 (MB):', font=CTK_FONT_MAIN, width=80, anchor='w'
        ).grid(row=0, column=2, padx=5, pady=5, sticky='w')
        self.memory_entry = ctk.CTkEntry(row2, placeholder_text='2048', width=100)
        self.memory_entry.grid(row=0, column=3, padx=5, pady=5, sticky='w')
        self.memory_entry.insert(0, '2048')

        # 第三行：虚拟化类型和机器类型
        row3 = ctk.CTkFrame(tab, fg_color='transparent')
        row3.grid(row=2, column=0, sticky='ew', padx=10, pady=5)

        ctk.CTkLabel(row3, text='虚拟化:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=0, column=0, padx=5, pady=5, sticky='w'
        )
        self.virt_type = ctk.CTkOptionMenu(
            row3, values=['hvm', 'pv'], width=100, font=CTK_FONT_SMALL
        )
        self.virt_type.set('hvm')
        self.virt_type.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        ctk.CTkLabel(row3, text='机器类型:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=0, column=2, padx=5, pady=5, sticky='w'
        )
        self.machine_type = ctk.CTkEntry(row3, placeholder_text='q35', width=100)
        self.machine_type.grid(row=0, column=3, padx=5, pady=5, sticky='w')
        self.machine_type.insert(0, 'q35')

        ctk.CTkLabel(row3, text='固件:', font=CTK_FONT_MAIN, width=50, anchor='w').grid(
            row=0, column=4, padx=5, pady=5, sticky='w'
        )
        self.firmware_type = ctk.CTkOptionMenu(
            row3, values=['BIOS', 'UEFI'], width=80, font=CTK_FONT_SMALL
        )
        self.firmware_type.set('BIOS')
        self.firmware_type.grid(row=0, column=5, padx=5, pady=5, sticky='w')

        # 第四行：操作系统
        row4 = ctk.CTkFrame(tab, fg_color='transparent')
        row4.grid(row=3, column=0, sticky='ew', padx=10, pady=5)

        ctk.CTkLabel(row4, text='操作系统:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=0, column=0, padx=5, pady=5, sticky='w'
        )
        self.os_type = ctk.CTkOptionMenu(
            row4,
            values=['Linux', 'Windows', 'FreeBSD', 'Other'],
            width=120,
            font=CTK_FONT_SMALL,
        )
        self.os_type.set('Linux')
        self.os_type.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        ctk.CTkLabel(
            row4, text='引导设备:', font=CTK_FONT_MAIN, width=80, anchor='w'
        ).grid(row=0, column=2, padx=5, pady=5, sticky='w')
        self.boot_device = ctk.CTkOptionMenu(
            row4, values=['hd', 'cdrom', 'network'], width=100, font=CTK_FONT_SMALL
        )
        self.boot_device.set('hd')
        self.boot_device.grid(row=0, column=3, padx=5, pady=5, sticky='w')

    def _init_disk_tab(self) -> None:
        """初始化磁盘配置 Tab."""
        tab = self.tabview.tab('磁盘配置')

        # 工具栏
        toolbar = ctk.CTkFrame(tab, fg_color='transparent')
        toolbar.grid(row=0, column=0, sticky='ew', padx=10, pady=5)

        add_disk_btn = ctk.CTkButton(
            toolbar,
            text='添加磁盘',
            command=lambda: (self.add_disk(), self._update_xml_preview()),
            fg_color='#4caf50',
            hover_color='#388e3c',
            width=100,
        )
        add_disk_btn.pack(side='left', padx=5)

        # 磁盘列表
        self.disk_frame = ScrollableDiskFrame(
            tab, corner_radius=0, fg_color=BG_COLOR_CONTENT, on_change_callback=self._update_xml_preview
        )
        self.disk_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=5)
        tab.grid_rowconfigure(1, weight=1)

        # 默认添加一个磁盘
        self.add_disk()

    def _init_network_tab(self) -> None:
        """初始化网络配置 Tab."""
        tab = self.tabview.tab('网络配置')

        # 工具栏
        toolbar = ctk.CTkFrame(tab, fg_color='transparent')
        toolbar.grid(row=0, column=0, sticky='ew', padx=10, pady=5)

        add_net_btn = ctk.CTkButton(
            toolbar,
            text='添加网卡',
            command=lambda: (self.add_network(), self._update_xml_preview()),
            fg_color='#4caf50',
            hover_color='#388e3c',
            width=100,
        )
        add_net_btn.pack(side='left', padx=5)

        # 网络列表
        self.network_frame = ScrollableNetworkFrame(
            tab, corner_radius=0, fg_color=BG_COLOR_CONTENT, on_change_callback=self._update_xml_preview
        )
        self.network_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=5)
        tab.grid_rowconfigure(1, weight=1)

        # 默认添加一个网卡
        self.add_network()

    def _init_advanced_tab(self) -> None:
        """初始化高级配置 Tab."""
        tab = self.tabview.tab('高级配置')

        # GPU/PCI 直通
        gpu_label = ctk.CTkLabel(
            tab,
            text='GPU / PCI 直通设备',
            font=CTK_FONT_BOLD,
            text_color='#81c784',
            anchor='w',
        )
        gpu_label.grid(row=0, column=0, sticky='ew', padx=10, pady=5)

        # 添加工具栏
        gpu_toolbar = ctk.CTkFrame(tab, fg_color='transparent')
        gpu_toolbar.grid(row=1, column=0, sticky='ew', padx=10, pady=5)

        add_gpu_btn = ctk.CTkButton(
            gpu_toolbar,
            text='添加 PCI 设备',
            command=self.add_hostdev,
            fg_color='#ff9800',
            hover_color='#f57c00',
            width=120,
        )
        add_gpu_btn.pack(side='left', padx=5)

        # PCI 设备列表
        self.hostdev_frame = ScrollableHostdevFrame(
            tab, corner_radius=0, fg_color=BG_COLOR_CONTENT, height=150, on_change_callback=self._update_xml_preview
        )
        self.hostdev_frame.grid(row=2, column=0, sticky='ew', padx=10, pady=5)

        # USB 设备
        usb_label = ctk.CTkLabel(
            tab,
            text='USB 设备 (Vendor:Product)',
            font=CTK_FONT_BOLD,
            text_color='#64b5f6',
            anchor='w',
        )
        usb_label.grid(row=3, column=0, sticky='ew', padx=10, pady=(15, 5))

        usb_frame = ctk.CTkFrame(tab, fg_color='transparent')
        usb_frame.grid(row=4, column=0, sticky='ew', padx=10, pady=5)

        self.usb_entry = ctk.CTkEntry(
            usb_frame, placeholder_text='例如：8087:8008', width=200
        )
        self.usb_entry.grid(row=0, column=0, padx=5, sticky='w')
        self.usb_entry.bind('<KeyRelease>', lambda e: self._update_xml_preview())

        add_usb_btn = ctk.CTkButton(
            usb_frame,
            text='添加 USB',
            command=lambda: (self.add_usb(), self._update_xml_preview()),
            fg_color='#00bcd4',
            hover_color='#0097a7',
            width=100,
        )
        add_usb_btn.grid(row=0, column=1, padx=5)

        self.usb_list = []
        self.usb_display = ctk.CTkLabel(
            tab, text='', font=CTK_FONT_SMALL, text_color='#aaaaaa', anchor='w'
        )
        self.usb_display.grid(row=5, column=0, sticky='ew', padx=10, pady=5)

        # 其他选项
        other_label = ctk.CTkLabel(
            tab, text='其他选项', font=CTK_FONT_BOLD, text_color='#ba68c8', anchor='w'
        )
        other_label.grid(row=6, column=0, sticky='ew', padx=10, pady=(15, 5))

        other_frame = ctk.CTkFrame(tab, fg_color='transparent')
        other_frame.grid(row=7, column=0, sticky='ew', padx=10, pady=5)

        # 启用 ACPI
        self.acpi_check = ctk.CTkCheckBox(other_frame, text='启用 ACPI', font=CTK_FONT_SMALL, command=self._update_xml_preview)
        self.acpi_check.grid(row=0, column=0, padx=10)
        self.acpi_check.select()

        # 启用 APIC
        self.apic_check = ctk.CTkCheckBox(other_frame, text='启用 APIC', font=CTK_FONT_SMALL, command=self._update_xml_preview)
        self.apic_check.grid(row=0, column=1, padx=10)
        self.apic_check.select()

        # 启用 Hyper-V
        self.hyperv_check = ctk.CTkCheckBox(
            other_frame, text='启用 Hyper-V', font=CTK_FONT_SMALL, command=self._update_xml_preview
        )
        self.hyperv_check.grid(row=0, column=2, padx=10)

        # 启用 IOMMU
        self.iommu_check = ctk.CTkCheckBox(
            other_frame, text='启用 IOMMU', font=CTK_FONT_SMALL, command=self._update_xml_preview
        )
        self.iommu_check.grid(row=0, column=3, padx=10)

    def _create_xml_preview(self, parent) -> None:
        """创建 XML 预览区."""
        preview_frame = ctk.CTkFrame(parent, fg_color=BG_COLOR_CONTENT, corner_radius=8)
        preview_frame.grid(row=2, column=0, padx=15, pady=(0, 10), sticky='nsew')
        parent.grid_rowconfigure(2, weight=1)

        # 预览区标题
        preview_label = ctk.CTkLabel(
            preview_frame,
            text='XML 预览',
            font=CTK_FONT_BOLD,
            text_color='#ffb74d',
        )
        preview_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')

        # XML 文本框
        self.xml_textbox = ctk.CTkTextbox(
            preview_frame,
            font=CTK_FONT_MONO,
            fg_color=BG_COLOR_CONTENT,
            text_color='#f0f0f0',
            border_color='#333333',
            border_width=1,
            corner_radius=6,
        )
        self.xml_textbox.grid(row=1, column=0, padx=10, pady=(0, 10), sticky='nsew')
        preview_frame.grid_rowconfigure(1, weight=1)
        preview_frame.grid_columnconfigure(0, weight=1)

    def _create_info_bar(self, parent) -> None:
        """创建底部信息栏."""
        self.info_frame = ctk.CTkFrame(
            parent, fg_color=BG_COLOR_CONTENT, corner_radius=0, height=30
        )
        self.info_frame.grid(row=3, column=0, sticky='ew')
        self.info_frame.grid_propagate(False)

        self.info_label = ctk.CTkLabel(
            self.info_frame,
            text='就绪',
            font=CTK_FONT_SMALL,
            text_color='#aaaaaa',
            anchor='w',
        )
        self.info_label.pack(fill='x', padx=20, pady=5)

    def update_info(self, text: str, is_success: bool = True) -> None:
        """更新底部信息栏."""
        color = '#4caf50' if is_success else '#f44336'
        self.info_label.configure(text=text, text_color=color)

    def _bind_basic_events(self) -> None:
        """绑定基础配置的变化事件，实现动态 XML 预览."""
        # 绑定 Entry 的 KeyRelease 事件
        for widget in [self.vm_name_entry, self.vm_desc_entry, self.vcpu_entry,
                       self.memory_entry, self.machine_type]:
            widget.bind('<KeyRelease>', lambda e: self._update_xml_preview())

        # 绑定 OptionMenu 的变化事件
        for widget in [self.virt_type, self.firmware_type, self.os_type, self.boot_device]:
            widget.configure(command=self._update_xml_preview)

    def _update_xml_preview(self) -> None:
        """更新 XML 预览（不显示错误消息）."""
        if self._updating_xml:
            return
        self._updating_xml = True
        try:
            xml_str = self._build_xml_preview()
            self.xml_textbox.delete('1.0', END)
            self.xml_textbox.insert('1.0', xml_str)
        except Exception:
            # 配置不完整时显示空或部分内容
            pass
        finally:
            self._updating_xml = False

    def _build_xml_preview(self) -> str:
        """构建 XML 预览（不抛出错误）."""
        try:
            data = self.collect_vm_data()
            return self._build_libvirt_xml(data)
        except Exception:
            return '<!-- 配置不完整或无效，请检查输入 -->'

    # ========== 磁盘配置方法 ==========
    def add_disk(self) -> None:
        """添加磁盘配置行."""
        self.disk_frame.add_disk()

    # ========== 网络配置方法 ==========
    def add_network(self) -> None:
        """添加网络配置行."""
        self.network_frame.add_network()

    # ========== 高级配置方法 ==========
    def add_hostdev(self) -> None:
        """添加 PCI 直通设备."""
        self.hostdev_frame.add_hostdev()

    def add_usb(self) -> None:
        """添加 USB 设备."""
        usb_id = self.usb_entry.get().strip()
        if not usb_id or ':' not in usb_id:
            messagebox.showwarning('警告', '请输入有效的 USB 设备 ID (格式：Vendor:Product)!')
            return
        self.usb_list.append(usb_id)
        self.usb_display.configure(text=f'已添加 USB: {", ".join(self.usb_list)}')
        self.usb_entry.delete(0, END)
        self.update_info(f'已添加 USB 设备：{usb_id}')

    # ========== 核心功能方法 ==========
    def clear_all(self) -> None:
        """清空所有配置."""
        if messagebox.askyesno('确认', '确定要清空所有配置吗？'):
            # 清空基础配置
            self.vm_name_entry.delete(0, END)
            self.vm_desc_entry.delete(0, END)
            self.vcpu_entry.delete(0, END)
            self.vcpu_entry.insert(0, '2')
            self.memory_entry.delete(0, END)
            self.memory_entry.insert(0, '2048')
            self.machine_type.delete(0, END)
            self.machine_type.insert(0, 'q35')

            # 清空磁盘
            for entry in self.disk_frame.disk_entries[:]:
                self.disk_frame.remove_disk(entry['frame'])

            # 清空网络
            for entry in self.network_frame.network_entries[:]:
                self.network_frame.remove_network(entry['frame'])

            # 清空 PCI 设备
            for entry in self.hostdev_frame.hostdev_entries[:]:
                self.hostdev_frame.remove_hostdev(entry['frame'])

            # 清空 USB
            self.usb_list.clear()
            self.usb_display.configure(text='')
            self.usb_entry.delete(0, END)

            # 清空 XML 预览
            self.xml_textbox.delete('1.0', END)

            self.update_info('已清空所有配置')

    def collect_vm_data(self) -> dict:
        """收集虚拟机配置数据."""
        vm_name = self.vm_name_entry.get().strip()
        if not vm_name:
            raise ValueError('虚拟机名称不能为空!')

        return {
            'name': vm_name,
            'description': self.vm_desc_entry.get().strip(),
            'vcpu': int(self.vcpu_entry.get().strip() or '2'),
            'memory': int(self.memory_entry.get().strip() or '2048'),
            'virt_type': self.virt_type.get(),
            'machine': self.machine_type.get().strip() or 'q35',
            'firmware': self.firmware_type.get(),
            'os_type': self.os_type.get(),
            'boot_device': self.boot_device.get(),
            'disks': self.disk_frame.get_disks(),
            'networks': self.network_frame.get_networks(),
            'hostdevs': self.hostdev_frame.get_hostdevs(),
            'usb_devices': self.usb_list.copy(),
            'features': {
                'acpi': self.acpi_check.get(),
                'apic': self.apic_check.get(),
                'hyperv': self.hyperv_check.get(),
                'iommu': self.iommu_check.get(),
            },
        }

    def generate_xml(self) -> None:
        """生成 XML 配置."""
        try:
            self.vm_data = self.collect_vm_data()
            xml_str = self._build_libvirt_xml(self.vm_data)
            self.xml_textbox.delete('1.0', END)
            self.xml_textbox.insert('1.0', xml_str)
            self.update_info('XML 生成成功')
        except ValueError as e:
            messagebox.showerror('错误', str(e))
            self.update_info(str(e), False)
        except Exception as e:
            messagebox.showerror('错误', f'生成失败：{e!s}')
            self.update_info(f'生成失败：{e!s}', False)

    def _build_libvirt_xml(self, data: dict) -> str:
        """构建 libvirt domain XML."""
        # 根元素
        domain = ET.Element('domain', type='kvm')

        # 名称
        name = ET.SubElement(domain, 'name')
        name.text = data['name']

        # 描述
        if data['description']:
            desc = ET.SubElement(domain, 'description')
            desc.text = data['description']

        # 内存 (KB)
        memory = ET.SubElement(domain, 'memory', unit='KiB')
        memory.text = str(data['memory'] * 1024)

        # 当前内存
        current_memory = ET.SubElement(domain, 'currentMemory', unit='KiB')
        current_memory.text = str(data['memory'] * 1024)

        # vCPU
        vcpu = ET.SubElement(domain, 'vcpu')
        vcpu.text = str(data['vcpu'])

        # 操作系统
        os_elem = ET.SubElement(domain, 'os')
        os_type = ET.SubElement(os_elem, 'type', arch='x86_64', machine=data['machine'])
        if data['virt_type'] == 'hvm':
            os_type.text = 'hvm'
        else:
            os_type.text = 'linux'

        # 引导设备
        boot = ET.SubElement(os_elem, 'boot', dev=data['boot_device'])

        # UEFI 固件
        if data['firmware'] == 'UEFI':
            loader = ET.SubElement(
                os_elem, 'loader', readonly='yes', type='pflash'
            )
            loader.text = '/usr/share/OVMF/OVMF_CODE.fd'
            nvram = ET.SubElement(os_elem, 'nvram')
            nvram.text = f'/var/lib/libvirt/qemu/nvram/{data["name"]}._VARS.fd'

        # 功能特性
        features = ET.SubElement(domain, 'features')
        if data['features']['acpi']:
            ET.SubElement(features, 'acpi')
        if data['features']['apic']:
            ET.SubElement(features, 'apic')
        if data['features']['hyperv']:
            hyperv = ET.SubElement(features, 'hyperv')
            ET.SubElement(hyperv, 'vpindex', mode='native')
            ET.SubElement(hyperv, 'synic', mode='native')

        # IOMMU
        if data['features']['iommu']:
            iommu = ET.SubElement(domain, 'iommu', type='intel')

        # 时钟
        clock = ET.SubElement(domain, 'clock', offset='utc')
        ET.SubElement(clock, 'timer', name='rtc', tickpolicy='catchup')
        ET.SubElement(clock, 'timer', name='pit', tickpolicy='delay')
        ET.SubElement(clock, 'timer', name='hpet', present='no')

        # 设备
        devices = ET.SubElement(domain, 'devices')

        # 磁盘
        for i, disk in enumerate(data['disks']):
            disk_elem = ET.SubElement(
                devices, 'disk', type='file', device='disk'
            )
            driver = ET.SubElement(
                disk_elem, 'driver', name='qemu', type=disk['type'], cache='none'
            )
            source = ET.SubElement(
                disk_elem, 'source', file=disk['path']
            )
            target = ET.SubElement(
                disk_elem, 'target', dev=f'vd{chr(ord("a") + i)}', bus=disk['bus']
            )

        # 网络
        for i, network in enumerate(data['networks']):
            interface = ET.SubElement(
                devices, 'interface', type='network' if network['mode'] == 'NAT' else 'bridge'
            )
            if network['mac']:
                ET.SubElement(interface, 'mac', address=network['mac'])
            if network['mode'] == 'NAT':
                ET.SubElement(interface, 'source', network='default')
            else:
                ET.SubElement(interface, 'source', bridge=network['bridge'] or 'br0')
            ET.SubElement(interface, 'model', type=network['model'])

        # 控制台
        console = ET.SubElement(devices, 'console', type='pty')
        ET.SubElement(console, 'target', type='serial', port='0')

        # 输入设备
        ET.SubElement(devices, 'input', type='tablet', bus='usb')
        ET.SubElement(devices, 'input', type='mouse', bus='ps2')

        # 图形 (VNC)
        graphics = ET.SubElement(
            devices, 'graphics', type='vnc', port='-1', autoport='yes', listen='0.0.0.0'
        )
        listen = ET.SubElement(graphics, 'listen', type='address')

        # 视频
        video = ET.SubElement(devices, 'video')
        ET.SubElement(video, 'model', type='qxl', ram='65536', vram='65536', vgamem='16384')

        # PCI 直通设备
        for hostdev in data['hostdevs']:
            hd = ET.SubElement(
                devices, 'hostdev', mode='subsystem', type='pci', managed='yes'
            )
            source = ET.SubElement(hd, 'source')
            # 解析 PCI 地址
            try:
                parts = hostdev['pci'].replace(',', ':').split(':')
                if len(parts) >= 4:
                    addr = parts[3].split('.')
                    ET.SubElement(
                        source, 'address',
                        domain=parts[0],
                        bus=parts[1],
                        slot=parts[2],
                        function=addr[1] if len(addr) > 1 else '0',
                    )
            except (IndexError, ValueError):
                pass

        # USB 设备
        for usb in data['usb_devices']:
            if ':' in usb:
                vendor, product = usb.split(':')
                usb_elem = ET.SubElement(
                    devices, 'hostdev', mode='subsystem', type='usb', managed='yes'
                )
                source = ET.SubElement(usb_elem, 'source')
                ET.SubElement(source, 'vendor', id=f'0x{vendor}')
                ET.SubElement(source, 'product', id=f'0x{product}')

        # 生成格式化的 XML
        xml_str = ET.tostring(domain, encoding='unicode')
        parsed = minidom.parseString(xml_str)
        return parsed.toprettyxml(indent='  ')

    def save_xml(self) -> None:
        """保存 XML 到文件."""
        xml_content = self.xml_textbox.get('1.0', END).strip()
        if not xml_content:
            messagebox.showwarning('警告', '请先生成 XML!')
            self.update_info('请先生成 XML', False)
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension='.xml',
            filetypes=[('XML 文件', '*.xml'), ('所有文件', '*.*')],
            title='保存 XML 文件',
            initialfile=f'{self.vm_data.get("name", "vm")}.xml',
        )

        if not file_path:
            self.update_info('已取消保存', False)
            return

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(xml_content)
            messagebox.showinfo('成功', f'XML 已保存到:\n{file_path}')
            self.update_info(f'保存成功：{file_path}')
        except Exception as e:
            messagebox.showerror('错误', f'保存失败：{e!s}')
            self.update_info(f'保存失败：{e!s}', False)

    def create_vm(self) -> None:
        """通过 virsh 创建虚拟机."""
        xml_content = self.xml_textbox.get('1.0', END).strip()
        if not xml_content:
            messagebox.showwarning('警告', '请先生成 XML!')
            self.update_info('请先生成 XML', False)
            return

        # 检查 virsh 是否可用
        import subprocess

        try:
            # 尝试定义虚拟机
            result = subprocess.run(
                ['virsh', 'define', '--file', '-'],
                input=xml_content,
                capture_output=True,
                text=True,
                check=False,
            )

            if result.returncode == 0:
                vm_name = self.vm_data.get('name', 'vm')
                messagebox.showinfo(
                    '成功', f'虚拟机 {vm_name} 定义成功!\n\n请运行以下命令启动:\n  virsh start {vm_name}'
                )
                self.update_info(f'虚拟机 {vm_name} 定义成功')
            else:
                error_msg = result.stderr.strip()
                messagebox.showerror('错误', f'定义虚拟机失败:\n{error_msg}')
                self.update_info(f'定义失败：{error_msg}', False)

        except FileNotFoundError:
            messagebox.showerror(
                '错误',
                '未找到 virsh 命令!\n请确保已安装 libvirt-client 并以管理员/root 身份运行。',
            )
            self.update_info('未找到 virsh 命令', False)
        except Exception as e:
            messagebox.showerror('错误', f'创建失败：{e!s}')
            self.update_info(f'创建失败：{e!s}', False)
