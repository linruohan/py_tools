"""CPU 调优配置 Tab - CPU Tuning (cputune).

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

from typing import Any

import customtkinter as ctk

from components.base_tab import BaseConfigTab


class CPUTuningTab(BaseConfigTab):
    """CPU 调优配置 Tab - 5 列布局实现完整的 cputune 配置."""

    def _init_ui(self) -> None:
        """初始化 UI - 5 列布局."""
        # 先初始化列表，避免在创建 UI 时访问未定义的属性
        self.vcpupin_entries: list[
            tuple[ctk.CTkEntry, ctk.CTkEntry, ctk.CTkFrame]
        ] = []  # [(id_entry, cpuset_entry, frame), ...]
        self.iothreadpin_entries: list[
            tuple[ctk.CTkEntry, ctk.CTkEntry, ctk.CTkFrame]
        ] = []  # [(id_entry, cpuset_entry, frame), ...]
        self.cachetune_entries: list[dict[str, Any]] = []
        self.memorytune_entries: list[dict[str, Any]] = []

        # 主框架使用网格布局
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 创建 5 列主容器
        main_container = ctk.CTkFrame(self, fg_color='transparent')
        main_container.grid(row=0, column=0, sticky='nsew')
        main_container.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        # === 第 1 列：CPU 亲和性 ===
        self.affinity_frame = ctk.CTkFrame(main_container, fg_color='#1a1a1a', corner_radius=8)
        self.affinity_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        self.affinity_frame.grid_columnconfigure(0, weight=1)
        self._create_affinity_section(self.affinity_frame)

        # === 第 2 列：CPU 带宽控制 ===
        self.bandwidth_frame = ctk.CTkFrame(main_container, fg_color='#1a1a1a', corner_radius=8)
        self.bandwidth_frame.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
        self.bandwidth_frame.grid_columnconfigure(0, weight=1)
        self._create_bandwidth_section(self.bandwidth_frame)

        # === 第 3 列：调度器配置 ===
        self.scheduler_frame = ctk.CTkFrame(main_container, fg_color='#1a1a1a', corner_radius=8)
        self.scheduler_frame.grid(row=0, column=2, padx=5, pady=5, sticky='nsew')
        self.scheduler_frame.grid_columnconfigure(0, weight=1)
        self._create_scheduler_section(self.scheduler_frame)

        # === 第 4 列：缓存调优 ===
        self.cachetune_frame = ctk.CTkFrame(main_container, fg_color='#1a1a1a', corner_radius=8)
        self.cachetune_frame.grid(row=0, column=3, padx=5, pady=5, sticky='nsew')
        self.cachetune_frame.grid_columnconfigure(0, weight=1)
        self._create_cachetune_section(self.cachetune_frame)

        # === 第 5 列：内存带宽调优 ===
        self.memorytune_frame = ctk.CTkFrame(main_container, fg_color='#1a1a1a', corner_radius=8)
        self.memorytune_frame.grid(row=0, column=4, padx=5, pady=5, sticky='nsew')
        self.memorytune_frame.grid_columnconfigure(0, weight=1)
        self._create_memorytune_section(self.memorytune_frame)

    def _create_affinity_section(self, parent: ctk.CTkFrame) -> None:
        """创建第 1 列：CPU 亲和性."""
        row = 0

        # 标题
        ctk.CTkLabel(
            parent,
            text='CPU 亲和性',
            font=ctk.CTkFont(family='', size=11, weight='bold'),
            text_color='#FFD93D',
        ).grid(row=row, column=0, padx=10, pady=8, sticky='w')
        row += 1

        # === 第一组：vCPU Pin ===
        vcpu_header_frame = ctk.CTkFrame(parent, fg_color='transparent')
        vcpu_header_frame.grid(row=row, column=0, padx=10, pady=2, sticky='ew')
        ctk.CTkLabel(vcpu_header_frame, text='vCPU Pin:', font=ctk.CTkFont(size=9)).pack(
            side='left'
        )

        vcpupin_add_btn = ctk.CTkButton(
            vcpu_header_frame,
            text='+',
            width=25,
            height=20,
            command=self._add_vcpupin,
            font=ctk.CTkFont(size=8),
        )
        vcpupin_add_btn.pack(side='right', padx=2)
        vcpupin_remove_btn = ctk.CTkButton(
            vcpu_header_frame,
            text='-',
            width=25,
            height=20,
            command=self._remove_vcpupin,
            font=ctk.CTkFont(size=8),
        )
        vcpupin_remove_btn.pack(side='right', padx=2)
        row += 1

        # vCPU Pin 列表容器
        self.vcpupin_list_frame = ctk.CTkFrame(parent, fg_color='transparent')
        self.vcpupin_list_frame.grid(row=row, column=0, padx=10, pady=2, sticky='ew')
        parent.grid_rowconfigure(row, weight=1)
        row += 1

        # === 第二组：模拟器 Pin ===
        emu_header_frame = ctk.CTkFrame(parent, fg_color='transparent')
        emu_header_frame.grid(row=row, column=0, padx=10, pady=2, sticky='ew')
        ctk.CTkLabel(emu_header_frame, text='模拟器 Pin:', font=ctk.CTkFont(size=9)).pack(
            side='left'
        )

        self.emulatorpin_none = ctk.CTkCheckBox(
            emu_header_frame, text='None', font=ctk.CTkFont(size=8)
        )
        self.emulatorpin_none.pack(side='right', padx=5)
        self.emulatorpin_none.configure(command=self._on_emulatorpin_none_change)

        self.emulatorpin = ctk.CTkEntry(emu_header_frame, width=100, font=ctk.CTkFont(size=8))
        self.emulatorpin.pack(side='right', padx=5)
        self.emulatorpin.insert(0, '')
        self.emulatorpin.configure(placeholder_text='例如: 0-3,5')
        self.emulatorpin.bind('<KeyRelease>', lambda e: self._trigger_change())
        self.emulatorpin_state = 'enabled'
        row += 1

        # === 第三组：IOThread Pin ===
        io_header_frame = ctk.CTkFrame(parent, fg_color='transparent')
        io_header_frame.grid(row=row, column=0, padx=10, pady=2, sticky='ew')
        ctk.CTkLabel(io_header_frame, text='IOThread Pin:', font=ctk.CTkFont(size=9)).pack(
            side='left'
        )

        iothreadpin_add_btn = ctk.CTkButton(
            io_header_frame,
            text='+',
            width=25,
            height=20,
            command=self._add_iothreadpin,
            font=ctk.CTkFont(size=8),
        )
        iothreadpin_add_btn.pack(side='right', padx=2)
        iothreadpin_remove_btn = ctk.CTkButton(
            io_header_frame,
            text='-',
            width=25,
            height=20,
            command=self._remove_iothreadpin_last,
            font=ctk.CTkFont(size=8),
        )
        iothreadpin_remove_btn.pack(side='right', padx=2)
        row += 1

        # IOThread Pin 列表容器
        self.iothreadpin_list_frame = ctk.CTkFrame(parent, fg_color='transparent')
        self.iothreadpin_list_frame.grid(row=row, column=0, padx=10, pady=2, sticky='ew')
        parent.grid_rowconfigure(row, weight=1)

        # 初始检查列表状态
        self._update_frame_visibility()

    def _create_bandwidth_section(self, parent: ctk.CTkFrame) -> None:
        """创建第 2 列：CPU 带宽控制."""
        row = 0

        # 标题
        ctk.CTkLabel(
            parent,
            text='CPU 带宽控制',
            font=ctk.CTkFont(family='', size=11, weight='bold'),
            text_color='#4caf50',
        ).grid(row=row, column=0, padx=10, pady=8, sticky='w')
        row += 1

        # 第一行：shares, period, quota, global_period (4 个)
        row_frame = ctk.CTkFrame(parent, fg_color='transparent')
        row_frame.grid(row=row, column=0, padx=5, pady=3, sticky='ew')
        row_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # shares
        ctk.CTkLabel(row_frame, text='份额:', font=ctk.CTkFont(size=8)).grid(
            row=0, column=0, padx=2, pady=1, sticky='w'
        )
        self.shares = ctk.CTkEntry(row_frame, width=70, font=ctk.CTkFont(size=8))
        self.shares.grid(row=1, column=0, padx=2, pady=2, sticky='ew')
        self.shares.insert(0, '')
        self.shares.bind('<KeyRelease>', lambda e: self._trigger_change())

        # period
        ctk.CTkLabel(row_frame, text='周期 (μs):', font=ctk.CTkFont(size=8)).grid(
            row=0, column=1, padx=2, pady=1, sticky='w'
        )
        self.period = ctk.CTkEntry(row_frame, width=70, font=ctk.CTkFont(size=8))
        self.period.grid(row=1, column=1, padx=2, pady=2, sticky='ew')
        self.period.insert(0, '')
        self.period.bind('<KeyRelease>', lambda e: self._trigger_change())

        # quota
        ctk.CTkLabel(row_frame, text='配额 (μs):', font=ctk.CTkFont(size=8)).grid(
            row=0, column=2, padx=2, pady=1, sticky='w'
        )
        self.quota = ctk.CTkEntry(row_frame, width=70, font=ctk.CTkFont(size=8))
        self.quota.grid(row=1, column=2, padx=2, pady=2, sticky='ew')
        self.quota.insert(0, '')
        self.quota.bind('<KeyRelease>', lambda e: self._trigger_change())

        # global_period
        ctk.CTkLabel(row_frame, text='全局周期 (μs):', font=ctk.CTkFont(size=8)).grid(
            row=0, column=3, padx=2, pady=1, sticky='w'
        )
        self.global_period = ctk.CTkEntry(row_frame, width=70, font=ctk.CTkFont(size=8))
        self.global_period.grid(row=1, column=3, padx=2, pady=2, sticky='ew')
        self.global_period.insert(0, '')
        self.global_period.bind('<KeyRelease>', lambda e: self._trigger_change())
        row += 1

        # 第二行：global_quota, emulator_period, emulator_quota, iothread_period (4 个)
        row_frame2 = ctk.CTkFrame(parent, fg_color='transparent')
        row_frame2.grid(row=row, column=0, padx=5, pady=3, sticky='ew')
        row_frame2.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # global_quota
        ctk.CTkLabel(row_frame2, text='全局配额 (μs):', font=ctk.CTkFont(size=8)).grid(
            row=0, column=0, padx=2, pady=1, sticky='w'
        )
        self.global_quota = ctk.CTkEntry(row_frame2, width=70, font=ctk.CTkFont(size=8))
        self.global_quota.grid(row=1, column=0, padx=2, pady=2, sticky='ew')
        self.global_quota.insert(0, '')
        self.global_quota.bind('<KeyRelease>', lambda e: self._trigger_change())

        # emulator_period
        ctk.CTkLabel(row_frame2, text='模拟器周期 (μs):', font=ctk.CTkFont(size=8)).grid(
            row=0, column=1, padx=2, pady=1, sticky='w'
        )
        self.emulator_period = ctk.CTkEntry(row_frame2, width=70, font=ctk.CTkFont(size=8))
        self.emulator_period.grid(row=1, column=1, padx=2, pady=2, sticky='ew')
        self.emulator_period.insert(0, '')
        self.emulator_period.bind('<KeyRelease>', lambda e: self._trigger_change())

        # emulator_quota
        ctk.CTkLabel(row_frame2, text='模拟器配额 (μs):', font=ctk.CTkFont(size=8)).grid(
            row=0, column=2, padx=2, pady=1, sticky='w'
        )
        self.emulator_quota = ctk.CTkEntry(row_frame2, width=70, font=ctk.CTkFont(size=8))
        self.emulator_quota.grid(row=1, column=2, padx=2, pady=2, sticky='ew')
        self.emulator_quota.insert(0, '')
        self.emulator_quota.bind('<KeyRelease>', lambda e: self._trigger_change())

        # iothread_period
        ctk.CTkLabel(row_frame2, text='IOThread 周期 (μs):', font=ctk.CTkFont(size=8)).grid(
            row=0, column=3, padx=2, pady=1, sticky='w'
        )
        self.iothread_period = ctk.CTkEntry(row_frame2, width=70, font=ctk.CTkFont(size=8))
        self.iothread_period.grid(row=1, column=3, padx=2, pady=2, sticky='ew')
        self.iothread_period.insert(0, '')
        self.iothread_period.bind('<KeyRelease>', lambda e: self._trigger_change())
        row += 1

        # 第三行：iothread_quota (单独一个)
        ctk.CTkLabel(parent, text='IOThread 配额 (μs):', font=ctk.CTkFont(size=8)).grid(
            row=row, column=0, padx=5, pady=1, sticky='w'
        )
        self.iothread_quota = ctk.CTkEntry(parent, width=120, font=ctk.CTkFont(size=8))
        self.iothread_quota.grid(row=row + 1, column=0, padx=5, pady=2, sticky='ew')
        self.iothread_quota.insert(0, '')
        self.iothread_quota.bind('<KeyRelease>', lambda e: self._trigger_change())

    def _create_scheduler_section(self, parent: ctk.CTkFrame) -> None:
        """创建第 3 列：调度器配置."""
        row = 0

        # 标题
        ctk.CTkLabel(
            parent,
            text='调度器配置',
            font=ctk.CTkFont(family='', size=11, weight='bold'),
            text_color='#ff9800',
        ).grid(row=row, column=0, padx=10, pady=8, sticky='w')
        row += 1

        # vcpusched
        vs_header_frame = ctk.CTkFrame(parent, fg_color='transparent')
        vs_header_frame.grid(row=row, column=0, padx=5, pady=2, sticky='ew')
        ctk.CTkLabel(vs_header_frame, text='vCPU 调度器:', font=ctk.CTkFont(size=9)).pack(
            side='left'
        )
        self.vcpusched_none = ctk.CTkCheckBox(
            vs_header_frame, text='None', font=ctk.CTkFont(size=8)
        )
        self.vcpusched_none.pack(side='right', padx=2)
        self.vcpusched_none.configure(command=self._on_vcpusched_none_change)
        row += 1

        vs_frame2 = ctk.CTkFrame(parent, fg_color='transparent')
        vs_frame2.grid(row=row, column=0, padx=5, pady=2, sticky='ew')
        ctk.CTkLabel(vs_frame2, text='vCPUs:', font=ctk.CTkFont(size=8), width=40).pack(side='left')
        self.vcpusched_vcpus = ctk.CTkEntry(vs_frame2, width=70, font=ctk.CTkFont(size=8))
        self.vcpusched_vcpus.pack(side='left', padx=2)
        self.vcpusched_vcpus.insert(0, '')
        self.vcpusched_vcpus.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(vs_frame2, text='调度器:', font=ctk.CTkFont(size=8), width=40).pack(
            side='left', padx=(5, 2)
        )
        self.vcpusched_scheduler = ctk.CTkOptionMenu(
            vs_frame2, values=['batch', 'idle', 'fifo', 'rr'], width=50, font=ctk.CTkFont(size=8)
        )
        self.vcpusched_scheduler.set('batch')
        self.vcpusched_scheduler.pack(side='left', padx=2)
        self.vcpusched_scheduler.configure(command=self._on_vcpusched_scheduler_change)
        row += 1

        vs_frame3 = ctk.CTkFrame(parent, fg_color='transparent')
        vs_frame3.grid(row=row, column=0, padx=5, pady=2, sticky='ew')
        ctk.CTkLabel(vs_frame3, text='优先级:', font=ctk.CTkFont(size=8), width=40).pack(
            side='left'
        )
        self.vcpusched_priority = ctk.CTkEntry(vs_frame3, width=70, font=ctk.CTkFont(size=8))
        self.vcpusched_priority.pack(side='left', padx=2)
        self.vcpusched_priority.insert(0, '')
        self.vcpusched_priority.bind('<KeyRelease>', lambda e: self._trigger_change())
        self.vcpusched_state = 'enabled'
        row += 1

        # iothreadsched
        ios_header_frame = ctk.CTkFrame(parent, fg_color='transparent')
        ios_header_frame.grid(row=row, column=0, padx=5, pady=(8, 2), sticky='ew')
        ctk.CTkLabel(ios_header_frame, text='IOThread 调度器:', font=ctk.CTkFont(size=9)).pack(
            side='left'
        )
        self.iothreadsched_none = ctk.CTkCheckBox(
            ios_header_frame, text='None', font=ctk.CTkFont(size=8)
        )
        self.iothreadsched_none.pack(side='right', padx=2)
        self.iothreadsched_none.configure(command=self._on_iothreadsched_none_change)
        row += 1

        ioss_frame2 = ctk.CTkFrame(parent, fg_color='transparent')
        ioss_frame2.grid(row=row, column=0, padx=5, pady=2, sticky='ew')
        ctk.CTkLabel(ioss_frame2, text='IOThreads:', font=ctk.CTkFont(size=8), width=50).pack(
            side='left'
        )
        self.iothreadsched_iothreads = ctk.CTkEntry(ioss_frame2, width=60, font=ctk.CTkFont(size=8))
        self.iothreadsched_iothreads.pack(side='left', padx=2)
        self.iothreadsched_iothreads.insert(0, '')
        self.iothreadsched_iothreads.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(ioss_frame2, text='调度器:', font=ctk.CTkFont(size=8), width=40).pack(
            side='left', padx=(5, 2)
        )
        self.iothreadsched_scheduler = ctk.CTkOptionMenu(
            ioss_frame2, values=['batch', 'idle', 'fifo', 'rr'], width=50, font=ctk.CTkFont(size=8)
        )
        self.iothreadsched_scheduler.set('batch')
        self.iothreadsched_scheduler.pack(side='left', padx=2)
        self.iothreadsched_scheduler.configure(command=self._on_iothreadsched_scheduler_change)
        row += 1

        ios_frame3 = ctk.CTkFrame(parent, fg_color='transparent')
        ios_frame3.grid(row=row, column=0, padx=5, pady=2, sticky='ew')
        ctk.CTkLabel(ios_frame3, text='优先级:', font=ctk.CTkFont(size=8), width=40).pack(
            side='left'
        )
        self.iothreadsched_priority = ctk.CTkEntry(ios_frame3, width=70, font=ctk.CTkFont(size=8))
        self.iothreadsched_priority.pack(side='left', padx=2)
        self.iothreadsched_priority.insert(0, '')
        self.iothreadsched_priority.bind('<KeyRelease>', lambda e: self._trigger_change())
        self.iothreadsched_state = 'enabled'
        row += 1

        # emulatorsched
        es_header_frame = ctk.CTkFrame(parent, fg_color='transparent')
        es_header_frame.grid(row=row, column=0, padx=5, pady=(8, 2), sticky='ew')
        ctk.CTkLabel(es_header_frame, text='模拟器调度器:', font=ctk.CTkFont(size=9)).pack(
            side='left'
        )
        self.emulatorsched_none = ctk.CTkCheckBox(
            es_header_frame, text='None', font=ctk.CTkFont(size=8)
        )
        self.emulatorsched_none.pack(side='right', padx=2)
        self.emulatorsched_none.configure(command=self._on_emulatorsched_none_change)
        row += 1

        es_frame2 = ctk.CTkFrame(parent, fg_color='transparent')
        es_frame2.grid(row=row, column=0, padx=5, pady=2, sticky='ew')
        ctk.CTkLabel(es_frame2, text='调度器:', font=ctk.CTkFont(size=8), width=50).pack(
            side='left'
        )
        self.emulatorsched_scheduler = ctk.CTkOptionMenu(
            es_frame2, values=['batch', 'idle', 'fifo', 'rr'], width=60, font=ctk.CTkFont(size=8)
        )
        self.emulatorsched_scheduler.set('batch')
        self.emulatorsched_scheduler.pack(side='left', padx=2)
        self.emulatorsched_scheduler.configure(command=self._on_emulatorsched_scheduler_change)

        ctk.CTkLabel(es_frame2, text='优先级:', font=ctk.CTkFont(size=8), width=40).pack(
            side='left', padx=(5, 2)
        )
        self.emulatorsched_priority = ctk.CTkEntry(es_frame2, width=60, font=ctk.CTkFont(size=8))
        self.emulatorsched_priority.pack(side='left', padx=2)
        self.emulatorsched_priority.insert(0, '')
        self.emulatorsched_priority.bind('<KeyRelease>', lambda e: self._trigger_change())
        self.emulatorsched_state = 'enabled'

    def _create_cachetune_section(self, parent: ctk.CTkFrame) -> None:
        """创建第 4 列：缓存调优."""
        row = 0

        # 标题
        ctk.CTkLabel(
            parent,
            text='缓存调优',
            font=ctk.CTkFont(family='', size=11, weight='bold'),
            text_color='#9c27b0',
        ).grid(row=row, column=0, padx=10, pady=8, sticky='w')
        row += 1

        # 添加按钮
        ctk.CTkButton(
            parent,
            text='+ CacheTune',
            width=100,
            height=25,
            command=self._add_cachetune,
            font=ctk.CTkFont(size=9),
        ).grid(row=row, column=0, padx=10, pady=5, sticky='w')
        row += 1

        # Cachetune 列表容器
        self.cachetune_scroll_frame = ctk.CTkFrame(parent, fg_color='transparent')
        self.cachetune_scroll_frame.grid(row=row, column=0, padx=5, pady=2, sticky='ew')
        parent.grid_rowconfigure(row, weight=1)

    def _create_memorytune_section(self, parent: ctk.CTkFrame) -> None:
        """创建第 5 列：内存带宽调优."""
        row = 0

        # 标题
        ctk.CTkLabel(
            parent,
            text='内存带宽调优',
            font=ctk.CTkFont(family='', size=11, weight='bold'),
            text_color='#e91e63',
        ).grid(row=row, column=0, padx=10, pady=8, sticky='w')
        row += 1

        # 添加按钮
        ctk.CTkButton(
            parent,
            text='+ MemoryTune',
            width=100,
            height=25,
            command=self._add_memorytune,
            font=ctk.CTkFont(size=9),
        ).grid(row=row, column=0, padx=10, pady=5, sticky='w')
        row += 1

        # MemoryTune 列表容器
        self.memorytune_scroll_frame = ctk.CTkFrame(parent, fg_color='transparent')
        self.memorytune_scroll_frame.grid(row=row, column=0, padx=5, pady=2, sticky='ew')
        parent.grid_rowconfigure(row, weight=1)

    # ========== vCPU Pin 操作方法 ==========
    def _add_vcpupin(self) -> None:
        """添加一个 vCPU Pin 配置."""
        row_frame = ctk.CTkFrame(self.vcpupin_list_frame, fg_color='#2a2a2a', corner_radius=4)
        row_frame.pack(fill='x', padx=3, pady=1)

        ctk.CTkLabel(row_frame, text='vCPU', font=ctk.CTkFont(size=8), width=35, anchor='w').pack(
            side='left'
        )
        id_entry = ctk.CTkEntry(row_frame, width=35, font=ctk.CTkFont(size=8))
        id_entry.insert(0, str(len(self.vcpupin_entries)))
        id_entry.pack(side='left', padx=1)
        id_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(row_frame, text='CPUs', font=ctk.CTkFont(size=8), width=35, anchor='w').pack(
            side='left'
        )
        cpuset_entry = ctk.CTkEntry(row_frame, width=60, font=ctk.CTkFont(size=8))
        cpuset_entry.insert(0, '')
        cpuset_entry.configure(placeholder_text='例如: 0-3,5')
        cpuset_entry.pack(side='left', padx=1)
        cpuset_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        self.vcpupin_entries.append((id_entry, cpuset_entry, row_frame))
        self._trigger_change()
        self._update_frame_visibility()

    def _remove_vcpupin(self) -> None:
        """删除最后一条 vCPU Pin 配置."""
        if self.vcpupin_entries:
            _id_entry, _cpuset_entry, frame = self.vcpupin_entries.pop()
            frame.destroy()
            self._trigger_change()
            self._update_frame_visibility()

    def _on_emulatorpin_none_change(self) -> None:
        """处理 emulatorpin None 复选框变化."""
        if self.emulatorpin_none.get():
            self.emulatorpin.configure(state='disabled')
            self.emulatorpin_state = 'disabled'
        else:
            self.emulatorpin.configure(state='normal')
            self.emulatorpin_state = 'enabled'
        self._trigger_change()

    # ========== IOThread Pin 操作方法 ==========
    def _add_iothreadpin(self) -> None:
        """添加一个 IOThread Pin 配置."""
        row_frame = ctk.CTkFrame(self.iothreadpin_list_frame, fg_color='#2a2a2a', corner_radius=4)
        row_frame.pack(fill='x', padx=3, pady=1)

        ctk.CTkLabel(
            row_frame, text='IOThread', font=ctk.CTkFont(size=8), width=50, anchor='w'
        ).pack(side='left')
        id_entry = ctk.CTkEntry(row_frame, width=35, font=ctk.CTkFont(size=8))
        id_entry.insert(0, str(len(self.iothreadpin_entries)))
        id_entry.pack(side='left', padx=1)
        id_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(row_frame, text='CPUs', font=ctk.CTkFont(size=8), width=35, anchor='w').pack(
            side='left'
        )
        cpuset_entry = ctk.CTkEntry(row_frame, width=60, font=ctk.CTkFont(size=8))
        cpuset_entry.insert(0, '')
        cpuset_entry.configure(placeholder_text='例如: 0-3,5')
        cpuset_entry.pack(side='left', padx=1)
        cpuset_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        self.iothreadpin_entries.append((id_entry, cpuset_entry, row_frame))
        self._trigger_change()
        self._update_frame_visibility()

    def _update_frame_visibility(self) -> None:
        """根据列表状态更新框架可见性."""
        has_vcpupins = len(self.vcpupin_entries) > 0
        if has_vcpupins:
            self.vcpupin_list_frame.grid()
        else:
            self.vcpupin_list_frame.grid_remove()

        has_iothreadpins = len(self.iothreadpin_entries) > 0
        if has_iothreadpins:
            self.iothreadpin_list_frame.grid()
        else:
            self.iothreadpin_list_frame.grid_remove()

    def _remove_iothreadpin_last(self) -> None:
        """删除最后一条 IOThread Pin 配置."""
        if self.iothreadpin_entries:
            _id_entry, _cpuset_entry, frame = self.iothreadpin_entries.pop()
            frame.destroy()
            self._trigger_change()
            self._update_frame_visibility()

    # ========== 调度器事件处理 ==========
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

    # ========== CacheTune 操作方法 ==========
    def _add_cachetune(self) -> None:
        """添加一个 cachetune 配置组."""
        frame = ctk.CTkFrame(self.cachetune_scroll_frame, fg_color='#2a2a2a', corner_radius=4)
        frame.pack(fill='x', padx=5, pady=3)

        # 第一行：vcpus 和删除按钮
        top_row = ctk.CTkFrame(frame, fg_color='transparent')
        top_row.pack(fill='x', padx=5, pady=2)

        ctk.CTkLabel(top_row, text='vCPUs:', font=ctk.CTkFont(size=8), width=35, anchor='w').pack(
            side='left'
        )
        vcpus_entry = ctk.CTkEntry(top_row, width=60, font=ctk.CTkFont(size=8))
        vcpus_entry.insert(0, '')
        vcpus_entry.pack(side='left', padx=2)
        vcpus_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        del_btn = ctk.CTkButton(
            top_row,
            text='×',
            width=24,
            height=18,
            command=lambda f=frame: self._remove_cachetune(f),
            font=ctk.CTkFont(size=8),
        )
        del_btn.pack(side='left', padx=5)

        # 第二行：cache 配置
        cache_row = ctk.CTkFrame(frame, fg_color='transparent')
        cache_row.pack(fill='x', padx=5, pady=1)

        ctk.CTkLabel(cache_row, text='Cache:', font=ctk.CTkFont(size=8), width=35, anchor='w').pack(
            side='left'
        )
        ctk.CTkLabel(cache_row, text='L:', font=ctk.CTkFont(size=8), width=15, anchor='w').pack(
            side='left', padx=(5, 1)
        )
        cache_level = ctk.CTkOptionMenu(
            cache_row, values=['1', '2', '3'], width=35, font=ctk.CTkFont(size=8)
        )
        cache_level.set('3')
        cache_level.pack(side='left', padx=1)
        cache_level.configure(command=lambda e: self._trigger_change())

        ctk.CTkLabel(cache_row, text='T:', font=ctk.CTkFont(size=8), width=12, anchor='w').pack(
            side='left', padx=(3, 1)
        )
        cache_type = ctk.CTkOptionMenu(
            cache_row, values=['code', 'data', 'both'], width=45, font=ctk.CTkFont(size=8)
        )
        cache_type.set('both')
        cache_type.pack(side='left', padx=1)
        cache_type.configure(command=lambda e: self._trigger_change())

        ctk.CTkLabel(cache_row, text='S:', font=ctk.CTkFont(size=8), width=12, anchor='w').pack(
            side='left', padx=(3, 1)
        )
        cache_size = ctk.CTkEntry(cache_row, width=35, font=ctk.CTkFont(size=8))
        cache_size.insert(0, '')
        cache_size.pack(side='left', padx=1)
        cache_size.bind('<KeyRelease>', lambda e: self._trigger_change())

        cache_unit = ctk.CTkOptionMenu(
            cache_row, values=['KiB', 'MiB', 'GiB'], width=38, font=ctk.CTkFont(size=8)
        )
        cache_unit.set('MiB')
        cache_unit.pack(side='left', padx=1)
        cache_unit.configure(command=lambda e: self._trigger_change())

        # 第三行：monitor 配置
        monitor_row = ctk.CTkFrame(frame, fg_color='transparent')
        monitor_row.pack(fill='x', padx=5, pady=1)

        ctk.CTkLabel(monitor_row, text='Mon:', font=ctk.CTkFont(size=8), width=35, anchor='w').pack(
            side='left'
        )
        ctk.CTkLabel(
            monitor_row, text='vCPUs:', font=ctk.CTkFont(size=8), width=35, anchor='w'
        ).pack(side='left', padx=(2, 1))
        monitor_vcpus = ctk.CTkEntry(monitor_row, width=50, font=ctk.CTkFont(size=8))
        monitor_vcpus.insert(0, '')
        monitor_vcpus.pack(side='left', padx=1)
        monitor_vcpus.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(monitor_row, text='L:', font=ctk.CTkFont(size=8), width=15, anchor='w').pack(
            side='left', padx=(5, 1)
        )
        monitor_level = ctk.CTkOptionMenu(
            monitor_row, values=['1', '2', '3'], width=35, font=ctk.CTkFont(size=8)
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

    def _remove_cachetune(self, frame: ctk.CTkFrame) -> None:
        """删除一个 cachetune 配置."""
        frame.destroy()
        self.cachetune_entries = [e for e in self.cachetune_entries if e['frame'] != frame]
        self._trigger_change()

    # ========== MemoryTune 操作方法 ==========
    def _add_memorytune(self) -> None:
        """添加一个 memorytune 配置组."""
        frame = ctk.CTkFrame(self.memorytune_scroll_frame, fg_color='#2a2a2a', corner_radius=4)
        frame.pack(fill='x', padx=5, pady=3)

        # 第一行：vcpus 和删除按钮
        top_row = ctk.CTkFrame(frame, fg_color='transparent')
        top_row.pack(fill='x', padx=5, pady=2)

        ctk.CTkLabel(top_row, text='vCPUs:', font=ctk.CTkFont(size=8), width=35, anchor='w').pack(
            side='left'
        )
        vcpus_entry = ctk.CTkEntry(top_row, width=60, font=ctk.CTkFont(size=8))
        vcpus_entry.insert(0, '')
        vcpus_entry.pack(side='left', padx=2)
        vcpus_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        del_btn = ctk.CTkButton(
            top_row,
            text='×',
            width=24,
            height=18,
            command=lambda f=frame: self._remove_memorytune(f),
            font=ctk.CTkFont(size=8),
        )
        del_btn.pack(side='left', padx=5)

        # 第二行：node 配置
        node_row = ctk.CTkFrame(frame, fg_color='transparent')
        node_row.pack(fill='x', padx=5, pady=1)

        ctk.CTkLabel(node_row, text='Node:', font=ctk.CTkFont(size=8), width=35, anchor='w').pack(
            side='left'
        )
        node_id = ctk.CTkEntry(node_row, width=35, font=ctk.CTkFont(size=8))
        node_id.insert(0, '')
        node_id.pack(side='left', padx=2)
        node_id.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(
            node_row, text='Bandwidth (%):', font=ctk.CTkFont(size=8), width=75, anchor='w'
        ).pack(side='left', padx=(5, 2))
        bandwidth = ctk.CTkEntry(node_row, width=40, font=ctk.CTkFont(size=8))
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

    def _remove_memorytune(self, frame: ctk.CTkFrame) -> None:
        """删除一个 memorytune 配置."""
        frame.destroy()
        self.memorytune_entries = [e for e in self.memorytune_entries if e['frame'] != frame]
        self._trigger_change()

    def get_config(self) -> dict[str, Any]:
        """获取配置数据."""
        config: dict[str, Any] = {}

        # vcpupin
        vcpupins = []
        for id_entry, cpuset_entry, _ in self.vcpupin_entries:
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
        for id_entry, cpuset_entry, _ in self.iothreadpin_entries:
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
            vcpus = self.vcpusched_vcpus.get().strip()
            if vcpus:
                vcpusched = {}
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
            iothreads = self.iothreadsched_iothreads.get().strip()
            if iothreads:
                iothreadsched = {}
                iothreadsched['iothreads'] = iothreads
                scheduler = self.iothreadsched_scheduler.get()
                iothreadsched['scheduler'] = scheduler
                priority = self.iothreadsched_priority.get().strip()
                if priority and scheduler in ('fifo', 'rr'):
                    iothreadsched['priority'] = int(priority)
                if iothreadsched.get('scheduler') and iothreadsched['scheduler'] != 'batch':
                    config['iothreadsched'] = iothreadsched

        # emulatorsched
        if self.emulatorsched_state == 'enabled':
            emulatorsched = {}
            scheduler = self.emulatorsched_scheduler.get()
            emulatorsched['scheduler'] = scheduler
            priority = self.emulatorsched_priority.get().strip()
            if priority and scheduler in ('fifo', 'rr'):
                emulatorsched['priority'] = int(priority)
            if emulatorsched.get('scheduler') and emulatorsched['scheduler'] != 'batch':
                config['emulatorsched'] = emulatorsched

        # cachetune
        cachetunes = []
        for entry in self.cachetune_entries:
            ct = {}
            vcpus = entry['vcpus'].get().strip()
            if not vcpus:
                continue

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

        # memorytune
        memorytunes = []
        for entry in self.memorytune_entries:
            vcpus = entry['vcpus'].get().strip()
            if not vcpus:
                continue

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
