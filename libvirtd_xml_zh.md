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

  cpu 元素是描述客户机 CPU 要求的主要容器。其 match 属性指定提供给客户机的虚拟 CPU 与这些要求的匹配程度。自 0.7.6 起，如果 topology 是 cpu 中的唯一元素，则可以省略 match 属性。match 属性的可能值为：minimum 指定的 CPU 模型和功能描述了最小请求的 CPU。如果使用当前主机上的请求 hypervisor 可能，将向客户机提供更好的 CPU。这是一种受限的 host-model 模式；如果提供的虚拟 CPU 不满足要求，将不会创建域。exact 提供给客户机的虚拟 CPU 应与规范完全匹配。如果不支持这样的 CPU，libvirt 将拒绝启动域。strict 除非主机 CPU 与规范完全匹配，否则不会创建域。这在实践中不是很有用，应该只在有真正原因时使用。 自 0.8.5 起，match 属性可以省略，默认值为 exact。有时，hypervisor 无法创建与 libvirt 传递的规范完全匹配的虚拟 CPU。自 3.2.0 起，可以使用可选的 check 属性来请求特定的方式来检查虚拟 CPU 是否与规范匹配。启动域时通常可以安全地省略此属性，并坚持使用默认值。一旦域启动，libvirt 将自动将 check 属性更改为最佳支持的值，以确保虚拟 CPU 在域迁移到另一台主机时不会改变。可以使用以下值：none Libvirt 不进行检查，由 hypervisor 负责拒绝启动域，如果它无法提供请求的 CPU。对于 QEMU，这意味着根本不进行检查，因为 QEMU 的默认行为是发出警告，但仍然启动域。partial Libvirt 将在启动域之前检查客户机 CPU 规范，但其余部分由 hypervisor 处理。full Libvirt 将在启动域之前完全检查客户机 CPU 规范。

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
