"""CPU 优化配置 Tab - CPU Tuning (cputune).

根据 libvirt 文档实现完整的 cputune 配置，包括:
- vcpupin: vCPU 亲和性绑定
- emulatorpin: 模拟器线程亲和性
- iothreadpin: IOThread 亲和性
- shares: CPU 份额
- period/quota: 带宽控制
- global_period/global_quota: 全局带宽控制
- emulator_period/emulator_quota: 模拟器带宽控制
- iothread_period/iothread_quota: IOThread 带宽控制
- vcpusched/iothreadsched/emulatorsched: 调度器配置
- cachetune: 缓存分配 (resctrl)
- memorytune: 内存带宽分配 (resctrl)
"""

from typing import ClassVar

import customtkinter as ctk

from components.base_tab import SectionConfig, StandardConfigTab


class CPUTuningTab(StandardConfigTab):
    """CPU 优化配置 Tab - 使用紧凑的单 section 布局."""

    SECTIONS: ClassVar[dict] = {
        'cputune': SectionConfig(
            title='CPU Tuning',
            fields=[],  # 通过自定义代码创建 UI
            color='#64b5f6',
        ),
    }

    def _init_sections_ui(self) -> None:
        """初始化 UI - 所有配置项放在一个区域，每组一行."""
        super()._init_sections_ui()

        frame = self.section_frames['cputune']
        row = 1

        # === CPU 亲和性 ===
        self._create_section_header(frame, 'CPU 亲和性 (Affinity)', row, '#FFD93D')
        row += 1

        # vCPU Pin 列表
        self._create_vcpupin_section(frame, row)
        row += 2

        # emulatorpin
        self._create_emulatorpin_row(frame, row)
        row += 1

        # iothreadpin 列表
        self._create_iothreadpin_section(frame, row)
        row += 2

        # === CPU 带宽控制 ===
        self._create_section_header(frame, 'CPU 带宽控制 (Bandwidth)', row, '#4caf50')
        row += 1

        # shares, period, quota
        self._create_bandwidth_basic_row(frame, row)
        row += 1

        # global_period, global_quota
        self._create_global_bandwidth_row(frame, row)
        row += 1

        # emulator_period, emulator_quota
        self._create_emulator_bandwidth_row(frame, row)
        row += 1

        # iothread_period, iothread_quota
        self._create_iothread_bandwidth_row(frame, row)
        row += 1

        # === 调度器配置 ===
        self._create_section_header(frame, '调度器配置 (Scheduler)', row, '#ff9800')
        row += 1

        # vcpusched
        self._create_vcpusched_row(frame, row)
        row += 1

        # iothreadsched
        self._create_iothreadsched_row(frame, row)
        row += 1

        # emulatorsched
        self._create_emulatorsched_row(frame, row)
        row += 1

        # === 缓存调优 (Cachetune) ===
        self._create_section_header(frame, '缓存调优 (CacheTune) - resctrl', row, '#9c27b0')
        row += 1

        self._create_cachetune_section(frame, row)
        row += 2

        # === 内存带宽调优 (MemoryTune) ===
        self._create_section_header(frame, '内存带宽调优 (MemoryTune) - resctrl', row, '#e91e63')
        row += 1

        self._create_memorytune_section(frame, row)
        row += 2

    def _create_section_header(
        self, parent: ctk.CTkFrame, title: str, row: int, color: str
    ) -> None:
        """创建分组标题."""
        ctk.CTkLabel(parent, text=title, font=('', 11, 'bold'), text_color=color).grid(
            row=row, column=0, columnspan=2, padx=10, pady=(8, 4), sticky='w'
        )

    # ========== CPU 亲和性 ==========
    def _create_vcpupin_section(self, parent: ctk.CTkFrame, row: int) -> None:
        """创建 vCPU Pin 配置区域."""
        # 标题行
        ctk.CTkLabel(parent, text='vCPU Pin:', font=('', 10), width=80, anchor='w').grid(
            row=row, column=0, padx=10, pady=3, sticky='w'
        )

        # 添加按钮行
        btn_frame = ctk.CTkFrame(parent, fg_color='transparent')
        btn_frame.grid(row=row, column=1, sticky='w')

        ctk.CTkLabel(btn_frame, text='vCPU ID:', font=('', 9), width=50, anchor='w').pack(
            side='left'
        )
        self.vcpupin_add_id = ctk.CTkEntry(btn_frame, width=50, font=('', 9))
        self.vcpupin_add_id.insert(0, '0')
        self.vcpupin_add_id.pack(side='left', padx=2)

        ctk.CTkLabel(btn_frame, text='CPUs:', font=('', 9), width=30, anchor='w').pack(
            side='left', padx=(5, 2)
        )
        self.vcpupin_add_cpuset = ctk.CTkEntry(btn_frame, width=80, font=('', 9))
        self.vcpupin_add_cpuset.insert(0, '0-3')
        self.vcpupin_add_cpuset.pack(side='left', padx=2)

        add_btn = ctk.CTkButton(
            btn_frame, text='添加', width=40, height=20, command=self._add_vcpupin, font=('', 9)
        )
        add_btn.pack(side='left', padx=5)

        # 显示区域
        self.vcpupin_frame = ctk.CTkFrame(parent, fg_color='transparent')
        self.vcpupin_frame.grid(row=row + 1, column=0, columnspan=2, padx=10, pady=3, sticky='w')
        self.vcpupin_entries = []  # [(id_entry, cpuset_entry), ...]

    def _add_vcpupin(self) -> None:
        """添加一个 vCPU Pin 配置."""
        vcpu_id = self.vcpupin_add_id.get().strip()
        cpuset = self.vcpupin_add_cpuset.get().strip()
        if not vcpu_id or not cpuset:
            return

        # 检查是否已存在
        for id_entry, _ in self.vcpupin_entries:
            if id_entry.get().strip() == vcpu_id:
                return

        row_frame = ctk.CTkFrame(self.vcpupin_frame, fg_color='transparent')
        row_frame.pack(side='left', padx=3, pady=2)

        ctk.CTkLabel(row_frame, text='vCPU', font=('', 9), width=30, anchor='w').pack(side='left')
        id_entry = ctk.CTkEntry(row_frame, width=40, font=('', 9))
        id_entry.insert(0, vcpu_id)
        id_entry.pack(side='left', padx=2)
        id_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(row_frame, text='CPUs:', font=('', 9), width=30, anchor='w').pack(
            side='left', padx=(2, 2)
        )
        cpuset_entry = ctk.CTkEntry(row_frame, width=70, font=('', 9))
        cpuset_entry.insert(0, cpuset)
        cpuset_entry.pack(side='left', padx=2)
        cpuset_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        del_btn = ctk.CTkButton(
            row_frame,
            text='×',
            width=20,
            height=18,
            command=lambda: self._remove_vcpupin(row_frame, id_entry, cpuset_entry),
            font=('', 9),
        )
        del_btn.pack(side='left', padx=2)

        self.vcpupin_entries.append((id_entry, cpuset_entry))
        self._trigger_change()

    def _remove_vcpupin(self, frame, id_entry, cpuset_entry) -> None:
        """删除一个 vCPU Pin 配置."""
        frame.destroy()
        self.vcpupin_entries.remove((id_entry, cpuset_entry))
        self._trigger_change()

    def _create_emulatorpin_row(self, parent: ctk.CTkFrame, row: int) -> None:
        """创建 emulatorpin 配置行."""
        frame = ctk.CTkFrame(parent, fg_color='transparent')
        frame.grid(row=row, column=0, columnspan=2, padx=10, pady=3, sticky='w')

        ctk.CTkLabel(frame, text='模拟器 Pin:', font=('', 10), width=80, anchor='w').pack(
            side='left'
        )

        ctk.CTkLabel(frame, text='None', font=('', 9), width=40, anchor='w').pack(
            side='left', padx=(10, 2)
        )
        self.emulatorpin_none = ctk.CTkCheckBox(frame, width=15, font=('', 9))
        self.emulatorpin_none.pack(side='left', padx=2)
        self.emulatorpin_none.configure(command=self._on_emulatorpin_none_change)

        ctk.CTkLabel(frame, text='CPUs:', font=('', 9), width=30, anchor='w').pack(
            side='left', padx=(10, 2)
        )
        self.emulatorpin = ctk.CTkEntry(frame, width=100, font=('', 9))
        self.emulatorpin.insert(0, '0-3')
        self.emulatorpin.pack(side='left', padx=2)
        self.emulatorpin.bind('<KeyRelease>', lambda e: self._trigger_change())
        self.emulatorpin_state = 'enabled'

    def _on_emulatorpin_none_change(self) -> None:
        """处理 emulatorpin None 复选框变化."""
        if self.emulatorpin_none.get():
            self.emulatorpin.configure(state='disabled')
            self.emulatorpin_state = 'disabled'
        else:
            self.emulatorpin.configure(state='normal')
            self.emulatorpin_state = 'enabled'
        self._trigger_change()

    def _create_iothreadpin_section(self, parent: ctk.CTkFrame, row: int) -> None:
        """创建 iothreadpin 配置区域."""
        # 标题行
        ctk.CTkLabel(parent, text='IOThread Pin:', font=('', 10), width=80, anchor='w').grid(
            row=row, column=0, padx=10, pady=3, sticky='w'
        )

        # 添加按钮行
        btn_frame = ctk.CTkFrame(parent, fg_color='transparent')
        btn_frame.grid(row=row, column=1, sticky='w')

        ctk.CTkLabel(btn_frame, text='IOThread ID:', font=('', 9), width=70, anchor='w').pack(
            side='left'
        )
        self.iothreadpin_add_id = ctk.CTkEntry(btn_frame, width=50, font=('', 9))
        self.iothreadpin_add_id.insert(0, '1')
        self.iothreadpin_add_id.pack(side='left', padx=2)

        ctk.CTkLabel(btn_frame, text='CPUs:', font=('', 9), width=30, anchor='w').pack(
            side='left', padx=(5, 2)
        )
        self.iothreadpin_add_cpuset = ctk.CTkEntry(btn_frame, width=80, font=('', 9))
        self.iothreadpin_add_cpuset.insert(0, '4-7')
        self.iothreadpin_add_cpuset.pack(side='left', padx=2)

        add_btn = ctk.CTkButton(
            btn_frame, text='添加', width=40, height=20, command=self._add_iothreadpin, font=('', 9)
        )
        add_btn.pack(side='left', padx=5)

        # 显示区域
        self.iothreadpin_frame = ctk.CTkFrame(parent, fg_color='transparent')
        self.iothreadpin_frame.grid(
            row=row + 1, column=0, columnspan=2, padx=10, pady=3, sticky='w'
        )
        self.iothreadpin_entries = []  # [(id_entry, cpuset_entry), ...]

    def _add_iothreadpin(self) -> None:
        """添加一个 IOThread Pin 配置."""
        iothread_id = self.iothreadpin_add_id.get().strip()
        cpuset = self.iothreadpin_add_cpuset.get().strip()
        if not iothread_id or not cpuset:
            return

        # 检查是否已存在
        for id_entry, _ in self.iothreadpin_entries:
            if id_entry.get().strip() == iothread_id:
                return

        row_frame = ctk.CTkFrame(self.iothreadpin_frame, fg_color='transparent')
        row_frame.pack(side='left', padx=3, pady=2)

        ctk.CTkLabel(row_frame, text='IOThread', font=('', 9), width=50, anchor='w').pack(
            side='left'
        )
        id_entry = ctk.CTkEntry(row_frame, width=40, font=('', 9))
        id_entry.insert(0, iothread_id)
        id_entry.pack(side='left', padx=2)
        id_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(row_frame, text='CPUs:', font=('', 9), width=30, anchor='w').pack(
            side='left', padx=(2, 2)
        )
        cpuset_entry = ctk.CTkEntry(row_frame, width=70, font=('', 9))
        cpuset_entry.insert(0, cpuset)
        cpuset_entry.pack(side='left', padx=2)
        cpuset_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        del_btn = ctk.CTkButton(
            row_frame,
            text='×',
            width=20,
            height=18,
            command=lambda: self._remove_iothreadpin(row_frame, id_entry, cpuset_entry),
            font=('', 9),
        )
        del_btn.pack(side='left', padx=2)

        self.iothreadpin_entries.append((id_entry, cpuset_entry))
        self._trigger_change()

    def _remove_iothreadpin(self, frame, id_entry, cpuset_entry) -> None:
        """删除一个 IOThread Pin 配置."""
        frame.destroy()
        self.iothreadpin_entries.remove((id_entry, cpuset_entry))
        self._trigger_change()

    # ========== CPU 带宽控制 ==========
    def _create_bandwidth_basic_row(self, parent: ctk.CTkFrame, row: int) -> None:
        """创建基础带宽配置行：shares, period, quota."""
        frame = ctk.CTkFrame(parent, fg_color='transparent')
        frame.grid(row=row, column=0, columnspan=2, padx=10, pady=3, sticky='w')

        # shares
        ctk.CTkLabel(frame, text='份额 (shares):', font=('', 10), width=90, anchor='w').pack(
            side='left'
        )
        self.shares = ctk.CTkEntry(frame, width=70, font=('', 9))
        self.shares.insert(0, '')
        self.shares.pack(side='left', padx=2)
        self.shares.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(frame, text='周期 (μs):', font=('', 9), width=60, anchor='w').pack(
            side='left', padx=(10, 2)
        )
        self.period = ctk.CTkEntry(frame, width=70, font=('', 9))
        self.period.insert(0, '')
        self.period.pack(side='left', padx=2)
        self.period.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(frame, text='配额 (μs):', font=('', 9), width=60, anchor='w').pack(
            side='left', padx=(10, 2)
        )
        self.quota = ctk.CTkEntry(frame, width=70, font=('', 9))
        self.quota.insert(0, '')
        self.quota.pack(side='left', padx=2)
        self.quota.bind('<KeyRelease>', lambda e: self._trigger_change())

    def _create_global_bandwidth_row(self, parent: ctk.CTkFrame, row: int) -> None:
        """创建全局带宽配置行：global_period, global_quota."""
        frame = ctk.CTkFrame(parent, fg_color='transparent')
        frame.grid(row=row, column=0, columnspan=2, padx=10, pady=3, sticky='w')

        ctk.CTkLabel(frame, text='全局周期 (μs):', font=('', 10), width=90, anchor='w').pack(
            side='left'
        )
        self.global_period = ctk.CTkEntry(frame, width=70, font=('', 9))
        self.global_period.insert(0, '')
        self.global_period.pack(side='left', padx=2)
        self.global_period.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(frame, text='全局配额 (μs):', font=('', 9), width=70, anchor='w').pack(
            side='left', padx=(10, 2)
        )
        self.global_quota = ctk.CTkEntry(frame, width=70, font=('', 9))
        self.global_quota.insert(0, '')
        self.global_quota.pack(side='left', padx=2)
        self.global_quota.bind('<KeyRelease>', lambda e: self._trigger_change())

    def _create_emulator_bandwidth_row(self, parent: ctk.CTkFrame, row: int) -> None:
        """创建模拟器带宽配置行：emulator_period, emulator_quota."""
        frame = ctk.CTkFrame(parent, fg_color='transparent')
        frame.grid(row=row, column=0, columnspan=2, padx=10, pady=3, sticky='w')

        ctk.CTkLabel(frame, text='模拟器周期 (μs):', font=('', 10), width=90, anchor='w').pack(
            side='left'
        )
        self.emulator_period = ctk.CTkEntry(frame, width=70, font=('', 9))
        self.emulator_period.insert(0, '')
        self.emulator_period.pack(side='left', padx=2)
        self.emulator_period.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(frame, text='模拟器配额 (μs):', font=('', 9), width=70, anchor='w').pack(
            side='left', padx=(10, 2)
        )
        self.emulator_quota = ctk.CTkEntry(frame, width=70, font=('', 9))
        self.emulator_quota.insert(0, '')
        self.emulator_quota.pack(side='left', padx=2)
        self.emulator_quota.bind('<KeyRelease>', lambda e: self._trigger_change())

    def _create_iothread_bandwidth_row(self, parent: ctk.CTkFrame, row: int) -> None:
        """创建 IOThread 带宽配置行：iothread_period, iothread_quota."""
        frame = ctk.CTkFrame(parent, fg_color='transparent')
        frame.grid(row=row, column=0, columnspan=2, padx=10, pady=3, sticky='w')

        ctk.CTkLabel(frame, text='IOThread 周期 (μs):', font=('', 10), width=90, anchor='w').pack(
            side='left'
        )
        self.iothread_period = ctk.CTkEntry(frame, width=70, font=('', 9))
        self.iothread_period.insert(0, '')
        self.iothread_period.pack(side='left', padx=2)
        self.iothread_period.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(frame, text='IOThread 配额 (μs):', font=('', 9), width=70, anchor='w').pack(
            side='left', padx=(10, 2)
        )
        self.iothread_quota = ctk.CTkEntry(frame, width=70, font=('', 9))
        self.iothread_quota.insert(0, '')
        self.iothread_quota.pack(side='left', padx=2)
        self.iothread_quota.bind('<KeyRelease>', lambda e: self._trigger_change())

    # ========== 调度器配置 ==========
    def _create_vcpusched_row(self, parent: ctk.CTkFrame, row: int) -> None:
        """创建 vcpusched 配置行."""
        frame = ctk.CTkFrame(parent, fg_color='transparent')
        frame.grid(row=row, column=0, columnspan=2, padx=10, pady=3, sticky='w')

        # None 选项
        ctk.CTkLabel(frame, text='vCPU 调度器:', font=('', 10), width=90, anchor='w').pack(
            side='left'
        )
        self.vcpusched_none = ctk.CTkCheckBox(frame, text='None', width=50, font=('', 9))
        self.vcpusched_none.pack(side='left', padx=2)
        self.vcpusched_none.configure(command=self._on_vcpusched_none_change)

        ctk.CTkLabel(frame, text='vCPUs:', font=('', 9), width=40, anchor='w').pack(
            side='left', padx=(10, 2)
        )
        self.vcpusched_vcpus = ctk.CTkEntry(frame, width=60, font=('', 9))
        self.vcpusched_vcpus.insert(0, '0-3')
        self.vcpusched_vcpus.pack(side='left', padx=2)
        self.vcpusched_vcpus.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(frame, text='调度器:', font=('', 9), width=50, anchor='w').pack(
            side='left', padx=(10, 2)
        )
        self.vcpusched_scheduler = ctk.CTkOptionMenu(
            frame, values=['batch', 'idle', 'fifo', 'rr'], width=50, font=('', 9)
        )
        self.vcpusched_scheduler.set('batch')
        self.vcpusched_scheduler.pack(side='left', padx=2)
        self.vcpusched_scheduler.configure(command=self._on_vcpusched_scheduler_change)

        ctk.CTkLabel(frame, text='优先级:', font=('', 9), width=40, anchor='w').pack(
            side='left', padx=(10, 2)
        )
        self.vcpusched_priority = ctk.CTkEntry(frame, width=40, font=('', 9))
        self.vcpusched_priority.insert(0, '')
        self.vcpusched_priority.pack(side='left', padx=2)
        self.vcpusched_priority.bind('<KeyRelease>', lambda e: self._trigger_change())

        self.vcpusched_state = 'enabled'

    def _on_vcpusched_none_change(self) -> None:
        """处理 vcpusched None 复选框变化."""
        if self.vcpusched_none.get():
            self.vcpusched_vcpus.configure(state='disabled')
            self.vcpusched_scheduler.configure(state='disabled')
            self.vcpusched_priority.configure(state='disabled')
            self.vcpusched_state = 'disabled'
        else:
            self.vcpusched_vcpus.configure(state='normal')
            self.vcpusched_scheduler.configure(state='normal')
            self.vcpusched_priority.configure(state='normal')
            self.vcpusched_state = 'enabled'
        self._trigger_change()

    def _on_vcpusched_scheduler_change(self, value: str) -> None:
        """调度器类型变化时，启用/禁用优先级."""
        if value in ('fifo', 'rr'):
            self.vcpusched_priority.configure(state='normal')
        else:
            self.vcpusched_priority.configure(state='disabled')
            self.vcpusched_priority.delete(0, 'end')
        self._trigger_change()

    def _create_iothreadsched_row(self, parent: ctk.CTkFrame, row: int) -> None:
        """创建 iothreadsched 配置行."""
        frame = ctk.CTkFrame(parent, fg_color='transparent')
        frame.grid(row=row, column=0, columnspan=2, padx=10, pady=3, sticky='w')

        # None 选项
        ctk.CTkLabel(frame, text='IOThread 调度器:', font=('', 10), width=90, anchor='w').pack(
            side='left'
        )
        self.iothreadsched_none = ctk.CTkCheckBox(frame, text='None', width=50, font=('', 9))
        self.iothreadsched_none.pack(side='left', padx=2)
        self.iothreadsched_none.configure(command=self._on_iothreadsched_none_change)

        ctk.CTkLabel(frame, text='IOThreads:', font=('', 9), width=60, anchor='w').pack(
            side='left', padx=(10, 2)
        )
        self.iothreadsched_iothreads = ctk.CTkEntry(frame, width=50, font=('', 9))
        self.iothreadsched_iothreads.insert(0, '1')
        self.iothreadsched_iothreads.pack(side='left', padx=2)
        self.iothreadsched_iothreads.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(frame, text='调度器:', font=('', 9), width=50, anchor='w').pack(
            side='left', padx=(10, 2)
        )
        self.iothreadsched_scheduler = ctk.CTkOptionMenu(
            frame, values=['batch', 'idle', 'fifo', 'rr'], width=50, font=('', 9)
        )
        self.iothreadsched_scheduler.set('batch')
        self.iothreadsched_scheduler.pack(side='left', padx=2)
        self.iothreadsched_scheduler.configure(command=self._on_iothreadsched_scheduler_change)

        ctk.CTkLabel(frame, text='优先级:', font=('', 9), width=40, anchor='w').pack(
            side='left', padx=(10, 2)
        )
        self.iothreadsched_priority = ctk.CTkEntry(frame, width=40, font=('', 9))
        self.iothreadsched_priority.insert(0, '')
        self.iothreadsched_priority.pack(side='left', padx=2)
        self.iothreadsched_priority.bind('<KeyRelease>', lambda e: self._trigger_change())

        self.iothreadsched_state = 'enabled'

    def _on_iothreadsched_none_change(self) -> None:
        """处理 iothreadsched None 复选框变化."""
        if self.iothreadsched_none.get():
            self.iothreadsched_iothreads.configure(state='disabled')
            self.iothreadsched_scheduler.configure(state='disabled')
            self.iothreadsched_priority.configure(state='disabled')
            self.iothreadsched_state = 'disabled'
        else:
            self.iothreadsched_iothreads.configure(state='normal')
            self.iothreadsched_scheduler.configure(state='normal')
            self.iothreadsched_priority.configure(state='normal')
            self.iothreadsched_state = 'enabled'
        self._trigger_change()

    def _on_iothreadsched_scheduler_change(self, value: str) -> None:
        """调度器类型变化时，启用/禁用优先级."""
        if value in ('fifo', 'rr'):
            self.iothreadsched_priority.configure(state='normal')
        else:
            self.iothreadsched_priority.configure(state='disabled')
            self.iothreadsched_priority.delete(0, 'end')
        self._trigger_change()

    def _create_emulatorsched_row(self, parent: ctk.CTkFrame, row: int) -> None:
        """创建 emulatorsched 配置行."""
        frame = ctk.CTkFrame(parent, fg_color='transparent')
        frame.grid(row=row, column=0, columnspan=2, padx=10, pady=3, sticky='w')

        # None 选项
        ctk.CTkLabel(frame, text='模拟器调度器:', font=('', 10), width=90, anchor='w').pack(
            side='left'
        )
        self.emulatorsched_none = ctk.CTkCheckBox(frame, text='None', width=50, font=('', 9))
        self.emulatorsched_none.pack(side='left', padx=2)
        self.emulatorsched_none.configure(command=self._on_emulatorsched_none_change)

        ctk.CTkLabel(frame, text='调度器:', font=('', 9), width=50, anchor='w').pack(
            side='left', padx=(10, 2)
        )
        self.emulatorsched_scheduler = ctk.CTkOptionMenu(
            frame, values=['batch', 'idle', 'fifo', 'rr'], width=50, font=('', 9)
        )
        self.emulatorsched_scheduler.set('batch')
        self.emulatorsched_scheduler.pack(side='left', padx=2)
        self.emulatorsched_scheduler.configure(command=self._on_emulatorsched_scheduler_change)

        ctk.CTkLabel(frame, text='优先级:', font=('', 9), width=40, anchor='w').pack(
            side='left', padx=(10, 2)
        )
        self.emulatorsched_priority = ctk.CTkEntry(frame, width=40, font=('', 9))
        self.emulatorsched_priority.insert(0, '')
        self.emulatorsched_priority.pack(side='left', padx=2)
        self.emulatorsched_priority.bind('<KeyRelease>', lambda e: self._trigger_change())

        self.emulatorsched_state = 'enabled'

    def _on_emulatorsched_none_change(self) -> None:
        """处理 emulatorsched None 复选框变化."""
        if self.emulatorsched_none.get():
            self.emulatorsched_scheduler.configure(state='disabled')
            self.emulatorsched_priority.configure(state='disabled')
            self.emulatorsched_state = 'disabled'
        else:
            self.emulatorsched_scheduler.configure(state='normal')
            self.emulatorsched_priority.configure(state='normal')
            self.emulatorsched_state = 'enabled'
        self._trigger_change()

    def _on_emulatorsched_scheduler_change(self, value: str) -> None:
        """调度器类型变化时，启用/禁用优先级."""
        if value in ('fifo', 'rr'):
            self.emulatorsched_priority.configure(state='normal')
        else:
            self.emulatorsched_priority.configure(state='disabled')
            self.emulatorsched_priority.delete(0, 'end')
        self._trigger_change()

    # ========== 缓存调优 (Cachetune) ==========
    def _create_cachetune_section(self, parent: ctk.CTkFrame, row: int) -> None:
        """创建 cachetune 配置区域."""
        # 添加 cachetune 按钮行
        btn_frame = ctk.CTkFrame(parent, fg_color='transparent')
        btn_frame.grid(row=row, column=0, columnspan=2, padx=10, pady=3, sticky='w')

        ctk.CTkButton(
            btn_frame,
            text='添加 CacheTune',
            width=100,
            height=25,
            command=self._add_cachetune,
            font=('', 9),
        ).pack(side='left', padx=0)

        # cachetune 列表显示区域
        self.cachetune_container = ctk.CTkScrollableFrame(
            parent, fg_color='transparent', height=120
        )
        self.cachetune_container.grid(
            row=row + 1, column=0, columnspan=2, padx=10, pady=3, sticky='nsew'
        )
        self.cachetune_entries = []  # [cachetune_frame, ...]

    def _add_cachetune(self) -> None:
        """添加一个 cachetune 配置组."""
        frame = ctk.CTkFrame(self.cachetune_container, fg_color='#2a2a2a', corner_radius=4)
        frame.pack(fill='x', padx=5, pady=3)

        # 第一行：vcpus 和删除按钮
        top_row = ctk.CTkFrame(frame, fg_color='transparent')
        top_row.pack(fill='x', padx=5, pady=2)

        ctk.CTkLabel(top_row, text='vCPUs:', font=('', 9), width=40, anchor='w').pack(side='left')
        vcpus_entry = ctk.CTkEntry(top_row, width=80, font=('', 9))
        vcpus_entry.insert(0, '0-3')
        vcpus_entry.pack(side='left', padx=2)
        vcpus_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        del_btn = ctk.CTkButton(
            top_row,
            text='删除',
            width=40,
            height=18,
            command=lambda: self._remove_cachetune(frame),
            font=('', 9),
        )
        del_btn.pack(side='left', padx=10)

        # 第二行：cache 配置
        cache_row = ctk.CTkFrame(frame, fg_color='transparent')
        cache_row.pack(fill='x', padx=5, pady=2)

        ctk.CTkLabel(cache_row, text='Cache:', font=('', 9), width=45, anchor='w').pack(side='left')
        ctk.CTkLabel(cache_row, text='Level:', font=('', 8), width=35, anchor='w').pack(
            side='left', padx=(5, 2)
        )
        cache_level = ctk.CTkOptionMenu(cache_row, values=['1', '2', '3'], width=45, font=('', 8))
        cache_level.set('3')
        cache_level.pack(side='left', padx=2)
        cache_level.configure(command=lambda e: self._trigger_change())

        ctk.CTkLabel(cache_row, text='Type:', font=('', 8), width=30, anchor='w').pack(
            side='left', padx=(5, 2)
        )
        cache_type = ctk.CTkOptionMenu(
            cache_row, values=['code', 'data', 'both'], width=50, font=('', 8)
        )
        cache_type.set('both')
        cache_type.pack(side='left', padx=2)
        cache_type.configure(command=lambda e: self._trigger_change())

        ctk.CTkLabel(cache_row, text='Size:', font=('', 8), width=30, anchor='w').pack(
            side='left', padx=(5, 2)
        )
        cache_size = ctk.CTkEntry(cache_row, width=50, font=('', 8))
        cache_size.insert(0, '3')
        cache_size.pack(side='left', padx=2)
        cache_size.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(cache_row, text='Unit:', font=('', 8), width=30, anchor='w').pack(
            side='left', padx=(2, 2)
        )
        cache_unit = ctk.CTkOptionMenu(
            cache_row, values=['KiB', 'MiB', 'GiB'], width=45, font=('', 8)
        )
        cache_unit.set('MiB')
        cache_unit.pack(side='left', padx=2)
        cache_unit.configure(command=lambda e: self._trigger_change())

        # 第三行：monitor 配置
        monitor_row = ctk.CTkFrame(frame, fg_color='transparent')
        monitor_row.pack(fill='x', padx=5, pady=2)

        ctk.CTkLabel(monitor_row, text='Monitor:', font=('', 9), width=45, anchor='w').pack(
            side='left'
        )
        ctk.CTkLabel(monitor_row, text='vCPUs:', font=('', 8), width=35, anchor='w').pack(
            side='left', padx=(5, 2)
        )
        monitor_vcpus = ctk.CTkEntry(monitor_row, width=80, font=('', 8))
        monitor_vcpus.insert(0, '0-3')
        monitor_vcpus.pack(side='left', padx=2)
        monitor_vcpus.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(monitor_row, text='Level:', font=('', 8), width=30, anchor='w').pack(
            side='left', padx=(10, 2)
        )
        monitor_level = ctk.CTkOptionMenu(
            monitor_row, values=['1', '2', '3'], width=45, font=('', 8)
        )
        monitor_level.set('3')
        monitor_level.pack(side='left', padx=2)
        monitor_level.configure(command=lambda e: self._trigger_change())

        self.cachetune_entries.append(
            {
                'frame': frame,
                'vcpus': vcpus_entry,
                'cache_level': cache_level,
                'cache_type': cache_type,
                'cache_size': cache_size,
                'cache_unit': cache_unit,
                'monitor_vcpus': monitor_vcpus,
                'monitor_level': monitor_level,
            }
        )
        self._trigger_change()

    def _remove_cachetune(self, frame) -> None:
        """删除一个 cachetune 配置."""
        frame.destroy()
        self.cachetune_entries = [e for e in self.cachetune_entries if e['frame'] != frame]
        self._trigger_change()

    # ========== 内存带宽调优 (MemoryTune) ==========
    def _create_memorytune_section(self, parent: ctk.CTkFrame, row: int) -> None:
        """创建 memorytune 配置区域."""
        # 添加 memorytune 按钮行
        btn_frame = ctk.CTkFrame(parent, fg_color='transparent')
        btn_frame.grid(row=row, column=0, columnspan=2, padx=10, pady=3, sticky='w')

        ctk.CTkButton(
            btn_frame,
            text='添加 MemoryTune',
            width=100,
            height=25,
            command=self._add_memorytune,
            font=('', 9),
        ).pack(side='left', padx=0)

        # memorytune 列表显示区域
        self.memorytune_container = ctk.CTkScrollableFrame(
            parent, fg_color='transparent', height=120
        )
        self.memorytune_container.grid(
            row=row + 1, column=0, columnspan=2, padx=10, pady=3, sticky='nsew'
        )
        self.memorytune_entries = []  # [memorytune_frame, ...]

    def _add_memorytune(self) -> None:
        """添加一个 memorytune 配置组."""
        frame = ctk.CTkFrame(self.memorytune_container, fg_color='#2a2a2a', corner_radius=4)
        frame.pack(fill='x', padx=5, pady=3)

        # 第一行：vcpus 和删除按钮
        top_row = ctk.CTkFrame(frame, fg_color='transparent')
        top_row.pack(fill='x', padx=5, pady=2)

        ctk.CTkLabel(top_row, text='vCPUs:', font=('', 9), width=40, anchor='w').pack(side='left')
        vcpus_entry = ctk.CTkEntry(top_row, width=80, font=('', 9))
        vcpus_entry.insert(0, '0-3')
        vcpus_entry.pack(side='left', padx=2)
        vcpus_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        del_btn = ctk.CTkButton(
            top_row,
            text='删除',
            width=40,
            height=18,
            command=lambda: self._remove_memorytune(frame),
            font=('', 9),
        )
        del_btn.pack(side='left', padx=10)

        # 第二行：node 配置
        node_row = ctk.CTkFrame(frame, fg_color='transparent')
        node_row.pack(fill='x', padx=5, pady=2)

        ctk.CTkLabel(node_row, text='NUMA Node:', font=('', 9), width=60, anchor='w').pack(
            side='left'
        )
        node_id = ctk.CTkEntry(node_row, width=50, font=('', 9))
        node_id.insert(0, '0')
        node_id.pack(side='left', padx=2)
        node_id.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(node_row, text='Bandwidth (%):', font=('', 9), width=80, anchor='w').pack(
            side='left', padx=(10, 2)
        )
        bandwidth = ctk.CTkEntry(node_row, width=50, font=('', 9))
        bandwidth.insert(0, '100')
        bandwidth.pack(side='left', padx=2)
        bandwidth.bind('<KeyRelease>', lambda e: self._trigger_change())

        self.memorytune_entries.append(
            {
                'frame': frame,
                'vcpus': vcpus_entry,
                'node_id': node_id,
                'bandwidth': bandwidth,
            }
        )
        self._trigger_change()

    def _remove_memorytune(self, frame) -> None:
        """删除一个 memorytune 配置."""
        frame.destroy()
        self.memorytune_entries = [e for e in self.memorytune_entries if e['frame'] != frame]
        self._trigger_change()

    def get_config(self) -> dict:
        """获取配置数据."""
        config = {}

        # vcpupin
        vcpupins = []
        for id_entry, cpuset_entry in self.vcpupin_entries:
            vcpu_id = id_entry.get().strip()
            cpuset = cpuset_entry.get().strip()
            if vcpu_id and cpuset:
                vcpupins.append({'vcpu': vcpu_id, 'cpuset': cpuset})
        if vcpupins:
            config['vcpupin'] = vcpupins

        # emulatorpin
        if self.emulatorpin_state == 'enabled':
            emulatorpin = self.emulatorpin.get().strip()
            if emulatorpin:
                config['emulatorpin'] = emulatorpin

        # iothreadpin
        iothreadpins = []
        for id_entry, cpuset_entry in self.iothreadpin_entries:
            iothread_id = id_entry.get().strip()
            cpuset = cpuset_entry.get().strip()
            if iothread_id and cpuset:
                iothreadpins.append({'iothread': iothread_id, 'cpuset': cpuset})
        if iothreadpins:
            config['iothreadpin'] = iothreadpins

        # shares, period, quota
        shares = self.shares.get().strip()
        if shares:
            config['shares'] = int(shares)
        period = self.period.get().strip()
        if period:
            config['period'] = int(period)
        quota = self.quota.get().strip()
        if quota:
            config['quota'] = int(quota)

        # global_period, global_quota
        global_period = self.global_period.get().strip()
        if global_period:
            config['global_period'] = int(global_period)
        global_quota = self.global_quota.get().strip()
        if global_quota:
            config['global_quota'] = int(global_quota)

        # emulator_period, emulator_quota
        emulator_period = self.emulator_period.get().strip()
        if emulator_period:
            config['emulator_period'] = int(emulator_period)
        emulator_quota = self.emulator_quota.get().strip()
        if emulator_quota:
            config['emulator_quota'] = int(emulator_quota)

        # iothread_period, iothread_quota
        iothread_period = self.iothread_period.get().strip()
        if iothread_period:
            config['iothread_period'] = int(iothread_period)
        iothread_quota = self.iothread_quota.get().strip()
        if iothread_quota:
            config['iothread_quota'] = int(iothread_quota)

        # vcpusched
        if self.vcpusched_state == 'enabled':
            vcpusched = {}
            vcpus = self.vcpusched_vcpus.get().strip()
            if vcpus:
                vcpusched['vcpus'] = vcpus
            scheduler = self.vcpusched_scheduler.get()
            vcpusched['scheduler'] = scheduler
            priority = self.vcpusched_priority.get().strip()
            if priority and scheduler in ('fifo', 'rr'):
                vcpusched['priority'] = int(priority)
            if vcpusched:
                config['vcpusched'] = vcpusched

        # iothreadsched
        if self.iothreadsched_state == 'enabled':
            iothreadsched = {}
            iothreads = self.iothreadsched_iothreads.get().strip()
            if iothreads:
                iothreadsched['iothreads'] = iothreads
            scheduler = self.iothreadsched_scheduler.get()
            iothreadsched['scheduler'] = scheduler
            priority = self.iothreadsched_priority.get().strip()
            if priority and scheduler in ('fifo', 'rr'):
                iothreadsched['priority'] = int(priority)
            if iothreadsched:
                config['iothreadsched'] = iothreadsched

        # emulatorsched
        if self.emulatorsched_state == 'enabled':
            emulatorsched = {}
            scheduler = self.emulatorsched_scheduler.get()
            emulatorsched['scheduler'] = scheduler
            priority = self.emulatorsched_priority.get().strip()
            if priority and scheduler in ('fifo', 'rr'):
                emulatorsched['priority'] = int(priority)
            if emulatorsched:
                config['emulatorsched'] = emulatorsched

        # cachetune
        cachetunes = []
        for entry in self.cachetune_entries:
            ct = {}
            vcpus = entry['vcpus'].get().strip()
            if vcpus:
                ct['vcpus'] = vcpus

            cache = {}
            cache['level'] = int(entry['cache_level'].get())
            cache['type'] = entry['cache_type'].get()
            cache['size'] = int(entry['cache_size'].get())
            cache['unit'] = entry['cache_unit'].get()
            ct['cache'] = cache

            monitor = {}
            monitor['vcpus'] = entry['monitor_vcpus'].get().strip()
            monitor['level'] = int(entry['monitor_level'].get())
            ct['monitor'] = monitor

            if ct:
                cachetunes.append(ct)
        if cachetunes:
            config['cachetune'] = cachetunes

        # memorytune
        memorytunes = []
        for entry in self.memorytune_entries:
            mt = {}
            vcpus = entry['vcpus'].get().strip()
            if vcpus:
                mt['vcpus'] = vcpus

            node = {}
            node['id'] = int(entry['node_id'].get())
            node['bandwidth'] = int(entry['bandwidth'].get())
            mt['node'] = node

            if mt:
                memorytunes.append(mt)
        if memorytunes:
            config['memorytune'] = memorytunes

        return config

    def to_xml(self) -> dict:
        """生成 XML 配置字典."""
        return {'cpu_tuning': self.get_config()}

    def load_config(self, config: dict) -> None:
        """加载配置数据."""
        # TODO: 实现配置加载
        pass
