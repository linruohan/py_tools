"""功能特性 Tab - ACPI, APIC, Hyper-V, IOMMU."""

import customtkinter as ctk

from ..styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_SMALL


class FeaturesTab(ctk.CTkFrame):
    """功能特性 Tab."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent')
        self.on_change_callback = on_change_callback

        # 控件引用
        self.acpi_check = None
        self.apic_check = None
        self.hyperv_check = None
        self.iommu_check = None

        # 初始化 UI
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面."""
        # 配置 grid 权重
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)

        features_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=8)
        features_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=10)
        features_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            features_frame, text='功能特性', font=CTK_FONT_BOLD, text_color='#64b5f6'
        ).grid(row=0, column=0, columnspan=4, padx=10, pady=5, sticky='w')

        # ACPI
        self.acpi_check = ctk.CTkCheckBox(
            features_frame, text='ACPI', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.acpi_check.grid(row=1, column=0, padx=10, pady=5, sticky='w')
        self.acpi_check.select()

        # APIC
        self.apic_check = ctk.CTkCheckBox(
            features_frame, text='APIC', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.apic_check.grid(row=1, column=1, padx=10, pady=5, sticky='w')
        self.apic_check.select()

        # Hyper-V
        self.hyperv_check = ctk.CTkCheckBox(
            features_frame, text='Hyper-V', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.hyperv_check.grid(row=1, column=2, padx=10, pady=5, sticky='w')

        # IOMMU
        self.iommu_check = ctk.CTkCheckBox(
            features_frame, text='IOMMU', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.iommu_check.grid(row=1, column=3, padx=10, pady=5, sticky='w')

    def _trigger_change(self):
        """触发变化回调."""
        if self.on_change_callback:
            self.on_change_callback()

    def get_features(self):
        """获取功能特性配置."""
        return {
            'acpi': self.acpi_check.get(),
            'apic': self.apic_check.get(),
            'hyperv': self.hyperv_check.get(),
            'iommu': self.iommu_check.get(),
        }
