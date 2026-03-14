"""虚拟化特性配置 Tab - Hypervisor features."""

from typing import ClassVar

import customtkinter as ctk

from components.base_tab import BaseConfigTab
from components.inner_tab_panel import InnerTabPanel
from utils.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class HypervFeaturesSubTab(BaseConfigTab):
    """Hyper-V 特性子 Tab."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, on_change_callback, **kwargs)

        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        left_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        left_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

        ctk.CTkLabel(
            left_frame, text='Hyper-V 特性', font=CTK_FONT_BOLD, text_color='#64b5f6'
        ).grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w')

        self.relaxed = ctk.CTkCheckBox(
            left_frame, text='relaxed', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.relaxed.grid(row=1, column=0, padx=10, pady=3, sticky='w')

        self.vapic = ctk.CTkCheckBox(
            left_frame, text='vapic', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.vapic.grid(row=2, column=0, padx=10, pady=3, sticky='w')

        self.spinlocks = ctk.CTkCheckBox(
            left_frame, text='spinlocks', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.spinlocks.grid(row=3, column=0, padx=10, pady=3, sticky='w')

        self.vpindex = ctk.CTkCheckBox(
            left_frame, text='vpindex', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.vpindex.grid(row=4, column=0, padx=10, pady=3, sticky='w')

        self.runtime = ctk.CTkCheckBox(
            left_frame, text='runtime', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.runtime.grid(row=5, column=0, padx=10, pady=3, sticky='w')

        self.synic = ctk.CTkCheckBox(
            left_frame, text='synic', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.synic.grid(row=6, column=0, padx=10, pady=3, sticky='w')

        self.stimer = ctk.CTkCheckBox(
            left_frame, text='stimer', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.stimer.grid(row=7, column=0, padx=10, pady=3, sticky='w')

        right_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        right_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)

        ctk.CTkLabel(right_frame, text='更多特性', font=CTK_FONT_BOLD, text_color='#4caf50').grid(
            row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
        )

        self.reset = ctk.CTkCheckBox(
            right_frame, text='reset', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.reset.grid(row=1, column=0, padx=10, pady=3, sticky='w')

        self.frequencies = ctk.CTkCheckBox(
            right_frame, text='frequencies', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.frequencies.grid(row=2, column=0, padx=10, pady=3, sticky='w')

        self.reenlightenment = ctk.CTkCheckBox(
            right_frame, text='reenlightenment', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.reenlightenment.grid(row=3, column=0, padx=10, pady=3, sticky='w')

        self.tlbflush = ctk.CTkCheckBox(
            right_frame, text='tlbflush', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.tlbflush.grid(row=4, column=0, padx=10, pady=3, sticky='w')

        self.ipi = ctk.CTkCheckBox(
            right_frame, text='ipi', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.ipi.grid(row=5, column=0, padx=10, pady=3, sticky='w')

        self.evmcs = ctk.CTkCheckBox(
            right_frame, text='evmcs', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.evmcs.grid(row=6, column=0, padx=10, pady=3, sticky='w')

        ctk.CTkLabel(right_frame, text='模式:', font=CTK_FONT_MAIN, width=60, anchor='w').grid(
            row=7, column=0, padx=10, pady=5, sticky='w'
        )
        self.hyperv_mode = ctk.CTkOptionMenu(
            right_frame,
            values=['custom', 'passthrough', 'host-model'],
            width=120,
            font=CTK_FONT_SMALL,
        )
        self.hyperv_mode.set('custom')
        self.hyperv_mode.grid(row=7, column=1, padx=5, pady=5, sticky='w')
        self.hyperv_mode.configure(command=self._trigger_change)

    def get_config(self) -> dict:
        """获取配置数据."""
        return {
            'mode': self.hyperv_mode.get(),
            'relaxed': self.relaxed.get(),
            'vapic': self.vapic.get(),
            'spinlocks': self.spinlocks.get(),
            'vpindex': self.vpindex.get(),
            'runtime': self.runtime.get(),
            'synic': self.synic.get(),
            'stimer': self.stimer.get(),
            'reset': self.reset.get(),
            'frequencies': self.frequencies.get(),
            'reenlightenment': self.reenlightenment.get(),
            'tlbflush': self.tlbflush.get(),
            'ipi': self.ipi.get(),
            'evmcs': self.evmcs.get(),
        }


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

        ctk.CTkLabel(left_frame, text='KVM 特性', font=CTK_FONT_BOLD, text_color='#ff9800').grid(
            row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
        )

        self.hidden = ctk.CTkCheckBox(
            left_frame, text='hidden (隐藏KVM)', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.hidden.grid(row=1, column=0, padx=10, pady=5, sticky='w')

        self.hint_dedicated = ctk.CTkCheckBox(
            left_frame, text='hint-dedicated', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.hint_dedicated.grid(row=2, column=0, padx=10, pady=5, sticky='w')

        self.poll_control = ctk.CTkCheckBox(
            left_frame, text='poll-control', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.poll_control.grid(row=3, column=0, padx=10, pady=5, sticky='w')

        self.pv_ipi = ctk.CTkCheckBox(
            left_frame, text='pv-ipi', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.pv_ipi.grid(row=4, column=0, padx=10, pady=5, sticky='w')

        right_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        right_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)

        ctk.CTkLabel(right_frame, text='Dirty Ring', font=CTK_FONT_BOLD, text_color='#9c27b0').grid(
            row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
        )

        self.dirty_ring = ctk.CTkCheckBox(
            right_frame, text='dirty-ring', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.dirty_ring.grid(row=1, column=0, padx=10, pady=5, sticky='w')

        ctk.CTkLabel(right_frame, text='大小:', font=CTK_FONT_MAIN, width=60, anchor='w').grid(
            row=1, column=1, padx=10, pady=5, sticky='w'
        )
        self.dirty_ring_size = ctk.CTkEntry(right_frame, placeholder_text='4096', width=80)
        self.dirty_ring_size.grid(row=1, column=2, padx=5, pady=5, sticky='w')
        self.dirty_ring_size.bind('<KeyRelease>', lambda e: self._trigger_change())

    def get_config(self) -> dict:
        """获取配置数据."""
        return {
            'hidden': self.hidden.get(),
            'hint_dedicated': self.hint_dedicated.get(),
            'poll_control': self.poll_control.get(),
            'pv_ipi': self.pv_ipi.get(),
            'dirty_ring': self.dirty_ring.get(),
            'dirty_ring_size': self.dirty_ring_size.get().strip(),
        }


class GeneralFeaturesSubTab(BaseConfigTab):
    """通用特性子 Tab."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, on_change_callback, **kwargs)

        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        left_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        left_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

        ctk.CTkLabel(left_frame, text='通用特性', font=CTK_FONT_BOLD, text_color='#e91e63').grid(
            row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
        )

        self.pae = ctk.CTkCheckBox(
            left_frame, text='pae (物理地址扩展)', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.pae.grid(row=1, column=0, padx=10, pady=3, sticky='w')

        self.acpi = ctk.CTkCheckBox(
            left_frame, text='acpi', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.acpi.select()
        self.acpi.grid(row=2, column=0, padx=10, pady=3, sticky='w')

        self.apic = ctk.CTkCheckBox(
            left_frame, text='apic', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.apic.select()
        self.apic.grid(row=3, column=0, padx=10, pady=3, sticky='w')

        self.hap = ctk.CTkCheckBox(
            left_frame, text='hap (硬件辅助分页)', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.hap.grid(row=4, column=0, padx=10, pady=3, sticky='w')

        self.viridian = ctk.CTkCheckBox(
            left_frame, text='viridian', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.viridian.grid(row=5, column=0, padx=10, pady=3, sticky='w')

        self.privnet = ctk.CTkCheckBox(
            left_frame, text='privnet', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.privnet.grid(row=6, column=0, padx=10, pady=3, sticky='w')

        right_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        right_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)

        ctk.CTkLabel(right_frame, text='其他特性', font=CTK_FONT_BOLD, text_color='#00bcd4').grid(
            row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
        )

        self.pvspinlock = ctk.CTkCheckBox(
            right_frame, text='pvspinlock', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.pvspinlock.grid(row=1, column=0, padx=10, pady=3, sticky='w')

        self.pmu = ctk.CTkCheckBox(
            right_frame, text='pmu', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.pmu.grid(row=2, column=0, padx=10, pady=3, sticky='w')

        self.vmport = ctk.CTkCheckBox(
            right_frame, text='vmport', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.vmport.grid(row=3, column=0, padx=10, pady=3, sticky='w')

        self.smm = ctk.CTkCheckBox(
            right_frame, text='smm', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.smm.grid(row=4, column=0, padx=10, pady=3, sticky='w')

        self.vmcoreinfo = ctk.CTkCheckBox(
            right_frame, text='vmcoreinfo', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.vmcoreinfo.grid(row=5, column=0, padx=10, pady=3, sticky='w')

        self.ras = ctk.CTkCheckBox(
            right_frame, text='ras', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.ras.grid(row=6, column=0, padx=10, pady=3, sticky='w')

    def get_config(self) -> dict:
        """获取配置数据."""
        return {
            'pae': self.pae.get(),
            'acpi': self.acpi.get(),
            'apic': self.apic.get(),
            'hap': self.hap.get(),
            'viridian': self.viridian.get(),
            'privnet': self.privnet.get(),
            'pvspinlock': self.pvspinlock.get(),
            'pmu': self.pmu.get(),
            'vmport': self.vmport.get(),
            'smm': self.smm.get(),
            'vmcoreinfo': self.vmcoreinfo.get(),
            'ras': self.ras.get(),
        }


class HypervisorFeaturesTab(BaseConfigTab):
    """虚拟化特性配置 Tab."""

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
        """生成XML配置字典."""
        return {'hypervisor_features': self.get_config()}
