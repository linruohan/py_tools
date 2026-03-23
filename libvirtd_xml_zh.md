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

  event 元素定义了一个性能监控事件。name 属性指定事件的名称，enabled 属性指定事件是否启用。


