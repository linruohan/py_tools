"""虚拟化特性配置 Tab - Hypervisor features.

根据 libvirt 文档第 15 章实现，支持以下虚拟化特性:

通用特性 (features 元素):
- pae, acpi, apic, hap, viridian, privnet
- pvspinlock, pmu, vmport, gic, vmcoreinfo, smm
- ioapic, hpt, htm, nested-hv, ccf-assist
- cfpc, sbbc, ibs, ras, ps2, aia, virtualization
- msrs (bhyve), async-teardown (QEMU)

Hyper-V 特性 (hyperv 元素):
- relaxed, vapic, spinlocks, vpindex, runtime
- synic, stimer, reset, vendor_id, frequencies
- reenlightenment, tlbflush, ipi, evmcs, avic
- emsr_bitmap, xmm_input

KVM 特性 (kvm 元素):
- hidden, hint-dedicated, poll-control, pv-ipi, dirty-ring

Xen 特性 (xen 元素):
- e820_host, passthrough

TCG 特性 (tcg 元素):
- tb-cache
"""

from typing import ClassVar

import customtkinter as ctk

from components.base_tab import BaseConfigTab
from components.inner_tab_panel import InnerTabPanel
from utils.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class GeneralFeaturesSubTab(BaseConfigTab):
    """通用特性子 Tab - 支持所有架构的通用虚拟化特性."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, on_change_callback, **kwargs)
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面 - 使用四列布局."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

        # === 第一列：基础特性 ===
        left_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        left_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        left_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(left_frame, text='基础特性', font=CTK_FONT_BOLD, text_color='#e91e63').grid(
            row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
        )

        self._create_checkbox_row(left_frame, 'pae', '物理地址扩展', 1)
        self._create_checkbox_row(left_frame, 'acpi', '电源管理', 2)
        self._create_checkbox_row(left_frame, 'apic', '可编程中断', 3)
        self._create_checkbox_row(left_frame, 'hap', '硬件辅助分页', 4)
        self._create_checkbox_row(left_frame, 'viridian', 'Hyper-V 扩展', 5)
        self._create_checkbox_row(left_frame, 'privnet', '私有网络命名空间', 6)

        # === 第二列：KVM/QEMU 特性 ===
        mid1_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        mid1_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        mid1_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            mid1_frame, text='KVM/QEMU 特性', font=CTK_FONT_BOLD, text_color='#ff9800'
        ).grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w')

        self._create_checkbox_row(mid1_frame, 'pvspinlock', '半虚拟自旋锁', 1)
        self._create_checkbox_row(mid1_frame, 'pmu', '性能监控单元', 2)
        self._create_checkbox_row(mid1_frame, 'vmport', 'VMware IO 端口', 3)
        self._create_checkbox_row(mid1_frame, 'vmcoreinfo', 'QEMU vmcoreinfo', 4)
        self._create_checkbox_row(mid1_frame, 'smm', '系统管理模式', 5)
        self._create_checkbox_row(mid1_frame, 'ioapic', 'I/O APIC', 6)

        # === 第三列：pSeries/ARM 特性 ===
        mid2_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        mid2_frame.grid(row=0, column=2, sticky='nsew', padx=5, pady=5)
        mid2_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            mid2_frame, text='pSeries/ARM 特性', font=CTK_FONT_BOLD, text_color='#4caf50'
        ).grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w')

        self._create_checkbox_row(mid2_frame, 'gic', '通用中断控制器', 1)
        self._create_checkbox_row(mid2_frame, 'hpt', 'Hash Page Table', 2)
        self._create_checkbox_row(mid2_frame, 'htm', '硬件事务内存', 3)
        self._create_checkbox_row(mid2_frame, 'nested-hv', '嵌套虚拟化', 4)
        self._create_checkbox_row(mid2_frame, 'ccf-assist', '计数缓存刷新辅助', 5)
        self._create_checkbox_row(mid2_frame, 'ras', '内存错误报告', 6)

        # === 第四列：其他特性 ===
        right_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        right_frame.grid(row=0, column=3, sticky='nsew', padx=5, pady=5)
        right_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(right_frame, text='其他特性', font=CTK_FONT_BOLD, text_color='#00bcd4').grid(
            row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
        )

        self._create_checkbox_row(right_frame, 'cfpc', '特权变更缓存刷新', 1)
        self._create_checkbox_row(right_frame, 'sbbc', '推测屏障边界检查', 2)
        self._create_checkbox_row(right_frame, 'ibs', '间接分支预测', 3)
        self._create_checkbox_row(right_frame, 'ps2', 'PS/2 控制器', 4)
        self._create_checkbox_row(right_frame, 'aia', '高级中断架构', 5)
        self._create_checkbox_row(right_frame, 'virtualization', 'ARM 虚拟化扩展', 6)

        # === 第五行：特殊配置 ===
        special_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        special_frame.grid(row=1, column=0, columnspan=4, sticky='nsew', padx=5, pady=5)
        special_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(special_frame, text='特殊配置', font=CTK_FONT_BOLD, text_color='#9c27b0').grid(
            row=0, column=0, columnspan=4, padx=10, pady=5, sticky='w'
        )

        # msrs (bhyve)
        self._create_checkbox_row(special_frame, 'msrs', 'MSRs 未知忽略 (bhyve)', 1, col=0)
        self.msrs_unknown = ctk.CTkOptionMenu(
            special_frame, values=['None', 'ignore', 'fault'], width=80, font=CTK_FONT_SMALL
        )
        self.msrs_unknown.set('None')
        self.msrs_unknown.grid(row=1, column=1, padx=5, pady=3, sticky='w')
        self.msrs_unknown.configure(command=self._trigger_change)

        # async-teardown (QEMU)
        self._create_checkbox_row(special_frame, 'async-teardown', '异步卸载 (QEMU)', 2, col=0)
        self.async_teardown = ctk.CTkOptionMenu(
            special_frame, values=['None', 'yes', 'no'], width=80, font=CTK_FONT_SMALL
        )
        self.async_teardown.set('None')
        self.async_teardown.grid(row=2, column=1, padx=5, pady=3, sticky='w')
        self.async_teardown.configure(command=self._trigger_change)

        # GIC version
        self._create_checkbox_row(special_frame, 'gic_version', 'GIC 版本 (ARM)', 3, col=0)
        self.gic_version = ctk.CTkOptionMenu(
            special_frame, values=['None', '2', '3', 'host'], width=80, font=CTK_FONT_SMALL
        )
        self.gic_version.set('None')
        self.gic_version.grid(row=3, column=1, padx=5, pady=3, sticky='w')
        self.gic_version.configure(command=self._trigger_change)

        # IOAPIC driver
        self._create_checkbox_row(special_frame, 'ioapic_driver', 'IOAPIC 驱动', 4, col=0)
        self.ioapic_driver = ctk.CTkOptionMenu(
            special_frame, values=['None', 'kvm', 'qemu'], width=80, font=CTK_FONT_SMALL
        )
        self.ioapic_driver.set('None')
        self.ioapic_driver.grid(row=4, column=1, padx=5, pady=3, sticky='w')
        self.ioapic_driver.configure(command=self._trigger_change)

        # HPT resizing
        self._create_checkbox_row(special_frame, 'hpt_resizing', 'HPT 调整大小', 5, col=0)
        self.hpt_resizing = ctk.CTkOptionMenu(
            special_frame,
            values=['None', 'enabled', 'disabled', 'required'],
            width=80,
            font=CTK_FONT_SMALL,
        )
        self.hpt_resizing.set('None')
        self.hpt_resizing.grid(row=5, column=1, padx=5, pady=3, sticky='w')
        self.hpt_resizing.configure(command=self._trigger_change)

        # HPT maxpagesize
        ctk.CTkLabel(
            special_frame, text='HPT 页大小:', font=CTK_FONT_MAIN, width=80, anchor='w'
        ).grid(row=6, column=0, padx=10, pady=3, sticky='w')
        self.hpt_maxpagesize = ctk.CTkOptionMenu(
            special_frame, values=['None', '64 KiB', '16 MiB', '16 GiB'], width=100
        )
        self.hpt_maxpagesize.set('None')
        self.hpt_maxpagesize.grid(row=6, column=1, padx=5, pady=3, sticky='w')
        self.hpt_maxpagesize.configure(command=self._trigger_change)

        # TCG tb-cache size
        ctk.CTkLabel(
            special_frame, text='TCG TB 缓存:', font=CTK_FONT_MAIN, width=80, anchor='w'
        ).grid(row=1, column=2, padx=10, pady=3, sticky='w')
        self.tcg_tb_cache = ctk.CTkEntry(
            special_frame, placeholder_text='128 (MiB)', width=100, font=CTK_FONT_SMALL
        )
        self.tcg_tb_cache.grid(row=1, column=3, padx=5, pady=3, sticky='w')
        self.tcg_tb_cache.bind('<KeyRelease>', lambda e: self._trigger_change())

        # SMM TSEG size
        ctk.CTkLabel(
            special_frame, text='SMM TSEG:', font=CTK_FONT_MAIN, width=80, anchor='w'
        ).grid(row=2, column=2, padx=10, pady=3, sticky='w')
        self.smm_tseg = ctk.CTkEntry(
            special_frame, placeholder_text='48 (MiB)', width=100, font=CTK_FONT_SMALL
        )
        self.smm_tseg.grid(row=2, column=3, padx=5, pady=3, sticky='w')
        self.smm_tseg.bind('<KeyRelease>', lambda e: self._trigger_change())

    def _create_checkbox_row(
        self, parent: ctk.CTkFrame, name: str, desc: str, row: int, col: int = 0
    ) -> None:
        """创建复选框行."""
        label_text = f'{name}'
        if desc:
            label_text = f'{name} ({desc})'
        cb = ctk.CTkCheckBox(parent, text=label_text, font=CTK_FONT_SMALL)
        cb.grid(row=row, column=col, padx=10, pady=2, sticky='w')
        cb.configure(command=self._trigger_change)
        setattr(self, name.replace('-', '_'), cb)

    def get_config(self) -> dict:
        """获取配置数据，过滤掉 None 和默认值."""
        config = {}

        # 基础特性 (boolean) - 只返回 True/False，未选中的不返回
        for name in ['pae', 'acpi', 'apic', 'hap', 'viridian', 'privnet']:
            widget = getattr(self, name, None)
            if widget:
                val = widget.get()
                if val:  # 1 = True, 0 = False (不添加)
                    config[name] = True

        # KVM/QEMU 特性 (boolean)
        for name in ['pvspinlock', 'pmu', 'vmport', 'vmcoreinfo', 'smm', 'ioapic']:
            widget = getattr(self, name.replace('-', '_'), None)
            if widget:
                val = widget.get()
                if val:
                    config[name] = True

        # pSeries/ARM 特性 (boolean)
        for name in ['gic', 'hpt', 'htm', 'nested-hv', 'ccf-assist', 'ras']:
            widget = getattr(self, name.replace('-', '_'), None)
            if widget:
                val = widget.get()
                if val:
                    config[name] = True

        # 其他特性 (boolean)
        for name in ['cfpc', 'sbbc', 'ibs', 'ps2', 'aia', 'virtualization']:
            widget = getattr(self, name.replace('-', '_'), None)
            if widget:
                val = widget.get()
                if val:
                    config[name] = True

        # 选项类型特性
        msrs_val = self.msrs_unknown.get()
        if msrs_val != 'None':
            config['msrs_unknown'] = msrs_val

        async_val = self.async_teardown.get()
        if async_val != 'None':
            config['async_teardown'] = async_val

        gic_ver = self.gic_version.get()
        if gic_ver != 'None':
            config['gic_version'] = gic_ver

        ioapic_drv = self.ioapic_driver.get()
        if ioapic_drv != 'None':
            config['ioapic_driver'] = ioapic_drv

        hpt_res = self.hpt_resizing.get()
        if hpt_res != 'None':
            config['hpt_resizing'] = hpt_res

        hpt_page = self.hpt_maxpagesize.get()
        if hpt_page != 'None':
            config['hpt_maxpagesize'] = hpt_page

        tcg_cache = self.tcg_tb_cache.get().strip()
        if tcg_cache:
            config['tcg_tb_cache'] = tcg_cache

        smm_tseg_val = self.smm_tseg.get().strip()
        if smm_tseg_val:
            config['smm_tseg'] = smm_tseg_val

        return config


class HypervFeaturesSubTab(BaseConfigTab):
    """Hyper-V 特性子 Tab - 支持所有 Hyper-V enlightenment 特性."""

    # 根据 libvirt 文档的完整特性列表
    HYPERV_FEATURES: ClassVar[list] = [
        ('relaxed', '放宽计时器约束'),
        ('vapic', '虚拟 APIC'),
        ('spinlocks', '自旋锁'),
        ('vpindex', '虚拟处理器索引'),
        ('runtime', '运行时信息'),
        ('synic', '合成中断控制器'),
        ('stimer', '合成计时器'),
        ('reset', 'hypervisor 重置'),
        ('frequencies', '频率 MSR'),
        ('reenlightenment', '再通知'),
        ('tlbflush', 'TLB 刷新'),
        ('ipi', '处理器间中断'),
        ('evmcs', 'Enlightened VMCS'),
        ('avic', 'Hyper-V SynIC with APICv/AVIC'),
        ('emsr_bitmap', 'MSR 位图优化'),
        ('xmm_input', 'XMM 快速超调用输入'),
    ]

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, on_change_callback, **kwargs)
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面 - 使用三列布局."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # === 第一列：基础特性 ===
        left_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        left_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        left_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            left_frame, text='Hyper-V 基础特性', font=CTK_FONT_BOLD, text_color='#64b5f6'
        ).grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w')

        row = 1
        for name, desc in self.HYPERV_FEATURES[:8]:
            self._create_checkbox_row(left_frame, name, desc, row)
            row += 1

        # === 第二列：高级特性 ===
        mid_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        mid_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        mid_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            mid_frame, text='Hyper-V 高级特性', font=CTK_FONT_BOLD, text_color='#4caf50'
        ).grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w')

        row = 1
        for name, desc in self.HYPERV_FEATURES[8:]:
            self._create_checkbox_row(mid_frame, name, desc, row)
            row += 1

        # === 第三列：配置选项 ===
        right_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        right_frame.grid(row=0, column=2, sticky='nsew', padx=5, pady=5)
        right_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(right_frame, text='配置选项', font=CTK_FONT_BOLD, text_color='#ff9800').grid(
            row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
        )

        # 模式选择
        ctk.CTkLabel(right_frame, text='模式:', font=CTK_FONT_MAIN, width=60, anchor='w').grid(
            row=1, column=0, padx=10, pady=3, sticky='w'
        )
        self.hyperv_mode = ctk.CTkOptionMenu(
            right_frame,
            values=['None', 'custom', 'passthrough', 'host-model'],
            width=120,
            font=CTK_FONT_SMALL,
        )
        self.hyperv_mode.set('None')
        self.hyperv_mode.grid(row=1, column=1, padx=5, pady=3, sticky='w')
        self.hyperv_mode.configure(command=self._trigger_change)

        # Vendor ID
        ctk.CTkLabel(right_frame, text='Vendor ID:', font=CTK_FONT_MAIN, width=60, anchor='w').grid(
            row=2, column=0, padx=10, pady=3, sticky='w'
        )
        self.vendor_id = ctk.CTkEntry(
            right_frame, placeholder_text='KVM Hv', width=120, font=CTK_FONT_SMALL
        )
        self.vendor_id.grid(row=2, column=1, padx=5, pady=3, sticky='w')
        self.vendor_id.bind('<KeyRelease>', lambda e: self._trigger_change())

        # Spinlocks retries
        ctk.CTkLabel(
            right_frame, text='Spinlocks 重试:', font=CTK_FONT_MAIN, width=80, anchor='w'
        ).grid(row=3, column=0, padx=10, pady=3, sticky='w')
        self.spinlocks_retries = ctk.CTkEntry(
            right_frame, placeholder_text='4096', width=80, font=CTK_FONT_SMALL
        )
        self.spinlocks_retries.grid(row=3, column=1, padx=5, pady=3, sticky='w')
        self.spinlocks_retries.bind('<KeyRelease>', lambda e: self._trigger_change())

        # TLBflush 子特性
        ctk.CTkLabel(
            right_frame, text='TLBflush direct:', font=CTK_FONT_MAIN, width=90, anchor='w'
        ).grid(row=4, column=0, padx=10, pady=3, sticky='w')
        self.tlbflush_direct = ctk.CTkOptionMenu(
            right_frame, values=['None', 'on', 'off'], width=60, font=CTK_FONT_SMALL
        )
        self.tlbflush_direct.set('None')
        self.tlbflush_direct.grid(row=4, column=1, padx=5, pady=3, sticky='w')
        self.tlbflush_direct.configure(command=self._trigger_change)

        ctk.CTkLabel(
            right_frame, text='TLBflush extended:', font=CTK_FONT_MAIN, width=90, anchor='w'
        ).grid(row=5, column=0, padx=10, pady=3, sticky='w')
        self.tlbflush_extended = ctk.CTkOptionMenu(
            right_frame, values=['None', 'on', 'off'], width=60, font=CTK_FONT_SMALL
        )
        self.tlbflush_extended.set('None')
        self.tlbflush_extended.grid(row=5, column=1, padx=5, pady=3, sticky='w')
        self.tlbflush_extended.configure(command=self._trigger_change)

        # Stimer direct
        ctk.CTkLabel(
            right_frame, text='Stimer direct:', font=CTK_FONT_MAIN, width=90, anchor='w'
        ).grid(row=6, column=0, padx=10, pady=3, sticky='w')
        self.stimer_direct = ctk.CTkOptionMenu(
            right_frame, values=['None', 'on', 'off'], width=60, font=CTK_FONT_SMALL
        )
        self.stimer_direct.set('None')
        self.stimer_direct.grid(row=6, column=1, padx=5, pady=3, sticky='w')
        self.stimer_direct.configure(command=self._trigger_change)

    def _create_checkbox_row(self, parent: ctk.CTkFrame, name: str, desc: str, row: int) -> None:
        """创建复选框行，带 None 选项支持."""
        # 使用 OptionMenu 来支持 None/on/off 三态
        ctk.CTkLabel(
            parent, text=f'{name} ({desc})', font=CTK_FONT_SMALL, width=180, anchor='w'
        ).grid(row=row, column=0, padx=10, pady=2, sticky='w')

        option = ctk.CTkOptionMenu(
            parent,
            values=['None', 'on', 'off'],
            width=80,
            font=CTK_FONT_SMALL,
            command=self._trigger_change,
        )
        option.set('None')
        option.grid(row=row, column=1, padx=5, pady=2, sticky='w')
        setattr(self, name, option)

    def get_config(self) -> dict:
        """获取配置数据，过滤掉 None 值."""
        config = {}

        # 模式
        mode_val = self.hyperv_mode.get()
        if mode_val != 'None':
            config['mode'] = mode_val

        # Vendor ID
        vendor_id_val = self.vendor_id.get().strip()
        if vendor_id_val:
            config['vendor_id'] = vendor_id_val

        # Spinlocks retries
        retries_val = self.spinlocks_retries.get().strip()
        if retries_val:
            config['spinlocks_retries'] = retries_val

        # TLBflush 子特性
        tlbflush_direct = self.tlbflush_direct.get()
        if tlbflush_direct != 'None':
            config['tlbflush_direct'] = tlbflush_direct

        tlbflush_extended = self.tlbflush_extended.get()
        if tlbflush_extended != 'None':
            config['tlbflush_extended'] = tlbflush_extended

        # Stimer 子特性
        stimer_direct = self.stimer_direct.get()
        if stimer_direct != 'None':
            config['stimer_direct'] = stimer_direct

        # 所有 Hyper-V 特性
        for name, _ in self.HYPERV_FEATURES:
            widget = getattr(self, name, None)
            if widget:
                val = widget.get()
                if val != 'None':
                    config[name] = val

        return config


class KVMFeaturesSubTab(BaseConfigTab):
    """KVM 特性子 Tab."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, on_change_callback, **kwargs)
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        left_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        left_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        left_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(left_frame, text='KVM 特性', font=CTK_FONT_BOLD, text_color='#ff9800').grid(
            row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
        )

        # hidden
        ctk.CTkLabel(
            left_frame, text='hidden (隐藏 KVM)', font=CTK_FONT_MAIN, width=120, anchor='w'
        ).grid(row=1, column=0, padx=10, pady=3, sticky='w')
        self.hidden = ctk.CTkOptionMenu(
            left_frame, values=['None', 'on', 'off'], width=80, font=CTK_FONT_SMALL
        )
        self.hidden.set('None')
        self.hidden.grid(row=1, column=1, padx=5, pady=3, sticky='w')
        self.hidden.configure(command=self._trigger_change)

        # hint-dedicated
        ctk.CTkLabel(
            left_frame, text='hint-dedicated', font=CTK_FONT_MAIN, width=120, anchor='w'
        ).grid(row=2, column=0, padx=10, pady=3, sticky='w')
        self.hint_dedicated = ctk.CTkOptionMenu(
            left_frame, values=['None', 'on', 'off'], width=80, font=CTK_FONT_SMALL
        )
        self.hint_dedicated.set('None')
        self.hint_dedicated.grid(row=2, column=1, padx=5, pady=3, sticky='w')
        self.hint_dedicated.configure(command=self._trigger_change)

        # poll-control
        ctk.CTkLabel(
            left_frame, text='poll-control', font=CTK_FONT_MAIN, width=120, anchor='w'
        ).grid(row=3, column=0, padx=10, pady=3, sticky='w')
        self.poll_control = ctk.CTkOptionMenu(
            left_frame, values=['None', 'on', 'off'], width=80, font=CTK_FONT_SMALL
        )
        self.poll_control.set('None')
        self.poll_control.grid(row=3, column=1, padx=5, pady=3, sticky='w')
        self.poll_control.configure(command=self._trigger_change)

        # pv-ipi
        ctk.CTkLabel(left_frame, text='pv-ipi', font=CTK_FONT_MAIN, width=120, anchor='w').grid(
            row=4, column=0, padx=10, pady=3, sticky='w'
        )
        self.pv_ipi = ctk.CTkOptionMenu(
            left_frame, values=['None', 'on', 'off'], width=80, font=CTK_FONT_SMALL
        )
        self.pv_ipi.set('None')
        self.pv_ipi.grid(row=4, column=1, padx=5, pady=3, sticky='w')
        self.pv_ipi.configure(command=self._trigger_change)

        right_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        right_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        right_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(right_frame, text='Dirty Ring', font=CTK_FONT_BOLD, text_color='#9c27b0').grid(
            row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
        )

        # dirty-ring
        ctk.CTkLabel(
            right_frame, text='dirty-ring:', font=CTK_FONT_MAIN, width=80, anchor='w'
        ).grid(row=1, column=0, padx=10, pady=3, sticky='w')
        self.dirty_ring = ctk.CTkOptionMenu(
            right_frame, values=['None', 'on', 'off'], width=80, font=CTK_FONT_SMALL
        )
        self.dirty_ring.set('None')
        self.dirty_ring.grid(row=1, column=1, padx=5, pady=3, sticky='w')
        self.dirty_ring.configure(command=self._trigger_change)

        # dirty-ring size
        ctk.CTkLabel(right_frame, text='大小:', font=CTK_FONT_MAIN, width=60, anchor='w').grid(
            row=2, column=0, padx=10, pady=3, sticky='w'
        )
        self.dirty_ring_size = ctk.CTkEntry(
            right_frame, placeholder_text='4096', width=80, font=CTK_FONT_SMALL
        )
        self.dirty_ring_size.grid(row=2, column=1, padx=5, pady=3, sticky='w')
        self.dirty_ring_size.bind('<KeyRelease>', lambda e: self._trigger_change())

    def get_config(self) -> dict:
        """获取配置数据."""
        config = {}

        # KVM 特性
        for name in ['hidden', 'hint_dedicated', 'poll_control', 'pv_ipi', 'dirty_ring']:
            widget = getattr(self, name, None)
            if widget:
                val = widget.get()
                if val != 'None':
                    config[name] = val

        # Dirty ring size
        size_val = self.dirty_ring_size.get().strip()
        if size_val:
            config['dirty_ring_size'] = size_val

        return config


