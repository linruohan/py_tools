"""测试虚拟机配置类"""

from model.vm_model.domain import Domain
from model.vm_model.os import OS, Boot, Loader, Nvram
from model.vm_model.devices_config import DevicesConfig
from model.vm_model.features import Features, HypervFeature, KVMFeature
from model.vm_model.cpu.numa import NUMA, NumaNode
from model.vm_model.memoryBacking import MemoryBacking, HugePage
from model.vm_model.cputune import CpuTune, VCPUPin
from model.vm_model.numatune import NumaTune
from model.vm_model.memtune import MemTune
from model.vm_model.blkiotune import BlkioTune
from model.vm_model.throttlegroups import ThrottleGroups, ThrottleGroup
from model.vm_model.resource import Resources, FibreChannel
from model.vm_model.sysinfo import SysInfo, SMBIOSSystem


def test_domain_config():
    """测试域配置"""
    print("测试域配置...")
    
    # 创建一个完整的域配置
    domain = Domain(
        name="test-vm",
        uuid="4dea22b3-1d52-d8f3-2516-782e98ab3fa0",
        hwuuid="5dea22b3-1d52-d8f3-2516-782e98ab3fa1",
        genid="6dea22b3-1d52-d8f3-2516-782e98ab3fa2",
        title="Test VM",
        description="This is a test VM",
        on_poweroff="destroy",
        on_reboot="restart",
        on_crash="destroy",
        on_lockfailure="poweroff"
    )
    
    # 测试转换为配置字典
    config = domain.to_config()
    print("配置字典创建成功")
    
    # 测试从配置字典创建
    new_domain = Domain.from_config(config)
    print("从配置字典创建域成功")
    
    # 测试转换为 XML 元素
    xml_element = domain.to_xml_element()
    print("XML 元素创建成功")
    
    print("域配置测试通过！\n")


def test_os_config():
    """测试操作系统配置"""
    print("测试操作系统配置...")
    
    # 创建 OS 配置
    os = OS(
        type="hvm",
        arch="x86_64",
        machine="q35",
        firmware="efi",
        boot=[Boot(dev="hd"), Boot(dev="cdrom")],
        loader=Loader(
            path="/usr/share/OVMF/OVMF_CODE.fd",
            readonly=True,
            secure=True,
            type="pflash"
        ),
        nvram=Nvram(
            path="/var/lib/libvirt/nvram/test_VARS.fd",
            template="/usr/share/OVMF/OVMF_VARS.fd"
        )
    )
    
    print("OS 配置创建成功")
    print("操作系统配置测试通过！\n")


def test_features_config():
    """测试特性配置"""
    print("测试特性配置...")
    
    # 创建特性配置
    features = Features(
        acpi=None,
        apic=None,
        hyperv=[
            HypervFeature(name="relaxed", state="on"),
            HypervFeature(name="vapic", state="on"),
            HypervFeature(name="spinlocks", state="on", retries=4096)
        ],
        kvm=[
            KVMFeature(name="hidden", state="on")
        ]
    )
    
    # 测试转换为字典
    features_dict = features.to_dict()
    print("特性配置字典创建成功")
    
    # 测试从字典创建
    new_features = Features.from_dict(features_dict)
    print("从字典创建特性配置成功")
    
    print("特性配置测试通过！\n")


def test_numa_config():
    """测试 NUMA 配置"""
    print("测试 NUMA 配置...")
    
    # 创建 NUMA 配置
    numa = NUMA(
        nodes=[
            NumaNode(
                id=0,
                memory=512000,
                unit="KiB",
                cpus="0-3"
            ),
            NumaNode(
                id=1,
                memory=512000,
                unit="KiB",
                cpus="4-7"
            )
        ]
    )
    
    print("NUMA 配置创建成功")
    print("NUMA 配置测试通过！\n")


def test_memory_backing_config():
    """测试内存后端配置"""
    print("测试内存后端配置...")
    
    # 创建内存后端配置
    memory_backing = MemoryBacking(
        hugepages=[
            HugePage(size=1, unit="G", nodeset="0-3"),
            HugePage(size=2, unit="M", nodeset="4")
        ],
        locked=True,
        discard=True
    )
    
    print("内存后端配置创建成功")
    print("内存后端配置测试通过！\n")


def test_cputune_config():
    """测试 CPU 调优配置"""
    print("测试 CPU 调优配置...")
    
    # 创建 CPU 调优配置
    cputune = CpuTune(
        vcpu_pins=[
            VCPUPin(vcpu=0, cpuset="0-1"),
            VCPUPin(vcpu=1, cpuset="2-3")
        ],
        shares=2048,
        period=1000000,
        quota=-1
    )
    
    print("CPU 调优配置创建成功")
    print("CPU 调优配置测试通过！\n")


def test_throttlegroups_config():
    """测试节流组配置"""
    print("测试节流组配置...")
    
    # 创建节流组配置
    throttlegroups = ThrottleGroups(
        throttlegroups=[
            ThrottleGroup(
                name="limit0",
                total_bytes_sec=10000000,
                read_iops_sec=400000,
                write_iops_sec=100000
            )
        ]
    )
    
    print("节流组配置创建成功")
    print("节流组配置测试通过！\n")


def test_resource_config():
    """测试资源配置"""
    print("测试资源配置...")
    
    # 创建资源配置
    resources = Resources(
        partition="/virtualmachines/production",
        fibrechannel=FibreChannel(appid="userProvidedID")
    )
    
    print("资源配置创建成功")
    print("资源配置测试通过！\n")


def test_sysinfo_config():
    """测试系统信息配置"""
    print("测试系统信息配置...")
    
    # 创建系统信息配置
    sysinfo = SysInfo(
        type="smbios",
        system=SMBIOSSystem(
            manufacturer="Fedora",
            product="Virt-Manager",
            version="0.9.4"
        )
    )
    
    print("系统信息配置创建成功")
    print("系统信息配置测试通过！\n")


if __name__ == "__main__":
    print("开始测试虚拟机配置类...\n")
    
    test_domain_config()
    test_os_config()
    test_features_config()
    test_numa_config()
    test_memory_backing_config()
    test_cputune_config()
    test_throttlegroups_config()
    test_resource_config()
    test_sysinfo_config()
    
    print("所有测试通过！")
