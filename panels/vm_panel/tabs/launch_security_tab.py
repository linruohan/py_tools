"""启动安全配置 Tab - Launch Security."""

import customtkinter as ctk

from ..styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class LaunchSecurityTab(ctk.CTkFrame):
    """启动安全配置 Tab - SEV/SNP 启动安全."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent')
        self.on_change_callback = on_change_callback

        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        left_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        left_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        left_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            left_frame, text='启动安全配置', font=CTK_FONT_BOLD, text_color='#64b5f6'
        ).grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w')

        ctk.CTkLabel(left_frame, text='类型:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.sec_type = ctk.CTkOptionMenu(
            left_frame,
            values=['sev', 'snp'],
            width=100,
            font=CTK_FONT_SMALL,
        )
        self.sec_type.set('sev')
        self.sec_type.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.sec_type.configure(command=self._trigger_change)

        ctk.CTkLabel(left_frame, text='策略:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.policy = ctk.CTkEntry(left_frame, placeholder_text='0x0001', width=100)
        self.policy.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.policy.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(left_frame, text='DH 证书:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=3, column=0, padx=10, pady=5, sticky='w'
        )
        self.dh_cert = ctk.CTkEntry(left_frame, placeholder_text='证书路径', width=250)
        self.dh_cert.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        self.dh_cert.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(left_frame, text='会话数据:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=4, column=0, padx=10, pady=5, sticky='w'
        )
        self.session = ctk.CTkEntry(left_frame, placeholder_text='会话文件路径', width=250)
        self.session.grid(row=4, column=1, padx=5, pady=5, sticky='w')
        self.session.bind('<KeyRelease>', lambda e: self._trigger_change())

        right_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        right_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)

        ctk.CTkLabel(
            right_frame, text='SEV-SNP 选项', font=CTK_FONT_BOLD, text_color='#4caf50'
        ).grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w')

        self.cbitpos = ctk.CTkCheckBox(
            right_frame, text='CBitPos', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.cbitpos.grid(row=1, column=0, padx=10, pady=5, sticky='w')

        ctk.CTkLabel(right_frame, text='值:', font=CTK_FONT_MAIN, width=60, anchor='w').grid(
            row=1, column=1, padx=5, pady=5, sticky='w'
        )
        self.cbitpos_value = ctk.CTkEntry(right_frame, placeholder_text='47', width=60)
        self.cbitpos_value.grid(row=1, column=2, padx=5, pady=5, sticky='w')
        self.cbitpos_value.bind('<KeyRelease>', lambda e: self._trigger_change())

        self.reduced_phys_bits = ctk.CTkCheckBox(
            right_frame, text='ReducedPhysBits', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.reduced_phys_bits.grid(row=2, column=0, padx=10, pady=5, sticky='w')

        ctk.CTkLabel(right_frame, text='值:', font=CTK_FONT_MAIN, width=60, anchor='w').grid(
            row=2, column=1, padx=5, pady=5, sticky='w'
        )
        self.reduced_phys_bits_value = ctk.CTkEntry(right_frame, placeholder_text='1', width=60)
        self.reduced_phys_bits_value.grid(row=2, column=2, padx=5, pady=5, sticky='w')
        self.reduced_phys_bits_value.bind('<KeyRelease>', lambda e: self._trigger_change())

        self.kernel_hashes = ctk.CTkCheckBox(
            right_frame, text='KernelHashes', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.kernel_hashes.grid(row=3, column=0, columnspan=3, padx=10, pady=5, sticky='w')

        info_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        info_frame.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=5, pady=5)

        ctk.CTkLabel(info_frame, text='说明', font=CTK_FONT_BOLD, text_color='#ff9800').grid(
            row=0, column=0, padx=10, pady=5, sticky='w'
        )

        info_text = (
            'AMD 安全加密虚拟化 (SEV):\n'
            '• SEV - 内存加密\n'
            '• SEV-ES - 加密状态保护\n'
            '• SEV-SNP - 安全嵌套分页\n\n'
            '要求:\n'
            '• AMD EPYC 处理器\n'
            '• 主板固件支持\n'
            '• KVM 支持'
        )
        ctk.CTkLabel(
            info_frame,
            text=info_text,
            font=CTK_FONT_SMALL,
            text_color='#888888',
            justify='left',
        ).grid(row=1, column=0, padx=10, pady=5, sticky='w')

    def _trigger_change(self):
        """触发变化回调."""
        if self.on_change_callback:
            self.on_change_callback()

    def get_config(self) -> dict:
        """获取配置数据."""
        return {
            'type': self.sec_type.get(),
            'policy': self.policy.get().strip(),
            'dh_cert': self.dh_cert.get().strip(),
            'session': self.session.get().strip(),
            'cbitpos': self.cbitpos.get(),
            'cbitpos_value': self.cbitpos_value.get().strip(),
            'reduced_phys_bits': self.reduced_phys_bits.get(),
            'reduced_phys_bits_value': self.reduced_phys_bits_value.get().strip(),
            'kernel_hashes': self.kernel_hashes.get(),
        }

    def to_xml(self) -> dict:
        """生成XML配置字典."""
        return {'launch_security': self.get_config()}
