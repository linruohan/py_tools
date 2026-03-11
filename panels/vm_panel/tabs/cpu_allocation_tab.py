"""CPU 分配配置 Tab - vCPU 分配和配置."""

import customtkinter as ctk

from ..styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class CPUAllocationTab(ctk.CTkFrame):
    """CPU 分配配置 Tab."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent')
        self.on_change_callback = on_change_callback

        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        left_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        left_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        left_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(left_frame, text='vCPU 配置', font=CTK_FONT_BOLD, text_color='#64b5f6').grid(
            row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
        )

        ctk.CTkLabel(left_frame, text='最大 vCPU:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.max_vcpu = ctk.CTkEntry(left_frame, placeholder_text='2', width=100)
        self.max_vcpu.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.max_vcpu.insert(0, '2')
        self.max_vcpu.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(left_frame, text='当前 vCPU:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.current_vcpu = ctk.CTkEntry(left_frame, placeholder_text='2', width=100)
        self.current_vcpu.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.current_vcpu.insert(0, '2')
        self.current_vcpu.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(left_frame, text='放置模式:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=3, column=0, padx=10, pady=5, sticky='w'
        )
        self.placement = ctk.CTkOptionMenu(
            left_frame,
            values=['static', 'auto'],
            width=100,
            font=CTK_FONT_SMALL,
        )
        self.placement.set('static')
        self.placement.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        self.placement.configure(command=self._trigger_change)

        ctk.CTkLabel(
            left_frame, text='CPU 亲和性:', font=CTK_FONT_MAIN, width=100, anchor='w'
        ).grid(row=4, column=0, padx=10, pady=5, sticky='w')
        self.cpuset = ctk.CTkEntry(left_frame, placeholder_text='1-4,^3', width=150)
        self.cpuset.grid(row=4, column=1, padx=5, pady=5, sticky='w')
        self.cpuset.bind('<KeyRelease>', lambda e: self._trigger_change())

        mid_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        mid_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        mid_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(mid_frame, text='CPU 拓扑', font=CTK_FONT_BOLD, text_color='#4caf50').grid(
            row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
        )

        ctk.CTkLabel(mid_frame, text='Sockets:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.sockets = ctk.CTkEntry(mid_frame, placeholder_text='1', width=80)
        self.sockets.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.sockets.insert(0, '1')
        self.sockets.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(mid_frame, text='Dies:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.dies = ctk.CTkEntry(mid_frame, placeholder_text='1', width=80)
        self.dies.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.dies.insert(0, '1')
        self.dies.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(mid_frame, text='Clusters:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=3, column=0, padx=10, pady=5, sticky='w'
        )
        self.clusters = ctk.CTkEntry(mid_frame, placeholder_text='1', width=80)
        self.clusters.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        self.clusters.insert(0, '1')
        self.clusters.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(mid_frame, text='Cores:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=4, column=0, padx=10, pady=5, sticky='w'
        )
        self.cores = ctk.CTkEntry(mid_frame, placeholder_text='2', width=80)
        self.cores.grid(row=4, column=1, padx=5, pady=5, sticky='w')
        self.cores.insert(0, '2')
        self.cores.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(mid_frame, text='Threads:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=5, column=0, padx=10, pady=5, sticky='w'
        )
        self.threads = ctk.CTkEntry(mid_frame, placeholder_text='1', width=80)
        self.threads.grid(row=5, column=1, padx=5, pady=5, sticky='w')
        self.threads.insert(0, '1')
        self.threads.bind('<KeyRelease>', lambda e: self._trigger_change())

        right_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        right_frame.grid(row=0, column=2, sticky='nsew', padx=5, pady=5)
        right_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(right_frame, text='vCPU 状态', font=CTK_FONT_BOLD, text_color='#ff9800').grid(
            row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
        )

        ctk.CTkLabel(right_frame, text='vCPU ID:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.vcpu_id = ctk.CTkEntry(right_frame, placeholder_text='0', width=80)
        self.vcpu_id.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.vcpu_id.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(right_frame, text='启用:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.vcpu_enabled = ctk.CTkCheckBox(
            right_frame, text='', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.vcpu_enabled.select()
        self.vcpu_enabled.grid(row=2, column=1, padx=5, pady=5, sticky='w')

        ctk.CTkLabel(right_frame, text='热插拔:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=3, column=0, padx=10, pady=5, sticky='w'
        )
        self.hotpluggable = ctk.CTkCheckBox(
            right_frame, text='', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.hotpluggable.grid(row=3, column=1, padx=5, pady=5, sticky='w')

        ctk.CTkLabel(right_frame, text='顺序:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=4, column=0, padx=10, pady=5, sticky='w'
        )
        self.vcpu_order = ctk.CTkEntry(right_frame, placeholder_text='1', width=80)
        self.vcpu_order.grid(row=4, column=1, padx=5, pady=5, sticky='w')
        self.vcpu_order.bind('<KeyRelease>', lambda e: self._trigger_change())

    def _trigger_change(self):
        """触发变化回调."""
        if self.on_change_callback:
            self.on_change_callback()

    def get_config(self) -> dict:
        """获取配置数据."""
        return {
            'max_vcpu': int(self.max_vcpu.get().strip() or '2'),
            'current_vcpu': int(self.current_vcpu.get().strip() or '2'),
            'placement': self.placement.get(),
            'cpuset': self.cpuset.get().strip(),
            'topology': {
                'sockets': int(self.sockets.get().strip() or '1'),
                'dies': int(self.dies.get().strip() or '1'),
                'clusters': int(self.clusters.get().strip() or '1'),
                'cores': int(self.cores.get().strip() or '2'),
                'threads': int(self.threads.get().strip() or '1'),
            },
            'vcpu_state': {
                'id': int(self.vcpu_id.get().strip() or '0'),
                'enabled': self.vcpu_enabled.get(),
                'hotpluggable': self.hotpluggable.get(),
                'order': int(self.vcpu_order.get().strip() or '1'),
            },
        }
