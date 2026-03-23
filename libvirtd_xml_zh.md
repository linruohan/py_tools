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
</perf>
...
```

- perf

  perf 元素是性能监控事件的容器。

- event

  event 元素定义了一个性能监控事件。name 属性指定事件的名称，enabled 属性指定事 件是否启用。

## 21 [设备](https://www.libvirt.org/formatdomain.html#id28)

### 21.2 [文件系统](https://www.libvirt.org/formatdomain.html#id30)

主机上的目录可以从客户机直接访问。自 0.3.3 起，QEMU/KVM 自 0.8.5 起

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

  filesystem 属性 type 指定源的类型。可能的值包括：mount 要在客户机中挂载的主机目录。由 LXC、OpenVZ（自 0.6.2 起）和 QEMU/KVM（自 0.8.5 起）使用。如果未指定，这是默认类型。此模式还有一个可选的子元素 driver，其属性 type='path' 或 type='handle'（自 0.9.7 起）。driver 块有一个可选的属性 wrpolicy，用于进一步控制与主机页面缓存的交互；省略该属性会提供默认行为，而值 immediate 表示在客户机文件写入操作期间触及的所有页面会立即触发主机写回（自 0.9.10 起）。自 6.2.0 起，还支持 type='virtiofs'。使用 virtiofs 需要设置共享内存，请参阅指南：[Virtiofs](https://www.libvirt.org/kbase/virtiofs.html) template OpenVZ 文件系统模板。仅由 OpenVZ 驱动程序使用。file 主机文件将被视为映像并在客户机中挂载。文件系统格式将被自动检测。仅由 LXC 驱动程序使用。block 要在客户机中挂载的主机块设备。文件系统格式将被自动检测。仅由 LXC 驱动程序使用（自 0.9.5 起）。ram 内存文件系统，使用来自主机 OS 的内存。source 元素有一个属性 usage，用于指定内存使用限制（以 KiB 为单位），除非 units 属性指定了单位。仅由 LXC 驱动程序使用。（自 0.9.13 起）bind 客户机内的目录将绑定到客户机内的另一个目录。仅由 LXC 驱动程序使用（自 0.9.13 起） filesystem 元素有一个可选的属性 accessmode，用于指定访问源的安全模式（自 0.8.5 起）。目前，这仅适用于 QEMU/KVM 驱动程序的 type='mount'。对于驱动程序类型 virtiofs，仅支持 passthrough。对于其他驱动程序类型，可能的值为：passthrough 源以客户机内用户的权限访问。如果未指定，这是默认的 accessmode。mapped 源以 QEMU 进程的权限访问，UID/GID 从客户机映射到主机。squash 与 mapped 类似，但将客户机的 root 用户映射到主机上的非特权用户。

- driver

  可选的 driver 元素允许指定与用于提供文件系统的 hypervisor 驱动程序相关的更多详细信息。自 1.0.6 起 如果 hypervisor 支持多个后端驱动程序，则 type 属性选择主要后端驱动程序名称，而 format 属性提供格式类型。例如，LXC 支持类型为 "loop"，格式为 "raw" 或 "nbd"（具有任何格式）。QEMU 支持类型为 "path" 或 "handle"，但没有格式。Virtuozzo 驱动程序支持类型为 "ploop"，格式为 "ploop"。对于 virtio 后端设备，还可以设置 [Virtio 相关选项](https://www.libvirt.org/formatdomain.html#virtio-related-options)。（自 3.5.0 起）对于 virtiofs，可以使用 queue 属性指定队列大小（即队列可以容纳多少请求）。（自 6.2.0 起）QEMU 支持 mtp，它向客户机公开虚拟 USB MTP 设备。（自 10.2.0 起）

- binary

  可选的 binary 元素可以调整 virtiofsd 的选项。以下所有属性和元素都是可选的。属性 path 可用于覆盖守护程序的路径。属性 xattr 启用文件系统扩展属性的使用。缓存可以通过 cache 元素进行调整，可能的模式值为 none 和 always。锁定可以通过 lock 元素控制 - 属性 posix 和 flock 都接受值 on 或 off。（自 6.2.0 起）virtiofsd 使用的沙箱方法可以通过 sandbox 元素配置，可能的模式值为 namespace 和 chroot，请参阅 [virtiofsd 文档](https://qemu.readthedocs.io/en/latest/tools/virtiofsd.html) 了解更多详细信息。（自 7.2.0 起）元素 thread_pool 接受一个属性 size，用于定义最大线程池大小。值 "0" 禁用池。线程池有助于在使用具有较高延迟的存储时增加正在处理的请求数量。但是，它有开销，因此对于快速、低延迟的文件系统，最好将其关闭。（自 8.5.0 起）元素 openfiles 接受一个属性 max，用于定义文件描述符的最大数量。非正值是禁止的。打开文件数量的上限是由实现定义的。（自 10.6.0 起）

- source

  主机上在客户机中访问的资源。name 属性必须与 type='template' 一起使用，dir 属性必须与 type='mount' 一起使用。对于 virtiofs，可以使用 socket 属性连接到在 libvirt 外部启动的 virtiofsd 守护程序。在这种情况下，target 元素不适用，大多数 virtiofs 相关选项也不适用，因为它们由 virtiofsd 而不是 libvirtd 控制。usage 属性与 type='ram' 一起使用，用于设置内存限制（以 KiB 为单位），除非 units 属性指定了单位。

- target

  源在客户机中的访问位置。对于大多数驱动程序，这是一个自动挂载点，但对于 QEMU/KVM，这只是一个任意字符串标签，作为挂载位置的提示导出到客户机。

- idmap

  对于 virtiofs，可以指定 idmap 元素来映射用户命名空间中的 ID。有关元素的语法，请参阅 [容器引导](https://www.libvirt.org/formatdomain.html#container-boot) 部分。自 10.0.0 起

- readonly

  启用将文件系统作为只读挂载导出给客户机，默认情况下提供读写访问（适用于 QEMU/KVM 驱动程序，自 11.0.0 起，需要 virtiofs 1.13.0）。

- space_hard_limit

  此客户机文件系统可用的最大空间。自 0.9.13 起仅由 OpenVZ 驱动程序支持。

- space_soft_limit

  此客户机文件系统可用的最大空间。容器允许在宽限期内超过其软限制。之后将强制执行硬限制。自 0.9.13 起仅由 OpenVZ 驱动程序支持。

### 21.3 [设备地址](https://www.libvirt.org/formatdomain.html#id31)

许多设备都有一个可选的 <address> 子元素，用于描述设备在呈现给客户机的虚拟总线上的位置。如果在输入时省略地址（或地址内的任何可选属性），libvirt 将生成适当的地址；但如果需要对布局进行更多控制，则需要明确的地址。请参阅下面的包含地址元素的设备示例。

每个地址都有一个必需的属性 type，用于描述设备所在的总线。为给定设备选择使用哪个地址部分受设备和客户机架构的约束。例如，<disk> 设备使用 type='drive'，而 <console> 设备在 i686 或 x86_64 客户机上使用 type='pci'，或在 PowerPC64 pseries 客户机上使用 type='spapr-vio'。每种地址类型都有进一步的可选属性，用于控制设备在总线上的放置位置：

- pci

  PCI 地址具有以下附加属性：domain（2 字节十六进制整数，当前未被 qemu 使用）、bus（十六进制值，介于 0 和 0xff 之间，包括 0 和 0xff）、slot（十六进制值，介于 0x0 和 0x1f 之间，包括 0x0 和 0x1f）和 function（值介于 0 和 7 之间，包括 0 和 7）。还可以使用 multifunction 属性，用于控制在 PCI 控制寄存器中为特定槽/功能打开多功能位（自 0.9.7 起，需要 QEMU 0.13）。multifunction 默认为 'off'，但对于将使用多个功能的槽的功能 0，应设置为 'on'。（自 4.10.0 起），支持取决于架构的 PCI 地址扩展。例如，S390 客户机的 PCI 地址将具有 zpci 子元素，带有两个属性：uid（十六进制值，介于 0x0001 和 0xffff 之间，包括 0x0001 和 0xffff）和 fid（十六进制值，介于 0x00000000 和 0xffffffff 之间，包括 0x00000000 和 0xffffffff），由 S390 上的 PCI 设备用于用户定义标识符和功能标识符。自 1.3.5 起，一些 hypervisor 驱动程序可能接受 <address type='pci'/> 元素，没有其他属性，作为为设备分配 PCI 地址的明确请求，而不是可能也适用于同一设备的其他类型的地址（例如 virtio-mmio）。在域 XML 中配置的 PCI 地址与客户机 OS 看到的地址之间的关系有时可能看起来令人困惑：单独的文档更详细地描述了 [PCI 地址如何工作](https://www.libvirt.org/pci-addresses.html)。

- drive

  驱动器地址具有以下附加属性：controller（2 位控制器编号）、bus（2 位总线编号）、target（2 位目标编号）和 unit（总线上的 2 位单元编号）。

- virtio-serial

  每个 virtio-serial 地址具有以下附加属性：controller（2 位控制器编号）、bus（2 位总线编号）和 slot（总线内的 2 位槽）。

- ccid

  智能卡的 CCID 地址具有以下附加属性：bus（2 位总线编号）和 slot 属性（总线内的 2 位槽）。自 0.8.8 起。

- usb

  USB 地址具有以下附加属性：bus（十六进制值，介于 0 和 0xfff 之间，包括 0 和 0xfff）和 port（最多四个八位字节的点分表示法，例如 1.2 或 2.1.3.1）。

- spapr-vio

  在 PowerPC pseries 客户机上，设备可以分配到 SPAPR-VIO 总线。它有一个扁平的 32 位地址空间；按照惯例，设备通常分配在 0x00001000 的非零倍数处，但其他地址也是有效的，并被 libvirt 允许。每个地址具有以下附加属性：reg（起始寄存器的十六进制值地址）。自 0.9.9 起。

- ccw

  机器值为 s390-ccw-virtio 的 S390 客户机使用本机 CCW 总线进行 I/O 设备。CCW 总线地址具有以下附加属性：cssid（十六进制值，介于 0 和 0xfe 之间，包括 0 和 0xfe）、ssid（值介于 0 和 3 之间，包括 0 和 3）和 devno（十六进制值，介于 0 和 0xffff 之间，包括 0 和 0xffff）。不允许部分指定的总线地址。如果省略，libvirt 将分配一个空闲的总线地址，cssid=0xfe 和 ssid=0。Virtio-ccw 设备必须将其 cssid 设置为 0xfe。自 1.0.4 起

- virtio-mmio

  这将设备放置在 virtio-mmio 传输上，目前仅适用于某些 armv7l 和 aarch64 虚拟机。virtio-mmio 地址没有任何附加属性。自 1.1.3 起 如果客户机架构是 aarch64 且机器类型是 virt，libvirt 将自动为设备分配 PCI 地址；但是，客户机配置中存在单个带有 virtio-mmio 地址的设备将导致 libvirt 为所有其他设备分配 virtio-mmio 地址。自 3.0.0 起

- isa

  ISA 地址具有以下附加属性：iobase 和 irq。自 1.2.1 起

- unassigned

  对于 PCI hostdev，<address type='unassigned'/> 允许管理员在域 XML 定义中包含 PCI hostdev，而不使其对客户机可用。这允许在其中 Libvirt 将设备作为常规 PCI hostdev 管理的配置，无论客户机是否可以访问它。<address type='unassigned'/> 对所有其他设备类型是无效的地址类型。自 6.0.0 起

### 21.4 [Virtio 相关选项](https://www.libvirt.org/formatdomain.html#id32)

QEMU 的 virtio 设备在 driver 元素下有一些与 virtio 传输相关的属性：iommu 属性启用设备对模拟 IOMMU 的使用。ats 属性控制 PCIe 设备的地址转换服务支持。这是使用 IOTLB 支持所必需的（请参阅 [IOMMU 设备](https://www.libvirt.org/formatdomain.html#iommu-devices)）。可能的值为 on 或 off。自 3.5.0 起

packed 属性控制 QEMU 是否应尝试使用打包 virtqueue。与常规分离队列相比，打包队列仅由单个描述符环组成，替换可用和已使用的环、索引和描述符缓冲区。这可以导致更好的缓存利用率和性能。是否实际使用打包 virtqueue 取决于 QEMU、vhost 后端和客户机驱动程序之间的功能协商。可能的值为 on 或 off。自 6.3.0 起（仅 QEMU 和 KVM）

此可选属性 page_per_vq 控制暴露给客户机的通知功能的布局。启用时，每个 virtio 队列将在暴露给客户机的设备 BAR 上有一个专用页面。建议在 hypervisor 上启用 vDPA 时使用，因为它允许将通知区域映射到物理设备，这仅在页面粒度上支持。默认值由 QEMU 确定。自 7.9.0 起（QEMU 2.8）注意：一般情况下，您应该保持此选项不变，除非您非常确定自己在做什么。

### 21.5 [Virtio 设备模型](https://www.libvirt.org/formatdomain.html#id33)

Virtio 设备有几种变体，其中一些仅适用于特定的机器类型或场景。可以通过 model 属性选择变体，该属性支持以下值：

- virtio

  这是在没有客户机 OS 特定约束的情况下的推荐选择，因为它通常可以在各种架构、机器类型和 libvirt 版本上正常工作。

自 5.2.0 起，以下值还可以与基于 PCI 的机器类型（常规 PCI 或 PCI Express）一起使用：

- virtio-transitional

  此设备可以同时与 virtio 0.9 和 virtio 1.0 客户机驱动程序一起工作，因此当需要与较旧的客户机操作系统兼容时，它是最佳选择。libvirt 将设备插入常规 PCI 槽。

- virtio-non-transitional

  此设备只能与 virtio 1.0 客户机驱动程序一起工作，除非需要与较旧的客户机操作系统兼容，否则它是推荐选项。libvirt 将根据机器类型将设备插入 PCI Express 槽或常规 PCI 槽，从而产生更优化的 PCI 拓扑。

虽然上面概述的信息适用于大多数 virtio 设备，但有一些例外：

- 对于 SCSI 控制器，由于历史原因，没有可用的 virtio 模型：请改用 virtio-scsi，它的行为与其他设备的 virtio 相同。virtio-transitional 和 virtio-non-transitional 都适用于 SCSI 控制器；
- 某些设备，如 GPU 和输入设备（键盘、平板电脑和鼠标），仅在 virtio 1.0 规范中定义，因此没有过渡变体：唯一接受的模型是 virtio，这将导致非过渡设备。

有关更多详细信息，请参阅 [qemu patch posting](https://lists.gnu.org/archive/html/qemu-devel/2018-12/msg00923.html) 和 [virtio-1.0 规范](https://docs.oasis-open.org/virtio/virtio/v1.0/virtio-v1.0.html)。

### 21.6 [控制器](https://www.libvirt.org/formatdomain.html#id34)

根据客户机架构，某些设备总线可能出现多次，一组虚拟设备绑定到一个虚拟控制器。通常，libvirt 可以自动推断这些控制器，而不需要显式的 XML 标记，但有时需要提供显式的 controller 元素，特别是在规划期望设备热插拔的客户机的 [PCI 拓扑](https://www.libvirt.org/pci-hotplug.html) 时。

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

每个控制器都有一个必需的属性 type，必须是 'ide'、'fdc'、'scsi'、'sata'、'usb'、'ccid'、'virtio-serial' 或 'pci' 之一，以及一个必需的属性 index，它是描述总线控制器遇到顺序的十进制整数（用于 <address> 元素的 controller 属性）。自 1.3.5 起，index 是可选的；如果未指定，它将自动分配为给定控制器类型的最低未使用索引。某些控制器类型有额外的属性来控制特定功能，例如：

- virtio-serial

  virtio-serial 控制器有两个额外的可选属性 ports 和 vectors，用于控制可以通过控制器连接的设备数量。自 5.2.0 起，它支持可选的属性 model，可以是 'virtio'、'virtio-transitional' 或 'virtio-non-transitional'。有关更多详细信息，请参阅 [virtio 设备模型](https://www.libvirt.org/formatdomain.html#virtio-device-models)。

- scsi

  scsi 控制器有一个可选的属性 model，可以是 'auto'、'buslogic'、'ibmvscsi'、'lsilogic'、'lsisas1068'、'lsisas1078'、'virtio-scsi'、'vmpvscsi'、'virtio-transitional'、'virtio-non-transitional'、'ncr53c90'（仅作为内置隐式控制器）、'am53c974'、'dc390'。有关更多详细信息，请参阅 [virtio 设备模型](https://www.libvirt.org/formatdomain.html#virtio-device-models)。

- usb

  usb 控制器有一个可选的属性 model，可以是 "piix3-uhci"、"piix4-uhci"、"ehci"、"ich9-ehci1"、"ich9-uhci1"、"ich9-uhci2"、"ich9-uhci3"、"vt82c686b-uhci"、"pci-ohci"、"nec-xhci"、"qusb1"（带有 qemu 后端的 xen pvusb，版本 1.1）、"qusb2"（带有 qemu 后端的 xen pvusb，版本 2.0）或 "qemu-xhci"。此外，自 0.10.0 起，如果需要为客户机明确禁用 USB 总线，可以使用 model='none'。自 1.0.5 起，s390 上不会构建默认的 USB 控制器。自 1.3.5 起，USB 控制器接受 ports 属性来配置可以连接到控制器的设备数量。

- ide

  自 3.10.0 起，对于 vbox 驱动程序，ide 控制器有一个可选的属性 model，可以是 "piix3"、"piix4" 或 "ich6"。

- xenbus

  自 5.2.0 起，xenbus 控制器有一个可选的属性 maxGrantFrames，用于指定控制器为连接的设备提供的最大授权帧数。自 6.3.0 起，xenbus 控制器支持可选的 maxEventChannels 属性，用于指定客户机可以使用的最大事件通道数（PV 中断）。

- nvme

  自 11.5.0 起支持，nvme 控制器可用于支持 NVMe 磁盘。它有一个可选的 serial 子元素，就像常规磁盘一样。

注意：PowerPC64 "spapr-vio" 地址没有关联的控制器。

对于本身是 PCI 或 USB 总线上的设备的控制器，可选的子元素 <address> 可以指定控制器与其主总线的精确关系，其语义在 [设备地址](https://www.libvirt.org/formatdomain.html#device-addresses) 部分中描述。

可选的子元素 driver 可以指定驱动程序特定的选项：

- queues

  可选的 queues 属性指定控制器的队列数。为获得最佳性能，建议指定与 vCPU 数量匹配的值。自 1.0.5 起（仅 QEMU 和 KVM）

- cmd_per_lun

  可选的 cmd_per_lun 属性指定可以在由主机控制的设备上排队的最大命令数。自 1.2.7 起（仅 QEMU 和 KVM）

- max_sectors

  可选的 max_sectors 属性指定在单个命令中传输到或从设备传输的最大数据量（以字节为单位）。传输长度以扇区为单位测量，其中一个扇区为 512 字节。自 1.2.7 起（仅 QEMU 和 KVM）

- ioeventfd

  可选的 ioeventfd 属性指定控制器是否应使用 [I/O 异步处理](https://patchwork.kernel.org/patch/43390/)。接受的值为 "on" 和 "off"。自 1.2.18 起

- iothread

  自 1.3.5 起（QEMU 2.4），支持使用模型 virtio-scsi 且地址类型为 pci 和 ccw 的控制器类型 scsi。可选的 iothread 属性将控制器分配给 IOThread，该 IOThread 由域 iothreads 的范围定义（请参阅 [IOThreads 分配](https://www.libvirt.org/formatdomain.html#iothreads-allocation)）。分配给使用指定控制器的每个 SCSI 磁盘将使用同一个 IOThread。如果需要为特定 SCSI 磁盘使用特定的 IOThread，则必须定义多个控制器，每个控制器都有特定的 iothread 值。iothread 值必须在 1 到域 iothreads 值的范围内。

- iothreads

  自 11.2.0 起（QEMU 10.0），支持使用地址类型 pci 和 ccw 的 virtio-scsi 控制器。与 iothread 互斥。可选的 iothreads 子元素允许通过 iothread 子元素（带有属性 id）指定多个 IOThread，virtio-scsi 控制器将用于 I/O 操作。virt 队列（请参阅 driver 的 queues 属性）会自动分布在配置的 iothread 之间。可选的 iothread 元素可以有多个 queue 子元素，带有必需的 id 属性，指定该 iothread 应用于处理给定的 virt 队列。如果存在队列映射，则必须配置 driver 的 queues 属性，并且所有配置的 virt 队列必须包含在映射中。virtio-scsi 设备公开请求 virt 队列 0 到 N-1，其中 N 是为设备配置的队列数。示例：`<driver queues='4>  <iothreads>    <iothread id='2'/>    <iothread id='3'/>  </iothreads> </driver> <driver queues='3'>  <iothreads>    <iothread id='2'>      <queue id='1'/>    </iothread>    <iothread id='3'>      <queue id='0'/>      <queue id='2'/>    </iothread>  </iothreads> </driver>`

