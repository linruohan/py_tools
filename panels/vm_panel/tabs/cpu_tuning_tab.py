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
        """初始化 UI - 5 个 section 按列布局."""
        super()._init_sections_ui()

        # 清除默认的 section 框架，重新创建 5 列布局
        for widget in self.section_frames['cputune'].winfo_children():
            widget.destroy()

        main_frame = self.section_frames['cputune']
        main_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        # === 第 1 列：CPU 亲和性 ===
        col0 = ctk.CTkFrame(main_frame, fg_color='#1a1a1a', corner_radius=8)
        col0.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        col0.grid_columnconfigure(0, weight=1)
        self._create_affinity_section(col0, row=0)

        # === 第 2 列：CPU 带宽控制 ===
        col1 = ctk.CTkFrame(main_frame, fg_color='#1a1a1a', corner_radius=8)
        col1.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
        col1.grid_columnconfigure(0, weight=1)
        self._create_bandwidth_section(col1, row=0)

        # === 第 3 列：调度器配置 ===
        col2 = ctk.CTkFrame(main_frame, fg_color='#1a1a1a', corner_radius=8)
        col2.grid(row=0, column=2, padx=5, pady=5, sticky='nsew')
        col2.grid_columnconfigure(0, weight=1)
        self._create_scheduler_section(col2, row=0)

        # === 第 4 列：缓存调优 ===
        col3 = ctk.CTkFrame(main_frame, fg_color='#1a1a1a', corner_radius=8)
        col3.grid(row=0, column=3, padx=5, pady=5, sticky='nsew')
        col3.grid_columnconfigure(0, weight=1)
        self._create_cachetune_section(col3, row=0)

        # === 第 5 列：内存带宽调优 ===
        col4 = ctk.CTkFrame(main_frame, fg_color='#1a1a1a', corner_radius=8)
        col4.grid(row=0, column=4, padx=5, pady=5, sticky='nsew')
        col4.grid_columnconfigure(0, weight=1)
        self._create_memorytune_section(col4, row=0)

    def _create_affinity_section(self, parent: ctk.CTkFrame, row: int) -> None:
        """创建第 1 列：CPU 亲和性."""
        # 标题
        ctk.CTkLabel(parent, text='CPU 亲和性', font=('', 11, 'bold'), text_color='#FFD93D').grid(
            row=row, column=0, padx=10, pady=8, sticky='w'
        )
        row += 1

        # vCPU Pin
        ctk.CTkLabel(parent, text='vCPU Pin:', font=('', 9)).grid(
            row=row, column=0, padx=5, pady=2, sticky='w'
        )
        row += 1

        self.vcpupin_frame = ctk.CTkFrame(parent, fg_color='transparent')
        self.vcpupin_frame.grid(row=row, column=0, padx=5, pady=2, sticky='ew')
        self.vcpupin_entries = []

        entry_row = ctk.CTkFrame(self.vcpupin_frame, fg_color='transparent')
        entry_row.pack(fill='x')
        ctk.CTkLabel(entry_row, text='vCPU:', font=('', 8), width=35).pack(side='left')
        self.vcpupin_add_id = ctk.CTkEntry(entry_row, width=40, font=('', 8))
        self.vcpupin_add_id.pack(side='left', padx=2)

        ctk.CTkLabel(entry_row, text='CPUs:', font=('', 8), width=35).pack(side='left', padx=(5, 2))
        self.vcpupin_add_cpuset = ctk.CTkEntry(entry_row, width=60, font=('', 8))
        self.vcpupin_add_cpuset.pack(side='left', padx=2)

        ctk.CTkButton(
            entry_row, text='+', width=25, height=20, command=self._add_vcpupin, font=('', 8)
        ).pack(side='left', padx=5)
        row += 1

        # vCPU Pin 列表容器
        self.vcpupin_list_frame = ctk.CTkScrollableFrame(parent, fg_color='transparent', height=60)
        self.vcpupin_list_frame.grid(row=row, column=0, padx=5, pady=2, sticky='ew')
        row += 1

        # emulatorpin
        ctk.CTkLabel(parent, text='模拟器 Pin:', font=('', 9)).grid(
            row=row, column=0, padx=5, pady=(8, 2), sticky='w'
        )
        row += 1

        emu_frame = ctk.CTkFrame(parent, fg_color='transparent')
        emu_frame.grid(row=row, column=0, padx=5, pady=2, sticky='ew')
        self.emulatorpin_none = ctk.CTkCheckBox(emu_frame, text='None', font=('', 8))
        self.emulatorpin_none.pack(side='left', padx=2)
        self.emulatorpin_none.configure(command=self._on_emulatorpin_none_change)

        self.emulatorpin = ctk.CTkEntry(emu_frame, width=80, font=('', 8))
        self.emulatorpin.pack(side='left', padx=5)
        self.emulatorpin.insert(0, '')
        self.emulatorpin.bind('<KeyRelease>', lambda e: self._trigger_change())
        self.emulatorpin_state = 'enabled'
        row += 1

        # IOThread Pin
        ctk.CTkLabel(parent, text='IOThread Pin:', font=('', 9)).grid(
            row=row, column=0, padx=5, pady=(8, 2), sticky='w'
        )
        row += 1

        self.iothreadpin_frame = ctk.CTkFrame(parent, fg_color='transparent')
        self.iothreadpin_frame.grid(row=row, column=0, padx=5, pady=2, sticky='ew')
        self.iothreadpin_entries = []

        io_entry_row = ctk.CTkFrame(self.iothreadpin_frame, fg_color='transparent')
        io_entry_row.pack(fill='x')
        ctk.CTkLabel(io_entry_row, text='IOThread:', font=('', 8), width=50).pack(side='left')
        self.iothreadpin_add_id = ctk.CTkEntry(io_entry_row, width=35, font=('', 8))
        self.iothreadpin_add_id.pack(side='left', padx=2)

        ctk.CTkLabel(io_entry_row, text='CPUs:', font=('', 8), width=35).pack(
            side='left', padx=(5, 2)
        )
        self.iothreadpin_add_cpuset = ctk.CTkEntry(io_entry_row, width=60, font=('', 8))
        self.iothreadpin_add_cpuset.pack(side='left', padx=2)

        ctk.CTkButton(
            io_entry_row, text='+', width=25, height=20, command=self._add_iothreadpin, font=('', 8)
        ).pack(side='left', padx=5)
        row += 1

        # IOThread Pin 列表容器
        self.iothreadpin_list_frame = ctk.CTkScrollableFrame(
            parent, fg_color='transparent', height=60
        )
        self.iothreadpin_list_frame.grid(row=row, column=0, padx=5, pady=2, sticky='ew')

    def _create_section_header(
        self, parent: ctk.CTkFrame, title: str, row: int, color: str
    ) -> None:
        """创建分组标题."""
        ctk.CTkLabel(parent, text=title, font=('', 11, 'bold'), text_color=color).grid(
            row=row, column=0, columnspan=5, padx=10, pady=(8, 4), sticky='w'
        )

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

        # 添加到滚动框架中
        row_frame = ctk.CTkFrame(self.vcpupin_list_frame, fg_color='#2a2a2a', corner_radius=4)
        row_frame.pack(side='left', padx=3, pady=2, anchor='n')

        ctk.CTkLabel(row_frame, text='vCPU', font=('', 8), width=28, anchor='w').pack(
            side='left', padx=2
        )
        id_entry = ctk.CTkEntry(row_frame, width=35, font=('', 8))
        id_entry.insert(0, vcpu_id)
        id_entry.pack(side='left', padx=1)
        id_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(row_frame, text='CPUs', font=('', 8), width=28, anchor='w').pack(
            side='left', padx=(2, 1)
        )
        cpuset_entry = ctk.CTkEntry(row_frame, width=60, font=('', 8))
        cpuset_entry.insert(0, cpuset)
        cpuset_entry.pack(side='left', padx=1)
        cpuset_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        del_btn = ctk.CTkButton(
            row_frame,
            text='×',
            width=20,
            height=18,
            command=lambda: self._remove_vcpupin(row_frame, id_entry, cpuset_entry),
            font=('', 8),
        )
        del_btn.pack(side='left', padx=2)

        self.vcpupin_entries.append((id_entry, cpuset_entry))
        self._trigger_change()

        # 清空输入框
        self.vcpupin_add_id.delete(0, 'end')
        self.vcpupin_add_cpuset.delete(0, 'end')

    def _remove_vcpupin(self, frame, id_entry, cpuset_entry) -> None:
        """删除一个 vCPU Pin 配置."""
        frame.destroy()
        self.vcpupin_entries.remove((id_entry, cpuset_entry))
        self._trigger_change()

    def _on_emulatorpin_none_change(self) -> None:
        """处理 emulatorpin None 复选框变化."""
        if self.emulatorpin_none.get():
            self.emulatorpin.configure(state='disabled')
            self.emulatorpin_state = 'disabled'
        else:
            self.emulatorpin.configure(state='normal')
            self.emulatorpin_state = 'enabled'
        self._trigger_change()

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

        # 添加到滚动框架中
        row_frame = ctk.CTkFrame(self.iothreadpin_list_frame, fg_color='#2a2a2a', corner_radius=4)
        row_frame.pack(side='left', padx=3, pady=2, anchor='n')

        ctk.CTkLabel(row_frame, text='IOThread', font=('', 8), width=40, anchor='w').pack(
            side='left', padx=2
        )
        id_entry = ctk.CTkEntry(row_frame, width=35, font=('', 8))
        id_entry.insert(0, iothread_id)
        id_entry.pack(side='left', padx=1)
        id_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(row_frame, text='CPUs', font=('', 8), width=28, anchor='w').pack(
            side='left', padx=(2, 1)
        )
        cpuset_entry = ctk.CTkEntry(row_frame, width=60, font=('', 8))
        cpuset_entry.insert(0, cpuset)
        cpuset_entry.pack(side='left', padx=1)
        cpuset_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        del_btn = ctk.CTkButton(
            row_frame,
            text='x',
            width=20,
            height=18,
            command=lambda: self._remove_iothreadpin(row_frame, id_entry, cpuset_entry),
            font=('', 8),
        )
        del_btn.pack(side='left', padx=2)

        self.iothreadpin_entries.append((id_entry, cpuset_entry))
        self._trigger_change()

        # 清空输入框
        self.iothreadpin_add_id.delete(0, 'end')
        self.iothreadpin_add_cpuset.delete(0, 'end')

    def _remove_iothreadpin(self, frame, id_entry, cpuset_entry) -> None:
        """删除一个 IOThread Pin 配置."""
        frame.destroy()
        self.iothreadpin_entries.remove((id_entry, cpuset_entry))
        self._trigger_change()

    # ========== CPU 带宽控制 ==========
    def _create_bandwidth_section(self, parent: ctk.CTkFrame, row: int) -> None:
        """创建第 2 列：CPU 带宽控制."""
        # 标题
        ctk.CTkLabel(parent, text='CPU 带宽控制', font=('', 11, 'bold'), text_color='#4caf50').grid(
            row=row, column=0, padx=10, pady=8, sticky='w'
        )
        row += 1

        # 第一行：shares, period, quota, global_period (4 个)
        row_frame = ctk.CTkFrame(parent, fg_color='transparent')
        row_frame.grid(row=row, column=0, padx=5, pady=3, sticky='ew')
        row_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # shares
        ctk.CTkLabel(row_frame, text='份额:', font=('', 8)).grid(row=0, column=0, padx=2, pady=1, sticky='w')
        self.shares = ctk.CTkEntry(row_frame, width=70, font=('', 8))
        self.shares.grid(row=1, column=0, padx=2, pady=2, sticky='ew')
        self.shares.insert(0, '')
        self.shares.bind('<KeyRelease>', lambda e: self._trigger_change())

        # period
        ctk.CTkLabel(row_frame, text='周期 (μs):', font=('', 8)).grid(row=0, column=1, padx=2, pady=1, sticky='w')
        self.period = ctk.CTkEntry(row_frame, width=70, font=('', 8))
        self.period.grid(row=1, column=1, padx=2, pady=2, sticky='ew')
        self.period.insert(0, '')
        self.period.bind('<KeyRelease>', lambda e: self._trigger_change())

        # quota
        ctk.CTkLabel(row_frame, text='配额 (μs):', font=('', 8)).grid(row=0, column=2, padx=2, pady=1, sticky='w')
        self.quota = ctk.CTkEntry(row_frame, width=70, font=('', 8))
        self.quota.grid(row=1, column=2, padx=2, pady=2, sticky='ew')
        self.quota.insert(0, '')
        self.quota.bind('<KeyRelease>', lambda e: self._trigger_change())

        # global_period
        ctk.CTkLabel(row_frame, text='全局周期 (μs):', font=('', 8)).grid(row=0, column=3, padx=2, pady=1, sticky='w')
        self.global_period = ctk.CTkEntry(row_frame, width=70, font=('', 8))
        self.global_period.grid(row=1, column=3, padx=2, pady=2, sticky='ew')
        self.global_period.insert(0, '')
        self.global_period.bind('<KeyRelease>', lambda e: self._trigger_change())
        row += 1

        # 第二行：global_quota, emulator_period, emulator_quota, iothread_period (4 个)
        row_frame2 = ctk.CTkFrame(parent, fg_color='transparent')
        row_frame2.grid(row=row, column=0, padx=5, pady=3, sticky='ew')
        row_frame2.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # global_quota
        ctk.CTkLabel(row_frame2, text='全局配额 (μs):', font=('', 8)).grid(row=0, column=0, padx=2, pady=1, sticky='w')
        self.global_quota = ctk.CTkEntry(row_frame2, width=70, font=('', 8))
        self.global_quota.grid(row=1, column=0, padx=2, pady=2, sticky='ew')
        self.global_quota.insert(0, '')
        self.global_quota.bind('<KeyRelease>', lambda e: self._trigger_change())

        # emulator_period
        ctk.CTkLabel(row_frame2, text='模拟器周期 (μs):', font=('', 8)).grid(row=0, column=1, padx=2, pady=1, sticky='w')
        self.emulator_period = ctk.CTkEntry(row_frame2, width=70, font=('', 8))
        self.emulator_period.grid(row=1, column=1, padx=2, pady=2, sticky='ew')
        self.emulator_period.insert(0, '')
        self.emulator_period.bind('<KeyRelease>', lambda e: self._trigger_change())

        # emulator_quota
        ctk.CTkLabel(row_frame2, text='模拟器配额 (μs):', font=('', 8)).grid(row=0, column=2, padx=2, pady=1, sticky='w')
        self.emulator_quota = ctk.CTkEntry(row_frame2, width=70, font=('', 8))
        self.emulator_quota.grid(row=1, column=2, padx=2, pady=2, sticky='ew')
        self.emulator_quota.insert(0, '')
        self.emulator_quota.bind('<KeyRelease>', lambda e: self._trigger_change())

        # iothread_period
        ctk.CTkLabel(row_frame2, text='IOThread 周期 (μs):', font=('', 8)).grid(row=0, column=3, padx=2, pady=1, sticky='w')
        self.iothread_period = ctk.CTkEntry(row_frame2, width=70, font=('', 8))
        self.iothread_period.grid(row=1, column=3, padx=2, pady=2, sticky='ew')
        self.iothread_period.insert(0, '')
        self.iothread_period.bind('<KeyRelease>', lambda e: self._trigger_change())
        row += 1

        # 第三行：iothread_quota (单独一个)
        ctk.CTkLabel(parent, text='IOThread 配额 (μs):', font=('', 8)).grid(
            row=row, column=0, padx=5, pady=1, sticky='w'
        )
        self.iothread_quota = ctk.CTkEntry(parent, width=120, font=('', 8))
        self.iothread_quota.grid(row=row + 1, column=0, padx=5, pady=2, sticky='ew')
        self.iothread_quota.insert(0, '')
        self.iothread_quota.bind('<KeyRelease>', lambda e: self._trigger_change())

    # ========== 调度器配置 ==========
    def _create_scheduler_section(self, parent: ctk.CTkFrame, row: int) -> None:
        """创建第 3 列：调度器配置."""
        # 标题
        ctk.CTkLabel(parent, text='调度器配置', font=('', 11, 'bold'), text_color='#ff9800').grid(
            row=row, column=0, padx=10, pady=8, sticky='w'
        )
        row += 1

        # vcpusched
        ctk.CTkLabel(parent, text='vCPU 调度器:', font=('', 9)).grid(
            row=row, column=0, padx=5, pady=2, sticky='w'
        )
        row += 1

        vs_frame = ctk.CTkFrame(parent, fg_color='transparent')
        vs_frame.grid(row=row, column=0, padx=5, pady=2, sticky='ew')
        self.vcpusched_none = ctk.CTkCheckBox(vs_frame, text='None', font=('', 8))
        self.vcpusched_none.pack(side='left', padx=2)
        self.vcpusched_none.configure(command=self._on_vcpusched_none_change)
        row += 1

        vs_frame2 = ctk.CTkFrame(parent, fg_color='transparent')
        vs_frame2.grid(row=row, column=0, padx=5, pady=2, sticky='ew')
        ctk.CTkLabel(vs_frame2, text='vCPUs:', font=('', 8), width=40).pack(side='left')
        self.vcpusched_vcpus = ctk.CTkEntry(vs_frame2, width=70, font=('', 8))
        self.vcpusched_vcpus.pack(side='left', padx=2)
        self.vcpusched_vcpus.insert(0, '')
        self.vcpusched_vcpus.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(vs_frame2, text='调度器:', font=('', 8), width=40).pack(
            side='left', padx=(5, 2)
        )
        self.vcpusched_scheduler = ctk.CTkOptionMenu(
            vs_frame2, values=['batch', 'idle', 'fifo', 'rr'], width=50, font=('', 8)
        )
        self.vcpusched_scheduler.set('batch')
        self.vcpusched_scheduler.pack(side='left', padx=2)
        self.vcpusched_scheduler.configure(command=self._on_vcpusched_scheduler_change)
        row += 1

        vs_frame3 = ctk.CTkFrame(parent, fg_color='transparent')
        vs_frame3.grid(row=row, column=0, padx=5, pady=2, sticky='ew')
        ctk.CTkLabel(vs_frame3, text='优先级:', font=('', 8), width=40).pack(side='left')
        self.vcpusched_priority = ctk.CTkEntry(vs_frame3, width=70, font=('', 8))
        self.vcpusched_priority.pack(side='left', padx=2)
        self.vcpusched_priority.insert(0, '')
        self.vcpusched_priority.bind('<KeyRelease>', lambda e: self._trigger_change())
        self.vcpusched_state = 'enabled'
        row += 1

        # iothreadsched
        ctk.CTkLabel(parent, text='IOThread 调度器:', font=('', 9)).grid(
            row=row, column=0, padx=5, pady=(8, 2), sticky='w'
        )
        row += 1

        ios_frame = ctk.CTkFrame(parent, fg_color='transparent')
        ios_frame.grid(row=row, column=0, padx=5, pady=2, sticky='ew')
        self.iothreadsched_none = ctk.CTkCheckBox(ios_frame, text='None', font=('', 8))
        self.iothreadsched_none.pack(side='left', padx=2)
        self.iothreadsched_none.configure(command=self._on_iothreadsched_none_change)
        row += 1

        ioss_frame2 = ctk.CTkFrame(parent, fg_color='transparent')
        ioss_frame2.grid(row=row, column=0, padx=5, pady=2, sticky='ew')
        ctk.CTkLabel(ioss_frame2, text='IOThreads:', font=('', 8), width=50).pack(side='left')
        self.iothreadsched_iothreads = ctk.CTkEntry(ioss_frame2, width=60, font=('', 8))
        self.iothreadsched_iothreads.pack(side='left', padx=2)
        self.iothreadsched_iothreads.insert(0, '')
        self.iothreadsched_iothreads.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(ioss_frame2, text='调度器:', font=('', 8), width=40).pack(
            side='left', padx=(5, 2)
        )
        self.iothreadsched_scheduler = ctk.CTkOptionMenu(
            ioss_frame2, values=['batch', 'idle', 'fifo', 'rr'], width=50, font=('', 8)
        )
        self.iothreadsched_scheduler.set('batch')
        self.iothreadsched_scheduler.pack(side='left', padx=2)
        self.iothreadsched_scheduler.configure(command=self._on_iothreadsched_scheduler_change)
        row += 1

        ios_frame3 = ctk.CTkFrame(parent, fg_color='transparent')
        ios_frame3.grid(row=row, column=0, padx=5, pady=2, sticky='ew')
        ctk.CTkLabel(ios_frame3, text='优先级:', font=('', 8), width=40).pack(side='left')
        self.iothreadsched_priority = ctk.CTkEntry(ios_frame3, width=70, font=('', 8))
        self.iothreadsched_priority.pack(side='left', padx=2)
        self.iothreadsched_priority.insert(0, '')
        self.iothreadsched_priority.bind('<KeyRelease>', lambda e: self._trigger_change())
        self.iothreadsched_state = 'enabled'
        row += 1

        # emulatorsched
        ctk.CTkLabel(parent, text='模拟器调度器:', font=('', 9)).grid(
            row=row, column=0, padx=5, pady=(8, 2), sticky='w'
        )
        row += 1

        es_frame = ctk.CTkFrame(parent, fg_color='transparent')
        es_frame.grid(row=row, column=0, padx=5, pady=2, sticky='ew')
        self.emulatorsched_none = ctk.CTkCheckBox(es_frame, text='None', font=('', 8))
        self.emulatorsched_none.pack(side='left', padx=2)
        self.emulatorsched_none.configure(command=self._on_emulatorsched_none_change)
        row += 1

        es_frame2 = ctk.CTkFrame(parent, fg_color='transparent')
        es_frame2.grid(row=row, column=0, padx=5, pady=2, sticky='ew')
        ctk.CTkLabel(es_frame2, text='调度器:', font=('', 8), width=50).pack(side='left')
        self.emulatorsched_scheduler = ctk.CTkOptionMenu(
            es_frame2, values=['batch', 'idle', 'fifo', 'rr'], width=60, font=('', 8)
        )
        self.emulatorsched_scheduler.set('batch')
        self.emulatorsched_scheduler.pack(side='left', padx=2)
        self.emulatorsched_scheduler.configure(command=self._on_emulatorsched_scheduler_change)

        ctk.CTkLabel(es_frame2, text='优先级:', font=('', 8), width=40).pack(
            side='left', padx=(5, 2)
        )
        self.emulatorsched_priority = ctk.CTkEntry(es_frame2, width=60, font=('', 8))
        self.emulatorsched_priority.pack(side='left', padx=2)
        self.emulatorsched_priority.insert(0, '')
        self.emulatorsched_priority.bind('<KeyRelease>', lambda e: self._trigger_change())
        self.emulatorsched_state = 'enabled'

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
        """创建第 4 列：缓存调优."""
        # 标题
        ctk.CTkLabel(parent, text='缓存调优', font=('', 11, 'bold'), text_color='#9c27b0').grid(
            row=row, column=0, padx=10, pady=8, sticky='w'
        )
        row += 1

        # 添加按钮
        ctk.CTkButton(
            parent,
            text='+ CacheTune',
            width=100,
            height=25,
            command=self._add_cachetune,
            font=('', 9),
        ).grid(row=row, column=0, padx=10, pady=5, sticky='w')
        row += 1

        # Cachetune 列表容器
        self.cachetune_scroll_frame = ctk.CTkScrollableFrame(
            parent, fg_color='transparent', height=150
        )
        self.cachetune_scroll_frame.grid(row=row, column=0, padx=5, pady=2, sticky='nsew')
        self.cachetune_entries = []

    def _add_cachetune(self) -> None:
        """添加一个 cachetune 配置组."""
        frame = ctk.CTkFrame(self.cachetune_scroll_frame, fg_color='#2a2a2a', corner_radius=4)
        frame.pack(side='left', padx=5, pady=3, anchor='n')

        # 第一行：vcpus 和删除按钮
        top_row = ctk.CTkFrame(frame, fg_color='transparent')
        top_row.pack(fill='x', padx=5, pady=2)

        ctk.CTkLabel(top_row, text='vCPUs:', font=('', 8), width=35, anchor='w').pack(side='left')
        vcpus_entry = ctk.CTkEntry(top_row, width=60, font=('', 8))
        vcpus_entry.insert(0, '')
        vcpus_entry.pack(side='left', padx=2)
        vcpus_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        del_btn = ctk.CTkButton(
            top_row,
            text='×',
            width=24,
            height=18,
            command=lambda: self._remove_cachetune(frame),
            font=('', 8),
        )
        del_btn.pack(side='left', padx=5)

        # 第二行：cache 配置
        cache_row = ctk.CTkFrame(frame, fg_color='transparent')
        cache_row.pack(fill='x', padx=5, pady=1)

        ctk.CTkLabel(cache_row, text='Cache:', font=('', 8), width=35, anchor='w').pack(side='left')
        ctk.CTkLabel(cache_row, text='L:', font=('', 8), width=15, anchor='w').pack(
            side='left', padx=(5, 1)
        )
        cache_level = ctk.CTkOptionMenu(cache_row, values=['1', '2', '3'], width=35, font=('', 8))
        cache_level.set('3')
        cache_level.pack(side='left', padx=1)
        cache_level.configure(command=lambda e: self._trigger_change())

        ctk.CTkLabel(cache_row, text='T:', font=('', 8), width=12, anchor='w').pack(
            side='left', padx=(3, 1)
        )
        cache_type = ctk.CTkOptionMenu(
            cache_row, values=['code', 'data', 'both'], width=45, font=('', 8)
        )
        cache_type.set('both')
        cache_type.pack(side='left', padx=1)
        cache_type.configure(command=lambda e: self._trigger_change())

        ctk.CTkLabel(cache_row, text='S:', font=('', 8), width=12, anchor='w').pack(
            side='left', padx=(3, 1)
        )
        cache_size = ctk.CTkEntry(cache_row, width=35, font=('', 8))
        cache_size.insert(0, '')
        cache_size.pack(side='left', padx=1)
        cache_size.bind('<KeyRelease>', lambda e: self._trigger_change())

        cache_unit = ctk.CTkOptionMenu(
            cache_row, values=['KiB', 'MiB', 'GiB'], width=38, font=('', 8)
        )
        cache_unit.set('MiB')
        cache_unit.pack(side='left', padx=1)
        cache_unit.configure(command=lambda e: self._trigger_change())

        # 第三行：monitor 配置
        monitor_row = ctk.CTkFrame(frame, fg_color='transparent')
        monitor_row.pack(fill='x', padx=5, pady=1)

        ctk.CTkLabel(monitor_row, text='Mon:', font=('', 8), width=35, anchor='w').pack(side='left')
        ctk.CTkLabel(monitor_row, text='vCPUs:', font=('', 8), width=35, anchor='w').pack(
            side='left', padx=(2, 1)
        )
        monitor_vcpus = ctk.CTkEntry(monitor_row, width=50, font=('', 8))
        monitor_vcpus.insert(0, '')
        monitor_vcpus.pack(side='left', padx=1)
        monitor_vcpus.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(monitor_row, text='L:', font=('', 8), width=15, anchor='w').pack(
            side='left', padx=(5, 1)
        )
        monitor_level = ctk.CTkOptionMenu(
            monitor_row, values=['1', '2', '3'], width=35, font=('', 8)
        )
        monitor_level.set('3')
        monitor_level.pack(side='left', padx=1)
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
        """创建第 5 列：内存带宽调优."""
        # 标题
        ctk.CTkLabel(parent, text='内存带宽调优', font=('', 11, 'bold'), text_color='#e91e63').grid(
            row=row, column=0, padx=10, pady=8, sticky='w'
        )
        row += 1

        # 添加按钮
        ctk.CTkButton(
            parent,
            text='+ MemoryTune',
            width=100,
            height=25,
            command=self._add_memorytune,
            font=('', 9),
        ).grid(row=row, column=0, padx=10, pady=5, sticky='w')
        row += 1

        # MemoryTune 列表容器
        self.memorytune_scroll_frame = ctk.CTkScrollableFrame(
            parent, fg_color='transparent', height=100
        )
        self.memorytune_scroll_frame.grid(row=row, column=0, padx=5, pady=2, sticky='nsew')
        self.memorytune_entries = []

    def _add_memorytune(self) -> None:
        """添加一个 memorytune 配置组."""
        frame = ctk.CTkFrame(self.memorytune_scroll_frame, fg_color='#2a2a2a', corner_radius=4)
        frame.pack(side='left', padx=5, pady=3, anchor='n')

        # 第一行：vcpus 和删除按钮
        top_row = ctk.CTkFrame(frame, fg_color='transparent')
        top_row.pack(fill='x', padx=5, pady=2)

        ctk.CTkLabel(top_row, text='vCPUs:', font=('', 8), width=35, anchor='w').pack(side='left')
        vcpus_entry = ctk.CTkEntry(top_row, width=60, font=('', 8))
        vcpus_entry.insert(0, '')
        vcpus_entry.pack(side='left', padx=2)
        vcpus_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        del_btn = ctk.CTkButton(
            top_row,
            text='×',
            width=24,
            height=18,
            command=lambda: self._remove_memorytune(frame),
            font=('', 8),
        )
        del_btn.pack(side='left', padx=5)

        # 第二行：node 配置
        node_row = ctk.CTkFrame(frame, fg_color='transparent')
        node_row.pack(fill='x', padx=5, pady=1)

        ctk.CTkLabel(node_row, text='Node:', font=('', 8), width=35, anchor='w').pack(side='left')
        node_id = ctk.CTkEntry(node_row, width=35, font=('', 8))
        node_id.insert(0, '')
        node_id.pack(side='left', padx=2)
        node_id.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(node_row, text='Bandwidth (%):', font=('', 8), width=75, anchor='w').pack(
            side='left', padx=(5, 2)
        )
        bandwidth = ctk.CTkEntry(node_row, width=40, font=('', 8))
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

        # vcpusched - 只有在启用且 vcpus 有值时才生成
        if self.vcpusched_state == 'enabled':
            vcpus = self.vcpusched_vcpus.get().strip()
            if vcpus:  # 只有 vcpus 有值时才生成配置
                vcpusched = {}
                vcpusched['vcpus'] = vcpus
                scheduler = self.vcpusched_scheduler.get()
                vcpusched['scheduler'] = scheduler
                priority = self.vcpusched_priority.get().strip()
                if priority and scheduler in ('fifo', 'rr'):
                    vcpusched['priority'] = int(priority)
                if vcpusched:
                    config['vcpusched'] = vcpusched

        # iothreadsched - 只有在启用且 iothreads 有值时才生成
        if self.iothreadsched_state == 'enabled':
            iothreads = self.iothreadsched_iothreads.get().strip()
            if iothreads:  # 只有 iothreads 有值时才生成配置
                iothreadsched = {}
                iothreadsched['iothreads'] = iothreads
                scheduler = self.iothreadsched_scheduler.get()
                iothreadsched['scheduler'] = scheduler
                priority = self.iothreadsched_priority.get().strip()
                if priority and scheduler in ('fifo', 'rr'):
                    iothreadsched['priority'] = int(priority)
                # 至少要有 scheduler 且不是默认值 batch
                if iothreadsched.get('scheduler') and iothreadsched['scheduler'] != 'batch':
                    config['iothreadsched'] = iothreadsched

        # emulatorsched - 只有在启用时才生成
        if self.emulatorsched_state == 'enabled':
            emulatorsched = {}
            scheduler = self.emulatorsched_scheduler.get()
            emulatorsched['scheduler'] = scheduler
            priority = self.emulatorsched_priority.get().strip()
            if priority and scheduler in ('fifo', 'rr'):
                emulatorsched['priority'] = int(priority)
            # 至少要有 scheduler 且不是默认值 batch
            if emulatorsched.get('scheduler') and emulatorsched['scheduler'] != 'batch':
                config['emulatorsched'] = emulatorsched

        # cachetune - 只有 vcpus 有值时才生成
        cachetunes = []
        for entry in self.cachetune_entries:
            ct = {}
            vcpus = entry['vcpus'].get().strip()
            if not vcpus:
                continue  # vcpus 为空时跳过此条目

            ct['vcpus'] = vcpus

            cache = {}
            cache['level'] = int(entry['cache_level'].get())
            cache['type'] = entry['cache_type'].get()
            cache_size = entry['cache_size'].get().strip()
            if cache_size:
                cache['size'] = int(cache_size)
            cache['unit'] = entry['cache_unit'].get()
            ct['cache'] = cache

            monitor = {}
            monitor_vcpus = entry['monitor_vcpus'].get().strip()
            if monitor_vcpus:
                monitor['vcpus'] = monitor_vcpus
            monitor['level'] = int(entry['monitor_level'].get())
            ct['monitor'] = monitor

            if ct:
                cachetunes.append(ct)
        if cachetunes:
            config['cachetune'] = cachetunes

        # memorytune - 只有 vcpus 有值时才生成
        memorytunes = []
        for entry in self.memorytune_entries:
            vcpus = entry['vcpus'].get().strip()
            if not vcpus:
                continue  # vcpus 为空时跳过此条目

            mt = {}
            mt['vcpus'] = vcpus

            node = {}
            node_id = entry['node_id'].get().strip()
            if node_id:
                node['id'] = int(node_id)
            bandwidth = entry['bandwidth'].get().strip()
            if bandwidth:
                node['bandwidth'] = int(bandwidth)
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
