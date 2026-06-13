"""启动安全配置模块 - SEV/SEV-SNP/TDX/s390-pv."""

from dataclasses import dataclass


@dataclass
class LaunchSecurityConfig:
    """启动安全配置 - 支持 AMD SEV/SEV-SNP, Intel TDX, IBM s390-pv."""

    # 安全类型:sev, sev-snp, tdx, s390-pv, none
    sec_type: str = 'none'

    # ========== 通用配置 ==========
    #  Guest 策略 (十六进制字符串,如 0x0001)
    policy: str = ''

    # C-bit 位置启用标志
    cbitpos_enabled: bool = False

    # C-bit 位置 (加密位在页表条目中的位置)
    cbitpos_value: str = ''

    # 物理地址位减少量启用标志
    reduced_phys_bits_enabled: bool = False

    # 物理地址位减少量
    reduced_phys_bits_value: str = ''

    # 是否包含内核哈希 (仅 SEV/SEV-SNP 直接内核引导时有效)
    kernel_hashes: bool = False

    # ========== SEV 特有配置 ==========
    # Diffie-Hellman 密钥 (Base64 编码)
    dh_cert: str = ''

    # 会话数据 (Base64 编码)
    session: str = ''

    # ========== SEV-SNP 特有配置 ==========
    # 是否包含 Author Key
    author_key: bool = False

    # 是否使用 VCEK (默认为 True,False 则使用 VLEK)
    vcek: bool = True

    # Guest 可见的变通方案 (16 字节 Base64 编码)
    guest_visible_workarounds: str = ''

    # ID Block (96 字节 Base64 编码)
    id_block: str = ''

    # ID Auth (4096 字节 Base64 编码)
    id_auth: str = ''

    # Host Data (32 字节 Base64 编码)
    host_data: str = ''

    # ========== Intel TDX 特有配置 ==========
    # MrConfigId - 非所有者定义配置的 ID (SHA384 Base64)
    mr_config_id: str = ''

    # MrOwner - Guest TD 所有者 ID (SHA384 Base64)
    mr_owner: str = ''

    # MrOwnerConfig - 所有者定义配置的 ID (SHA384 Base64)
    mr_owner_config: str = ''

    # Quote Generation Service 路径
    quote_generation_service: str = '/var/run/tdx-qgs/qgs.socket'

    def to_dict(self) -> dict:
        """转换为字典."""
        return {
            'type': self.sec_type,
            'policy': self.policy,
            'cbitpos_enabled': self.cbitpos_enabled,
            'cbitpos_value': self.cbitpos_value,
            'reduced_phys_bits_enabled': self.reduced_phys_bits_enabled,
            'reduced_phys_bits_value': self.reduced_phys_bits_value,
            'kernel_hashes': self.kernel_hashes,
            'dh_cert': self.dh_cert,
            'session': self.session,
            'author_key': self.author_key,
            'vcek': self.vcek,
            'guest_visible_workarounds': self.guest_visible_workarounds,
            'id_block': self.id_block,
            'id_auth': self.id_auth,
            'host_data': self.host_data,
            'mr_config_id': self.mr_config_id,
            'mr_owner': self.mr_owner,
            'mr_owner_config': self.mr_owner_config,
            'quote_generation_service': self.quote_generation_service,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'LaunchSecurityConfig':
        """从字典创建实例,支持两种格式:
        1. Tab 格式:cbitpos_enabled/cbitpos_value, reduced_phys_bits_enabled/reduced_phys_bits_value
        2. 直接格式:cbitpos, reduced_phys_bits
        """
        # 支持 Tab 输出的格式 (cbitpos_enabled/cbitpos_value)
        cbitpos_enabled = data.get('cbitpos_enabled', False)
        cbitpos_value = data.get('cbitpos_value', '')

        # 如果没有 cbitpos_enabled,尝试使用旧格式 cbitpos
        if 'cbitpos_enabled' not in data and 'cbitpos' in data:
            cbitpos_val = data.get('cbitpos')
            if cbitpos_val is not None:
                cbitpos_enabled = True
                cbitpos_value = str(cbitpos_val)

        reduced_phys_bits_enabled = data.get('reduced_phys_bits_enabled', False)
        reduced_phys_bits_value = data.get('reduced_phys_bits_value', '')

        # 如果没有 reduced_phys_bits_enabled,尝试使用旧格式 reduced_phys_bits
        if 'reduced_phys_bits_enabled' not in data and 'reduced_phys_bits' in data:
            rpb_val = data.get('reduced_phys_bits')
            if rpb_val is not None:
                reduced_phys_bits_enabled = True
                reduced_phys_bits_value = str(rpb_val)

        return cls(
            sec_type=data.get('type', data.get('sec_type', 'none')),
            policy=data.get('policy', ''),
            cbitpos_enabled=cbitpos_enabled,
            cbitpos_value=cbitpos_value,
            reduced_phys_bits_enabled=reduced_phys_bits_enabled,
            reduced_phys_bits_value=reduced_phys_bits_value,
            kernel_hashes=data.get('kernel_hashes', False),
            dh_cert=data.get('dh_cert', ''),
            session=data.get('session', ''),
            author_key=data.get('author_key', False),
            vcek=data.get('vcek', True),
            guest_visible_workarounds=data.get('guest_visible_workarounds', ''),
            id_block=data.get('id_block', ''),
            id_auth=data.get('id_auth', ''),
            host_data=data.get('host_data', ''),
            mr_config_id=data.get('mr_config_id', ''),
            mr_owner=data.get('mr_owner', ''),
            mr_owner_config=data.get('mr_owner_config', ''),
            quote_generation_service=data.get(
                'quote_generation_service', '/var/run/tdx-qgs/qgs.socket'
            ),
        )

    def is_enabled(self) -> bool:
        """是否启用了启动安全."""
        return self.sec_type != 'none'

    def is_sev(self) -> bool:
        """是否为 AMD SEV 类型."""
        return self.sec_type == 'sev'

    def is_sev_snp(self) -> bool:
        """是否为 AMD SEV-SNP 类型."""
        return self.sec_type == 'sev-snp'

    def is_tdx(self) -> bool:
        """是否为 Intel TDX 类型."""
        return self.sec_type == 'tdx'

    def is_s390_pv(self) -> bool:
        """是否为 IBM s390-pv 类型."""
        return self.sec_type == 's390-pv'
