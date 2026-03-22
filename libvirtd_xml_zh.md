# 域 XML 格式

[toc]

本节描述用于表示域的 XML 格式，根据运行的域类型和用于启动它们的选项，格式会有所不同。有关特定于 hypervisor 的详细信息，请参考 [驱动程序文档](https://www.libvirt.org/drivers.html)

# [元素和属性概述](https://www.libvirt.org/formatdomain.html#id1)

所有虚拟机所需的根元素名为 domain。它有两个属性，type 指定用于运行域的 hypervisor。允许的值特定于驱动程序，但包括 "xen"、"kvm"、"hvf"（自 8.1.0 和 QEMU 2.12 起）、"qemu" 和 "lxc"。第二个属性是 id，它是运行中的客户机的唯一整数标识符。非活动机器没有 id 值。

## 1 [通用元数据](https://www.libvirt.org/formatdomain.html#id2)

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

  name 元素的内容为虚拟机提供一个简短名称。此名称应仅由字母数字字符组成，并且在单个主机范围内必须是唯一的。它通常用于形成用于存储持久配置文件的文件名。自 0.0.1 起

- uuid

  uuid 元素的内容为虚拟机提供全局唯一标识符。格式必须符合 RFC 4122，例如 3e3fce45-4f53-4fa7-bb32-11f34168b82b。如果在定义/创建新机器时省略，将生成随机 UUID。自 0.0.1 起 自 0.8.7 起，也可以通过 [SMBIOS 系统信息](https://www.libvirt.org/formatdomain.html#smbios-system-information) 规范提供 UUID。

- hwuuid

  可选的 hwuuid 元素可用于提供替代 UUID，用于从上面的域 uuid 标识虚拟机。使用 hwuuid 元素与通过 [SMBIOS 系统信息](https://www.libvirt.org/formatdomain.html#smbios-system-information) 规范简单提供替代 UUID 的区别在于，hwuuid 会影响向客户机公开 UUID 的所有设备。自 11.7.0 起仅 QEMU/KVM

- genid

  自 4.4.0 起，genid 元素可用于添加虚拟机生成 ID，该 ID 使用与 uuid 相同的格式公开 128 位、加密随机的整数值标识符，称为全局唯一标识符 (GUID)。该值用于帮助通知客户机操作系统虚拟机何时重新执行已经执行过的操作，例如：VM 开始执行快照 VM 从备份中恢复 VM 在灾难恢复环境中故障转移 VM 被导入、复制或克隆 客户机操作系统会注意到这一变化，然后能够做出适当的反应，例如将其分布式数据库的副本标记为脏，重新初始化其随机数生成器等。libvirt XML 解析器将接受提供的 GUID 值或仅接受 <genid/>，在这种情况下将生成 GUID 并保存在 XML 中。对于上述转换，libvirt 将在重新执行之前更改 GUID。

- title

  可选元素 title 为域的简短描述提供空间。title 不应包含任何换行符。自 0.9.10 起。

- description

  description 元素的内容为虚拟机提供人类可读的描述。这些数据不会被 libvirt 以任何方式使用，它可以包含用户想要的任何信息。自 0.7.2 起

- metadata

  metadata 节点可由应用程序用于以 XML 节点/树的形式存储自定义元数据。应用程序必须在其 XML 节点/树上使用自定义命名空间，每个命名空间只有一个顶级元素（如果应用程序需要结构，它们应该在其命名空间元素下有子元素）。自 0.9.10 起

## 2 [操作系统启动](https://www.libvirt.org/formatdomain.html#id3)

有多种不同的方式来启动虚拟机，每种方式都有其优缺点。

### 2.1 [客户机固件](https://www.libvirt.org/formatdomain.html#id4)

通过客户机固件启动适用于支持完全虚拟化的 hypervisor。在这种情况下，固件具有启动顺序优先级（软盘、硬盘、CD-ROM、网络），决定从哪里获取/找到启动映像。

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

  firmware 属性允许管理应用程序自动填充 <loader/> 和 <nvram/> 或 <varstore/> 元素，并可能启用所选固件所需的某些功能。接受的值为 bios 和 efi。选择过程会扫描指定位置中描述已安装固件映像的文件，并使用满足域要求的最特定文件。偏好顺序（从通用到最特定）的位置是：/usr/share/qemu/firmware /etc/qemu/firmware $XDG_CONFIG_HOME/qemu/firmware 有关更多信息，请参考 QEMU 存储库中 docs/interop/firmware.json 中描述的固件元数据规范。普通用户不需要费心。自 5.2.0 起（仅 QEMU 和 KVM）对于 VMware 客户机，当客户机使用 UEFI 时，它设置为 efi，当使用 BIOS 时，它不设置。自 5.3.0 起（VMware ESX 和 Workstation/Player）

- type

  type 元素的内容指定要在虚拟机中启动的操作系统类型。hvm 表示该操作系统设计为在裸机上运行，因此需要完全虚拟化。linux（命名不当！）指的是支持 Xen 3  hypervisor 客户机 ABI 的操作系统。还有两个可选属性，arch 指定要虚拟化的 CPU 架构，machine 指机器类型。[功能 XML](https://www.libvirt.org/formatcaps.html) 提供了这些允许值的详细信息。如果省略 arch，则对于大多数 hypervisor 驱动程序，将选择主机本机架构。但是，对于测试、ESX 和 VMWare hypervisor 驱动程序，即使在 x86_64 主机上，也会始终选择 i686 架构。自 0.0.1 起

- firmware

  自 7.2.0 起仅 QEMU/KVM 使用固件自动选择时，固件中启用了不同的功能。功能列表可用于限制应为 VM 自动选择的固件。可以使用零个或多个 feature 元素指定功能列表。Libvirt 在选择固件时将只考虑列出的功能并忽略其余功能。feature 强制属性列表：enabled（接受的值为 yes 和 no）用于告诉 libvirt 在自动选择的固件中是否必须启用该功能 name 功能的名称，功能列表：enrolled-keys 所选 nvram 模板是否已注册默认证书。具有 Secure Boot 功能但没有注册密钥的固件也会成功引导未签名的二进制文件。仅对具有 Secure Boot 功能的固件有效。secure-boot 固件是否实现 UEFI Secure boot 功能。

- loader

  可选的 loader 标签引用固件 blob，由绝对路径指定，用于辅助域创建过程。它被 Xen 完全虚拟化域使用，以及为 QEMU/KVM 域设置 QEMU BIOS 文件路径。Xen 自 0.1.0 起，QEMU/KVM 自 0.9.12 起 然后，自 1.2.8 起，该元素可以有两个可选属性：readonly（接受的值为 yes 和 no）以反映映像应该是可写还是只读。第二个属性 type 接受值 rom 和 pflash。它告诉 hypervisor 文件应该映射到客户机内存中的哪个位置。例如，如果 loader 路径指向 UEFI 映像，type 应该是 pflash。此外，一些固件可能实现 Secure boot 功能。属性 secure 可用于告诉 hypervisor 固件能够实现 Secure Boot 功能。它不能用于在固件中启用或禁用功能本身。自 2.1.0 起。如果 loader 标记为只读，则对于 UEFI，假定将有可写的 NVRAM 可用。但是，在某些情况下，可能希望 loader 在没有任何 NVRAM 的情况下运行，在关闭时丢弃任何配置更改。stateless 标志（自 8.6.0 起）可用于控制此行为，当设置为 yes 时，永远不会创建 NVRAM。启用固件自动选择时，format 属性可用于告诉 libvirt 只考虑特定格式的固件构建。支持的值为 raw 和 qcow2。自 9.2.0 起（仅 QEMU）

- nvram

  一些 UEFI 固件可能希望使用非易失性内存来存储一些变量。在主机中，这表示为文件，文件的绝对路径存储在此元素中。此外，当域启动时，libvirt 会复制由固件自动选择过程选择或在 qemu.conf 中定义的所谓主 NVRAM 存储文件。如果需要，可以使用 template 属性覆盖自动选择的 NVRAM 模板，并使用 templateFormat 指定模板文件的格式（当前支持 raw 和 qcow2）。使用固件自动选择时，templateFormat 字段反映所选模板的格式。自 10.10.0 起（仅 QEMU）注意，对于瞬态域，如果 NVRAM 文件由 libvirt 创建，它会被留下，管理应用程序有责任保存和删除文件（如果需要持久化）。自 1.2.8 起 自 8.5.0 起，该元素可以具有 type 属性（接受值 file、block 和 network），在这种情况下，NVRAM 存储由 <source> 子元素描述，语法与磁盘的 source 相同。请参阅 [硬盘、软盘、CD-ROM](https://www.libvirt.org/formatdomain.html#hard-drives-floppy-disks-cdroms)。对于基于块的 NVRAM 映像，可能需要确保块设备具有基于 hypervisor 期望的正确客户机可见大小。这可能需要使用允许任意磁盘大小的非 raw 格式映像。**注意：** 网络支持的 NVRAM 变量不是从模板实例化的，用户有责任提供有效的 NVRAM 映像。此元素支持 format 属性，该属性指定 NVRAM 映像的格式。自 9.2.0 起（仅 QEMU）请注意，如果格式与 templateFormat 不同，hypervisor 可能不支持 NVRAM 的自动填充，或者可能只支持特定格式。如果 loader 标记为 stateless，则提供此元素是无效的。

- varstore

  这与上面描述的 <nvram/> 元素的工作方式非常相似，不同之处在于变量存储由 uefi-vars QEMU 设备处理，而不是由 pflash 设备支持。自 12.1.0 起（仅 QEMU）path 属性包含存储变量的域特定文件的路径，而 template 属性指向可以从中（重新）生成域特定文件的模板。假设存在必要的 JSON 固件描述符文件，两个属性都将由 libvirt 自动填充。在非 x86 架构（如 aarch64）上使用 <varstore/> 而不是 <nvram/> 特别有用，因为它是使 Secure Boot 工作的唯一方法。它也可以在 x86 上使用，这样做将使 UEFI 认证变量免受篡改，而不需要使用 SMM 仿真。

- boot

  dev 属性取 "fd"、"hd"、"cdrom" 或 "network" 之一，用于指定要考虑的下一个启动设备。boot 元素可以重复多次，以设置要依次尝试的启动设备的优先级列表。相同类型的多个设备根据其目标排序，同时保留总线的顺序。定义域后，libvirt（通过 virDomainGetXMLDesc）返回的其 XML 配置按排序顺序列出设备。排序后，第一个设备被标记为可启动。因此，例如，配置为从 "hd" 启动并分配了 vdb、hda、vda 和 hdc 磁盘的域将从 vda 启动（排序后的列表是 vda、vdb、hda、hdc）。具有 hdc、vda、vdb 和 hda 磁盘的类似域将从 hda 启动（排序后的磁盘是：hda、hdc、vda、vdb）。这可能很难按预期方式配置，这就是为什么引入了每设备启动元素（请参阅下面的 [硬盘、软盘、CD-ROM](https://www.libvirt.org/formatdomain.html#hard-drives-floppy-disks-cdroms)、[网络接口](https://www.libvirt.org/formatdomain.html#network-interfaces) 和 [主机设备分配](https://www.libvirt.org/formatdomain.html#host-device-assignment) 部分），它们是提供对启动顺序完全控制的首选方式。boot 元素和每设备启动元素是互斥的。自 0.1.3 起，每设备启动自 0.8.8 起

- smbios

  如何填充客户机中可见的 SMBIOS 信息。必须指定 mode 属性，它是 "emulate"（让 hypervisor 生成所有值）、"host"（从主机的 SMBIOS 值复制 Block 0 和 Block 1 的所有内容，除了 UUID；[virConnectGetSysinfo](https://www.libvirt.org/html/libvirt-libvirt-host.html#virConnectGetSysinfo) 调用可用于查看复制了哪些值）或 "sysinfo"（使用 [SMBIOS 系统信息](https://www.libvirt.org/formatdomain.html#smbios-system-information) 元素中的值）。如果未指定，则使用 hypervisor 默认值。自 0.8.7 起

到目前为止，BIOS/UEFI 配置旋钮足够通用，可以由大多数（如果不是全部）固件实现。但是，从现在开始，并非每个设置都对所有固件有意义。例如，rebootTimeout 对 UEFI 没有意义，useserial 可能无法与不在串行线上产生任何输出的 BIOS 固件一起使用，等等。此外，固件通常不会导出其功能供 libvirt（或用户）检查。而且它们的功能集可能会随着每个新版本而改变。因此，建议用户在生产环境中依赖之前尝试他们使用的设置。

- bootmenu

  是否在客户机启动时启用交互式启动菜单提示。enable 属性可以是 "yes" 或 "no"。如果未指定，则使用 hypervisor 默认值。自 0.8.3 起 附加属性 timeout 采用启动菜单应等待直到超时的毫秒数。允许的值是范围 [0, 65535] 内的数字，除非 enable 设置为 "yes"，否则将被忽略。自 1.2.8 起

- bios

  此元素具有 useserial 属性，可能的值为 yes 或 no。它启用或禁用串行图形适配器，允许用户在串行端口上查看 BIOS 消息。因此，需要定义 [串行端口](https://www.libvirt.org/formatdomain.html#serial-port)。自 0.9.4 起。rebootTimeout 属性（自 0.10.2 起（仅 QEMU））控制在启动失败的情况下（根据 BIOS）客户机是否以及多久后应再次开始启动。该值以毫秒为单位，最大值为 65535，特殊值 -1 禁用重启。

### 2.2 [主机引导加载程序](https://www.libvirt.org/formatdomain.html#id5)

采用半虚拟化的 hypervisor 通常不模拟 BIOS，而是由主机负责启动操作系统引导。这可能会使用主机中的伪引导加载程序来提供选择客户机内核的接口。一个例子是 Xen 的 pygrub。Bhyve hypervisor 也使用主机引导加载程序，无论是 bhyveload 还是 grub-bhyve。

```
...
<bootloader>/usr/bin/pygrub</bootloader>
<bootloader_args>--append single</bootloader_args>
...
```

- bootloader

  bootloader 元素的内容提供了主机 OS 中引导加载程序可执行文件的完全限定路径。将运行此引导加载程序来选择要引导的内核。引导加载程序的所需输出取决于所使用的 hypervisor。自 0.1.0 起

- bootloader_args

  可选的 bootloader_args 元素允许将命令行参数传递给引导加载程序。自 0.2.3 起

### 2.3 [直接内核引导](https://www.libvirt.org/formatdomain.html#id6)

安装新的客户机 OS 时，通常直接从主机 OS 中存储的内核和 initrd 引导很有用，允许将命令行参数直接传递给安装程序。此功能通常可用于半虚拟化和完全虚拟化的客户机。

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

  此元素与前面在 [客户机固件](https://www.libvirt.org/formatdomain.html#guest-firmware) 部分中描述的语义相同。

- loader

  此元素与前面在 [客户机固件](https://www.libvirt.org/formatdomain.html#guest-firmware) 部分中描述的语义相同。

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

使用基于容器的虚拟化引导域时，需要使用 init 元素指定 init 二进制文件的路径，而不是内核/引导映像。默认情况下，它将在没有参数的情况下启动。要指定初始 argv，请使用 initarg 元素，根据需要重复多次。如果设置了 cmdline 元素，它将用于提供相当于 /proc/cmdline 的内容，但不会影响 init argv。

要设置环境变量，请使用 initenv 元素，每个变量一个。

要为 init 设置自定义工作目录，请使用 initdir 元素。

要以给定用户或组运行 init 命令，请分别使用 inituser 或 initgroup 元素。两个元素都可以提供用户（或组）ID 或名称。在用户或组 ID 前加上 + 将强制将其视为数值。没有此前缀，它将首先尝试作为用户名或组名。

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

  容器中允许映射到主机用户的用户数量。

```
<idmap>
  <uid start='0' target='1000' count='10'/>
  <gid start='0' target='1000' count='10'/>
</idmap>
```

### 2.5 [通用元素配置](https://www.libvirt.org/formatdomain.html#id8)

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

  table 元素包含 ACPI 表的完全限定路径，type 属性指定文件中必须存在的数据：raw：单个 ACPI 表，带有头和数据，ACPI 签名从头部自动检测（自 11.2.0 起（QEMU））。rawset：多个 ACPI 表的连接，带有头和数据，每个都有任何 ACPI 签名，从头部自动检测（自 11.2.0 起（Xen））。slic：单个 ACPI 表，带有头和数据，提供软件许可信息。头部中的 ACPI 表签名将被强制为 SLIC（自 1.3.5 起（QEMU），自 5.9.0 起（Xen）被错误解释为 rawset）。msdm：单个 ACPI 表，带有头和数据，提供 Microsoft 数据管理信息。头部中的 ACPI 表签名将被强制为 MSDM（自 11.2.0 起（QEMU））。每种类型只能使用一次，除了 raw 可以出现多次。

## 3 [SMBIOS 系统信息](https://www.libvirt.org/formatdomain.html#id9)

一些 hypervisor 允许控制向客户机呈现的系统信息（例如，SMBIOS 字段可以由 hypervisor 填充，并通过客户机中的 dmidecode 命令检查）。可选的 sysinfo 元素涵盖所有此类信息类别。自 0.8.7 起

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

sysinfo 元素具有强制性的 type 属性，该属性确定子元素的布局，支持的值为：

- smbios

  子元素调用特定的 SMBIOS 值，如果与 os 元素的 smbios 子元素一起使用（请参阅 [操作系统引导](https://www.libvirt.org/formatdomain.html#operating-system-booting)），这些值将影响客户机。sysinfo 的每个子元素都命名一个 SMBIOS 块，在这些元素中可以有一系列 entry 元素，描述块内的字段。识别以下块和条目：bios 这是 SMBIOS 的块 0，条目名称来自：vendor BIOS 供应商名称 version BIOS 版本 date BIOS 发布日期。如果提供，格式为 mm/dd/yy 或 mm/dd/yyyy。如果字符串的年份部分是两位数，则年份假定为 19yy。release 系统 BIOS 主要和次要版本号值连接在一起，作为一个用句点分隔的字符串，例如 10.22。 system 这是 SMBIOS 的块 1，条目名称来自：manufacturer BIOS 制造商 product 产品名称 version 产品版本 serial 序列号 uuid 通用唯一 ID 号。如果此条目与顶级 uuid 元素一起提供（请参阅 [通用元数据](https://www.libvirt.org/formatdomain.html#general-metadata)），则两个值必须匹配。sku 用于标识特定配置的 SKU 编号。family 标识特定计算机所属的系列。 baseBoard 这是 SMBIOS 的块 2。此元素可以重复多次以描述所有主板；但是，并非所有 hypervisor 都一定支持重复。该元素可以有以下子元素：manufacturer BIOS 制造商 product 产品名称 version 产品版本 serial 序列号 asset 资产标签 location 机箱中的位置 注意：为 bios、system 或 baseBoard 块提供的不正确条目将被无错误地忽略。除了 uuid 验证和日期格式检查外，所有值都作为字符串传递给 hypervisor 驱动程序。chassis 自 4.1.0 起，这是 SMBIOS 的块 3，带有 en[... 535 个字符省略 ...]

- fwcfg

  一些 hypervisor 提供了统一的方式来调整固件如何配置自身，或者可能包含要为客户机 OS 安装的表，例如启动顺序、ACPI、SMBIOS 等。它甚至允许用户定义自己的配置 blob。在 QEMU 的情况下，这些会出现在域的 sysfs 下（如果客户机内核启用了 FW_CFG_SYSFS 配置选项），在 /sys/firmware/qemu_fw_cfg 下。注意，这些值无论 <os/> 下的 <smbios/> 模式如何都适用。自 6.5.0 起 **请注意，由于数据槽数量有限，强烈建议不要使用 fwcfg，而应使用 <oemStrings/>**。 `<sysinfo type='fwcfg'>  <entry name='opt/com.example/name'>example value</entry>  <entry name='opt/com.example/config' file='/tmp/provision.ign'/> </sysinfo>` sysinfo 元素可以有多个 entry 子元素。每个元素都有强制性的 name 属性，该属性定义 blob 的名称，必须以 opt/ 开头，为避免与其他名称冲突，建议采用 opt/$RFQDN/$name 的形式，其中 $RFQDN 是您控制的反向完全限定域名。然后，该元素可以包含值（直接设置 blob 值），或 file 属性（从文件设置 blob 值）。

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

  此元素的内容定义为客户机 OS 分配的最大虚拟 CPU 数量，必须在 1 和 hypervisor 支持的最大值之间。cpuset 可选属性 cpuset 是主机物理 CPU 编号的逗号分隔列表，域进程和虚拟 CPU 默认可以固定到这些编号。（注意：域进程和虚拟 CPU 的固定策略可以通过 cputune 单独指定。如果指定了 cputune 的 emulatorpin 属性，则此处 vcpu 指定的 cpuset 将被忽略。同样，对于指定了 vcpupin 的虚拟 CPU，此处 cpuset 指定的 cpuset 将被忽略。对于未指定 vcpupin 的虚拟 CPU，每个都将固定到此处 cpuset 指定的物理 CPU。）该列表中的每个元素要么是单个 CPU 编号，要么是 CPU 编号范围，要么是后跟要从先前范围中排除的 CPU 编号的脱字符。自 0.4.4 起 current 可选属性 current 可用于指定是否应启用少于最大数量的虚拟 CPU。自 0.8.5 起 placement 可选属性 placement 可用于指示域进程的 CPU 放置模式。值可以是 "static" 或 "auto"，但默认为 numatune 的放置或如果指定了 cpuset 则为 "static"。使用 "auto" 表示域进程将固定到通过查询 numad 获得的建议节点集，如果指定了 cpuset 属性的值将被忽略。如果未指定 cpuset 和 placement，或者 placement 是 "static" 但未指定 cpuset，则域进程将固定到所有可用的物理 CPU。自 0.9.11 起（仅 QEMU 和 KVM）

- vcpus

  vcpus 元素允许控制各个 vCPU 的状态。id 属性指定 libvirt 在其他地方（如 vCPU 固定、调度程序信息和 NUMA 分配）使用的 vCPU id。请注意，在客户机中看到的 vCPU ID 在某些情况下可能与 libvirt ID 不同。有效 ID 从 0 到由 vcpu 元素设置的最大 vCPU 计数减 1。enabled 属性允许控制 vCPU 的状态。有效值为 yes 和 no。hotpluggable 控制给定 vCPU 在 CPU 在引导时启用的情况下是否可以热插拔和热拔出。请注意，所有禁用的 vCPU 必须是可热插拔的。有效值为 yes 和 no。order 允许指定添加在线 vCPU 的顺序。对于需要一次插入多个 vCPU 的 hypervisor/平台，顺序可以在所有需要一次启用的 vCPU 之间重复。指定顺序不是必需的，vCPU 然后以任意顺序添加。如果使用顺序信息，必须对所有在线 vCPU 使用。Hypervisor 可能会在某些操作期间清除或更新排序信息，以确保有效的配置。请注意，hypervisor 可能会以与引导 vCPU 不同的方式创建可热插拔的 vCPU，因此可能需要特殊初始化。Hypervisor 可能要求在引导时启用的不可热插拔的 vCPU 从 ID 0 开始聚集在开头。还可能要求 vCPU 0 始终存在且不可热插拔。请注意，为各个 CPU 提供状态可能是启用可寻址 vCPU 热插拔支持所必需的，并且此功能可能不被所有 hypervisor 支持。对于 QEMU，需要满足以下条件。vCPU 0 需要启用且不可热插拔。在 PPC64 上，与其在同一核心中的 vCPU 也需要启用。所有在引导时存在的不可热插拔 CPU 需要在 vCPU 0 之后分组。自 2.2.0 起（仅 QEMU）

## 5 [IOThreads 分配](https://www.libvirt.org/formatdomain.html#id11)

IOThreads 是支持的磁盘设备的专用事件循环线程，用于执行块 I/O 请求，以提高可扩展性，尤其是在具有许多 LUN 的 SMP 主机/客户机上。自 1.2.8 起（仅 QEMU）

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

  可选的 iothreadids 元素提供了为域专门定义 IOThread ID 的能力。默认情况下，IOThread ID 从 1 开始按顺序编号，直到为域定义的 iothreads 数量。id 属性用于定义 IOThread ID。id 属性必须是大于 0 的正整数。如果定义的 iothreadids 少于为域定义的 iothreads，则 libvirt 将从 1 开始按顺序填充 iothreadids，避免任何预定义的 id。如果定义的 iothreadids 多于为域定义的 iothreads，则 iothreads 值将相应调整。自 1.2.15 起 该元素有两个可选属性 thread_pool_min 和 thread_pool_max，允许为给定 IOThread 设置工作线程数的下限和上限。前者可以为零，后者不能。自 8.5.0 起 自 9.4.0 起，可选的子元素 poll 可用于覆盖 hypervisor 默认的 iothread 在切换回事件之前的轮询间隔。可选属性 max 设置轮询应使用的最大时间（以纳秒为单位）。将 max 设置为 0 会禁用轮询。属性 grow 和 shrink 覆盖（或在设置为 0 时禁用）如果设置的间隔被认为不足或过大，则增加/减少轮询间隔的默认步骤。

- defaultiothread

  此元素表示 hypervisor 中的默认事件循环，处理未分配给特定 IOThread 的设备的 I/O 请求。该元素可以有 thread_pool_min 和/或 thread_pool_max 属性，控制默认事件循环的工作线程数的下限和上限。模拟器可能是多线程的，并根据需要生成所谓的工作线程。一般来说，这些属性都不应设置（让模拟器使用其自己的默认值），除非模拟器在实时工作负载中运行，因此无法承受生成新工作线程所需时间的不可预测性。自 8.5.0 起

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

  可选的 cputune 元素提供有关域的 CPU 可调参数的详细信息。注意：对于 qemu 驱动程序，可选的 vcpupin 和 emulatorpin 固定设置在模拟器启动和考虑 NUMA 约束后生效。这意味着在这段时间内，域预计会使用主机的其他物理 CPU，这将反映在 virsh cpu-stats 的输出中。自 0.9.0 起

- vcpupin

  可选的 vcpupin 元素指定域 vCPU 将固定到主机的哪些物理 CPU。如果省略，并且未指定元素 vcpu 的属性 cpuset，则 vCPU 默认固定到所有物理 CPU。它包含两个必需属性，属性 vcpu 指定 vCPU id，属性 cpuset 与元素 vcpu 的属性 cpuset 相同。QEMU 驱动程序支持自 0.9.0 起，Xen 驱动程序支持自 0.9.1 起

- emulatorpin

  可选的 emulatorpin 元素指定 "emulator"（域的子集，不包括 vCPU 或 iothreads）将固定到主机的哪些物理 CPU。如果省略，并且未指定元素 vcpu 的属性 cpuset，则 "emulator" 默认固定到所有物理 CPU。它包含一个必需的属性 cpuset，指定要固定到的物理 CPU。

- iothreadpin

  可选的 iothreadpin 元素指定 IOThreads 将固定到主机的哪些物理 CPU。如果省略且未指定元素 vcpu 的属性 cpuset，则 IOThreads 默认固定到所有物理 CPU。有两个必需属性，属性 iothread 指定 IOThread ID，属性 cpuset 指定要固定到的物理 CPU。请参阅 [IOThreads 分配](https://www.libvirt.org/formatdomain.html#iothreads-allocation) 部分，记录 iothread 的有效值。自 1.2.9 起

- shares

  可选的 shares 元素指定域的比例加权份额。如果省略，它默认为操作系统提供的默认值。注意，该值没有单位，它是基于其他 VM 设置的相对度量，例如，配置为值 2048 的 VM 将获得比配置为值 1024 的 VM 多一倍的 CPU 时间。使用 cgroups v1 时，值应在 [2, 262144] 范围内，使用 cgroups v2 时，值应在 [1, 10000] 范围内。自 0.9.0 起

- period

  可选的 period 元素指定执行间隔（单位：微秒）。在 period 内，域的每个 vCPU 将不允许消耗超过 quota  worth 的运行时间。值应在 [1000, 1000000] 范围内。值为 0 的 period 表示无值。仅 QEMU 驱动程序支持自 0.9.4 起，LXC 自 0.9.10 起

- quota

  可选的 quota 元素指定最大允许带宽（单位：微秒）。quota 为任何负值的域表示该域对 vCPU 线程具有无限带宽，这意味着它不受带宽控制。值应在 [1000, 17592186044415] 范围内或小于 0。值为 0 的 quota 表示无值。您可以使用此功能确保所有 vCPU 以相同的速度运行。仅 QEMU 驱动程序支持自 0.9.4 起，LXC 自 0.9.10 起

- global_period

  可选的 global_period 元素指定整个域的执行 CFS 调度程序间隔（单位：微秒），与 period 不同，后者按 vCPU 执行间隔。值应在 1000, 1000000] 范围内。值为 0 的 global_period 表示无值。仅 QEMU 驱动程序支持自 1.3.3 起

- global_quota

  可选的 global_quota 元素指定整个域在一个周期内的最大允许带宽（单位：微秒）。global_quota 为任何负值的域表示该域具有无限带宽，这意味着它不受带宽控制。值应在 [1000, 17592186044415] 范围内或小于 0。值为 0 的 global_quota 表示无值。仅 QEMU 驱动程序支持自 1.3.3 起

- emulator_period

  可选的 emulator_period 元素指定执行间隔（单位：微秒）。在 emulator_period 内，域的模拟器线程（不包括 vCPU）将不允许消耗超过 emulator_quota worth 的运行时间。值应在 [1000, 1000000] 范围内。值为 0 的 period 表示无值。仅 QEMU 驱动程序支持自 0.10.0 起

- emulator_quota

  可选的 emulator_quota 元素指定域的模拟器线程（不包括 vCPU）的最大允许带宽（单位：微秒）。emulator_quota 为任何负值的域表示该域对模拟器线程（不包括 vCPU）具有无限带宽，这意味着它不受带宽控制。值应在 [1000, 17592186044415] 范围内或小于 0。值为 0 的 quota 表示无值。仅 QEMU 驱动程序支持自 0.10.0 起

- iothread_period

  可选的 iothread_period 元素指定 IOThreads 的执行间隔（单位：微秒）。在 iothread_period 内，域的每个 IOThread 将不允许消耗超过 iothread_quota worth 的运行时间。值应在 [1000, 1000000] 范围内。值为 0 的 iothread_period 表示无值。仅 QEMU 驱动程序支持自 2.1.0 起

- iothread_quota

  可选的 iothread_quota 元素指定 IOThreads 的最大允许带宽（单位：微秒）。iothread_quota 为任何负值的域表示该域的 IOThreads 具有无限带宽，这意味着它不受带宽控制。值应在 [1000, 17592186044415] 范围内或小于 0。值为 0 的 iothread_quota 表示无值。您可以使用此功能确保所有 IOThreads 以相同的速度运行。仅 QEMU 驱动程序支持自 2.1.0 起

- vcpusched、iothreadsched 和 emulatorsched

  可选的 vcpusched、iothreadsched 和 emulatorsched 元素分别指定特定 vCPU、IOThread 和模拟器线程的调度程序类型（值 batch、idle、fifo、rr）。对于 vcpusched 和 iothreadsched，属性 vcpus 和 iothreads 选择此设置适用的 vCPU/IOThreads，省略它们将设置默认值。元素 emulatorsched 没有该属性。有效的 vcpus 值从 0 开始，到为域定义的 vCPU 数量减 1。有效的 iothreads 值在 [IOThreads 分配](https://www.libvirt.org/formatdomain.html#iothreads-allocation) 部分中描述。如果未定义 iothreadids，则 libvirt 将 IOThreads 从 1 编号到域可用的 iothreads 数量。对于实时调度程序（fifo、rr），还必须指定优先级（对于非实时调度程序，优先级被忽略）。优先级的取值范围取决于主机内核（通常为 1-99）。自 1.2.13 起 emulatorsched 自 5.3.0 起

- cachetune 自 4.1.0 起

  可选的 cachetune 元素可以使用主机上的 resctrl 控制 CPU 缓存的分配。是否支持这一点可以从功能中收集，其中也报告了一些限制，如最小大小和所需的粒度。必需的属性 vcpus 指定此分配适用的 vCPU。一个 vCPU 只能是一个 cachetune 元素分配的成员。cachetune 指定的 vCPU 可以与 memorytune 中的 vCPU 相同，但它们不允许重叠。可选的、仅输出的 id 属性唯一标识缓存。支持的子元素是：cache 此可选元素控制 CPU 缓存的分配，具有以下属性：level 要从中分配的主机缓存级别。id 要从中分配的主机缓存 id。type 分配类型。可以是 code（指令）、data（数据）或 both（代码和数据（统一））。当前，分配只能使用与主机支持的相同类型，这意味着对于启用了 CDP（代码/数据优先级）的主机，您不能请求 both。size 要分配的区域大小。该值默认以字节为单位，但 unit 属性可用于缩放该值。unit（可选）如果指定，它是大小指定的单位，如 KiB、MiB、GiB 或 TiB（在 [内存分配](https://www.libvirt.org/formatdomain.html#memory-allocation) 的 memory 元素中描述），默认为字节。 monitor 自 4.10.0 起 可选元素 monitor 为当前缓存分配创建缓存监视器，并具有以下必需属性：level 监视器所属的主机缓存级别。vcpus 监视器适用的 vCPU 列表。监视器的 vCPU 列表只能是关联分配的 vCPU 列表的成员。默认监视器与关联分配具有相同的 vCPU 列表。对于非默认监视器，不允许重叠的 vCPU。

- memorytune 自 4.7.0 起

  可选的 memorytune 元素可以使用主机上的 resctrl 控制内存带宽的分配。是否支持这一点可以从功能中收集，其中也报告了一些限制，如最小带宽和所需的粒度。必需的属性 vcpus 指定此分配适用的 vCPU。一个 vCPU 只能是一个 memorytune 元素分配的成员。memorytune 指定的 vcpus 可以与 cachetune 指定的 vcpus 相同。但是它们不允许相互重叠。支持的子元素是：node 此元素控制 CPU 内存带宽的分配，具有以下属性：id 要从中分配内存带宽的主机节点 id。bandwidth 要从此节点分配的内存带宽。该值通常以百分比表示（Intel），但也可以以 MB/s 表示（如果 resctrl 以 mba_MBps 选项挂载）或以 1/8 GB/s 增量表示（AMD）。 用户负责确保该值在其系统和配置上有意义。

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

  引导时为客户机分配的最大内存。内存分配包括启动时指定或以后热插拔的可能的额外内存设备。此值的单位由可选属性 unit 确定，默认为 "KiB"（ kibibytes，2^10 或 1024 字节的块）。有效的单位是 "b" 或 "bytes"（字节）、"KB"（千字节，10^3 或 1,000 字节）、"k" 或 "KiB"（ kibibytes，1024 字节）、"MB"（兆字节，10^6 或 1,000,000 字节）、"M" 或 "MiB"（ mebibytes，2^20 或 1,048,576 字节）、"GB"（吉字节，10^9 或 1,000,000,000 字节）、"G" 或 "GiB"（ gibibytes，2^30 或 1,073,741,824 字节）、"TB"（太字节，10^12 或 1,000,000,000,000 字节），或 "T" 或 "TiB"（ tebibytes，2^40 或 1,099,511,627,776 字节）。但是，该值将被 libvirt 向上舍入到最接近的 kibibyte，并且可能进一步舍入到 hypervisor 支持的粒度。一些 hypervisor 还强制执行最小值，例如 4000KiB。如果为客户机配置了 NUMA（请参阅 [CPU 模型和拓扑](https://www.libvirt.org/formatdomain.html#cpu-model-and-topology)），则可以省略 memory 元素。在崩溃的情况下，可选属性 dumpCore 可用于控制客户机内存是否应包含在生成的核心转储中（值 "on"、"off"）。unit 自 0.9.11 起，dumpCore 自 0.10.2 起（仅 QEMU）

- maxMemory

  客户机的运行时最大内存分配。通过热插拔内存，可以将由 <memory> 元素或 NUMA 单元大小配置指定的初始内存增加到由此元素指定的限制。unit 属性的行为与 <memory> 相同。slots 属性指定可用于向客户机添加内存的槽位数。边界特定于 hypervisor。请注意，由于通过内存热插拔添加的内存块的对齐，可能无法实现此元素指定的完整大小分配。自 1.2.14 起由 QEMU 驱动程序支持。

- currentMemory

  客户机的实际内存分配。此值可以小于最大分配，以允许动态增加客户机内存。如果省略，它默认为与 memory 元素相同的值。unit 属性的行为与 memory 相同。

## 8 [内存后端](https://www.libvirt.org/formatdomain.html#id14)

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

  这告诉 hypervisor，客户机的内存应该使用大页而不是正常的本机页大小进行分配。自 1.2.5 起，可以更具体地按 numa 节点设置大页。引入了 page 元素。它有一个强制属性 size，指定应该使用哪些大页（在支持不同大小大页的系统上特别有用）。size 属性的默认单位是 kiB（1024 的倍数）。如果要使用不同的单位，请使用可选的 unit 属性。对于具有 NUMA 的系统，可选的 nodeset 属性可能很有用，因为它将给定客户机的 NUMA 节点与特定的大页大小绑定。从示例片段中，除了节点 4 之外的每个 NUMA 节点都使用 1 GB 的大页。有关正确的语法，请参阅 [NUMA 节点调优](https://www.libvirt.org/formatdomain.html#numa-node-tuning)。

- nosharepages

  指示 hypervisor 为此域禁用共享页（内存合并，KSM）。自 1.0.6 起

- locked

  当设置并被 hypervisor 支持时，属于域的内存页将被锁定在主机的内存中，主机将不允许将它们换出，这可能是某些工作负载（如实时）所必需的。对于 QEMU/KVM 客户机，QEMU 进程本身使用的内存也会被锁定：与客户机内存不同，这是 libvirt 无法提前计算的数量，因此它必须完全移除锁定内存的限制。因此，启用此选项会带来潜在的安全风险：当主机内存不足时，主机将无法从客户机回收锁定的内存，这意味着恶意客户机分配大量锁定内存可能会对主机造成拒绝服务攻击。因此，除非您的工作负载需要，否则不建议使用此选项；即使如此，强烈建议同时对内存分配设置适合特定环境的 hard_limit（请参阅 [内存调优](https://www.libvirt.org/formatdomain.html#memory-tuning)），以减轻上述风险。自 1.0.6 起

- source

  使用 type 属性，可以提供 "file" 以利用文件内存后端或保持默认的 "anonymous"。自 4.10.0 起，您可以选择 "memfd" 后端。（仅 QEMU/KVM）

- access

  使用 mode 属性，指定内存是 "shared"（共享）还是 "private"（私有）。这可以通过 memAccess 按 numa 节点覆盖。

- allocation

  使用可选的 mode 属性，通过提供 "immediate"（立即）或 "ondemand"（按需）指定何时分配内存。自 8.2.0 起，可以通过 threads 属性设置 hypervisor 用于分配内存的线程数。为了加快分配过程，固定模拟器线程时，建议包括来自所需 NUMA 节点的 CPU，以便分配线程可以设置其亲和性。

- discard

  当设置并被 hypervisor 支持时，内存内容会在客户机关闭前（或 DIMM 模块拔出时）被丢弃。请注意，这只是一种优化，并不保证在所有情况下都有效（例如，当 hypervisor 崩溃时）。自 4.4.0 起（仅 QEMU/KVM）

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

  可选的 memtune 元素提供有关域的内存可调参数的详细信息。如果省略，它默认为操作系统提供的默认值。对于 QEMU/KVM，参数应用于整个 QEMU 进程。因此，计算它们时，需要将客户机 RAM、客户机视频 RAM 和 QEMU 本身的一些内存开销相加。最后一部分很难确定，所以需要猜测和尝试。对于每个可调参数，可以指定输入时数字的单位，使用与 <memory> 相同的值。为了向后兼容，输出始终以 KiB 为单位。unit 自 0.9.11 起 所有 *limit 参数的可能值范围从 0 到 VIR_DOMAIN_MEMORY_PARAM_UNLIMITED。

- hard_limit

  可选的 hard_limit 元素是客户机可以使用的最大内存。此值的单位是 kibibytes（即 1024 字节的块）。强烈建议 QEMU 和 KVM 的用户不要设置此限制，因为如果猜测过低，域可能会被内核杀死，而确定进程运行所需的内存是一个 [不可判定问题](https://en.wikipedia.org/wiki/Undecidable_problem)；也就是说，如果你已经在 [内存后端](https://www.libvirt.org/formatdomain.html#memory-backing) 中设置了 locked，因为你的工作负载需要它，你将不得不考虑部署的具体情况，并找出一个足够大的 hard_limit 值来支持客户机的内存需求，但又足够小以保护主机免受恶意客户机锁定所有内存的影响。

- soft_limit

  可选的 soft_limit 元素是内存争用时要强制执行的内存限制。此值的单位是 kibibytes（即 1024 字节的块）

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

  可选的 numatune 元素提供有关如何通过控制域进程的 NUMA 策略来调优 NUMA 主机性能的详细信息。注意，仅由 QEMU 驱动程序支持。自 0.9.3 起

- memory

  可选的 memory 元素指定如何在 NUMA 主机上为域进程分配内存。它包含几个可选属性。属性 mode 可以是 'interleave'、'strict'、'preferred' 或 'restrictive'，默认为 'strict'。值 'restrictive' 指定使用系统默认策略，只使用 cgroups 来限制内存节点，并且需要在 memnode 元素中将 mode 设置为 'restrictive'（见下面的怪癖）。这仅用于能够使用 virsh numatune 或 virDomainSetNumaParameters 请求移动运行域的此类内存，并不保证会发生。属性 nodeset 指定 NUMA 节点，使用与元素 vcpu 的属性 cpuset 相同的语法。属性 placement（自 0.9.12 起）可用于指示域进程的内存放置模式，其值可以是 "static" 或 "auto"，默认为 vcpu 的放置，或如果指定了 nodeset 则为 "static"。"auto" 表示域进程将仅从查询 numad 返回的建议节点集分配内存，如果指定了 nodeset 属性的值将被忽略。如果 vcpu 的放置是 'auto'，并且未指定 numatune，则会隐式添加一个默认的 numatune，放置为 'auto'，模式为 'strict'。自 0.9.3 起 有关此元素更新的更多信息，请参阅 [virDomainSetNumaParameters](https://www.libvirt.org/html/libvirt-libvirt-domain.html#virDomainSetNumaParameters)。

- memnode

  可选的 memnode 元素可以为每个客户机 NUMA 节点指定内存分配策略。对于没有相应 memnode 元素的节点，将使用元素 memory 的默认值。属性 cellid 寻址应用设置的客户机 NUMA 节点。属性 mode 和 nodeset 与 memory 元素中的含义和语法相同。此设置与自动放置不兼容。注意，对于 memnode，这只会指导 vCPU 线程的内存访问或类似机制，并且是非常特定于 hypervisor 的。这不保证节点内存分配的放置。对于适当的限制，应使用其他方法（例如，不同的模式，预分配的大页）。QEMU 自 1.2.7 起

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
      <read_iops_sec>20000</read_iops_sec>
      <write_iops_sec>20000</write_iops_sec>
    </device>
  </blkiotune>
  ...
</domain>
```

- blkiotune

  可选的 blkiotune 元素提供了为域调优 Blkio cgroup 可调参数的能力。如果省略，它默认为操作系统提供的默认值。自 0.8.8 起

- weight

  可选的 weight 元素是客户机的整体 I/O 权重。值应在 [100, 1000] 范围内。内核 2.6.39 之后，值可以在 [10, 1000] 范围内。

- device

  域可能有多个 device 元素，进一步调整域使用的每个主机块设备的权重。请注意，多个磁盘（请参阅 [硬盘、软盘、CD-ROM](https://www.libvirt.org/formatdomain.html#hard-drives-floppy-disks-cdroms)）可以共享单个主机块设备，如果它们由同一主机文件系统中的文件支持，这就是为什么此调优参数在全局域级别而不是与每个客户机磁盘设备相关联（与磁盘定义的 <iotune> 元素（请参阅 [硬盘、软盘、CD-ROM](https://www.libvirt.org/formatdomain.html#hard-drives-floppy-disks-cdroms)）相比，后者可以应用于单个磁盘）。每个 device 元素有两个强制子元素，path 描述设备的绝对路径，weight 给出该设备的相对权重，范围在 [100, 1000] 之间。内核 2.6.39 之后，值可以在 [10, 1000] 范围内。自 0.9.8 起 此外，可以使用以下可选子元素：read_bytes_sec 读取吞吐量限制（字节/秒）。自 1.2.2 起 write_bytes_sec 写入吞吐量限制（字节/秒）。自 1.2.2 起 read_iops_sec 读取 I/O 操作/秒限制。自 1.2.2 起 write_iops_sec 写入 I/O 操作/秒限制。自 1.2.2 起

## 12 [资源分区](https://www.libvirt.org/formatdomain.html#id18)

Hypervisor 可能允许将虚拟机放置到资源分区中，可能带有所述分区的嵌套。resource 元素将与资源分区相关的配置分组在一起。它当前支持一个子元素 partition，其内容定义了放置域的资源分区的绝对路径。如果未列出分区，则域将被放置在默认分区中。应用程序/管理员有责任确保在启动客户机之前分区存在。只有（特定于 hypervisor 的）默认分区可以默认存在。

```
...
<resource>
  <partition>/virtualmachines/production</partition>
</resource>
...
```

资源分区目前由 QEMU 和 LXC 驱动程序支持，它们将分区路径映射到所有已挂载控制器中的 cgroups 目录。自 1.0.5 起

## 13 [光纤通道 VMID](https://www.libvirt.org/formatdomain.html#id19)

FC SAN 可以根据 VMID 提供各种 QoS 级别和访问控制。它还可以在每 VM 级别收集遥测数据，可用于增强 VM 的 IO 性能。这可以通过使用 fibrechannel 元素的 appid 属性进行配置。该属性包含单个字符串（最大 128 字节），内核使用它来创建 VMID。

```
...
<resource>
  <fibrechannel appid='userProvidedID'/>
</resource>
...
```

使用此功能需要支持光纤通道的硬件，内核编译时启用了 CONFIG_BLK_CGROUP_FC_APPID 选项，并且加载了 nvme_fc 内核模块。自 7.7.0 起

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

  cpu 元素是描述客户机 CPU 要求的主要容器。其 match 属性指定提供给客户机的虚拟 CPU 与这些要求的匹配程度。自 0.7.6 起，如果 topology 是 cpu 内的唯一元素，则可以省略 match 属性。match 属性的可能值为：minimum 指定的 CPU 模型和功能描述了最低请求的 CPU。如果使用当前主机上的请求 hypervisor 可能，将向客户机提供更好的 CPU。这是一种受约束的 host-model 模式；如果提供的虚拟 CPU 不满足要求，域将不会创建。exact 提供给客户机的虚拟 CPU 应与规范完全匹配。如果不支持这样的 CPU，libvirt 将拒绝启动域。strict 除非主机 CPU 与规范完全匹配，否则不会创建域。这在实践中不是很有用，只有在有真正原因的情况下才应使用。自 0.8.5 起，可以省略 match 属性，默认为 exact。有时，hypervisor 无法创建与 libvirt 传递的规范完全匹配的虚拟 CPU。自 3.2.0 起，可以使用可选的 check 属性来请求特定方式检查虚拟 CPU 是否与规范匹配。启动域时，通常可以安全地省略此属性并坚持默认值。域启动后，libvirt 将自动更改 check 属性为最佳支持值，以确保当域迁移到另一台主机时虚拟 CPU 不会更改。可以使用以下值：none Libvirt 不进行任何检查，由 hypervisor 负责在无法提供请求的 CPU 时拒绝启动域。对于 QEMU，这意味着完全不进行检查，因为 QEMU 的默认行为是发出警告，但无论如何启动域。partial Libvirt 将在启动域之前检查客户机 CPU 规范，但其余部分由 hypervisor 处理。

- model

  model 元素的内容指定客户机请求的 CPU 模型。可用 CPU 模型及其定义的列表可以在 cpu_map 目录中找到，该目录安装在 libvirt 的数据目录中。如果 hypervisor 无法使用确切的 CPU 模型，libvirt 会自动回退到 hypervisor 支持的最接近的模型，同时保持 CPU 功能列表。自 0.9.10 起，可以使用可选的 fallback 属性来禁止此行为，在这种情况下，尝试启动请求不支持的 CPU 模型的域将失败。fallback 属性的支持值为：allow（默认）和 forbid。可选的 vendor_id 属性（自 0.10.0 起）可用于设置客户机看到的供应商 ID。它必须恰好 12 个字符长。如果未设置，则使用主机的供应商 ID。典型的可能值是 "AuthenticAMD" 和 "GenuineIntel"。

- vendor

  自 0.8.3 起，vendor 元素的内容指定客户机请求的 CPU 供应商。如果缺少此元素，客户机可以在与给定功能匹配的 CPU 上运行，无论其供应商如何。支持的供应商列表可以在 cpu_map/*_vendors.xml 中找到。

- topology

  topology 元素指定提供给客户机的虚拟 CPU 的请求拓扑。其属性 sockets、dies（自 6.1.0 起）、clusters（自 10.1.0 起）、cores 和 threads 接受非零正整数值。它们分别指 CPU 插槽总数、每个插槽的 dies 数、每个 die 的 clusters 数、每个 cluster 的核心数以及每个核心的线程数。dies 和 clusters 属性是可选的，如果省略，将默认为 1，而其他属性都是必需的。Hypervisor 可能要求 cpus 元素指定的最大 vCPU 数量等于拓扑产生的 vcpus 数量。此外，并非所有架构和机器类型都支持为所有属性指定除 1 以外的值。

- feature

  cpu 元素可以包含零个或多个 feature 元素，用于微调所选 CPU 模型提供的功能。已知功能名称的列表可以在与 CPU 模型相同的文件中找到。每个 feature 元素的含义取决于其 policy 属性，该属性必须设置为以下值之一：force 虚拟 CPU 将声称支持该功能，无论主机 CPU 是否支持。require 除非该功能由主机 CPU 支持或 hypervisor 能够模拟，否则客户机创建将失败。optional 虚拟 CPU 将支持该功能当且仅当它由主机 CPU 支持。disable 虚拟 CPU 将不支持该功能。forbid 如果主机 CPU 支持该功能，客户机创建将失败。自 0.8.5 起，可以省略 policy 属性，默认为 require。各个 CPU 功能名称在 name 属性中指定。例如，要使用 Intel IvyBridge CPU 模型显式指定 'pcid' 功能：`... <cpu match='exact'>  <model fallback='forbid'>IvyBridge</model>  <vendor>Intel</vendor>  <feature policy='require' name='pcid'/> </cpu> ...`

- deprecated_features

  自 11.0.0 起，S390 客户机可以利用 deprecated_features 属性来指定切换被 hypervisor 标记为已弃用的 CPU 模型功能。当此属性设置为 off 时，活动客户机 XML 将反映具有 disable 策略的相应功能。当此属性设置为 on 时，相应功能将被启用。

- cache

  自 3.3.0 起，cache 元素描述虚拟 CPU 缓存。如果元素缺失，hypervisor 将使用合理的默认值。level 此可选属性指定元素描述的缓存级别。缺失属性意味着元素同时描述所有 CPU 缓存级别。禁止混合设置了 level 属性的 cache 元素和没有该属性的元素。mode 支持以下值：emulate hypervisor 将提供假的 CPU 缓存数据。passthrough 主机 CPU 报告的真实 CPU 缓存数据将传递给虚拟 CPU。disable 虚拟 CPU 将报告没有指定级别的 CPU 缓存（如果缺失 level 属性，则根本没有缓存）。

- maxphysaddr

  自 8.7.0 起，maxphysaddr 元素描述虚拟 CPU 地址大小（以位为单位）。如果元素缺失，将使用 hypervisor 默认值。mode 此强制属性指定地址大小的呈现方式。支持以下模式：passthrough 主机 CPU 报告的物理地址位数将传递给虚拟 CPU emulate hypervisor 将通过 bits 属性为物理地址位数定义特定值，（自 9.2.0 起可选）位数不能超过 hypervisor 支持的物理地址位数。 bits 如果 mode 属性设置为 emulate，则 bits 属性是必需的，指定虚拟 CPU 地址大小（以位为单位）。 limit limit 属性可用于限制 passthrough 模式的地址位数的最大值，即，如果主机 CPU 报告的位数超过该值，则使用 limit。自 9.3.0 起

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

每个 cell 元素指定一个 NUMA 单元或 NUMA 节点。cpus 指定作为节点一部分的 CPU 或 CPU 范围。自 6.5.0 起 对于 qemu 驱动程序，如果模拟器二进制文件支持每个 cell 中的不连续 cpu 范围，则在每个 cell 中声明的所有 CPU 的总和将与 vcpu 元素中声明的最大虚拟 CPU 数量匹配。这是通过将任何剩余的 CPU 填充到第一个 NUMA cell 中来完成的。鼓励用户提供完整的 NUMA 拓扑，其中 NUMA CPU 的总和与 vcpus 中声明的最大虚拟 CPU 数量匹配，以使域在 qemu 和 libvirt 版本之间保持一致。memory 指定节点内存（以 kibibytes 为单位，即 1024 字节的块）。自 6.6.0 起，cpus 属性是可选的，如果省略，将创建无 CPU 的 NUMA 节点。自 1.2.11 起，可以使用额外的 unit 属性（请参阅 [内存分配](https://www.libvirt.org/formatdomain.html#memory-allocation)）来定义指定内存的单位。自 1.2.7 起，所有 cell 都应有 id 属性，以防代码中需要引用某个 cell，否则 cell 将按从 0 开始的递增顺序分配 id。不建议混合使用有和没有 id 属性的 cell，因为这可能导致意外行为。自 1.2.9 起，可选属性 memAccess 可以控制内存是映射为 "shared"（共享）还是 "private"（私有）。这仅对大页支持的内存和 nvdimm 模块有效。每个 cell 元素可以有一个可选的 discard 属性，用于微调给定 numa 节点的 discard 功能，如 [内存后端](https://www.libvirt.org/formatdomain.html#memory-backing) 中所述。接受的值为 yes 和 no。自 4.4.0 起

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

描述 NUMA cell 之间的距离目前仅由 Xen 和 QEMU 支持。如果没有提供距离来描述不同 cell 之间的 SLIT 数据，它将默认为本地距离为 10、远程距离为 20 的方案。

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

自 6.6.0 起，cell 元素可以有一个 cache 子元素，描述内存邻近域的内存侧缓存。cache 元素有一个 level 属性，描述缓存级别，因此该元素可以重复多次以描述不同级别的缓存。

cache 元素有以下强制属性：

- level

  此描述所指的缓存级别。

- associativity

  描述缓存关联性（接受的值为 none、direct 和 full）。

- policy

  描述缓存写入关联性（接受的值为 none、writeback 和 writethrough）。

cache 元素有两个强制子元素：size 和 line，描述缓存大小和缓存行大小。两个元素都接受两个属性：value 和 unit，用于设置相应缓存属性的值。

NUMA 描述有一个可选的 interconnects 元素，描述归一化的内存读/写延迟、发起者邻近域（处理器或 I/O）和目标邻近域（内存）之间的读/写带宽。

interconnects 元素可以有零个或多个 latency 子元素来描述两个内存节点之间的延迟，以及零个或多个 bandwidth 子元素来描述两个内存节点之间的带宽。这两个元素都有以下强制属性：

- initiator

  引用源 NUMA 节点

- target

  引用目标 NUMA 节点

- type

  访问类型。接受的值：access、read、write

- value

  实际值。对于延迟，这是以纳秒为单位的延迟，对于带宽，此值是以 kibibytes/秒为单位。使用额外的 unit 属性更改单位。

要描述从一个 NUMA 节点到另一个 NUMA 节点的缓存的延迟，latency 元素有一个可选的 cache 属性，该属性与 target 属性结合使用，创建对远程 NUMA 节点缓存级别的完整引用。例如，target='0' cache='1' 引用 NUMA 节点 0 的第一级缓存。

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

以下元素集合允许指定当客户机 OS 触发生命周期操作时要采取的操作。一个常见的用例是在进行初始 OS 安装时，强制将重启视为关机。这允许在第一次安装后启动时重新配置 VM。

- on_poweroff

  此元素的内容指定当客户机请求关机时要采取的操作。

- on_reboot

  此元素的内容指定当客户机请求重启时要采取的操作。

- on_crash

  此元素的内容指定当客户机崩溃时要采取的操作。

每个这些状态都允许相同的四个可能操作。

- destroy

  域将被完全终止，所有资源将被释放。

- restart

  域将被终止，然后使用相同的配置重新启动。

- preserve

  域将被终止，其资源将被保留以允许分析。

- rename-restart

  域将被终止，然后使用新名称重新启动。（仅由 libxl hypervisor 驱动程序支持。）

QEMU/KVM/HVF 支持 on_poweroff 和 on_reboot 事件处理 destroy 和 restart 操作，但 on_poweroff 设置为 restart 和 on_reboot 设置为 destroy 的组合是被禁止的。

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

  域将被暂停，以便在锁问题解决后可以手动恢复。

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

  这些元素启用（'yes'）或禁用（'no'）BIOS 对 S3（挂起到内存）和 S4（挂起到磁盘）ACPI 睡眠状态的支持。如果未指定任何内容，则 hypervisor 将保留其默认值。注意：此设置无法防止客户机 OS 执行挂起，因为客户机 OS 本身可以选择规避睡眠状态的不可用性（例如，通过完全关闭来实现 S4）。

## 17 [磁盘限制组管理](https://www.libvirt.org/formatdomain.html#id24)

自 11.2.0 起，可以创建多个命名的限制组，然后在 throttlefilters`（`disk 元素的子元素）中引用它们，以在 QEMU 中为特定磁盘形成过滤器链。限制（throttlegroups）在域内共享，因此同一个组可以被不同的过滤器引用。

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

  它具有与 iotune 相同的子元素（请参阅 [硬盘、软盘、CD-ROM](https://www.libvirt.org/formatdomain.html#hard-drives-floppy-disks-cdroms)），区别在于 group_name> 是必需的。

## 18 [Hypervisor 功能](https://www.libvirt.org/formatdomain.html#id25)

Hypervisor 可能允许切换某些 CPU / 机器功能的开/关。

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

所有功能都列在 features 元素中，省略可切换的功能标签会将其关闭。可用功能可以通过请求 [功能 XML](https://www.libvirt.org/formatcaps.html) 和 [域功能 XML](https://www.libvirt.org/formatdomaincaps.html) 找到，但完全虚拟化域的常见集合是：

- pae

  物理地址扩展模式允许 32 位客户机寻址超过 4 GB 的内存。

- acpi

  ACPI 对电源管理很有用，例如，对于 KVM 或 HVF 客户机，它是正常关闭工作所必需的。

- apic

  APIC 允许使用可编程 IRQ 管理。自 0.10.2 起（仅 QEMU），有一个可选的 eoi 属性，值为 on 和 off，用于切换客户机 EOI（中断结束）的可用性。

- hap

  根据 state 属性（值为 on、off）启用或禁用硬件辅助分页的使用。如果 hypervisor 检测到硬件辅助分页的可用性，默认值为 on。

- viridian

  启用用于半虚拟化客户机操作系统的 Viridian hypervisor 扩展

- privnet

  始终创建私有网络命名空间。如果定义了任何接口设备，这会自动设置。此功能仅与基于容器的虚拟化驱动程序（如 LXC）相关。

- hyperv

  启用各种功能，改善运行 Microsoft Windows 的客户机的行为。自 11.3.0 起，其中一些标志也可用于运行 Microsoft Windows 的 Xen 域。
  | 功能 | 描述 | 值 | 自 |
  | --- | --- | --- | --- |
  | relaxed | 放宽对计时器的约束 | on, off | 1.0.0 (QEMU 2.0), 11.3.0 (Xen, always on) |
  | vapic | 启用虚拟 APIC | on, off | 1.1.0 (QEMU 2.0), 11.3.0 (Xen) |
  | spinlocks | 启用自旋锁支持 - retries 属性定义在多少次失败的获取尝试后通知 hypervisor | on, off; retries - 在 4095 和 4294967295 之间，特殊值 4294967295 意味着永远不通知 hypervisor（如果省略则默认） | 1.1.0 (QEMU 2.0), never-notify 模式 11.9.0 (QEMU 2.0) |
  | vpindex | 虚拟处理器索引 | on, off | 1.3.3 (QEMU 2.5), 11.3.0 (Xen, always on) |
  | runtime | 处理器在运行客户机代码和代表客户机代码上花费的时间 | on, off | 1.3.3 (QEMU 2.5) |
  | synic | 启用合成中断控制器 (SynIC) | on, off | 1.3.3 (QEMU 2.6), 11.3.0 (Xen) |
  | stimer | 启用 SynIC 计时器，可选支持直接模式 | on, off; direct - on,off | 1.3.3 (QEMU 2.6), 直接模式 5.7.0 (QEMU 4.1), 11.3.0 (Xen, on/off only) |
  | reset | 启用 hypervisor 重置 | on, off | 1.3.3 (QEMU 2.5) |
  | vendor_id | 设置 hypervisor 供应商 ID | on, off; value - 字符串，最多 12 个字符 | 1.3.3 (QEMU 2.5) |
  | frequencies | 暴露频率 MSR | on, off | 4.7.0 (QEMU 2.12), 11.3.0 (Xen) |
  | reenlightenment | 在迁移时启用重新启蒙通知 | on, off | 4.7.0 (QEMU 3.0) |
  | tlbflush | 启用 PV TLB 刷新支持 | on, off; direct - on,off; extended - on,off | 4.7.0 (QEMU 3.0), 直接和扩展模式 11.0.0 (QEMU 7.1.0), 11.3.0 (Xen, on/off only) |
  | ipi | 启用 PV IPI 支持 | on, off | 4.10.0 (QEMU 3.1), 11.3.0 (Xen) |
  | evmcs | 启用 Enlightened VMCS | on, off | 4.10.0 (QEMU 3.1) |
  | avic | 启用将 Hyper-V SynIC 与硬件 APICv/AVIC 一起使用 | on, off | 8.10.0 (QEMU 6.2) |
  | emsr_bitmap | 避免在 vmexits 时对 L2 MSR 位图进行不必要的更新。 | on, off | 10.7.0 (QEMU 7.1) |
  | xmm_input | 启用 XMM 快速超调用输入 | on, off | 10.7.0 (QEMU 7.1) |
  自 8.0.0 起（QEMU）自 11.3.0 起（Xen），可以通过将 mode 属性设置为以下值之一来进一步配置 hypervisor：custom 精确设置指定的功能。passthrough 启用 hypervisor 当前支持的所有功能，即使是 libvirt 不理解的功能。如果源主机和目标主机在硬件、QEMU 版本、微代码版本和配置方面不相同，使用 passthrough 的客户机迁移是危险的。如果尝试这样的迁移，客户机可能会在目标主机上恢复执行时挂起或崩溃。根据 hypervisor 版本，虚拟 CPU 可能包含可能阻止迁移到相同主机的功能。host-model 类似于 passthrough 模式，不同之处在于 libvirt 检测 hypervisor 支持哪些启发式功能，并在域启动时将它们扩展到活动 XML 中。从某种意义上说，这类似于 host-model CPU 模式（请参阅 [CPU 模型和拓扑](https://www.libvirt.org/formatdomain.html#cpu-model-and-topology)）。自 11.9.0 起 也可以像在 custom 模式中一样设置功能。然后这些功能保持不变，不会对它们进行扩展。自 12.1.0 起 mode 属性可以省略，默认为 custom。

- pvspinlock

  通知客户机主机支持半虚拟化自旋锁，例如通过公开 pvticketlocks 机制。此功能可以通过使用 state='off' 属性显式禁用。

- kvm

  用于更改 KVM hypervisor 行为的各种功能。
  | 功能 | 描述 | 值 | 自 |
  | --- | --- | --- | --- |
  | hidden | 对标准 MSR 基于发现隐藏 KVM hypervisor | on, off | 1.2.8 (QEMU 2.1.0) |
  | hint-dedicated | 允许客户机在专用 vCPU 上运行时启用优化 | on, off | 5.7.0 (QEMU 2.12.0) |
  | poll-control | 通过引入忙等待的宽限期来减少 IO 完成延迟 | on, off | 6.10.0 (QEMU 4.2) |
  | pv-ipi | 半虚拟化发送 IPIs | on, off | 7.10.0 (QEMU 3.1) |
  | dirty-ring | 启用脏环功能 | on, off; size - 必须是 2 的幂，范围 [1024,65536] | 8.0.0 (QEMU 6.1) |

- xen

  用于更改 Xen hypervisor 行为的各种功能。
  | 功能 | 描述 | 值 | 自 |
  | --- | --- | --- | --- |
  | e820_host | 向客户机公开主机 e820（仅 PV） | on, off | 6.3.0 |
  | passthrough | 启用 IOMMU 映射，允许 PCI 直通 | on, off; mode - 可选字符串 sync_pt 或 share_pt | 6.3.0 |

- pmu

  根据 state 属性（值为 on、off，默认为 on）启用或禁用客户机的性能监控单元。自 1.2.12 起

- vmport

  根据 state 属性（值为 on、off，默认为 on）启用或禁用 VMware IO 端口的仿真，用于 vmmouse 等。自 1.2.16 起

- gic

  为使用通用中断控制器而不是 APIC 来处理中断的架构启用。例如，'aarch64' 架构使用 gic 而不是 apic。可选属性 version 指定 GIC 版本；但是，并非所有 hypervisor 都支持它。接受的值为 2、3 和 host。自 1.2.16 起

- smm

  根据 state 属性（值为 on、off，默认为 on）启用或禁用系统管理模式。自 2.1.0 起 可选子元素 tseg 可用于指定专用于 SMM 扩展 TSEG 的内存量。这提供了第四个选项大小，除了现有的选项（1 MiB、2 MiB 和 8 MiB）之外，客户机 OS（或更确切地说是加载程序）可以选择。大小可以指定为该元素的值，可选属性 unit 可用于指定上述值的单位（默认为 'MiB'）。如果设置为 0，则不通告扩展大小，只有默认大小（见上文）可用。**如果 VM 正在启动，您应该保持此选项不变，除非您非常确定您知道自己在做什么。** 此值是可配置的，因为无法保证计算正确，以确保它能正常工作。在 QEMU 中，用户可配置的扩展 TSEG 功能在 pc-q35-2.9 及之前版本中不可用。从 pc-q35-2.10 开始，该功能可用，默认大小为 16 MiB。这应该足以支持最多约 272 个 vCPU、总共 5 GiB 客户机 RAM、无热插拔内存范围和 32 GiB 的 64 位 PCI MMIO 孔径。或者对于 48 个 vCPU，1TB 客户机 RAM，无热插拔 DIMM 范围，和 32GB 的 64 位 PCI MMIO 孔径。这些值也可能根据 VM 使用的加载程序而有所不同。对于显著更高的 vCPU 数量或增加的地址空间（可以是内存、maxMemory、64 位 PCI MMIO 孔径大小；大约每 1 TiB 地址空间 8 MiB TSEG），可能需要额外的大小，这也可以向上舍入。由于此设置的性质类似于"客户机应该有多少 RAM"，建议用户要么参考客户机 OS 或加载程序的文档（如果有的话），要么通过试验更改值直到 VM 成功启动来测试这一点。另一个指导值可能是 48 MiB 应该足够大的客户机（240 个 vCPU 和 4TB 客户机 RAM）。

- ioapic

  调整 I/O APIC。driver 属性的可能值为：kvm（KVM 域的默认值）和 qemu，它将 I/O APIC 放在用户空间，也称为拆分 I/O APIC 模式。自 3.4.0 起（仅 QEMU/KVM）

- hpt

  配置 pSeries 客户机的 HPT（哈希页表）。resizing 属性的可能值为 enabled，这会导致如果客户机和主机都支持，则启用 HPT 调整大小；disabled，这会导致无论客户机和主机支持如何都禁用 HPT 调整大小；以及 required，这会阻止客户机启动，除非客户机和主机都支持 HPT 调整大小。如果未定义该属性，将使用 hypervisor 默认值。自 3.10.0 起（仅 QEMU/KVM）。可选的 maxpagesize 子元素可用于限制 HPT 客户机的可用页大小。常见值为 64 KiB、16 MiB 和 16 GiB；如果未指定，将使用 hypervisor 默认值。自 4.5.0 起（仅 QEMU/KVM）。

- vmcoreinfo

  启用 QEMU vmcoreinfo 设备，让客户机内核保存调试详细信息。自 4.4.0 起（仅 QEMU）

- htm

  为 pSeries 客户机配置 HTM（硬件事务内存）可用性。state 属性的可能值为 on 和 off。如果未定义该属性，将使用 hypervisor 默认值。自 4.6.0 起（仅 QEMU/KVM）

- nested-hv

  为 pSeries 客户机配置嵌套 HV 可用性。这需要从主机 (L0) 启用才能有效；如果计划在其中运行嵌套 (L2) 客户机，在 (L1) 客户机中具有 HV 支持是非常可取的，因为这将导致这些嵌套客户机具有比使用 KVM PR 或 TCG 时更好的性能。state 属性的可能值为 on 和 off。如果未定义该属性，将使用 hypervisor 默认值。自 4.10.0 起（仅 QEMU/KVM）

- msrs

  一些客户机可能需要忽略未知的模型特定寄存器 (MSR) 读写。可以通过将 msrs 的 unknown 属性设置为 ignore 来切换此功能。如果未定义该属性，或设置为 fault，则不会忽略未知的读写。自 5.1.0 起（仅 bhyve）

- ccf-assist

  为 pSeries 客户机配置 ccf-assist（计数缓存刷新辅助）可用性。state 属性的可能值为 on 和 off。如果未定义该属性，将使用 hypervisor 默认值。自 5.9.0 起（仅 QEMU/KVM）

- cfpc

  为 pSeries 客户机配置 cfpc（特权更改时的缓存刷新）可用性。value 属性的可能值为 broken（无保护）、workaround（可用软件解决方法）和 fixed（硬件中已修复）。如果未定义该属性，将使用 hypervisor 默认值。自 6.3.0 起（仅 QEMU/KVM）

- sbbc

  为 pSeries 客户机配置 sbbc（推测屏障边界检查）可用性。value 属性的可能值为 broken（无保护）、workaround（可用软件解决方法）和 fixed（硬件中已修复）。如果未定义该属性，将使用 hypervisor 默认值。自 6.3.0 起（仅 QEMU/KVM）

- ibs

  为 pSeries 客户机配置 ibs（间接分支推测）可用性。value 属性的可能值为 broken（无保护）、workaround（计数缓存刷新）、fixed-ibs（通过序列化间接分支修复）、fixed-ccd（通过禁用缓存计数修复）和 fixed-na（硬件中已修复 - 不再适用）。如果未定义该属性，将使用 hypervisor 默认值。自 6.3.0 起（仅 QEMU/KVM）

- tcg

  用于更改 TCG 加速器行为的各种功能。
  | 功能 | 描述 | 值 | 自 |
  | --- | --- | --- | --- |
  | tb-cache | 翻译块缓存大小 | 整数（MiB 的倍数） | 8.0.0 |

- async-teardown

  根据 enabled 属性（值为 yes、no）启用或禁用 QEMU 异步拆卸，以改善客户机上的内存回收。自 9.6.0 起（仅 QEMU）

- ras

  启用时（on），使用 ACPI 和客户机外部中止异常向客户机报告主机内存错误。如果未定义该属性，将使用 hypervisor 默认值。自 10.4.0 起（仅 QEMU/KVM 和 ARM virt 客户机）

- ps2

  根据 state 属性（值为 on、off）启用或禁用由 ps2 总线输入设备使用的 PS/2 控制器的仿真。如果未定义该属性，将使用 hypervisor 默认值。自 10.7.0 起（仅 QEMU）

- aia

  为 RISC-V 'virt' 客户机配置 aia（高级中断架构）。value 属性的可能值为 aplic（每个套接字存在一个仿真的 APLIC 设备）、aplic-imsic（每个核心存在一个 APLIC 和一个 IMSIC 设备）或 none（不支持 AIA）。如果未定义该属性，将使用 hypervisor 默认值。自 11.1.0 起（仅 QEMU/KVM 和 RISC-V 客户机）

- virtualization

  启用模拟实现 Arm 虚拟化扩展的客户机 CPU。如果未定义该属性，将使用 hypervisor 默认值。自 12.1.0 起（仅 QEMU/KVM 和 ARM virt 客户机）

## 19 [时间保持](https://www.libvirt.org/formatdomain.html#id26)

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

  offset 属性有四个可能的值，允许对客户机时钟如何与主机同步进行细粒度控制。注意，并非所有 hypervisor 都支持所有模式。utc 客户机时钟在启动时将始终与 UTC 同步。自 0.9.11 起，'utc' 模式可以转换为 'variable' 模式，这可以通过使用 adjustment 属性来控制。如果值为 'reset'，则永远不会进行转换（并非所有 hypervisor 都能在每次启动时与 UTC 同步；使用 'reset' 将在那些 hypervisor 上导致错误）。数值强制转换为 'variable' 模式，使用该值作为初始调整。默认调整是特定于 hypervisor 的。localtime 客户机时钟在启动时将与主机配置的时区（如果有）同步。自 0.9.11 起，adjustment 属性的行为与 'utc' 模式相同。timezone 客户机时钟将使用 timezone 属性同步到请求的时区。自 0.7.7 起 variable 客户机时钟将应用相对于 UTC 或 localtime 的任意偏移，具体取决于 basis 属性。相对于 UTC（或 localtime）的增量以秒为单位，使用 adjustment 属性指定。客户机可以自由随时间调整 RTC，并期望在下次重启时会被遵守。这与 'utc' 和 'localtime' 模式（带有可选属性 adjustment='reset'）形成对比，其中 RTC 调整在每次重启时都会丢失。自 0.7.7 起 自 0.9.11 起，basis 属性可以是 'utc'（默认）或 'localtime'。absolute 客户机时钟在域启动时将始终设置为 start 属性的值。start 属性采用纪元时间戳。自 8.4.0 起。 时钟可能有零个或多个 timer 子元素。自 0.8.0 起

- timer

  每个 timer 元素需要一个 name 属性，并且具有其他取决于指定名称的可选属性。各种 hypervisor 支持不同的属性组合。name name 属性选择要修改的计时器，可以是 "platform"（当前不受支持）、"hpet"（xen、qemu、lxc）、"kvmclock"（qemu）、"pit"（qemu）、"rtc"（qemu、lxc）、"tsc"（xen、qemu - 自 3.2.0 起）、"hypervclock"（qemu - 自 1.2.2 起）或 "armvtimer"（qemu - 自 6.1.0 起）。hypervclock 计时器为运行 Microsoft Windows 操作系统的客户机添加对参考时间计数器和 iTSC 功能参考页的支持。track track 属性指定计时器跟踪的内容，可以是 "boot"、"guest"、"wall" 或 "realtime"。仅对 name="rtc" 或 name="platform" 有效。tickpolicy tickpolicy 属性确定当 QEMU 错过向客户机注入 tick 的截止日期时会发生什么。例如，这可能因为客户机被暂停而发生。delay 继续以正常速率传递 tick。客户机 OS 不会注意到任何问题，因为从它的角度来看，时间将继续正常流动。客户机中的时间现在应该落后于主机中的时间，正好是错过 tick 的时间量。catchup 以更高的速率传递 tick 以赶上错过的 tick。客户机 OS 不会注意到任何问题，因为从它的角度来看，时间将继续正常流动。一旦计时器设法赶上所有错过的 tick，客户机和主机中的时间应该匹配。merge 将错过的 tick(s) 合并为一个 tick 并注入。客户机时间可能会延迟，具体取决于 OS 对 tick 合并的反应 discard 丢弃错过的 tick 并正常继续未来的注入。客户机 OS 将看到计时器一次性跳转相当大的量，就好像中间的时间块根本不存在一样；不用说，

## 20 [性能监控事件](https://www.libvirt.org/formatdomain.html#id27)

某些平台允许监控虚拟机和其中执行的代码的性能。要启用性能监控事件，您可以在 perf 元素中指定它们，或通过 virDomainSetPerfEvents API 启用它们。然后使用 virConnectGetAllDomainStats API 检索性能值。自 2.0.0 起

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

| 事件名称 | 描述 | 统计参数名称 |
| --- | --- | --- |
| cmt | 平台上运行的应用程序对 l3 缓存的使用（字节） | perf.cmt |
| mbmt | 来自一级缓存的总系统带宽 | perf.mbmt |
| mbml | 内存控制器的内存流量带宽 | perf.mbml |
| cpu_cycles | CPU 周期计数（总/经过） | perf.cpu_cycles |
| instructions | 平台上运行的应用程序的指令计数 | perf.instructions |
| cache_references | 平台上运行的应用程序的缓存命中计数 | perf.cache_references |
| cache_misses | 平台上运行的应用程序的缓存未命中计数 | perf.cache_misses |
| branch_instructions | 平台上运行的应用程序的分支指令计数 | perf.branch_instructions |
| branch_misses | 平台上运行的应用程序的分支未命中计数 | perf.branch_misses |
| bus_cycles | 平台上运行的应用程序的总线周期计数 | perf.bus_cycles |
| stalled_cycles_frontend | 平台上运行的应用程序在指令处理器管道前端的停滞 CPU 周期计数 | perf.stalled_cycles_frontend |
| stalled_cycles_backend | 平台上运行的应用程序在指令处理器管道后端的停滞 CPU 周期计数 | perf.stalled_cycles_backend |
| ref_cpu_cycles | 平台上运行的应用程序不受 CPU 频率缩放影响的总 CPU 周期计数 | perf.ref_cpu_cycles |
| cpu_clock | 平台上运行的应用程序通过单调高分辨率每 CPU 计时器测量的 CPU 时钟时间计数 | perf.cpu_clock |
| task_clock | 平台上运行的应用程序特定于运行任务的单调高分辨率 CPU 计时器测量的任务时钟时间计数 | perf.task_clock |
| page_faults | 平台上运行的应用程序的页面错误计数。这包括次要、主要、无效和其他类型的页面错误 | perf.page_faults |
| context_switches | 平台上运行的应用程序的上下文切换计数 | perf.context_switches |
| cpu_migrations | 平台上运行的应用程序的 CPU 迁移计数，即进程从一个逻辑处理器移动到另一个逻辑处理器的情况 | perf.cpu_migrations |
| page_faults_min | 平台上运行的应用程序的次要页面错误计数，即页面存在于页面缓存中，因此故障避免了从存储中加载它 | perf.page_faults_min |
| page_faults_maj | 平台上运行的应用程序的主要页面错误计数，即页面不存在于页面缓存中，因此必须从存储中获取 | perf.page_faults_maj |
| alignment_faults | 平台上运行的应用程序的对齐故障计数，即加载或存储未正确对齐的情况 | perf.alignment_faults |
| emulation_faults | 平台上运行的应用程序的仿真故障计数，即内核捕获未实现的指令并为用户空间仿真它们的情况 | perf.emulation_faults |

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

  emulator 元素的内容指定设备模型模拟器二进制文件的完全限定路径。[功能 XML](https://www.libvirt.org/formatcaps.html) 指定了每种特定域类型/架构组合推荐使用的默认模拟器。

为了帮助用户识别他们关心的设备，每个设备都可以有直接子元素 alias，然后该元素有 name 属性，用户可以在其中存储设备的标识符。标识符必须有 "ua-" 前缀，并且在域内必须是唯一的。此外，标识符只能由以下字符组成：[a-zA-Z0-9_-]。自 3.9.0 起

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

### 21.1 [硬盘、软盘、CD-ROM](https://www.libvirt.org/formatdomain.html#id29)

任何看起来像磁盘的设备，无论是软盘、硬盘、CD-ROM 还是半虚拟化驱动程序，都通过 disk 元素指定。

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
    <source protocol="http" name="url_path" query="foo=bar&amp;baz=flurb>
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

  disk 元素是描述磁盘的主要容器，支持以下属性：type 有效值为 "file"、"block"、"dir"（自 0.7.5 起）、"network"（自 0.8.7 起）、"volume"（自 1.0.5 起）、"nvme"（自 6.0.0 起）、"vhostuser"（自 7.1.0 起）、"vhostvdpa"（自 9.8.0 起（QEMU 8.1.0））或 "ctl"（自 12.0.0 起），并引用磁盘的底层源。自 0.0.3 起 device 指示磁盘如何向客户机 OS 公开。此属性的可能值为 "floppy"、"disk"、"cdrom" 和 "lun"，默认为 "disk"。使用 "lun"（自 0.9.10 起）仅在 type 为 "block" 或 protocol='iscsi' 的 "network" 时有效，或当 type 为 "volume" 且使用 iSCSI 源池用于 mode "host" 或作为使用光纤通道存储池的 [NPIV](https://wiki.libvirt.org/page/NPIV_in_libvirt) 虚拟主机总线适配器 (vHBA) 时有效。以这种方式配置，LUN 的行为与 "disk" 完全相同，除了来自客户机的通用 SCSI 命令被接受并传递到物理设备。另请注意，device='lun' 仅对实际原始设备有效，而永远不会对单个分区或 LVM 分区有效（在这些情况下，内核将拒绝通用 SCSI 命令，使其与 device='disk' 相同）。自 0.1.4 起 model 指示磁盘的仿真设备模型。通常这仅由 bus 属性指示。对于 bus "virtio"，模型可以进一步指定为 "virtio"、"virtio-transitional" 或 "virtio-non-transitional"。有关更多详细信息，请参阅 [virtio 设备模型](https://www.libvirt.org/formatdomain.html#virtio-device-models)。自 5.2.0 起 对于 bus "usb"，模型可以进一步指定为 usb-storage 或 usb-bot。对于 <disk type='disk'>，这两个模型之间没有区别。然而，对于配置为 <disk type='cdrom'> 的设备，usb-bot 会将其正确公开为客户机 OS 内的 cdrom 设备。不幸的是，这种配置与 usb-storage 不兼容，并且

- source

  磁盘源的表示取决于磁盘 type 属性值，如下所示：file file 属性指定包含磁盘的文件的完全限定路径。自 0.0.3 起 自 9.0.0 起，可以添加新的可选属性 fdgroup，指示通过通过 virDomainFDAssociate() API 与域对象关联的文件描述符访问磁盘，而不是打开文件。这些文件不一定必须通过文件系统可由 libvirt 访问。通过 file 传递的文件名仍然可用于在执行块操作时生成写入映像元数据的路径，但 libvirt 不会本地访问这些路径。block dev 属性指定用作磁盘的主机设备的完全限定路径。自 0.0.3 起 dir dir 属性指定用作磁盘的目录的完全限定路径。自 0.7.5 起 请注意，大多数支持 dir 磁盘的 hypervisor 通过公开带有填充了配置目录内容的仿真文件系统的仿真块设备来实现这一点。由于客户机操作系统可能会缓存文件系统元数据，对目录的外部更改可能不会出现在客户机中和/或可能导致从 VM 可观察到损坏的数据。仿真文件系统的格式由 <driver> 驱动程序元素的 format 属性控制。目前仅支持 fat 格式。Hypervisor 可能只支持 <readonly/> 模式。network protocol 属性指定访问请求映像的协议。可能的值为 "nbd"、"iscsi"、"rbd"、"sheepdog"、"gluster"、"vxhs"、"nfs"、"http"、"https"、"ftp"、"ftps"、"tftp" 或 "ssh"。对于 nbd 以外的任何协议，必须使用附加属性 name 来指定将使用哪个卷/映像。对于 "nbd"，name 属性是可选的。可以通过将 tls 属性设置为 yes 来启用 NBD 的 TLS 传输。对于 QEMU hypervisor，TLS 环境的使用也可以通过 nbd_tls 和 nbd

  | 协议 | 含义 | 主机数量 | 默认端口 |
  | --- | --- | --- | --- |
  | nbd | 运行 nbd-server 的服务器 | 只有一个 | 10809 |
  | iscsi | iSCSI 服务器 | 只有一个 | 3260 |
  | rbd | RBD 的监控服务器 | 一个或多个 | librados 默认 |
  | sheepdog | sheepdog 服务器之一（默认是 localhost:7000） | 零或一个 | 7000 |
  | gluster | 运行 glusterd 守护进程的服务器 | 一个或多个（自 2.1.0 起），之前仅一个 | 24007 |
  | vxhs | 运行 Veritas HyperScale 守护进程的服务器 | 只有一个 | 9999 |
  | nfs | 运行网络文件系统的服务器 | 只有一个（自 7.0.0 起） | 必须省略 |
  gluster 支持 "tcp"、"rdma"、"unix" 作为 transport 属性的有效值。nbd 支持 "tcp" 和 "unix"。其他仅支持 "tcp"。如果未指定，默认假设为 "tcp"。如果 transport 为 "unix"，则 socket 属性指定 AF_UNIX 套接字的路径。nfs 仅支持使用 "tcp" 传输，并且完全不支持使用端口，因此必须省略。

  snapshot snapshot 元素的 name 属性可以可选地指定要用作存储协议源的内部快照名称。自 1.2.11 起支持 'rbd'（仅 QEMU）。config config 元素的 file 属性提供配置文件的完全限定路径，作为网络存储协议客户端的参数。自 1.2.11 起支持 'rbd'（仅 QEMU）。auth 自 3.9.0 起，对于使用带有 protocol 属性 "rbd"、"iscsi" 或 "ssh" 的 source 元素的 disk type "network"，支持 auth 元素。如果存在，auth 元素提供访问源所需的认证凭据。它包括一个强制性的 username 属性，标识认证期间使用的用户名，以及一个带有强制性 type 属性的 secret 子元素，以关联到持有实际密码或其他凭据的 [libvirt 密钥对象](https://www.libvirt.org/formatsecret.html)（域 XML 故意不暴露密码，只暴露对管理密码的对象的引用）。已知的密钥类型是 Ceph RBD 网络源的 "ceph" 和 iSCSI 目标的 CHAP 认证的 "iscsi"。两者都需要带有密钥对象 UUID 的 uuid 属性或与密钥对象中指定的键匹配的 usage 属性。encryption 自 3.9.0 起，encryption 可以是加密存储源的 source 元素的子元素。如果存在，指定存储源如何加密 有关更多信息，请参阅 [存储加密](https://www.libvirt.org/formatstorageencryption.html) 页面。请注意，'qcow' 加密格式已损坏，因此不再支持用于磁盘映像。（自 4.5.0 起）reservations 自 4.4.0 起，reservations 可以是存储源的 source 元素的子元素（仅 QEMU 驱动程序）。如果存在，它启用基于 SCSI 的磁盘的持久预留。该元素有一个

- backingStore

  此元素描述由同级 source 元素指定的磁盘使用的后端存储。自 1.2.4 起。如果 hypervisor 驱动程序不支持 [backingStoreInput](https://www.libvirt.org/formatdomaincaps.html#backingstoreinput)（自 5.10.0 起）域功能，则 backingStore 在输入时被忽略，仅用于输出来描述运行域的检测到的后端链。如果支持 backingStoreInput，则 backingStore 用作 source 或其他 backingStore 的后端映像，覆盖映像元数据中记录的任何后端映像信息。空的 backingStore 元素意味着同级 source 是自包含的，不基于任何后端存储。为了使检测到的后端链信息准确，必须在链中每个文件的元数据中正确指定后端格式（libvirt 创建的文件满足此属性，但使用现有的外部文件进行快照或块复制操作需要最终用户正确预创建文件）。backingStore 支持以下属性：type type 属性表示后端存储使用的磁盘类型，有关更多详细信息和可能的值，请参阅上面的 disk type 属性。index 此属性仅在输出中有效（在输入时被忽略），可用于在执行块操作（例如通过 virDomainBlockRebase API）时引用磁盘链的特定部分。例如，vda[2] 引用目标为 vda 的磁盘的 index='2' 的后端存储。 此外，backingStore 支持以下子元素：format format 元素包含 type 属性，指定后端存储的内部格式，如 raw 或 qcow2。format 元素可以包含 metadata_cache 子元素，其语义与磁盘驱动程序的同名子元素相同。source 此元素与 disk 中的 source 元素具有相同的结构。它指定包含数据的文件、设备或网络位置

- mirror

  如果 hypervisor 已启动长时间运行的块作业操作，则存在此元素，其中 source 子元素中的镜像位置最终将具有与源相同的内容，并且子元素 format 中的文件格式（可能与源的格式不同）。source 子元素的详细信息由 mirror 的 type 属性确定，类似于整个磁盘设备元素的处理方式。job 属性提及哪个 API 启动了操作（"copy" 用于 virDomainBlockRebase API，或 "active-commit" 用于 virDomainBlockCommit API），自 1.2.7 起。如果存在 ready 属性，它会跟踪作业的进度：如果磁盘已知已准备好进行 pivot，则为 yes，或者自 1.2.7 起，如果作业正在完成过程中，则为 abort 或 pivot。如果 ready 不存在，磁盘可能仍在复制。目前，此元素仅在输出中有效；在输入时被忽略。自 1.2.6 起，所有两阶段作业都存在 source 子元素。较旧的 libvirt 仅支持块复制到文件，自 0.9.12 起；为了与较旧的客户端兼容，此类作业在 mirror 元素的 file 和 format 属性中包含冗余信息。

- target

  target 元素控制磁盘在客户机 OS 下暴露的总线/设备。dev 属性指示 "逻辑" 设备名称。指定的实际设备名称不保证映射到客户机 OS 中的设备名称。将其视为设备排序提示。可选的 bus 属性指定要仿真的磁盘设备类型；可能的值特定于驱动程序，典型值为 "ide"、"scsi"、"virtio"、"xen"、"usb"、"sata"、"sd" 或 "nvme" "sd" 自 1.1.2 起，"nvme" 自 11.5.0 起。如果省略，总线类型从设备名称的样式推断（例如，名为 'sda' 的设备通常使用 SCSI 总线导出）。可选的 tray 属性指示可移动磁盘（即 CDROM 或软盘）的托盘状态，值可以是 "open" 或 "closed"，默认为 "closed"。注意，tray 的值可以在域运行时更新。可选的 removable 属性为 USB 或 SCSI 磁盘设置可移动标志，其值可以是 "on" 或 "off"，默认为 "off"。可选的 rotation_rate 属性为 SCSI、IDE 或 SATA 总线上的磁盘设置存储的旋转速率。范围 1025 到 65534 的值用于表示旋转介质速度（以每分钟转数为单位）。值 1 用于表示固态或其他非旋转存储。这些值不需要与底层主机存储的值匹配。自 0.0.3 起；bus 属性自 0.4.3 起；tray 属性自 0.9.11 起；"usb" 属性值自 0.4.4 之后起；"sata" 属性值自 0.9.7 起；"removable" 属性值自 1.1.3 起；"rotation_rate" 属性值自 7.3.0 起 可选属性 dpofua（自 11.10.0 起，仅 QEMU 驱动程序）控制 SCSI 磁盘缓存访问的 DPO（禁用页出）和 FUA（强制单元访问）属性的支持（两者必须同时存在或不存在）。如果省略该值，则应用 hypervisor 默认值（可能取决于机器类型版本），这是建议的

- throttlefilters

  可选的 throttlefilters 元素提供了提供额外的每设备限制链的能力 自 11.2.0 起 例如，如果我们有四个不同的磁盘，我们希望限制每个磁盘的 I/O，并且我们还希望限制所有四个磁盘的组合 I/O，我们可以通过为每个磁盘设置两个 throttlefilter 来利用 throttlefilters 实现这一目标：磁盘自己的过滤器（例如 limit2）和组合过滤器（例如 limit012）。throttlefilter 在 throttlefilters 中的顺序无关紧要。throttlefilters 和 iotune 应独占使用。throttlefilter 可选的 throttlefilter 元素用于引用定义的限制组。

- iotune

  可选的 iotune 元素提供了提供额外的每设备 I/O 调优的能力，每个设备的值可以不同（与 blkiotune 元素（请参阅 [块 I/O 调优](https://www.libvirt.org/formatdomain.html#block-i-o-tuning)）形成对比，后者全局应用于域）。目前，唯一可用的调优是 qemu 的块 I/O 限制。此元素有可选的子元素；任何未指定或值为 0 的子元素都意味着无限制。自 0.9.8 起 total_bytes_sec 可选的 total_bytes_sec 元素是总吞吐量限制（字节/秒）。这不能与 read_bytes_sec 或 write_bytes_sec 一起出现。read_bytes_sec 可选的 read_bytes_sec 元素是读取吞吐量限制（字节/秒）。write_bytes_sec 可选的 write_bytes_sec 元素是写入吞吐量限制（字节/秒）。total_iops_sec 可选的 total_iops_sec 元素是总 I/O 操作/秒。这不能与 read_iops_sec 或 write_iops_sec 一起出现。read_iops_sec 可选的 read_iops_sec 元素是读取 I/O 操作/秒。write_iops_sec 可选的 write_iops_sec 元素是写入 I/O 操作/秒。total_bytes_sec_max 可选的 total_bytes_sec_max 元素是最大总吞吐量限制（字节/秒）。这不能与 read_bytes_sec_max 或 write_bytes_sec_max 一起出现。read_bytes_sec_max 可选的 read_bytes_sec_max 元素是最大读取吞吐量限制（字节/秒）。write_bytes_sec_max 可选的 write_bytes_sec_max 元素是最大写入吞吐量限制（字节/秒）。total_iops_sec_max 可选的 total_iops_sec_max 元素是最大总 I/O 操作/秒。这不能与 read_iops_sec_max 或 write_iops_sec_max 一起出现。read_iops_sec_max 可选的 read_iops_sec_max 元素是最大读取 I/O 操作/秒。write_iops_sec_max 可选的

- driver

  可选的 driver 元素允许指定与提供磁盘的 hypervisor 驱动程序相关的更多详细信息。自 0.1.8 起 如果 hypervisor 支持多个后端驱动程序，则 name 属性选择主要后端驱动程序名称，而可选的 type 属性提供子类型。例如，xen 支持名称 "tap"、"tap2"、"phy" 或 "file"，类型为 "aio"，而 qemu 仅支持名称 "qemu"，但支持多种类型，包括 "raw"、"bochs"、"qcow2" 和 "qed"。可选的 cache 属性控制缓存机制，可能的值为 "default"、"none"、"writethrough"、"writeback"、"directsync"（自 0.9.5 起；类似于 "writethrough"，但它绕过主机页缓存）和 "unsafe"（自 0.9.7 起；主机可能缓存所有磁盘 I/O，并且忽略来自客户机的同步请求）。自 0.6.0 起 可选的 error_policy 属性控制 hypervisor 在磁盘读写错误时的行为，可能的值为 stop（在错误时挂起/暂停域）、report（向客户机 OS 报告错误；自 0.9.7 起）、ignore（忽略错误并尝试继续）和 enospace（仅在主机存储已满时挂起/暂停域；否则向客户机 OS 报告错误）。默认值由 hypervisor 自行决定。自 0.8.0 起。可选的 rerror_policy 属性仅控制读取错误的行为。如果未给出 rerror_policy，则 error_policy 用于读取和写入错误。如果给出 rerror_policy，它会覆盖读取错误的 error_policy。另请注意，"enospace" 不是读取错误的有效策略，因此如果 error_policy 设置为 "enospace" 且未给出 rerror_policy，则读取错误策略将保持其默认值。自 0.9.7 起 可选的 io 属性控制 I/O 的特定策略；qemu 客户机支持 "threads" 和 "native" 自 0.8.8 起，io_uring 自 6.3.0 起（QEMU 5.0）。可选的 ioeventfd 属性允许用户设置 [域 I/O 异步处理](https://patchwork.kernel.org/patc

- backenddomain

  可选的 backenddomain 元素允许指定托管磁盘的后端域（也称为驱动程序域）。使用 name 属性指定后端域名称。自 1.2.13 起（仅 Xen）

- boot

  指定磁盘是可启动的。order 属性确定引导序列期间尝试设备的顺序。在 S390 架构上，仅使用第一个引导设备。可选的 loadparm 属性是一个 8 字符字符串，S390 上的客户机可以通过 sclp 或 diag 308 查询。S390 上的 Linux 客户机可以使用 loadparm 选择引导条目。自 3.5.0 起 每设备引导元素不能与 [客户机固件](https://www.libvirt.org/formatdomain.html#guest-firmware) 部分中的一般引导元素一起使用。自 0.8.8 起

- encryption

  自 3.9.0 起，encryption 元素首选作为 source 元素的子元素。如果存在，指定卷如何使用 "qcow" 加密。有关更多信息，请参阅 [存储加密](https://www.libvirt.org/formatstorageencryption.html) 页面。

- readonly

  如果存在，这表示设备不能被客户机修改。目前，这是 attribute device='cdrom' 的磁盘的默认值。

- shareable

  如果存在，这表示设备预计在域之间共享（假设 hypervisor 和 OS 支持这一点），这意味着应该为该设备停用缓存。

- transient

  如果存在，这表示当客户机退出时，对设备内容的更改应自动恢复。对于某些 hypervisor，将磁盘标记为 transient 会阻止域参与迁移、快照或块作业。仅在 vmx hypervisor（自 0.9.5 起）和 qemu hypervisor（自 6.9.0 起）中支持。如果 <transient/> 磁盘的源映像应该在多个并发运行的 VM 之间共享，则应将可选的 shareBacking 属性设置为 yes。注意，hypervisor 驱动程序可能需要热插拔此类磁盘，因此它仅适用于支持热插拔的配置。自 7.4.0 起 Hypervisor 可能需要存储包含域在运行时写入的数据的临时文件，该文件可能存储在与磁盘原始源相同的位置（qemu 驱动程序将临时文件存储为 $(origsource).TRANSIENT-$(vmname)，其中 $(origsource) 是磁盘源的完整原始路径，$(vmname) 是域的名称）。

- serial

  如果存在，这指定虚拟硬盘的序列号。例如，它可能看起来像 <serial>WD-WMAP9A966149</serial>。不支持 scsi-block 设备，即那些在总线上使用 device 'lun' 的 disk type 'block'。也不支持同一控制器上的多个 NVMe 设备，因为它们每个控制器有一个序列号，而不是每个磁盘。自 0.7.1 起 请注意，根据 hypervisor 和设备类型，序列号可能会被静默截断。IDE/SATA 设备通常限制为 20 个字符。SCSI 设备根据 hypervisor 版本限制为 20、36 或 247 个字符。Hypervisor 将来也可能开始拒绝过长的序列号，而不是截断它们，因此建议通过使用所需的设备和 hypervisor 组合测试所需的序列号长度范围来避免隐式截断。

- wwn

  如果存在，此元素指定虚拟硬盘或 CD-ROM 驱动器的 WWN（全球名称）。它必须由 16 个十六进制数字组成。自 0.10.1 起

- vendor

  如果存在，此元素指定虚拟硬盘或 CD-ROM 设备的供应商。它不得超过 8 个可打印字符。仅适用于 'scsi' 总线。自 1.0.1 起

- product

  如果存在，此元素指定虚拟硬盘或 CD-ROM 设备的产品。对于 'scsi'，它不得超过 16 个可打印字符（自 1.0.1 起）。对于 'sata' 或 'ide'，不得超过 40 个可打印字符（自 11.1.0 起）。不支持其他总线。

- address

  如果存在，address 元素将磁盘绑定到控制器的给定插槽（实际的 <controller> 设备通常可以由 libvirt 推断，尽管可以显式指定。请参阅 [控制器](https://www.libvirt.org/formatdomain.html#controllers)）。type 属性是强制性的，通常为 "pci" 或 "drive"。对于 "pci" 控制器，必须存在 bus、slot 和 function 的附加属性，以及可选的 domain 和 multifunction（自 0.9.7 起）。Multifunction 默认为 'off'。对于 "drive" 控制器，控制器、总线、target（自 0.9.11 起）和 unit 的附加属性可用，每个默认为 0。

- auth

  自 3.9.0 起，auth 元素首选作为 source 元素的子元素。该元素仍作为 disk 子元素读取和管理。将 auth 同时用作 disk 和 source 的子元素是无效的。自 0.9.7 起

- geometry

  可选的 geometry 元素提供了覆盖几何设置的能力。这主要对 S390 DASD 磁盘或较旧的 DOS 磁盘有用。自 0.10.0 起 cyls cyls 属性是柱面数。heads heads 属性是磁头数。secs secs 属性是每磁道的扇区数。trans 可选的 trans 属性是 BIOS 转换模式（none、lba 或 auto）

- blockio

  如果存在，blockio 元素允许覆盖下面列出的任何块设备属性。自 0.10.2 起（QEMU 和 KVM） logical_block_size 磁盘将向客户机 OS 报告的逻辑块大小。对于 Linux，这将是 BLKSSZGET ioctl 返回的值，描述磁盘 I/O 的最小单位。physical_block_size 磁盘将向客户机 OS 报告的物理块大小。对于 Linux，这将是 BLKPBSZGET ioctl 返回的值，描述磁盘的硬件扇区大小，这可能与磁盘数据的对齐有关。discard_granularity 可以在单个操作中丢弃的最小数据量。它影响 unmap 操作，并且必须是 logical_block_size 的倍数。这通常由 hypervisor 正确配置。

### 21.2 [文件系统](https://www.libvirt.org/formatdomain.html#id30)

可以从客户机直接访问的主机上的目录。自 0.3.3 起，QEMU/KVM 自 0.8.5 起

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
  | gluster | 运行 glusterd 守护程序的服务器 | 一个或多个（自 2.1.0 起），在此之前只有一个 | 24007 |