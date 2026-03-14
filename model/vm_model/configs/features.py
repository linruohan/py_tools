"""Features 配置 - 整合策略模式."""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


@dataclass
class Feature:
    """特性配置"""

    name: str
    policy: Optional[str] = None  # require, optional, disable
    present: Optional[bool] = None
    state: Optional[str] = None  # on, off
    value: Optional[str] = None
    retries: Optional[int] = None


@dataclass
class HypervFeature:
    """Hyper-V 特性配置"""

    name: str  # relaxed, vapic, spinlocks, vpindex, runtime, synic, stimer, reset, vendor_id, frequencies, reenlightenment, tlbflush, ipi, evmcs, avic, emsr_bitmap, xmm_input
    state: str = 'on'  # on, off
    retries: Optional[int] = None
    direct: Optional[bool] = None  # 用于 stimer, tlbflush
    extended: Optional[bool] = None  # 用于 tlbflush
    value: Optional[str] = None  # 用于 vendor_id


@dataclass
class KVMFeature:
    """KVM 特性配置"""

    name: str  # hidden, hint-dedicated, poll-control, pv-ipi, dirty-ring
    state: str = 'on'  # on, off
    size: Optional[int] = None  # 用于 dirty-ring


@dataclass
class XenFeature:
    """Xen 特性配置"""

    name: str  # e820_host, passthrough
    state: str = 'on'  # on, off
    mode: Optional[str] = None  # 用于 passthrough (sync_pt, share_pt)


@dataclass
class TSeg:
    """SMM TSEG 配置"""

    size: int = 0
    unit: str = 'MiB'  # b, bytes, KB, k, KiB, MB, M, MiB, GB, G, GiB, TB, T, TiB


@dataclass
class HPT:
    """HPT (Hash Page Table) 配置"""

    resizing: str = 'enabled'  # enabled, disabled, required
    maxpagesize: Optional[Dict[str, Any]] = None


@dataclass
class ACPI:
    """ACPI 配置"""

    state: str = 'on'  # on, off
    tables: List[Dict[str, str]] = field(default_factory=list)  # ACPI 表列表


@dataclass
class APIC:
    """APIC 配置"""

    state: str = 'on'  # on, off
    eoi: Optional[str] = None  # on, off


@dataclass
class PMU:
    """PMU (Performance Monitoring Unit) 配置"""

    state: str = 'on'  # on, off


@dataclass
class VMPort:
    """VMPort 配置"""

    state: str = 'on'  # on, off


@dataclass
class GIC:
    """GIC (General Interrupt Controller) 配置"""

    version: Optional[str] = None  # 2, 3, host


@dataclass
class SMM:
    """SMM (System Management Mode) 配置"""

    state: str = 'on'  # on, off
    tseg: Optional[TSeg] = None


@dataclass
class IOAPIC:
    """IOAPIC 配置"""

    driver: str = 'kvm'  # kvm, qemu


