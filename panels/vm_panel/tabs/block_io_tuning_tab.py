"""块 I/O 优化配置 Tab - Block I/O Tuning."""

import customtkinter as ctk

from components.base_tab import BaseConfigTab
from utils.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class BlockIOTuningTab(BaseConfigTab):
    """块 I/O 优化配置 Tab."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        self._devices = []
        super().__init__(master, on_change_callback, **kwargs)

    def _init_ui(self) -> None:
        """初始化界面."""
        self._devices = []

        # 主容器
        main_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        main_frame.pack(fill='both', expand=True, padx=5, pady=5)

        # 全局权重 - 单行
        weight_row = ctk.CTkFrame(main_frame, fg_color='transparent')
        weight_row.pack(fill='x', padx=10, pady=5)
        ctk.CTkLabel(weight_row, text='全局权重:', font=CTK_FONT_BOLD, width=80, anchor='w').pack(
            side='left'
        )
        self.weight_var = ctk.StringVar(value='None')
        self.weight_menu = ctk.CTkOptionMenu(
            weight_row,
            variable=self.weight_var,
            values=['None', '100', '200', '300', '400', '500', '600', '700', '800', '900', '1000'],
            width=80,
            command=self._trigger_change,
        )
        self.weight_menu.pack(side='left', padx=5)
        ctk.CTkLabel(
            weight_row,
            text='(100-1000，None 表示不生成)',
            font=CTK_FONT_SMALL,
            text_color='#888888',
        ).pack(side='left', padx=5)

        # 分隔线
        ctk.CTkFrame(main_frame, height=1, fg_color='#444444').pack(fill='x', padx=10, pady=5)

        # 设备标题行
        header_row = ctk.CTkFrame(main_frame, fg_color='transparent')
        header_row.pack(fill='x', padx=10, pady=5)
        ctk.CTkLabel(
            header_row, text='设备 I/O 限制', font=CTK_FONT_BOLD, text_color='#4caf50'
        ).pack(side='left')
        ctk.CTkButton(
            header_row,
            text='+ 添加设备',
            command=self._add_device_entry,
            fg_color='#4caf50',
            hover_color='#388e3c',
            width=100,
            height=24,
            font=CTK_FONT_SMALL,
        ).pack(side='right')

        # 设备列表容器
        self.devices_container = ctk.CTkScrollableFrame(main_frame, fg_color='transparent')
        self.devices_container.pack(fill='both', expand=True, padx=10, pady=5)

        # 说明信息
        info_text = '路径：主机块设备的绝对路径 (如/dev/sda) | 权重：100-1000 | 吞吐量：字节/秒 | IOPS: 次/秒 | None 或留空不生成 XML'
        ctk.CTkLabel(
            main_frame,
            text=info_text,
            font=CTK_FONT_SMALL,
            text_color='#888888',
            justify='left',
        ).pack(anchor='w', padx=10, pady=(5, 10))

        # 添加一个默认设备条目
        self._add_device_entry()

    def _create_device_entry(self) -> ctk.CTkFrame:
        """创建设备条目框架 - 单行布局."""
        frame = ctk.CTkFrame(self.devices_container, fg_color=BG_COLOR_CONTENT, corner_radius=4)
        frame.pack(fill='x', pady=2)

        # 设备标签
        ctk.CTkLabel(frame, text='设备:', font=CTK_FONT_BOLD, width=40, anchor='w').pack(
            side='left', padx=5
        )

        # 路径
        ctk.CTkLabel(frame, text='路径:', font=CTK_FONT_MAIN, width=35, anchor='w').pack(
            side='left'
        )
        path_entry = ctk.CTkEntry(frame, placeholder_text='/dev/sda', width=150)
        path_entry.pack(side='left', padx=2)
        path_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        # 权重
        ctk.CTkLabel(frame, text='权重:', font=CTK_FONT_MAIN, width=40, anchor='w').pack(
            side='left', padx=(5, 0)
        )
        weight_var = ctk.StringVar(value='None')
        weight_menu = ctk.CTkOptionMenu(
            frame,
            variable=weight_var,
            values=['None', '100', '200', '300', '400', '500', '600', '700', '800', '900', '1000'],
            width=70,
            command=self._trigger_change,
        )
        weight_menu.pack(side='left', padx=2)

        # 读吞吐量
        ctk.CTkLabel(frame, text='读 (B/s):', font=CTK_FONT_MAIN, width=55, anchor='w').pack(
            side='left', padx=(5, 0)
        )
        read_bytes = ctk.CTkEntry(frame, placeholder_text='', width=100)
        read_bytes.pack(side='left', padx=2)
        read_bytes.bind('<KeyRelease>', lambda e: self._trigger_change())

        # 写吞吐量
        ctk.CTkLabel(frame, text='写 (B/s):', font=CTK_FONT_MAIN, width=55, anchor='w').pack(
            side='left', padx=(5, 0)
        )
        write_bytes = ctk.CTkEntry(frame, placeholder_text='', width=100)
        write_bytes.pack(side='left', padx=2)
        write_bytes.bind('<KeyRelease>', lambda e: self._trigger_change())

        # 读 IOPS
        ctk.CTkLabel(frame, text='读 IOPS:', font=CTK_FONT_MAIN, width=50, anchor='w').pack(
            side='left', padx=(5, 0)
        )
        read_iops = ctk.CTkEntry(frame, placeholder_text='', width=80)
        read_iops.pack(side='left', padx=2)
        read_iops.bind('<KeyRelease>', lambda e: self._trigger_change())

        # 写 IOPS
        ctk.CTkLabel(frame, text='写 IOPS:', font=CTK_FONT_MAIN, width=50, anchor='w').pack(
            side='left', padx=(5, 0)
        )
        write_iops = ctk.CTkEntry(frame, placeholder_text='', width=80)
        write_iops.pack(side='left', padx=2)
        write_iops.bind('<KeyRelease>', lambda e: self._trigger_change())

        # 删除按钮
        del_btn = ctk.CTkButton(
            frame,
            text='删除',
            command=lambda f=frame: self._remove_device_entry(f),
            fg_color='#f44336',
            hover_color='#d32f2f',
            width=50,
            height=22,
            font=CTK_FONT_SMALL,
        )
        del_btn.pack(side='left', padx=5)

        # 存储控件引用
        frame._widgets = {
            'path': path_entry,
            'weight_var': weight_var,
            'weight_menu': weight_menu,
            'read_bytes': read_bytes,
            'write_bytes': write_bytes,
            'read_iops': read_iops,
            'write_iops': write_iops,
        }

        return frame

    def _add_device_entry(self) -> None:
        """添加设备条目."""
        device_frame = self._create_device_entry()
        self._devices.append(device_frame)
        self._trigger_change()

    def _remove_device_entry(self, frame: ctk.CTkFrame) -> None:
        """删除设备条目."""
        if frame in self._devices:
            self._devices.remove(frame)
            frame.destroy()
            self._trigger_change()

    def get_config(self) -> dict:
        """获取配置数据."""
        config = {}

        # 全局权重
        weight_val = self.weight_var.get()
        if weight_val != 'None':
            config['weight'] = int(weight_val)

        # 设备配置
        devices = []
        for device_frame in self._devices:
            widgets = device_frame._widgets
            path = widgets['path'].get().strip()

            # 只有路径不为空才添加设备
            if path:
                device_config = {'path': path}

                weight_val = widgets['weight_var'].get()
                if weight_val != 'None':
                    device_config['weight'] = int(weight_val)

                read_bytes = widgets['read_bytes'].get().strip()
                if read_bytes:
                    device_config['read_bytes_sec'] = int(read_bytes)

                write_bytes = widgets['write_bytes'].get().strip()
                if write_bytes:
                    device_config['write_bytes_sec'] = int(write_bytes)

                read_iops = widgets['read_iops'].get().strip()
                if read_iops:
                    device_config['read_iops_sec'] = int(read_iops)

                write_iops = widgets['write_iops'].get().strip()
                if write_iops:
                    device_config['write_iops_sec'] = int(write_iops)

                devices.append(device_config)

        if devices:
            config['devices'] = devices

        return config

    def to_xml(self) -> dict:
        """生成 XML 配置字典."""
        return {'block_io_tuning': self.get_config()}

    def load_config(self, config: dict) -> None:
        """加载配置数据."""
        # 清空现有设备
        for device_frame in self._devices:
            device_frame.destroy()
        self._devices = []

        if not config:
            self.weight_var.set('None')
            self._add_device_entry()
            return

        # 设置全局权重
        weight = config.get('weight')
        if weight:
            self.weight_var.set(str(weight))
        else:
            self.weight_var.set('None')

        # 加载设备配置
        devices = config.get('devices', [])
        if devices:
            for device_data in devices:
                device_frame = self._create_device_entry()
                self._devices.append(device_frame)

                widgets = device_frame._widgets
                widgets['path'].insert(0, device_data.get('path', ''))

                weight_val = device_data.get('weight')
                if weight_val:
                    widgets['weight_menu'].set(str(weight_val))

                read_bytes = device_data.get('read_bytes_sec')
                if read_bytes:
                    widgets['read_bytes'].insert(0, str(read_bytes))

                write_bytes = device_data.get('write_bytes_sec')
                if write_bytes:
                    widgets['write_bytes'].insert(0, str(write_bytes))

                read_iops = device_data.get('read_iops_sec')
                if read_iops:
                    widgets['read_iops'].insert(0, str(read_iops))

                write_iops = device_data.get('write_iops_sec')
                if write_iops:
                    widgets['write_iops'].insert(0, str(write_iops))
        else:
            self._add_device_entry()

        self._trigger_change()