class XenFeaturesSubTab(BaseConfigTab):
    """Xen 特性子 Tab."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, on_change_callback, **kwargs)
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        left_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        left_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        left_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(left_frame, text='Xen 特性', font=CTK_FONT_BOLD, text_color='#3f51b5').grid(
            row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
        )

        # e820_host
        ctk.CTkLabel(left_frame, text='e820_host', font=CTK_FONT_MAIN, width=120, anchor='w').grid(
            row=1, column=0, padx=10, pady=3, sticky='w'
        )
        self.e820_host = ctk.CTkOptionMenu(
            left_frame, values=['None', 'on', 'off'], width=80, font=CTK_FONT_SMALL
        )
        self.e820_host.set('None')
        self.e820_host.grid(row=1, column=1, padx=5, pady=3, sticky='w')
        self.e820_host.configure(command=self._trigger_change)

        # passthrough
        ctk.CTkLabel(
            left_frame, text='passthrough', font=CTK_FONT_MAIN, width=120, anchor='w'
        ).grid(row=2, column=0, padx=10, pady=3, sticky='w')
        self.passthrough = ctk.CTkOptionMenu(
            left_frame, values=['None', 'on', 'off'], width=80, font=CTK_FONT_SMALL
        )
        self.passthrough.set('None')
        self.passthrough.grid(row=2, column=1, padx=5, pady=3, sticky='w')
        self.passthrough.configure(command=self._trigger_change)

        # passthrough mode
        ctk.CTkLabel(
            left_frame, text='passthrough mode:', font=CTK_FONT_MAIN, width=120, anchor='w'
        ).grid(row=3, column=0, padx=10, pady=3, sticky='w')
        self.passthrough_mode = ctk.CTkOptionMenu(
            left_frame, values=['None', 'sync_pt', 'share_pt'], width=100, font=CTK_FONT_SMALL
        )
        self.passthrough_mode.set('None')
        self.passthrough_mode.grid(row=3, column=1, padx=5, pady=3, sticky='w')
        self.passthrough_mode.configure(command=self._trigger_change)

        right_frame = ctk.CTkFrame(self, fg_color='transparent')
        right_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)

        ctk.CTkLabel(
            right_frame,
            text='Xen 特性用于配置 Xen\nhypervisor 的行为。\n\ne820_host: 暴露主机 e820 给客户机\n\npassthrough: 启用 IOMMU 映射\n允许 PCI passthrough',
            font=CTK_FONT_SMALL,
            text_color='#888888',
            justify='left',
        ).grid(row=0, column=0, padx=10, pady=10, sticky='nw')

    def get_config(self) -> dict:
        """获取配置数据."""
        config = {}

        passthrough_val = self.passthrough.get()
        if passthrough_val != 'None':
            config['passthrough'] = passthrough_val

        passthrough_mode = self.passthrough_mode.get()
        if passthrough_mode != 'None':
            config['passthrough_mode'] = passthrough_mode

        e820_val = self.e820_host.get()
        if e820_val != 'None':
            config['e820_host'] = e820_val

        return config


class HypervisorFeaturesTab(BaseConfigTab):
    """虚拟化特性配置 Tab - 使用 InnerTabPanel 组织子 Tab."""

    SUB_TABS_CONFIG: ClassVar[dict] = {
        'general': {
            'name': '通用特性',
            'class': GeneralFeaturesSubTab,
            'default': True,
        },
        'hyperv': {
            'name': 'Hyper-V',
            'class': HypervFeaturesSubTab,
            'default': False,
        },
        'kvm': {
            'name': 'KVM',
            'class': KVMFeaturesSubTab,
            'default': False,
        },
        'xen': {
            'name': 'Xen',
            'class': XenFeaturesSubTab,
            'default': False,
        },
    }

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, on_change_callback, **kwargs)
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.inner_panel = InnerTabPanel(
            self,
            tabs_config=self.SUB_TABS_CONFIG,
            on_change_callback=self.on_change_callback,
        )
        self.inner_panel.grid(row=0, column=0, sticky='nsew')

    def get_config(self) -> dict:
        """获取配置数据."""
        return self.inner_panel.collect_data()

    def to_xml(self) -> dict:
        """生成 XML 配置字典."""
        return {'hypervisor_features': self.get_config()}
