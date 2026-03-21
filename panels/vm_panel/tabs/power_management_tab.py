"""电源管理配置 Tab - Power Management.

根据 libvirt 文档第 18 章实现:
https://www.libvirt.org/formatdomain.html#power-management
"""

import customtkinter as ctk

from components.base_tab import BaseConfigTab


class PowerManagementTab(BaseConfigTab):
    """电源管理配置 Tab.

    支持配置 BIOS 对 ACPI 睡眠状态的支持:
    - S3 (suspend-to-mem): 挂起到内存，功耗较低，唤醒较快
    - S4 (suspend-to-disk): 挂起到磁盘，功耗最低，唤醒较慢

    注意：此设置无法阻止客户机自行执行挂起操作.
    """

    def _init_ui(self) -> None:
        """初始化 UI."""
        row = 0

        # ========== 第一行：S3 和 S4 并排显示 ==========
        row_frame = ctk.CTkFrame(self, fg_color='transparent')
        row_frame.grid(row=row, column=0, padx=10, pady=5, sticky='w')

        # S3 标签
        s3_label = ctk.CTkLabel(
            row_frame,
            text='S3 (挂起到内存):',
            font=('', 10),
            width=120,
            anchor='w',
        )
        s3_label.pack(side='left', padx=(0, 5))

        self.suspend_to_mem = ctk.CTkOptionMenu(
            row_frame,
            values=['None', 'yes', 'no'],
            width=80,
            font=('', 10),
            command=self._trigger_change,
        )
        self.suspend_to_mem.set('None')
        self.suspend_to_mem.pack(side='left', padx=5)

        # S4 标签
        s4_label = ctk.CTkLabel(
            row_frame,
            text='S4 (挂起到磁盘):',
            font=('', 10),
            width=120,
            anchor='w',
        )
        s4_label.pack(side='left', padx=(15, 5))

        self.suspend_to_disk = ctk.CTkOptionMenu(
            row_frame,
            values=['None', 'yes', 'no'],
            width=80,
            font=('', 10),
            command=self._trigger_change,
        )
        self.suspend_to_disk.set('None')
        self.suspend_to_disk.pack(side='left', padx=5)

        row += 1

        # ========== 第二行：说明信息 ==========
        info_text = (
            'S3 (挂起到内存): 系统状态保存到内存，功耗较低，唤醒较快.\n'
            'S4 (挂起到磁盘): 系统状态保存到磁盘，功耗最低，唤醒较慢.\n'
            '注意：此设置无法阻止客户机自行执行挂起操作.\n'
            '提示：选择 "None" 时不生成对应 XML 元素.'
        )
        info_label = ctk.CTkLabel(
            self,
            text=info_text,
            font=('', 9),
            text_color='#888888',
            justify='left',
        )
        info_label.grid(row=row, column=0, padx=10, pady=10, sticky='w')

    def get_config(self) -> dict:
        """获取配置数据."""
        config = {}

        mem_val = self.suspend_to_mem.get()
        if mem_val != 'None':
            config['suspend_to_mem'] = mem_val

        disk_val = self.suspend_to_disk.get()
        if disk_val != 'None':
            config['suspend_to_disk'] = disk_val

        return config

    def to_xml(self) -> dict:
        """生成 XML 配置字典."""
        return {'power_management': self.get_config()}

    def load_config(self, config: dict) -> None:
        """加载配置数据.

        Args:
            config: 包含 suspend_to_mem 和 suspend_to_disk 的字典
        """
        if not config:
            # 重置为 None
            self.suspend_to_mem.set('None')
            self.suspend_to_disk.set('None')
            return

        mem_val = config.get('suspend_to_mem')
        disk_val = config.get('suspend_to_disk')

        # 如果配置中没有值，设置为 None
        self.suspend_to_mem.set(mem_val if mem_val else 'None')
        self.suspend_to_disk.set(disk_val if disk_val else 'None')
