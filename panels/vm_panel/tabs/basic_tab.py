"""基础配置 Tab - 虚拟机名称、UUID、机型、CPU、内存等."""

import customtkinter as ctk

from ..styles import CTK_FONT_MAIN, CTK_FONT_BOLD, CTK_FONT_SMALL, BG_COLOR_CONTENT


class BasicTab(ctk.CTkFrame):
    """基础配置 Tab."""

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent')

        # 控件引用
        self.vm_name_entry = None
        self.vm_desc_entry = None
        self.uuid_entry = None
        self.machine_type = None
        self.virt_type = None
        self.chipset_type = None
        self.vcpu_entry = None
        self.cpu_mode = None
        self.memory_entry = None
        self.current_memory_entry = None
        self.max_memory_entry = None
        self.swap_entry = None

        # 初始化 UI
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面."""
        # 配置 grid 权重
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)

        # 系统配置
        sys_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=8)
        sys_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=10)
        sys_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            sys_frame, text='系统配置', font=CTK_FONT_BOLD, text_color='#64b5f6'
        ).grid(row=0, column=0, columnspan=4, padx=10, pady=5, sticky='w')

        # 第一行：虚拟机名称和描述
        ctk.CTkLabel(
            sys_frame, text='虚拟机名称:', font=CTK_FONT_MAIN, width=100, anchor='w'
        ).grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.vm_name_entry = ctk.CTkEntry(sys_frame, placeholder_text='vm-name', width=200)
        self.vm_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.vm_name_entry.insert(0, 'vm0')

        ctk.CTkLabel(
            sys_frame, text='描述:', font=CTK_FONT_MAIN, width=60, anchor='w'
        ).grid(row=1, column=2, padx=5, pady=5, sticky='w')
        self.vm_desc_entry = ctk.CTkEntry(sys_frame, placeholder_text='虚拟机描述', width=200)
        self.vm_desc_entry.grid(row=1, column=3, padx=5, pady=5, sticky='w')

        # 第二行：UUID 和 机型
        ctk.CTkLabel(sys_frame, text='UUID:', font=CTK_FONT_MAIN, width=60, anchor='w').grid(
            row=2, column=0, padx=5, pady=5, sticky='w'
        )
        self.uuid_entry = ctk.CTkEntry(sys_frame, placeholder_text='自动生成', width=300)
        self.uuid_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')

        ctk.CTkLabel(sys_frame, text='机型:', font=CTK_FONT_MAIN, width=60, anchor='w').grid(
            row=2, column=2, padx=5, pady=5, sticky='w'
        )
        self.machine_type = ctk.CTkOptionMenu(
            sys_frame, values=['q35', 'pc', 'pc-i440fx', 'virt', 'arm-virt'], width=120, font=CTK_FONT_SMALL
        )
        self.machine_type.set('q35')
        self.machine_type.grid(row=2, column=3, padx=5, pady=5, sticky='w')

        # 第三行：虚拟化类型和芯片组
        ctk.CTkLabel(sys_frame, text='虚拟化:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=3, column=0, padx=5, pady=5, sticky='w'
        )
        self.virt_type = ctk.CTkOptionMenu(
            sys_frame, values=['hvm', 'pv', 'exe'], width=100, font=CTK_FONT_SMALL
        )
        self.virt_type.set('hvm')
        self.virt_type.grid(row=3, column=1, padx=5, pady=5, sticky='w')

        ctk.CTkLabel(sys_frame, text='芯片组:', font=CTK_FONT_MAIN, width=70, anchor='w').grid(
            row=3, column=2, padx=5, pady=5, sticky='w'
        )
        self.chipset_type = ctk.CTkOptionMenu(
            sys_frame, values=['PIIX3', 'PIIX4', 'Q35', 'virtio'], width=100, font=CTK_FONT_SMALL
        )
        self.chipset_type.set('Q35')
        self.chipset_type.grid(row=3, column=3, padx=5, pady=5, sticky='w')

        # CPU 配置
        cpu_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=8)
        cpu_frame.grid(row=1, column=0, sticky='ew', padx=10, pady=10)
        cpu_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            cpu_frame, text='CPU 配置', font=CTK_FONT_BOLD, text_color='#4caf50'
        ).grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky='w')

        # vCPU 数量
        ctk.CTkLabel(
            cpu_frame, text='vCPU:', font=CTK_FONT_MAIN, width=80, anchor='w'
        ).grid(row=1, column=0, padx=10, pady=5, sticky='w')
        self.vcpu_entry = ctk.CTkEntry(cpu_frame, placeholder_text='2', width=100)
        self.vcpu_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.vcpu_entry.insert(0, '2')

        # CPU 模式
        ctk.CTkLabel(
            cpu_frame, text='CPU 模式:', font=CTK_FONT_MAIN, width=80, anchor='w'
        ).grid(row=1, column=2, padx=10, pady=5, sticky='w')
        self.cpu_mode = ctk.CTkOptionMenu(
            cpu_frame, values=['host-passthrough', 'host-model', 'custom'], width=150, font=CTK_FONT_SMALL
        )
        self.cpu_mode.set('host-model')
        self.cpu_mode.grid(row=1, column=3, padx=5, pady=5, sticky='w')

        # 内存配置
        mem_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=8)
        mem_frame.grid(row=2, column=0, sticky='ew', padx=10, pady=10)
        mem_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            mem_frame, text='内存配置', font=CTK_FONT_BOLD, text_color='#81c784'
        ).grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky='w')

        # 内存大小
        ctk.CTkLabel(
            mem_frame, text='内存 (MB):', font=CTK_FONT_MAIN, width=80, anchor='w'
        ).grid(row=1, column=0, padx=10, pady=5, sticky='w')
        self.memory_entry = ctk.CTkEntry(mem_frame, placeholder_text='2048', width=100)
        self.memory_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.memory_entry.insert(0, '2048')

        # 当前内存（动态内存）
        ctk.CTkLabel(
            mem_frame, text='当前内存 (MB):', font=CTK_FONT_MAIN, width=100, anchor='w'
        ).grid(row=1, column=2, padx=10, pady=5, sticky='w')
        self.current_memory_entry = ctk.CTkEntry(mem_frame, placeholder_text='2048', width=100)
        self.current_memory_entry.grid(row=1, column=3, padx=5, pady=5, sticky='w')
        self.current_memory_entry.insert(0, '2048')

        # 最大内存（动态内存）
        ctk.CTkLabel(
            mem_frame, text='最大内存 (MB):', font=CTK_FONT_MAIN, width=100, anchor='w'
        ).grid(row=2, column=0, padx=10, pady=5, sticky='w')
        self.max_memory_entry = ctk.CTkEntry(mem_frame, placeholder_text='4096', width=100)
        self.max_memory_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.max_memory_entry.insert(0, '4096')

        # 交换内存
        ctk.CTkLabel(
            mem_frame, text='交换内存 (KB):', font=CTK_FONT_MAIN, width=100, anchor='w'
        ).grid(row=2, column=2, padx=10, pady=5, sticky='w')
        self.swap_entry = ctk.CTkEntry(mem_frame, placeholder_text='0', width=100)
        self.swap_entry.grid(row=2, column=3, padx=5, pady=5, sticky='w')
        self.swap_entry.insert(0, '0')
