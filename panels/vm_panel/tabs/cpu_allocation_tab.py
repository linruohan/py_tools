"""CPU 分配配置 Tab - vCPU 分配和配置."""

import customtkinter as ctk
from components.base_tab import BaseConfigTab
from utils.parsers import parse_integer_value


class CPUAllocationTab(BaseConfigTab):
    """CPU 分配配置 Tab."""

    def _init_ui(self) -> None:
        """初始化界面."""
        # 使用三列布局，每行三个元素
        for i in range(3):
            self.grid_columnconfigure(i, weight=1)
        
        # 添加标题
        self._create_section_title(self, 'CPU 拓扑配置', row=0, column=0, columnspan=3)
        
        # 第一行：Sockets, Dies, Clusters
        # Sockets
        ctk.CTkLabel(
            self, text='Sockets:', font=('Arial', 12), width=80, anchor='w'
        ).grid(row=1, column=0, padx=10, pady=5, sticky='w')
        self.sockets = ctk.CTkEntry(self, placeholder_text='1', width=100)
        self.sockets.grid(row=1, column=0, padx=100, pady=5, sticky='w')
        self.sockets.insert(0, '1')
        self.sockets.bind('<KeyRelease>', lambda e: self._trigger_change())
        
        # Dies
        ctk.CTkLabel(
            self, text='Dies:', font=('Arial', 12), width=80, anchor='w'
        ).grid(row=1, column=1, padx=10, pady=5, sticky='w')
        self.dies = ctk.CTkEntry(self, placeholder_text='1', width=100)
        self.dies.grid(row=1, column=1, padx=100, pady=5, sticky='w')
        self.dies.insert(0, '1')
        self.dies.bind('<KeyRelease>', lambda e: self._trigger_change())
        
        # Clusters
        ctk.CTkLabel(
            self, text='Clusters:', font=('Arial', 12), width=80, anchor='w'
        ).grid(row=1, column=2, padx=10, pady=5, sticky='w')
        self.clusters = ctk.CTkEntry(self, placeholder_text='1', width=100)
        self.clusters.grid(row=1, column=2, padx=100, pady=5, sticky='w')
        self.clusters.insert(0, '1')
        self.clusters.bind('<KeyRelease>', lambda e: self._trigger_change())
        
        # 第二行：Cores, Threads
        # Cores
        ctk.CTkLabel(
            self, text='Cores:', font=('Arial', 12), width=80, anchor='w'
        ).grid(row=2, column=0, padx=10, pady=5, sticky='w')
        self.cores = ctk.CTkEntry(self, placeholder_text='2', width=100)
        self.cores.grid(row=2, column=0, padx=100, pady=5, sticky='w')
        self.cores.insert(0, '2')
        self.cores.bind('<KeyRelease>', lambda e: self._trigger_change())
        
        # Threads
        ctk.CTkLabel(
            self, text='Threads:', font=('Arial', 12), width=80, anchor='w'
        ).grid(row=2, column=1, padx=10, pady=5, sticky='w')
        self.threads = ctk.CTkEntry(self, placeholder_text='1', width=100)
        self.threads.grid(row=2, column=1, padx=100, pady=5, sticky='w')
        self.threads.insert(0, '1')
        self.threads.bind('<KeyRelease>', lambda e: self._trigger_change())
        
        # 添加说明文本
        info_text = (
            'CPU 拓扑配置说明:\n'
            '- Sockets: 物理插座数量\n'
            '- Dies: 每个插座上的芯片数量\n'
            '- Clusters: 每个芯片上的集群数量\n'
            '- Cores: 每个集群上的核心数量\n'
            '- Threads: 每个核心上的线程数量'
        )
        self._create_info_label(self, info_text, row=3, column=0, columnspan=3)

    def get_config(self) -> dict:
        """获取配置数据."""
        return {
            'topology': {
                'sockets': parse_integer_value(self.sockets.get(), default=1),
                'dies': parse_integer_value(self.dies.get(), default=1),
                'clusters': parse_integer_value(self.clusters.get(), default=1),
                'cores': parse_integer_value(self.cores.get(), default=2),
                'threads': parse_integer_value(self.threads.get(), default=1),
            },
        }

    def to_xml(self) -> dict:
        """生成XML配置字典."""
        return {'cpu_allocation': self.get_config()}