- virtio 选项

  对于 virtio 控制器，还可以设置 [Virtio 相关选项](https://www.libvirt.org/formatdomain.html#virtio-related-options)。（自 3.5.0 起）

USB 伴生控制器有一个可选的子元素 <master>，用于指定伴生与主控制器的确切关系。伴生控制器与主控制器在同一总线上，因此伴生索引值应相等。并非所有控制器模型都可以用作伴生控制器，libvirt 可能会为某些特定模型提供一些合理的默认值（主 startport 和地址功能的设置）。首选的伴生控制器是 ich-uhci[123]。

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

- pci-root、pci-bridge（自 1.0.5 起）
- pcie-root、dmi-to-pci-bridge（自 1.1.2 起）
- pcie-root-port、pcie-switch-upstream-port、pcie-switch-downstream-port（自 1.2.19 起）
- pci-expander-bus、pcie-expander-bus（自 1.3.4 起）
- pcie-to-pci-bridge（自 4.3.0 起）

根控制器（pci-root 和 pcie-root）有一个可选的 pcihole64 元素，指定 64 位 PCI 孔的大小（以 kiB 为单位，或由 pcihole64 的 unit 属性指定的单位）。当 QEMU 和 Seabios 足够新以支持 64 位 PCI 孔时，某些客户机（如 Windows XP 或 Windows Server 2003）可能会崩溃，除非将其禁用（设置为 0）。自 1.1.2 起（仅 QEMU）

PCI 控制器还有一个可选的子元素 <model>，带有属性 name。name 属性包含 qemu 正在模拟的特定设备的名称（例如 "i82801b11-bridge"），而不仅仅是设备的类（"pcie-to-pci-bridge"、"pci-bridge"），这在控制器元素的 model **属性** 中设置。在几乎所有情况下，您都不应手动向控制器添加 <model> 子元素，也不应修改由 libvirt 自动生成的 <model> 子元素。自 1.2.19 起（仅 QEMU）。

PCI 控制器还有一个可选的子元素 <target>，带有以下属性和子元素。这些是可配置项，1）对客户机 OS 可见，因此必须为客户机 ABI 兼容性而保留，2）通常保留为默认值或由 libvirt 自动派生。在几乎所有情况下，您都不应手动向控制器添加 <target> 子元素，也不应修改由 libvirt 自动生成的 <target> 子元素中的值。自 1.2.19 起（仅 QEMU）。

- chassisNr

  具有属性 model="pci-bridge" 的 PCI 控制器还可以在 <target> 子元素中具有 chassisNr 属性，用于控制 pci-bridge 设备的 QEMU "chassis_nr" 选项（通常 libvirt 自动将其设置为与 pci 控制器的 index 属性相同的值）。如果设置，chassisNr 必须在 1 到 255 之间。

- chassis

  pcie-root-port 和 pcie-switch-downstream-port 控制器还可以在 <target> 子元素中具有 chassis 属性，用于设置控制器的 "chassis" 配置值，该值对虚拟机可见。如果设置，chassis 必须在 0 到 255 之间。

- port

  pcie-root-port 和 pcie-switch-downstream-port 控制器还可以在 <target> 子元素中具有 port 属性，用于设置控制器的 "port" 配置值，该值对虚拟机可见。如果设置，port 必须在 0 到 255 之间。

- hotplug

  pci-root（自 7.9.0 起）、pcie-root-port（自 6.3.0 起）和 pcie-switch-downstream-port 控制器（自 6.3.0 起）还可以在 <target> 子元素中具有 hotplug 属性，用于禁用特定控制器上设备的热插拔/拔出。对于 pci-root 控制器，此设置影响基于 ACPI 的热插拔。对于其他控制器，此设置影响基于 ACPI 的热插拔以及 PCIE 原生热插拔。hotplug 的默认设置为 on；应将其设置为 off 以禁用特定控制器上设备的热插拔/拔出。

- busNr

  pci-expander-bus 和 pcie-expander-bus 控制器可以有一个可选的 busNr 属性（1-254）。这将是新总线的总线编号；从指定值到 255 之间的所有总线编号将仅可用于分配给插入到此扩展总线开始的层次结构中的 PCI/PCIe 控制器，而小于指定值的总线编号将可用于下一个较低的扩展总线（或如果没有较低的扩展总线，则可用于根总线）。如果不指定 busNumber，libvirt 将在所有其他扩展总线中找到最低的现有 busNumber（或如果没有其他扩展总线，则使用 256），并自动分配该找到的总线的 busNr - 2，这为 pci-expander-bus 和自动附加到它的 pci-bridge 提供一个总线编号（如果计划向总线的层次结构添加更多 pci-bridge，则应手动将 busNr 设置为较低的值）。类似的算法用于自动确定 pcie-expander-bus 的 busNr 属性，但由于 pcie-expander-bus 没有任何内置的 pci-bridge，第二个总线编号只是为必须连接到总线才能实际插入端点设备的 pcie-root-port 保留。如果打算将多个设备插入 pcie-expander-bus，则必须将 pcie-switch-upstream-port 连接到插入 pcie-expander-bus 的 pcie-root-port，并将多个 pcie-switch-downstream-port 连接到 pcie-switch-upstream-port，当然，为了使此工作正常，需要相应地减少 pcie-expander-bus 的 busNr，以便在其上方有足够的未使用总线编号，以容纳为上游端口和每个下游端口分配一个总线编号（除了 pcie-root-port 和 pcie-expander-bus 本身）。

- node

  某些 PCI 控制器（pc 机器类型的 pci-expander-bus、q35 机器类型的 pcie-expander-bus，以及自 3.6.0 起，pseries 机器类型的 pci-root）可以在 <target> 子元素中具有可选的 <node> 子元素，用于设置向客户机 OS 报告的该总线的 NUMA 节点 - 客户机 OS 然后将知道该总线上的所有设备都是指定 NUMA 节点的一部分（在将主机设备分配给域时，由 libvirt API 的用户负责将主机设备附加到正确的 pci-expander-bus）。

- index

  pSeries 客户机的 pci-root 控制器使用此属性记录它们在客户机中显示的顺序。自 3.6.0 起

- memReserve

  某些 PCI 设备具有大于 2MiB 的非预取内存条。使用此属性覆盖固件计算的值，从而使控制器保留更多内存（以 KiB 为单位），以便可以热插拔此类 PCI 设备。对于冷插拔的 PCI 设备，固件将自动保留正确数量的内存。自 10.3.0 起

对于提供隐式 PCI 总线的机器类型，会自动添加 index=0 的 pci-root 控制器，并且是使用 PCI 设备所必需的。pci-root 没有地址。如果有太多设备无法容纳在 pci-root 提供的一个总线上，或者指定了大于零的 PCI 总线编号，则会自动添加 PCI 桥。也可以手动指定 PCI 桥，但其地址应仅引用由已指定的 PCI 控制器提供的 PCI 总线。在 PCI 控制器索引中留下间隙可能会导致无效配置。

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

对于提供隐式 PCI Express (PCIe) 总线的机器类型（例如，基于 Q35 芯片组的机器类型），会自动将 index=0 的 pcie-root 控制器添加到域的配置中。pcie-root 也没有地址，提供 31 个槽（编号 1-31），可用于连接 PCIe 或 PCI 设备（尽管 libvirt 永远不会自动将 PCI 设备分配给 PCIe 槽，但它会允许手动指定此类分配）。连接到 pcie-root 的设备不能热插拔。如果客户机配置中存在传统 PCI 设备，将自动添加 pcie-to-pci-bridge 控制器：此控制器插入 pcie-root-port，提供 31 个可用的 PCI 槽（1-31），支持热插拔（自 4.3.0 起）。如果 QEMU 二进制不支持相应的设备，则会添加 dmi-to-pci-bridge 控制器代替，通常位于 slot=0x1e 的默认标准位置。dmi-to-pci-bridge 控制器插入 PCIe 槽（由 pcie-root 提供），并本身提供 31 个标准 PCI 槽（也不支持设备热插拔）。为了在客户机系统中拥有可热插拔的 PCI 槽，还将自动创建 pci-bridge 控制器并连接到自动创建的 dmi-to-pci-bridge 控制器的一个槽；所有地址由 libvirt 自动确定的客户机 PCI 设备将放置在此 pci-bridge 设备上。（自 1.1.2 起）。

具有隐式 pcie-root 的域还可以添加 model='pcie-root-port'、model='pcie-switch-upstream-port' 和 model='pcie-switch-downstream-port' 的控制器。pcie-root-port 是一种简单的桥接设备，只能在其上游侧连接到 pcie-root 总线上的 31 个槽之一，并在下游侧（在 slot='0'）提供单个（PCIe，可热插拔）端口。pcie-root-port 可用于提供单个槽，以便稍后热插拔 PCIe 设备（但它本身不可热插拔 - 它必须在域启动时在配置中）。（自 1.2.19 起）

pcie-switch-upstream-port 是一种更灵活（但也更复杂）的设备，只能在其上游侧插入 pcie-root-port 或 pcie-switch-downstream-port（并且只能在域启动之前 - 它不可热插拔），并在下游侧（slot='0' - slot='31'）提供 32 个端口，仅接受 pcie-switch-downstream-port 设备；每个 pcie-switch-downstream-port 设备只能在其上游侧插入 pcie-switch-upstream-port（同样，不可热插拔），并在其下游侧提供单个可热插拔的 pcie 端口，可以接受任何标准 pci 或 pcie 设备（或另一个 pcie-switch-upstream-port），即功能与 pcie-root-port 相同。（自 1.2.19 起）

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

### 21.8 [主机设备分配](https://www.libvirt.org/formatdomain.html#id36)

#### 21.8.1 [USB / PCI / SCSI 设备](https://www.libvirt.org/formatdomain.html#id37)

主机上连接的 USB（自 0.4.4 起）、PCI（自 0.6.0 起，仅 KVM）和 SCSI（自 1.0.6 起，仅 KVM）设备可以使用 hostdev 元素传递给客户机。

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

  hostdev 元素是描述主机设备的主要容器。对于每个设备，mode 始终为 "subsystem"，type 是以下值之一，并带有附加属性：
  - usb USB 设备在客户机启动时从主机分离，在客户机退出或设备热插拔后重新附加。
  - pci 对于 PCI 设备，当 managed 为 "yes" 时，它在传递给客户机之前从主机分离，并在客户机退出后重新附加到主机。如果省略 managed 或为 "no"，用户负责在启动客户机或热插拔设备之前调用 virNodeDeviceDetachFlags（或 virsh nodedev-detach），并在热插拔或停止客户机后调用 virNodeDeviceReAttach（或 virsh nodedev-reattach）。自 10.3.0 起，可以使用可选的 display 属性来启用将 vgpu 设备用作客户机的显示设备。支持的值为 on 或 off（默认）。还有一个可选的 ramfb 属性，值为 on 或 off（默认）。启用时，ramfb 属性为客户机提供内存帧缓冲区设备。此帧缓冲区允许 vgpu 在客户机内加载 gpu 驱动程序之前用作启动显示。ramfb 需要将 display 属性设置为 on。
  - scsi 对于 SCSI 设备，用户负责确保设备不被主机使用。

    如果 hypervisor 和 OS 支持，可选的 sgio（自 1.0.6 起，但目前不再被任何 hypervisor 驱动程序支持）属性指示是否为磁盘过滤非特权 SG_IO 命令。有效的设置是 "filtered" 或 "unfiltered"，默认值为 "filtered"。

    可选的 rawio（自 1.2.9 起）属性指示 lun 是否需要 rawio 能力。有效的设置是 "yes" 或 "no"。请参阅 [硬盘、软盘、CDROM](https://www.libvirt.org/formatdomain.html#hard-drives-floppy-disks-cdroms) 部分中的 rawio 描述。如果域中的磁盘 lun 已经具有 rawio 能力，则不需要此设置。
  - scsi_host 自 2.5.0 起 对于 SCSI 设备，用户负责确保设备不被主机使用。此类型将单个 HBA 呈现的所有 LUN 传递给客户机。自 5.2.0 起，可以使用 model 属性进一步指定为 "virtio"、"virtio-transitional" 或 "virtio-non-transitional"。有关更多详细信息，请参阅 [virtio 设备模型](https://www.libvirt.org/formatdomain.html#virtio-device-models)。
  - mdev 对于中介设备（自 3.2.0 起），model 属性指定设备 API，该 API 确定主机的 vfio 驱动程序如何向客户机公开设备。目前，支持 model='vfio-pci'、model='vfio-ccw'（自 4.4.0 起）和 model='vfio-ap'（自 4.9.0 起）。[MDEV](https://www.libvirt.org/drvnodedev.html#mediated-devices-mdevs) 部分提供了有关中介设备以及如何在主机上创建中介设备的更多信息。自 4.6.0（QEMU 2.12）起，可以使用可选的 display 属性来启用或禁用支持由中介设备（如 NVIDIA vGPU 或 Intel GVT-g）支持的加速远程桌面，作为模拟 [视频设备](https://www.libvirt.org/formatdomain.html#video-devices) 的替代方案。此属性仅限于 model='vfio-pci'。支持的值为 on 或 off（默认值为 'off'）。为了使用此属性，需要使用图形帧缓冲区（请参阅 [图形帧缓冲区](https://www.libvirt.org/formatdomain.html#graphical-framebuffers)），目前仅支持 VNC、Spice 和 egl-headless 图形设备。自 5.10.0 版本起，对于 model='vfio-pci' 的设备，有一个可选的 ramfb 属性。支持的值为 on 或 off（默认值为 'off'）。启用时，此属性为客户机提供内存帧缓冲区设备。当 vgpu 设备是主显示时，此帧缓冲区将用作启动显示。
  - 注意：根据 model 属性，对客户机地址类型的使用也有一些影响，请参见下面的 address 元素。
  注意：managed 属性仅用于 type='pci'，并被所有其他设备类型忽略，因此使用除 PCI 设备以外的其他设备显式设置 managed 与省略它具有相同的效果。同样，model 属性仅受中介设备支持，并被所有其他设备类型忽略。
- source

  source 元素使用以下机制描述从主机看到的设备：
  - usb USB 设备可以通过使用 vendor 和 product 元素的厂商/产品 ID 或通过使用 address 元素的设备在主机上的地址来寻址。
  自 1.0.0 起，USB 设备的 source 元素可能包含 startupPolicy 属性，可用于定义如果未找到指定的主机 USB 设备时要执行的策略。该属性接受以下值：
  | mandatory | 如果因任何原因缺失则失败（默认）                          |
  | --------- | ------------------------------------------------------- |
  | requisite | 启动时缺失则失败，迁移/恢复/还原时缺失则丢弃                 |
  | optional  | 在任何启动尝试时缺失则丢弃                                   |
  自 8.6.0 起，source 元素可以包含 guestReset 属性，具有以下值：
  | off           | 忽略所有客户机发起的设备重置请求                            |
  | ------------- | -------------------------------------------------------- |
  | uninitialized | 如果设备已初始化则忽略设备请求，否则执行重置                   |
  | on            | 在每次客户机发起的请求时重置设备                              |
  此属性在分配带有在重置时崩溃的固件的 USB 设备时可能很有帮助。
  - pci PCI 设备只能通过其地址来描述。自 6.8.0（仅 Xen）起，PCI 设备的 source 元素可能包含 writeFiltering 属性，用于控制对 PCI 配置空间的写访问。默认情况下，Xen 只允许写入已知安全值到配置空间。设置 writeFiltering='no' 将允许对设备的 PCI 配置空间进行所有写入。
  - scsi SCSI 设备由 adapter 和 address 元素描述。address 元素包括 bus 属性（2 位总线编号）、target 属性（10 位目标编号）和 unit 属性（总线上的 20 位单元编号）。并非所有 hypervisor 都支持更大的 target 和 unit 值。每个 hypervisor 负责确定适配器支持的最大值。

    自 1.2.8 起，SCSI 设备的 source 元素可能包含 protocol 属性。当该属性设置为 "iscsi" 时，主机设备 XML 遵循网络磁盘设备（请参阅 [硬盘、软盘、CDROM](https://www.libvirt.org/formatdomain.html#hard-drives-floppy-disks-cdroms)），使用相同的 name 属性，并可选地使用 auth 元素为 iSCSI 服务器提供认证凭证。

    自 6.7.0 起，可选的 initiator 子元素通过其 <iqn name='iqn...' 子元素控制 hypervisor 运行的发起方的 IQN。
  - scsi_host 自 2.5.0 起，单个 SCSI HBA 后面的多个 LUN 通过设置为 "vhost" 的 protocol 属性和 wwpn 属性（主机 configfs 中建立的 vhost_scsi wwpn，带有 "naa." 前缀的 16 位十六进制数字）来描述。
  - mdev 中介设备（自 3.2.0 起）由 address 元素描述。address 元素包含单个必需的 uuid 属性。
- vendor, product

  vendor 和 product 元素各有一个 id 属性，指定 USB 厂商和产品 ID。这些 ID 可以以十进制、十六进制（以 0x 开头）或八进制（以 0 开头）形式给出。
- boot

  指定设备可引导。order 属性确定引导序列期间尝试设备的顺序。每设备引导元素不能与 [客户机固件](https://www.libvirt.org/formatdomain.html#guest-firmware) 部分中的一般引导元素一起使用。自 0.8.8 起用于 PCI 设备，自 1.0.1 起用于 USB 设备。
- rom

  rom 元素用于更改 PCI 设备的 ROM 如何呈现给客户机。可选的 bar 属性可以设置为 "on" 或 "off"，并确定设备的 ROM 是否会在客户机的内存映射中可见。（在 PCI 文档中，"rombar" 设置控制 ROM 基址寄存器的存在）。如果未指定 rom bar，则使用 qemu 默认值（较旧版本的 qemu 使用 "off" 的默认值，而较新的 qemus 使用 "on" 的默认值）。自 0.9.7（仅 QEMU 和 KVM）起。可选的 file 属性包含一个二进制文件的绝对路径，该文件将作为设备的 ROM BIOS 呈现给客户机。这对于为 sr-iov 功能的以太网设备的虚拟功能（其 VF 没有启动 ROM）提供 PXE 启动 ROM 等情况很有用。自 0.9.10（仅 QEMU 和 KVM）起。可选的 enabled 属性可以设置为 no 以完全禁用 PCI ROM 加载；如果通过此属性禁用了 PCI ROM 加载，尝试通过 bar 或 file 属性进一步调整加载过程将被拒绝。自 4.3.0（仅 QEMU 和 KVM）起。
- address

  USB 设备的 address 元素具有 bus 属性，用于指定 USB 总线。此外，需要 device 属性或 port 属性来标识主机上的设备。虽然设备编号在设备连接时分配，但端口号是物理主机端口的稳定标识符。总线和设备编号可以以十进制、十六进制（以 0x 开头）或八进制（以 0 开头）形式给出。端口号是点分路径（例如：2, 1.2.5）。对于 PCI 设备，该元素带有 4 个属性，允许指定设备，如通过 lspci 或 virsh nodedev-list 找到的那样。对于 SCSI 设备，必须使用 'drive' 地址类型。对于中介设备，它们是在物理父设备上定义资源分配的纯软件设备，使用的地址类型必须符合 hostdev 元素的 model 属性，例如，对于 vfio-pci 设备 API，除了 PCI 之外的任何地址类型，或者对于 vfio-ccw 设备 API，除了 CCW 之外的任何地址类型都会导致错误。有关 address 元素的更多详细信息，请参阅 [设备地址](https://www.libvirt.org/formatdomain.html#device-addresses) 部分。
- driver

  PCI hostdev 设备可以有一个可选的 driver 子元素，指定在准备将设备分配给客户机时绑定到设备的主机驱动程序。自 10.0.0（仅对 QEMU 和 KVM 有用）起。这是通过设置 <driver> 元素的 model 属性来完成的，例如：`...  <hostdev mode='subsystem' type='pci' managed='yes'>    <driver model='vfio-pci-igb'/> ...` 告诉 libvirt 在将设备交给 QEMU 分配给客户机之前，在主机上将驱动程序 "vfio-pci-igb" 绑定到设备。通常，libvirt 会将设备绑定到它在内核的 modules.alias 文件中找到的 "最佳匹配" VFIO 类型驱动程序（基于匹配设备的 sysfs 中的 modalias 文件的相应字段），或者如果没有找到更好的匹配，则绑定到通用的 "vfio-pci" 驱动程序（在 libvirt 10.0.0 之前始终使用 vfio-pci），但在正确的驱动程序未在 modules.alias 中列出的情况下，可以通过设置驱动程序名称来强制使用所需的设备特定驱动程序，或者如果找到的设备特定驱动程序在某些方面 "有问题"，同样可以强制使用通用的 vfio-pci 驱动程序。自 12.1.0（仅 QEMU 和 KVM）起，可以使用 iommufd 元素来为 VFIO 设备启用 IOMMUFD 后端。这提供了一个接口，用于将 DMA 映射传播到内核以用于分配的设备。Libvirt 将打开 /dev/iommu 和 VFIO 设备 cdev，并将相关的文件描述符传递给 QEMU。（注意：自 1.0.5 起，name 属性被描述为用于选择 PCI 设备分配的类型（"vfio"、"kvm" 或 "xen"），但这些值大多无用，因为设备分配的类型实际上由使用的 hypervisor 决定。这意味着您可能会偶尔在域的状态 XML 中看到 <driver name='vfio'/> 或 <driver name='xen'/>，或者更罕见地在配置中看到，但这些特定值基本上被忽略。）
- readonly

  指示设备为只读，目前仅支持 SCSI 主机设备。自 1.0.6（仅 QEMU 和 KVM）起
- shareable

  如果存在，这表示设备预期在域之间共享（假设 hypervisor 和 OS 支持此功能）。仅支持 SCSI 主机设备。自 1.0.6 起，但仅自 1.2.2 起按预期工作。

#### 21.8.2 [ACPI Generic Initiators](https://www.libvirt.org/formatdomain.html#id38)

主机设备可以包含 <acpi> 元素，用于在 QEMU 中为设备创建 ACPI Generic Initiator 对象。

这可用于 **NVIDIA Multi-Instance GPU (MIG)** 配置，其中物理 GPU 被划分为多个隔离的实例，每个实例与一个或多个虚拟 NUMA 节点相关联。

通过将 <acpi nodeset=.../> 元素附加到域 XML 中的 MIG 设备，客户机将为该实例配置正确的分区。

```
<numa>
  <cell id='0' cpus='0-15' memory='8388608' unit='KiB'/>
  <cell id='1' memory='0' unit='KiB'/>
  <cell id='2' memory='0' unit='KiB'/>
  <cell id='3' memory='0' unit='KiB'/>
</numa>
...
<devices>
  ...
  <hostdev mode='subsystem' type='mdev' model='vfio-pci'>
    <source>
      <address uuid='64139528-a53f-45b4-851e-fa80c87c1a88'/>
    </source>
    <acpi nodeset='0' type='numa'/>
  </hostdev>
  ...
</devices>
```

- acpi

  acpi 元素具有以下属性：
  - nodeset 逗号分隔的 NUMA 节点列表，与设备关联。
  - type 关联类型，目前仅支持 'numa'。

### 21.9 [智能卡设备](https://www.libvirt.org/formatdomain.html#id39)

智能卡设备允许将主机上的智能卡或智能卡读卡器传递给客户机。

```
...
<devices>
  <smartcard mode='passthrough' type='tcp'>
    <source mode='connect' host='192.168.1.1' service='2001'/>  
  </smartcard>
  <smartcard mode='host' type='ccid'>
    <address type='ccid' bus='0' slot='0'/>
  </smartcard>
</devices>
...
```

- mode

  智能卡设备模式，可以是 'passthrough'、'host' 或 'emulated'。

- type

  智能卡设备类型，如 'tcp'、'unix' 或 'ccid'。

- source

  智能卡设备的源，如 TCP 连接或主机设备地址。

### 21.10 [网络接口](https://www.libvirt.org/formatdomain.html#id40)

网络接口允许客户机连接到网络。libvirt 支持多种网络连接类型，包括虚拟网络、桥接到 LAN、用户空间连接等。

```
...
<devices>
  <interface type='network'>
    <mac address='00:11:22:33:44:55'/>
    <source network='default'/>
    <target dev='vnet0'/>
    <model type='virtio'/>
    <address type='pci' domain='0x0000' bus='0x00' slot='0x03' function='0x0'/>
  </interface>
</devices>
...
```

- type

  网络接口类型，可以是 'network'、'bridge'、'direct'、'user'、'vhostuser' 等。

- mac

  网络接口的 MAC 地址。

- source

  网络接口的源，如网络名称或桥