@dataclass
class Features:
    """特性集合配置"""

    # 基础特性
    pae: Optional[str] = None  # on, off
    acpi: Optional[ACPI] = None
    apic: Optional[APIC] = None
    hap: Optional[str] = None  # on, off

    # Xen 相关
    viridian: Optional[str] = None  # on, off
    privnet: Optional[str] = None  # on, off

    # Hyper-V 相关
    hyperv: List[HypervFeature] = field(default_factory=list)
    hyperv_mode: Optional[str] = None  # custom, passthrough, host-model

    # KVM 相关
    kvm: List[KVMFeature] = field(default_factory=list)
    pvspinlock: Optional[str] = None  # on, off

    # Xen 相关
    xen: List[XenFeature] = field(default_factory=list)

    # 平台相关
    pmu: Optional[PMU] = None
    vmport: Optional[VMPort] = None
    gic: Optional[GIC] = None
    smm: Optional[SMM] = None
    ioapic: Optional[IOAPIC] = None

    # pSeries 相关
    hpt: Optional[HPT] = None
    vmcoreinfo: Optional[str] = None  # on, off
    htm: Optional[str] = None  # on, off
    nested_hv: Optional[str] = None  # on, off
    ccf_assist: Optional[str] = None  # on, off

    # bhyve 相关
    msrs: Optional[Dict[str, str]] = None  # unknown: ignore/fault

    # TCG 相关
    tcg: Optional[Dict[str, Any]] = None

    # 其他
    async_teardown: Optional[str] = None  # on, off
    ras: Optional[str] = None  # on, off
    ps2: Optional[str] = None  # on, off
    aia: Optional[Dict[str, Any]] = None
    virtualization: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Features':
        """从字典创建"""
        # ACPI
        acpi_data = data.get('acpi')
        acpi = None
        if acpi_data:
            acpi = ACPI(
                state=acpi_data.get('state', 'on'),
                tables=acpi_data.get('tables', []),
            )

        # APIC
        apic_data = data.get('apic')
        apic = None
        if apic_data:
            apic = APIC(
                state=apic_data.get('state', 'on'),
                eoi=apic_data.get('eoi'),
            )

        # PMU
        pmu_data = data.get('pmu')
        pmu = None
        if pmu_data:
            pmu = PMU(state=pmu_data.get('state', 'on'))

        # VMPort
        vmport_data = data.get('vmport')
        vmport = None
        if vmport_data:
            vmport = VMPort(state=vmport_data.get('state', 'on'))

        # GIC
        gic_data = data.get('gic')
        gic = None
        if gic_data:
            gic = GIC(version=gic_data.get('version'))

        # SMM
        smm_data = data.get('smm')
        smm = None
        if smm_data:
            tseg_data = smm_data.get('tseg')
            tseg = None
            if tseg_data:
                tseg = TSeg(
                    size=tseg_data.get('size', 0),
                    unit=tseg_data.get('unit', 'MiB'),
                )
            smm = SMM(
                state=smm_data.get('state', 'on'),
                tseg=tseg,
            )

        # IOAPIC
        ioapic_data = data.get('ioapic')
        ioapic = None
        if ioapic_data:
            ioapic = IOAPIC(driver=ioapic_data.get('driver', 'kvm'))

        # HPT
        hpt_data = data.get('hpt')
        hpt = None
        if hpt_data:
            hpt = HPT(
                resizing=hpt_data.get('resizing', 'enabled'),
                maxpagesize=hpt_data.get('maxpagesize'),
            )

        # Hyper-V 特性
        hyperv_data = data.get('hyperv', [])
        hyperv = [HypervFeature(**h) if isinstance(h, dict) else h for h in hyperv_data]

        # KVM 特性
        kvm_data = data.get('kvm', [])
        kvm = [KVMFeature(**k) if isinstance(k, dict) else k for k in kvm_data]

        # Xen 特性
        xen_data = data.get('xen', [])
        xen = [XenFeature(**x) if isinstance(x, dict) else x for x in xen_data]

        return cls(
            pae=data.get('pae'),
            acpi=acpi,
            apic=apic,
            hap=data.get('hap'),
            viridian=data.get('viridian'),
            privnet=data.get('privnet'),
            hyperv=hyperv,
            hyperv_mode=data.get('hyperv_mode'),
            kvm=kvm,
            pvspinlock=data.get('pvspinlock'),
            xen=xen,
            pmu=pmu,
            vmport=vmport,
            gic=gic,
            smm=smm,
            ioapic=ioapic,
            hpt=hpt,
            vmcoreinfo=data.get('vmcoreinfo'),
            htm=data.get('htm'),
            nested_hv=data.get('nested_hv'),
            ccf_assist=data.get('ccf_assist'),
            msrs=data.get('msrs'),
            tcg=data.get('tcg'),
            async_teardown=data.get('async_teardown'),
            ras=data.get('ras'),
            ps2=data.get('ps2'),
            aia=data.get('aia'),
            virtualization=data.get('virtualization'),
        )

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        result = {}

        if self.pae:
            result['pae'] = self.pae
        if self.acpi:
            result['acpi'] = {
                'state': self.acpi.state,
                'tables': self.acpi.tables,
            }
        if self.apic:
            result['apic'] = {
                'state': self.apic.state,
                'eoi': self.apic.eoi,
            }
        if self.hap:
            result['hap'] = self.hap
        if self.viridian:
            result['viridian'] = self.viridian
        if self.privnet:
            result['privnet'] = self.privnet
        if self.hyperv:
            result['hyperv'] = [
                {
                    'name': h.name,
                    'state': h.state,
                    'retries': h.retries,
                    'direct': h.direct,
                    'extended': h.extended,
                    'value': h.value,
                }
                for h in self.hyperv
            ]
        if self.hyperv_mode:
            result['hyperv_mode'] = self.hyperv_mode
        if self.kvm:
            result['kvm'] = [
                {
                    'name': k.name,
                    'state': k.state,
                    'size': k.size,
                }
                for k in self.kvm
            ]
        if self.pvspinlock:
            result['pvspinlock'] = self.pvspinlock
        if self.xen:
            result['xen'] = [
                {
                    'name': x.name,
                    'state': x.state,
                    'mode': x.mode,
                }
                for x in self.xen
            ]
        if self.pmu:
            result['pmu'] = {'state': self.pmu.state}
        if self.vmport:
            result['vmport'] = {'state': self.vmport.state}
        if self.gic:
            result['gic'] = {'version': self.gic.version}
        if self.smm:
            smm_dict = {'state': self.smm.state}
            if self.smm.tseg:
                smm_dict['tseg'] = {
                    'size': self.smm.tseg.size,
                    'unit': self.smm.tseg.unit,
                }
            result['smm'] = smm_dict
        if self.ioapic:
            result['ioapic'] = {'driver': self.ioapic.driver}
        if self.hpt:
            hpt_dict = {'resizing': self.hpt.resizing}
            if self.hpt.maxpagesize:
                hpt_dict['maxpagesize'] = self.hpt.maxpagesize
            result['hpt'] = hpt_dict
        if self.vmcoreinfo:
            result['vmcoreinfo'] = self.vmcoreinfo
        if self.htm:
            result['htm'] = self.htm
        if self.nested_hv:
            result['nested_hv'] = self.nested_hv
        if self.ccf_assist:
            result['ccf_assist'] = self.ccf_assist
        if self.msrs:
            result['msrs'] = self.msrs
        if self.tcg:
            result['tcg'] = self.tcg
        if self.async_teardown:
            result['async_teardown'] = self.async_teardown
        if self.ras:
            result['ras'] = self.ras
        if self.ps2:
            result['ps2'] = self.ps2
        if self.aia:
            result['aia'] = self.aia
        if self.virtualization:
            result['virtualization'] = self.virtualization

        return result
