"""启动安全配置 Tab - Launch Security.

支持 AMD SEV/SEV-SNP, Intel TDX, IBM s390-pv 启动安全配置。
"""

from typing import ClassVar

import customtkinter as ctk

from components.base_tab import SectionConfig, StandardConfigTab


class LaunchSecurityTab(StandardConfigTab):
    """启动安全配置 Tab - SEV/SEV-SNP/TDX/s390-pv 启动安全."""

    SECTIONS: ClassVar[dict] = {
        'basic': SectionConfig(
            title='启动安全类型',
            fields=[],
            color='#64b5f6',
        ),
        'sev_common': SectionConfig(
            title='SEV/SEV-SNP 通用选项',
            fields=[],
            color='#4caf50',
        ),
        'sev_specific': SectionConfig(
            title='SEV 专用选项',
            fields=[],
            color='#8bc34a',
        ),
        'snp_options': SectionConfig(
            title='SEV-SNP 高级选项',
            fields=[],
            color='#9c27b0',
        ),
        'tdx_options': SectionConfig(
            title='Intel TDX 选项',
            fields=[],
            color='#2196f3',
        ),
        'info': SectionConfig(
            title='说明',
            fields=[],
            color='#ff9800',
        ),
    }

    def _init_sections_ui(self) -> None:
        """初始化基于 Sections 的 UI，自定义每行的布局."""
        super()._init_sections_ui()

        # 在 basic section 添加自定义 UI
        basic_frame = self.section_frames['basic']
        basic_row = 1
        self._create_basic_row(basic_frame, basic_row)
        basic_row += 1
        self.section_rows['basic'] = basic_row

        # 在 sev_common section 添加 SEV/SEV-SNP 通用选项
        sev_frame = self.section_frames['sev_common']
        sev_row = 1
        self._create_sev_common_options(sev_frame, sev_row)
        sev_row += 1
        self.section_rows['sev_common'] = sev_row

        # 在 sev_specific section 添加 SEV 专用选项
        sev_spec_frame = self.section_frames['sev_specific']
        sev_spec_row = 1
        self._create_sev_specific_options(sev_spec_frame, sev_spec_row)
        sev_spec_row += 1
        self.section_rows['sev_specific'] = sev_spec_row

        # 在 snp_options section 添加 SEV-SNP 特有选项
        snp_frame = self.section_frames['snp_options']
        snp_row = 1
        self._create_snp_options(snp_frame, snp_row)
        snp_row += 1
        self.section_rows['snp_options'] = snp_row

        # 在 tdx_options section 添加 Intel TDX 特有选项
        tdx_frame = self.section_frames['tdx_options']
        tdx_row = 1
        self._create_tdx_options(tdx_frame, tdx_row)
        tdx_row += 1
        self.section_rows['tdx_options'] = tdx_row

        # 在 info section 添加说明文本
        info_frame = self.section_frames['info']
        info_row = 1
        self._create_info_text(info_frame, info_row)
        info_row += 1
        self.section_rows['info'] = info_row

    def _create_basic_row(self, parent: ctk.CTkFrame, row: int) -> None:
        """创建基本信息行：类型 + 策略."""
        frame = ctk.CTkFrame(parent, fg_color='transparent')
        frame.grid(row=row, column=0, columnspan=2, padx=10, pady=3, sticky='w')

        # 类型选择
        ctk.CTkLabel(frame, text='类型:', font=('', 11), width=50, anchor='w').pack(
            side='left', padx=(0, 3)
        )
        self.sec_type = ctk.CTkOptionMenu(
            frame,
            values=['none', 'sev', 'sev-snp', 'tdx', 's390-pv'],
            width=120,
            font=('', 10),
            command=self._on_type_change,
        )
        self.sec_type.set('none')
        self.sec_type.pack(side='left', padx=3)

        # 策略 (Policy) - 十六进制字符串
        ctk.CTkLabel(frame, text='策略:', font=('', 11), width=40, anchor='w').pack(
            side='left', padx=(15, 3)
        )
        self.policy = ctk.CTkEntry(frame, placeholder_text='0x0001', width=100, font=('', 10))
        self.policy.pack(side='left', padx=3)
        self.policy.bind('<KeyRelease>', lambda e: self._trigger_change())

        # 说明标签
        policy_tip = ctk.CTkLabel(frame, text='(十六进制)', font=('', 9), text_color='#888888')
        policy_tip.pack(side='left', padx=3)

    def _create_sev_common_options(self, parent: ctk.CTkFrame, row: int) -> None:
        """创建 SEV/SEV-SNP 通用选项."""
        frame = ctk.CTkFrame(parent, fg_color='transparent')
        frame.grid(row=row, column=0, columnspan=2, padx=10, pady=3, sticky='w')

        # CBitPos
        ctk.CTkLabel(frame, text='CBitPos:', font=('', 10), width=60, anchor='w').pack(
            side='left', padx=(0, 3)
        )
        self.cbitpos_enable = ctk.CTkCheckBox(
            frame, text='启用', font=('', 10), command=self._trigger_change
        )
        self.cbitpos_enable.pack(side='left', padx=3)

        self.cbitpos_value = ctk.CTkEntry(frame, placeholder_text='47', width=60, font=('', 10))
        self.cbitpos_value.pack(side='left', padx=3)
        self.cbitpos_value.bind('<KeyRelease>', lambda e: self._trigger_change())

        # ReducedPhysBits
        ctk.CTkLabel(frame, text='ReducedPhysBits:', font=('', 10), width=100, anchor='w').pack(
            side='left', padx=(15, 3)
        )
        self.reduced_phys_bits_enable = ctk.CTkCheckBox(
            frame, text='启用', font=('', 10), command=self._trigger_change
        )
        self.reduced_phys_bits_enable.pack(side='left', padx=3)

        self.reduced_phys_bits_value = ctk.CTkEntry(
            frame, placeholder_text='1', width=60, font=('', 10)
        )
        self.reduced_phys_bits_value.pack(side='left', padx=3)
        self.reduced_phys_bits_value.bind('<KeyRelease>', lambda e: self._trigger_change())

        # KernelHashes (第二行)
        row += 1
        frame2 = ctk.CTkFrame(parent, fg_color='transparent')
        frame2.grid(row=row, column=0, columnspan=2, padx=10, pady=3, sticky='w')

        self.kernel_hashes = ctk.CTkCheckBox(
            frame2,
            text='KernelHashes (包含内核/ramdisk/命令行哈希)',
            font=('', 10),
            command=self._trigger_change,
        )
        self.kernel_hashes.pack(side='left', padx=(0, 3))

        kernel_hashes_tip = ctk.CTkLabel(
            frame2, text='(仅直接内核引导时有效)', font=('', 9), text_color='#888888'
        )
        kernel_hashes_tip.pack(side='left', padx=3)

    def _create_sev_specific_options(self, parent: ctk.CTkFrame, row: int) -> None:
        """创建 SEV 专用选项."""
        frame = ctk.CTkFrame(parent, fg_color='transparent')
        frame.grid(row=row, column=0, columnspan=2, padx=10, pady=3, sticky='w')

        # DH Cert
        ctk.CTkLabel(frame, text='DH Cert:', font=('', 10), width=60, anchor='w').pack(
            side='left', padx=(0, 3)
        )
        self.dh_cert = ctk.CTkEntry(
            frame, placeholder_text='Base64 编码的 DH 密钥', width=300, font=('', 10)
        )
        self.dh_cert.pack(side='left', padx=3)
        self.dh_cert.bind('<KeyRelease>', lambda e: self._trigger_change())

        # Session (第二行)
        row += 1
        frame2 = ctk.CTkFrame(parent, fg_color='transparent')
        frame2.grid(row=row, column=0, columnspan=2, padx=10, pady=3, sticky='w')

        ctk.CTkLabel(frame2, text='Session:', font=('', 10), width=60, anchor='w').pack(
            side='left', padx=(0, 3)
        )
        self.session = ctk.CTkEntry(
            frame2, placeholder_text='Base64 编码的会话数据', width=300, font=('', 10)
        )
        self.session.pack(side='left', padx=3)
        self.session.bind('<KeyRelease>', lambda e: self._trigger_change())

    def _create_snp_options(self, parent: ctk.CTkFrame, row: int) -> None:
        """创建 SEV-SNP 特有选项."""
        # 第一行：authorKey + vcek
        frame1 = ctk.CTkFrame(parent, fg_color='transparent')
        frame1.grid(row=row, column=0, columnspan=2, padx=10, pady=3, sticky='w')

        self.author_key = ctk.CTkCheckBox(
            frame1, text='AuthorKey', font=('', 10), command=self._trigger_change
        )
        self.author_key.pack(side='left', padx=(0, 3))

        self.vcek = ctk.CTkCheckBox(
            frame1, text='VCEK (取消则使用 VLEK)', font=('', 10), command=self._trigger_change
        )
        self.vcek.select()  # 默认启用 VCEK
        self.vcek.pack(side='left', padx=(15, 3))

        # 第二行：guestVisibleWorkarounds
        row += 1
        frame2 = ctk.CTkFrame(parent, fg_color='transparent')
        frame2.grid(row=row, column=0, columnspan=2, padx=10, pady=3, sticky='w')

        ctk.CTkLabel(
            frame2, text='GuestVisibleWorkarounds:', font=('', 10), width=150, anchor='w'
        ).pack(side='left', padx=(0, 3))
        self.guest_visible_workarounds = ctk.CTkEntry(
            frame2, placeholder_text='16 字节 Base64 编码', width=250, font=('', 10)
        )
        self.guest_visible_workarounds.pack(side='left', padx=3)
        self.guest_visible_workarounds.bind('<KeyRelease>', lambda e: self._trigger_change())

        # 第三行：idBlock
        row += 1
        frame3 = ctk.CTkFrame(parent, fg_color='transparent')
        frame3.grid(row=row, column=0, columnspan=2, padx=10, pady=3, sticky='w')

        ctk.CTkLabel(frame3, text='ID Block:', font=('', 10), width=150, anchor='w').pack(
            side='left', padx=(0, 3)
        )
        self.id_block = ctk.CTkEntry(
            frame3, placeholder_text='96 字节 Base64 编码', width=250, font=('', 10)
        )
        self.id_block.pack(side='left', padx=3)
        self.id_block.bind('<KeyRelease>', lambda e: self._trigger_change())

        # 第四行：idAuth
        row += 1
        frame4 = ctk.CTkFrame(parent, fg_color='transparent')
        frame4.grid(row=row, column=0, columnspan=2, padx=10, pady=3, sticky='w')

        ctk.CTkLabel(frame4, text='ID Auth:', font=('', 10), width=150, anchor='w').pack(
            side='left', padx=(0, 3)
        )
        self.id_auth = ctk.CTkEntry(
            frame4, placeholder_text='4096 字节 Base64 编码', width=250, font=('', 10)
        )
        self.id_auth.pack(side='left', padx=3)
        self.id_auth.bind('<KeyRelease>', lambda e: self._trigger_change())

        # 第五行：hostData
        row += 1
        frame5 = ctk.CTkFrame(parent, fg_color='transparent')
        frame5.grid(row=row, column=0, columnspan=2, padx=10, pady=3, sticky='w')

        ctk.CTkLabel(frame5, text='Host Data:', font=('', 10), width=150, anchor='w').pack(
            side='left', padx=(0, 3)
        )
        self.host_data = ctk.CTkEntry(
            frame5, placeholder_text='32 字节 Base64 编码', width=250, font=('', 10)
        )
        self.host_data.pack(side='left', padx=3)
        self.host_data.bind('<KeyRelease>', lambda e: self._trigger_change())

    def _create_tdx_options(self, parent: ctk.CTkFrame, row: int) -> None:
        """创建 Intel TDX 特有选项."""
        # 第一行：mrConfigId + mrOwner
        frame1 = ctk.CTkFrame(parent, fg_color='transparent')
        frame1.grid(row=row, column=0, columnspan=2, padx=10, pady=3, sticky='w')

        ctk.CTkLabel(frame1, text='MrConfigId:', font=('', 10), width=80, anchor='w').pack(
            side='left', padx=(0, 3)
        )
        self.mr_config_id = ctk.CTkEntry(
            frame1, placeholder_text='SHA384 Base64', width=200, font=('', 10)
        )
        self.mr_config_id.pack(side='left', padx=3)
        self.mr_config_id.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(frame1, text='MrOwner:', font=('', 10), width=70, anchor='w').pack(
            side='left', padx=(15, 3)
        )
        self.mr_owner = ctk.CTkEntry(
            frame1, placeholder_text='SHA384 Base64', width=200, font=('', 10)
        )
        self.mr_owner.pack(side='left', padx=3)
        self.mr_owner.bind('<KeyRelease>', lambda e: self._trigger_change())

        # 第二行：mrOwnerConfig
        row += 1
        frame2 = ctk.CTkFrame(parent, fg_color='transparent')
        frame2.grid(row=row, column=0, columnspan=2, padx=10, pady=3, sticky='w')

        ctk.CTkLabel(frame2, text='MrOwnerConfig:', font=('', 10), width=100, anchor='w').pack(
            side='left', padx=(0, 3)
        )
        self.mr_owner_config = ctk.CTkEntry(
            frame2, placeholder_text='SHA384 Base64', width=250, font=('', 10)
        )
        self.mr_owner_config.pack(side='left', padx=3)
        self.mr_owner_config.bind('<KeyRelease>', lambda e: self._trigger_change())

        # 第三行：quoteGenerationService
        row += 1
        frame3 = ctk.CTkFrame(parent, fg_color='transparent')
        frame3.grid(row=row, column=0, columnspan=2, padx=10, pady=3, sticky='w')

        ctk.CTkLabel(frame3, text='QuoteService 路径:', font=('', 10), width=100, anchor='w').pack(
            side='left', padx=(0, 3)
        )
        self.quote_generation_service = ctk.CTkEntry(
            frame3, placeholder_text='/var/run/tdx-qgs/qgs.socket', width=250, font=('', 10)
        )
        self.quote_generation_service.pack(side='left', padx=3)
        self.quote_generation_service.bind('<KeyRelease>', lambda e: self._trigger_change())

    def _create_info_text(self, parent: ctk.CTkFrame, row: int) -> None:
        """创建说明文本."""
        info_text = """启动安全类型说明:
• SEV - AMD Secure Encrypted Virtualization (安全加密虚拟化)
  适用于：AMD EPYC 处理器 (Naples, Rome, Milan)
  功能：内存加密，每个 VM 有唯一的加密密钥

• SEV-SNP - AMD Secure Nested Paging (安全嵌套分页)
  适用于：AMD EPYC 处理器 (Milan 及更新)
  功能：在 SEV 基础上增加内存完整性和反向追踪保护

• TDX - Intel Trust Domain Extensions (信任域扩展)
  适用于：Intel Xeon Scalable 第 4 代及更新
  功能：创建隔离的信任域，保护内存和 CPU 状态

• s390-pv - IBM Protected Virtualization (保护虚拟化)
  适用于：IBM z15 及更新主机
  功能：保护 VM 免受宿主机和 hypervisor 访问

要求:
• 硬件支持：对应平台的 SEV/TDX/s390-pv 功能
• 固件：AMD SEV 固件、Intel TDX 模块、IBM s390 固件
• 内核：KVM 支持并启用相应功能
• QEMU：QEMU 6.0+ (SEV), 7.2+ (SEV-SNP), 8.0+ (TDX)"""

        ctk.CTkLabel(
            parent,
            text=info_text,
            font=('', 9),
            text_color='#888888',
            justify='left',
            anchor='nw',
        ).grid(row=row, column=0, columnspan=2, padx=10, pady=5, sticky='nw')

    def _on_type_change(self, value: str) -> None:
        """当安全类型改变时的处理."""
        is_none = value == 'none'
        is_sev = value == 'sev'
        is_snp = value == 'sev-snp'
        is_tdx = value == 'tdx'
        is_s390 = value == 's390-pv'

        # 基本选项 - 策略字段
        # s390-pv 不需要策略字段
        policy_state = 'disabled' if is_none or is_s390 else 'normal'
        self.policy.configure(state=policy_state)

        # SEV/SEV-SNP 通用选项
        sev_common_state = 'disabled' if is_none or is_tdx or is_s390 else 'normal'
        self.cbitpos_enable.configure(state=sev_common_state)
        self.cbitpos_value.configure(
            state=sev_common_state if self.cbitpos_enable.get() else 'disabled'
        )
        self.reduced_phys_bits_enable.configure(state=sev_common_state)
        self.reduced_phys_bits_value.configure(
            state=sev_common_state if self.reduced_phys_bits_enable.get() else 'disabled'
        )
        self.kernel_hashes.configure(state=sev_common_state)

        # SEV 专用选项 (仅 SEV)
        sev_specific_state = 'disabled' if not is_sev else 'normal'
        self.dh_cert.configure(state=sev_specific_state)
        self.session.configure(state=sev_specific_state)

        # SEV-SNP 特有选项
        snp_state = 'disabled' if not is_snp else 'normal'
        self.author_key.configure(state=snp_state)
        self.vcek.configure(state=snp_state)
        self.guest_visible_workarounds.configure(state=snp_state)
        self.id_block.configure(state=snp_state)
        self.id_auth.configure(state=snp_state)
        self.host_data.configure(state=snp_state)

        # Intel TDX 特有选项
        tdx_state = 'disabled' if not is_tdx else 'normal'
        self.mr_config_id.configure(state=tdx_state)
        self.mr_owner.configure(state=tdx_state)
        self.mr_owner_config.configure(state=tdx_state)
        self.quote_generation_service.configure(state=tdx_state)

        # 显示/隐藏 SEV 专用选项区域
        sev_spec_frame = self.section_frames['sev_specific']
        if is_sev:
            sev_spec_frame.grid()
        else:
            sev_spec_frame.grid_remove()

        # 显示/隐藏 SEV-SNP 选项区域
        snp_frame = self.section_frames['snp_options']
        if is_snp:
            snp_frame.grid()
        else:
            snp_frame.grid_remove()

        # 显示/隐藏 TDX 选项区域
        tdx_frame = self.section_frames['tdx_options']
        if is_tdx:
            tdx_frame.grid()
        else:
            tdx_frame.grid_remove()

        # 触发配置变更
        self._trigger_change()

    def _toggle_cbitpos_value(self) -> None:
        """根据 CBitPos 复选框状态切换输入框启用/禁用."""
        if self.cbitpos_enable.get():
            self.cbitpos_value.configure(state='normal')
        else:
            self.cbitpos_value.configure(state='disabled')
        self._trigger_change()

    def _toggle_reduced_phys_bits_value(self) -> None:
        """根据 ReducedPhysBits 复选框状态切换输入框启用/禁用."""
        if self.reduced_phys_bits_enable.get():
            self.reduced_phys_bits_value.configure(state='normal')
        else:
            self.reduced_phys_bits_value.configure(state='disabled')
        self._trigger_change()

    def get_config(self) -> dict:
        """获取配置数据."""
        sec_type = self.sec_type.get()

        # 如果类型为 none，返回空配置
        if sec_type == 'none':
            return {}

        config = {
            'type': sec_type,
            'policy': self.policy.get().strip() if self.policy.get() else '',
            'cbitpos_enabled': self.cbitpos_enable.get(),
            'cbitpos_value': self.cbitpos_value.get().strip(),
            'reduced_phys_bits_enabled': self.reduced_phys_bits_enable.get(),
            'reduced_phys_bits_value': self.reduced_phys_bits_value.get().strip(),
            'kernel_hashes': self.kernel_hashes.get(),
        }

        # SEV 特有选项
        if sec_type == 'sev':
            config['dh_cert'] = self.dh_cert.get().strip()
            config['session'] = self.session.get().strip()

        # SEV-SNP 特有选项
        if sec_type == 'sev-snp':
            config['author_key'] = self.author_key.get()
            config['vcek'] = self.vcek.get()
            config['guest_visible_workarounds'] = self.guest_visible_workarounds.get().strip()
            config['id_block'] = self.id_block.get().strip()
            config['id_auth'] = self.id_auth.get().strip()
            config['host_data'] = self.host_data.get().strip()

        # Intel TDX 特有选项
        if sec_type == 'tdx':
            config['mr_config_id'] = self.mr_config_id.get().strip()
            config['mr_owner'] = self.mr_owner.get().strip()
            config['mr_owner_config'] = self.mr_owner_config.get().strip()
            config['quote_generation_service'] = self.quote_generation_service.get().strip()

        return config

    def to_xml(self) -> dict:
        """生成 XML 配置字典."""
        config = self.get_config()

        # 如果配置为空（类型为 none），返回空字典
        if not config:
            return {}

        launch_security_config = {
            'type': config.get('type', 'sev'),
        }

        # 策略
        policy = config.get('policy', '')
        if policy:
            launch_security_config['policy'] = policy

        # CBitPos - 使用正确的字段名
        cbitpos_enabled = config.get('cbitpos_enabled')
        cbitpos_value = config.get('cbitpos_value', '')
        if cbitpos_enabled and cbitpos_value:
            launch_security_config['cbitpos_enabled'] = True
            launch_security_config['cbitpos_value'] = cbitpos_value

        # ReducedPhysBits - 使用正确的字段名
        reduced_phys_bits_enabled = config.get('reduced_phys_bits_enabled')
        reduced_phys_bits_value = config.get('reduced_phys_bits_value', '')
        if reduced_phys_bits_enabled and reduced_phys_bits_value:
            launch_security_config['reduced_phys_bits_enabled'] = True
            launch_security_config['reduced_phys_bits_value'] = reduced_phys_bits_value

        # KernelHashes
        kernel_hashes = config.get('kernel_hashes')
        if kernel_hashes:
            launch_security_config['kernel_hashes'] = True

        # SEV 特有选项
        dh_cert = config.get('dh_cert', '')
        if dh_cert:
            launch_security_config['dh_cert'] = dh_cert

        session = config.get('session', '')
        if session:
            launch_security_config['session'] = session

        # SEV-SNP 特有选项
        author_key = config.get('author_key')
        if author_key:
            launch_security_config['author_key'] = True

        vcek = config.get('vcek')
        if not vcek:  # vcek 默认为 True，只有取消选中时才设置
            launch_security_config['vcek'] = False

        guest_visible_workarounds = config.get('guest_visible_workarounds', '')
        if guest_visible_workarounds:
            launch_security_config['guest_visible_workarounds'] = guest_visible_workarounds

        id_block = config.get('id_block', '')
        if id_block:
            launch_security_config['id_block'] = id_block

        id_auth = config.get('id_auth', '')
        if id_auth:
            launch_security_config['id_auth'] = id_auth

        host_data = config.get('host_data', '')
        if host_data:
            launch_security_config['host_data'] = host_data

        # Intel TDX 特有选项
        mr_config_id = config.get('mr_config_id', '')
        if mr_config_id:
            launch_security_config['mr_config_id'] = mr_config_id

        mr_owner = config.get('mr_owner', '')
        if mr_owner:
            launch_security_config['mr_owner'] = mr_owner

        mr_owner_config = config.get('mr_owner_config', '')
        if mr_owner_config:
            launch_security_config['mr_owner_config'] = mr_owner_config

        quote_generation_service = config.get('quote_generation_service', '')
        if quote_generation_service:
            launch_security_config['quote_generation_service'] = quote_generation_service

        return {'launch_security': launch_security_config}

    def load_config(self, config: dict) -> None:
        """加载配置数据到 UI."""
        launch_config = config.get('launch_security', config)

        sec_type = launch_config.get('type', launch_config.get('sec_type', 'none'))

        # 如果没有配置或类型为 none，设置为 none
        if not sec_type:
            sec_type = 'none'

        self.sec_type.set(sec_type)

        # 触发类型变更处理，更新控件状态
        self._on_type_change(sec_type)

        # 通用选项
        policy = launch_config.get('policy')
        if policy:
            self.policy.delete(0, ctk.END)
            self.policy.insert(0, policy)

        cbitpos = launch_config.get('cbitpos')
        cbitpos_value = launch_config.get('cbitpos_value')
        if cbitpos or cbitpos_value:
            self.cbitpos_enable.select()
            if cbitpos_value:
                self.cbitpos_value.delete(0, ctk.END)
                self.cbitpos_value.insert(0, cbitpos_value)
        else:
            self.cbitpos_enable.deselect()

        reduced_phys_bits = launch_config.get('reduced_phys_bits')
        reduced_phys_bits_value = launch_config.get('reduced_phys_bits_value')
        if reduced_phys_bits or reduced_phys_bits_value:
            self.reduced_phys_bits_enable.select()
            if reduced_phys_bits_value:
                self.reduced_phys_bits_value.delete(0, ctk.END)
                self.reduced_phys_bits_value.insert(0, reduced_phys_bits_value)
        else:
            self.reduced_phys_bits_enable.deselect()

        kernel_hashes = launch_config.get('kernel_hashes')
        if kernel_hashes:
            self.kernel_hashes.select()
        else:
            self.kernel_hashes.deselect()

        # SEV 特有选项
        dh_cert = launch_config.get('dh_cert')
        if dh_cert:
            self.dh_cert.delete(0, ctk.END)
            self.dh_cert.insert(0, dh_cert)

        session = launch_config.get('session')
        if session:
            self.session.delete(0, ctk.END)
            self.session.insert(0, session)

        # SEV-SNP 特有选项
        author_key = launch_config.get('author_key')
        if author_key:
            self.author_key.select()
        else:
            self.author_key.deselect()

        vcek = launch_config.get('vcek')
        if vcek is False:
            self.vcek.deselect()
        else:
            self.vcek.select()

        guest_visible_workarounds = launch_config.get('guest_visible_workarounds')
        if guest_visible_workarounds:
            self.guest_visible_workarounds.delete(0, ctk.END)
            self.guest_visible_workarounds.insert(0, guest_visible_workarounds)

        id_block = launch_config.get('id_block')
        if id_block:
            self.id_block.delete(0, ctk.END)
            self.id_block.insert(0, id_block)

        id_auth = launch_config.get('id_auth')
        if id_auth:
            self.id_auth.delete(0, ctk.END)
            self.id_auth.insert(0, id_auth)

        host_data = launch_config.get('host_data')
        if host_data:
            self.host_data.delete(0, ctk.END)
            self.host_data.insert(0, host_data)

        # Intel TDX 特有选项
        mr_config_id = launch_config.get('mr_config_id')
        if mr_config_id:
            self.mr_config_id.delete(0, ctk.END)
            self.mr_config_id.insert(0, mr_config_id)

        mr_owner = launch_config.get('mr_owner')
        if mr_owner:
            self.mr_owner.delete(0, ctk.END)
            self.mr_owner.insert(0, mr_owner)

        mr_owner_config = launch_config.get('mr_owner_config')
        if mr_owner_config:
            self.mr_owner_config.delete(0, ctk.END)
            self.mr_owner_config.insert(0, mr_owner_config)

        quote_generation_service = launch_config.get('quote_generation_service')
        if quote_generation_service:
            self.quote_generation_service.delete(0, ctk.END)
            self.quote_generation_service.insert(0, quote_generation_service)
