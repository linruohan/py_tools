# 域 XML 格式

[toc]

本节描述用于表示域的 XML 格式，根据运行的域类型和启动它们的选项，格式会有所不同。有关特定于 hypervisor 的详细信息，请参考 [驱动文档](https://www.libvirt.org/drivers.html)

# [元素和属性概述](https://www.libvirt.org/formatdomain.html#id1)

所有虚拟机所需的根元素名为 domain。它有两个属性，type 指定用于运行域的 hypervisor。允许的值是特定于驱动程序的，但包括 "xen"、"kvm"、"hvf"（自 8.1.0 和 QEMU 2.12 起）、"qemu" 和 "lxc"。第二个属性是 id，它是运行中的客户机的唯一整数标识符。非活动机器没有 id 值。

## 1 [一般元数据](https://www.libvirt.org/formatdomain.html#id2)

```
<domain type='kvm' id='1'>
  <name>MyGuest</name>
  <uuid>4dea22b3-1d52-d8f3-2516-782e98ab3fa0</uuid>
  <genid>43dc0cf8-809b-4adb-9bea-a9abb5f3d90e</genid>
  <title>A short description - title - of the domain</title>
  <description>Some human readable description</description>
  <metadata>
    <app1:foo xmlns:app1="http://app1.org/app1/">..</app1:foo>
    <app2:bar xmlns:app2="http://app1.org/app2/">..</app2:bar>
  </metadata>
  ...
```

- name

  name 元素的内容为虚拟机提供一个简短名称。此名称应仅由字母数字字符组成，并且在单个主机的范围内必须是唯一的。它通常用于形成用于存储持久配置文件的文件名。自 0.0.1 起

- uuid

  uuid 元素的内容为虚拟机提供全局唯一标识符。格式必须符合 RFC 4122，例如 3e3fce45-4f53-4fa7-bb32-11f34168b82b。如果在定义/创建新机器时省略，则会生成随机 UUID。自 0.0.1 起 自 0.8.7 起，也可以通过 [SMBIOS 系统信息](https://www.libvirt.org/formatdomain.html#smbios-system-information) 规范提供 UUID。

- hwuuid

  可选的 hwuuid 元素可用于提供替代 UUID，用于从上面的域 uuid 识别虚拟机。使用 hwuuid 元素与通过 [SMBIOS 系统信息](https://www.libvirt.org/formatdomain.html#smbios-system-information) 规范简单提供替代 UUID 之间的区别在于，hwuuid 会影响所有向客户机公开 UUID 的设备。自 11.7.0 起仅 QEMU/KVM

- genid

  自 4.4.0 起，genid 元素可用于添加虚拟机生成 ID，该 ID 使用与 uuid 相同的格式公开 128 位加密随机整数值标识符，称为全局唯一标识符 (GUID)。该值用于帮助通知客户机操作系统虚拟机何时重新执行已经执行过的操作，例如：VM 开始执行快照 VM 从备份中恢复 VM 在灾难恢复环境中故障转移 VM 被导入、复制或克隆 客户机操作系统注意到更改，然后能够通过将其分布式数据库的副本标记为脏、重新初始化其随机数生成器等方式做出适当的反应。libvirt XML 解析器将接受提供的 GUID 值或仅接受 <genid/>，在这种情况下，将生成 GUID 并保存在 XML 中。对于上述转换，libvirt 将在重新执行前更改 GUID。

- title

  可选元素 title 为域提供简短描述的空间。title 不应包含任何换行符。自 0.9.10 起。

- description

  description 元素的内容提供虚拟机的人类可读描述。这些数据不会被 libvirt 以任何方式使用，它可以包含用户想要的任何信息。自 0.7.2 起

- metadata

  metadata 节点可由应用程序用于以 XML 节点/树的形式存储自定义元数据。应用程序必须在其 XML 节点/树上使用自定义命名空间，每个命名空间只有一个顶级元素（如果应用程序需要结构，它们应该在其命名空间元素中有子元素）。自 0.9.10 起

## 2 [操作系统引导](https://www.libvirt.org/formatdomain.html#id3)

有多种不同的方式引导虚拟机，每种方式都有其优缺点。

### 2.1 [客户机固件](https://www.libvirt.org/formatdomain.html#id4)

通过客户机固件引导适用于支持完全虚拟化的 hypervisor。在这种情况下，固件具有引导顺序优先级（软盘、硬盘、光盘、网络），决定从哪里获取/查找引导映像。

```
<!-- Xen with fullvirt loader -->
...
<os>
  <type>hvm</type>
  <loader>/usr/lib/xen/boot/hvmloader</loader>
  <boot dev='hd'/>
</os>
...

<!-- QEMU with default firmware, serial console and SMBIOS -->
...
<os>
  <type>hvm</type>
  <boot dev='cdrom'/>
  <bootmenu enable='yes' timeout='3000'/>
  <smbios mode='sysinfo'/>
  <bios useserial='yes' rebootTimeout='0'/>
</os>
...

<!-- QEMU with UEFI manual firmware and secure boot -->
...
<os>
  <type>hvm</type>
  <loader readonly='yes' secure='yes' type='pflash'>/usr/share/OVMF/OVMF_CODE.fd</loader>
  <nvram template='/usr/share/OVMF/OVMF_VARS.fd'>/var/lib/libvirt/nvram/guest_VARS.fd</nvram>
  <boot dev='hd'/>
</os>
...

<!-- QEMU with UEFI manual firmware, secure boot and with NVRAM type 'file'-->
...
<os>
  <type>hvm</type>
  <loader readonly='yes' secure='yes' type='pflash'>/usr/share/OVMF/OVMF_CODE.fd</loader>
  <nvram type='file' template='/usr/share/OVMF/OVMF_VARS.fd'>
    <source file='/var/lib/libvirt/nvram/guest_VARS.fd'/>
  </nvram>
  <boot dev='hd'/>
</os>
...

<!-- QEMU with UEFI manual firmware, secure boot and with network backed NVRAM'-->
...
<os>
  <type>hvm</type>
  <loader readonly='yes' secure='yes' type='pflash'>/usr/share/OVMF/OVMF_CODE.fd</loader>
  <nvram type='network'>
    <source protocol='iscsi' name='iqn.2013-07.com.example:iscsi-nopool/0'>
      <host name='example.com' port='6000'/>
      <auth username='myname'>
        <secret type='iscsi' usage='mycluster_myname'/>
      </auth>
    </source>
  </nvram>
  <boot dev='hd'/>
</os>
...

<!-- QEMU with automatic UEFI firmware and secure boot -->
...
<os firmware='efi'>
  <type>hvm</type>
  <loader secure='yes'/>
  <boot dev='hd'/>
</os>
...

<!-- QEMU with automatic UEFI stateless firmware for AMD SEV -->
...
<os firmware='efi'>
  <type>hvm</type>
  <loader stateless='yes'/>
  <boot dev='hd'/>
</os>
...
```

- firmware

  firmware 属性允许管理应用程序自动填充 <loader/> 和 <nvram/> 或 <varstore/> 元素，并可能启用所选固件所需的一些功能。接受的值为 bios 和 efi。选择过程扫描指定位置中描述已安装固件映像的文件，并使用最能满足域要求的特定文件。优先顺序（从通用到最特定）的位置是：/usr/share/qemu/firmware /etc/qemu/firmware $XDG_CONFIG_HOME/qemu/firmware 有关更多信息，请参考 QEMU 存储库中 docs/interop/firmware.json 中描述的固件元数据规范。普通用户不需要担心。自 5.2.0 起（仅 QEMU 和 KVM）对于 VMware 客户机，当客户机使用 UEFI 时设置为 efi，使用 BIOS 时不设置。自 5.3.0 起（VMware ESX 和 Workstation/Player）

- type

  type 元素的内容指定要在虚拟机中引导的操作系统类型。hvm 表示操作系统是设计为在裸机上运行的，因此需要完全虚拟化。linux（命名不佳！）指的是支持 Xen 3 hypervisor 客户机 ABI 的操作系统。还有两个可选属性，arch 指定要虚拟化的 CPU 架构，machine 指的是机器类型。[Capabilities XML](https://www.libvirt.org/formatcaps.html) 提供了这些允许值的详细信息。如果省略 arch，则对于大多数 hypervisor 驱动程序，将选择主机本机架构。但是，对于 test、ESX 和 VMWare hypervisor 驱动程序，即使在 x86_64 主机上，也始终会选择 i686 架构。自 0.0.1 起

- firmware

  自 7.2.0 起仅 QEMU/KVM 使用固件自动选择时，固件中启用了不同的功能。功能列表可用于限制应为 VM 自动选择哪种固件。可以使用零个或多个 feature 元素指定功能列表。Libvirt 在选择固件时将只考虑列出的功能，忽略其余功能。feature 强制属性列表：enabled（接受的值为 yes 和 no）用于告诉 libvirt 在自动选择的固件中是否必须启用该功能 name 功能的名称，功能列表：enrolled-keys 所选 nvram 模板是否已注册默认证书。具有 Secure Boot 功能但未注册密钥的固件也会成功引导未签名的二进制文件。仅对具有 Secure Boot 功能的固件有效。secure-boot 固件是否实现 UEFI Secure boot 功能。

- loader

  可选的 loader 标签指的是固件 blob，由绝对路径指定，用于协助域创建过程。它被 Xen 完全虚拟化域使用，以及为 QEMU/KVM 域设置 QEMU BIOS 文件路径。Xen 自 0.1.0 起，QEMU/KVM 自 0.9.12 起 然后，自 1.2.8 起，该元素可以有两个可选属性：readonly（接受的值为 yes 和 no）以反映映像应该是可写的还是只读的。第二个属性 type 接受值 rom 和 pflash。它告诉 hypervisor 文件应该映射到客户机内存中的什么位置。例如，如果 loader 路径指向 UEFI 映像，type 应该是 pflash。此外，一些固件可能实现 Secure boot 功能。属性 secure 可用于告诉 hypervisor 固件能够实现 Secure Boot 功能。它不能用于在固件中启用或禁用该功能本身。自 2.1.0 起。如果 loader 被标记为只读，那么对于 UEFI，假设会有可用的可写 NVRAM。但是，在某些情况下，可能希望 loader 在没有任何 NVRAM 的情况下运行，在关闭时丢弃任何配置更改。stateless 标志（自 8.6.0 起）可用于控制此行为，当设置为 yes 时，永远不会创建 NVRAM。启用固件自动选择时，format 属性可用于告诉 libvirt 只考虑特定格式的固件构建。支持的值为 raw 和 qcow2。自 9.2.0 起（仅 QEMU）

- nvram

  一些 UEFI 固件可能希望使用非易失性内存来存储一些变量。在主机上，这表示为一个文件，该文件的绝对路径存储在此元素中。此外，当域启动时，libvirt 会复制所谓的主 NVRAM 存储文件，该文件要么由固件自动选择过程选择，要么在 qemu.conf 中定义。如果需要，可以使用 template 属性覆盖自动选择的 NVRAM 模板，并使用 templateFormat 指定模板文件的格式（当前支持 raw 和 qcow2）。使用固件自动选择时，templateFormat 字段反映所选模板的格式。自 10.10.0 起（仅 QEMU）注意，对于瞬态域，如果 NVRAM 文件是由 libvirt 创建的，它会被留下，管理应用程序有责任保存和删除文件（如果需要持久化）。自 1.2.8 起 自 8.5.0 起，该元素可以具有 type 属性（接受值 file、block 和 network），在这种情况下，NVRAM 存储由 <source> 子元素描述，其语法与磁盘的源相同。请参阅 [硬盘、软盘、光盘](https://www.libvirt.org/formatdomain.html#hard-drives-floppy-disks-cdroms)。对于基于块的 NVRAM 映像，可能需要确保块设备具有基于 hypervisor 期望的正确客户机可见大小。这可能需要使用允许任意磁盘大小的非原始格式映像。**注意：** 网络备份的 NVRAM 变量不会从模板实例化，用户有责任提供有效的 NVRAM 映像。此元素支持 format 属性，指定 NVRAM 映像的格式。自 9.2.0 起（仅 QEMU）注意，hypervisor 可能不支持如果 format 与 templateFormat 不同，则自动填充 nvram，或者可能只支持特定格式。如果 loader 被标记为 stateless，则提供此元素无效。

- varstore

  这与上面描述的 <nvram/> 元素工作方式大致相同，不同之处在于变量存储由 uefi-vars QEMU 设备处理，而不是由 pflash 设备支持。自 12.1.0 起（仅 QEMU）path 属性包含存储变量的域特定文件的路径，而 template 属性指向可以从中（重新）生成域特定文件的模板。假设存在必要的 JSON 固件描述符文件，libvirt 将自动填充这两个属性。在非 x86 架构（如 aarch64）上使用 <varstore/> 而不是 <nvram/> 特别有用，因为它是使 Secure Boot 工作的唯一方式。它也可以在 x86 上使用，这样做可以在不需要使用 SMM 模拟的情况下保持 UEFI 认证变量不被篡改。

- boot

  dev 属性采用 "fd"、"hd"、"cdrom" 或 "network" 之一的值，用于指定要考虑的下一个引导设备。boot 元素可以重复多次，以设置要依次尝试的引导设备的优先级列表。相同类型的多个设备根据其目标排序，同时保留总线顺序。定义域后，libvirt（通过 virDomainGetXMLDesc）返回的 XML 配置按排序顺序列出设备。排序后，第一个设备被标记为可引导。因此，例如，配置为从 "hd" 引导并分配了 vdb、hda、vda 和 hdc 磁盘的域将从 vda 引导（排序后的列表是 vda、vdb、hda、hdc）。具有 hdc、vda、vdb 和 hda 磁盘的类似域将从 hda 引导（排序后的磁盘是：hda、hdc、vda、vdb）。这可能很难按预期方式配置，这就是为什么引入了每个设备的 boot 元素（请参阅下面的 [硬盘、软盘、光盘](https://www.libvirt.org/formatdomain.html#hard-drives-floppy-disks-cdroms)、[网络接口](https://www.libvirt.org/formatdomain.html#network-interfaces) 和 [主机设备分配](https://www.libvirt.org/formatdomain.html#host-device-assignment) 部分），它们是提供对引导顺序完全控制的首选方式。boot 元素和每个设备的 boot 元素是互斥的。自 0.1.3 起，每个设备的 boot 自 0.8.8 起

- smbios

  如何填充在客户机中可见的 SMBIOS 信息。必须指定 mode 属性，它可以是 "emulate"（让 hypervisor 生成所有值）、"host"（从主机的 SMBIOS 值复制所有 Block 0 和 Block 1，除了 UUID；[virConnectGetSysinfo](https://www.libvirt.org/html/libvirt-libvirt-host.html#virConnectGetSysinfo) 调用可用于查看复制了哪些值），或 "sysinfo"（使用 [SMBIOS 系统信息](https://www.libvirt.org/formatdomain.html#smbios-system-information) 元素中的值）。如果未指定，则使用 hypervisor 默认值。自 0.8.7 起

到目前为止，BIOS/UEFI 配置旋钮足够通用，可以由大多数（如果不是全部）固件实现。然而，从现在开始，并不是每一个设置都对所有固件有意义。例如，rebootTimeout 对 UEFI 没有意义，useserial 可能无法与不在串行线上产生任何输出的 BIOS 固件一起使用，等等。此外，固件通常不会导出其功能供 libvirt（或用户）检查。并且它们的功能集可能会随着每个新版本而变化。因此，建议用户在依赖生产环境中使用的设置之前先尝试它们。

- bootmenu

  是否在客户机启动时启用交互式引导菜单提示。enable 属性可以是 "yes" 或 "no"。如果未指定，则使用 hypervisor 默认值。自 0.8.3 起 附加属性 timeout 采用引导菜单应等待直到超时的毫秒数。允许的值是 [0, 65535] 范围内的数字，除非 enable 设置为 "yes"，否则将被忽略。自 1.2.8 起

- bios

  此元素具有 useserial 属性，可能的值为 yes 或 no。它启用或禁用串行图形适配器，允许用户在串行端口上查看 BIOS 消息。因此，需要定义 [串行端口](https://www.libvirt.org/formatdomain.html#serial-port)。自 0.9.4 起。rebootTimeout 属性（自 0.10.2 起，仅 QEMU）控制在引导失败时（根据 BIOS）客户机是否以及多长时间后应该再次开始引导。该值以毫秒为单位，最大值为 65535，特殊值 -1 禁用重新引导。

### 2.2 [主机引导加载程序](https://www.libvirt.org/formatdomain.html#id5)

采用半虚拟化的 hypervisor 通常不模拟 BIOS，而是由主机负责启动操作系统引导。这可能使用主机中的伪引导加载程序来提供选择客户机内核的接口。例如，Xen 的 pygrub。Bhyve hypervisor 也使用主机引导加载程序，要么是 bhyveload 要么是 grub-bhyve。

```
...
<bootloader>/usr/bin/pygrub</bootloader>
<bootloader_args>--append single</bootloader_args>
...
```

- bootloader

  bootloader 元素的内容提供主机 OS 中引导加载程序可执行文件的完全限定路径。将运行此引导加载程序以选择要引导的内核。引导加载程序的所需输出取决于所使用的 hypervisor。自 0.1.0 起

- bootloader_args

  可选的 bootloader_args 元素允许将命令行参数传递给引导加载程序。自 0.2.3 起

### 2.3 [直接内核引导](https://www.libvirt.org/formatdomain.html#id6)

安装新的客户机 OS 时，通常有用的是直接从存储在主机 OS 中的内核和 initrd 引导，允许将命令行参数直接传递给安装程序。这种能力通常可用于半虚拟化和完全虚拟化的客户机。

```
...
<os>
  <type>hvm</type>
  <loader>/usr/lib/xen/boot/hvmloader</loader>
  <kernel>/root/f8-i386-vmlinuz</kernel>
  <initrd>/root/f8-i386-initrd</initrd>
  <cmdline>console=ttyS0 ks=http://example.com/f8-i386/os/</cmdline>
  <shim>/path/to/shim.efi</shim>
  <dtb>/root/ppc.dtb</dtb>
</os>
...
```

- type

  此元素具有与前面 [客户机固件](https://www.libvirt.org/formatdomain.html#guest-firmware) 部分中描述的相同语义。

- loader

  此元素具有与前面 [客户机固件](https://www.libvirt.org/formatdomain.html#guest-firmware) 部分中描述的相同语义。

- kernel

  此元素的内容指定主机 OS 中内核映像的完全限定路径。

- initrd

  此元素的内容指定主机 OS 中（可选）ramdisk 映像的完全限定路径。

- cmdline

  此元素的内容指定在引导时传递给内核（或安装程序）的参数。这通常用于指定备用主控制台（例如串行端口），或安装介质源 / kickstart 文件

- shim

  使用指定的完全限定路径加载初始 UEFI 引导加载程序，该引导加载程序在安全引导环境下处理链接到受信任的完整引导加载程序。

- dtb

  此元素的内容指定主机 OS 中（可选）设备树二进制（dtb）映像的完全限定路径。自 1.0.4 起

### 2.4 [容器引导](https://www.libvirt.org/formatdomain.html#id7)

使用基于容器的虚拟化引导域时，不需要内核/引导映像，而是需要使用 init 元素指定 init 二进制文件的路径。默认情况下，它将在没有参数的情况下启动。要指定初始 argv，请使用 initarg 元素，根据需要重复多次。如果设置了 cmdline 元素，它将用于提供等效于 /proc/cmdline 的内容，但不会影响 init argv。

要设置环境变量，请使用 initenv 元素，每个变量一个。

要为 init 设置自定义工作目录，请使用 initdir 元素。

要以给定用户或组运行 init 命令，请分别使用 inituser 或 initgroup 元素。这两个元素都可以提供用户（或组）id 或名称。在用户或组 id 前加上 + 将强制将其视为数值。否则，它将首先尝试作为用户或组名称。

```
<os>
  <type arch='x86_64'>exe</type>
  <init>/bin/systemd</init>
  <initarg>--unit</initarg>
  <initarg>emergency.service</initarg>
  <initenv name='MYENV'>some value</initenv>
  <initdir>/my/custom/cwd</initdir>
  <inituser>tester</inituser>
  <initgroup>1000</initgroup>
</os>
```

如果要启用用户命名空间，请设置 idmap 元素。uid 和 gid 元素有三个属性：

- start

  容器中的第一个用户 ID。它必须是 '0'。

- target

  容器中的第一个用户 ID 将映射到主机中的此目标用户 ID。

- count

  容器中有多少用户被允许映射到主机的用户。

```
<idmap>
  <uid start='0' target='1000' count='10'/>
  <gid start='0' target='1000' count='10'/>
</idmap>
```

### 2.5 [通用 元素配置](https://www.libvirt.org/formatdomain.html#id8)

这些选项适用于客户机 OS 的任何形式的引导。

```
...
<os>
  ...
  <acpi>
    <table type='slic'>/path/to/slic.dat</table>
  </acpi>
</os>
...
```

- acpi

  table 元素包含 ACPI 表的完全限定路径，type 属性指示文件中必须存在的数据：raw: 单个 ACPI 表，带有头和数据，ACPI 签名从头部自动检测（自 11.2.0 起，QEMU）。rawset: 多个 ACPI 表的连接，带有头和数据，每个表都有任何 ACPI 签名，从头部自动检测（自 11.2.0 起，Xen）。slic: 单个 ACPI 表，带有头和数据，提供软件许可信息。头部中的 ACPI 表签名将被强制设置为 SLIC（自 1.3.5 起，QEMU），自 5.9.0 起（Xen）被错误解释为 rawset。msdm: 单个 ACPI 表，带有头和数据，提供 Microsoft 数据管理信息。头部中的 ACPI 表签名将被强制设置为 MSDM（自 11.2.0 起，QEMU）。每种类型只能使用一次，除了 raw 可以出现多次。

## 3 [SMBIOS 系统信息](https://www.libvirt.org/formatdomain.html#id9)

一些 hypervisor 允许控制呈现给客户机的系统信息（例如，SMBIOS 字段可以由 hypervisor 填充并通过客户机中的 dmidecode 命令检查）。可选的 sysinfo 元素涵盖所有此类信息类别。自 0.8.7 起

```
...
<os>
  <smbios mode='sysinfo'/>
  ...
</os>
<sysinfo type='smbios'>
  <bios>
    <entry name='vendor'>LENOVO</entry>
  </bios>
  <system>
    <entry name='manufacturer'>Fedora</entry>
    <entry name='product'>Virt-Manager</entry>
    <entry name='version'>0.9.4</entry>
  </system>
  <baseBoard>
    <entry name='manufacturer'>LENOVO</entry>
    <entry name='product'>20BE0061MC</entry>
    <entry name='version'>0B98401 Pro</entry>
    <entry name='serial'>W1KS427111E</entry>
  </baseBoard>
  <chassis>
    <entry name='manufacturer'>Dell Inc.</entry>
    <entry name='version'>2.12</entry>
    <entry name='serial'>65X0XF2</entry>
    <entry name='asset'>40000101</entry>
    <entry name='sku'>Type3Sku1</entry>
  </chassis>
  <oemStrings>
    <entry>myappname:some arbitrary data</entry>
    <entry>otherappname:more arbitrary data</entry>
  </oemStrings>
</sysinfo>
<sysinfo type='fwcfg'>
  <entry name='opt/com.example/name'>example value</entry>
  <entry name='opt/com.coreos/config' file='/tmp/provision.ign'/>
</sysinfo>
...
```

sysinfo 元素具有强制属性 type，确定子元素的布局，支持的值为：

- smbios

  子元素调用特定的 SMBIOS 值，如果与 os 元素的 smbios 子元素（请参阅 [操作系统引导](https://www.libvirt.org/formatdomain.html#operating-system-booting)）结合使用，将影响客户机。sysinfo 的每个子元素都命名一个 SMBIOS 块，在这些元素中可以有描述块中字段的 entry 元素列表。识别以下块和条目：bios 这是 SMBIOS 的块 0，条目名称来自：vendor BIOS 供应商名称 version BIOS 版本 date BIOS 发布日期。如果提供，格式为 mm/dd/yy 或 mm/dd/yyyy。如果字符串的年份部分是两位数字，则年份被假定为 19yy。release 系统 BIOS 主要和次要版本号值连接在一起作为一个用句点分隔的字符串，例如 10.22。 system 这是 SMBIOS 的块 1，条目名称来自：manufacturer BIOS 制造商 product 产品名称 version 产品版本 serial 序列号 uuid 全局唯一 ID 号。如果此条目与顶级 uuid 元素（请参阅 [一般元数据](https://www.libvirt.org/formatdomain.html#general-metadata)）一起提供，则两个值必须匹配。sku 用于识别特定配置的 SKU 编号。family 识别特定计算机所属的系列。 baseBoard 这是 SMBIOS 的块 2。此元素可以重复多次以描述所有主板；但是，并非所有 hypervisor 都必然支持重复。该元素可以有以下子元素：manufacturer BIOS 制造商 product 产品名称 version 产品版本 serial 序列号 asset 资产标签 location 机箱中的位置 注意：为 bios、system 或 baseBoard 块提供的不正确条目将被忽略，不会出错。除了 uuid 验证和日期格式检查外，所有值都作为字符串传递给 hypervisor 驱动程序。chassis 自 4.1.0 起，这是 SMBIOS 的块 3，带有

- fwcfg

  一些 hypervisor 提供统一的方式来调整固件如何配置自己，或者可能包含要为客户机 OS 安装的表，例如引导顺序、ACPI、SMBIOS 等。它甚至允许用户定义自己的配置 blob。在 QEMU 的情况下，这些会出现在域的 sysfs 下（如果客户机内核启用了 FW_CFG_SYSFS 配置选项），在 /sys/firmware/qemu_fw_cfg 下。注意，这些值无论 <os/> 下的 <smbios/> 模式如何都适用。自 6.5.0 起 **请注意，由于数据槽数量有限，强烈建议不要使用 fwcfg，而应使用 <oemStrings/>**。 `<sysinfo type='fwcfg'>  <entry name='opt/com.example/name'>example value</entry>  <entry name='opt/com.example/config' file='/tmp/provision.ign'/> </sysinfo>` sysinfo 元素可以有多个 entry 子元素。每个元素都有强制的 name 属性，定义 blob 的名称，必须以 opt/ 开头，为避免与其他名称冲突，建议采用 opt/$RFQDN/$name 的形式，其中 $RFQDN 是您控制的反向完全限定域名。然后，该元素可以包含值（直接设置 blob 值），或 file 属性（从文件设置 blob 值）。

## 4 [CPU 分配](https://www.libvirt.org/formatdomain.html#id10)

```
<domain>
  ...
  <vcpu placement='static' cpuset="1-4,^3,6" current="1">2</vcpu>
  <vcpus>
    <vcpu id='0' enabled='yes' hotpluggable='no' order='1'/>
    <vcpu id='1' enabled='no' hotpluggable='yes'/>
  </vcpus>
  ...
</domain>
```

- vcpu

  此元素的内容定义为客户机 OS 分配的最大虚拟 CPU 数量，必须在 1 和 hypervisor 支持的最大值之间。cpuset 可选属性 cpuset 是物理 CPU 编号的逗号分隔列表，默认情况下域进程和虚拟 CPU 可以固定到这些编号。（注意：域进程和虚拟 CPU 的固定策略可以通过 cputune 单独指定。如果指定了 cputune 的 emulatorpin 属性，则此处由 vcpu 指定的 cpuset 将被忽略。同样，对于指定了 vcpupin 的虚拟 CPU，此处由 cpuset 指定的 cpuset 将被忽略。对于未指定 vcpupin 的虚拟 CPU，每个都将固定到此处由 cpuset 指定的物理 CPU。）该列表中的每个元素要么是单个 CPU 编号，要么是 CPU 编号范围，要么是插入号后跟要从先前范围中排除的 CPU 编号。自 0.4.4 起 current 可选属性 current 可用于指定是否应启用少于最大数量的虚拟 CPU。自 0.8.5 起 placement 可选属性 placement 可用于指示域进程的 CPU 放置模式。值可以是 "static" 或 "auto"，但默认为 numatune 的放置或如果指定了 cpuset 则为 "static"。使用 "auto" 表示域进程将固定到查询 numad 的建议节点集，如果指定了 cpuset 属性，则将被忽略。如果既未指定 cpuset 和 placement，或者 placement 为 "static" 但未指定 cpuset，则域进程将固定到所有可用的物理 CPU。自 0.9.11 起（仅 QEMU 和 KVM）

- vcpus

  vcpus 元素允许控制各个 vCPU 的状态。id 属性指定 libvirt 在其他地方（如 vCPU 固定、调度程序信息和 NUMA 分配）使用的 vCPU id。请注意，在客户机中看到的 vCPU ID 在某些情况下可能与 libvirt ID 不同。有效 ID 从 0 到由 vcpu 元素设置的最大 vCPU 计数减 1。enabled 属性允许控制 vCPU 的状态。有效值为 yes 和 no。hotpluggable 控制给定 vCPU 是否可以在 CPU 在引导时启用的情况下进行热插拔和热卸载。请注意，所有禁用的 vCPU 必须是可热插拔的。有效值为 yes 和 no。order 允许指定添加在线 vCPU 的顺序。对于需要一次插入多个 vCPU 的 hypervisor/平台，顺序可以在需要同时启用的所有 vCPU 上重复。指定顺序不是必需的，vCPU 然后以任意顺序添加。如果使用顺序信息，则必须对所有在线 vCPU 使用。Hypervisor 可能会在某些操作期间清除或更新排序信息以确保有效的配置。请注意，hypervisor 可能以与引导 vCPU 不同的方式创建可热插拔 vCPU，因此可能需要特殊初始化。Hypervisor 可能要求在引导时启用的不可热插拔 vCPU 聚集在开头，从 ID 0 开始。还可能要求 vCPU 0 始终存在且不可热插拔。请注意，提供各个 CPU 的状态可能是启用可寻址 vCPU 热插拔支持所必需的，并且此功能可能不被所有 hypervisor 支持。对于 QEMU，需要以下条件。vCPU 0 需要启用且不可热插拔。在 PPC64 上，与其在同一核心中的 vCPU 也需要启用。启动时存在的所有不可热插拔 CPU 需要在 vCPU 0 之后分组。自 2.2.0 起（仅 QEMU）

## 5 [IOThreads 分配](https://www.libvirt.org/formatdomain.html#id11)

IOThreads 是用于支持的磁盘设备的专用事件循环线程，用于执行块 I/O 请求，以提高可扩展性，尤其是在具有许多 LUN 的 SMP 主机/客户机上。自 1.2.8 起（仅 QEMU）

```
<domain>
  ...
  <iothreads>4</iothreads>
  ...
</domain>
<domain>
  ...
  <iothreadids>
    <iothread id="2"/>
    <iothread id="4"/>
    <iothread id="6"/>
    <iothread id="8" thread_pool_min="2" thread_pool_max="32">
      <poll max='123' grow='456' shrink='789'/>
    </iothread>
  </iothreadids>
  <defaultiothread thread_pool_min="8" thread_pool_max="16"/>
  ...
</domain>
```

- iothreads

  此可选元素的内容定义要分配给域的 IOThreads 数量，供支持的目标存储设备使用。每个主机 CPU 应该只有 1 或 2 个 IOThreads。每个 IOThread 可以分配多个支持的设备。自 1.2.8 起

- iothreadids

  可选的 iothreadids 元素提供了专门定义域的 IOThread ID 的能力。默认情况下，IOThread ID 从 1 开始顺序编号，直到为域定义的 iothreads 数量。id 属性用于定义 IOThread ID。id 属性必须是大于 0 的正整数。如果定义的 iothreadids 少于为域定义的 iothreads，则 libvirt 将从 1 开始顺序填充 iothreadids，避免任何预定义的 id。如果定义的 iothreadids 多于为域定义的 iothreads，则 iothreads 值将相应调整。自 1.2.15 起 该元素有两个可选属性 thread_pool_min 和 thread_pool_max，允许为给定 IOThread 设置工作线程数量的下限和上限。前者可以为零，后者不能。自 8.5.0 起 自 9.4.0 起，可选的子元素 poll 可用于覆盖 hypervisor 默认的 iothread 在切换回事件之前的轮询间隔。可选属性 max 设置轮询应使用的最大时间（以纳秒为单位）。将 max 设置为 0 禁用轮询。属性 grow 和 shrink 覆盖（或在设置为 0 时禁用）如果设置的间隔被认为不足或过度，则增加/减少轮询间隔的默认步骤。

- defaultiothread

  此元素表示 hypervisor 内的默认事件循环，处理未分配给特定 IOThread 的设备的 I/O 请求。该元素可以具有 thread_pool_min 和/或 thread_pool_max 属性，控制默认事件循环的工作线程数量的下限和上限。模拟器可能是多线程的，并根据需要生成所谓的工作线程。一般来说，这些属性都不应设置（让模拟器使用其自己的默认值），除非模拟器在实时工作负载中运行，因此无法承受生成新工作线程所需时间的不可预测性。自 8.5.0 起

## 6 [CPU 调优](https://www.libvirt.org/formatdomain.html#id12)

```
<domain>
  ...
  <cputune>
    <vcpupin vcpu="0" cpuset="1-4,^2"/>
    <vcpupin vcpu="1" cpuset="0,1"/>
    <vcpupin vcpu="2" cpuset="2,3"/>
    <vcpupin vcpu="3" cpuset="0,4"/>
    <emulatorpin cpuset="1-3"/>
    <iothreadpin iothread="1" cpuset="5,6"/>
    <iothreadpin iothread="2" cpuset="7,8"/>
    <shares>2048</shares>
    <period>1000000</period>
    <quota>-1</quota>
    <global_period>1000000</global_period>
    <global_quota>-1</global_quota>
    <emulator_period>1000000</emulator_period>
    <emulator_quota>-1</emulator_quota>
    <iothread_period>1000000</iothread_period>
    <iothread_quota>-1</iothread_quota>
    <vcpusched vcpus='0-4,^3' scheduler='fifo' priority='1'/>
    <iothreadsched iothreads='2' scheduler='batch'/>
    <cachetune vcpus='0-3'>
      <cache id='0' level='3' type='both' size='3' unit='MiB'/>
      <cache id='1' level='3' type='both' size='3' unit='MiB'/>
      <monitor level='3' vcpus='1'/>
      <monitor level='3' vcpus='0-3'/>
    </cachetune>
    <cachetune vcpus='4-5'>
      <monitor level='3' vcpus='4'/>
      <monitor level='3' vcpus='5'/>
    </cachetune>
    <memorytune vcpus='0-3'>
      <node id='0' bandwidth='60'/>
    </memorytune>

  </cputune>
  ...
</domain>
```

- cputune

  可选的 cputune 元素提供有关域的 CPU 可调参数的详细信息。注意：对于 qemu 驱动程序，可选的 vcpupin 和 emulatorpin 固定设置在模拟器启动和考虑 NUMA 约束后生效。这意味着在此期间，域预计会使用主机的其他物理 CPU，这将通过 virsh cpu-stats 的输出来反映。自 0.9.0 起

- vcpupin

  可选的 vcpupin 元素指定域 vCPU 将固定到主机的哪些物理 CPU。如果省略，并且未指定元素 vcpu 的属性 cpuset，则 vCPU 默认固定到所有物理 CPU。它包含两个必需属性，属性 vcpu 指定 vCPU id，属性 cpuset 与元素 vcpu 的属性 cpuset 相同。QEMU 驱动程序支持自 0.9.0 起，Xen 驱动程序支持自 0.9.1 起

- emulatorpin

  可选的 emulatorpin 元素指定域的"模拟器"（不包括 vCPU 或 iothreads 的域子集）将固定到主机的哪些物理 CPU。如果省略，并且未指定元素 vcpu 的属性 cpuset，则"模拟器"默认固定到所有物理 CPU。它包含一个必需属性 cpuset，指定要固定到的物理 CPU。

- iothreadpin

  可选的 iothreadpin 元素指定 IOThreads 将固定到主机的哪些物理 CPU。如果省略，并且未指定元素 vcpu 的属性 cpuset，则 IOThreads 默认固定到所有物理 CPU。有两个必需属性，属性 iothread 指定 IOThread ID，属性 cpuset 指定要固定到的物理 CPU。请参阅 [IOThreads 分配](https://www.libvirt.org/formatdomain.html#iothreads-allocation) 部分，记录 iothread 的有效值。自 1.2.9 起

- shares

  可选的 shares 元素指定域的比例加权份额。如果省略，默认为 OS 提供的默认值。注意，该值没有单位，它是基于其他 VM 设置的相对度量，例如，配置为值 2048 的 VM 将获得配置为值 1024 的 VM 的两倍 CPU 时间。使用 cgroups v1 时，值应在 [2, 262144] 范围内，使用 cgroups v2 时，值应在 [1, 10000] 范围内。自 0.9.0 起

- period

  可选的 period 元素指定执行间隔（单位：微秒）。在 period 内，域的每个 vCPU 不允许消耗超过 quota 的运行时间。值应在 [1000, 1000000] 范围内。值为 0 的 period 表示无值。仅 QEMU 驱动程序支持自 0.9.4 起，LXC 自 0.9.10 起

- quota

  可选的 quota 元素指定最大允许带宽（单位：微秒）。quota 为任何负值的域表示该域对 vCPU 线程具有无限带宽，这意味着它不受带宽控制。值应在 [1000, 17592186044415] 范围内或小于 0。值为 0 的 quota 表示无值。您可以使用此功能确保所有 vCPU 以相同的速度运行。仅 QEMU 驱动程序支持自 0.9.4 起，LXC 自 0.9.10 起

- global_period

  可选的 global_period 元素指定整个域的执行 CFS 调度程序间隔（单位：微秒），与 period 相比，后者按 vCPU 执行间隔。值应在 1000, 1000000] 范围内。值为 0 的 global_period 表示无值。仅 QEMU 驱动程序支持自 1.3.3 起

- global_quota

  可选的 global_quota 元素指定在一个周期内整个域的最大允许带宽（单位：微秒）。global_quota 为任何负值的域表示该域具有无限带宽，这意味着它不受带宽控制。值应在 [1000, 17592186044415] 范围内或小于 0。值为 0 的 global_quota 表示无值。仅 QEMU 驱动程序支持自 1.3.3 起

- emulator_period

  可选的 emulator_period 元素指定执行间隔（单位：微秒）。在 emulator_period 内，域的模拟器线程（不包括 vCPU）不允许消耗超过 emulator_quota 的运行时间。值应在 [1000, 1000000] 范围内。值为 0 的 period 表示无值。仅 QEMU 驱动程序支持自 0.10.0 起

- emulator_quota

  可选的 emulator_quota 元素指定域的模拟器线程（不包括 vCPU）的最大允许带宽（单位：微秒）。emulator_quota 为任何负值的域表示该域对模拟器线程（不包括 vCPU）具有无限带宽，这意味着它不受带宽控制。值应在 [1000, 17592186044415] 范围内或小于 0。值为 0 的 quota 表示无值。仅 QEMU 驱动程序支持自 0.10.0 起

- iothread_period

  可选的 iothread_period 元素指定 IOThreads 的执行间隔（单位：微秒）。在 iothread_period 内，域的每个 IOThread 不允许消耗超过 iothread_quota 的运行时间。值应在 [1000, 1000000] 范围内。值为 0 的 iothread_period 表示无值。仅 QEMU 驱动程序支持自 2.1.0 起

- iothread_quota

  可选的 iothread_quota 元素指定 IOThreads 的最大允许带宽（单位：微秒）。iothread_quota 为任何负值的域表示该域的 IOThreads 具有无限带宽，这意味着它不受带宽控制。值应在 [1000, 17592186044415] 范围内或小于 0。值为 0 的 iothread_quota 表示无值。您可以使用此功能确保所有 IOThreads 以相同的速度运行。仅 QEMU 驱动程序支持自 2.1.0 起

- vcpusched、iothreadsched 和 emulatorsched

  可选的 vcpusched、iothreadsched 和 emulatorsched 元素分别指定特定 vCPU、IOThread 和模拟器线程的调度程序类型（值 batch、idle、fifo、rr）。对于 vcpusched 和 iothreadsched，属性 vcpus 和 iothreads 选择此设置适用的 vCPU/IOThreads，省略它们设置默认值。元素 emulatorsched 没有该属性。有效的 vcpus 值从 0 开始，到为域定义的 vCPU 数量减 1。有效的 iothreads 值在 [IOThreads 分配](https://www.libvirt.org/formatdomain.html#iothreads-allocation) 部分中描述。如果未定义 iothreadids，则 libvirt 从 1 到域可用的 iothreads 数量对 IOThreads 进行编号。对于实时调度程序（fifo、rr），还必须指定优先级（对于非实时调度程序，优先级被忽略）。优先级的取值范围取决于主机内核（通常为 1-99）。自 1.2.13 起 emulatorsched 自 5.3.0 起

- cachetune 自 4.1.0 起

  可选的 cachetune 元素可以使用主机上的 resctrl 控制 CPU 缓存分配。是否支持这一点可以从功能中获取，其中还报告了一些限制，如最小大小和所需的粒度。必需属性 vcpus 指定此分配适用的 vCPU。一个 vCPU 只能是一个 cachetune 元素分配的成员。cachetune 指定的 vCPU 可以与 memorytune 中的 vCPU 相同，但它们不允许重叠。可选的、仅输出的 id 属性唯一标识缓存。支持的子元素有：cache 此可选元素控制 CPU 缓存的分配，具有以下属性：level 要从中分配的主机缓存级别。id 要从中分配的主机缓存 id。type 分配类型。可以是 code 用于代码（指令），data 用于数据，或 both 用于代码和数据（统一）。目前，分配只能使用与主机支持相同的类型，这意味着对于启用了 CDP（代码/数据优先级）的主机，您不能请求两者。size 要分配的区域大小。默认值以字节为单位，但可以使用 unit 属性来缩放值。unit（可选）如果指定，它是 size 指定的单位，如 KiB、MiB、GiB 或 TiB（在 [内存分配](https://www.libvirt.org/formatdomain.html#memory-allocation) 的 memory 元素中描述），默认为字节。 monitor 自 4.10.0 起 可选元素 monitor 为当前缓存分配创建缓存监视器，并具有以下必需属性：level 监视器所属的主机缓存级别。vcpus 监视器适用的 vCPU 列表。监视器的 vCPU 列表只能是关联分配的 vCPU 列表的成员。默认监视器具有与关联分配相同的 vCPU 列表。对于非默认监视器，不允许重叠的 vCPU。

- memorytune 自 4.7.0 起

  可选的 memorytune 元素可以使用主机上的 resctrl 控制内存带宽分配。是否支持这一点可以从功能中获取，其中还报告了一些限制，如最小带宽和所需的粒度。必需属性 vcpus 指定此分配适用的 vCPU。一个 vCPU 只能是一个 memorytune 元素分配的成员。memorytune 指定的 vcpus 可以与 cachetune 指定的 vcpus 相同。但是它们不允许相互重叠。支持的子元素有：node 此元素控制 CPU 内存带宽的分配，具有以下属性：id 要从中分配内存带宽的主机节点 id。bandwidth 要从该节点分配的内存带宽。该值通常以百分比表示（Intel），但也可以以 MB/s 表示（如果 resctrl 以 mba_MBps 选项挂载）或以 1/8 GB/s 增量表示（AMD）。 用户负责确保该值在其系统和配置上有意义。

## 7 [内存分配](https://www.libvirt.org/formatdomain.html#id13)

```
<domain>
  ...
  <maxMemory slots='16' unit='KiB'>1524288</maxMemory>
  <memory unit='KiB'>524288</memory>
  <currentMemory unit='KiB'>524288</currentMemory>
  ...
</domain>
```

- memory

  客户机在引导时的最大内存分配。内存分配包括启动时指定或稍后热插拔的可能的额外内存设备。此值的单位由可选属性 unit 确定，默认为 "KiB"（ kibibytes，2^10 或 1024 字节块）。有效的单位是 "b" 或 "bytes" 表示字节，"KB" 表示千字节（10^3 或 1,000 字节），"k" 或 "KiB" 表示 kibibytes（1024 字节），"MB" 表示兆字节（10^6 或 1,000,000 字节），"M" 或 "MiB" 表示 mebibytes（2^20 或 1,048,576 字节），"GB" 表示吉字节（10^9 或 1,000,000,000 字节），"G" 或 "GiB" 表示 gibibytes（2^30 或 1,073,741,824 字节），"TB" 表示太字节（10^12 或 1,000,000,000,000 字节），或 "T" 或 "TiB" 表示 tebibytes（2^40 或 1,099,511,627,776 字节）。然而，libvirt 会将值向上舍入到最接近的 kibibyte，并且可能会进一步舍入到 hypervisor 支持的粒度。一些 hypervisor 还强制执行最小值，例如 4000KiB。如果为客户机配置了 NUMA（请参阅 [CPU 模型和拓扑](https://www.libvirt.org/formatdomain.html#cpu-model-and-topology)），则可以省略 memory 元素。在崩溃的情况下，可选属性 dumpCore 可用于控制是否应在生成的核心转储中包含客户机内存（值 "on"、"off"）。unit 自 0.9.11 起，dumpCore 自 0.10.2 起（仅 QEMU）

- maxMemory

  客户机的运行时最大内存分配。由 <memory> 元素或 NUMA 单元大小配置指定的初始内存可以通过热插拔内存增加到该元素指定的限制。unit 属性的行为与 <memory> 相同。slots 属性指定可用于向客户机添加内存的插槽数。边界是特定于 hypervisor 的。请注意，由于通过内存热插拔添加的内存块的对齐，可能无法实现此元素指定的完整大小分配。自 1.2.14 起由 QEMU 驱动程序支持。

- currentMemory

  客户机的实际内存分配。此值可以小于最大分配，以允许动态增加客户机内存。如果省略，默认为与 memory 元素相同的值。unit 属性的行为与 memory 相同。

## 8 [内存后备](https://www.libvirt.org/formatdomain.html#id14)

```
<domain>
  ...
  <memoryBacking>
    <hugepages>
      <page size="1" unit="G" nodeset="0-3,5"/>
      <page size="2" unit="M" nodeset="4"/>
    </hugepages>
    <nosharepages/>
    <locked/>
    <source type="file|anonymous|memfd"/>
    <access mode="shared|private"/>
    <allocation mode="immediate|ondemand" threads='8'/>
    <discard/>
  </memoryBacking>
  ...
</domain>
```

可选的 memoryBacking 元素可能包含几个影响虚拟内存页如何由主机页支持的元素。

- hugepages

  这告诉 hypervisor 客户机的内存应该使用大页而不是正常的本机页大小来分配。自 1.2.5 起，可以更具体地为每个 numa 节点设置大页。引入了 page 元素。它有一个强制属性 size，指定应该使用哪些大页（在支持不同大小大页的系统上特别有用）。size 属性的默认单位是 kiB（1024 的倍数）。如果要使用不同的单位，请使用可选的 unit 属性。对于具有 NUMA 的系统，可选的 nodeset 属性可能很有用，因为它将给定客户机的 NUMA 节点与特定的大页大小相关联。从示例代码片段中，除了节点 4 之外，每个 NUMA 节点都使用 1GB 的大页。有关正确的语法，请参阅 [NUMA 节点调优](https://www.libvirt.org/formatdomain.html#numa-node-tuning)。

- nosharepages

  指示 hypervisor 为此域禁用共享页（内存合并，KSM）。自 1.0.6 起

- locked

  当设置并由 hypervisor 支持时，属于域的内存页将被锁定在主机内存中，主机将不允许将它们换出，这对于某些工作负载（如实时）可能是必需的。对于 QEMU/KVM 客户机，QEMU 进程本身使用的内存也会被锁定：与客户机内存不同，这是 libvirt 无法提前计算的数量，因此它必须完全删除锁定内存的限制。因此，启用此选项会带来潜在的安全风险：当主机内存不足时，主机将无法从客户机收回锁定的内存，这意味着分配大量锁定内存的恶意客户机可能会对主机造成拒绝服务攻击。因此，除非工作负载需要，否则不建议使用此选项；即使如此，也强烈建议同时设置适合特定环境的内存分配硬限制（请参阅 [内存调优](https://www.libvirt.org/formatdomain.html#memory-tuning)）以减轻上述风险。自 1.0.6 起

- source

  使用 type 属性，可以提供 "file" 来利用文件内存后备，或保持默认的 "anonymous"。自 4.10.0 起，您可以选择 "memfd" 后备。（仅 QEMU/KVM）

- access

  使用 mode 属性，指定内存是 "shared" 还是 "private"。这可以通过 memAccess 按 numa 节点覆盖。

- allocation

  使用可选的 mode 属性，通过提供 "immediate" 或 "ondemand" 来指定何时分配内存。自 8.2.0 起，可以通过 threads 属性设置 hypervisor 用于分配内存的线程数。为了加快分配过程，当固定模拟器线程时，建议包括来自所需 NUMA 节点的 CPU，以便分配线程可以设置其亲和性。

- discard

  当设置并由 hypervisor 支持时，内存内容会在客户机关闭前（或 DIMM 模块拔出时）被丢弃。请注意，这只是一种优化，并不保证在所有情况下都能工作（例如，当 hypervisor 崩溃时）。自 4.4.0 起（仅 QEMU/KVM）

## 9 [内存调优](https://www.libvirt.org/formatdomain.html#id15)

```
<domain>
  ...
  <memtune>
    <hard_limit unit='G'>1</hard_limit>
    <soft_limit unit='M'>128</soft_limit>
    <swap_hard_limit unit='G'>2</swap_hard_limit>
    <min_guarantee unit='bytes'>67108864</min_guarantee>
  </memtune>
  ...
</domain>
```

- memtune

  可选的 memtune 元素提供有关域的内存可调参数的详细信息。如果省略，默认为 OS 提供的默认值。对于 QEMU/KVM，参数应用于整个 QEMU 进程。因此，在计算它们时，需要将客户机 RAM、客户机视频 RAM 和 QEMU 本身的一些内存开销相加。最后一部分很难确定，所以需要猜测和尝试。对于每个可调参数，可以使用与 <memory> 相同的值指定输入中数字的单位。为了向后兼容，输出始终以 KiB 为单位。unit 自 0.9.11 起 所有 limit 参数的可能值范围从 0 到 VIR_DOMAIN_MEMORY_PARAM_UNLIMITED。

- hard_limit

  可选的 hard_limit 元素是客户机可以使用的最大内存。此值的单位是 kibibytes（即 1024 字节的块）。强烈建议 QEMU 和 KVM 的用户不要设置此限制，因为如果猜测过低，域可能会被内核杀死，并且确定进程运行所需的内存是一个 [不可判定的问题](https://en.wikipedia.org/wiki/Undecidable_problem)；也就是说，如果您已经在 [内存后备](https://www.libvirt.org/formatdomain.html#memory-backing) 中设置了 locked，因为您的工作负载需要它，您将不得不考虑部署的具体情况，并找出一个足够大的 hard_limit 值来支持客户机的内存需求，但又足够小以保护主机免受恶意客户机锁定所有内存的影响。

- soft_limit

  可选的 soft_limit 元素是内存争用时强制执行的内存限制。此值的单位是 kibibytes（即 1024 字节的块）

- swap_hard_limit

  可选的 swap_hard_limit 元素是客户机可以使用的最大内存加交换空间。此值的单位是 kibibytes（即 1024 字节的块）。这必须大于提供的 hard_limit 值

- min_guarantee

  可选的 min_guarantee 元素是客户机的保证最小内存分配。此值的单位是 kibibytes（即 1024 字节的块）。此元素仅由 VMware ESX 和 OpenVZ 驱动程序支持。

## 10 [NUMA 节点调优](https://www.libvirt.org/formatdomain.html#id16)

```
<domain>
  ...
  <numatune>
    <memory mode="strict" nodeset="1-4,^3"/>
    <memnode cellid="0" mode="strict" nodeset="1"/>
    <memnode cellid="2" mode="preferred" nodeset="2"/>
  </numatune>
  ...
</domain>
```

- numatune

  可选的 numatune 元素提供了如何通过控制域进程的 NUMA 策略来调优 NUMA 主机性能的详细信息。注意，仅由 QEMU 驱动程序支持。自 0.9.3 起

- memory

  可选的 memory 元素指定如何在 NUMA 主机上为域进程分配内存。它包含几个可选属性。属性 mode 可以是 'interleave'、'strict'、'preferred' 或 'restrictive'，默认为 'strict'。值 'restrictive' 指定使用系统默认策略，仅使用 cgroups 来限制内存节点，并且需要在 memnode 元素中设置 mode 为 'restrictive'（见下面的怪癖）。这仅用于能够使用 virsh numatune 或 virDomainSetNumaParameters 请求移动运行中域的此类内存，并且不保证会发生。属性 nodeset 指定 NUMA 节点，使用与元素 vcpu 的属性 cpuset 相同的语法。属性 placement（自 0.9.12 起）可用于指示域进程的内存放置模式，其值可以是 "static" 或 "auto"，默认为 vcpu 的放置，或者如果指定了 nodeset 则为 "static"。"auto" 表示域进程将仅从查询 numad 返回的建议节点集分配内存，如果指定了属性 nodeset，则将忽略其值。如果 vcpu 的放置是 'auto'，并且未指定 numatune，则会隐式添加一个默认的 numatune，其中放置为 'auto' 且 mode 为 'strict'。自 0.9.3 起 有关此元素更新的更多信息，请参阅 [virDomainSetNumaParameters](https://www.libvirt.org/html/libvirt-libvirt-domain.html#virDomainSetNumaParameters)。

- memnode

  可选的 memnode 元素可以为每个客户机 NUMA 节点指定内存分配策略。对于没有对应 memnode 元素的节点，将使用元素 memory 中的默认值。属性 cellid 寻址应用设置的客户机 NUMA 节点。属性 mode 和 nodeset 与 memory 元素中的含义和语法相同。此设置与自动放置不兼容。请注意，对于 memnode，这只会指导 vCPU 线程的内存访问或类似机制，并且是非常特定于 hypervisor 的。这不能保证节点内存分配的放置。对于正确的限制，应使用其他方法（例如，不同的模式，预分配的大页）。QEMU 自 1.2.7 起

## 11 [块 I/O 调优](https://www.libvirt.org/formatdomain.html#id17)

```
<domain>
  ...
  <blkiotune>
    <weight>800</weight>
    <device>
      <path>/dev/sda</path>
      <weight>1000</weight>
    </device>
    <device>
      <path>/dev/sdb</path>
      <weight>500</weight>
      <read_bytes_sec>10000</read_bytes_sec>
      <write_bytes_sec>10000</write_bytes_sec>
    </device>
  </blkiotune>
  ...
</domain>
```

- blkiotune

  可选的 blkiotune 元素提供有关域的块 I/O 可调参数的详细信息。如果省略，默认为 OS 提供的默认值。

- weight

  可选的 weight 元素指定域的相对权重。当多个域竞争相同的磁盘 I/O 时，这个值决定了域将获得的 I/O 时间的比例。有效值范围从 100 到 1000。自 0.10.2 起

- device

  可选的 device 元素指定特定设备的块 I/O 可调参数。

- path

  必需的 path 元素指定设备的路径。

- weight

  可选的 weight 元素指定设备的相对权重。当多个域竞争相同的磁盘 I/O 时，这个值决定了域将获得的 I/O 时间的比例。有效值范围从 100 到 1000。

- read_bytes_sec

  可选的 read_bytes_sec 元素指定设备的最大读取速率（以字节/秒为单位）。

- write_bytes_sec

  可选的 write_bytes_sec 元素指定设备的最大写入速率（以字节/秒为单位）。

- read_iops_sec

  可选的 read_iops_sec 元素指定设备的最大读取 I/O 操作数/秒。

- write_iops_sec

  可选的 write_iops_sec 元素指定设备的最大写入 I/O 操作数/秒。

- read_bytes_sec_max

  可选的 read_bytes_sec_max 元素指定设备的突发最大读取速率（以字节/秒为单位）。

- write_bytes_sec_max

  可选的 write_bytes_sec_max 元素指定设备的突发最大写入速率（以字节/秒为单位）。

- read_iops_sec_max

  可选的 read_iops_sec_max 元素指定设备的突发最大读取 I/O 操作数/秒。

- write_iops_sec_max

  可选的 write_iops_sec_max 元素指定设备的突发最大写入 I/O 操作数/秒。

- read_bytes_sec_cds

  可选的 read_bytes_sec_cds 元素指定设备的突发读取持续时间（以秒为单位）。

- write_bytes_sec_cds

  可选的 write_bytes_sec_cds 元素指定设备的突发写入持续时间（以秒为单位）。

- read_iops_sec_cds

  可选的 read_iops_sec_cds 元素指定设备的突发读取 I/O 操作持续时间（以秒为单位）。

- write_iops_sec_cds

  可选的 write_iops_sec_cds 元素指定设备的突发写入 I/O 操作持续时间（以秒为单位）。

## 12 [资源分区](https://www.libvirt.org/formatdomain.html#id18)

Hypervisor 可能允许将虚拟机放置到资源分区中，可能会嵌套这些分区。resource 元素将与资源分区相关的配置分组在一起。它目前支持一个子元素 partition，其内容定义了放置域的资源分区的绝对路径。如果没有列出分区，则域将被放置在默认分区中。应用程序/管理员有责任确保在启动客户机之前分区存在。只有（特定于 hypervisor 的）默认分区可以假定默认存在。

```
...
<resource>
  <partition>/virtualmachines/production</partition>
</resource>
...
```

资源分区目前由 QEMU 和 LXC 驱动程序支持，它们将分区路径映射到所有已挂载控制器中的 cgroups 目录。自 1.0.5 起

## 13 [Fibre Channel VMID](https://www.libvirt.org/formatdomain.html#id19)

FC SAN 可以根据 VMID 提供各种 QoS 级别和访问控制。它还可以在每个 VM 级别收集遥测数据，这些数据可用于增强 VM 的 IO 性能。这可以通过使用 fibrechannel 元素的 appid 属性来配置。该属性包含单个字符串（最大 128 字节），内核使用它来创建 VMID。

```
...
<resource>
  <fibrechannel appid='userProvidedID'/>
</resource>
...
```

使用此功能需要支持 Fibre Channel 的硬件、编译时启用了 CONFIG_BLK_CGROUP_FC_APPID 选项的内核以及加载的 nvme_fc 内核模块。自 7.7.0 起

## 14 [CPU 模型和拓扑](https://www.libvirt.org/formatdomain.html#id20)

可以使用以下元素集合指定 CPU 模型、其功能和拓扑的要求。自 0.7.5 起

```
...
<cpu match='exact'>
  <model fallback='allow'>core2duo</model>
  <vendor>Intel</vendor>
  <topology sockets='1' dies='1' clusters='1' cores='2' threads='1'/>
  <cache level='3' mode='emulate'/>
  <maxphysaddr mode='emulate' bits='42'/>
  <feature policy='disable' name='lahf_lm'/>
</cpu>
...
<cpu mode='host-model'>
  <model fallback='forbid'/>
  <topology sockets='1' dies='1' clusters='1' cores='2' threads='1'/>
</cpu>
...
<cpu mode='host-passthrough' migratable='off'>
  <cache mode='passthrough'/>
  <maxphysaddr mode='passthrough' limit='39'/>
  <feature policy='disable' name='lahf_lm'/>
...
<cpu mode='maximum' migratable='off'>
  <cache mode='passthrough'/>
  <feature policy='disable' name='lahf_lm'/>
...
```

如果不需要对 CPU 模型及其功能施加限制，可以使用更简单的 cpu 元素。自 0.7.6 起

```
...
<cpu>
  <topology sockets='1' dies='1' clusters='1' cores='2' threads='1'/>
</cpu>
...
```

- cpu

  cpu 元素是描述客户机 CPU 要求的主要容器。其 match 属性指定提供给客户机的虚拟 CPU 与这些要求的匹配程度。自 0.7.6 起，如果 topology 是 cpu 中的唯一元素，则可以省略 match 属性。match 属性的可能值为：minimum 指定的 CPU 模型和功能描述了请求的最小 CPU。如果当前主机上的请求 hypervisor 可能，将为客户机提供更好的 CPU。这是一种受约束的 host-model 模式；如果提供的虚拟 CPU 不满足要求，将不会创建域。exact 提供给客户机的虚拟 CPU 应与规范完全匹配。如果不支持此类 CPU，libvirt 将拒绝启动域。strict 除非主机 CPU 与规范完全匹配，否则不会创建域。这在实践中不是很有用，只有在有真正原因时才应使用。自 0.8.5 起，match 属性可以省略，默认为 exact。有时 hypervisor 无法创建与 libvirt 传递的规范完全匹配的虚拟 CPU。自 3.2.0 起，可以使用可选的 check 属性来请求特定的方式检查虚拟 CPU 是否与规范匹配。启动域时通常可以安全地省略此属性并使用默认值。域启动后，libvirt 将自动将 check 属性更改为最佳支持值，以确保在域迁移到另一台主机时虚拟 CPU 不会改变。可以使用以下值：none Libvirt 不进行任何检查，由 hypervisor 决定如果无法提供请求的 CPU 是否拒绝启动域。对于 QEMU，这意味着完全不进行检查，因为 QEMU 的默认行为是发出警告，但仍然启动域。partial Libvirt 将在启动域之前检查客户机 CPU 规范，但其余部分由 hypervisor 决定。full Libvirt 将在启动域之前完全检查客户机 CPU 规范，确保虚拟 CPU 与规范完全匹配。

- model

  model 元素的内容指定客户机请求的 CPU 模型。可用 CPU 模型及其定义的列表可以在 libvirt 数据目录中安装的 cpu_map 目录中找到。如果 hypervisor 无法使用确切的 CPU 模型，libvirt 会自动回退到 hypervisor 支持的最接近的模型，同时保持 CPU 功能列表。自 0.9.10 起，可以使用可选的 fallback 属性来禁止此行为，在这种情况下，尝试启动请求不支持的 CPU 模型的域将失败。fallback 属性支持的值为：allow（默认值）和 forbid。可选的 vendor_id 属性（自 0.10.0 起）可用于设置客户机看到的供应商 ID。它必须正好 12 个字符长。如果未设置，则使用主机的供应商 ID。典型的可能值是 "AuthenticAMD" 和 "GenuineIntel"。

- vendor

  自 0.8.3 起，vendor 元素的内容指定客户机请求的 CPU 供应商。如果缺少此元素，客户机可以在任何匹配给定功能的 CPU 上运行，无论其供应商如何。支持的供应商列表可以在 cpu_map/\*\_vendors.xml 中找到。

- topology

  topology 元素指定提供给客户机的虚拟 CPU 的请求拓扑。其属性 sockets、dies（自 6.1.0 起）、clusters（自 10.1.0 起）、cores 和 threads 接受非零正整数值。它们分别指 CPU 插槽总数、每个插槽的 die 数、每个 die 的集群数、每个集群的核心数以及每个核心的线程数。dies 和 clusters 属性是可选的，如果省略，默认为 1，而其他属性都是必需的。Hypervisor 可能要求 cpus 元素指定的最大 vCPU 数等于拓扑产生的 vCPU 数。此外，并非所有架构和机器类型都支持为所有属性指定非 1 的值。

- feature

  cpu 元素可以包含零个或多个 feature 元素，用于微调所选 CPU 模型提供的功能。已知功能名称的列表可以在与 CPU 模型相同的文件中找到。每个 feature 元素的含义取决于其 policy 属性，该属性必须设置为以下值之一：force 虚拟 CPU 将声称支持该功能，无论主机 CPU 是否支持。require 除非主机 CPU 支持该功能或 hypervisor 能够模拟它，否则客户机创建将失败。optional 虚拟 CPU 将仅在主机 CPU 支持该功能时才支持该功能。disable 虚拟 CPU 将不支持该功能。forbid 如果主机 CPU 支持该功能，客户机创建将失败。自 0.8.5 起，policy 属性可以省略，默认为 require。各个 CPU 功能名称在 name 属性中指定。例如，要使用 Intel IvyBridge CPU 模型明确指定 'pcid' 功能：`... <cpu match='exact'>  <model fallback='forbid'>IvyBridge</model>  <vendor>Intel</vendor>  <feature policy='require' name='pcid'/> </cpu> ...`

- deprecated_features

  自 11.0.0 起，S390 客户机可以使用 deprecated_features 属性来指定切换被 hypervisor 标记为已弃用的 CPU 模型功能。当此属性设置为 off 时，活动客户机 XML 将反映具有 disable 策略的相应功能。当此属性设置为 on 时，相应功能将被启用。

- cache

  自 3.3.0 起，cache 元素描述虚拟 CPU 缓存。如果缺少该元素，hypervisor 将使用合理的默认值。level 此可选属性指定元素描述的缓存级别。缺少属性意味着该元素同时描述所有 CPU 缓存级别。禁止混合使用设置了 level 属性的 cache 元素和没有该属性的 cache 元素。mode 支持以下值：emulate hypervisor 将提供假的 CPU 缓存数据。passthrough 主机 CPU 报告的真实 CPU 缓存数据将传递给虚拟 CPU。disable 虚拟 CPU 将报告指定级别的无 CPU 缓存（如果缺少 level 属性，则报告无缓存）。

- maxphysaddr

  自 8.7.0 起，maxphysaddr 元素描述虚拟 CPU 地址大小（以位为单位）。如果缺少该元素，将使用 hypervisor 默认值。mode 此强制属性指定地址大小的呈现方式。支持以下模式：passthrough 主机 CPU 报告的物理地址位数将传递给虚拟 CPU。emulate hypervisor 将通过 bits 属性定义物理地址位数的特定值，（自 9.2.0 起可选）位数不能超过 hypervisor 支持的物理地址位数。bits 如果 mode 属性设置为 emulate，则 bits 属性是必需的，并指定虚拟 CPU 地址大小（以位为单位）。limit limit 属性可用于限制 passthrough 模式的地址位数的最大值，即如果主机 CPU 报告的位数超过该值，则使用 limit。自 9.3.0 起

可以使用 numa 元素指定客户机 NUMA 拓扑。自 0.9.8 起

```
...
<cpu>
  ...
  <numa>
    <cell id='0' cpus='0-3' memory='512000' unit='KiB' discard='yes'/>
    <cell id='1' cpus='4-7' memory='512000' unit='KiB' memAccess='shared'/>
  </numa>
  ...
</cpu>
...
```

每个 cell 元素指定一个 NUMA cell 或 NUMA 节点。cpus 指定作为节点一部分的 CPU 或 CPU 范围。自 6.5.0 起对于 qemu 驱动程序，如果模拟器二进制文件支持每个 cell 中的不连续 cpu 范围，则每个 cell 中声明的所有 CPU 的总和将与 vcpu 元素中声明的最大虚拟 CPU 数匹配。这是通过将任何剩余的 CPU 填充到第一个 NUMA cell 中来完成的。鼓励用户提供完整的 NUMA 拓扑，其中 NUMA CPU 的总和与 vcpus 中声明的最大虚拟 CPU 数匹配，以使域在 qemu 和 libvirt 版本之间保持一致。memory 指定节点内存（以 kibibytes 为单位，即 1024 字节块）。自 6.6.0 起，cpus 属性是可选的，如果省略，则创建无 CPU 的 NUMA 节点。自 1.2.11 起，可以使用额外的 unit 属性（请参阅 [内存分配](https://www.libvirt.org/formatdomain.html#memory-allocation)）来定义指定内存的单位。自 1.2.7 起，所有 cell 都应该有 id 属性，以防代码中需要引用某个 cell，否则 cell 将按从 0 开始的递增顺序分配 id。不建议混合使用有和没有 id 属性的 cell，因为这可能导致意外行为。自 1.2.9 起，可选属性 memAccess 可以控制内存是映射为 "shared" 还是 "private"。这仅对大页支持的内存和 nvdimm 模块有效。每个 cell 元素可以有一个可选的 discard 属性，用于微调给定 numa 节点的 discard 功能，如 [内存后备](https://www.libvirt.org/formatdomain.html#memory-backing) 下所述。接受的值为 yes 和 no。自 4.4.0 起

此客户机 NUMA 规范目前仅适用于 QEMU/KVM 和 Xen。

NUMA 硬件架构支持 NUMA cell 之间距离的概念。自 3.10.0 起，可以使用 NUMA cell 描述中的 distances 元素定义 NUMA cell 之间的距离。sibling 子元素用于指定兄弟 NUMA cell 之间的距离值。有关更多详细信息，请参阅 ACPI（高级配置和电源接口）规范中解释系统 SLIT（系统局部性信息表）的章节。

```
...
<cpu>
  ...
  <numa>
    <cell id='0' cpus='0,4-7' memory='512000' unit='KiB'>
      <distances>
        <sibling id='0' value='10'/>
        <sibling id='1' value='21'/>
        <sibling id='2' value='31'/>
        <sibling id='3' value='41'/>
      </distances>
    </cell>
    <cell id='1' cpus='1,8-10,12-15' memory='512000' unit='KiB' memAccess='shared'>
      <distances>
        <sibling id='0' value='21'/>
        <sibling id='1' value='10'/>
        <sibling id='2' value='21'/>
        <sibling id='3' value='31'/>
      </distances>
    </cell>
    <cell id='2' cpus='2,11' memory='512000' unit='KiB' memAccess='shared'>
      <distances>
        <sibling id='0' value='31'/>
        <sibling id='1' value='21'/>
        <sibling id='2' value='10'/>
        <sibling id='3' value='21'/>
      </distances>
    </cell>
    <cell id='3' cpus='3' memory='512000' unit='KiB'>
      <distances>
        <sibling id='0' value='41'/>
        <sibling id='1' value='31'/>
        <sibling id='2' value='21'/>
        <sibling id='3' value='10'/>
      </distances>
    </cell>
  </numa>
  ...
</cpu>
...
```

描述 NUMA cell 之间的距离目前仅由 Xen 和 QEMU 支持。如果没有提供距离来描述不同 cell 之间的 SLIT 数据，将默认为本地距离为 10，远程距离为 20 的方案。

### 14.1 [ACPI 异构内存属性表](https://www.libvirt.org/formatdomain.html#id21)

```
...
<cpu>
  ...
  <numa>
    <cell id='0' cpus='0-3' memory='2097152' unit='KiB' discard='yes'>
      <cache level='1' associativity='direct' policy='writeback'>
        <size value='10' unit='KiB'/>
        <line value='8' unit='B'/>
      </cache>
    </cell>
    <cell id='1' cpus='4-7' memory='512000' unit='KiB' memAccess='shared'/>
    <interconnects>
      <latency initiator='0' target='0' type='access' value='5'/>
      <latency initiator='0' target='0' cache='1' type='access' value='10'/>
      <bandwidth initiator='0' target='0' type='access' value='204800' unit='KiB'/>
    </interconnects>
  </numa>
  ...
</cpu>
...
```

自 6.6.0 起，cell 元素可以有一个 cache 子元素，描述内存邻近域的内存侧缓存。cache 元素具有描述缓存级别的 level 属性，因此该元素可以重复多次以描述缓存的不同级别。

cache 元素具有以下强制属性：

- level

  此描述所指的缓存级别。

- associativity

  描述缓存关联性（接受的值为 none、direct 和 full）。

- policy

  描述缓存写入关联性（接受的值为 none、writeback 和 writethrough）。

cache 元素有两个强制子元素：size 和 line，分别描述缓存大小和缓存行大小。两个元素都接受两个属性：value 和 unit，用于设置相应缓存属性的值。

NUMA 描述有一个可选的 interconnects 元素，描述规范化的内存读/写延迟、发起方邻近域（处理器或 I/O）和目标邻近域（内存）之间的读/写带宽。

interconnects 元素可以有零个或多个 latency 子元素来描述两个内存节点之间的延迟，以及零个或多个 bandwidth 子元素来描述两个内存节点之间的带宽。两者都具有以下强制属性：

- initiator

  指源 NUMA 节点

- target

  指目标 NUMA 节点

- type

  访问类型。接受的值：access、read、write

- value

  实际值。对于延迟，这是延迟（以纳秒为单位），对于带宽，此值是 kibibytes/秒。使用额外的 unit 属性来更改单位。

要描述从一个 NUMA 节点到另一个 NUMA 节点的缓存的延迟，latency 元素具有可选的 cache 属性，该属性与 target 属性结合使用，创建对远程 NUMA 节点缓存级别的完整引用。例如，target='0' cache='1' 指的是 NUMA 节点 0 的第一级缓存。

- model

  model 元素的内容指定客户机请求的 CPU 模型。可用的 CPU 模型及其定义可以在安装在 libvirt 数据目录中的 cpu_map 目录中找到。如果 hypervisor 无法使用确切的 CPU 模型，libvirt 会自动回退到 hypervisor 支持的最接近的模型，同时保持 CPU 功能列表。自 0.9.10 起，可以使用可选的 fallback 属性来禁止此行为，在这种情况下，尝试启动请求不支持的 CPU 模型的域将失败。fallback 属性支持的值为：allow（默认值）和 forbid。可选的 vendor_id 属性（自 0.10.0 起）可用于设置客户机看到的供应商 ID。它必须恰好 12 个字符长。如果未设置，则使用主机的供应商 ID。典型的可能值是 "AuthenticAMD" 和 "GenuineIntel"。

- vendor

  自 0.8.3 起，vendor 元素的内容指定客户机请求的 CPU 供应商。如果缺少此元素，客户机可以在任何 CPU 上运行，只要它匹配给定的功能，无论其供应商如何。支持的供应商列表可以在 cpu_map/\*\_vendors.xml 中找到。

- topology

  topology 元素指定提供给客户机的虚拟 CPU 的请求拓扑。其属性 sockets、dies（自 6.1.0 起）、clusters（自 10.1.0 起）、cores 和 threads 接受非零正整数值。它们分别指 CPU 插槽总数、每个插槽的 die 数、每个 die 的簇数、每个簇的核心数以及每个核心的线程数。dies 和 clusters 属性是可选的，如果省略，默认为 1，而其他属性都是必需的。Hypervisor 可能要求 cpus 元素指定的最大 vCPU 数量等于拓扑产生的 vCPU 数量。此外，并非所有架构和机器类型都支持为所有属性指定除 1 之外的值。

- feature

  cpu 元素可以包含零个或多个 feature 元素，用于微调所选 CPU 模型提供的功能。已知功能名称的列表可以在与 CPU 模型相同的文件中找到。每个 feature 元素的含义取决于其 policy 属性，该属性必须设置为以下值之一：force 虚拟 CPU 将声称支持该功能，无论主机 CPU 是否支持。require 除非主机 CPU 支持该功能或 hypervisor 能够模拟它，否则客户机创建将失败。optional 虚拟 CPU 将支持该功能，当且仅当主机 CPU 支持它。disable 虚拟 CPU 将不支持该功能。forbid 如果主机 CPU 支持该功能，则客户机创建将失败。 自 0.8.5 起，policy 属性可以省略，默认值为 require。各个 CPU 功能名称在 name 属性中指定。例如，要使用 Intel IvyBridge CPU 模型明确指定 'pcid' 功能：`... <cpu match='exact'>  <model fallback='forbid'>IvyBridge</model>  <vendor>Intel</vendor>  <feature policy='require' name='pcid'/> </cpu> ...`

- deprecated_features

  自 11.0.0 起，S390 客户机可以利用 deprecated_features 属性来指定切换被 hypervisor 标记为已弃用的 CPU 模型功能。当此属性设置为 off 时，活动的客户机 XML 将反映具有 disable 策略的相应功能。当此属性设置为 on 时，相应的功能将被启用。

- cache

  自 3.3.0 起，cache 元素描述虚拟 CPU 缓存。如果缺少该元素，hypervisor 将使用合理的默认值。level 此可选属性指定元素描述的缓存级别。缺少属性意味着元素同时描述所有 CPU 缓存级别。禁止混合使用设置了 level 属性的 cache 元素和未设置该属性的 cache 元素。mode 支持以下值：emulate hypervisor 将提供假的 CPU 缓存数据。passthrough 主机 CPU 报告的真实 CPU 缓存数据将传递给虚拟 CPU。disable 虚拟 CPU 将报告没有指定级别的 CPU 缓存（如果缺少 level 属性，则完全没有缓存）。

- maxphysaddr

  自 8.7.0 起，maxphysaddr 元素描述虚拟 CPU 地址大小（以位为单位）。如果缺少该元素，则使用 hypervisor 默认值。mode 此必需属性指定地址大小的呈现方式。支持以下模式：passthrough 主机 CPU 报告的物理地址位数将传递给虚拟 CPU emulate hypervisor 将通过 bits 属性为物理地址位数定义特定值（自 9.2.0 起可选）位数不能超过 hypervisor 支持的物理地址位数。 bits 如果 mode 属性设置为 emulate，则 bits 属性是必需的，指定虚拟 CPU 地址大小（以位为单位）。limit limit 属性可用于限制 passthrough 模式的地址位数的最大值，即如果主机 CPU 报告的位数超过该值，则使用 limit。自 9.3.0 起

可以使用 numa 元素指定客户机 NUMA 拓扑。自 0.9.8 起

```
...
<cpu>
  ...
  <numa>
    <cell id='0' cpus='0-3' memory='512000' unit='KiB' discard='yes'/>
    <cell id='1' cpus='4-7' memory='512000' unit='KiB' memAccess='shared'/>
  </numa>
  ...
</cpu>
...
```

每个 cell 元素指定一个 NUMA cell 或 NUMA 节点。cpus 指定属于该节点的 CPU 或 CPU 范围。自 6.5.0 起 对于 qemu 驱动程序，如果模拟器二进制文件支持每个 cell 中的不连续 cpu 范围，则在每个 cell 中声明的所有 CPU 的总和将与 vcpu 元素中声明的最大虚拟 CPU 数量匹配。这是通过将任何剩余的 CPU 填充到第一个 NUMA cell 中来完成的。鼓励用户提供完整的 NUMA 拓扑，其中 NUMA CPU 的总和与 vcpus 中声明的最大虚拟 CPU 数量匹配，以确保域在 qemu 和 libvirt 版本之间保持一致。memory 指定节点内存（以 kibibytes 为单位，即 1024 字节块）。自 6.6.0 起，cpus 属性是可选的，如果省略，则创建无 CPU 的 NUMA 节点。自 1.2.11 起，可以使用附加的 unit 属性（请参阅 [内存分配](https://www.libvirt.org/formatdomain.html#memory-allocation)）来定义指定内存的单位。自 1.2.7 起，所有 cell 都应该有 id 属性，以防在代码中需要引用某个 cell，否则 cell 将按从 0 开始的递增顺序分配 id。不建议混合使用有和没有 id 属性的 cell，因为这可能导致意外行为。自 1.2.9 起，可选属性 memAccess 可以控制内存是映射为 "shared" 还是 "private"。这仅对大页支持的内存和 nvdimm 模块有效。每个 cell 元素可以有一个可选的 discard 属性，该属性根据 [内存后备](https://www.libvirt.org/formatdomain.html#memory-backing) 中描述的内容微调给定 numa 节点的 discard 功能。接受的值为 yes 和 no。自 4.4.0 起

此客户机 NUMA 规范目前仅适用于 QEMU/KVM 和 Xen。

NUMA 硬件架构支持 NUMA cell 之间距离的概念。自 3.10.0 起，可以使用 NUMA cell 描述中的 distances 元素定义 NUMA cell 之间的距离。sibling 子元素用于指定兄弟 NUMA cell 之间的距离值。有关更多详细信息，请参阅 ACPI（高级配置和电源接口）规范中解释系统 SLIT（系统 locality 信息表）的章节。

```
...
<cpu>
  ...
  <numa>
    <cell id='0' cpus='0,4-7' memory='512000' unit='KiB'>
      <distances>
        <sibling id='0' value='10'/>
        <sibling id='1' value='21'/>
        <sibling id='2' value='31'/>
        <sibling id='3' value='41'/>
      </distances>
    </cell>
    <cell id='1' cpus='1,8-10,12-15' memory='512000' unit='KiB' memAccess='shared'>
      <distances>
        <sibling id='0' value='21'/>
        <sibling id='1' value='10'/>
        <sibling id='2' value='21'/>
        <sibling id='3' value='31'/>
      </distances>
    </cell>
    <cell id='2' cpus='2,11' memory='512000' unit='KiB' memAccess='shared'>
      <distances>
        <sibling id='0' value='31'/>
        <sibling id='1' value='21'/>
        <sibling id='2' value='10'/>
        <sibling id='3' value='21'/>
      </distances>
    </cell>
    <cell id='3' cpus='3' memory='512000' unit='KiB'>
      <distances>
        <sibling id='0' value='41'/>
        <sibling id='1' value='31'/>
        <sibling id='2' value='21'/>
        <sibling id='3' value='10'/>
      </distances>
    </cell>
  </numa>
  ...
</cpu>
...
```

描述 NUMA cell 之间的距离目前仅由 Xen 和 QEMU 支持。如果没有给出描述不同 cell 之间 SLIT 数据的距离，它将默认为本地距离为 10、远程距离为 20 的方案。

### 14.1 [ACPI 异构内存属性表](https://www.libvirt.org/formatdomain.html#id21)

```
...
<cpu>
  ...
  <numa>
    <cell id='0' cpus='0-3' memory='2097152' unit='KiB' discard='yes'>
      <cache level='1' associativity='direct' policy='writeback'>
        <size value='10' unit='KiB'/>
        <line value='8' unit='B'/>
      </cache>
    </cell>
    <cell id='1' cpus='4-7' memory='512000' unit='KiB' memAccess='shared'/>
    <interconnects>
      <latency initiator='0' target='0' type='access' value='5'/>
      <latency initiator='0' target='0' cache='1' type='access' value='10'/>
      <bandwidth initiator='0' target='0' type='access' value='204800' unit='KiB'/>
    </interconnects>
  </numa>
  ...
</cpu>
...
```

自 6.6.0 起，cell 元素可以有一个 cache 子元素，用于描述内存邻近域的内存侧缓存。cache 元素有一个 level 属性，描述缓存级别，因此该元素可以重复多次以描述缓存的不同级别。

cache 元素具有以下必需属性：

- level

  此描述所指的缓存级别。

- associativity

  描述缓存关联度（接受的值为 none、direct 和 full）。

- policy

  描述缓存写入关联度（接受的值为 none、writeback 和 writethrough）。

cache 元素有两个必需的子元素：size 和 line，分别描述缓存大小和缓存行大小。这两个元素都接受两个属性：value 和 unit，用于设置相应缓存属性的值。

NUMA 描述有一个可选的 interconnects 元素，用于描述发起方邻近域（处理器或 I/O）和目标邻近域（内存）之间的标准化内存读/写延迟、读/写带宽。

interconnects 元素可以有零个或多个 latency 子元素来描述两个内存节点之间的延迟，以及零个或多个 bandwidth 子元素来描述两个内存节点之间的带宽。这两者都具有以下必需属性：

- initiator

  引用源 NUMA 节点

- target

  引用目标 NUMA 节点

- type

  访问类型。接受的值：access、read、write

- value

  实际值。对于延迟，这是以纳秒为单位的延迟，对于带宽，此值是以 kibibytes/秒为单位。使用附加的 unit 属性更改单位。

要描述从一个 NUMA 节点到另一个 NUMA 节点缓存的延迟，latency 元素具有可选的 cache 属性，该属性与 target 属性结合使用，创建对远程 NUMA 节点缓存级别的完整引用。例如，target='0' cache='1' 引用 NUMA 节点 0 的第一级缓存。

## 15 [事件配置](https://www.libvirt.org/formatdomain.html#id22)

有时需要覆盖对各种事件采取的默认操作。并非所有 hypervisor 都支持所有事件和操作。这些操作可能是调用 libvirt API [virDomainReboot](https://www.libvirt.org/html/libvirt-libvirt-domain.html#virDomainReboot)、[virDomainShutdown](https://www.libvirt.org/html/libvirt-libvirt-domain.html#virDomainShutdown) 或 [virDomainShutdownFlags](https://www.libvirt.org/html/libvirt-libvirt-domain.html#virDomainShutdownFlags) 的结果。使用 virsh reboot 或 virsh shutdown 也会触发事件。

```
...
<on_poweroff>destroy</on_poweroff>
<on_reboot>restart</on_reboot>
<on_crash>restart</on_crash>
<on_lockfailure>poweroff</on_lockfailure>
...
```

以下元素集合允许指定当客户机 OS 触发生命周期操作时要采取的操作。一个常见用例是在进行初始 OS 安装时将重启视为关机。这允许在首次安装后启动时重新配置 VM。

- on_poweroff

  此元素的内容指定当客户机请求关机时要采取的操作。

- on_reboot

  此元素的内容指定当客户机请求重启时要采取的操作。

- on_crash

  此元素的内容指定当客户机崩溃时要采取的操作。

每个这些状态都允许相同的四种可能操作。

- destroy

  域将被完全终止，所有资源将被释放。

- restart

  域将被终止，然后使用相同的配置重新启动。

- preserve

  域将被终止，其资源将被保留以供分析。

- rename-restart

  域将被终止，然后使用新名称重新启动。（仅由 libxl hypervisor 驱动程序支持。）

QEMU/KVM/HVF 支持 on_poweroff 和 on_reboot 事件处理 destroy 和 restart 操作，但禁止将 on_poweroff 设置为 restart 且 on_reboot 设置为 destroy 的组合。

自 0.8.4 起，on_crash 事件支持这些额外操作。

- coredump-destroy

  崩溃域的核心将被转储，然后域将被完全终止，所有资源将被释放

- coredump-restart

  崩溃域的核心将被转储，然后域将使用相同的配置重新启动

自 3.9.0 起，可以通过 [virDomainSetLifecycleAction](https://www.libvirt.org/html/libvirt-libvirt-domain.html#virDomainSetLifecycleAction) API 配置生命周期事件。

on_lockfailure 元素（自 1.0.0 起）可用于配置当锁管理器失去资源锁时应采取的操作。libvirt 识别以下操作，尽管并非所有操作都需要由各个锁管理器支持。当未指定操作时，每个锁管理器将采取其默认操作。

- poweroff

  域将被强制关机。

- restart

  域将被关机并重新启动以重新获取其锁。

- pause

  域将被暂停，以便在解决锁问题时可以手动恢复。

- ignore

  保持域运行，就像什么都没发生一样。

## 16 [电源管理](https://www.libvirt.org/formatdomain.html#id23)

自 0.10.2 起，可以强制启用或禁用对客户机 OS 的 BIOS 广告。（注意：仅 qemu 驱动程序支持）

```
...
<pm>
  <suspend-to-disk enabled='no'/>
  <suspend-to-mem enabled='yes'/>
</pm>
...
```

- pm

  这些元素启用（'yes'）或禁用（'no'）BIOS 对 S3（挂起到内存）和 S4（挂起到磁盘）ACPI 睡眠状态的支持。如果未指定任何内容，则 hypervisor 将保持其默认值。注意：此设置不能阻止客户机 OS 执行挂起，因为客户机 OS 本身可以选择规避睡眠状态的不可用性（例如，通过完全关闭来实现 S4）。

## 17 [磁盘 Throttle 组管理](https://www.libvirt.org/formatdomain.html#id24)

自 11.2.0 起，可以创建多个命名的 throttle 组，然后在 throttlefilters（disk 元素的子元素）中引用它们，以在 QEMU 中为特定磁盘形成过滤器链。限制（throttlegroups）在域内共享，因此同一组可以被不同的过滤器引用。

```
<domain>
  ...
  <throttlegroups>
    <throttlegroup>
      <group_name>limit0</group_name>
      <total_bytes_sec>10000000</total_bytes_sec>
      <read_iops_sec>400000</read_iops_sec>
      <write_iops_sec>100000</write_iops_sec>
    </throttlegroup>
  </throttlegroups>
  ...
</domain>
```

- throttlegroup

  它具有与 iotune 相同的子元素（请参阅 [硬盘、软盘、光盘](https://www.libvirt.org/formatdomain.html#hard-drives-floppy-disks-cdroms)），不同之处在于 group_name> 是必需的。

## 18 [Hypervisor 特性](https://www.libvirt.org/formatdomain.html#id25)

Hypervisor 可能允许切换某些 CPU / 机器特性的开/关。

```xml
...
<features>
  <pae/>
  <acpi/>
  <apic/>
  <hap/>
  <privnet/>
  <hyperv mode='custom'>
    <relaxed state='on'/>
    <vapic state='on'/>
    <spinlocks state='on' retries='4096'/>
    <vpindex state='on'/>
    <runtime state='on'/>
    <synic state='on'/>
    <stimer state='on'>
      <direct state='on'/>
    </stimer>
    <reset state='on'/>
    <vendor_id state='on' value='KVM Hv'/>
    <frequencies state='on'/>
    <reenlightenment state='on'/>
    <tlbflush state='on'>
      <direct state='on'/>
      <extended state='on'/>
    </tlbflush>
    <ipi state='on'/>
    <evmcs state='on'/>
    <emsr_bitmap state='on'/>
    <xmm_input state='on'/>
  </hyperv>
  <kvm>
    <hidden state='on'/>
    <hint-dedicated state='on'/>
    <poll-control state='on'/>
    <pv-ipi state='off'/>
    <dirty-ring state='on' size='4096'/>
  </kvm>
  <xen>
    <e820_host state='on'/>
    <passthrough state='on' mode='share_pt'/>
  </xen>
  <pvspinlock state='on'/>
  <gic version='2'/>
  <ioapic driver='qemu'/>
  <hpt resizing='required'>
    <maxpagesize unit='MiB'>16</maxpagesize>
  </hpt>
  <vmcoreinfo state='on'/>
  <smm state='on'>
    <tseg unit='MiB'>48</tseg>
  </smm>
  <htm state='on'/>
  <ccf-assist state='on'/>
  <msrs unknown='ignore'/>
  <cfpc value='workaround'/>
  <sbbc value='workaround'/>
  <ibs value='fixed-na'/>
  <tcg>
    <tb-cache unit='MiB'>128</tb-cache>
  </tcg>
  <async-teardown enabled='yes'/>
  <ras state='on'/>
  <ps2 state='on'/>
  <aia value='aplic-imsic'/>
</features>
...
```

- features

  features 元素包含一组可选元素，用于启用或禁用特定的 hypervisor 特性。这些特性因 hypervisor 而异，并非所有 hypervisor 都支持所有特性。

- pae

  启用 Physical Address Extension (PAE)，允许 32 位 x86 处理器访问超过 4GB 的物理内存。

- acpi

  启用 Advanced Configuration and Power Interface (ACPI)，提供操作系统与硬件之间的电源管理和配置接口。

- apic

  启用 Advanced Programmable Interrupt Controller (APIC)，提供更高级的中断管理。

- hap

  启用 Hardware Assisted Paging (HAP)，利用硬件虚拟化支持进行内存管理。

- privnet

  启用私有网络功能。

- hyperv

  配置 Hyper-V 特定的特性。mode 属性可以是 'custom' 或 'passthrough'。

- kvm

  配置 KVM 特定的特性。

- xen

  配置 Xen 特定的特性。

- pvspinlock

  启用 paravirtualized spinlock 支持，提高虚拟机内自旋锁的性能。

- gic

  配置 Generic Interrupt Controller (GIC) 版本。

- ioapic

  配置 I/O APIC 驱动程序。

- hpt

  配置 Hash Page Table (HPT) 相关设置。

- vmcoreinfo

  启用 vmcoreinfo 支持，提供虚拟机崩溃时的核心转储信息。

- smm

  启用 System Management Mode (SMM) 支持。

- htm

  启用 Hardware Transactional Memory (HTM) 支持。

- ccf-assist

  启用 CCF (Common Clock Framework) 辅助功能。

- msrs

  配置如何处理未知的 Model Specific Registers (MSRs)。

- cfpc

  配置 Control Flow Protection Control (CFPC) 设置。

- sbbc

  配置 Speculative Barrier Control (SBBC) 设置。

- ibs

  配置 Instruction Based Sampling (IBS) 设置。

- tcg

  配置 Tiny Code Generator (TCG) 相关设置。

- async-teardown

  根据 enabled 属性（值为 yes、no）启用或禁用 QEMU 异步拆卸，以改善客户机的内存回收。自 9.6.0 起（仅 QEMU）

- ras

  当启用（on）时，使用 ACPI 和客户机外部中止异常向客户机报告主机内存错误。如果未定义该属性，则使用 hypervisor 默认值。自 10.4.0 起（仅 QEMU/KVM 和 ARM virt 客户机）

- ps2

  根据 state 属性（值为 on、off）启用或禁用 PS/2 控制器的仿真，该控制器由 ps2 总线输入设备使用。如果未定义该属性，则使用 hypervisor 默认值。自 10.7.0 起（仅 QEMU）

- aia

  为 RISC-V 'virt' 客户机配置 aia（Advanced Interrupt Architecture）。value 属性的可能值为 aplic（每个插座存在一个仿真的 APLIC 设备）、aplic-imsic（每个核心存在一个 APLIC 和一个 IMSIC 设备）或 none（不支持 AIA）。如果未定义该属性，则使用 hypervisor 默认值。自 11.1.0 起（仅 QEMU/KVM 和 RISC-V 客户机）

- virtualization

  启用模拟实现 Arm 虚拟化扩展的客户机 CPU。如果未定义该属性，则使用 hypervisor 默认值。自 12.1.0 起（仅 QEMU/KVM 和 ARM virt 客户机）

## 19 [时间管理](https://www.libvirt.org/formatdomain.html#id26)

客户机时钟通常从主机时钟初始化。大多数操作系统期望硬件时钟保持在 UTC 中，这是默认设置。然而，Windows 期望它在所谓的 'localtime' 中。

```
...
<clock offset='localtime'>
  <timer name='rtc' tickpolicy='catchup' track='guest'>
    <catchup threshold='123' slew='120' limit='10000'/>
  </timer>
  <timer name='pit' tickpolicy='delay'/>
</clock>
...
```

- clock

  offset 属性接受四个可能的值，允许精细控制客户机时钟如何与主机同步。注意，并非所有 hypervisor 都支持所有模式。utc 客户机时钟在启动时始终与 UTC 同步。自 0.9.11 起，'utc' 模式可以转换为 'variable' 模式，这可以通过使用 adjustment 属性来控制。如果值为 'reset'，则永远不会进行转换（并非所有 hypervisor 都能在每次启动时同步到 UTC；在那些 hypervisor 上使用 'reset' 会导致错误）。数值强制转换为 'variable' 模式，使用该值作为初始调整。默认调整是特定于 hypervisor 的。localtime 客户机时钟在启动时将与主机配置的时区同步（如果有）。自 0.9.11 起，adjustment 属性的行为与 'utc' 模式相同。timezone 客户机时钟将使用 timezone 属性同步到请求的时区。自 0.7.7 起 variable 客户机时钟将应用相对于 UTC 或 localtime 的任意偏移，具体取决于 basis 属性。相对于 UTC（或 localtime）的 delta 使用 adjustment 属性以秒为单位指定。客户机可以随时间调整 RTC，并期望在下次重启时会被尊重。这与 'utc' 和 'localtime' 模式（带有可选属性 adjustment='reset'）形成对比，其中 RTC 调整在每次重启时都会丢失。自 0.7.7 起 自 0.9.11 起，basis 属性可以是 'utc'（默认）或 'localtime'。absolute 客户机时钟将在域启动时始终设置为 start 属性的值。start 属性接受纪元时间戳。自 8.4.0 起。 时钟可以有零个或多个 timer 子元素。自 0.8.0 起

- timer

  每个 timer 元素需要一个 name 属性，并具有其他取决于指定名称的可选属性。各种 hypervisor 支持不同的属性组合。name name 属性选择要修改的计时器，可以是 "platform"（当前不支持）、"hpet"（xen、qemu、lxc）、"kvmclock"（qemu）、"pit"（qemu）、"rtc"（qemu、lxc）、"tsc"（xen、qemu - 自 3.2.0 起）、"hypervclock"（qemu - 自 1.2.2 起）或 "armvtimer"（qemu - 自 6.1.0 起）。hypervclock 计时器为运行 Microsoft Windows 操作系统的客户机添加了对参考时间计数器和 iTSC 功能参考页的支持。track track 属性指定计时器跟踪的内容，可以是 "boot"、"guest"、"wall" 或 "realtime"。仅对 name="rtc" 或 name="platform" 有效。tickpolicy tickpolicy 属性确定当 QEMU 错过向客户机注入 tick 的截止日期时会发生什么。例如，这可能是因为客户机被暂停。delay 继续以正常速率传递 tick。客户机 OS 不会注意到任何问题，因为从它的角度来看，时间将继续正常流动。客户机中的时间现在应该落后于主机中的时间，正好是错过 tick 的时间量。catchup 以更高的速率传递 tick 以赶上错过的 tick。客户机 OS 不会注意到任何问题，因为从它的角度来看，时间将继续正常流动。一旦计时器设法赶上所有错过的 tick，客户机和主机中的时间应该匹配。merge 将错过的 tick 合并为一个 tick 并注入。客户机时间可能会延迟，具体取决于 OS 对 tick 合并的反应 discard 丢弃错过的 tick 并正常继续未来的注入。客户机 OS 将看到计时器一次性跳过多可能相当大的时间量，就好像中间的时间块根本不存在一样；不用说，这可能会导致客户机 OS 出现问题。

## 20 [性能监控事件](https://www.libvirt.org/formatdomain.html#id27)

某些平台允许监控虚拟机和内部执行的代码的性能。要启用性能监控事件，您可以在 perf 元素中指定它们，或通过 virDomainSetPerfEvents API 启用它们。然后使用 virConnectGetAllDomainStats API 检索性能值。自 2.0.0 起

```xml
...
<perf>
  <event name='cmt' enabled='yes'/>
  <event name='mbmt' enabled='no'/>
  <event name='mbml' enabled='yes'/>
  <event name='cpu_cycles' enabled='no'/>
  <event name='instructions' enabled='yes'/>
  <event name='cache_references' enabled='no'/>
  <event name='cache_misses' enabled='no'/>
  <event name='branch_instructions' enabled='no'/>
  <event name='branch_misses' enabled='no'/>
  <event name='bus_cycles' enabled='no'/>
  <event name='stalled_cycles_frontend' enabled='no'/>
  <event name='stalled_cycles_backend' enabled='no'/>
  <event name='ref_cpu_cycles' enabled='no'/>
  <event name='cpu_clock' enabled='no'/>
  <event name='task_clock' enabled='no'/>
  <event name='page_faults' enabled='no'/>
  <event name='context_switches' enabled='no'/>
  <event name='cpu_migrations' enabled='no'/>
  <event name='page_faults_min' enabled='no'/>
  <event name='page_faults_maj' enabled='no'/>
  <event name='alignment_faults' enabled='no'/>
  <event name='emulation_faults' enabled='no'/>
</perf>
...
```

| 事件名称                | 描述                                                                                       | 统计参数名称                 |
| ----------------------- | ------------------------------------------------------------------------------------------ | ---------------------------- |
| cmt                     | 平台上运行的应用程序使用的 L3 缓存（以字节为单位）                                         | perf.cmt                     |
| mbmt                    | 来自一级缓存的总系统带宽                                                                   | perf.mbmt                    |
| mbml                    | 内存控制器的内存流量带宽                                                                   | perf.mbml                    |
| cpu_cycles              | CPU 周期计数（总/经过）                                                                    | perf.cpu_cycles              |
| instructions            | 平台上运行的应用程序的指令计数                                                             | perf.instructions            |
| cache_references        | 平台上运行的应用程序的缓存命中计数                                                         | perf.cache_references        |
| cache_misses            | 平台上运行的应用程序的缓存未命中计数                                                       | perf.cache_misses            |
| branch_instructions     | 平台上运行的应用程序的分支指令计数                                                         | perf.branch_instructions     |
| branch_misses           | 平台上运行的应用程序的分支未命中计数                                                       | perf.branch_misses           |
| bus_cycles              | 平台上运行的应用程序的总线周期计数                                                         | perf.bus_cycles              |
| stalled_cycles_frontend | 平台上运行的应用程序在指令处理器管道前端的停滞 CPU 周期计数                                | perf.stalled_cycles_frontend |
| stalled_cycles_backend  | 平台上运行的应用程序在指令处理器管道后端的停滞 CPU 周期计数                                | perf.stalled_cycles_backend  |
| ref_cpu_cycles          | 平台上运行的应用程序不受 CPU 频率缩放影响的总 CPU 周期计数                                 | perf.ref_cpu_cycles          |
| cpu_clock               | 平台上运行的应用程序通过每个 CPU 的单调高分辨率计时器测量的 CPU 时钟时间计数               | perf.cpu_clock               |
| task_clock              | 平台上运行的应用程序通过特定于任务的单调高分辨率 CPU 计时器测量的任务时钟时间计数          | perf.task_clock              |
| page_faults             | 平台上运行的应用程序的页面错误计数。这包括次要、主要、无效和其他类型的页面错误             | perf.page_faults             |
| context_switches        | 平台上运行的应用程序的上下文切换计数                                                       | perf.context_switches        |
| cpu_migrations          | 平台上运行的应用程序的 CPU 迁移计数，即进程从一个逻辑处理器移动到另一个逻辑处理器          | perf.cpu_migrations          |
| page_faults_min         | 平台上运行的应用程序的次要页面错误计数，即页面存在于页面缓存中，因此避免了从存储加载的错误 | perf.page_faults_min         |
| page_faults_maj         | 平台上运行的应用程序的主要页面错误计数，即页面不存在于页面缓存中，因此必须从存储中获取     | perf.page_faults_maj         |
| alignment_faults        | 平台上运行的应用程序的对齐错误计数，即加载或存储未正确对齐时                               | perf.alignment_faults        |
| emulation_faults        | 平台上运行的应用程序的仿真错误计数，即内核捕获未实现的指令并为用户空间仿真它们时           | perf.emulation_faults        |

## 21 [设备](https://www.libvirt.org/formatdomain.html#id28)

最后一组 XML 元素都用于描述提供给客户机域的设备。所有设备都作为主 devices 元素的子元素出现。自 0.1.3 起

```
...
<devices>
  <emulator>/usr/lib/xen/bin/qemu-dm</emulator>
</devices>
...
```

- emulator

  emulator 元素的内容指定设备模型模拟器二进制文件的完全限定路径。[capabilities XML](https://www.libvirt.org/formatcaps.html) 指定了每种特定域类型/架构组合的推荐默认模拟器。

为了帮助用户识别他们关心的设备，每个设备都可以有直接的子元素 alias，该元素具有 name 属性，用户可以在其中存储设备的标识符。标识符必须有 "ua-" 前缀，并且在域内必须是唯一的。此外，标识符必须仅由以下字符组成：[a-zA-Z0-9_-]。自 3.9.0 起

```
<devices>
  <disk type='file'>
    <alias name='ua-myDisk'/>
  </disk>
  <interface type='network' trustGuestRxFilters='yes'>
    <alias name='ua-myNIC'/>
  </interface>
  ...
</devices>
```

### 21.1 [硬盘、软盘、光盘](https://www.libvirt.org/formatdomain.html#id29)

任何看起来像磁盘的设备，无论是软盘、硬盘、光盘还是半虚拟化驱动程序，都通过 disk 元素指定。

```xml
...
<devices>
  <disk type='file' snapshot='external'>
    <driver name="tap" type="aio" cache="default"/>
    <source file='/var/lib/xen/images/fv0' startupPolicy='optional'>
      <seclabel relabel='no'/>
    </source>
    <target dev='hda' bus='ide'/>
    <iotune>
      <total_bytes_sec>10000000</total_bytes_sec>
      <read_iops_sec>400000</read_iops_sec>
      <write_iops_sec>100000</write_iops_sec>
    </iotune>
    <boot order='2'/>
    <encryption type='...'>
      ...
    </encryption>
    <shareable/>
    <serial>
      ...
    </serial>
  </disk>
    ...
  <disk type='network'>
    <driver name="qemu" type="raw" io="threads" ioeventfd="on" event_idx="off"/>
    <source protocol="sheepdog" name="image_name">
      <host name="hostname" port="7000"/>
    </source>
    <target dev="hdb" bus="ide"/>
    <boot order='1'/>
    <transient/>
    <address type='drive' controller='0' bus='1' unit='0'/>
  </disk>
  <disk type='network'>
    <driver name="qemu" type="raw"/>
    <source protocol="rbd" name="image_name2">
      <host name="hostname" port="7000"/>
      <snapshot name="snapname"/>
      <config file="/path/to/file"/>
      <auth username='myuser'>
        <secret type='ceph' usage='mypassid'/>
      </auth>
    </source>
    <target dev="hdc" bus="ide"/>
  </disk>
  <disk type='block' device='cdrom'>
    <driver name='qemu' type='raw'/>
    <target dev='hdd' bus='ide' tray='open'/>
    <readonly/>
  </disk>
  <disk type='network' device='cdrom'>
    <driver name='qemu' type='raw'/>
    <source protocol="http" name="url_path" query="foo=bar&amp;baz=flurb">
      <host name="hostname" port="80"/>
      <cookies>
        <cookie name="test">somevalue</cookie>
      </cookies>
      <readahead size='65536'/>
      <timeout seconds='6'/>
    </source>
    <target dev='hde' bus='ide' tray='open'/>
    <readonly/>
  </disk>
  <disk type='network' device='cdrom'>
    <driver name='qemu' type='raw'/>
    <source protocol="https" name="url_path">
      <host name="hostname" port="443"/>
      <ssl verify="no"/>
    </source>
    <target dev='hdf' bus='ide' tray='open'/>
    <readonly/>
  </disk>
  <disk type='network' device='cdrom'>
    <driver name='qemu' type='raw'/>
    <source protocol="ftp" name="url_path">
      <host name="hostname" port="21"/>
    </source>
    <target dev='hdg' bus='ide' tray='open'/>
    <readonly/>
  </disk>
  <disk type='network' device='cdrom'>
    <driver name='qemu' type='raw'/>
    <source protocol="ftps" name="url_path">
      <host name="hostname" port="990"/>
    </source>
    <target dev='hdh' bus='ide' tray='open'/>
    <readonly/>
  </disk>
  <disk type='network' device='cdrom'>
    <driver name='qemu' type='raw'/>
    <source protocol="tftp" name="url_path">
      <host name="hostname" port="69"/>
    </source>
    <target dev='hdi' bus='ide' tray='open' rotation_rate='7200'/>
    <readonly/>
  </disk>
  <disk type='block' device='lun'>
    <driver name='qemu' type='raw'/>
    <source dev='/dev/sda'>
      <slices>
        <slice type='storage' offset='12345' size='123'/>
      </slices>
      <reservations managed='no'>
        <source type='unix' path='/path/to/qemu-pr-helper' mode='client'/>
      </reservations>
    </source>
    <target dev='sda' bus='scsi' rotation_rate='1'/>
    <address type='drive' controller='0' bus='0' target='3' unit='0'/>
  </disk>
  <disk type='block' device='disk'>
    <driver name='qemu' type='raw'/>
    <source dev='/dev/sda'/>
    <geometry cyls='16383' heads='16' secs='63' trans='lba'/>
    <blockio logical_block_size='512' physical_block_size='4096' discard_granularity='4096'/>
    <target dev='hdj' bus='ide'/>
  </disk>
  <disk type='volume' device='disk'>
    <driver name='qemu' type='raw'/>
    <source pool='blk-pool0' volume='blk-pool0-vol0'/>
    <target dev='hdk' bus='ide'/>
  </disk>
  <disk type='network' device='disk'>
    <driver name='qemu' type='raw'/>
    <source protocol='iscsi' name='iqn.2013-07.com.example:iscsi-nopool/2'>
      <host name='example.com' port='3260'/>
      <auth username='myuser'>
        <secret type='iscsi' usage='libvirtiscsi'/>
      </auth>
    </source>
    <target dev='vda' bus='virtio'/>
  </disk>
  <disk type='network' device='lun'>
    <driver name='qemu' type='raw'/>
    <source protocol='iscsi' name='iqn.2013-07.com.example:iscsi-nopool/1'>
      <host name='example.com' port='3260'/>
      <auth username='myuser'>
        <secret type='iscsi' usage='libvirtiscsi'/>
      </auth>
    </source>
    <target dev='sdb' bus='scsi'/>
  </disk>
  <disk type='network' device='disk'>
    <driver name='qemu' type='raw'/>
    <source protocol='nfs' name='PATH'>
      <host name='example.com'/>
      <identity user='USER' group='GROUP'/>
    </source>
    <target dev='vda' bus='virtio'/>
  </disk>
  <disk type='network' device='lun'>
    <driver name='qemu' type='raw'/>
    <source protocol='iscsi' name='iqn.2013-07.com.example:iscsi-nopool/0'>
      <host name='example.com' port='3260'/>
      <initiator>
        <iqn name='iqn.2013-07.com.example:client'/>
      </initiator>
    </source>
    <target dev='sdb' bus='scsi'/>
  </disk>
  <disk type='dir' device='floppy'>
    <driver name='qemu' type='fat'/>
    <source dir='/var/somefiles'>
    <target dev='fda'/>
    <readonly/>
  </disk>
  <disk type='volume' device='disk'>
    <driver name='qemu' type='raw'/>
    <source pool='iscsi-pool' volume='unit:0:0:1' mode='host'/>
    <target dev='vdb' bus='virtio'/>
  </disk>
  <disk type='volume' device='disk'>
    <driver name='qemu' type='raw'/>
    <source pool='iscsi-pool' volume='unit:0:0:2' mode='direct'/>
    <target dev='vdc' bus='virtio'/>
  </disk>
  <disk type='file' device='disk'>
    <driver name='qemu' type='qcow2' queues='4' queue_size='256' />
    <source file='/var/lib/libvirt/images/domain.qcow'/>
    <backingStore type='file'>
      <format type='qcow2'/>
      <source file='/var/lib/libvirt/images/snapshot.qcow'/>
      <backingStore type='block'>
        <format type='raw'/>
        <source dev='/dev/mapper/base'/>
        <backingStore/>
      </backingStore>
    </backingStore>
    <target dev='vdd' bus='virtio'/>
  </disk>
  <disk type='nvme' device='disk'>
    <driver name='qemu' type='raw'/>
    <source type='pci' managed='yes' namespace='1'>
      <address domain='0x0000' bus='0x01' slot='0x00' function='0x0'/>
    </source>
    <target dev='vde' bus='virtio'/>
  </disk>
  <disk type='vhostuser' device='disk'>
    <driver name='qemu' type='raw'/>
    <source type='unix' path='/tmp/vhost-blk.sock'>
      <reconnect enabled='yes' timeout='10'/>
    </source>
    <target dev='vdf' bus='virtio'/>
  </disk>
  <disk type='vhostvdpa' device='disk'>
    <driver name='qemu' type='raw'/>
    <source dev='/dev/vhost-vdpa-0' />
    <target dev='vdg' bus='virtio'/>
  </disk>
  <disk type='ctl' device='disk'>
    <source dev='/dev/cam/ctl'/>
    <target dev='sda' bus='scsi'/>
  </disk>
  <disk type='file' device='disk'>
    <driver name='qemu' type='qcow2'/>
    <source file='/path/to/datastore.qcow2'>
      <dataStore type='file'>
        <format type='raw'/>
        <source file='/path/to/datastore'/>
      <dataStore/>
    </source>
    <backingStore type='file'>
      <format type='qcow2'/>
      <source file='/var/lib/libvirt/images/base-with-data-file.qcow'>
        <dataStore type='block'>
          <format type='raw'/>
          <source dev='/dev/mapper/base2'/>
        <dataStore/>
      </source>
    </backingStore>
    <target dev='vdh' bus='virtio'/>
  </disk>
  <disk type='file' device='disk'>
    <driver name='qemu' type='qcow2' />
    <source file='/var/lib/libvirt/images/disk.qcow2'/>
    <target dev='nvme0n1' bus='nvme'/>
    <throttlefilters>
      <throttlefilter group='limit2'/>
      <throttlefilter group='limit012'/>
    </throttlefilters>
  </disk>
</devices>
...
```

- disk

  disk 元素是描述磁盘的主要容器，支持以下属性：type 有效值为 "file"、"block"、"dir"（自 0.7.5 起）、"network"（自 0.8.7 起）、"volume"（自 1.0.5 起）、"nvme"（自 6.0.0 起）、"vhostuser"（自 7.1.0 起）、"vhostvdpa"（自 9.8.0 起，QEMU 8.1.0）或 "ctl"（自 12.0.0 起），指的是磁盘的底层源。自 0.0.3 起 device 指示磁盘如何向客户机 OS 公开。此属性的可能值为 "floppy"、"disk"、"cdrom" 和 "lun"，默认为 "disk"。使用 "lun"（自 0.9.10 起）仅在 type 为 "block" 或 protocol='iscsi' 的 "network" 时有效，或者当 type 为 "volume" 且使用 iSCSI 源池进行 mode "host" 或作为使用光纤通道存储池的 [NPIV](https://wiki.libvirt.org/page/NPIV_in_libvirt) 虚拟主机总线适配器 (vHBA) 时有效。以这种方式配置，LUN 的行为与 "disk" 完全相同，不同之处在于来自客户机的通用 SCSI 命令被接受并传递到物理设备。另请注意，device='lun' 仅对实际原始设备有效，而对单个分区或 LVM 分区无效（在这些情况下，内核将拒绝通用 SCSI 命令，使其与 device='disk' 相同）。自 0.1.4 起 model 指示磁盘的仿真设备模型。通常这仅由 bus 属性指示。对于 bus "virtio"，模型可以进一步指定为 "virtio"、"virtio-transitional" 或 "virtio-non-transitional"。有关更多详细信息，请参阅 [virtio 设备模型](https://www.libvirt.org/formatdomain.html#virtio-device-models)。自 5.2.0 起 对于 bus "usb"，模型可以进一步指定为 usb-storage 或 usb-bot。对于 <disk type='disk'>，这两个模型之间没有区别。然而，对于 usb-bot，配置为 <disk type='cdrom'> 的设备在客户机 OS 中被正确暴露为 cdrom 设备。不幸的是，此配置与 usb-storage 不兼容，并且可能需要更新客户机驱动程序。

- source

  磁盘源的表示取决于 disk type 属性值，如下所示：file file 属性指定包含磁盘的文件的完全限定路径。自 0.0.3 起 自 9.0.0 起，可以添加一个新的可选属性 fdgroup，指示通过与域对象关联的文件描述符（通过 virDomainFDAssociate() API）访问磁盘，而不是打开文件。这些文件不一定必须通过文件系统可被 libvirt 访问。通过 file 传递的文件名仍可用于在执行块操作时生成写入映像元数据的路径，但 libvirt 不会本地访问这些路径。block dev 属性指定作为磁盘的主机设备的完全限定路径。自 0.0.3 起 dir dir 属性指定用作磁盘的目录的完全限定路径。自 0.7.5 起 请注意，大多数支持 dir 磁盘的 hypervisor 通过公开一个仿真块设备来实现，该设备具有填充了配置目录内容的仿真文件系统。由于客户机操作系统可能会缓存文件系统元数据，对目录的外部更改可能不会在客户机中出现和/或可能导致从 VM 可观察到的损坏数据。仿真文件系统的格式由 <driver> 驱动程序元素的 format 属性控制。目前仅支持 fat 格式。Hypervisor 可能仅支持 <readonly/> 模式。network protocol 属性指定访问请求映像的协议。可能的值为 "nbd"、"iscsi"、"rbd"、"sheepdog"、"gluster"、"vxhs"、"nfs"、"http"、"https"、"ftp"、"ftps"、"tftp" 或 "ssh"。对于除 nbd 之外的任何协议，必须使用附加属性 name 来指定要使用的卷/映像。对于 "nbd"，name 属性是可选的。可以通过将 tls 属性设置为 yes 来启用 NBD 的 TLS 传输。对于 QEMU hypervisor，可以通过主机上的 nbd_tls 和 nbd_tls_x509_cert_dir 配置选项全局控制 TLS 环境的使用。自 1.2.0 起

  | 协议     | 含义                                         | 主机数量                              | 默认端口        |
  | -------- | -------------------------------------------- | ------------------------------------- | --------------- |
  | nbd      | 运行 nbd-server 的服务器                     | 仅一个                                | 10809           |
  | iscsi    | iSCSI 服务器                                 | 仅一个                                | 3260            |
  | rbd      | RBD 的监控服务器                             | 一个或多个                            | librados 默认值 |
  | sheepdog | sheepdog 服务器之一（默认为 localhost:7000） | 零或一个                              | 7000            |
  | gluster  | 运行 glusterd 守护进程的服务器               | 一个或多个（自 2.1.0 起），之前仅一个 | 24007           |
  | vxhs     | 运行 Veritas HyperScale 守护进程的服务器     | 仅一个                                | 9999            |
  | nfs      | 运行网络文件系统的服务器                     | 仅一个（自 7.0.0 起）                 | 必须省略        |

  gluster 支持 "tcp"、"rdma"、"unix" 作为 transport 属性的有效值。nbd 支持 "tcp" 和 "unix"。其他仅支持 "tcp"。如果未指定，假设为 "tcp"。如果传输是 "unix"，则 socket 属性指定 AF_UNIX 套接字的路径。nfs 仅支持使用 "tcp" 传输，并且根本不支持使用端口，因此必须省略。

  snapshot snapshot 元素的 name 属性可以可选地指定内部快照名称，用作存储协议的源。自 1.2.11 起支持 'rbd'（仅 QEMU）。config config 元素的 file 属性提供完全限定路径到配置文件，作为网络存储协议客户端的参数。自 1.2.11 起支持 'rbd'（仅 QEMU）。auth 自 3.9.0 起，对于使用带有协议属性 "rbd"、"iscsi" 或 "ssh" 的 source 元素的 disk type "network"，支持 auth 元素。如果存在，auth 元素提供访问源所需的认证凭据。它包括一个必需的属性 username，标识认证期间使用的用户名，以及一个子元素 secret，带有必需的属性 type，以绑定到持有实际密码或其他凭据的 [libvirt secret 对象](https://www.libvirt.org/formatsecret.html)（域 XML 故意不公开密码，仅公开对管理密码的对象的引用）。已知的 secret 类型是 Ceph RBD 网络源的 "ceph" 和 iSCSI 目标的 CHAP 认证的 "iscsi"。两者都需要带有 secret 对象 UUID 的 uuid 属性或与 secret 对象中指定的键匹配的 usage 属性。encryption 自 3.9.0 起，encryption 可以是加密存储源的 source 元素的子元素。如果存在，指定存储源如何加密 有关更多信息，请参阅 [存储加密](https://www.libvirt.org/formatstorageencryption.html) 页面。注意，'qcow' 加密格式已损坏，因此不再支持用于磁盘映像。（自 4.5.0 起）reservations 自 4.4.0 起，reservations 可以是存储源的 source 元素的子元素（仅 QEMU 驱动程序）。如果存在，它启用基于 SCSI 的磁盘的持久预留。该元素有一个 mandatory managed 属性，指示预留是由 libvirt 管理还是由外部实体管理。如果 managed='yes'，则 libvirt 将处理预留的创建和释放。如果 managed='no'，则需要外部实体（如 qemu-pr-helper）来管理预留。

- backingStore

  此元素描述由同级 source 元素指定的磁盘使用的后备存储。自 1.2.4 起。如果 hypervisor 驱动程序不支持 [backingStoreInput](https://www.libvirt.org/formatdomaincaps.html#backingstoreinput)（自 5.10.0 起）域功能，则 backingStore 在输入时被忽略，仅用于输出来描述运行域的检测到的后备链。如果支持 backingStoreInput，则 backingStore 用作 source 或其他 backingStore 的后备映像，覆盖映像元数据中记录的任何后备映像信息。空的 backingStore 元素意味着同级 source 是自包含的，不基于任何后备存储。为了使检测到的后备链信息准确，必须在链中每个文件的元数据中正确指定后备格式（由 libvirt 创建的文件满足此属性，但使用现有的外部文件进行快照或块复制操作需要最终用户正确预创建文件）。backingStore 支持以下属性：type type 属性表示后备存储使用的磁盘类型，请参阅上面的 disk type 属性以获取更多详细信息和可能的值。index 此属性仅在输出中有效（在输入时被忽略），可用于在执行块操作（例如通过 virDomainBlockRebase API）时引用磁盘链的特定部分。例如，vda[2] 指的是目标为 vda 的磁盘的 index='2' 的后备存储。 此外，backingStore 支持以下子元素：format format 元素包含 type 属性，指定后备存储的内部格式，如 raw 或 qcow2。format 元素可以包含 metadata_cache 子元素，其语义与磁盘 driver 的同名子元素相同。source 此元素与 disk 中的 source 元素具有相同的结构。它指定包含数据的文件、设备或网络位置。

- mirror

  如果 hypervisor 已启动长时间运行的块作业操作，则此元素存在，其中 source 子元素中的镜像位置最终将具有与源相同的内容，并具有子元素 format 中的文件格式（可能与源的格式不同）。source 子元素的详细信息由 mirror 的 type 属性确定，类似于为整个磁盘设备元素所做的操作。job 属性提及哪个 API 启动了操作（"copy" 用于 virDomainBlockRebase API，或 "active-commit" 用于 virDomainBlockCommit API），自 1.2.7 起。ready 属性（如果存在）跟踪作业的进度：如果磁盘已知可以进行切换，则为 yes，或者自 1.2.7 起，如果作业正在完成过程中，则为 abort 或 pivot。如果 ready 不存在，则磁盘可能仍在复制。目前，此元素仅在输出中有效；在输入时被忽略。自 1.2.6 起，所有两阶段作业都存在 source 子元素。较旧的 libvirt 仅支持块复制到文件，自 0.9.12 起；为了与较旧的客户端兼容，此类作业在 mirror 元素的属性 file 和 format 中包含冗余信息。

- target

  target 元素控制磁盘在客户机 OS 下公开的总线/设备。dev 属性指示 "逻辑" 设备名称。指定的实际设备名称不保证映射到客户机 OS 中的设备名称。将其视为设备排序提示。可选的 bus 属性指定要仿真的磁盘设备类型；可能的值是特定于驱动程序的，典型值为 "ide"、"scsi"、"virtio"、"xen"、"usb"、"sata"、"sd" 或 "nvme" "sd" 自 1.1.2 起，"nvme" 自 11.5.0 起。如果省略，总线类型从设备名称的样式推断（例如，名为 'sda' 的设备通常使用 SCSI 总线导出）。可选属性 tray 指示可移动磁盘（即 CDROM 或软盘）的托盘状态，值可以是 "open" 或 "closed"，默认为 "closed"。注意，tray 的值可以在域运行时更新。可选属性 removable 为 USB 或 SCSI 磁盘设置可移动标志，其值可以是 "on" 或 "off"，默认为 "off"。可选属性 rotation_rate 为 SCSI、IDE 或 SATA 总线上的磁盘设置存储的旋转速率。1025 到 65534 范围内的值用于表示旋转介质速度（以转/分钟为单位）。值 1 用于表示固态或其他非旋转存储。这些值不需要与底层主机存储的值匹配。自 0.0.3 起；bus 属性自 0.4.3 起；tray 属性自 0.9.11 起；"usb" 属性值自 0.4.4 之后起；"sata" 属性值自 0.9.7 起；"removable" 属性值自 1.1.3 起；"rotation_rate" 属性值自 7.3.0 起 可选属性 dpofua（自 11.10.0 起，仅 QEMU 驱动程序）控制 SCSI 磁盘缓存访问的 DPO（禁用页面输出）和 FUA（强制单元访问）属性的支持（两者必须同时存在或不存在）。如果省略该值，则应用 hypervisor 默认值（可能取决于机器类型版本），这是建议的设置。

- throttlefilters

  可选的 throttlefilters 元素提供了提供额外的每设备节流链的能力 自 11.2.0 起 例如，如果我们有四个不同的磁盘，我们希望限制每个磁盘的 I/O，并且我们还希望限制所有四个磁盘的组合 I/O，我们可以通过为每个磁盘设置两个 throttlefilter 来实现这一目标：磁盘自己的过滤器（例如 limit2）和组合过滤器（例如 limit012）。throttlefilter 在 throttlefilters 中的顺序无关紧要。throttlefilters 和 iotune 应该排他使用。throttlefilter 可选的 throttlefilter 元素是引用定义的节流组。

- iotune

  可选的 iotune 元素提供了提供额外的每设备 I/O 调优的能力，每个设备的值可以不同（与 blkiotune 元素（请参阅 [块 I/O 调优](https://www.libvirt.org/formatdomain.html#block-i-o-tuning)）形成对比，后者全局应用于域）。目前，唯一可用的调优是 qemu 的块 I/O 节流。此元素有可选的子元素；任何未指定或值为 0 的子元素都意味着无限制。自 0.9.8 起 total_bytes_sec 可选的 total_bytes_sec 元素是总吞吐量限制（以字节/秒为单位）。这不能与 read_bytes_sec 或 write_bytes_sec 一起出现。read_bytes_sec 可选的 read_bytes_sec 元素是读取吞吐量限制（以字节/秒为单位）。write_bytes_sec 可选的 write_bytes_sec 元素是写入吞吐量限制（以字节/秒为单位）。total_iops_sec 可选的 total_iops_sec 元素是总 I/O 操作数/秒。这不能与 read_iops_sec 或 write_iops_sec 一起出现。read_iops_sec 可选的 read_iops_sec 元素是读取 I/O 操作数/秒。write_iops_sec 可选的 write_iops_sec 元素是写入 I/O 操作数/秒。total_bytes_sec_max 可选的 total_bytes_sec_max 元素是最大总吞吐量限制（以字节/秒为单位）。这不能与 read_bytes_sec_max 或 write_bytes_sec_max 一起出现。read_bytes_sec_max 可选的 read_bytes_sec_max 元素是最大读取吞吐量限制（以字节/秒为单位）。write_bytes_sec_max 可选的 write_bytes_sec_max 元素是最大写入吞吐量限制（以字节/秒为单位）。total_iops_sec_max 可选的 total_iops_sec_max 元素是最大总 I/O 操作数/秒。这不能与 read_iops_sec_max 或 write_iops_sec_max 一起出现。read_iops_sec_max 可选的 read_iops_sec_max 元素是最大读取 I/O 操作数/秒。write_iops_sec_max 可选的 write_iops_sec_max 元素是最大写入 I/O 操作数/秒。

- driver

  可选的 driver 元素允许指定与提供磁盘的 hypervisor 驱动程序相关的更多详细信息。自 0.1.8 起 如果 hypervisor 支持多个后端驱动程序，则 name 属性选择主要后端驱动程序名称，而可选的 type 属性提供子类型。例如，xen 支持名称 "tap"、"tap2"、"phy" 或 "file"，类型为 "aio"，而 qemu 仅支持名称 "qemu"，但支持多种类型，包括 "raw"、"bochs"、"qcow2" 和 "qed"。可选的 cache 属性控制缓存机制，可能的值为 "default"、"none"、"writethrough"、"writeback"、"directsync"（自 0.9.5 起；如 "writethrough"，但绕过主机页面缓存）和 "unsafe"（自 0.9.7 起；主机可能缓存所有磁盘 I/O，并且忽略来自客户机的同步请求）。自 0.6.0 起 可选的 error_policy 属性控制 hypervisor 在磁盘读或写错误时的行为，可能的值为 stop（在错误时挂起/暂停域）、report（向客户机 OS 报告错误；自 0.9.7 起）、ignore（忽略错误并尝试继续）和 enospace（仅当主机存储已满时暂停/暂停域；否则向客户机 OS 报告错误）。默认为 hypervisor 自行决定。自 0.8.0 起。可选的 rerror_policy 属性仅控制读取错误的行为。如果未给出 rerror_policy，则 error_policy 用于读取和写入错误。如果给出 rerror_policy，则它覆盖读取错误的 error_policy。另请注意，"enospace" 不是读取错误的有效策略，因此如果 error_policy 设置为 "enospace" 且未给出 rerror_policy，则读取错误策略将保持其默认值。自 0.9.7 起 可选的 io 属性控制 I/O 的特定策略；qemu 客户机支持 "threads" 和 "native" 自 0.8.8 起，io_uring 自 6.3.0 起（QEMU 5.0）。可选的 ioeventfd 属性允许用户设置 [域 I/O 异步处理](https://patchwork.kernel.org/patch/43390/)。可能的值为 "on" 和 "off"。自 1.2.18 起 可选的 event_idx 属性允许用户设置 [事件索引功能](https://lwn.net/Articles/542012/)。可能的值为 "on" 和 "off"。自 1.2.18 起 可选的 queues 属性指定设备的队列数。对于最佳性能，建议指定与 vCPU 数量匹配的值。自 1.0.5 起（仅 QEMU 和 KVM） 可选的 queue_size 属性指定每个队列的大小。自 4.5.0 起（仅 QEMU 和 KVM） 可选的 iothread 属性分配磁盘到 IOThread 作为由域 iothreads 的范围定义（请参阅 [IOThreads 分配](https://www.libvirt.org/formatdomain.html#iothreads-allocation)）。分配给使用指定控制器的每个 SCSI 磁盘将使用相同的 IOThread。如果需要为特定 SCSI 磁盘使用特定的 IOThread，则必须定义多个控制器，每个控制器都有特定的 iothread 值。iothread 值必须在 1 到域 iothreads 值的范围内。自 1.3.5 起（QEMU 2.4） 可选的 discard 属性控制是否支持丢弃（trim/unmap）操作。可能的值为 "unmap"（启用）和 "ignore"（禁用）。自 1.0.2 起 可选的 detect_zeroes 属性控制是否检测和优化零写入。可能的值为 "on"、"off" 和 "unmap"（检测零并使用 discard 操作）。自 1.0.2 起 可选的 copy_on_read 属性控制是否在读取时复制。可能的值为 "on" 和 "off"。自 1.2.6 起 可选的 write_zeroes 属性控制是否优化零写入。可能的值为 "on" 和 "off"。自 2.1.0 起 可选的 metadata_cache 子元素控制元数据缓存的行为。它可以有一个 mode 属性，可能的值为 "on"、"off" 和 "auto"。自 4.10.0 起

- backenddomain

  可选的 backenddomain 元素允许指定托管磁盘的后端域（也称为驱动域）。使用 name 属性指定后端域名称。自 1.2.13 起（仅 Xen）

- boot

  指定磁盘是可引导的。order 属性确定启动序列中尝试设备的顺序。在 S390 架构上，仅使用第一个引导设备。可选的 loadparm 属性是一个 8 字符字符串，S390 上的客户机可以通过 sclp 或 diag 308 查询。S390 上的 Linux 客户机可以使用 loadparm 选择引导项。自 3.5.0 起 每个设备的 boot 元素不能与 [客户机固件](https://www.libvirt.org/formatdomain.html#guest-firmware) 部分中的一般 boot 元素一起使用。自 0.8.8 起

- encryption

  自 3.9.0 起，encryption 元素首选作为 source 元素的子元素。如果存在，指定卷如何使用 "qcow" 加密。有关更多信息，请参阅 [存储加密](https://www.libvirt.org/formatstorageencryption.html) 页面。

- readonly

  如果存在，这表示设备不能被客户机修改。目前，这是 attribute device='cdrom' 的磁盘的默认设置。

- shareable

  如果存在，这表示设备预计在域之间共享（假设 hypervisor 和 OS 支持此功能），这意味着应该为该设备停用缓存。

- transient

  如果存在，这表示设备内容的更改应在客户机退出时自动还原。对于某些 hypervisor，将磁盘标记为 transient 会阻止域参与迁移、快照或块作业。仅在 vmx hypervisor（自 0.9.5 起）和 qemu hypervisor（自 6.9.0 起）中受支持。在 <transient/> 磁盘的源映像应该在多个并发运行的 VM 之间共享的情况下，可选的 shareBacking 属性应设置为 yes。注意，hypervisor 驱动程序可能需要热插拔此类磁盘，因此它仅适用于支持热插拔的配置。自 7.4.0 起 Hypervisor 可能需要存储一个临时文件，包含域运行时写入的数据，该文件可能存储在与磁盘原始源相同的位置（qemu 驱动程序将临时文件存储为 $(origsource).TRANSIENT-$(vmname)，其中 $(origsource) 是磁盘源的完整原始路径，$(vmname) 是域的名称）。

- serial

  如果存在，这指定虚拟硬盘的序列号。例如，它可能看起来像 <serial>WD-WMAP9A966149</serial>。不支持 scsi-block 设备，即那些使用 disk type='block' 且 device='lun' 在 bus='scsi' 上的设备。也不支持同一控制器上的多个 NVMe 设备，因为它们每个控制器有一个序列号，而不是每个磁盘。自 0.7.1 起 注意，根据 hypervisor 和设备类型，序列号可能会被静默截断。IDE/SATA 设备通常限制为 20 个字符。SCSI 设备根据 hypervisor 版本限制为 20、36 或 247 个字符。Hypervisor 将来也可能开始拒绝过长的序列号，而不是截断它们，因此建议通过测试所需的序列号长度范围与所需的设备和 hypervisor 组合来避免隐式截断。

- wwn

  如果存在，此元素指定虚拟硬盘或 CD-ROM 驱动器的 WWN（全球唯一名称）。它必须由 16 个十六进制数字组成。自 0.10.1 起

- vendor

  如果存在，此元素指定虚拟硬盘或 CD-ROM 设备的供应商。它不得超过 8 个可打印字符。仅适用于 'scsi' 总线。自 1.0.1 起

- product

  如果存在，此元素指定虚拟硬盘或 CD-ROM 设备的产品。对于 'scsi'，它不得超过 16 个可打印字符（自 1.0.1 起）。对于 'sata' 或 'ide'，不得超过 40 个可打印字符（自 11.1.0 起）。不支持其他总线。

- address

  如果存在，address 元素将磁盘绑定到控制器的给定插槽（实际 <controller> 设备通常可以由 libvirt 推断，尽管可以显式指定。请参阅 [控制器](https://www.libvirt.org/formatdomain.html#controllers)）。type 属性是必需的，通常为 "pci" 或 "drive"。对于 "pci" 控制器，必须存在 bus、slot 和 function 的附加属性，以及可选的 domain 和 multifunction（自 0.9.7 起）。multifunction 默认为 'off'。对于 "drive" 控制器，控制器、bus、target（自 0.9.11 起）和 unit 的附加属性可用，每个默认为 0。

- auth

  自 3.9.0 起，auth 元素首选作为 source 元素的子元素。该元素仍作为 disk 子元素读取和管理。同时使用 auth 作为 disk 和 source 的子元素是无效的。自 0.9.7 起

- geometry

  可选的 geometry 元素提供覆盖几何设置的能力。这主要对 S390 DASD 磁盘或较旧的 DOS 磁盘有用。自 0.10.0 起 cyls cyls 属性是柱面数。heads heads 属性是磁头数。secs secs 属性是每磁道的扇区数。trans 可选的 trans 属性是 BIOS 转换模式（none、lba 或 auto）

- blockio

  如果存在，blockio 元素允许覆盖以下块设备属性中的任何一个。自 0.10.2 起（QEMU 和 KVM） logical_block_size 磁盘将向客户机 OS 报告的逻辑块大小。对于 Linux，这将是 BLKSSZGET ioctl 返回的值，描述磁盘 I/O 的最小单位。physical_block_size 磁盘将向客户机 OS 报告的物理块大小。对于 Linux，这将是 BLKPBSZGET ioctl 返回的值，描述磁盘的硬件扇区大小，这可能与磁盘数据的对齐相关。discard_granularity 单个操作中可以丢弃的最小数据量。它影响 unmap 操作，并且必须是 logical_block_size 的倍数。这通常由 hypervisor 正确配置。

### 21.2 [文件系统](https://www.libvirt.org/formatdomain.html#id30)

可以从客户机直接访问的主机上的目录。自 0.3.3 起，自 0.8.5 起支持 QEMU/KVM

```
...
<devices>
  <filesystem type='template'>
    <source name='my-vm-template'/>
    <target dir='/'/>
  </filesystem>
  <filesystem type='mount' accessmode='passthrough' multidevs='remap'>
    <driver type='path' wrpolicy='immediate'/>
    <source dir='/export/to/guest'/>
    <target dir='/import/from/host'/>
    <readonly/>
  </filesystem>
  <filesystem type='mount' accessmode='mapped' fmode='644' dmode='755'>
    <driver type='path'/>
    <source dir='/export/to/guest'/>
    <target dir='/import/from/host'/>
    <readonly/>
  </filesystem>
  <filesystem type='file' accessmode='passthrough'>
    <driver type='loop' format='raw'/>
    <source file='/export/to/guest.img'/>
    <target dir='/import/from/host'/>
    <readonly/>
  </filesystem>
  <filesystem type='mount' accessmode='passthrough'>
      <driver type='virtiofs' queue='1024'/>
      <binary path='/usr/libexec/virtiofsd' xattr='on'>
         <cache mode='always'/>
         <sandbox mode='namespace'/>
         <lock posix='on' flock='on'/>
         <thread_pool size='16'/>
      </binary>
      <source dir='/path'/>
      <target dir='mount_tag'/>
      <idmap>
          <uid start='0' target='100000' count='65535'/>
          <gid start='0' target='100000' count='65535'/>
      </idmap>
  </filesystem>
  <filesystem type='mount'>
      <driver type='virtiofs' queue='1024'/>
      <source socket='/tmp/sock'/>
      <target dir='tag'/>
  </filesystem>
  <filesystem type='mount'>
      <driver type='mtp'/>
      <source dir='/export/to/guest'/>
      <target dir='mtptag'/>
  </filesystem>
  ...
</devices>
...
```

- filesystem

  filesystem 属性 type 指定源的类型。可能的值为：mount 要在客户机中挂载的主机目录。由 LXC、OpenVZ（自 0.6.2 起）和 QEMU/KVM（自 0.8.5 起）使用。如果未指定，这是默认类型。此模式也有一个可选的子元素 driver，属性 type='path' 或 type='handle'（自 0.9.7 起）。driver 块有一个可选的属性 wrpolicy，进一步控制与主机页面缓存的交互；省略该属性给出默认行为，而值 immediate 意味着在客户机文件写入操作期间触及的所有页面立即触发主机写回（自 0.9.10 起）。自 6.2.0 起，也支持 type='virtiofs'。使用 virtiofs 需要设置共享内存，请参阅指南：[Virtiofs](https://www.libvirt.org/kbase/virtiofs.html) template OpenVZ 文件系统模板。仅由 OpenVZ 驱动程序使用。file 主机文件将被视为映像并在客户机中挂载。文件系统格式将被自动检测。仅由 LXC 驱动程序使用。block 要在客户机中挂载的主机块设备。文件系统格式将被自动检测。仅由 LXC 驱动程序使用（自 0.9.5 起）。ram 内存文件系统，使用来自主机 OS 的内存。source 元素有一个单个属性 usage，以 KiB 为单位给出内存使用限制，除非通过 units 属性指定单位。仅由 LXC 驱动程序使用。（自 0.9.13 起）bind 客户机内的目录将绑定到客户机内的另一个目录。仅由 LXC 驱动程序使用（自 0.9.13 起） filesystem 元素有一个可选的属性 accessmode，指定访问源的安全模式（自 0.8.5 起）。目前这仅适用于 QEMU/KVM 驱动程序的 type='mount'。对于驱动程序类型 virtiofs，仅支持 passthrough。对于其他驱动程序类型，可能的值为：passthrough 源以客户机内用户的权限访问。如果未指定，这是默认的 accessmode。mapped 源以 libvirt 运行的用户的权限访问，文件所有者和组被映射为客户机内的用户和组。squash 与 mapped 类似，但所有写入都被丢弃。 可选的 multidevs 属性指定如何处理源中的多个设备（自 0.9.7 起）。可能的值为：passthrough 源中的多个设备通过。remap 源中的多个设备被重新映射。ignore 源中的多个设备被忽略。 可选的 fmode 和 dmode 属性指定在映射模式下创建的文件和目录的权限（自 0.9.7 起）。它们接受八进制权限值，如 "644" 或 "755"。 可选的 readonly 属性指定文件系统以只读方式导出（自 0.9.7 起）。

- driver

  可选的 driver 元素允许指定与提供文件系统的 hypervisor 驱动程序相关的更多详细信息。自 1.0.6 起 如果 hypervisor 支持多个后端驱动程序，则 type 属性选择主要后端驱动程序名称，而 format 属性提供格式类型。例如，LXC 支持类型 "loop"，格式为 "raw" 或 "nbd" 与任何格式。QEMU 支持类型 "path" 或 "handle"，但没有格式。Virtuozzo 驱动程序支持类型 "ploop"，格式为 "ploop"。对于 virtio 支持的设备，也可以设置 [Virtio 相关选项](https://www.libvirt.org/formatdomain.html#virtio-related-options)。（自 3.5.0 起）对于 virtiofs，可以使用 queue 属性指定队列大小（即队列可以容纳多少请求）。（自 6.2.0 起）QEMU 支持 mtp，它向客户机公开虚拟 USB MTP 设备。（自 10.2.0 起）

- binary

  可选的 binary 元素可以调整 virtiofsd 的选项。以下所有属性和元素都是可选的。path 属性可用于覆盖守护程序的路径。xattr 属性启用文件系统扩展属性的使用。缓存可以通过 cache 元素调整，可能的 mode 值为 none 和 always。锁定可以通过 lock 元素控制 - posix 和 flock 属性都接受值 on 或 off。（自 6.2.0 起）virtiofsd 使用的沙箱方法可以通过 sandbox 元素配置，可能的 mode 值为 namespace 和 chroot，请参阅 [virtiofsd 文档](https://qemu.readthedocs.io/en/latest/tools/virtiofsd.html) 了解更多详细信息。（自 7.2.0 起）元素 thread_pool 接受一个属性 size，定义最大线程池大小。值 "0" 禁用池。线程池有助于在使用具有更高延迟的存储时增加飞行中的请求数量。但是，它有开销，因此对于快速、低延迟的文件系统，最好将其关闭。（自 8.5.0 起）元素 openfiles 接受一个属性 max，定义文件描述符的最大数量。非正值是禁止的。打开文件数量的上限是实现定义的。（自 10.6.0 起）

- source

  主机上在客户机中访问的资源。name 属性必须与 type='template' 一起使用，dir 属性必须与 type='mount' 一起使用。对于 virtiofs，可以使用 socket 属性连接到在 libvirt 外部启动的 virtiofsd 守护程序。在这种情况下，target 元素不适用，大多数与 virtiofs 相关的选项也不适用，因为它们由 virtiofsd 控制，而不是 libvirtd。usage 属性与 type='ram' 一起使用，以 KiB 为单位设置内存限制，除非通过 units 属性指定单位。

- target

  源在客户机中可以访问的位置。对于大多数驱动程序，这是一个自动挂载点，但对于 QEMU/KVM，这只是一个导出到客户机作为挂载位置提示的任意字符串标记。

- idmap

  对于 virtiofs，可以指定 idmap 元素来映射用户命名空间中的 ID。请参阅 [容器引导](https://www.libvirt.org/formatdomain.html#container-boot) 部分了解元素的语法。自 10.0.0 起

- readonly

  启用将文件系统作为客户机的只读挂载导出，默认情况下提供读写访问（适用于 QEMU/KVM 驱动程序，自 11.0.0 起，需要 virtiofs 1.13.0）。

- space_hard_limit

  此客户机文件系统可用的最大空间。自 0.9.13 起 仅由 OpenVZ 驱动程序支持。

- space_soft_limit

  此客户机文件系统可用的最大空间。容器被允许在宽限期内超过其软限制。之后将强制执行硬限制。自 0.9.13 起 仅由 OpenVZ 驱动程序支持。

### 21.3 [设备地址](https://www.libvirt.org/formatdomain.html#id31)

许多设备都有一个可选的 <address> 子元素，用于描述设备在呈现给客户机的虚拟总线上的位置。如果在输入时省略了地址（或地址中的任何可选属性），libvirt 将生成适当的地址；但如果需要对布局进行更多控制，则需要显式地址。请参阅下面包含地址元素的设备示例。

每个地址都有一个强制属性 type，描述设备所在的总线。为给定设备选择使用哪个地址部分受设备和客户机架构的限制。例如，<disk> 设备使用 type='drive'，而 <console> 设备在 i686 或 x86_64 客户机上使用 type='pci'，或在 PowerPC64 pseries 客户机上使用 type='spapr-vio'。每种地址类型都有进一步的可选属性，控制设备将被放置在总线上的位置：

- pci

  PCI 地址有以下附加属性：domain（2 字节十六进制整数，当前未被 qemu 使用）、bus（介于 0 和 0xff 之间的十六进制值，含）、slot（介于 0x0 和 0x1f 之间的十六进制值，含）和 function（介于 0 和 7 之间的值，含）。还可以使用 multifunction 属性，它控制在 PCI 控制寄存器中为特定插槽/功能打开多功能位（自 0.9.7 起，需要 QEMU 0.13）。multifunction 默认为 'off'，但对于将使用多个功能的插槽的功能 0，应设置为 'on'。（自 4.10.0 起），支持取决于架构的 PCI 地址扩展。例如，S390 客户机的 PCI 地址将有一个 zpci 子元素，带有两个属性：uid（介于 0x0001 和 0xffff 之间的十六进制值，含）和 fid（介于 0x00000000 和 0xffffffff 之间的十六进制值，含），由 S390 上的 PCI 设备用于用户定义标识符和功能标识符。自 1.3.5 起，一些 hypervisor 驱动程序可能接受一个没有其他属性的 <address type='pci'/> 元素，作为为设备分配 PCI 地址的显式请求，而不是可能也适用于同一设备的其他类型的地址（例如 virtio-mmio）。在域 XML 中配置的 PCI 地址与客户机 OS 看到的地址之间的关系有时可能看起来令人困惑：一个单独的文档更详细地描述了 [PCI 地址如何工作](https://www.libvirt.org/pci-addresses.html)。

- drive

  驱动器地址有以下附加属性：controller（2 位控制器编号）、bus（2 位总线编号）、target（2 位目标编号）和 unit（总线上的 2 位单元编号）。

- virtio-serial

  每个 virtio-serial 地址有以下附加属性：controller（2 位控制器编号）、bus（2 位总线编号）和 slot（总线内的 2 位插槽）。

- ccid

  智能卡的 CCID 地址有以下附加属性：bus（2 位总线编号）和 slot 属性（总线内的 2 位插槽）。自 0.8.8 起。

- usb

  USB 地址有以下附加属性：bus（介于 0 和 0xfff 之间的十六进制值，含）和 port（最多四个八位字节的点表示法，例如 1.2 或 2.1.3.1）。

- spapr-vio

  在 PowerPC pseries 客户机上，设备可以分配到 SPAPR-VIO 总线。它有一个 32 位的扁平地址空间；按照惯例，设备通常分配在 0x00001000 的非零倍数，但其他地址是有效的并被 libvirt 允许。每个地址有以下附加属性：reg（起始寄存器的十六进制值地址）。自 0.9.9 起。

- ccw

  机器值为 s390-ccw-virtio 的 S390 客户机使用本机 CCW 总线进行 I/O 设备。CCW 总线地址有以下附加属性：cssid（介于 0 和 0xfe 之间的十六进制值，含）、ssid（介于 0 和 3 之间的值，含）和 devno（介于 0 和 0xffff 之间的十六进制值，含）。不允许部分指定的总线地址。如果省略，libvirt 将分配一个自由总线地址，cssid=0xfe 和 ssid=0。Virtio-ccw 设备必须将其 cssid 设置为 0xfe。自 1.0.4 起

- virtio-mmio

  这将设备放置在 virtio-mmio 传输上，目前仅适用于某些 armv7l 和 aarch64 虚拟机。virtio-mmio 地址没有任何附加属性。自 1.1.3 起 如果客户机架构是 aarch64 且机器类型是 virt，libvirt 将自动为设备分配 PCI 地址；但是，客户机配置中单个具有 virtio-mmio 地址的设备的存在将导致 libvirt 为所有其他设备分配 virtio-mmio 地址。自 3.0.0 起

- isa

  ISA 地址有以下附加属性：iobase 和 irq。自 1.2.1 起

- unassigned

  对于 PCI hostdev，<address type='unassigned'/> 允许管理员在域 XML 定义中包含 PCI hostdev，而不使其对客户机可用。这允许配置中，Libvirt 将设备管理为常规 PCI hostdev，无论客户机是否可以访问它。<address type='unassigned'/> 对所有其他设备类型都是无效的地址类型。自 6.0.0 起

### 21.4 [Virtio 相关选项](https://www.libvirt.org/formatdomain.html#id32)

QEMU 的 virtio 设备在 driver 元素下有一些与 virtio 传输相关的属性：iommu 属性启用设备使用模拟的 IOMMU。ats 属性控制 PCIe 设备的地址转换服务支持。这是使用 IOTLB 支持所必需的（请参阅 [IOMMU 设备](https://www.libvirt.org/formatdomain.html#iommu-devices)）。可能的值是 on 或 off。自 3.5.0 起

packed 属性控制 QEMU 是否应该尝试使用打包的 virtqueue。与常规拆分队列相比，打包队列仅由单个描述符环组成，替换可用和使用的环、索引和描述符缓冲区。这可以导致更好的缓存利用率和性能。是否实际使用打包的 virtqueue 取决于 QEMU、vhost 后端和客户机驱动程序之间的功能协商。可能的值是 on 或 off。自 6.3.0 起（仅 QEMU 和 KVM）

此可选属性 page_per_vq 控制暴露给客户机的通知功能的布局。启用后，每个 virtio 队列将在暴露给客户机的设备 BAR 上有一个专用页面。建议在 hypervisor 上启用 vDPA 时使用，因为它允许将通知区域映射到物理设备，这仅在页面粒度上支持。默认值由 QEMU 确定。自 7.9.0 起（QEMU 2.8）注意：一般情况下，你应该保持此选项不变，除非你非常确定你知道自己在做什么。

### 21.5 [Virtio 设备模型](https://www.libvirt.org/formatdomain.html#id33)

Virtio 设备有几种变体，其中一些仅适用于特定的机器类型或场景。变体可以通过 model 属性选择，支持以下值：

- virtio

  在没有客户机 OS 特定约束的情况下，这是推荐的选择，因为它通常可以在大范围的架构、机器类型和 libvirt 版本上正常工作。

自 5.2.0 起，以下值还可以与基于 PCI 的机器类型（传统 PCI 或 PCI Express）一起使用：

- virtio-transitional

  此设备可以与 virtio 0.9 和 virtio 1.0 客户机驱动程序一起工作，因此当需要与较旧的客户机操作系统兼容时，它是最佳选择。libvirt 将设备插入传统 PCI 插槽。

- virtio-non-transitional

  此设备只能与 virtio 1.0 客户机驱动程序一起工作，除非需要与较旧的客户机操作系统兼容，否则它是推荐的选项。libvirt 将设备插入 PCI Express 插槽或基于机器类型的传统 PCI 插槽，从而产生更优化的 PCI 拓扑。

虽然上面概述的信息适用于大多数 virtio 设备，但有几个例外：

- 对于 SCSI 控制器，由于历史原因，没有可用的 virtio 模型：请改用 virtio-scsi，它的行为与其他设备的 virtio 相同。virtio-transitional 和 virtio-non-transitional 都可以与 SCSI 控制器一起使用；
- 一些设备，如 GPU 和输入设备（键盘、平板电脑和鼠标），仅在 virtio 1.0 规范中定义，因此没有过渡变体：唯一接受的模型是 virtio，这将导致非过渡设备。

有关更多详细信息，请参阅 [qemu 补丁发布](https://lists.gnu.org/archive/html/qemu-devel/2018-12/msg00923.html) 和 [virtio-1.0 规范](https://docs.oasis-open.org/virtio/virtio/v1.0/virtio-v1.0.html)。

### 21.6 [控制器](https://www.libvirt.org/formatdomain.html#id34)

根据客户机架构，某些设备总线可以出现多次，一组虚拟设备绑定到一个虚拟控制器。通常，libvirt 可以自动推断这些控制器，而不需要显式的 XML 标记，但有时需要提供显式的 controller 元素，特别是在为预期设备热插拔的客户机规划 [PCI 拓扑](https://www.libvirt.org/pci-hotplug.html) 时。

```
...
<devices>
  <controller type='ide' index='0'/>
  <controller type='virtio-serial' index='0' ports='16' vectors='4'/>
  <controller type='virtio-serial' index='1'>
    <address type='pci' domain='0x0000' bus='0x00' slot='0x0a' function='0x0'/>
  </controller>
  <controller type='scsi' index='0' model='virtio-scsi'>
    <driver iothread='4'/>
    <address type='pci' domain='0x0000' bus='0x00' slot='0x0b' function='0x0'/>
  </controller>
  <controller type='xenbus' maxGrantFrames='64' maxEventChannels='2047'/>
  <controller type='nvme'>
    <serial>
    ...
    </serial>
  ...
</devices>
...
```

每个控制器都有一个强制属性 type，必须是 'ide'、'fdc'、'scsi'、'sata'、'usb'、'ccid'、'virtio-serial' 或 'pci' 之一，以及一个强制属性 index，它是描述总线控制器遇到顺序的十进制整数（用于 <address> 元素的 controller 属性）。自 1.3.5 起，index 是可选的；如果未指定，它将被自动分配为给定控制器类型的最低未使用索引。某些控制器类型有额外的属性来控制特定功能，例如：

- virtio-serial

  virtio-serial 控制器有两个附加的可选属性 ports 和 vectors，它们控制通过控制器可以连接多少设备。自 5.2.0 起，它支持一个可选的 model 属性，可以是 'virtio'、'virtio-transitional' 或 'virtio-non-transitional'。有关更多详细信息，请参阅 [virtio 设备模型](https://www.libvirt.org/formatdomain.html#virtio-device-models)。

- scsi

  scsi 控制器有一个可选的 model 属性，它是 'auto'、'buslogic'、'ibmvscsi'、'lsilogic'、'lsisas1068'、'lsisas1078'、'virtio-scsi'、'vmpvscsi'、'virtio-transitional'、'virtio-non-transitional'、'ncr53c90'（仅作为内置隐式控制器）、'am53c974'、'dc390' 之一。有关更多详细信息，请参阅 [virtio 设备模型](https://www.libvirt.org/formatdomain.html#virtio-device-models)。

- usb

  usb 控制器有一个可选的 model 属性，它是 "piix3-uhci"、"piix4-uhci"、"ehci"、"ich9-ehci1"、"ich9-uhci1"、"ich9-uhci2"、"ich9-uhci3"、"vt82c686b-uhci"、"pci-ohci"、"nec-xhci"、"qusb1"（带有 qemu 后端的 xen pvusb，版本 1.1）、"qusb2"（带有 qemu 后端的 xen pvusb，版本 2.0）或 "qemu-xhci" 之一。此外，自 0.10.0 起，如果需要为客户机显式禁用 USB 总线，可以使用 model='none'。自 1.0.5 起，s390 上将不构建默认 USB 控制器。自 1.3.5 起，USB 控制器接受 ports 属性来配置可以连接到控制器的设备数量。

- ide

  自 3.10.0 起，对于 vbox 驱动程序，ide 控制器有一个可选的 model 属性，它是 "piix3"、"piix4" 或 "ich6" 之一。

- xenbus

  自 5.2.0 起，xenbus 控制器有一个可选的 maxGrantFrames 属性，它指定控制器为连接的设备提供的最大授权帧数。自 6.3.0 起，xenbus 控制器支持可选的 maxEventChannels 属性，它指定客户机可以使用的最大事件通道数（PV 中断）。

- nvme

  自 11.5.0 起支持，nvme 控制器可用于支持 NVMe 磁盘。它有一个可选的 serial 子元素，就像常规磁盘一样。

注意：PowerPC64 "spapr-vio" 地址没有关联的控制器。

对于本身是 PCI 或 USB 总线上的设备的控制器，可选的子元素 <address> 可以指定控制器与其主总线的确切关系，其语义在 [设备地址](https://www.libvirt.org/formatdomain.html#device-addresses) 部分中描述。

可选的子元素 driver 可以指定驱动程序特定的选项：

- queues

  可选的 queues 属性指定控制器的队列数。为了获得最佳性能，建议指定与 vCPU 数量匹配的值。自 1.0.5 起（仅 QEMU 和 KVM）

- cmd_per_lun

  可选的 cmd_per_lun 属性指定可以在由主机控制的设备上排队的最大命令数。自 1.2.7 起（仅 QEMU 和 KVM）

- max_sectors

  可选的 max_sectors 属性指定在单个命令中传输到设备或从设备传输的最大数据量（以字节为单位）。传输长度以扇区为单位测量，其中一个扇区为 512 字节。自 1.2.7 起（仅 QEMU 和 KVM）

- ioeventfd

  可选的 ioeventfd 属性指定控制器是否应该使用 [I/O 异步处理](https://patchwork.kernel.org/patch/43390/)。接受的值是 "on" 和 "off"。自 1.2.18 起

- iothread

  自 1.3.5 起（QEMU 2.4），对于使用模型 virtio-scsi 且地址类型为 pci 和 ccw 的控制器类型 scsi 支持。可选的 iothread 属性将控制器分配给 IOThread，如域 iothreads 的范围所定义（请参阅 [IOThreads 分配](https://www.libvirt.org/formatdomain.html#iothreads-allocation)）。分配给使用指定控制器的每个 SCSI 磁盘将使用相同的 IOThread。如果需要为特定 SCSI 磁盘使用特定的 IOThread，则必须定义多个控制器，每个控制器都有特定的 iothread 值。iothread 值必须在 1 到域 iothreads 值的范围内。

- iothreads

  自 11.2.0 起（QEMU 10.0），对于使用地址类型 pci 和 ccw 的 virtio-scsi 控制器支持。与 iothread 互斥。可选的 iothreads 子元素允许通过 iothread 子元素指定多个 IOThread，属性 id 是 virtio-scsi 控制器将用于 I/O 操作的。virt 队列（请参阅 driver 的 queues 属性）自动分布在配置的 iothread 之间。可选的 iothread 元素可以有多个 queue 子元素，带有强制的 id 属性，指定 iothread 应用于处理给定的 virt 队列。如果存在队列映射，则必须配置 driver 的 queues 属性，并且所有配置的 virt 队列必须包含在映射中。virtio-scsi 设备公开请求 virt 队列 0 到 N-1，其中 N 是为设备配置的队列数。例如：`<driver queues='4>  <iothreads>    <iothread id='2'/>    <iothread id='3'/>  </iothreads> </driver> <driver queues='3'>  <iothreads>    <iothread id='2'>      <queue id='1'/>    </iothread>    <iothread id='3'>      <queue id='0'/>      <queue id='2'/>    </iothread>  </iothreads> </driver>`

- virtio 选项

  对于 virtio 控制器，也可以设置 [Virtio 相关选项](https://www.libvirt.org/formatdomain.html#virtio-related-options)。（自 3.5.0 起）

USB companion 控制器有一个可选的子元素 <master>，用于指定 companion 与其主控制器的确切关系。companion 控制器与其主控制器在同一总线上，因此 companion 索引值应相等。并非所有控制器模型都可以用作 companion 控制器，libvirt 可能为某些特定模型提供一些合理的默认值（master startport 和地址的 function 的设置）。首选的 companion 控制器是 ich-uhci[123]。

```
...
<devices>
  <controller type='usb' index='0' model='ich9-ehci1'>
    <address type='pci' domain='0' bus='0' slot='4' function='7'/>
  </controller>
  <controller type='usb' index='0' model='ich9-uhci1'>
    <master startport='0'/>
    <address type='pci' domain='0' bus='0' slot='4' function='0' multifunction='on'/>
  </controller>
  ...
</devices>
...
```

PCI 控制器有一个可选的 model 属性；此属性的可能值为

- pci-root, pci-bridge（自 1.0.5 起）
- pcie-root, dmi-to-pci-bridge（自 1.1.2 起）
- pcie-root-port, pcie-switch-upstream-port, pcie-switch-downstream-port（自 1.2.19 起）
- pci-expander-bus, pcie-expander-bus（自 1.3.4 起）
- pcie-to-pci-bridge（自 4.3.0 起）

根控制器（pci-root 和 pcie-root）有一个可选的 pcihole64 元素，指定 64 位 PCI 空洞应该有多大（以 kiB 为单位，或以 pcihole64 的 unit 属性指定的单位）。一些客户机（如 Windows XP 或 Windows Server 2003）在 QEMU 和 Seabios 足够新以支持 64 位 PCI 空洞时可能会崩溃，除非这被禁用（设置为 0）。自 1.1.2 起（仅 QEMU）

PCI 控制器还有一个可选的子元素 <model>，带有属性 name。name 属性包含 qemu 正在模拟的特定设备的名称（例如 "i82801b11-bridge"），而不仅仅是设备的类（"pcie-to-pci-bridge"、"pci-bridge"），后者在 controller 元素的 model **属性**中设置。在几乎所有情况下，你都不应该手动向控制器添加 <model> 子元素，也不应该修改由 libvirt 自动生成的元素。自 1.2.19 起（仅 QEMU）。

PCI 控制器还有一个可选的子元素 <target>，带有下面列出的属性和子元素。这些是可配置的项目，1）对客户机 OS 可见，因此必须保留以保持客户机 ABI 兼容性，2）通常留给默认值或由 libvirt 自动派生。在几乎所有情况下，你都不应该手动向控制器添加 <target> 子元素，也不应该修改由 libvirt 自动生成的元素中的值。自 1.2.19 起（仅 QEMU）。

- chassisNr

  具有属性 model="pci-bridge" 的 PCI 控制器，也可以在 <target> 子元素中具有 chassisNr 属性，用于控制 QEMU 对 pci-bridge 设备的 "chassis_nr" 选项（通常 libvirt 自动将其设置为与 pci 控制器的 index 属性相同的值）。如果设置，chassisNr 必须在 1 到 255 之间。

- chassis

  pcie-root-port 和 pcie-switch-downstream-port 控制器也可以在 <target> 子元素中具有 chassis 属性，用于设置控制器的 "chassis" 配置值，该值对虚拟机可见。如果设置，chassis 必须在 0 到 255 之间。

- port

  pcie-root-port 和 pcie-switch-downstream-port 控制器也可以在 <target> 子元素中具有 port 属性，用于设置控制器的 "port" 配置值，该值对虚拟机可见。如果设置，port 必须在 0 到 255 之间。

- hotplug

  pci-root（自 7.9.0 起）、pcie-root-port（自 6.3.0 起）和 pcie-switch-downstream-port 控制器（自 6.3.0 起）也可以在 <target> 子元素中具有 hotplug 属性，用于禁用特定控制器上设备的热插拔/卸载。对于 pci-root 控制器，设置影响基于 ACPI 的热插拔。对于其他控制器，设置影响基于 ACPI 的热插拔以及 PCIE 原生热插拔。hotplug 的默认设置是 on；应设置为 off 以禁用特定控制器上设备的热插拔/卸载。

- busNr

  pci-expander-bus 和 pcie-expander-bus 控制器可以有一个可选的 busNr 属性（1-254）。这将是新总线的总线编号；从指定值到 255 之间的所有总线编号仅可用于分配给插入到从该扩展总线开始的层次结构中的 PCI/PCIe 控制器，而小于指定值的总线编号可用于下一个较低的扩展总线（如果没有较低的扩展总线，则可用于根总线）。如果不指定 busNumber，libvirt 将在所有其他扩展总线中找到最低的现有 busNumber（如果没有其他扩展总线，则使用 256），并自动分配找到的总线 - 2 作为 busNr，这为 pci-expander-bus 和自动附加到它的 pci-bridge 提供一个总线编号（如果计划向总线层次结构添加更多 pci-bridge，应手动将 busNr 设置为较低的值）。类似的算法用于自动确定 pcie-expander-bus 的 busNr 属性，但由于 pcie-expander-bus 没有任何内置的 pci-bridge，第二个总线编号只是为必须连接到总线才能实际插入端点设备的 pcie-root-port 保留。如果打算将多个设备插入 pcie-expander-bus，必须将 pcie-switch-upstream-port 连接到插入到 pcie-expander-bus 的 pcie-root-port，并将多个 pcie-switch-downstream-port 连接到 pcie-switch-upstream-port，当然，为了使此操作正常工作，需要相应地减少 pcie-expander-bus 的 busNr，以便在其上方有足够的未使用总线编号，以容纳为上游端口提供一个总线编号和为每个下游端口提供一个总线编号（除了 pcie-root-port 和 pcie-expander-bus 本身）。

- node

  一些 PCI 控制器（pc 机器类型的 pci-expander-bus、q35 机器类型的 pcie-expander-bus，以及自 3.6.0 起，pseries 机器类型的 pci-root）可以在 <target> 子元素内有一个可选的 <node> 子元素，用于设置向客户机 OS 报告的该总线的 NUMA 节点 - 客户机 OS 然后将知道该总线上的所有设备都是指定 NUMA 节点的一部分（在将主机设备分配给域时，由 libvirt API 的用户负责将主机设备附加到正确的 pci-expander-bus）。

- index

  pSeries 客户机的 pci-root 控制器使用此属性记录它们在客户机中显示的顺序。自 3.6.0 起

- memReserve

  一些 PCI 设备具有大于 2MiB 的非可预取内存条。使用此属性覆盖固件计算的值，从而使控制器保留更多内存（以 KiB 为单位），以便可以热插拔此类 PCI 设备。对于冷插拔的 PCI 设备，固件将自动保留正确数量的内存。自 10.3.0 起

对于提供隐式 PCI 总线的机器类型，会自动添加 index=0 的 pci-root 控制器，并且需要使用 PCI 设备。pci-root 没有地址。如果有太多设备无法容纳在 pci-root 提供的一个总线上，或者指定了大于零的 PCI 总线编号，则会自动添加 PCI 桥。也可以手动指定 PCI 桥，但其地址应仅引用由已指定的 PCI 控制器提供的 PCI 总线。在 PCI 控制器索引中留下间隙可能会导致无效配置。

```
...
<devices>
  <controller type='pci' index='0' model='pci-root'/>
  <controller type='pci' index='1' model='pci-bridge'>
    <address type='pci' domain='0' bus='0' slot='5' function='0' multifunction='off'/>
  </controller>
</devices>
...
```

对于提供隐式 PCI Express (PCIe) 总线的机器类型（例如，基于 Q35 芯片组的机器类型），会自动将 index=0 的 pcie-root 控制器添加到域的配置中。pcie-root 也没有地址，提供 31 个插槽（编号 1-31），可用于连接 PCIe 或 PCI 设备（尽管 libvirt 永远不会自动将 PCI 设备分配给 PCIe 插槽，但它允许手动指定这种分配）。连接到 pcie-root 的设备不能热插拔。如果客户机配置中存在传统 PCI 设备，将自动添加 pcie-to-pci-bridge 控制器：该控制器插入到 pcie-root-port 中，提供 31 个可用的 PCI 插槽（1-31），支持热插拔（自 4.3.0 起）。如果 QEMU 二进制文件不支持相应的设备，则会添加 dmi-to-pci-bridge 控制器，通常位于 slot=0x1e 的事实标准位置。dmi-to-pci-bridge 控制器插入到 PCIe 插槽（由 pcie-root 提供）中，本身提供 31 个标准 PCI 插槽（也不支持设备热插拔）。为了在客户机系统中拥有可热插拔的 PCI 插槽，还将自动创建一个 pci-bridge 控制器并连接到自动创建的 dmi-to-pci-bridge 控制器的插槽之一；所有具有由 libvirt 自动确定的地址的客户机 PCI 设备将放置在此 pci-bridge 设备上。（自 1.1.2 起）。

具有隐式 pcie-root 的域还可以添加模型为 'pcie-root-port'、'pcie-switch-upstream-port' 和 'pcie-switch-downstream-port' 的控制器。pcie-root-port 是一种简单类型的桥接设备，只能在其上游侧连接到 pcie-root 总线上的 31 个插槽之一，并在下游侧提供单个（PCIe，可热插拔）端口（在 slot='0'）。pcie-root-port 可用于提供单个插槽，以便稍后热插拔 PCIe 设备（但本身不可热插拔 - 它必须在域启动时的配置中）。（自 1.2.19 起）

pcie-switch-upstream-port 是一种更灵活（但也更复杂）的设备，只能在其上游侧插入到 pcie-root-port 或 pcie-switch-downstream-port 中（并且仅在域启动之前 - 它不可热插拔），并在下游侧提供 32 个端口（slot='0' - slot='31'），仅接受 pcie-switch-downstream-port 设备；每个 pcie-switch-downstream-port 设备只能在其上游侧插入到 pcie-switch-upstream-port 中（同样，不可热插拔），并在其下游侧提供单个可热插拔的 pcie 端口，可以接受任何标准 pci 或 pcie 设备（或另一个 pcie-switch-upstream-port），即功能与 pcie-root-port 相同。（自 1.2.19 起）

```
...
<devices>
  <controller type='pci' index='0' model='pcie-root'/>
  <controller type='pci' index='1' model='pcie-root-port'>
    <address type='pci' domain='0x0000' bus='0x00' slot='0x01' function='0x0'/>
  </controller>
  <controller type='pci' index='2' model='pcie-to-pci-bridge'>
    <address type='pci' domain='0x0000' bus='0x01' slot='0x00' function='0x0'/>
  </controller>
</devices>
...
```

### 21.7 [设备租约](https://www.libvirt.org/formatdomain.html#id35)

使用锁管理器时，可能需要记录针对 VM 的设备租约。锁管理器将确保除非可以获取租约，否则 VM 不会启动。

```
...
<devices>
  ...
  <lease>
    <lockspace>somearea</lockspace>
    <key>somekey</key>
    <target path='/some/lease/path' offset='1024'/>
  </lease>
  ...
</devices>
...
```

- lockspace

  这是一个任意字符串，标识持有键的锁空间。锁管理器可能对锁空间名称的格式或长度施加额外的限制。

- key

  这是一个任意字符串，唯一标识要获取的租约。锁管理器可能对键的格式或长度施加额外的限制。

- target

  这是与锁空间关联的文件的完全限定路径。offset 指定租约在文件中的存储位置。如果锁管理器不需要偏移量，只需传递 0。

### 21.8 [主机设备分配](https://www.libvirt.org/formatdomain.html#id36)

#### 21.8.1 [USB / PCI / SCSI 设备](https://www.libvirt.org/formatdomain.html#id37)

连接到主机的 USB（自 0.4.4 起）、PCI（自 0.6.0 起，仅 KVM）和 SCSI（自 1.0.6 起，仅 KVM）设备可以使用 hostdev 元素传递给客户机。

```
...
<devices>
  <hostdev mode='subsystem' type='usb'>
    <source startupPolicy='optional' guestReset='off'>
      <vendor id='0x1234'/>
      <product id='0xbeef'/>
    </source>
    <boot order='2'/>
  </hostdev>
</devices>
...
```

或：

```
...
<devices>
  <hostdev mode='subsystem' type='pci' managed='yes'>
    <source writeFiltering='no'>
      <address domain='0x0000' bus='0x06' slot='0x02' function='0x0'/>
    </source>
    <boot order='1'/>
    <rom bar='on' file='/etc/fake/boot.bin'/>
  </hostdev>
</devices>
...
```

或：

```
...
<devices>
  <hostdev mode='subsystem' type='scsi' rawio='yes'>
    <source>
      <adapter name='scsi_host0'/>
      <address bus='0' target='0' unit='0'/>
    </source>
    <readonly/>
    <address type='drive' controller='0' bus='0' target='0' unit='0'/>
  </hostdev>
</devices>
...
```

或：

```
...
<devices>
  <hostdev mode='subsystem' type='scsi'>
    <source protocol='iscsi' name='iqn.2014-08.com.example:iscsi-nopool/1'>
      <host name='example.com' port='3260'/>
      <auth username='myuser'>
        <secret type='iscsi' usage='libvirtiscsi'/>
      </auth>
      <initiator>
        <iqn name='iqn.2020-07.com.example:test'/>
      </initiator>
    </source>
    <address type='drive' controller='0' bus='0' target='0' unit='0'/>
  </hostdev>
</devices>
...
```

或：

```
...
<devices>
  <hostdev mode='subsystem' type='scsi_host'>
    <source protocol='vhost' wwpn='naa.50014057667280d8'/>
  </hostdev>
</devices>
...
```

或：

```
...
<devices>
  <hostdev mode='subsystem' type='mdev' model='vfio-pci'>
    <source>
      <address uuid='c2177883-f1bb-47f0-914d-32a22e3a8804'/>
    </source>
  </hostdev>
  <hostdev mode='subsystem' type='mdev' model='vfio-ccw'>
    <source>
      <address uuid='9063cba3-ecef-47b6-abcf-3fef4fdcad85'/>
    </source>
    <address type='ccw' cssid='0xfe' ssid='0x0' devno='0x0001'/>
  </hostdev>
</devices>
...
```

- hostdev

  hostdev 元素是描述主机设备的主要容器。对于每个设备，mode 始终为 "subsystem"，type 是以下值之一，并带有附加属性说明。
  - usb USB 设备在客户机启动时从主机分离，并在客户机退出或设备热插拔后重新连接。
  - pci 对于 PCI 设备，当 managed 为 "yes" 时，它在传递给客户机之前从主机分离，并在客户机退出后重新连接到主机。如果省略 managed 或为 "no"，用户负责调用 virNodeDeviceDetachFlags（或在启动客户机或热插拔设备之前调用 virsh nodedev-detach，以及在热插拔或停止客户机后调用 virNodeDeviceReAttach（或 virsh nodedev-reattach）。自 10.3.0 起，可以使用可选的 display 属性来启用使用 vgpu 设备作为客户机的显示设备。支持的值为 on 或 off（默认）。还有一个可选的 ramfb 属性，值为 on 或 off（默认）。启用时，ramfb 属性为客户机提供内存帧缓冲区设备。此帧缓冲区允许 vgpu 在客户机内加载 gpu 驱动程序之前用作引导显示。ramfb 需要将 display 属性设置为 on。
  - scsi 对于 SCSI 设备，用户负责确保设备未被主机使用。

    如果 hypervisor 和 OS 支持，可选的 sgio（自 1.0.6 起，但当前不再被任何 hypervisor 驱动程序支持）属性指示是否为磁盘过滤非特权 SG_IO 命令。有效的设置是 "filtered" 或 "unfiltered"，默认为 "filtered"。

    可选的 rawio（自 1.2.9 起）属性指示 lun 是否需要 rawio 功能。有效的设置是 "yes" 或 "no"。请参阅 [硬盘、软盘、光盘](https://www.libvirt.org/formatdomain.html#hard-drives-floppy-disks-cdroms) 部分中的 rawio 描述。如果域中的磁盘 lun 已经具有 rawio 功能，则不需要此设置。

  - scsi_host 自 2.5.0 起 对于 SCSI 设备，用户负责确保设备未被主机使用。此类型将单个 HBA 提供的所有 LUN 传递给客户机。自 5.2.0 起，model 属性可以进一步指定为 "virtio"、"virtio-transitional" 或 "virtio-non-transitional"。有关更多详细信息，请参阅 [virtio 设备模型](https://www.libvirt.org/formatdomain.html#virtio-device-models)。
  - mdev 对于中介设备（自 3.2.0 起），model 属性指定设备 API，该 API 确定主机的 vfio 驱动程序如何向客户机公开设备。目前，支持 model='vfio-pci'、model='vfio-ccw'（自 4.4.0 起）和 model='vfio-ap'（自 4.9.0 起）。[MDEV](https://www.libvirt.org/drvnodedev.html#mediated-devices-mdevs) 部分提供了有关中介设备的更多信息以及如何在主机上创建中介设备。自 4.6.0 起（QEMU 2.12），可以使用可选的 display 属性来启用或禁用由中介设备（如 NVIDIA vGPU 或 Intel GVT-g）支持的加速远程桌面，作为模拟 [视频设备](https://www.libvirt.org/formatdomain.html#video-devices) 的替代方案。此属性仅限于 model='vfio-pci'。支持的值为 on 或 off（默认值为 'off'）。使用此属性需要使用图形帧缓冲区（请参阅 [图形帧缓冲区](https://www.libvirt.org/formatdomain.html#graphical-framebuffers)），目前仅支持 VNC、Spice 和 egl-headless 图形设备。自版本 5.10.0 起，对于 model='vfio-pci' 的设备，有一个可选的 ramfb 属性。支持的值为 on 或 off（默认值为 'off'）。启用时，此属性为客户机提供内存帧缓冲区设备。当 vgpu 设备是主显示时，此帧缓冲区将用作引导显示。
  - 注意：根据 model 属性，客户机地址类型的使用也有一些影响，请参阅下面的 address 元素。
    注意：managed 属性仅用于 type='pci'，被所有其他设备类型忽略，因此使用 PCI 设备以外的设备显式设置 managed 与省略它具有相同的效果。同样，model 属性仅由中介设备支持，被所有其他设备类型忽略。

- source

  source 元素使用以下机制描述从主机看到的设备：
  - usb USB 设备可以通过 vendor 和 product 元素使用供应商/产品 ID 寻址，或通过 address 元素使用设备在主机上的地址寻址。
    自 1.0.0 起，USB 设备的 source 元素可能包含 startupPolicy 属性，可用于定义如果未找到指定的主机 USB 设备时的策略。该属性接受以下值：
    | mandatory | 任何原因缺失时失败（默认） |
    | --------- | ----------------------------------------------------- |
    | requisite | 启动时缺失失败，迁移/恢复/恢复时缺失丢弃 |
    | optional | 任何启动尝试时缺失丢弃 |
    自 8.6.0 起，source 元素可以包含 guestReset 属性，具有以下值：
    | off | 忽略所有客户机发起的设备重置请求 |
    | ------------- | -------------------------------------------------------------------------------- |
    | uninitialized | 如果设备已初始化，则忽略设备请求，否则执行重置 |
    | on | 每次客户机发起请求时重置设备 |
    当分配具有在重置时崩溃的固件的 USB 设备时，此属性可能很有帮助。
  - pci PCI 设备只能通过其地址描述。自 6.8.0 起（仅 Xen），PCI 设备的 source 元素可能包含 writeFiltering 属性，用于控制对 PCI 配置空间的写访问。默认情况下，Xen 只允许对配置空间写入已知安全的值。设置 writeFiltering='no' 将允许对设备的 PCI 配置空间的所有写入。
  - scsi SCSI 设备由 adapter 和 address 元素描述。address 元素包括 bus 属性（2 位总线编号）、target 属性（10 位目标编号）和 unit 属性（总线上的 20 位单元编号）。并非所有 hypervisor 都支持较大的 target 和 unit 值。由每个 hypervisor 决定 adapter 支持的最大值。

    自 1.2.8 起，SCSI 设备的 source 元素可能包含 protocol 属性。当该属性设置为 "iscsi" 时，主机设备 XML 遵循网络磁盘设备（请参阅 [硬盘、软盘、光盘](https://www.libvirt.org/formatdomain.html#hard-drives-floppy-disks-cdroms)），使用相同的 name 属性，并可选使用 auth 元素提供 iSCSI 服务器的认证凭据。

    自 6.7.0 起，可选的 initiator 子元素通过其 <iqn name='iqn...' 子元素控制 hypervisor 运行的发起者的 IQN。

  - scsi_host 自 2.5.0 起，单个 SCSI HBA 后面的多个 LUN 由设置为 "vhost" 的 protocol 属性和作为在主机 configfs 中建立的 vhost_scsi wwpn（带有 "naa." 前缀的 16 个十六进制数字）的 wwpn 属性描述。
  - mdev 中介设备（自 3.2.0 起）由 address 元素描述。address 元素包含单个强制属性 uuid。

- vendor, product

  vendor 和 product 元素各有一个 id 属性，指定 USB 供应商和产品 ID。ID 可以以十进制、十六进制（以 0x 开头）或八进制（以 0 开头）形式给出。

- boot

  指定设备是可引导的。order 属性确定启动序列中尝试设备的顺序。每个设备的 boot 元素不能与 [客户机固件](https://www.libvirt.org/formatdomain.html#guest-firmware) 部分中的一般 boot 元素一起使用。自 0.8.8 起适用于 PCI 设备，自 1.0.1 起适用于 USB 设备。

- rom

  rom 元素用于更改 PCI 设备的 ROM 如何呈现给客户机。可选的 bar 属性可以设置为 "on" 或 "off"，并确定设备的 ROM 是否会在客户机的内存映射中可见。（在 PCI 文档中，"rombar" 设置控制 ROM 的基地址寄存器的存在）。如果未指定 rom bar，则使用 qemu 默认值（较旧版本的 qemu 使用 "off" 的默认值，而较新的 qemu 使用 "on" 的默认值）。自 0.9.7 起（仅 QEMU 和 KVM）。可选的 file 属性包含一个二进制文件的绝对路径，该文件将作为设备的 ROM BIOS 呈现给客户机。这对于例如为支持 sr-iov 的以太网设备的虚拟功能（其 VF 没有引导 ROM）提供 PXE 引导 ROM 可能很有用。自 0.9.10 起（仅 QEMU 和 KVM）。可选的 enabled 属性可以设置为 no 以完全禁用设备的 PCI ROM 加载；如果通过此属性禁用了 PCI ROM 加载，尝试使用 bar 或 file 属性进一步调整加载过程将被拒绝。自 4.3.0 起（仅 QEMU 和 KVM）。

- address

  USB 设备的 address 元素有一个 bus 属性，用于指定 USB 总线。此外，需要 device 属性或 port 属性来识别主机上的设备。虽然设备编号是在设备连接时分配的，但端口编号是物理主机端口的稳定标识符。总线和设备编号可以以十进制、十六进制（以 0x 开头）或八进制（以 0 开头）形式给出。端口编号是点表示法（例如：2、1.2.5）。对于 PCI 设备，该元素携带 4 个属性，允许指定设备，如 lspci 或 virsh nodedev-list 所示。对于 SCSI 设备，必须使用 'drive' 地址类型。对于中介设备，它们是定义物理父设备上资源分配的纯软件设备，使用的地址类型必须符合 element hostdev 的 model 属性，例如，对于 vfio-pci 设备 API，任何非 PCI 的地址类型，或对于 vfio-ccw 设备 API，任何非 CCW 的地址类型都将导致错误。有关 address 元素的更多详细信息，请参阅 [设备地址](https://www.libvirt.org/formatdomain.html#device-addresses) 部分。

- driver

  PCI hostdev 设备可以有一个可选的 driver 子元素，指定在准备将设备分配给客户机时要绑定到设备的主机驱动程序。自 10.0.0 起（仅对 QEMU 和 KVM 有用）。这是通过设置 <driver> 元素的 model 属性来完成的，例如：`...  <hostdev mode='subsystem' type='pci' managed='yes'>    <driver model='vfio-pci-igb'/> ...` 告诉 libvirt 在将设备交给 QEMU 分配给客户机之前，将驱动程序 "vfio-pci-igb" 绑定到主机上的设备。通常，libvirt 会将设备绑定到它在内核的 modules.alias 文件中找到的 "最佳匹配" VFIO 类型驱动程序（基于匹配设备的 modalias 文件在 sysfs 中的相应字段），或者如果没有找到更好的匹配，则绑定到通用的 "vfio-pci" 驱动程序（在 libvirt 10.0.0 之前始终使用 vfio-pci），但在正确的驱动程序未在 modules.alias 中列出的情况下，可以通过设置驱动程序名称来强制使用所需的设备特定驱动程序，或者如果找到的设备特定驱动程序在某种程度上是"有问题的"，则同样可以强制使用通用的 vfio-pci 驱动程序。自 12.1.0 起（仅 QEMU 和 KVM），iommufd 元素可用于为 VFIO 设备启用 IOMMUFD 后端。这提供了一个接口，用于将 DMA 映射传播到内核以用于分配的设备。Libvirt 将打开 /dev/iommu 和 VFIO 设备 cdev，并将相关的文件描述符传递给 QEMU。（注意：自 1.0.5 起，name 属性已被描述为用于选择 PCI 设备分配的类型（"vfio"、"kvm" 或 "xen"），但这些值大多无用，因为设备分配的类型实际上由使用的 hypervisor 决定。这意味着你可能偶尔会在域的状态 XML 中看到 <driver name='vfio'/> 或 <driver name='xen'/>，或者更罕见地在配置中看到，但这些特定值基本上被忽略。）

- readonly

  表示设备是只读的，现在仅由 SCSI 主机设备支持。自 1.0.6 起（仅 QEMU 和 KVM）

- shareable

  如果存在，这表示设备预计在域之间共享（假设 hypervisor 和 OS 支持此功能）。仅由 SCSI 主机设备支持。自 1.0.6 起，但仅自 1.2.2 起按预期工作。

#### 21.8.2 [ACPI 通用发起者](https://www.libvirt.org/formatdomain.html#id38)

主机设备可以包含 <acpi> 元素，用于在 QEMU 中为设备创建 ACPI 通用发起者对象。

这可用于 **NVIDIA 多实例 GPU (MIG)** 配置，其中物理 GPU 被分区为多个隔离的实例，每个实例与一个或多个虚拟 NUMA 节点相关联。

通过将 <acpi nodeset=.../> 元素附加到域 XML 中的 MIG 设备，客户机将为该实例配置正确的分区。

```
<numa>
  <cell id='0' cpus='0-15' memory='8388608' unit='KiB'/>
  <cell id='1' memory='0' unit='KiB'/>
  <cell id='2' memory='0' unit='KiB'/>
  <cell id='3' memory='0' unit='KiB'/>
  <cell id='4' memory='0' unit='KiB'/>
  <cell id='5' memory='0' unit='KiB'/>
  <cell id='6' memory='0' unit='KiB'/>
  <cell id='7' memory='0' unit='KiB'/>
  <cell id='8' memory='0' unit='KiB'/>
</numa>
...
<hostdev mode='subsystem' type='pci' managed='yes'>
  <source>
    <address domain='0x0000' bus='0x06' slot='0x12' function='0x1'/>
  </source>
  <acpi nodeset='1-8'/>
  <address type='pci' domain='0x0000' bus='0x00'
           slot='0x02' function='0x0'/>
</hostdev>
```

<acpi> 的属性：

- nodeset

  将与设备关联的 NUMA 节点 ID 列表。集合中的每个节点都会导致 libvirt 在 QEMU 中创建一个 acpi-generic-initiator 对象，绑定到此设备。该值使用标准的 libvirt _nodeset_ 语法（例如 0-3,5）。

如果省略 <acpi> 元素，则不为设备创建 acpi-generic-initiator 对象。

#### 21.8.3 [块 / 字符设备](https://www.libvirt.org/formatdomain.html#id39)

主机的块/字符设备可以使用 hostdev 元素传递给客户机。这仅在基于容器的虚拟化中可能。设备通过完全限定路径指定。自 1.0.1 之后的 LXC：

```
...
<hostdev mode='capabilities' type='storage'>
  <source>
    <block>/dev/sdf1</block>
  </source>
</hostdev>
...
...
<hostdev mode='capabilities' type='misc'>
  <source>
    <char>/dev/input/event3</char>
  </source>
</hostdev>
...
...
<hostdev mode='capabilities' type='net'>
  <source>
    <interface>eth0</interface>
  </source>
</hostdev>
...
```

- hostdev

  hostdev 元素是描述主机设备的主要容器。对于块/字符设备传递，mode 始终为 "capabilities"，type 对于块设备为 "storage"，对于字符设备为 "misc"，对于主机网络接口为 "net"。

- source

  source 元素描述从主机看到的设备。对于块设备，主机 OS 中块设备的路径在嵌套的 "block" 元素中提供，而对于字符设备，使用 "char" 元素。对于网络接口，接口的名称在 "interface" 元素中提供。

### 21.9 [重定向设备](https://www.libvirt.org/formatdomain.html#id40)

通过字符设备重定向 USB 设备自 0.9.5 之后支持（仅 KVM）：

```
...
<devices>
  <redirdev bus='usb' type='spicevmc'/>
  <redirdev bus='usb' type='tcp'>
    <source mode='connect' host='localhost' service='4000'/>
    <boot order='1'/>
  </redirdev>
  <redirfilter>
    <usbdev class='0x08' vendor='0x1234' product='0xbeef' version='2.56' allow='yes'/>
    <usbdev allow='no'/>
  </redirfilter>
</devices>
...
```

- redirdev

  redirdev 元素是描述重定向设备的主要容器。对于 USB 设备，bus 必须为 "usb"。需要一个附加属性 type，匹配支持的串行设备类型之一（请参阅 [控制台、串行、并行和通道设备](https://www.libvirt.org/formatdomain.html#consoles-serial-parallel-channel-devices)），以描述隧道的主机端；type='tcp' 或 type='spicevmc'（使用 SPICE 图形设备的 usbredir 通道（请参阅 [图形帧缓冲区](https://www.libvirt.org/formatdomain.html#graphical-framebuffers)））是典型的。redirdev 元素有一个可选的子元素 <address>，可以将设备绑定到特定的控制器。根据给定的类型，可能需要进一步的子元素，例如 <source>，尽管不需要 <target> 子元素（因为字符设备的消费者是 hypervisor 本身，而不是客户机中可见的设备）。

- boot

  指定设备是可引导的。order 属性确定启动序列中尝试设备的顺序。每个设备的 boot 元素不能与 [客户机固件](https://www.libvirt.org/formatdomain.html#guest-firmware) 部分中的一般 boot 元素一起使用。（自 1.0.1 起）

- redirfilter

  redirfilter 元素用于创建过滤规则，以过滤掉某些要重定向的设备。它使用子元素 <usbdev> 定义每个过滤规则。class 属性是 USB 类代码，例如，0x08 表示大容量存储设备。USB 设备可以通过 vendor 和 product 属性使用供应商/产品 ID 寻址。version 是来自 bcdDevice 字段的设备修订版（不是 USB 协议的版本）。这四个属性是可选的，-1 可用于允许它们的任何值。allow 属性是必需的，'yes' 表示允许，'no' 表示拒绝。

### 21.10 [智能卡设备](https://www.libvirt.org/formatdomain.html#id41)

可以通过 smartcard 元素向客户机提供虚拟智能卡设备。主机上的 USB 智能卡读取器设备不能通过简单的设备传递在客户机上使用，因为它随后将在主机上不可用，可能在"移除"时锁定主机计算机。因此，一些 hypervisor 提供了一种专门的虚拟设备，可以向客户机呈现智能卡接口，具有几种模式，用于描述如何从主机或甚至从创建到第三方智能卡提供商的通道获取凭据。自 0.8.8 起

```
...
<devices>
  <smartcard mode='host'/>
  <smartcard mode='host-certificates'>
    <certificate>cert1</certificate>
    <certificate>cert2</certificate>
    <certificate>cert3</certificate>
    <database>/etc/pki/nssdb/</database>
  </smartcard>
  <smartcard mode='passthrough' type='tcp'>
    <source mode='bind' host='127.0.0.1' service='2001'/>
    <protocol type='raw'/>
    <address type='ccid' controller='0' slot='0'/>
  </smartcard>
  <smartcard mode='passthrough' type='spicevmc'/>
</devices>
...
```

<smartcard> 元素有一个强制属性 mode。支持以下模式；在每种模式下，客户机在其 USB 总线上看到一个设备，其行为类似于物理 USB CCID（芯片/智能卡接口设备）卡。

- host

  最简单的操作，其中 hypervisor 通过 NSS 将来自客户机的所有请求中继到对主机智能卡的直接访问。不需要其他属性或子元素。有关可选 <address> 子元素的使用，请参见下文。

- host-certificates

  不需要将智能卡插入主机，而是可以提供主机数据库中存在的三个 NSS 证书名称。这些证书可以通过命令 certutil -d /etc/pki/nssdb -x -t CT,CT,CT -S -s CN=cert1 -n cert1 生成，生成的三个证书名称必须作为三个 <certificate> 子元素的内容提供。附加子元素 <database> 可以指定替代目录的绝对路径（与创建证书时 certutil 命令的 -d 选项匹配）；如果不存在，默认为 /etc/pki/nssdb。

- passthrough

  不是让 hypervisor 直接与主机通信，而是可以通过辅助字符设备将所有请求通过隧道传输到第三方提供商（可能反过来与智能卡通信或使用三个证书文件）。在这种操作模式下，需要一个附加属性 type，匹配支持的串行设备类型之一（请参阅 [控制台、串行、并行和通道设备](https://www.libvirt.org/formatdomain.html#consoles-serial-parallel-channel-devices)），以描述隧道的主机端；type='tcp' 或 type='spicevmc'（使用 SPICE 图形设备的智能卡通道（请参阅 [图形帧缓冲区](https://www.libvirt.org/formatdomain.html#graphical-framebuffers)））是典型的。根据给定的类型，可能需要进一步的子元素，例如 <source>，尽管不需要 <target> 子元素（因为字符设备的消费者是 hypervisor 本身，而不是客户机中可见的设备）。

每种模式都支持可选的子元素 <address>（请参阅 [设备地址](https://www.libvirt.org/formatdomain.html#device-addresses)），它微调智能卡和 ccid 总线控制器之间的相关性。目前，qemu 最多只支持一个智能卡，地址为 bus=0 slot=0。

### 21.11 [网络接口](https://www.libvirt.org/formatdomain.html#id42)

```
...
<devices>
  <interface type='direct' trustGuestRxFilters='yes'>
    <source dev='eth0'/>
    <mac address='52:54:00:5d:c7:9e'/>
    <boot order='1'/>
    <rom bar='off'/>
    <acpi index='4'/>
  </interface>
</devices>
...
```

有几种指定客户机可见的网络接口的可能性。下面的每个子部分提供了有关常见设置选项的更多详细信息。

自 1.2.10 起，interface 元素属性 trustGuestRxFilters 通过将属性设置为 yes，为主机提供检测和信任来自客户机的关于接口 mac 地址和接收过滤器更改的报告的能力。出于安全原因，该属性的默认设置为 no，支持取决于客户机网络设备模型以及主机上的连接类型 - 目前仅支持 virtio 设备模型和主机上的 macvtap 连接。

每个 <interface> 元素都有一个可选的 <address> 子元素，可以将接口绑定到特定的 pci 插槽，属性 type='pci'，如 [设备地址](https://www.libvirt.org/formatdomain.html#device-addresses) 部分中所述。

自 6.6.0 起，可以通过向 <mac/> 元素添加 type="static" 属性来强制 libvirt 在 MAC 地址在保留的 VMware 范围内时保持提供的 MAC 地址。请注意，如果提供的 MAC 地址在保留的 VMWare 范围之外，此属性是无用的。

自 11.2.0 起，<mac/> 元素可以可选地包含 currentAddress 属性（仅输出），如果客户机更改了它，则包含新的 MAC 地址。这目前仅在 QEMU/KVM 中的模型类型 virtio 上实现，并且需要将 trustGuestRxFilters 设置为 yes。

自 7.3.0 起，可以为网络接口设置 ACPI 索引。对于某些操作系统（例如带有 systemd 的 Linux），ACPI 索引用于提供网络接口设备命名，该命名在分配给设备的 PCI 地址更改时保持稳定。此值需要在所有设备中唯一，并且在 1 到 (16\*1024-1) 之间。

#### 21.11.1 [虚拟网络](https://www.libvirt.org/formatdomain.html#id43)

**这是在具有动态/无线联网配置的主机上进行一般客户机连接的推荐配置。**（或多主机环境，其中主机硬件详细信息在 <network> 定义中单独描述 自 0.9.4 起）。

提供一个连接，其详细信息由命名的网络定义描述。根据虚拟网络的 "forward mode" 配置，网络可能完全隔离（未给出 <forward> 元素）、NAT 到显式网络设备或默认路由（<forward mode='nat'>）、无 NAT 路由（<forward mode='route'/>），或直接连接到主机的网络接口之一（通过 macvtap）或桥接设备（<forward mode='bridge|private|vepa|passthrough'/> 自 0.9.4 起）

对于转发模式为 bridge、private、vepa 和 passthrough 的网络，假设主机已经在 libvirt 范围之外设置了任何必要的 DNS 和 DHCP 服务。对于隔离、nat 和 routed 网络，libvirt 在虚拟网络上提供 DHCP 和 DNS，IP 范围可以通过使用 'virsh net-dumpxml [networkname]' 检查虚拟网络配置来确定。有一个名为 'default' 的虚拟网络开箱即用，它对默认路由进行 NAT，并具有 192.168.122.0/255.255.255.0 的 IP 范围。每个客户机将创建一个名为 vnetN 的关联 tun 设备，也可以使用 <target> 元素覆盖（请参阅 [覆盖目标元素](https://www.libvirt.org/formatdomain.html#overriding-the-target-element)）。

当接口的源是网络时，可以与网络名称一起指定 portgroup；一个网络可能定义多个 portgroup，每个 portgroup 包含不同类别的网络连接的略有不同的配置信息。自 0.9.4 起。

当客户机运行时，类型为 network 的接口可能包含 portid 属性。这提供了关联的 virNetworkPortPtr 对象的 UUID，该对象记录域接口和网络之间的关联。此属性是只读的，因为端口对象在启动和关闭期间自动创建和删除。自 5.1.0 起

此外，类似于直接网络连接（如下所述），类型为 network 的连接可以指定 virtualport 元素，其中包含要转发到 vepa（802.1Qbg）或 802.1Qbh 兼容交换机（自 0.8.2 起）或 Open vSwitch 虚拟交换机（自 0.9.11 起）的配置数据。

由于交换机的实际类型可能因主机上 <network> 中的配置而异，因此可以省略 virtualport type 属性，并指定来自多个不同 virtualport 类型的属性（也可以省略某些属性）；在域启动时，通过合并网络和接口引用的 portgroup 中定义的类型和属性，将构造完整的 <virtualport> 元素。新构造的 virtualport 是它们的组合。较低 virtualport 的属性不能更改在较高 virtualport 中定义的属性。接口优先级最高，portgroup 优先级最低。（自 0.10.0 起）。例如，为了与 802.1Qbh 交换机和 Open vSwitch 交换机都正常工作，您可以选择不指定类型，但同时指定 profileid（如果交换机是 802.1Qbh）和 interfaceid（如果交换机是 Open vSwitch）（您也可以省略其他属性，如 managerid、typeid 或 profileid，从网络的 <virtualport> 中填充）。如果要限制客户机仅连接到某些类型的交换机，可以指定 virtualport 类型，但仍然省略一些/所有参数 - 在这种情况下，如果主机的网络具有不同类型的 virtualport，则接口的连接将失败。

```
...
<devices>
  <interface type='network'>
    <source network='default'/>
  </interface>
  ...
  <interface type='network'>
    <source network='default' portgroup='engineering'/>
    <target dev='vnet7'/>
    <mac address="00:11:22:33:44:55"/>
    <virtualport>
      <parameters instanceid='09b11c53-8b5c-4eeb-8f00-d84eaa0aaa4f'/>
    </virtualport>
  </interface>
</devices>
...
```

#### 21.11.2 [桥接到 LAN](https://www.libvirt.org/formatdomain.html#id44)

**这是在具有静态有线联网配置的主机上进行一般客户机连接的推荐配置。**

提供从 VM 直接到 LAN 的桥接。这假设主机上有一个桥接设备，该设备连接了一个或多个主机物理 NIC。客户机 VM 将创建一个名为 vnetN 的关联 tun 设备，也可以使用 <target> 元素覆盖（请参阅 [覆盖目标元素](https://www.libvirt.org/formatdomain.html#overriding-the-target-element)）。tun 设备将连接到桥接。IP 范围/网络配置是 LAN 上使用的任何配置。这为客户机 VM 提供了与物理机器相同的完整传入和传出网络访问。

在 Linux 系统上，桥接设备通常是标准的 Linux 主机桥接。在支持 Open vSwitch 的主机上，也可以通过向接口定义添加 <virtualport type='openvswitch'/> 来连接到 Open vSwitch 桥接设备。（自 0.9.11 起）。Open vSwitch 类型的 virtualport 在其 <parameters> 元素中接受两个参数 - interfaceid 是用于唯一标识此特定接口到 Open vSwitch 的标准 uuid（如果不指定，首次定义接口时将为您生成随机 interfaceid），以及可选的 profileid，它作为接口的 "port-profile" 发送到 Open vSwitch。

```
...
<devices>
  ...
  <interface type='bridge'>
    <source bridge='br0'/>
  </interface>
  <interface type='bridge'>
    <source bridge='br1'/>
    <target dev='vnet7'/>
    <mac address="00:11:22:33:44:55"/>
  </interface>
  <interface type='bridge'>
    <source bridge='ovsbr'/>
    <virtualport type='openvswitch'>
      <parameters profileid='menial' interfaceid='09b11c53-8b5c-4eeb-8f00-d84eaa0aaa4f'/>
    </virtualport>
  </interface>
  ...
</devices>
...
```

在支持内核侧 Open vSwitch 并配置了 Midonet Host Agent 的主机上，也可以通过向接口定义添加 <virtualport type='midonet'/> 来连接到 'midonet' 桥接设备。（自 1.2.13 起）。Midonet virtualport 类型在其 <parameters> 元素中需要一个 interfaceid 属性。此接口 ID 是 UUID，指定虚拟网络拓扑中的哪个端口将绑定到接口。

```
...
<devices>
  ...
  <interface type='bridge'>
    <source bridge='br0'/>
  </interface>
  <interface type='bridge'>
    <source bridge='br1'/>
    <target dev='vnet7'/>
    <mac address="00:11:22:33:44:55"/>
  </interface>
  <interface type='bridge'>
    <source bridge='midonet'/>
    <virtualport type='midonet'>
      <parameters interfaceid='0b2d64da-3d0e-431e-afdd-804415d6ebbb'/>
    </virtualport>
  </interface>
  ...
</devices>
...
```

#### 21.11.3 [使用 SLIRP 的用户空间连接](https://www.libvirt.org/formatdomain.html#id45)

用户接口类型通过透明的用户空间代理将客户机接口连接到外部，该代理不需要任何特殊的系统权限，使其可用于 libvirt 本身以无权限运行的情况（例如，libvirt 的"会话模式"守护程序，或 libvirt 在无权限容器内运行时）。

默认情况下，此用户代理通过 QEMU 的 SLIRP 驱动程序完成，这是 QEMU 内置的用户空间代理，具有 DHCP 和 DNS 服务，为客户机提供 10.0.2.15 的 IP 地址、10.0.2.2 的默认路由和 10.0.2.3 的 DNS 服务器。

自 3.8.0 起，可以通过包含一个 ip 元素来覆盖客户机的默认网络地址，该元素在其一个强制属性 address 中指定 IPv4 地址。可选地，可以指定第二个 ip 元素，其 family 属性设置为 "ipv6"，以向接口添加 IPv6 地址。address. 可选地，可以指定地址前缀。

```
...
<devices>
  <interface type='user'/>
  ...
  <interface type='user'>
    <mac address="00:11:22:33:44:55"/>
    <ip family='ipv4' address='172.17.1.1' prefix='16'/>
    <ip family='ipv6' address='2001:db8:ac10:fd01::1' prefix='64'/>
  </interface>
</devices>
...
```

这些设置令人惊讶地**不是**被 SLIRP 用于设置确切的 IP 地址；相反，它们用于确定客户机的 IP 地址应该在哪个**网络/子网**上，客户机将在该子网中获得一个地址，但地址的主机部分仍将是 "10.0.2.15" 的主机部分（基于配置的前缀（如果未指定前缀，则为 24））。提供给客户机的 DNS 和默认网关地址也将类似地基于配置提供的 <ip> 的网络部分，结合 SLIRP 默认设置的 DNS/网关的主机部分（10.0.2.3/10.0.2.2）。为了帮助解决前面句子的混淆，下表显示了为 libvirt 的 <interface type='user'> 配置中 <ip> 元素地址和前缀的各种设置，将通过 DHCP 响应提供给客户机以用于其接口配置（ip/前缀、DNS、默认网关）的设置示例：

| libvirt <ip> 元素                | 客户机 ip/前缀 | 客户机 DNS | 客户机默认网关 |
| -------------------------------- | -------------- | ---------- | -------------- |
| (未指定)                         | 10.0.2.15/24   | 10.0.2.3   | 10.0.2.2       |
| address='172.17.1.1' prefix='16' | 172.17.2.15/16 | 172.17.2.3 | 172.17.2.2     |
| address='172.17.1.1' prefix='24' | 172.17.1.15/24 | 172.17.1.3 | 172.17.1.2     |
| address='172.17.1.1' prefix='8'  | 172.0.2.15/16  | 172.0.2.3  | 172.0.2.2      |
| address='172.17.1.1' prefix='23' | 172.17.0.15/23 | 172.17.0.3 | 172.17.0.2     |

#### 21.11.4 [使用 passt 的用户空间连接](https://www.libvirt.org/formatdomain.html#id46)

自 9.0.0 起（仅 QEMU 和 KVM），可以通过将接口的 <backend> 子元素 type 属性设置为 passt 来选择用户接口类型的替代后端实现。在这种情况下，使用 passt 传输 [(详细信息在此)](https://passt.top)。passt 作为与 QEMU 分开的进程运行 - passt 进程处理将网络流量来回转发到物理网络的详细信息（使用用户空间代理和单独的网络命名空间来提供传出的 UDP/TCP/ICMP 会话，并可选地将发往主机的传入流量重定向到客户机），并且 passt 和 QEMU 之间的套接字将该流量转发到客户机（当然也返回）。

自 11.1.0 起（仅 QEMU 和 KVM），你可能更喜欢使用 type='vhostuser' 而不是 type='user' 的 passt 后端。下面关于 passt 的所有选项也适用于使用 type='vhostuser' 的 passt 后端；有关 vhostuser 的其他详细信息在此 [此处](https://www.libvirt.org/formatdomain.html#vhost-user-connection-with-passt-backend) 描述。

与 SLIRP 类似，passt 有一个内部 DHCP 服务器，为请求的客户机提供一个 ipv4 和一个 ipv6 地址。这些都有默认值，或者你可以使用 <ip> 元素（如上所述，具有如下所述的行为差异）来配置 passt 的 DHCP 服务器可以提供给客户机的一个 IPv4 和一个 IPv6 地址。

与 SLIRP 不同，当未指定 <ip> 地址时，passt 默认会为客户机提供与主机本身相同的 IP 地址、DNS 服务器等（通过代理和单独的网络命名空间的魔力，这不会产生任何冲突）。

也与 SLIRP 的行为不同：如果你确实指定了 IP 地址，将向客户机提供你指定的确切地址和网络掩码/前缀（即 passt 不像 SLIRP 那样将 <ip> 设置解释为网络地址，而是将其解释为主机地址）。在上面给出的示例表中，客户机 IP 将在所有情况下都被设置为确切的 172.17.1.1（DNS 和默认网关将设置为与主机上的相同）。

不过，一旦来自客户机的流量离开主机前往网络的其余部分，它将始终看起来像是来自主机的 IP。

passt 后端有一些其他可配置的选项。例如，<backend> 子元素的 logFile 属性可用于告诉此接口的 passt 进程在哪里写入其消息日志（自 9.0.0 起）[]，而 hostname 属性用于在 DHCPv4 响应中设置发送给客户机的主机名（使用选项 12）（自 11.8.0 起），fqdn 设置在 DHCPv4 响应选项 81 和 DHCPv6 响应选项 39 中发送给客户机的"完全限定域名"（自 11.8.0 起）。此外，<source> 子元素属性 dev 可以告诉 passt 用于导出上游流量路由的特定主机接口。

[] _由于 passt 的设计决策，在主机上使用 SELinux 时，建议日志文件位于运行 passt 进程的用户的运行时目录中，很可能是_ _`/run/user/$UID`_ _（其中_ _`$UID`_ _是该用户的 UID），例如_ _`/run/user/1000`_ _。请注意，libvirt 不会创建此目录（如果它不存在），以避免可能的、尽管不太可能的孤立目录或权限等问题。logfile 属性主要用于调试，因此在正常情况下不应设置。_

此外，当使用 passt 时，可以添加多个 <portForward> 元素来将主机的传入网络流量转发到此客户机接口。每个 <portForward> 必须有一个 proto 属性（设置为 tcp 或 udp）、可选的原始地址（如果未指定，则给定 proto/port(s) 的所有传入会话到任何主机 IP 将被转发到客户机），以及可选的 dev 属性以将转发流量限制到特定的主机接口。

转发哪些端口的决定由 <portForward> 的零个或多个 <range> 子元素描述（如果没有 <range>，则**所有**给定 proto/address 的端口将被转发）。每个 <range> 有一个 start 和可选的 end 属性。如果省略 end，则将转发单个端口，否则将转发 start 和 end 之间（包括）的所有端口。如果会话转发时端口号应保持不变，则不需要进一步的选项，但如果客户机期望会话在不同端口上，则应通过 <range> 的 to 属性指定 - 范围内每个转发会话的端口号将偏移 "to - start"。<range> 元素也可用于指定**不应**转发的端口范围。这是通过将 range 的 exclude 属性设置为 yes 来完成的。这可能看起来不是很有用，但当希望转发长端口范围**除了**某些子集时，它会很有用。

```
...
<devices>
  ...
  <interface type='user'>
    <backend type='passt' hostname='bob' logFile='/run/user/$UID/passt-domain.log'/>
    <mac address="00:11:22:33:44:55"/>
    <source dev='eth0'/>
    <ip family='ipv4' address='172.17.5.4' prefix='24'/>
    <ip family='ipv6' address='2001:db8:ac10:fd01::20'/>
    <portForward proto='tcp'>
      <range start='2022' to='22'/>
    </portForward>
    <portForward proto='udp' address='1.2.3.4'>
      <range start='5000' end='5020' to='6000'/>
      <range start='5010' end='5015' exclude='yes'/>
    </portForward>
    <portForward proto='tcp' address='2001:db8:ac10:fd01::1:10' dev='eth0'>
      <range start='80'/>
      <range start='443' to='344'/>
    </portForward>
  </interface>
</devices>
...
```

#### 21.11.5 [通用以太网连接](https://www.libvirt.org/formatdomain.html#id47)

提供一种方法来使用部分或完全在 libvirt 外部设置的新的或现有的 tap 设备（或 veth 设备对，取决于 hypervisor 驱动程序的需要）（在客户机启动之前，或在通过配置中指定的可选脚本启动客户机期间）。

tap 设备的名称可以通过 <target> 元素的 dev 属性可选地指定。如果未指定目标 dev，libvirt 将创建一个名称为 "vnetN" 模式的新标准 tap 设备，其中 "N" 替换为数字。如果指定了目标 dev 并且该设备不存在，则将创建一个具有确切 dev 名称的新标准 tap 设备。如果指定的目标 dev 确实存在，则将使用该现有设备。通常，libvirt 会对设备进行一些基本设置，包括设置 MAC 地址和 IFF_UP 标志，但如果 dev 是预先存在的设备，并且 target 元素的 managed 属性也设置为 "no"（默认值为 "yes"），则甚至不会执行此基本设置 - libvirt 会简单地将设备传递给 hypervisor，不进行任何设置。自 5.7.0 起 使用 managed='no' 和预创建的 tap 设备很有用，因为它允许由无权限的 libvirtd 管理的虚拟机基于 tap 设备具有模拟的网络设备。

创建/打开 tap 设备后，将运行一个可选的 shell 脚本（在 <script> 元素的 path 属性中给出）。自 0.2.1 起 此外，在分离/关闭 tap 设备后，将运行一个可选的 shell 脚本（在 <downscript> 元素的 path 属性中给出）。自 6.4.0 起 这些可用于执行任何必要的主机网络集成。

```
...
<devices>
  <interface type='ethernet'>
    <script path='/etc/qemu-ifup-mynet'/>
    <downscript path='/etc/qemu-ifdown-mynet'/>
  </interface>
  ...
  <interface type='ethernet'>
    <target dev='mytap1' managed='no'/>
    <model type='virtio'/>
  </interface>
</devices>
...
```

#### 21.11.6 [直接附加到物理接口](https://www.libvirt.org/formatdomain.html#id48)

提供虚拟机的 NIC 直接附加到主机的给定物理接口。自 0.7.7 起（仅 QEMU 和 KVM）

此设置需要 Linux macvtap 驱动程序（在 2.6.34 中引入）可用。可以为 macvtap 设备的操作模式选择 'vepa'（['虚拟以太网端口聚合器'](https://www.ieee802.org/1/files/public/docs2009/new-evb-congdon-vepa-modular-0709-v01.pdf)）、'bridge' 或 'private' 之一，'vepa' 是默认模式。各个模式导致数据包传递的行为如下：

如果模型类型设置为 virtio 并且接口的 trustGuestRxFilters 属性设置为 yes，则客户机中对接口 mac 地址、单播/多播接收过滤器和 vlan 设置的更改将被监控并传播到主机上关联的 macvtap 设备（自 1.2.10 起）。如果未设置 trustGuestRxFilters，或者对于使用的设备模型不支持，则来自客户机侧的 mac 地址更改尝试将导致网络连接不工作。

- vepa

  所有 VM 的数据包都发送到外部桥接器。目标是与数据包来源同一主机上的 VM 的数据包由 VEPA 功能的桥接器发送回主机（今天的桥接器通常不支持 VEPA）。

- bridge

  目标在与来源同一主机上的数据包直接传递到目标 macvtap 设备。源设备和目标设备都需要处于 bridge 模式才能直接传递。如果其中一个处于 vepa 模式，则需要支持 VEPA 的桥接器。

- private

  所有数据包都发送到外部桥接器，只有通过外部路由器或网关发送并由该设备发送回主机时，才会传递到同一主机上的目标 VM。如果源设备或目标设备处于 private 模式，则遵循此过程。

- passthrough

  此功能将 SRIOV 功能 NIC 的虚拟功能直接附加到 VM，而不会失去迁移能力。所有数据包都发送到配置的网络设备的 VF/IF。根据设备的能力，可能需要额外的先决条件或限制；例如，在 Linux 上，这需要 2.6.38 或更新的内核。自 0.9.2 起

```
...
<devices>
  ...
  <interface type='direct' trustGuestRxFilters='no'>
    <source dev='eth0' mode='vepa'/>
  </interface>
</devices>
...
```

直接附加的虚拟机的网络访问可以由主机机器的物理接口连接到的硬件交换机管理。

如果交换机符合 IEEE 802.1Qbg 标准，则接口可以具有如下所示的附加参数。virtualport 元素的参数在 IEEE 802.1Qbg 标准中有更详细的文档。这些值是网络特定的，应由网络管理员提供。在 802.1Qbg 术语中，虚拟站接口 (VSI) 表示虚拟机的虚拟接口。自 0.8.2 起

请注意，IEEE 802.1Qbg 要求 VLAN ID 为非零值。

- managerid

  VSI 管理器 ID 标识包含 VSI 类型和实例定义的数据库。这是一个整数值，值 0 保留。

- typeid

  VSI 类型 ID 标识表征网络访问的 VSI 类型。VSI 类型通常由网络管理员管理。这是一个整数值。

- typeidversion

  VSI 类型版本允许多个版本的 VSI 类型。这是一个整数值。

- instanceid

  VSI 实例 ID 标识符在创建 VSI 实例（即虚拟机的虚拟接口）时生成。这是一个全局唯一标识符。

```
...
<devices>
  ...
  <interface type='direct'>
    <source dev='eth0.2' mode='vepa'/>
    <virtualport type="802.1Qbg">
      <parameters managerid="11" typeid="1193047" typeidversion="2" instanceid="09b11c53-8b5c-4eeb-8f00-d84eaa0aaa4f"/>
    </virtualport>
  </interface>
</devices>
...
```

如果交换机符合 IEEE 802.1Qbh 标准，则接口可以具有如下所示的附加参数。这些值是网络特定的，应由网络管理员提供。自 0.8.2 起

- profileid

  配置文件 ID 包含要应用于此接口的端口配置文件的名称。此名称由端口配置文件数据库解析为端口配置文件中的网络参数，这些网络参数将应用于此接口。

```
...
<devices>
  ...
  <interface type='direct'>
    <source dev='eth0' mode='private'/>
    <virtualport type='802.1Qbh'>
      <parameters profileid='finance'/>
    </virtualport>
  </interface>
</devices>
...
```

#### 21.11.7 [PCI 透传](https://www.libvirt.org/formatdomain.html#id49)

PCI 网络设备（由 <source> 元素指定）使用通用设备透传直接分配给客户机，首先可选地将设备的 MAC 地址设置为配置的值，并使用可选指定的 <virtualport> 元素（请参阅上面针对 type='direct' 网络设备给出的 virtualport 示例）将设备与 802.1Qbh 兼容交换机相关联。请注意 - 由于标准单端口 PCI 以太网卡驱动程序设计的限制 - 只有 SR-IOV（单根 I/O 虚拟化）虚拟功能 (VF) 设备可以以这种方式分配；要将标准单端口 PCI 或 PCIe 以太网卡分配给客户机，请使用传统的 <hostdev> 设备定义，并且自 0.9.11 起

要使用 VFIO 设备分配而不是传统/ legacy KVM 设备分配（VFIO 是一种与 UEFI Secure Boot 兼容的新设备分配方法），type='hostdev' 接口可以有一个可选的 driver 子元素，其 name 属性设置为 "vfio"。要使用 legacy KVM 设备分配，您可以将 name 设置为 "kvm"（默认值在 VFIO 驱动程序可用的系统上为 "vfio"，在较旧的系统上为 "kvm"。自 1.1.3 起（在此之前，默认值始终为 "kvm"））。

请注意，网络设备的这种"智能透传"与标准 <hostdev> 设备的功能非常相似，区别在于此方法允许为透传的设备指定 MAC 地址和 <virtualport>。如果不需要这些功能，如果您有不支持 SR-IOV 的标准单端口 PCI、PCIe 或 USB 网卡（因此在分配给客户机域后重置期间无论如何都会丢失配置的 MAC 地址），或者如果您使用的 libvirt 版本早于 0.9.11，则应使用标准 <hostdev> 将设备分配给客户机，而不是 <interface type='hostdev'/>。

与标准 <hostdev> 设备的功能类似，当 managed 为 "yes" 时，它在传递给客户机之前从主机分离，并在客户机退出后重新连接到主机。如果 managed 省略或为 "no"，用户负责在启动客户机或热插拔设备之前调用 virNodeDeviceDettach（或 virsh nodedev-detach），并在热卸载或停止客户机后调用 virNodeDeviceReAttach（或 virsh nodedev-reattach）。

```
...
<devices>
  <interface type='hostdev' managed='yes'>
    <source>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x07' function='0x0'/>
    </source>
    <mac address='52:54:00:6d:90:02'/>
    <virtualport type='802.1Qbh'>
      <parameters profileid='finance'/>
    </virtualport>
  </interface>
</devices>
...
```

#### 21.11.8 [vDPA 设备](https://www.libvirt.org/formatdomain.html#id50)

vDPA 网络设备可用于在域内提供线速网络性能。vDPA 设备是一种专门的网络设备类型，使用符合 virtio 规范的数据路径，但具有特定于供应商的控制路径。要在 libvirt 中使用此类设备，主机设备必须已经绑定到适当的设备特定 vDPA 驱动程序。这会创建一个 vDPA 字符设备（例如 /dev/vhost-vdpa-0），可用于将设备分配给 libvirt 域。自 6.9.0 起（仅 QEMU，需要 QEMU 5.1.0 或更新版本）

```
...
<devices>
  <interface type='vdpa'>
    <source dev='/dev/vhost-vdpa-0'/>
  </interface>
</devices>
...
```

#### 21.11.9 [组合 virtio/hostdev NIC 对](https://www.libvirt.org/formatdomain.html#id51)

自 6.1.0 起（仅 QEMU 和 KVM），两个接口的 <teaming> 元素可用于将它们作为客户机中的 team/bond 设备连接。这需要支持"故障转移"功能的客户机 virtio-net 驱动程序，例如 Linux 4.18 中包含的驱动程序。

```
...
<devices>
  <interface type='network'>
    <source network='mybridge'/>
    <mac address='00:11:22:33:44:55'/>
    <model type='virtio'/>
    <teaming type='persistent'/>
    <alias name='ua-backup0'/>
  </interface>
  <interface type='network'>
    <source network='hostdev-pool'/>
    <mac address='00:11:22:33:44:55'/>
    <model type='virtio'/>
    <teaming type='transient' persistent='ua-backup0'/>
  </interface>
</devices>
...
```

此示例中的第二个接口引用的是 SRIOV VF 池的网络（即"hostdev 网络"）。您也可以直接引用 SRIOV VF 设备：

```
...
  <interface type='hostdev'>
    <source>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x07' function='0x0'/>
    </source>
    <mac address='00:11:22:33:44:55'/>
    <teaming type='transient' persistent='ua-backup0'/>
  </interface>
...
```

<teaming> 元素的必需属性 type 将设置为 persistent 以指示应始终存在于域中的设备，或 transient 以指示可能定期移除，然后稍后重新添加到域的设备。当 type="transient" 时，<teaming> 应该有第二个属性称为 persistent - 此属性应设置为对中的另一个设备的别名名称（具有 <teaming type="persistent'/> 的那个）。

在 QEMU 的特定情况下，libvirt 的 <teaming> 元素用于设置 virtio-net "故障转移"设备对。对于此设置，persistent 设备必须是具有 <model type="virtio"/> 的接口，而 transient 设备必须是 <interface type='hostdev'/>（或 <interface type='network'/>，其中引用的网络定义了 SRIOV VF 池）。客户机然后将有一个由 virtio NIC + hostdev NIC 对组成的简单网络 team/bond 设备。在此配置中，性能更高的 hostdev NIC 通常会优先用于所有网络流量，但当域迁移时，QEMU 将自动从客户机中拔出 VF，然后在迁移完成后热插拔类似设备；在迁移过程中，网络流量将使用 virtio NIC。（当然，为了让绑定正常工作，模拟的 virtio NIC 和 hostdev NIC 必须连接到同一个子网）。

自 7.1.0 起，<teaming> 元素也可以添加到普通的 <hostdev> 设备。

```
...
  <hostdev mode='subsystem' type='pci' managed='no'>
    <source>
      <address domain='0x0000' bus='0x00' slot='0x07' function='0x0'/>
    </source>
    <teaming type='transient' persistent='ua-backup0'/>
  </hostdev>
...
```

此设备必须是网络设备，但不一定是 SRIOV VF。使用普通 <hostdev> 而不是 <interface type='hostdev'> 或 <interface type='network'> 很有用，如果将使用 VFIO 分配的设备是标准 NIC（不是 VF），或者如果 libvirt 没有必要的资源和权限来设置 VF 的 MAC 地址（例如，如果 libvirt 以无权限方式运行，或在容器中运行）。这当然意味着用户（或另一个应用程序）负责以一种在客户机驱动程序初始化时能够保留的方式设置设备的 MAC 地址。对于标准 NIC（即不是 SRIOV VF），这可能意味着需要将 NIC 的工厂编程的 MAC 地址用于组合对（因为客户机中的任何驱动程序初始化都会将 MAC 重置回工厂设置）。如果是 SRIOV VF，则需要通过 VF 的 PF 设置其 MAC 地址，例如，如果您要使用 PF enp2s0f1 的 VF 2，您将使用如下命令：

```
ip link set enp2s0f1 vf 2 mac 52:54:00:11:22:33
```

注意 1：由于在配置 hostdev NIC 时必须知道 virtio NIC 的别名名称，因此需要在 virtio NIC 的配置中手动设置它（与所有其他手动设置的别名名称一样，这意味着它必须以 "ua-" 开头）。

注意 2：目前，支持 virtio-net 故障转移的客户机 OS virtio-net 驱动程序的唯一实现要求 virtio 和 hostdev NIC 的 MAC 地址必须匹配。由于将来可能并不总是需要这一点，libvirt 不会强制执行此限制 - 由创建配置的人员/管理应用程序确保两个设备的 MAC 地址匹配。

注意 3：由于作为迁移源和目标的主机上的 SRIOV VF 的 PCI 地址几乎肯定不同，因此要么更高级别的管理软件需要在迁移开始时修改 hostdev NIC (<interface type='hostdev'>) 的 <source>，要么（更简单的解决方案）配置需要使用维护此类设备池的 libvirt "hostdev" 虚拟网络，如示例中使用名为 "hostdev-pool" 的 libvirt 网络所暗示的那样 - 只要两个主机上的 hostdev 网络池具有相同的名称，libvirt 本身将负责在迁移的两端分配适当的设备。同样，virtio 接口的 XML 也必须在迁移的源和目标上不加修改地正确工作（例如，通过连接到两个主机上的相同桥接设备，或使用相同的虚拟网络），或者管理软件必须在迁移期间正确修改接口 XML，以便 virtio 设备在迁移前后保持连接到相同的网络段。

#### 21.11.10 [多播隧道](https://www.libvirt.org/formatdomain.html#id52)

设置多播组以表示虚拟网络。网络设备位于同一多播组中的任何 VM 都可以相互通信，甚至跨主机。此模式也适用于无权限用户。没有默认的 DNS 或 DHCP 支持，也没有出站网络访问。要提供出站网络访问，其中一个 VM 应该有第二个 NIC，连接到前 4 种网络类型之一，并进行适当的路由。多播协议与用户模式 Linux 客户机使用的协议兼容。使用的源地址必须来自多播地址块。

```
...
<devices>
  <interface type='mcast'>
    <mac address='52:54:00:6d:90:01'/>
    <source address='230.0.0.1' port='5558'/>
  </interface>
</devices>
...
```

#### 21.11.11 [TCP 隧道](https://www.libvirt.org/formatdomain.html#id53)

TCP 客户端/服务器架构提供虚拟网络。一个 VM 提供网络的服务器端，所有其他 VM 配置为客户端。所有网络流量通过服务器在 VM 之间路由。此模式也适用于无权限用户。没有默认的 DNS 或 DHCP 支持，也没有出站网络访问。要提供出站网络访问，其中一个 VM 应该有第二个 NIC，连接到前 4 种网络类型之一，并进行适当的路由。

```
...
<devices>
  <interface type='server'>
    <mac address='52:54:00:22:c9:42'/>
    <source address='192.168.0.1' port='5558'/>
  </interface>
  ...
  <interface type='client'>
    <mac address='52:54:00:8b:c9:51'/>
    <source address='192.168.0.1' port='5558'/>
  </interface>
</devices>
...
```

#### 21.11.12 [UDP 单播隧道](https://www.libvirt.org/formatdomain.html#id54)

UDP 单播架构提供虚拟网络，使用 QEMU 的 UDP 基础设施实现 QEMU 实例之间的连接。xml "source" 地址是从运行 QEMU 的主机发送 UDP 套接字数据包的端点地址。xml "local" 地址是 QEMU 主机发送 UDP 套接字数据包的接口地址。自 1.2.20 起

```
...
<devices>
  <interface type='udp'>
    <mac address='52:54:00:22:c9:42'/>
    <source address='127.0.0.1' port='11115'>
      <local address='127.0.0.1' port='11116'/>
    </source>
  </interface>
</devices>
...
```

#### 21.11.13 [空网络接口](https://www.libvirt.org/formatdomain.html#id55)

未连接的网络接口听起来很没用，但例如在 VMWare 中可能会出现，没有指定要连接的网络。自 8.7.0 起

```
...
<devices>
  <interface type='null'>
    <mac address='52:54:00:22:c9:42'/>
  </interface>
</devices>
...
```

#### 21.11.14 [VMWare 分布式交换机](https://www.libvirt.org/formatdomain.html#id56)

接口可以连接到 VMWare 分布式交换机，但由于 libvirt 无法提供有关该架构的信息，此处提供的信息仅能从 VM 配置中收集。可以创建具有此接口类型的 VM，以便 XML 编辑正常工作，但是 libvirt 不能保证这些参数中的任何更改在 hypervisor 中都是有效的。自 8.7.0 起

```
...
<devices>
  <interface type='vds'>
    <mac address='52:54:00:22:c9:42'/>
    <source switchid='12345678-1234-1234-1234-123456789abc' portid='6' portgroupid='pg-4321' connectionid='12345'/>
  </interface>
</devices>
...
```

#### 21.11.15 [设置 NIC 模型](https://www.libvirt.org/formatdomain.html#id57)

```
...
<devices>
  <interface type='network'>
    <source network='default'/>
    <target dev='vnet1'/>
    <model type='ne2k_pci'/>
  </interface>
</devices>
...
```

对于支持此功能的 hypervisor，您可以通过 model 元素设置模拟网络接口卡的模型。

虽然 libvirt 接受任何值作为类型并将其传递给 hypervisor 以保持兼容性，但如今大多数设备都有额外的处理和地址分配，如果模型不为 libvirt 所知，可能无法正常工作。

Libvirt 原生支持以下网络设备模型：virtio、virtio-transitional（自 5.2.0 起）、virtio-non-transitional（自 5.2.0 起）、e1000、e1000e、igb（自 9.3.0 起）、rtl8139、netfront、usb-net（自 10.3.0 起）、spapr-vlan、lan9118、scm91c111、vlance、vmxnet、vmxnet2、vmxnet3、Am79C970A、Am79C973、82540EM、82545EM、82543GC。

对于 QEMU，您可以使用以下命令获取支持的模型列表：

```
qemu-system-x86_64 -net nic,model=?
```

#### 21.11.16 [设置 NIC 驱动特定选项](https://www.libvirt.org/formatdomain.html#id58)

```
...
<devices>
  <interface type='network'>
    <source network='default'/>
    <target dev='vnet1'/>
    <model type='virtio'/>
    <driver name='vhost' txmode='iothread' ioeventfd='on' event_idx='off' queues='5' rx_queue_size='256' tx_queue_size='256'>
      <host csum='off' gso='off' tso4='off' tso6='off' ecn='off' ufo='off' mrg_rxbuf='off'/>
      <guest csum='off' tso4='off' tso6='off' ecn='off' ufo='off'/>
    </driver>
  </interface>
</devices>
...
```

某些 NIC 可能具有可调的驱动特定选项。这些设置为接口定义的 driver 子元素的属性。目前，virtio NIC 驱动程序可用以下属性：

- name

  可选的 name 属性强制使用哪种类型的后端驱动程序。值可以是 'qemu'（用户空间后端）或 'vhost'（内核后端，需要内核提供 vhost 模块）；尝试在没有内核支持的情况下要求 vhost 驱动程序将被拒绝。如果不存在此属性，则域默认为 'vhost'（如果存在），但会无错误地静默回退到 'qemu'。自 0.8.8 起（仅 QEMU 和 KVM）对于 type='hostdev' 接口（PCI 透传设备），name 属性可以可选地设置为 "vfio" 或 "kvm"。"vfio" 告诉 libvirt 使用 VFIO 设备分配而不是传统的 KVM 设备分配（VFIO 是一种与 UEFI Secure Boot 兼容的新设备分配方法），"kvm" 告诉 libvirt 使用由 kvm 内核模块直接执行的传统设备分配（默认值当前为 "kvm"，但可能会更改）。自 1.0.5 起（仅 QEMU 和 KVM，需要内核 3.6 或更新版本）对于 type='vhostuser' 接口，name 属性被忽略。使用的后端驱动程序始终是 vhost-user。

- txmode

  txmode 属性指定当传输缓冲区已满时如何处理数据包传输。值可以是 'iothread' 或 'timer'。自 0.8.8 起（仅 QEMU 和 KVM）如果设置为 'iothread'，数据包 tx 全部在驱动程序下半部分的 iothread 中完成（此选项转化为在 qemu 命令行 -device virtio-net-pci 选项中添加 "tx=bh"）。如果设置为 'timer'，tx 工作在 qemu 中完成，如果当前有更多 tx 数据无法发送，则在 qemu 继续做其他事情之前设置一个计时器；当计时器触发时，再次尝试发送更多数据。根据添加此选项的 qemu 开发人员的说法，结果差异是："bh 使 tx 更加异步并减少延迟，但可能导致更多的处理器带宽争用，因为执行 tx 的 CPU 不一定是客户机生成数据包的 CPU。" **一般情况下，您应该保持此选项不变，除非您非常确定自己在做什么。**

- ioeventfd

  此可选属性允许用户为接口设备设置 [域 I/O 异步处理](https://patchwork.kernel.org/patch/43390/)。默认值由 hypervisor 决定。接受的值为 "on" 和 "off"。启用此功能允许 qemu 在单独的线程处理 I/O 时执行 VM。通常，在 I/O 期间经历高系统 CPU 利用率的客户机将受益于此。另一方面，在过载的主机上，它可能会增加客户机 I/O 延迟。自 0.9.3 起（仅 QEMU 和 KVM）**一般情况下，您应该保持此选项不变，除非您非常确定自己在做什么。**

- event_idx

  event_idx 属性控制设备事件处理的某些方面。值可以是 'on' 或 'off' - 如果为 on，它将减少客户机的中断和退出次数。默认值由 QEMU 确定；通常，如果支持该功能，默认值为 on。如果存在这种行为不理想的情况，此属性提供了一种强制关闭该功能的方法。自 0.9.5 起（仅 QEMU 和 KVM）**一般情况下，您应该保持此选项不变，除非您非常确定自己在做什么。**

- queues

  可选的 queues 属性控制用于 [多队列 virtio-net](https://www.linux-kvm.org/page/Multiqueue) 或 vhost-user（请参阅 [vhost-user 连接](https://www.libvirt.org/formatdomain.html#vhost-user-connection)）网络接口的队列数。使用多个数据包处理队列需要接口具有 <model type='virtio'/> 元素。每个队列可能由不同的处理器处理，从而产生更高的吞吐量。virtio-net 自 1.0.6 起（仅 QEMU 和 KVM）vhost-user 自 1.2.17 起（仅 QEMU 和 KVM）

- rx_queue_size

  可选的 rx_queue_size 属性控制如上所述的每个队列的 virtio 环的大小。默认值取决于 hypervisor，可能会在其版本之间变化。此外，一些 hypervisor 可能对实际值施加一些限制。例如，最新的 QEMU（截至 2016-09-01）要求值是 [256, 1024] 范围内的 2 的幂。自 2.3.0 起（仅 QEMU 和 KVM）**一般情况下，您应该保持此选项不变，除非您非常确定自己在做什么。**

- tx_queue_size

  可选的 tx_queue_size 属性控制如上所述的每个队列的 virtio 环的大小。默认值取决于 hypervisor，可能会在其版本之间变化。此外，一些 hypervisor 可能对实际值施加一些限制。例如，QEMU v2.9 要求值是 [256, 1024] 范围内的 2 的幂。此外，这可能仅适用于接口类型的子集，例如上述 QEMU 仅为 vhostuser 类型启用此选项。自 3.7.0 起（仅 QEMU 和 KVM）**一般情况下，您应该保持此选项不变，除非您非常确定自己在做什么。**

- rss

  rss 选项为 virtio NIC 启用 in-qemu/ebpf RSS。RSS 仅适用于 virtio 和 tap 后端。Virtio NIC 将以 "rss" 属性启动。目前，libvirt 支持 "in-qemu" RSS。如果 QEMU 具有 CAP_SYS_ADMIN 权限，它可能会加载 eBPF RSS，这在 libvirt 中默认不支持。自 8.3.0 和 QEMU 5.1 **一般情况下，您应该保持此选项不变，除非您非常确定自己在做什么。正确的 RSS 配置取决于 vcpu、tap 和 vhost 设置。**

- rss_hash_report

  rss_hash_report 选项为 virtio NIC 启用 in-qemu RSS 哈希报告。Virtio NIC 将以 "hash" 属性启动。提供给 VM 的网络数据包将在 virt 标头中包含数据包的哈希。通常与 rss 一起启用。没有 rss 选项，哈希报告本身不会影响转向，但会提供带有计算哈希的 vnet 标头。自 8.3.0 和 QEMU 5.1 **一般情况下，您应该保持此选项不变，除非您非常确定自己在做什么。正确的 RSS 配置取决于 vcpu、tap 和 vhost 设置。**

- virtio 选项

  对于 virtio 接口，也可以设置 [Virtio 相关选项](https://www.libvirt.org/formatdomain.html#virtio-related-options)。（自 3.5.0 起）

主机和客户机的卸载选项可以使用以下子元素配置：

- host

  csum、gso、tso4、tso6、ecn 和 ufo 属性，可能的值为 on 和 off，可用于关闭主机卸载选项。默认情况下，支持的卸载由 QEMU 启用。自 1.2.9 起（仅 QEMU）mrg_rxbuf 属性可用于控制主机端的可合并 rx 缓冲区。可能的值为 on（默认）和 off。自 1.2.13 起（仅 QEMU）

- guest

  csum、tso4、tso6、ecn 和 ufo 属性，可能的值为 on 和 off，可用于关闭客户机卸载选项。默认情况下，支持的卸载由 QEMU 启用。自 1.2.9 起（仅 QEMU）

#### 21.11.17 [设置网络后端特定选项](https://www.libvirt.org/formatdomain.html#id59)

```
...
<devices>
  <interface type='network'>
    <source network='default'/>
    <target dev='vnet1'/>
    <model type='virtio'/>
    <backend tap='/dev/net/tun' vhost='/dev/vhost-net'/>
    <driver name='vhost' txmode='iothread' ioeventfd='on' event_idx='off' queues='5'/>
    <tune>
      <sndbuf>1600</sndbuf>
    </tune>
  </interface>
</devices>
...
```

为了调优网络后端，可以使用 backend 元素。vhost 属性可以覆盖 virtio 模型设备的默认 vhost 设备路径 (/dev/vhost-net)。tap 属性覆盖网络和桥接接口的 tun/tap 设备路径（默认：/dev/net/tun）。这在会话模式下不起作用。自 1.2.9 起

对于 tap 设备，还有 sndbuf 元素，可以调整主机中发送缓冲区的大小。自 0.8.8 起

#### 21.11.18 [覆盖目标元素](https://www.libvirt.org/formatdomain.html#id60)

```
...
<devices>
  <interface type='network'>
    <source network='default'/>
    <target dev='vnet1'/>
  </interface>
</devices>
...
```

如果未指定目标，某些 hypervisor 将自动为创建的 tun 设备生成名称。此名称可以手动指定，但是名称 **不应以 'vnet'、'vif'、'macvtap' 或 'macvlan' 开头**，这些是 libvirt 和某些 hypervisor 保留的前缀。使用这些前缀的手动指定目标可能会被忽略。

请注意，对于 LXC 容器，这定义了主机端接口的名称。自 1.2.7 起，要定义客户机端设备的名称，应使用 guest 元素，如下所示：

```
...
<devices>
  <interface type='network'>
    <source network='default'/>
    <guest dev='myeth'/>
  </interface>
</devices>
...
```

#### 21.11.19 [指定引导顺序](https://www.libvirt.org/formatdomain.html#id61)

```
...
<devices>
  <interface type='network'>
    <source network='default'/>
    <target dev='vnet1'/>
    <boot order='1'/>
  </interface>
</devices>
...
```

对于支持此功能的 hypervisor，您可以设置特定的 NIC 用于网络引导。order 属性确定引导序列期间尝试设备的顺序。每个设备的 boot 元素不能与 [客户机固件](https://www.libvirt.org/formatdomain.html#guest-firmware) 部分中的通用 boot 元素一起使用。自 0.8.8 起

#### 21.11.20 [接口 ROM BIOS 配置](https://www.libvirt.org/formatdomain.html#id62)

```
...
<devices>
  <interface type='network'>
    <source network='default'/>
    <target dev='vnet1'/>
    <rom bar='on' file='/etc/fake/boot.bin'/>
  </interface>
</devices>
...
```

对于支持此功能的 hypervisor，您可以更改 PCI 网络设备的 ROM 如何呈现给客户机。bar 属性可以设置为 "on" 或 "off"，并确定设备的 ROM 是否会在客户机的内存映射中可见。（在 PCI 文档中，"rombar" 设置控制 ROM 的基址寄存器的存在）。如果未指定 rom bar，则使用 qemu 默认值（较旧版本的 qemu 使用默认值 "off"，而较新的 qemus 使用默认值 "on"）。可选的 file 属性用于指向要作为设备的 ROM BIOS 呈现给客户机的二进制文件。这对于为网络设备提供替代引导 ROM 很有用。自 0.9.10 起（仅 QEMU 和 KVM）。

#### 21.11.21 [在驱动域中设置网络后端](https://www.libvirt.org/formatdomain.html#id63)

```
...
<devices>
  ...
  <interface type='bridge'>
    <source bridge='br0'/>
    <backenddomain name='netvm'/>
  </interface>
  ...
</devices>
...
```

可选的 backenddomain 元素允许为接口指定后端域（也称为驱动域）。使用 name 属性指定后端域名称。您可以使用它在域之间创建直接网络链接（因此数据不会通过主机系统）。与 type 'ethernet' 一起使用以创建纯网络链接，或与 type 'bridge' 一起使用以连接到后端域内的桥接器。自 1.2.13 起（仅 Xen）

#### 21.11.22 [服务质量](https://www.libvirt.org/formatdomain.html#id64)

```
...
<devices>
  <interface type='network'>
    <source network='default'/>
    <target dev='vnet0'/>
    <bandwidth>
      <inbound average='1000' peak='5000' floor='200' burst='1024'/>
      <outbound average='128' peak='256' burst='256'/>
    </bandwidth>
  </interface>
</devices>
...
```

接口 XML 的这部分提供服务质量设置。传入和传出流量可以独立进行整形。bandwidth 元素及其子元素在网络 XML 的 [QoS](https://www.libvirt.org/formatnetwork.html#quality-of-service) 部分中描述。

#### 21.11.23 [设置 VLAN 标签（仅在支持的网络类型上）](https://www.libvirt.org/formatdomain.html#id65)

```
...
<devices>
  <interface type='bridge'>
    <vlan>
      <tag id='42'/>
    </vlan>
    <source bridge='ovsbr0'/>
    <virtualport type='openvswitch'>
      <parameters interfaceid='09b11c53-8b5c-4eeb-8f00-d84eaa0aaa4f'/>
    </virtualport>
  </interface>
  <interface type='bridge'>
    <vlan trunk='yes'>
      <tag id='42'/>
      <tag id='123' nativeMode='untagged'/>
    </vlan>
    ...
  </interface>
</devices>
...
```

如果（且仅当）客户机使用的网络连接支持对客户机透明的 VLAN 标记，则可选的 <vlan> 元素可以指定一个或多个 VLAN 标签应用于客户机的网络流量。自 0.10.0 起。

支持客户机透明 VLAN 标记的网络连接包括连接到 Open vSwitch 桥接器的 type='bridge' 接口、通过 type='hostdev'（直接设备分配）使用的 SRIOV 虚拟功能 (VF)（自 1.3.5 起）、通过 type='direct' 且 mode='passthrough'（macvtap "passthru" 模式）使用的 SRIOV VF，以及自 11.0.0 起的标准 Linux 桥接器。其他连接类型，包括 libvirt 自己的虚拟网络，**不** 支持它。802.1Qbh (vn-link) 和 802.1Qbg (VEPA) 交换机提供了自己的方式（在 libvirt 之外）将客户机流量标记到特定 VLAN。每个标签在 <vlan> 的单独 <tag> 子元素中给出（例如：<tag id='42'/>）。对于多个标签的 VLAN 中继（在 Open vSwitch 连接和标准 Linux 桥接器上支持），可以指定多个 <tag> 子元素，这意味着用户希望在接口上对所有指定的标签进行 VLAN 中继。如果需要单个标签的 VLAN 中继，可以将可选属性 trunk='yes' 添加到顶级 <vlan> 元素，以区分单个标签的中继与普通标记。

对于使用 Open vSwitch 和标准 Linux 桥接器的网络连接，还可以配置 'native-tagged' 和 'native-untagged' VLAN 模式。自 1.1.0 起。这通过 <tag> 子元素上的可选 nativeMode 属性完成：nativeMode 可以设置为 'tagged' 或 'untagged'。包含 nativeMode 的 <tag> 子元素的 id 属性设置哪个 VLAN 被视为此接口的"原生" VLAN，nativeMode 属性确定该 VLAN 的流量是否会被标记。

#### 21.11.24 [隔离客户机的网络流量](https://www.libvirt.org/formatdomain.html#id66)

```
...
<devices>
  <interface type='network'>
    <source network='default'/>
    <port isolated='yes'/>
  </interface>
</devices>
...
```

自 6.1.0 起。当 port 元素属性 isolated 设置为 yes（默认设置为 no）时，用于隔离此接口的网络流量与连接到同一网络且也具有 <port isolated='yes'/> 的其他客户机接口的流量。此设置仅支持使用标准 tap 设备通过 Linux 主机桥接器连接到网络的模拟接口设备。此属性可以从 libvirt 网络继承，因此如果所有将连接到网络的客户机都应被隔离，最好将设置放在网络配置中。（注意：这仅防止具有 isolated='yes' 的客户机相互通信；如果同一桥接器上有一个没有 isolated='yes' 的客户机，即使是隔离的客户机也能够与它通信。）

#### 21.11.25 [修改虚拟链路状态](https://www.libvirt.org/formatdomain.html#id67)

```
...
<devices>
  <interface type='network'>
    <source network='default'/>
    <target dev='vnet0'/>
    <link state='down'/>
  </interface>
</devices>
...
```

此元素提供设置虚拟网络链路状态的方法。属性 state 的可能值为 up 和 down。如果指定为 down，则接口的行为就像网络电缆断开一样。如果未指定此元素，默认行为是链路状态为 up。自 0.9.5 起

#### 21.11.26 [MTU 配置](https://www.libvirt.org/formatdomain.html#id68)

```
...
<devices>
  <interface type='network'>
    <source network='default'/>
    <target dev='vnet0'/>
    <mtu size='1500'/>
  </interface>
</devices>
...
```

此元素提供设置虚拟网络链路 MTU 的方法。目前只有一个属性 size，接受非负整数，指定接口的 MTU 大小。自 3.1.0 起

#### 21.11.27 [合并设置](https://www.libvirt.org/formatdomain.html#id69)

```
...
<devices>
  <interface type='network'>
    <source network='default'/>
    <target dev='vnet0'/>
    <coalesce>
      <rx>
        <frames max='7'/>
      </rx>
    </coalesce>
  </interface>
</devices>
...
```

此元素提供为某些接口设备（目前仅 type network 和 bridge）设置合并设置的方法。目前只有一个属性 max，在 rx 组的 frames 元素中调整，接受非负整数，指定在中断之前将接收的最大数据包数。自 3.3.0 起

#### 21.11.28 [IP 配置](https://www.libvirt.org/formatdomain.html#id70)

```
...
<devices>
  <interface type='network'>
    <source network='default'/>
    <target dev='vnet0'/>
    <ip address='192.168.122.5' prefix='24'/>
    <ip address='192.168.122.5' prefix='24' peer='10.0.0.10'/>
    <route family='ipv4' address='192.168.122.0' prefix='24' gateway='192.168.122.1'/>
    <route family='ipv4' address='192.168.122.8' gateway='192.168.122.1'/>
  </interface>
  ...
  <hostdev mode='capabilities' type='net'>
    <source>
      <interface>eth0</interface>
    </source>
    <ip address='192.168.122.6' prefix='24'/>
    <route family='ipv4' address='192.168.122.0' prefix='24' gateway='192.168.122.1'/>
    <route family='ipv4' address='192.168.122.8' gateway='192.168.122.1'/>
  </hostdev>
  ...
</devices>
...
```

自 1.2.12 起，网络设备和具有网络功能的 hostdev 设备可以可选地提供一个或多个 IP 地址，以在客户机的网络设备上设置。请注意，一些 hypervisor 或网络设备类型会简单地忽略它们或仅使用第一个。family 属性可以设置为 ipv4 或 ipv6，address 属性包含 IP 地址。可选的 prefix 是网络掩码中 1 位的数量，如果未指定，将自动设置 - 对于 IPv4，默认前缀根据网络"类别"（A、B 或 C - 见 RFC870）确定，对于 IPv6，默认前缀为 64。可选的 peer 属性保存点对点网络设备另一端的 IP 地址（自 2.1.0 起）。

自 1.2.12 起，还可以添加 route 元素来定义要在客户机中添加的 IP 路由。此元素的属性在 [网络定义](https://www.libvirt.org/formatnetwork.html#static-routes) 中 route 元素的文档中描述。LXC 驱动程序使用此元素在容器内添加通用路由。自 12.2.0 起，route 元素也由 QEMU 驱动程序使用，仅在基于 passt 的接口（<backend type='passt'/>）的情况下，并且仅用于默认路由（通过仅指定网关完成）。

```
...
<devices>
  <interface type='ethernet'>
    <source/>
      <ip address='192.168.123.1' prefix='24'/>
      <ip address='10.0.0.10' prefix='24' peer='192.168.122.5'/>
      <route family='ipv4' address='192.168.42.0' prefix='24' gateway='192.168.123.4'/>
    <source/>
    ...
  </interface>
  ...
</devices>
...
```

自 2.1.0 起，type "ethernet" 的网络设备可以可选地提供一个或多个 IP 地址和一个或多个路由，以在网络设备的 **主机** 侧设置。这些配置为接口的 <source> 元素的子元素，并且具有与用于配置接口客户机侧的同名元素相同的属性（如上所述）。

#### 21.11.29 [vhost-user 连接](https://www.libvirt.org/formatdomain.html#id71)

自 1.2.7 起，vhost-user 启用 QEMU 虚拟机和其他用户空间进程之间使用 Virtio 传输协议的通信。控制平面使用字符设备（例如 Unix 套接字），而数据平面基于共享内存。

```
...
<devices>
  <interface type='vhostuser'>
    <mac address='52:54:00:3b:83:1a'/>
    <source type='unix' path='/tmp/vhost1.sock' mode='server'/>
    <model type='virtio'/>
  </interface>
  <interface type='vhostuser'>
    <mac address='52:54:00:3b:83:1b'/>
    <source type='unix' path='/tmp/vhost2.sock' mode='client'>
      <reconnect enabled='yes' timeout='10'/>
    </source>
    <model type='virtio'/>
    <driver queues='5'/>
  </interface>
</devices>
...
```

必须指定 <source> 元素以及字符设备的类型。目前，仅支持 type='unix'，其中 path（套接字的目录路径）和 mode 属性是必需的。支持 mode='server' 和 mode='client'。（自 11.1.0 起，vhostuser 接口的默认源类型为 'unix'，默认模式为 'client'，因此这两个属性现在是可选的）。

vhost-user 协议仅与 virtio 客户机驱动程序一起工作，因此 <model> 元素 type 属性是强制性的（自 11.1.0 起，vhostuser 接口的默认模型类型现在是 'virtio'，因此 <model> 不再是强制性的）。自 4.1.0 起，<source> 元素有一个可选的子元素 reconnect，用于配置连接丢失时的重连超时。它有两个属性：enabled（接受 yes 和 no）和 timeout，指定 hypervisor 尝试重连的秒数。

请注意，当使用 mode='server' 时，hypervisor 将等待传入连接建立，然后才实际运行 VM。热插拔具有此类配置的接口时，即使没有建立连接，VM 也会继续运行。建议使用 mode='client' 代替。

#### 21.11.30 [使用 passt 后端的 vhost-user 连接](https://www.libvirt.org/formatdomain.html#id72)

自 11.1.0 起（仅 QEMU 和 KVM），passt 可以用作 vhost-user 连接的另一端。这是一个引人注目的替代方案，因为 passt 提供所有网络连接性而不需要任何提升的权限或能力，并且 vhost-user 使用共享内存使这种无权限连接也非常高性能。您可以通过添加 <backend type='passt'/> 来设置 type='vhostuser' 接口使用 passt 作为后端。当 passt 是后端时，仅支持单个驱动程序队列，并且 <source> path/type/mode 都隐含为"匹配 passt 进程"，因此 **不得** 指定。[此处描述](https://www.libvirt.org/formatdomain.html#userspace-connection-using-passt) 的所有 passt 选项也支持用于带有 passt 后端的 type='vhostuser'，例如使用 <ip> 设置客户机侧 IP 地址和使用 <portForward> 进行端口转发。

```
...
<devices>
  <interface type='vhostuser'>
    <backend type='passt' fqdn='bob.example.com'/>
    <mac address='52:54:00:3b:83:1a'/>
    <source dev='enp1s0'/>
    <ip address='10.30.0.5' prefix='24'/>
    <route gateway='10.30.0.1'/>
  </interface>
</devices>
...
```

#### 21.11.31 [使用 NWFilter 进行流量过滤](https://www.libvirt.org/formatdomain.html#id73)

自 0.8.0 起（QEMU），0.9.3 起（LXC），10.1.0 起（Cloud Hypervisor），可以为域接口分配 nwfilter 配置文件，这允许为虚拟机配置网络流量过滤规则。有关更完整的详细信息，请参阅 [nwfilter](https://www.libvirt.org/formatnwfilter.html) 文档。

```
...
<devices>
  <interface ...>
    ...
    <filterref filter='clean-traffic'/>
  </interface>
  <interface ...>
    ...
    <filterref filter='myfilter'>
      <parameter name='IP' value='104.207.129.11'/>
      <parameter name='IP6_ADDR' value='2001:19f0:300:2102::'/>
      <parameter name='IP6_MASK' value='64'/>
      ...
    </filterref>
  </interface>
</devices>
...
```

filter 属性指定要使用的 nwfilter 的名称。可以指定可选的 <parameter> 元素，用于通过 name 和 value 属性向 nwfilter 传递附加信息。有关参数的信息，请参阅 [nwfilter](https://www.libvirt.org/formatnwfilter.html#usage-of-variables-in-filters) 文档。

### 21.12 [输入设备](https://www.libvirt.org/formatdomain.html#id74)

输入设备允许与客户机虚拟机中的图形帧缓冲区进行交互。启用帧缓冲区时，会自动提供输入设备。可能可以显式添加额外的设备，例如，提供用于绝对光标移动的图形平板电脑。

```
...
<devices>
  <input type='mouse' bus='usb'/>
  <input type='keyboard' bus='usb'/>
  <input type='mouse' bus='virtio'/>
  <input type='keyboard' bus='virtio'/>
  <input type='tablet' bus='virtio'/>
  <input type='passthrough' bus='virtio'>
    <source evdev='/dev/input/event1'/>
  </input>
  <input type='evdev'>
    <source dev='/dev/input/event1234' grab='all' repeat='on' grabToggle='ctrl-ctrl'/>
  </input>
</devices>
...
```

- input

  input 元素有一个强制属性 type，其值可以是 'mouse'、'tablet'、（自 1.2.2 起）'keyboard'、（自 1.3.0 起）'passthrough' 或（自 7.4.0 起）'evdev'。tablet 提供绝对光标移动，而 mouse 使用相对移动。可选的 bus 属性可用于细化确切的设备类型。它接受值 "xen"（半虚拟化）、"ps2" 和 "usb" 或（自 1.3.0 起）"virtio"。

input 元素有一个可选的子元素 <address>，可以将设备绑定到特定的 PCI 插槽，在 [设备地址](https://www.libvirt.org/formatdomain.html#device-addresses) 部分中有记录。在 S390 上，address 可用于为输入设备提供 CCW 地址（自 4.2.0 起）。对于类型 passthrough 和 evdev，强制子元素 source 必须具有 evdev（对于 passthrough）或 dev（对于 evdev）属性，包含传递给客户机的事件设备的绝对路径。对于类型 evdev，source 有三个可选属性：grab，值为 'all'，启用时抓取所有输入设备而不仅仅是一个；repeat，值为 'on'/'off'，启用/禁用自动重复事件；以及 grabToggle（自 7.6.0 起），值为 ctrl-ctrl、alt-alt、shift-shift、meta-meta、scrolllock 或 ctrl-scrolllock，以更改抓取键组合。输入类型 evdev 目前仅在 linux 设备上受支持。（仅 KVM）自 5.2.0 起，input 元素接受 model 属性，其值为 'virtio'、'virtio-transitional' 或 'virtio-non-transitional'。有关更多详细信息，请参阅 [virtio 设备模型](https://www.libvirt.org/formatdomain.html#virtio-device-models)。

子元素 driver 可用于调整设备的 virtio 选项：[Virtio 相关选项](https://www.libvirt.org/formatdomain.html#virtio-related-options) 也可以设置。（自 3.5.0 起）

### 21.13 [集线器设备](https://www.libvirt.org/formatdomain.html#id75)

集线器是一种将单个端口扩展为多个端口的设备，以便有更多端口可用于将设备连接到主机系统。

```
...
<devices>
  <hub type='usb'/>
</devices>
...
```

- hub

  hub 元素有一个强制属性 type，其值只能是 'usb'。

hub 元素有一个可选的子元素 <address>（请参阅 [设备地址](https://www.libvirt.org/formatdomain.html#device-addresses)）type='usb'，可以将设备绑定到特定的控制器。

### 21.14 [图形帧缓冲区](https://www.libvirt.org/formatdomain.html#id76)

图形设备允许与客户机 OS 进行图形交互。客户机通常会配置帧缓冲区或文本控制台以允许与管理员交互。

```
...
<devices>
  <graphics type='sdl' display=':0.0'/>
  <graphics type='vnc' port='5904' sharePolicy='allow-exclusive'>
    <listen type='address' address='1.2.3.4'/>
  </graphics>
  <graphics type='rdp' autoport='yes' multiUser='yes'/>
  <graphics type='desktop'/>
  <graphics type='spice'>
    <listen type='network' network='rednet'/>
  </graphics>
</devices>
...
```

- graphics

  graphics 元素有一个强制的 type 属性，取值为 sdl、vnc、spice、rdp、desktop 或 egl-headless：sdl 在主机桌面上显示一个窗口，它可以接受 3 个可选参数：display 属性用于要使用的显示器，xauth 属性用于身份验证标识符，以及可选的 fullscreen 属性接受值 yes 或 no。您可以使用带有 enable="yes" 属性的 gl 来启用 SDL 中的 OpenGL 支持。同样，您可以使用 enable="no" 显式禁用 OpenGL 支持。vnc 启动 VNC 服务器。port 属性指定 TCP 端口号（-1 作为传统语法表示应自动分配）。autoport 属性是表示自动分配要使用的 TCP 端口的新首选语法。passwd 属性以明文形式提供 VNC 密码。如果 passwd 属性设置为空字符串，则禁用 VNC 访问。keymap 属性指定要使用的键盘映射。可以通过给出时间戳 passwdValidTo='2010-04-09T15:51:00'（假定为 UTC）来设置密码有效性的限制。connected 属性允许在密码更改期间控制连接的客户端。VNC 仅接受 keep 值自 0.9.3 起。注意，这可能不被所有 hypervisor 支持。可选的 sharePolicy 属性指定 vnc 服务器显示共享策略。allow-exclusive 允许客户端通过断开其他连接来请求独占访问。并行连接多个客户端需要所有客户端请求共享会话（vncviewer: -Shared 开关）。这是默认值。force-shared 禁用独占客户端访问，每个连接都必须为 vncviewer 指定 -Shared 开关。ignore 无条件欢迎每个连接自 1.0.6 起。QEMU 支持 socket 属性用于在 unix 域套接字路径上监听，而不是使用 listen/port。自 0.8.8 起。对于 VNC WebSocket 功能，可以使用 websocket 属性指定要监听的端口（-1 表示自动分配）。

图形设备使用 <listen> 来设置设备应该在哪里监听客户端。它有一个强制属性 type，指定监听类型。只有 vnc、spice 和 rdp 支持 <listen> 元素。自 0.9.4 起。可用类型有：

- address

  告诉图形设备使用在 address 属性中指定的地址，该地址将包含 IP 地址或主机名（将通过 DNS 查询解析为 IP 地址）以监听。可以省略 address 属性以使用配置文件中的地址。自 1.3.5 起。address 属性在 graphics 元素中被复制为 listen 属性以向后兼容。如果两者都提供，它们必须相等。

- network

  这用于指定 libvirt 配置网络列表中的现有网络，在 network 属性中。将检查命名的网络配置以确定适当的监听地址，该地址将存储在活动 XML 的 address 属性中。例如，如果网络在其配置中具有 IPv4 地址（例如，如果它具有 route、nat 或无 forward 类型（隔离）的 forward 类型），将使用网络配置中列出的第一个 IPv4 地址。如果网络描述主机桥接器，将使用与该桥接器设备关联的第一个 IPv4 地址，如果网络描述 'direct'（macvtap）模式之一，将使用第一个 forward dev 的第一个 IPv4 地址。

- socket 自 2.0.0 起（仅 QEMU）

  此监听类型告诉图形服务器在 unix 套接字上监听。属性 socket 包含 unix 套接字的路径。如果省略此属性，libvirt 将为您生成此路径。由图形类型 vnc 和 spice 支持。为了与 vnc 图形向后兼容，第一个 listen 元素的 socket 属性在 graphics 元素中被复制为 socket 属性。如果 graphics 元素包含 socket 属性，所有 listen 元素都将被忽略。

- none 自 2.0.0 起（仅 QEMU）

  此监听类型没有任何其他属性。Libvirt 支持通过我们的 API virDomainOpenGraphics() 和 virDomainOpenGraphicsFD() 传递文件描述符。如果使用此类型，则不允许其他监听类型，并且图形设备不会在任何地方监听。您需要使用两个 API 之一将 FD 传递给 QEMU 以连接到此图形设备。由图形类型 vnc 和 spice 支持。

### 21.15 [视频设备](https://www.libvirt.org/formatdomain.html#id77)

视频设备。

```
...
<devices>
  <video>
    <model type='vga' vram='16384' heads='1'>
      <acceleration accel3d='yes' accel2d='yes'/>
    </model>
    <driver name='qemu'/>
  </video>
</devices>
...
```

- video

  video 元素是用于描述视频设备的容器。为了向后兼容，如果没有设置 video 但域 xml 中有 graphics，则 libvirt 将根据客户机类型添加默认视频。对于类型为 "kvm" 的客户机，默认视频为：type 值为 "cirrus"，vram 值为 "16384"，heads 值为 "1"。默认情况下，域 xml 中的第一个视频设备是主设备，但可选属性 primary（自 1.0.2 起）值为 'yes' 可用于在多个视频设备的情况下标记主设备。非主设备必须是 "qxl" 类型或（自 2.4.0 起）"virtio" 类型。

- model

  model 元素有一个强制的 type 属性，取值为 "vga"、"cirrus"、"vmvga"、"xen"、"vbox"、"qxl"（自 0.8.6 起）、"virtio"（自 1.3.0 起）、"gop"（自 3.2.0 起）、"bochs"（自 5.6.0 起）、"ramfb"（自 5.9.0 起）或 "none"（自 4.6.0 起），具体取决于可用的 hypervisor 功能。注意：类型 none 的目的是指示 libvirt 不在客户机中添加默认视频设备（参见上面的 video 元素描述），因为在 GPU 介导的设备打算成为客户机内唯一渲染设备的情况下，这种行为不方便。如果这是您的用例，请在 XML 中指定 none 类型的视频设备以停止默认行为。请参阅 [主机设备分配](https://www.libvirt.org/formatdomain.html#host-device-assignment) 以了解如何将介导设备添加到客户机。您可以使用 vram 以 kibibytes（1024 字节的块）提供视频内存量。这仅支持客户机类型 "vz"、"qemu"、"kvm"、"hvf"、"vbox"、"vmx" 和 "xen"。如果未提供值，则使用默认值。如果大小不是 2 的幂，它将被舍入到最接近的一个。屏幕数量可以使用 heads 设置。这仅支持客户机类型 "vz"、"kvm"、"hvf"、"vbox" 和 "vmx"。对于客户机类型 "kvm"、"hvf" 或 "qemu" 和模型类型 "qxl"，有可选属性。属性 ram（自 1.0.2 起）指定主 bar 的大小，而属性 vram 指定次 bar 大小。如果未提供 ram 或 vram，则使用默认值。ram 也应像 vram 一样舍入到 2 的幂。还有可选属性 vgamem（自 1.2.11 起），用于为 QXL 设备的回退模式设置 VGA 帧缓冲区的大小。属性 vram64（自 1.3.3 起）扩展次 bar 并使其可作为 64 位内存寻址。自 9.2.0 起（仅 QEMU 驱动程序），类型为 "virtio" 的设备有一个可选的 blob 属性，可以设置为 "on" 或 "off"。将 blob 设置为 "on" 将启用使用 blob 资源。

- acceleration

  配置是否应启用视频加速。accel2d 启用 2D 加速（仅适用于 vbox 驱动程序，自 0.7.1 起）accel3d 启用 3D 加速（自 0.7.1 起适用于 vbox 驱动程序，自 1.3.0 起适用于 qemu 驱动程序）rendernode 用于渲染的主机 DRI 设备的绝对路径（仅适用于 'vhostuser' 驱动程序，自 5.8.0 起）。如果未指定，libvirt 将选择一个可用的。

- address

  可选的 address 子元素可用于将视频设备绑定到特定的 PCI 插槽。在 S390 上，address 可用于为视频设备提供 CCW 地址（自 4.2.0 起）。

- driver

  子元素 driver 可用于调整设备：name 指定要使用的后端驱动程序，根据可用的 hypervisor 功能，可以是 "qemu" 或 "vhostuser"（自 5.8.0 起）。"qemu" 是默认的 QEMU 后端。"vhostuser" 将使用单独的 vhost-user 进程后端（用于 virtio 设备）。virtio 选项 [Virtio 相关选项](https://www.libvirt.org/formatdomain.html#virtio-related-options) 也可以设置（自 3.5.0 起）VGA 配置使用 vgaconf 属性控制向客户机公开的视频设备，该属性取值为 "io"、"on" 或 "off"。目前，它仅适用于 bhyve 的 "gop" 视频模型类型（自 3.5.0 起）

### 21.16 [控制台、串行、并行和通道设备](https://www.libvirt.org/formatdomain.html#id78)

字符设备提供与虚拟机交互的方式。半虚拟化控制台、串行端口、并行端口和通道都被归类为字符设备，因此使用相同的语法表示。

```
...
<devices>
  <parallel type='pty'>
    <source path='/dev/pts/2'/>
    <target port='0'/>
  </parallel>
  <serial type='pty'>
    <source path='/dev/pts/3'/>
    <target port='0'/>
  </serial>
  <serial type='file'>
    <source path='/tmp/file' append='on'>
      <seclabel model='dac' relabel='no'/>
    </source>
    <target port='0'/>
  </serial>
  <console type='pty'>
    <source path='/dev/pts/4'/>
    <target port='0'/>
  </console>
  <channel type='unix'>
    <source mode='bind' path='/tmp/guestfwd'/>
    <target type='guestfwd' address='10.0.2.1' port='4600'/>
  </channel>
</devices>
...
```

在这些指令中的每一个中，顶级元素名称（parallel、serial、console、channel）描述设备如何呈现给客户机。客户机接口由 target 元素配置。

呈现给主机的接口在顶级元素的 type 属性中给出。主机接口由 source 元素配置。

source 元素可能包含一个可选的 seclabel，以覆盖在套接字路径上进行标记的方式。如果此元素不存在，则 [安全标签](https://www.libvirt.org/formatdomain.html#security-label) 从每个域设置继承。

如果呈现给主机的接口类型是 "file"，则 source 元素可能包含一个可选的 append 属性，指定在域重启时是否应保留文件中的信息。允许的值为 "on" 和 "off"（默认）。自 1.3.1 起。

无论类型如何，字符设备都可以有一个关联的可选日志文件。这通过 log 子元素表示，带有 file 属性。还可以有一个 append 属性，接受上述相同的值。自 1.3.3 起。

```
...
<log file="/var/log/libvirt/qemu/guestname-serial0.log" append="off"/>
...
```

每个字符设备元素都有一个可选的子元素 <address>，可以将设备绑定到特定的控制器（请参阅 [控制器](https://www.libvirt.org/formatdomain.html#controllers)）或 PCI 插槽。

对于类型为 unix 或 tcp 的字符设备，source 有一个可选元素 reconnect，用于配置连接丢失时的重连超时。有两个属性：enabled，可能的值为 "yes" 和 "no"；以及 timeout，以秒为单位。reconnect 属性仅对 connect 模式有效。自 3.7.0 起（仅 QEMU 驱动程序）。

#### 21.16.1 [客户机接口](https://www.libvirt.org/formatdomain.html#id79)

字符设备向客户机呈现为以下类型之一。

##### 21.16.1.1 [并行端口](https://www.libvirt.org/formatdomain.html#id80)

```
...
<devices>
  <parallel type='pty'>
    <source path='/dev/pts/2'/>
    <target port='0'/>
  </parallel>
</devices>
...
```

target 可以有一个 port 属性，指定端口号。端口从 0 开始编号。通常有 0、1 或 2 个并行端口。

##### 21.16.1.2 [串行端口](https://www.libvirt.org/formatdomain.html#id81)

```
...
<devices>
  <!-- Serial port -->
  <serial type='pty'>
    <source path='/dev/pts/3'/>
    <target port='0'/>
  </serial>
  <!-- Debug port for SeaBIOS / EDK II -->
  <serial type='file'>
    <target type='isa-debug'/>
    <address type='isa' iobase='0x402'/>
    <source path='/tmp/DOMAIN-ovmf.log'/>
  </serial>

</devices>
...
...
<devices>
  <!-- USB serial port -->
  <serial type='pty'>
    <target type='usb-serial' port='0'>
      <model name='usb-serial'/>
    </target>
    <address type='usb' bus='0' port='1'/>
  </serial>
</devices>
...
```

target 元素可以有一个可选的 port 属性，指定端口号（从 0 开始），以及一个可选的 type 属性：自 1.0.2 起，有效值为 isa-serial（可用于 x86 客户机）、usb-serial（只要 USB 支持可用）和 pci-serial（只要 PCI 支持可用）；自 3.10.0 起，spapr-vio-serial（可用于 ppc64/pseries 客户机）、system-serial（可用于 aarch64/virt，自 4.7.0 起，riscv/virt 客户机）、sclp-serial（可用于 s390 和 s390x 客户机）也可用，自 8.1.0 起 isa-debug（可用于 x86 客户机）。

自 3.10.0 起，target 元素可以有一个可选的 model 子元素；其 name 属性的有效值为：isa-serial（可用于 isa-serial target 类型）；usb-serial（可用于 usb-serial target 类型）；pci-serial（可用于 pci-serial target 类型）；spapr-vty（可用于 spapr-vio-serial target 类型）；pl011 和自 4.7.0 起 16550a（可用于 system-serial target 类型）；sclpconsole 和 sclplmconsole（可用于 sclp-serial target 类型）。自 8.1.0 起，isa-debugcon（可用于 isa-debug target 类型）；在 x86 平台上提供用于接收来自固件的调试消息的虚拟控制台。提供 target model 通常是不必要的：libvirt 会自动选择一个适合所选 target 类型的 model，通常不建议覆盖该值。

如果用户未指定任何属性，libvirt 将选择适合大多数用户的值。

大多数 target 类型支持配置客户机可见的设备地址，如 [设备地址](https://www.libvirt.org/formatdomain.html#device-addresses) 部分所述；更具体地说，可接受的地址类型是 isa（用于 isa-serial）、usb（用于 usb-serial）、pci（用于 pci-serial）和 spapr-vio（用于 spapr-vio-serial）。system-serial 和 sclp-serial target 类型不支持指定地址。

有关串行端口和控制台之间的关系，请参阅 [串行端口和控制台之间的关系](https://www.libvirt.org/formatdomain.html#relationship-between-serial-ports-and-consoles) 部分。

##### 21.16.1.3 [控制台](https://www.libvirt.org/formatdomain.html#id82)

```
...
<devices>
  <!-- Serial console -->
  <console type='pty'>
    <source path='/dev/pts/2'/>
   <target type='serial' port='0'/>
  </console>
</devices>
...
...
<devices>
  <!-- KVM virtio console -->
  <console type='pty'>
    <source path='/dev/pts/5'/>
    <target type='virtio' port='0'/>
  </console>
</devices>
...
```

console 元素用于表示交互式串行控制台。根据所使用的客户机类型和配置的具体情况，console 元素可能表示与现有 serial 元素相同的设备或单独的设备。

支持 target 子元素，其工作方式与 serial 元素相同（详见 [串行端口](https://www.libvirt.org/formatdomain.html#serial-port)）。type 属性的有效值为：serial（如下所述）；virtio（只要 VirtIO 支持可用）；xen、lxc 和 openvz（当使用相应的 hypervisor 时可用）。sclp 和 sclplm（可用于 s390 和 s390x QEMU 客户机）为兼容性原因受支持，但不应用于新客户机：请分别使用 sclpconsole 和 sclplmconsole target 模型与 serial 元素。

在上面列出的 target 类型中，serial 是特殊的，因为它不表示单独的设备，而是与第一个 serial 元素相同的设备。因此，每个客户机只能有一个 target 类型为 serial 的 console 元素。

Virtio 控制台通常可在客户机内部以 /dev/hvc[0-7] 访问；有关更多信息，请参阅 <https://fedoraproject.org/wiki/Features/VirtioSerial>。自 0.8.3 起

有关串行端口和控制台之间的关系，请参阅 [串行端口和控制台之间的关系](https://www.libvirt.org/formatdomain.html#relationship-between-serial-ports-and-consoles) 部分。

##### 21.16.1.4 [串行端口和控制台之间的关系](https://www.libvirt.org/formatdomain.html#id83)

由于历史原因，serial 和 console 元素的作用域部分重叠。

一般来说，这两个元素都用于配置一个或多个串行控制台，用于与客户机交互。两者之间的主要区别是 serial 用于模拟的、通常是原生的串行控制台，而 console 用于半虚拟化的串行控制台。

模拟和半虚拟化串行控制台都有优缺点：

- 模拟串行控制台通常比半虚拟化控制台初始化早得多，因此它们可用于控制引导加载程序并显示固件和早期引导消息；
- 在多个平台上，每个客户机只能有一个模拟串行控制台，但半虚拟化控制台不受此限制。

如下配置：

```
...
<devices>
  <console type='pty'>
    <target type='serial'/>
  </console>
  <console type='pty'>
    <target type='virtio'/>
  </console>
</devices>
...
```

将在任何平台上工作，并将产生一个用于早期引导日志/交互式/恢复使用的模拟串行控制台，以及一个用作侧通道的半虚拟化串行控制台。大多数人只需在其配置中包含第一个 console 元素就可以了，但如果需要特定配置，则应指定两个元素。

请注意，由于前面提到的兼容性问题，以下所有配置：

```
...
<devices>
  <serial type='pty'/>
</devices>
...
...
<devices>
  <console type='pty'/>
</devices>
...
...
<devices>
  <serial type='pty'/>
  <console type='pty'/>
</devices>
...
```

将被视为相同，并将导致客户机可以使用单个模拟串行控制台。

##### 21.16.1.5 [通道](https://www.libvirt.org/formatdomain.html#id84)

这表示主机和客户机之间的专用通信通道。

```
...
<devices>
  <channel type='unix'>
    <source mode='bind' path='/tmp/guestfwd'/>
    <target type='guestfwd' address='10.0.2.1' port='4600'/>
  </channel>

  <!-- KVM virtio channel -->
  <channel type='pty'>
    <target type='virtio' name='arbitrary.virtio.serial.port.name'/>
  </channel>
  <channel type='unix'>
    <source mode='bind' path='/var/lib/libvirt/qemu/f16x86_64.agent'/>
    <target type='virtio' name='org.qemu.guest_agent.0' state='connected'/>
  </channel>
  <channel type='spicevmc'>
    <target type='virtio' name='com.redhat.spice.0'/>
  </channel>
</devices>
...
```

这可以通过多种方式实现。通道的特定类型在 target 元素的 type 属性中给出。不同的通道类型有不同的 target 属性。

- guestfwd

  客户机发送到给定 IP 地址和端口的 TCP 流量被转发到主机上的通道设备。target 元素必须具有 address 和 port 属性。自 0.7.3 起

- virtio

  半虚拟化 virtio 通道。通道在客户机中以 /dev/vport\* 形式公开，如果指定了可选元素 name，则以 /dev/virtio-ports/$name 形式公开（有关更多信息，请参阅 <https://fedoraproject.org/wiki/Features/VirtioSerial>）。可选元素 address 可以将通道绑定到特定的 type='virtio-serial' 控制器，如 [设备地址](https://www.libvirt.org/formatdomain.html#device-addresses) 部分所述。对于 qemu，如果 name 是 "org.qemu.guest_agent.0"，则 libvirt 可以与安装在客户机中的客户机代理交互，执行客户机关闭或文件系统静默等操作。自 0.7.7 起，客户机代理交互自 0.9.10 起 此外，自 1.0.6 起，可以为 virtio unix 通道自动生成源路径。这在 qemu 客户机代理的情况下非常有用，因为用户通常不关心源路径，因为是 libvirt 与客户机代理通信。如果用户想要使用此功能，他们应该省略 <source> 元素。自 1.2.11 起，virtio 通道的活动 XML 可能包含一个可选的 state 属性，反映客户机中是否有进程在通道上处于活动状态。这是一个仅输出属性。state 属性的可能值为 connected 和 disconnected。

- xen

  半虚拟化 Xen 通道。通道在客户机中作为 Xen 控制台公开，但用名称标识。Xen 通道的设置和使用取决于客户机中的软件和配置。有关更多信息，请参阅 xen-pv-channel(7) 手册页。通道源路径语义与 virtio target 类型相同。由于 Xen 通道缺乏必要的探测机制，因此不支持 state 属性。自 2.3.0 起

- spicevmc

  半虚拟化 SPICE 通道。域还必须有一个 SPICE 服务器作为图形设备（请参阅 [图形帧缓冲区](https://www.libvirt.org/formatdomain.html#graphical-framebuffers)），此时主机会通过主通道附带消息。target 元素必须存在，属性 type='virtio'；可选属性 name 控制客户机如何访问通道，默认为 name='com.redhat.spice.0'。可选的 address 元素可以将通道绑定到特定的 type='virtio-serial' 控制器。自 0.8.8 起

- qemu-vdagent

  半虚拟化 qemu vdagent 通道。此通道实现 SPICE vdagent 协议，但由 qemu 内部处理，因此不需要 SPICE 图形设备。与 spicevmc 通道一样，target 元素必须存在，属性 type='virtio'；可选属性 name 控制客户机如何访问通道，默认为 name='com.redhat.spice.0'。可选的 address 元素可以将通道绑定到特定的 type='virtio-serial' 控制器。某些 vdagent 协议功能可以通过 source 元素启用或禁用。复制和粘贴功能由 clipboard 元素设置。默认情况下它是禁用的，可以通过将 copypaste 属性设置为 yes 来启用。这允许客户机的剪贴板与 qemu 剪贴板管理器同步。当使用 VNC 图形设备时（请参阅 [图形帧缓冲区](https://www.libvirt.org/formatdomain.html#graphical-framebuffers)），这可以启用客户机和客户端之间的复制和粘贴（当使用支持复制/粘贴功能的 VNC 客户端时）或其他支持 qemu 剪贴板管理器的图形类型。鼠标模式由 mouse 元素设置，将其 mode 属性设置为 server 或 client 之一。如果未指定模式，将使用 qemu 默认值（客户端模式）。自 8.4.0 起

#### 21.16.2 [主机接口](https://www.libvirt.org/formatdomain.html#id85)

字符设备向主机呈现为以下类型之一。

##### 21.16.2.1 [域日志文件](https://www.libvirt.org/formatdomain.html#id86)

这会禁用字符设备上的所有输入，并将输出发送到虚拟机的日志文件

```
...
<devices>
  <console type='stdio'>
    <target port='1'/>
  </console>
</devices>
...
```

##### 21.16.2.2 [设备日志文件](https://www.libvirt.org/formatdomain.html#id87)

打开一个文件，发送到字符设备的所有数据都写入该文件。

```
...
<devices>
  <serial type="file">
    <source path="/var/log/vm/vm-serial.log"/>
    <target port="1"/>
  </serial>
</devices>
...
```

##### 21.16.2.3 [虚拟控制台](https://www.libvirt.org/formatdomain.html#id88)

将字符设备连接到虚拟控制台中的图形帧缓冲区。这通常通过特殊的热键序列（如 "ctrl+alt+3"）访问

```
...
<devices>
  <serial type='vc'>
    <target port="1"/>
  </serial>
</devices>
...
```

##### 21.16.2.4 [空设备](https://www.libvirt.org/formatdomain.html#id89)

将字符设备连接到虚空。输入永远不会提供任何数据。所有写入的数据都被丢弃。

```
...
<devices>
  <serial type='null'>
    <target port="1"/>
  </serial>
</devices>
...
```

##### 21.16.2.5 [伪终端](https://www.libvirt.org/formatdomain.html#id90)

使用 /dev/ptmx 分配伪终端。可以使用 'virsh console' 等合适的客户端本地连接到串行端口进行交互。

```
...
<devices>
  <serial type="pty">
    <source path="/dev/pts/3"/>
    <target port="1"/>
  </serial>
</devices>
...
```

注意特殊情况：如果 <console type='pty'>，则 TTY 路径也会作为顶级 <console> 标签上的属性 tty='/dev/pts/3' 重复。这提供了与现有 <console> 标签语法的兼容性。

##### 21.16.2.6 [主机设备代理](https://www.libvirt.org/formatdomain.html#id91)

字符设备被传递到基础物理字符设备。设备类型必须匹配，例如，模拟串行端口应该只连接到主机串行端口 - 不要将串行端口连接到并行端口。

```
...
<devices>
  <serial type="dev">
    <source path="/dev/ttyS0"/>
    <target port="1"/>
  </serial>
</devices>
...
```

##### 21.16.2.7 [命名管道](https://www.libvirt.org/formatdomain.html#id92)

字符设备将输出写入命名管道。有关更多信息，请参阅 pipe(7)。

```
...
<devices>
  <serial type="pipe">
    <source path="/tmp/mypipe"/>
    <target port="1"/>
  </serial>
</devices>
...
```

##### 21.16.2.8 [TCP 客户端/服务器](https://www.libvirt.org/formatdomain.html#id93)

字符设备作为 TCP 客户端连接到远程服务器。

```
...
<devices>
  <serial type="tcp">
    <source mode="connect" host="0.0.0.0" service="2445"/>
    <protocol type="raw"/>
    <target port="1"/>
  </serial>
</devices>
 ...
```

或者作为等待客户端连接的 TCP 服务器。

```
...
<devices>
  <serial type="tcp">
    <source mode="bind" host="127.0.0.1" service="2445"/>
    <protocol type="raw"/>
    <target port="1"/>
  </serial>
</devices>
...
```

或者，您可以使用 telnet 而不是原始 TCP，以便利用 telnet 协议进行连接。

自 0.8.5 起，一些 hypervisor 支持使用 telnets（安全 telnet）或 tls（通过安全套接字层）作为连接的传输协议。

```
...
<devices>
  <serial type="tcp">
    <source mode="connect" host="0.0.0.0" service="2445"/>
    <protocol type="telnet"/>
    <target port="1"/>
  </serial>
  ...
  <serial type="tcp">
    <source mode="bind" host="127.0.0.1" service="2445"/>
    <protocol type="telnet"/>
    <target port="1"/>
  </serial>
</devices>
...
```

自 2.4.0 起，可选属性 tls 可用于控制 chardev TCP 通信通道是否使用 hypervisor 配置的 TLS X.509 证书环境来加密数据通道。对于 QEMU hypervisor，可以通过文件 /etc/libvirt/qemu.conf 中的 chardev_tls 和 chardev_tls_x509_cert_dir 或 default_tls_x509_cert_dir 设置在主机上控制 TLS 环境的使用。如果启用了 chardev_tls，则除非 tls 属性设置为 "no"，否则 libvirt 将使用主机配置的 TLS 环境。如果 chardev_tls 被禁用，但 tls 属性设置为 "yes"，则如果 chardev_tls_x509_cert_dir 或 default_tls_x509_cert_dir TLS 目录结构存在，libvirt 将尝试使用主机 TLS 环境。

```
...
<devices>
  <serial type="tcp">
    <source mode='connect' host="127.0.0.1" service="5555" tls="yes"/>
    <protocol type="raw"/>
    <target port="0"/>
  </serial>
</devices>
...
```

##### 21.16.2.9 [UDP 网络控制台](https://www.libvirt.org/formatdomain.html#id94)

字符设备作为 UDP netconsole 服务，发送和接收数据包。这是一种有损服务。

```
...
<devices>
  <serial type="udp">
    <source mode="bind" host="0.0.0.0" service="2445"/>
    <source mode="connect" host="0.0.0.0" service="2445"/>
    <target port="1"/>
  </serial>
</devices>
...
```

##### 21.16.2.10 [UNIX 域套接字客户端/服务器](https://www.libvirt.org/formatdomain.html#id95)

字符设备作为 UNIX 域套接字服务器，接受来自本地客户端的连接。

```
...
<devices>
  <serial type="unix">
    <source mode="bind" path="/tmp/foo"/>
    <target port="1"/>
  </serial>
</devices>
...
```

##### 21.16.2.11 [Spice 通道](https://www.libvirt.org/formatdomain.html#id96)

字符设备可通过 spice 连接在 channel 属性中指定的通道名称下访问。自 1.2.2 起

注意：根据 hypervisor 的不同，spiceports 可能（或可能不）在带有或不带有 spice 图形的域上启用（请参阅 [图形帧缓冲区](https://www.libvirt.org/formatdomain.html#graphical-framebuffers)）。

```
...
<devices>
  <serial type="spiceport">
    <source channel="org.qemu.console.serial.0"/>
    <target port="1"/>
  </serial>
</devices>
...
```

##### 21.16.2.12 [Nmdm 设备](https://www.libvirt.org/formatdomain.html#id97)

nmdm 设备驱动程序，在 FreeBSD 上可用，提供两个通过虚拟零调制解调器电缆连接在一起的 tty 设备。自 1.2.4 起

```
...
<devices>
  <serial type="nmdm">
    <source master="/dev/nmdm0A" slave="/dev/nmdm0B"/>
  </serial>
</devices>
...
```

source 元素具有这些属性：

- master

  对中的主设备，传递给 hypervisor。设备由完全限定路径指定。

- slave

  对中的从设备，传递给客户端以连接到客户机控制台。设备由完全限定路径指定。

### 21.17 [声音设备](https://www.libvirt.org/formatdomain.html#id98)

可以通过 sound 元素将虚拟声卡附加到主机。自 0.4.3 起

```
...
<devices>
  <sound model='es1370'/>
</devices>
...
```

- sound

  sound 元素有一个强制属性 model，指定模拟什么真实的声音设备。有效值特定于底层 hypervisor，尽管典型的选择是 sb16、es1370、pcspk、ac97（自 0.6.0 起）、ich6（自 0.8.8 起）、ich9（自 1.1.3 起）、usb（自 1.2.8 起）、ich7（自 6.7.0 起，仅 bhyve）和 virtio（自 10.4.0 和 QEMU 8.2.0 起）。

自 0.9.13 起，带有 ich6 或 ich9 模型的 sound 元素可以有可选的子元素 <codec> 来将各种音频编解码器附加到音频设备。如果未指定，将附加默认编解码器以允许播放和录制。

有效值为：

- duplex - 通告线路输入和线路输出
- micro - 通告扬声器和麦克风
- output - 通告线路输出 自 4.4.0 起

```
...
<devices>
  <sound model='ich6'>
    <codec type='micro'/>
  </sound>
</devices>
...
```

自 9.4.0 起，可以使用 multichannel 属性将 usb 声音设备可选地切换到多通道模式：

```
<sound model='usb' multichannel='yes'/>
```

自 10.4.0 和 QEMU 8.2.0 起，可以使用 streams 属性配置 virtio 声音设备中的 PCM 流数量，默认为 2（如果未指定）：

```
<sound model='virtio' streams='2'/>
```

每个 sound 元素都有一个可选的子元素 <address>，可以将设备绑定到特定的 PCI 插槽。请参阅 [设备地址](https://www.libvirt.org/formatdomain.html#device-addresses)。

声音设备可以可选地使用 <audio> 子元素映射到特定的主机音频后端：

```
...
<devices>
  <sound model='ich7'>
     <audio id='1'/>
  </sound>
</devices>
...
```

其中 1 是音频设备的 id（请参阅 [音频后端](https://www.libvirt.org/formatdomain.html#audio-backends)）。如果未指定 ID，则将使用默认音频后端。自 6.7.0 起，bhyve；自 7.2.0 起，qemu。

### 21.18 [音频后端](https://www.libvirt.org/formatdomain.html#id99)

虚拟音频设备对应于映射到客户机声音设备的主机音频后端。

- type

  必需的 type 属性指定音频后端类型。目前，支持的值为 none、alsa、coreaudio、dbus、jack、oss、pipewire、pulseaudio、sdl、spice、file。

- id

  音频设备的整数 id。必须大于 0。

- timerPeriod

  定时器周期（以微秒为单位）。必须大于 0。如果省略，将使用可能的最低周期。

所有后端都支持用于配置输入和输出属性的子元素

```
...
<devices>
  <audio id='1' type='pulseaudio' timerPeriod='40'>
    <input mixingEngine='yes' fixedSettings='yes' voices='1' bufferLength='100'>
      <settings frequency='44100' channels='2' format='s16'/>
    </input>
    <output mixingEngine='yes' fixedSettings='yes' voices='2' bufferLength='100'>
      <settings frequency='22050' channels='4' format='f32'/>
    </output>
  </audio>
</devices>
...
```

input 和 output 元素支持相同的属性和元素集

- mixingEngine

  控制是否使用主机混合引擎在不同音频格式和采样率之间进行转换。禁用混合引擎时，可以使用改进的音频格式，如 5.1/7.1。如果未指定，适用 hypervisor 默认值。

- fixedSettings

  控制混合引擎是否可以动态选择设置以最小化格式转换。这仅在显式启用混合引擎时有效。

- voices

  要使用的声音数量，通常默认为 1

- bufferLength

  音频缓冲区的长度（以微秒为单位）。默认为后端特定。

<input> 和 <output> 元素还可能允许后端特定的选项。

启用固定设置时，允许使用带有以下属性的 <settings> 子元素。

- frequency

  频率（以 HZ 为单位），通常默认为 44100

- channels

  通道数，通常默认为 2。允许的最大通道数是 hypervisor 特定的。

- format

  音频格式，为 s8、u8、s16、u16、s32、u32、f32 之一。默认值是 hypervisor 特定的。

注意：如果未定义 <audio/> 元素，并且 graphics 元素设置为 vnc 或 sdl，则 libvirtd 或 virtqemud 进程将遵循以下环境变量：

- SDL_AUDIODRIVER

  有效值为 pulseaudio、esd、alsa 或 arts。

- QEMU_AUDIO_DRV

  有效值为 pa、none、alsa、coreaudio、jack、oss、pipewire、sdl、spice 或 wav。

#### 21.18.1 [无音频后端](https://www.libvirt.org/formatdomain.html#id100)

无音频后端是一个虚拟后端，不连接到任何主机音频框架。但它仍然允许像 VNC 这样的远程桌面服务器发送和接收音频。当在 QEMU 中启用 VNC 图形时，这是默认后端。

自 7.2.0 起，qemu

#### 21.18.2 [ALSA 音频后端](https://www.libvirt.org/formatdomain.html#id101)

alsa 音频类型使用 ALSA 主机音频设备框架。

<input> 和 <output> 元素上允许以下附加属性

- dev

  要连接后端的主机设备节点的路径。如果未指定，适用 hypervisor 特定的默认值。

```
<audio id="1" type="alsa">
  <input dev="/dev/dsp0"/>
  <output dev="/dev/dsp1"/>
</audio>
```

自 7.2.0 起，qemu

#### 21.18.3 [Coreaudio 音频后端](https://www.libvirt.org/formatdomain.html#id102)

coreaudio 音频后端委托给 macOS 上的 CoreAudio 主机音频框架进行输入和输出。

<input> 和 <output> 元素上允许以下附加属性

- bufferCount

  缓冲区数量。建议同时设置 bufferLength 属性。

```
<audio id="1" type="coreaudio">
  <input bufferCount="50"/>
  <output bufferCount="42"/>
</audio>
```

自 7.2.0 起，qemu

#### 21.18.4 [D-Bus 音频后端](https://www.libvirt.org/formatdomain.html#id103)

dbus 音频后端不连接到任何主机音频框架。当与 D-Bus 显示关联时，它导出 D-Bus 接口。

自 8.4.0 起，qemu

#### 21.18.5 [Jack 音频后端](https://www.libvirt.org/formatdomain.html#id104)

jack 音频后端委托给 Jack 守护进程进行音频输入和输出。

<input> 和 <output> 元素上允许以下附加属性

- serverName

  选择要连接的 Jack 服务器实例。

- clientName

  要标识的客户端名称。除非启用 exactName，否则服务器可能会修改此名称以确保唯一性

- connectPorts

  要监视和连接的 Jack 客户端端口名称的正则表达式。

- exactName

  使用请求的确切 clientName

```
<audio id="1" type="jack">
  <input serverName="fish" clientName="food" connectPorts="system:capture_[13]" exactName="yes"/>
  <output serverName="fish" clientName="food" connectPorts="system:playback_[13]" exactName="yes"/>
</audio>
```

自 7.2.0 起，qemu

#### 21.18.6 [OSS 音频后端](https://www.libvirt.org/formatdomain.html#id105)

oss 音频类型使用 OSS 主机音频设备框架。

<音频> 元素上允许以下附加属性

- tryMMap

  尝试使用 mmap 进行数据传输

- exclusive

  强制对主机设备的独占访问

- dspPolicy

  设置设备的定时策略，值在 -1 和 10 之间。较小的数字导致较低的延迟但较高的 CPU 使用率。负值请求使用片段模式。

<input> 和 <output> 元素上允许以下附加属性

- dev

  要连接后端的主机设备节点的路径。如果未指定，适用 hypervisor 特定的默认值。

- bufferCount

  缓冲区数量。建议同时设置 bufferLength 属性。

- tryPoll

  尝试使用轮询模式

```
<audio type='oss' id='1' tryMMap='yes' exclusive='yes' dspPolicy='4'>
  <input dev='/dev/dsp0' bufferCount='40' tryPoll='yes'/>
  <output dev='/dev/dsp0' bufferCount='40' tryPoll='yes'/>
</audio>
```

自 6.7.0 起，bhyve；自 7.2.0 起，qemu

#### 21.18.7 [PipeWire 音频后端](https://www.libvirt.org/formatdomain.html#id106)

pipewire 音频后端委托给 PipeWire 守护进程进行音频输入和输出。

<input/> 和 <output/> 元素上允许以下附加属性：

- name

  要使用的接收器/源名称

- streamName

  用于标识与 VM 关联的流的名称

- latency

  服务器目标的期望延迟（以微秒为单位）

```
<audio id="1" type="pipewire">
  <input name="fish" streamName="food" latency="100"/>
  <output name="fish" streamName="food" latency="200"/>
</audio>
```

可选地，可以通过 runtimeDir 属性指定 pipewire 守护进程套接字的路径（也称为 PIPEWIRE_RUNTIME_DIR）。当 qemu:///system 下的域想要使用会话 pipewire 守护进程时，这很有用，反之亦然。

```
<audio id="1" type="pipewire" runtimeDir='/run/user/1000'>
  <input name="fish" streamName="food" latency="100"/>
  <output name="fish" streamName="food" latency="200"/>
</audio>
```

自 9.10.0 起，qemu

#### 21.18.8 [PulseAudio 音频后端](https://www.libvirt.org/formatdomain.html#id107)

pulseaudio 音频后端委托给 PulseAudio 守护进程进行音频输入和输出。

<音频> 元素上允许以下附加属性

- serverName

  PulseAudio 服务器的主机名

<input> 和 <output> 元素上允许以下附加属性

- name

  要使用的接收器/源名称

- streamName

  用于标识与 VM 关联的流的名称

- latency

  服务器目标的期望延迟（以微秒为单位）

```
<audio id="1" type="pulseaudio" serverName="acme.example.org">
  <input name="fish" streamName="food" latency="100"/>
  <output name="fish" streamName="food" latency="200"/>
</audio>
```

自 7.2.0 起，qemu

#### 21.18.9 [SDL 音频后端](https://www.libvirt.org/formatdomain.html#id108)

sdl 音频后端委托给 SDL 库进行音频输入和输出。

<音频> 元素上允许以下附加属性

- driver

  SDL 音频驱动程序。name 属性指定 SDL 驱动程序名称，为 esd、alsa、arts、pulseaudio 之一。

<input> 和 <output> 元素上允许以下附加属性

- bufferCount

  缓冲区数量。建议同时设置 bufferLength 属性。

```
<audio type='sdl' id='1' driver='pulseaudio'>
  <input bufferCount='40'/>
  <output bufferCount='40'/>
</audio>
```

自 7.2.0 起，qemu

#### 21.18.10 [Spice 音频后端](https://www.libvirt.org/formatdomain.html#id109)

spice 音频后端类似于 none 后端，因为它不连接到任何主机音频框架。它专门允许 SPICE 服务器发送和接收音频。当在 QEMU 中启用 SPICE 图形时，这是默认后端。

```
<audio type='spice' id='1'/>
```

自 7.2.0 起，qemu

#### 21.18.11 [文件音频后端](https://www.libvirt.org/formatdomain.html#id110)

文件音频后端是一个仅输出驱动程序，将音频记录到文件。文件格式是实现定义的，在 QEMU 中默认为 WAV。

```
<audio id="1" type="file" path="audio.wav"/>
```

自 7.2.0 起，qemu

### 21.19 [看门狗设备](https://www.libvirt.org/formatdomain.html#id111)

可以通过 watchdog 元素向客户机添加虚拟硬件看门狗设备。自 0.7.3 起，仅 QEMU 和 KVM

看门狗设备需要客户机中额外的驱动程序和管理守护程序。仅在 libvirt 配置中启用看门狗本身不会做任何有用的事情。

自 0.8.0 起，当看门狗触发时，可以使用事件 ID VIR_DOMAIN_EVENT_ID_WATCHDOG 获得通知。

拥有多个看门狗通常不是很常见，但请注意，这可能会发生，例如，当另一个设备的一部分添加隐式看门狗设备时。例如，iTCO 看门狗是 ich9 南桥的一部分，用于 q35 机器类型。自 9.1.0 起

```
...
<devices>
  <watchdog model='i6300esb'/>
</devices>
...
  ...
  <devices>
    <watchdog model='i6300esb' action='poweroff'/>
  </devices>
</domain>
```

- model

  必需的 model 属性指定模拟什么真实的看门狗设备。有效值特定于底层 hypervisor。QEMU 和 KVM 支持：'itco' - q35 机器类型默认包含 自 9.1.0 起 'i6300esb' - 推荐设备，模拟 PCI Intel 6300ESB 'ib700' - 模拟 ISA iBase IB700 'diag288' - 模拟 S390 DIAG288 设备 自 1.2.17 起

- action

  可选的 action 属性描述看门狗超时时要采取的操作。有效值特定于底层 hypervisor。QEMU 和 KVM 支持：'reset' - 默认，强制重置客户机 'shutdown' - 优雅关闭客户机（不推荐） 'poweroff' - 强制关闭客户机 'pause' - 暂停客户机 'none' - 不执行任何操作 'dump' - 自动转储客户机，请注意转储后客户机将被恢复 自 0.8.7 起 'inject-nmi' - 向客户机注入不可屏蔽中断 自 1.2.17 起 注意 1：'shutdown' 操作要求客户机对 ACPI 信号做出响应。在看门狗已超时的情况下，客户机通常无法响应 ACPI 信号。因此，不建议使用 'shutdown'。注意 2：保存转储文件的目录可以通过 /etc/libvirt/qemu.conf 中的 auto_dump_path 配置。

### 21.20 [内存气球设备](https://www.libvirt.org/formatdomain.html#id112)

所有 Xen 和 KVM/QEMU 客户机都添加了虚拟内存气球设备。它将显示为 memballoon 元素。它会在适当的时候自动添加，因此除非需要分配特定的 PCI 插槽，否则无需在客户机 XML 中显式添加此元素。自 0.8.3 起，仅 Xen、QEMU 和 KVM 此外，自 0.8.4 起，如果需要显式禁用 memballoon 设备，可以使用 model='none'。

示例：KVM 自动添加的设备

```
...
<devices>
  <memballoon model='virtio'/>
</devices>
...
```

示例：手动添加的设备，请求静态 PCI 插槽 2

```
  ...
  <devices>
    <memballoon model='virtio'>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x02' function='0x0'/>
      <stats period='10'/>
      <driver iommu='on' ats='on'/>
    </memballoon>
  </devices>
</domain>
```

- model

  必需的 model 属性指定提供什么类型的气球设备。有效值特定于虚拟化平台 'virtio' - QEMU/KVM 的默认值 'virtio-transitional' 自 5.2.0 起 'virtio-non-transitional' 自 5.2.0 起 'xen' - Xen 的默认值 有关更多详细信息，请参阅 [virtio 设备模型](https://www.libvirt.org/formatdomain.html#virtio-device-models)。

- autodeflate

  可选的 autodeflate 属性允许启用/禁用（值分别为 "on"/"off"）QEMU virtio 内存气球在客户机进程被内存不足杀手杀死之前的最后时刻释放一些内存的能力。自 1.3.1 起，仅 QEMU 和 KVM

- freePageReporting

  可选的 freePageReporting 属性允许启用/禁用（分别为 "on"/"off"）QEMU virtio 内存气球将未使用的页面返回给 hypervisor 以供其他客户机或进程使用的能力。请注意，尽管其名称，它对 virDomainMemoryStats() 和/或 virsh dommemstat 报告的可用内存没有影响。自 6.9.0 起，仅 QEMU 和 KVM

- period

  可选的 period 允许 QEMU virtio 内存气球驱动程序通过 virsh dommemstat [domain] 命令提供统计信息。默认情况下，未启用收集。要启用，请使用 virsh dommemstat [domain] --period [number] 命令或 virsh edit 命令将选项添加到 XML 定义。virsh dommemstat 将接受 --live、--current 或 --config 选项。如果未提供选项，对运行中域的更改将仅应用于活动客户机。如果 QEMU 驱动程序版本不够，尝试设置 period 将失败。较大的值（例如多年）可能会被忽略。自 1.1.1 起，需要 QEMU 1.5

- driver

  对于 model virtio memballoon，也可以设置 [Virtio 相关选项](https://www.libvirt.org/formatdomain.html#virtio-related-options)。（自 3.5.0 起）

### 21.21 [随机数生成器设备](https://www.libvirt.org/formatdomain.html#id113)

虚拟随机数生成器设备允许主机将熵传递给客户机操作系统。自 1.0.3 起

示例：RNG 设备的使用：

```
...
<devices>
  <rng model='virtio'>
    <rate period="2000" bytes="1234"/>
    <backend model='random'>/dev/random</backend>
    <!-- 或 -->
    <backend model='egd' type='udp'>
      <source mode='bind' service='1234'/>
      <source mode='connect' host='1.2.3.4' service='1234'/>
    </backend>
    <!-- 或 -->
    <backend model='builtin'/>
  </rng>
</devices>
...
```

- model

  必需的 model 属性指定提供什么类型的 RNG 设备。有效值特定于虚拟化平台：'virtio' - 由 qemu 和 virtio-rng 内核模块支持 'virtio-transitional' 自 5.2.0 起 'virtio-non-transitional' 自 5.2.0 起 有关更多详细信息，请参阅 [virtio 设备模型](https://www.libvirt.org/formatdomain.html#virtio-device-models)。

- rate

  可选的 rate 元素允许限制从源消耗熵的速率。必需属性 bytes 指定每个周期允许消耗多少字节。可选的 period 属性指定周期的持续时间（以毫秒为单位）；如果省略，周期为 1000 毫秒（1 秒）。自 1.0.4 起

- backend

  backend 元素指定用于域的熵源。源模型使用 model 属性配置。支持的源模型有：random 此后端类型需要非阻塞字符设备作为输入。文件名指定为 backend 元素的内容。自 1.3.4 起，接受任何路径。在此之前，只有 /dev/random 和 /dev/hwrng 是接受的路径。当未指定文件名时，使用 hypervisor 默认值。对于 QEMU，默认值是 /dev/random。但是，推荐的熵源是 /dev/urandom（因为它没有 /dev/random 的限制）。egd 此后端使用 EGD 协议连接到源。源指定为字符设备。有关更多信息，请参阅 [主机接口](https://www.libvirt.org/formatdomain.html#host-interface)。builtin 此后端使用 qemu 内置的随机生成器，它使用 getrandom() 系统调用作为熵源。（自 6.1.0 和 QEMU 4.2 起）

- driver

  子元素 driver 可用于调整设备：virtio 选项 [Virtio 相关选项](https://www.libvirt.org/formatdomain.html#virtio-related-options) 也可以设置。（自 3.5.0 起）

### 21.22 [TPM 设备](https://www.libvirt.org/formatdomain.html#id114)

TPM 设备使 QEMU 客户机能够访问 TPM 功能。TPM 设备可以是 TPM 1.2 或 TPM 2.0。

TPM 透传设备类型为一个 QEMU 客户机提供对主机 TPM 的访问。在 QEMU 客户机启动时，不得有其他软件使用 TPM 设备（通常是 /dev/tpm0）。'passthrough' 自 1.0.5 起

示例：TPM 透传设备的使用

```
...
<devices>
  <tpm model='tpm-tis'>
    <backend type='passthrough'>
      <device path='/dev/tpm0'/>
    </backend>
  </tpm>
</devices>
...
```

仿真器设备类型为每个 VM 提供访问 TPM 仿真器的权限，提供 TPM 功能。QEMU 通过 Unix 套接字与其通信。使用仿真器设备类型，每个客户机都获得自己的专用 TPM。自 4.5.0 起

自 5.6.0 起，可以通过提供 encryption 元素来加密 TPM 仿真器的状态。

示例：TPM 仿真器的使用

```
...
<devices>
  <tpm model='tpm-tis'>
    <backend type='emulator' version='2.0' debug='5'>
      <encryption secret='6dd3e4a5-1d76-44ce-961f-f119f5aad935'/>
      <active_pcr_banks>
          <sha256/>
      </active_pcr_banks>
      <profile source='local:restricted' removeDisabled='check' name='custom:restricted'/>
    </backend>
  </tpm>
</devices>
...
```

示例：外部 TPM 仿真器的使用 自 9.0.0 起

```
...
<devices>
  <tpm model='tpm-tis'>
    <backend type='external'>
      <source type='unix' mode='connect' path='/tmp/path.sock'/>
    </backend>
  </tpm>
</devices>
...
```

- model

  model 属性指定 QEMU 为客户机提供什么设备模型。如果未提供模型名称，对于非 PPC64 架构，将自动选择 tpm-tis。自 4.4.0 起，另一个可用选择是 tpm-crb，它应仅在后端设备是 TPM 2.0 时使用。自 6.1.0 起，PPC64 上的 pSeries 客户机受支持，默认值为 tpm-spapr。自 6.5.0 起，为 pSeries 客户机添加了一个名为 spapr-tpm-proxy 的新模型。此模型仅适用于 passthrough 后端。它创建一个 TPM 代理设备，与主机中现有的 TPM 资源管理器通信，例如 /dev/tpmrm0，使客户机能够在 Ultravisor 的帮助下以安全虚拟机模式运行。向 pSeries 客户机添加 TPM 代理不会带来安全好处，除非客户机在具有 Ultravisor 和 TPM 资源管理器的 PPC64 主机上运行。每个客户机只允许一个 TPM 代理设备，但 TPM 代理设备可以与其他 TPM 设备一起添加。

- backend

  backend 元素指定 TPM 设备的类型。支持以下类型：passthrough 使用主机的 TPM 或 TPM 资源管理器设备。此后端类型需要对主机上的 TPM 设备的独占访问。此类设备的示例是 /dev/tpm0。完全限定的文件名由 source 元素的 path 属性指定。如果未指定文件名，则自动使用 /dev/tpm0。自 6.5.0 起，当选择 spapr-tpm-proxy 模型时，指定的文件名应为 TPM 资源管理器设备，例如 /dev/tpmrm0。emulator 对于此后端类型，主机必须安装 'swtpm' TPM 仿真器。Libvirt 将为每个请求访问它的 QEMU 客户机自动启动独立的 TPM 仿真器。10.6.0 起，debug 参数可用于在仿真器后端启用日志记录，并接受非零整数值。external 对于此后端，libvirt 期望 TPM 仿真器在外部启动。仿真器监听的 unix 套接字的路径通过 source 元素传递。其他后端子元素在此情况下不适用，因为它们由仿真器命令行控制。

- version

  version 属性指示 TPM 的版本。此属性仅适用于仿真器后端。支持以下版本：'1.2'：创建 TPM 1.2 '2.0'：创建 TPM 2.0 使用的默认版本取决于 hypervisor、客户机架构、TPM 模型和后端的组合。

- source

  对于仿真器后端，source 元素指定 TPM 状态存储的位置。自 v10.10.0 起 对于外部后端，它指定外部启动的 TPM 仿真器的套接字。自 v9.0.0 起 此元素不适用于 passthrough 后端。指定后，用户有责任防止文件被多个 VM 或仿真器使用（swtpm 也会使用咨询锁定）。如果未指定，存储配置由 libvirt 决定。此元素要求安装 swtpm v0.7 或更高版本。支持以下属性：type 对于外部后端，仅支持 type unix。对于仿真器后端，可以提供 file 以利用单个文件或块设备存储 TPM 状态，或 dir 用于存储文件的目录。mode unix 套接字的连接模式。仅支持 connect。可以省略。path TPM 状态存储的路径，或 unix 套接字。

- persistent_state

  persistent_state 属性指示当瞬态域断电或未定义时，'swtpm' TPM 状态是否保留。此选项可用于保留 TPM 状态。默认值为 no。此属性仅适用于仿真器后端。接受的值为 yes 和 no。自 7.0.0 起

- active_pcr_banks

  active_pcr_banks 节点用于定义要激活 TPM 2.0 的哪些 PCR 库。有效名称例如 sha1、sha256、sha384 和 sha512。如果提供此节点，PCR 库集在 VM 每次启动前都会被激活，此步骤会在 swtpm 的日志中记录。如果此节点被删除或省略，libvirt 将在 VM 启动时不修改活动 PCR 库，而是将它们保持在最后配置的状态。此属性要求安装 swtpm_setup v0.7 或更高版本，否则可能没有任何效果。PCR 库的选择仅适用于仿真器后端。自 7.10.0 起

- profile

  profile 节点用于为 source 属性中给定的 TPM 2.0 设置配置文件。此属性描述配置文件存储的文件名，例如 'local:restricted' 描述本地创建的名为 'restricted.json' 的配置文件，该文件位于 swtpm_setup.conf 的 local_profiles_dir 指向的目录中。此配置文件将在 TPM 初始创建时设置，之后配置文件不能再更改。一旦设置了配置文件，name 属性将使用配置文件的 JSON 描述中的名称更新，例如 'custom:restricted'。如果未提供配置文件，swtpm 将使用最新的内置 'default' 配置文件或 swtpm_setup.conf 中设置的默认配置文件。否则，swtpm_setup 将在可配置的本地目录中，然后在发行版目录中搜索具有给定名称并附加 .json 后缀的配置文件。如果在任一目录中都找不到，它将尝试使用内置的配置文件。内置的 'null' 配置文件提供与 libtpms v0.9 的向后兼容性，但也限制用户仅使用 libtpms v0.9 时可用的 TPM 功能。内置的 'custom' 配置文件，或名称前缀为 'custom:' 的配置文件，是用户可以修改的唯一配置文件，其中 removeDisabled 属性有任何效果。当主机在 FIPS 模式下运行，因此某些加密算法（camellia、tdes、无填充 RSA 加密、1024 位 RSA 密钥等）被禁用时，此属性特别有用。当它设置为 check（推荐）时，只有当前被禁用的算法会自动从 'custom' 配置文件中删除，而当它设置为 fips-host 时，所有可能被禁用的算法都会被删除。自 10.10.0 起，发行版提供的 TPM 配置文件可以使用 'distro:' 前缀引用。本地创建的 TPM 配置文件可以使用 'local:' 前缀引用。有关 TPM 配置文件的更多信息，请参阅手册页。

- encryption

  encryption 元素允许加密 TPM 仿真器的状态。secret 必须引用一个包含从中派生加密密钥的密码短语的 secret 对象。

### 21.23 [NVRAM 设备](https://www.libvirt.org/formatdomain.html#id115)

nvram 设备始终添加到 PPC64 上的 pSeries 客户机，并且其地址允许更改。提供元素 nvram（仅对 pSeries 客户机有效，自 1.0.5 起）以启用地址设置。

示例：NVRAM 配置的使用

```
...
<devices>
  <nvram>
    <address type='spapr-vio' reg='0x00003000'/>
  </nvram>
</devices>
...
```

- spapr-vio

  VIO 设备地址类型，仅对 PPC64 有效。

- reg

  设备地址

### 21.24 [panic 设备](https://www.libvirt.org/formatdomain.html#id116)

panic 设备使 libvirt 能够接收来自 QEMU 客户机的 panic 通知。自 1.2.1 起，仅 QEMU 和 KVM

此功能始终为以下情况启用：

- pSeries 客户机，因为它由客户机固件实现
- S390 客户机，因为它是 S390 架构的组成部分

对于上面列出的客户机类型，libvirt 自动向域 XML 添加 panic 元素。

示例：panic 配置的使用

```
...
<devices>
  <panic model='hyperv'/>
  <panic model='isa'>
    <address type='isa' iobase='0x505'/>
  </panic>
</devices>
...
```

- model

  可选的 model 属性指定提供什么类型的 panic 设备。此属性缺失时使用的 panic 模型取决于 hypervisor 和客户机架构。'isa' - 用于 ISA pvpanic 设备 'pseries' - 默认为 pSeries 客户机，且仅对其有效。'hyperv' - 用于 Hyper-V 崩溃 CPU 功能。自 1.3.0 起，仅 QEMU 和 KVM 's390' - S390 客户机的默认值。自 1.3.5 起 'pvpanic' - 用于 PCI pvpanic 设备 自 9.1.0 起，仅 QEMU

- address

  panic 的地址。默认 ioport 为 0x505。大多数用户不需要指定地址，对于 s390、pseries 和 hyperv 模型完全禁止这样做。

### 21.25 [共享内存设备](https://www.libvirt.org/formatdomain.html#id117)

共享内存设备允许在不同虚拟机和主机之间共享内存区域。自 1.2.10 起，仅 QEMU 和 KVM

```
...
<devices>
  <shmem name='my_shmem0' role='peer'>
    <model type='ivshmem-plain'/>
    <size unit='M'>4</size>
  </shmem>
  <shmem name='shmem_server'>
    <model type='ivshmem-doorbell'/>
    <size unit='M'>2</size>
    <server path='/tmp/socket-shmem'/>
    <msi vectors='32' ioeventfd='on'/>
  </shmem>
</devices>
...
```

- shmem

  shmem 元素有一个强制属性 name，用于标识共享内存。此属性不能是目录特定的 . 或 ..，也不能包含路径分隔符 /。可选的 role（自 6.6.0 起）属性指定共享内存是否可迁移。值可以是 "master" 或 "peer"，前者意味着在迁移时，共享内存中的数据会随域一起迁移。每个共享内存对象应该只有一个 "master"。具有 "peer" 角色的迁移被禁用。如果需要迁移此类域，需要在迁移前拔出 shmem 设备，并在成功迁移后在目标端插入。如果未指定 role，使用 hypervisor 默认值。此属性目前仅适用于模型类型 ivshmem-plain 和 ivshmem-doorbell。

- model

  可选元素 model 的属性 type 指定提供 shmem 设备的底层设备模型。当前支持的模型有 ivshmem（支持服务器和无服务器 shmem，但被较新的 QEMU 弃用，转而使用 -plain 和 -doorbell 变体）、ivshmem-plain（仅用于无服务器 shmem）和 ivshmem-doorbell（仅用于带服务器的 shmem）。

- size

  可选的 size 元素指定共享内存的大小。这必须是 2 的幂且大于或等于 1 MiB。

- server

  可选的 server 元素可用于配置设备应该连接的服务器套接字。可选的 path 属性指定 unix 套接字的绝对路径，默认为 /var/lib/libvirt/shmem/$shmem-$name-sock。

- msi

  可选的 msi 元素启用/禁用（值分别为 "on"/"off"）MSI 中断。此选项目前只能与 server 元素一起使用。vectors 属性可用于指定中断向量的数量。ioeventd 属性启用/禁用（值分别为 "on"/"off"）ioeventfd。

### 21.26 [内存设备](https://www.libvirt.org/formatdomain.html#id118)

除了分配给客户机的初始内存外，内存设备还允许以内存模块的形式向客户机分配额外的内存。内存设备可以根据客户机的内存资源需求进行热插拔或热卸载。一些 hypervisor 可能要求为客户机配置 NUMA。

示例：内存设备的使用

```xml
...
<devices>
  <memory model='dimm' access='private' discard='yes'>
```
