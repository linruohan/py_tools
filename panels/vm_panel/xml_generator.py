"""Libvirt XML 生成器 - 根据Tab配置动态生成XML."""

import xml.etree.ElementTree as ET

from xml.dom import minidom


class LibvirtXMLGenerator:
    """Libvirt Domain XML 生成器."""

    def __init__(self):
        """初始化生成器."""
        self.domain = None

    def generate(self, config: dict) -> str:
        """生成完整的 libvirt domain XML.

        Args:
            config: 包含所有Tab配置的字典

        Returns:
            格式化后的 XML 字符串
        """
        self.domain = ET.Element('domain', type=config.get('hypervisor', 'kvm'))

        self._add_metadata(config)
        self._add_memory(config)
        self._add_cpu(config)
        self._add_os(config)
        self._add_features(config)
        self._add_clock(config)
        self._add_pm(config)
        self._add_events(config)
        self._add_devices(config)
        self._add_memory_backing(config)
        self._add_memory_tuning(config)
        self._add_cpu_tuning(config)
        self._add_numa_tuning(config)
        self._add_block_io_tuning(config)
        self._add_iothreads(config)
        self._add_resource(config)
        self._add_security(config)
        self._add_launch_security(config)

        return self._pretty_print()

    def _add_metadata(self, config: dict) -> None:
        """添加元数据."""
        if config.get('name'):
            name = ET.SubElement(self.domain, 'name')
            name.text = config['name']

        if config.get('title'):
            title = ET.SubElement(self.domain, 'title')
            title.text = config['title']

        if config.get('description'):
            desc = ET.SubElement(self.domain, 'description')
            desc.text = config['description']

        if config.get('uuid'):
            uuid_elem = ET.SubElement(self.domain, 'uuid')
            uuid_elem.text = config['uuid']

        if config.get('genid'):
            genid = ET.SubElement(self.domain, 'genid')
            genid.text = config['genid']

    def _add_memory(self, config: dict) -> None:
        """添加内存配置."""
        memory_config = config.get('memory_allocation', {})

        memory = memory_config.get('memory', 2097152)
        unit = memory_config.get('unit', 'KiB')

        mem_elem = ET.SubElement(self.domain, 'memory', unit=unit)
        mem_elem.text = str(memory)

        current_memory = memory_config.get('current_memory', memory)
        cm_elem = ET.SubElement(self.domain, 'currentMemory', unit=unit)
        cm_elem.text = str(current_memory)

        max_memory = memory_config.get('max_memory')
        if max_memory and max_memory > memory:
            slots = memory_config.get('memory_slots', 16)
            mm_elem = ET.SubElement(self.domain, 'maxMemory', slots=str(slots), unit=unit)
            mm_elem.text = str(max_memory)

    def _add_cpu(self, config: dict) -> None:
        """添加CPU配置."""
        cpu_alloc = config.get('cpu_allocation', {})
        cpu_model = config.get('cpu_model_topology', {})

        vcpu_count = cpu_alloc.get('max_vcpu', 1)
        current_vcpu = cpu_alloc.get('current_vcpu', vcpu_count)
        placement = cpu_alloc.get('placement', 'static')
        cpuset = cpu_alloc.get('cpuset', '')

        vcpu_attrs = {'placement': placement}
        if cpuset:
            vcpu_attrs['cpuset'] = cpuset
        if current_vcpu != vcpu_count:
            vcpu_attrs['current'] = str(current_vcpu)

        vcpu = ET.SubElement(self.domain, 'vcpu', **vcpu_attrs)
        vcpu.text = str(vcpu_count)

        topology = cpu_alloc.get('topology', {})
        if topology:
            sockets = topology.get('sockets', 1)
            dies = topology.get('dies', 1)
            clusters = topology.get('clusters', 1)
            cores = topology.get('cores', 1)
            threads = topology.get('threads', 1)

            cpu_elem = ET.SubElement(self.domain, 'cpu')
            ET.SubElement(
                cpu_elem,
                'topology',
                sockets=str(sockets),
                dies=str(dies),
                clusters=str(clusters),
                cores=str(cores),
                threads=str(threads),
            )

            model_config = cpu_model.get('model', {})
            if model_config.get('mode'):
                cpu_elem.set('mode', model_config['mode'])
            if model_config.get('model'):
                model = ET.SubElement(cpu_elem, 'model')
                model.text = model_config['model']
                if model_config.get('fallback'):
                    model.set('fallback', model_config['fallback'])

            features = cpu_model.get('feature', {}).get('features', [])
            for feat in features:
                ET.SubElement(
                    cpu_elem, 'feature', policy=feat.get('policy', 'require'), name=feat['name']
                )

            cache_config = cpu_model.get('cache', {})
            if cache_config.get('mode'):
                cache_attrs = {'mode': cache_config['mode']}
                if cache_config.get('level'):
                    cache_attrs['level'] = str(cache_config['level'])
                ET.SubElement(cpu_elem, 'cache', **cache_attrs)

    def _add_os(self, config: dict) -> None:
        """添加操作系统配置."""
        os_booting = config.get('os_booting', {})
        boot_type = os_booting.get('type', 'guest_firmware')

        os_elem = ET.SubElement(self.domain, 'os')

        if boot_type == 'guest_firmware':
            firmware = os_booting.get('firmware', 'bios')
            if firmware:
                os_elem.set('firmware', firmware)

            os_type = os_booting.get('os_type', 'hvm')
            arch = os_booting.get('arch', 'x86_64')
            type_elem = ET.SubElement(os_elem, 'type', arch=arch)
            type_elem.text = os_type

            loader_path = os_booting.get('loader_path')
            if loader_path:
                loader = ET.SubElement(os_elem, 'loader')
                loader.text = loader_path

            nvram_path = os_booting.get('nvram_path')
            if nvram_path:
                nvram = ET.SubElement(os_elem, 'nvram')
                nvram.text = nvram_path

            boot_dev = os_booting.get('boot_dev', 'hd')
            ET.SubElement(os_elem, 'boot', dev=boot_dev)

            if os_booting.get('boot_menu'):
                timeout = os_booting.get('boot_timeout', 3000)
                ET.SubElement(os_elem, 'bootmenu', enable='yes', timeout=str(timeout))

            smbios_mode = os_booting.get('smbios_mode')
            if smbios_mode:
                ET.SubElement(os_elem, 'smbios', mode=smbios_mode)

        elif boot_type == 'direct_kernel':
            type_elem = ET.SubElement(os_elem, 'type', arch='x86_64')
            type_elem.text = 'hvm'

            kernel = os_booting.get('kernel')
            if kernel:
                kernel_elem = ET.SubElement(os_elem, 'kernel')
                kernel_elem.text = kernel

            initrd = os_booting.get('initrd')
            if initrd:
                initrd_elem = ET.SubElement(os_elem, 'initrd')
                initrd_elem.text = initrd

            cmdline = os_booting.get('cmdline')
            if cmdline:
                cmdline_elem = ET.SubElement(os_elem, 'cmdline')
                cmdline_elem.text = cmdline

            dtb = os_booting.get('dtb')
            if dtb:
                dtb_elem = ET.SubElement(os_elem, 'dtb')
                dtb_elem.text = dtb

        elif boot_type == 'container':
            type_elem = ET.SubElement(os_elem, 'type', arch='x86_64')
            type_elem.text = 'exe'

            init = os_booting.get('init')
            if init:
                init_elem = ET.SubElement(os_elem, 'init')
                init_elem.text = init

            init_args = os_booting.get('init_args')
            if init_args:
                for arg in init_args.split():
                    ET.SubElement(os_elem, 'initarg').text = arg

        elif boot_type == 'host_bootloader':
            bootloader = os_booting.get('bootloader')
            if bootloader:
                bl_elem = ET.SubElement(self.domain, 'bootloader')
                bl_elem.text = bootloader

            bootloader_args = os_booting.get('bootloader_args')
            if bootloader_args:
                bl_args = ET.SubElement(self.domain, 'bootloader_args')
                bl_args.text = bootloader_args

    def _add_features(self, config: dict) -> None:
        """添加虚拟化特性."""
        features_config = config.get('hypervisor_features', {})

        general = features_config.get('general', {})
        if any(general.values()):
            features = ET.SubElement(self.domain, 'features')

            if general.get('pae'):
                ET.SubElement(features, 'pae')
            if general.get('acpi'):
                ET.SubElement(features, 'acpi')
            if general.get('apic'):
                ET.SubElement(features, 'apic')
            if general.get('hap'):
                ET.SubElement(features, 'hap')
            if general.get('viridian'):
                ET.SubElement(features, 'viridian')
            if general.get('privnet'):
                ET.SubElement(features, 'privnet')
            if general.get('pvspinlock'):
                ET.SubElement(features, 'pvspinlock')
            if general.get('pmu'):
                ET.SubElement(features, 'pmu')
            if general.get('vmport'):
                ET.SubElement(features, 'vmport')
            if general.get('smm'):
                ET.SubElement(features, 'smm')
            if general.get('vmcoreinfo'):
                ET.SubElement(features, 'vmcoreinfo')
            if general.get('ras'):
                ET.SubElement(features, 'ras')

        hyperv = features_config.get('hyperv', {})
        if any(v for k, v in hyperv.items() if k != 'mode'):
            if 'features' not in self.domain.find('.'):
                features = ET.SubElement(self.domain, 'features')
            else:
                features = self.domain.find('features')

            hyperv_elem = ET.SubElement(features, 'hyperv')
            if hyperv.get('mode'):
                hyperv_elem.set('mode', hyperv['mode'])

            hyperv_features = [
                'relaxed',
                'vapic',
                'spinlocks',
                'vpindex',
                'runtime',
                'synic',
                'stimer',
                'reset',
                'frequencies',
                'reenlightenment',
                'tlbflush',
                'ipi',
                'evmcs',
            ]
            for feat in hyperv_features:
                if hyperv.get(feat):
                    ET.SubElement(hyperv_elem, feat, state='on')

        kvm = features_config.get('kvm', {})
        if any(v for k, v in kvm.items() if not k.endswith('_size')):
            if self.domain.find('features') is None:
                features = ET.SubElement(self.domain, 'features')
            else:
                features = self.domain.find('features')

            kvm_elem = ET.SubElement(features, 'kvm')

            if kvm.get('hidden'):
                ET.SubElement(kvm_elem, 'hidden', state='on')
            if kvm.get('hint_dedicated'):
                ET.SubElement(kvm_elem, 'hint-dedicated', state='on')
            if kvm.get('poll_control'):
                ET.SubElement(kvm_elem, 'poll-control', state='on')
            if kvm.get('pv_ipi'):
                ET.SubElement(kvm_elem, 'pv-ipi', state='on')
            if kvm.get('dirty_ring'):
                size = kvm.get('dirty_ring_size', '4096')
                ET.SubElement(kvm_elem, 'dirty-ring', state='on', size=size)

    def _add_clock(self, config: dict) -> None:
        """添加时钟配置."""
        time_config = config.get('time_keeping', {})
        if not time_config:
            return

        offset = time_config.get('offset', 'utc')
        clock_attrs = {'offset': offset}

        if offset == 'timezone' and time_config.get('timezone'):
            clock_attrs['timezone'] = time_config['timezone']
        elif offset == 'variable':
            if time_config.get('adjustment'):
                clock_attrs['adjustment'] = time_config['adjustment']
            if time_config.get('basis'):
                clock_attrs['basis'] = time_config['basis']
        elif offset == 'absolute' and time_config.get('start'):
            clock_attrs['start'] = time_config['start']

        clock = ET.SubElement(self.domain, 'clock', **clock_attrs)

        timers = time_config.get('timers', {})
        if timers.get('rtc_tickpolicy'):
            ET.SubElement(clock, 'timer', name='rtc', tickpolicy=timers['rtc_tickpolicy'])
        if timers.get('pit_tickpolicy'):
            ET.SubElement(clock, 'timer', name='pit', tickpolicy=timers['pit_tickpolicy'])
        if timers.get('tsc_mode'):
            ET.SubElement(clock, 'timer', name='tsc', mode=timers['tsc_mode'])
        if timers.get('hpet_present') == 'yes':
            ET.SubElement(clock, 'timer', name='hpet', present='yes')
        if timers.get('kvmclock_present') == 'yes':
            ET.SubElement(clock, 'timer', name='kvmclock', present='yes')

    def _add_pm(self, config: dict) -> None:
        """添加电源管理配置."""
        pm_config = config.get('power_management', {})
        if not pm_config:
            return

        pm = ET.SubElement(self.domain, 'pm')

        suspend_mem = pm_config.get('suspend_to_mem', 'yes')
        ET.SubElement(pm, 'suspend-to-mem', enabled=suspend_mem)

        suspend_disk = pm_config.get('suspend_to_disk', 'yes')
        ET.SubElement(pm, 'suspend-to-disk', enabled=suspend_disk)

    def _add_events(self, config: dict) -> None:
        """添加事件配置."""
        events_config = config.get('events_configuration', {})
        if not events_config:
            return

        on_poweroff = events_config.get('on_poweroff', 'destroy')
        ET.SubElement(self.domain, 'on_poweroff').text = on_poweroff

        on_reboot = events_config.get('on_reboot', 'restart')
        ET.SubElement(self.domain, 'on_reboot').text = on_reboot

        on_crash = events_config.get('on_crash', 'destroy')
        ET.SubElement(self.domain, 'on_crash').text = on_crash

        on_lockfailure = events_config.get('on_lockfailure')
        if on_lockfailure:
            ET.SubElement(self.domain, 'on_lockfailure').text = on_lockfailure

    def _add_devices(self, config: dict) -> None:
        """添加设备配置."""
        devices_config = config.get('devices', {})
        if not devices_config:
            return

        devices = ET.SubElement(self.domain, 'devices')

        # 添加默认的输入设备
        ET.SubElement(devices, 'input', type='tablet', bus='usb')
        ET.SubElement(devices, 'input', type='keyboard', bus='usb')

        emulator = devices_config.get('emulator')
        if emulator:
            ET.SubElement(devices, 'emulator').text = emulator

        disks = devices_config.get('disks', [])
        for disk in disks:
            self._add_disk(devices, disk)

        interfaces = devices_config.get('interfaces', [])
        for iface in interfaces:
            self._add_interface(devices, iface)

        graphics = devices_config.get('graphics')
        if graphics:
            self._add_graphics(devices, graphics)

        videos = devices_config.get('videos', [])
        for video in videos:
            self._add_video(devices, video)

        controllers = devices_config.get('controllers', [])
        for ctrl in controllers:
            self._add_controller(devices, ctrl)

        serials = devices_config.get('serials', [])
        for serial in serials:
            self._add_serial(devices, serial)

        # 添加默认的控制台
        console = ET.SubElement(devices, 'console', type='pty')
        ET.SubElement(console, 'target', type='serial', port='0')

        inputs = devices_config.get('inputs', [])
        for inp in inputs:
            self._add_input(devices, inp)

        sounds = devices_config.get('sounds', [])
        for sound in sounds:
            ET.SubElement(devices, 'sound', model=sound.get('model', 'ich6'))

        hostdevs = devices_config.get('hostdevs', [])
        for hostdev in hostdevs:
            self._add_hostdev(devices, hostdev)

    def _add_disk(self, devices: ET.Element, disk: dict) -> None:
        """添加磁盘设备."""
        disk_type = disk.get('type', 'file')
        device = disk.get('device', 'disk')

        disk_attrs = {'type': disk_type, 'device': device}
        if disk.get('snapshot'):
            disk_attrs['snapshot'] = disk['snapshot']

        disk_elem = ET.SubElement(devices, 'disk', **disk_attrs)

        driver_attrs = {
            'name': disk.get('driver_name', 'qemu'),
            'type': disk.get('driver_type', 'qcow2'),
        }
        if disk.get('cache'):
            driver_attrs['cache'] = disk['cache']
        if disk.get('io'):
            driver_attrs['io'] = disk['io']
        if disk.get('discard'):
            driver_attrs['discard'] = disk['discard']
        ET.SubElement(disk_elem, 'driver', **driver_attrs)

        if disk_type == 'file' and disk.get('file'):
            ET.SubElement(disk_elem, 'source', file=disk['file'])
        elif disk_type == 'block' and disk.get('dev'):
            ET.SubElement(disk_elem, 'source', dev=disk['dev'])
        elif disk_type == 'network':
            source_attrs = {'protocol': disk.get('protocol', 'nbd')}
            if disk.get('name'):
                source_attrs['name'] = disk['name']
            source = ET.SubElement(disk_elem, 'source', **source_attrs)
            if disk.get('host'):
                ET.SubElement(
                    source, 'host', name=disk['host'], port=str(disk.get('port', '10809'))
                )

        target_attrs = {'dev': disk.get('target_dev', 'vda'), 'bus': disk.get('bus', 'virtio')}
        ET.SubElement(disk_elem, 'target', **target_attrs)

        if disk.get('readonly'):
            ET.SubElement(disk_elem, 'readonly')

        if disk.get('boot_order'):
            ET.SubElement(disk_elem, 'boot', order=str(disk['boot_order']))

    def _add_interface(self, devices: ET.Element, iface: dict) -> None:
        """添加网络接口."""
        iface_type = iface.get('type', 'network')
        iface_elem = ET.SubElement(devices, 'interface', type=iface_type)

        if iface.get('mac'):
            ET.SubElement(iface_elem, 'mac', address=iface['mac'])

        if iface_type == 'network':
            ET.SubElement(iface_elem, 'source', network=iface.get('network', 'default'))
        elif iface_type == 'bridge':
            ET.SubElement(iface_elem, 'source', bridge=iface.get('bridge', 'br0'))
        elif iface_type == 'direct':
            ET.SubElement(
                iface_elem, 'source', dev=iface.get('dev', 'eth0'), mode=iface.get('mode', 'bridge')
            )

        ET.SubElement(iface_elem, 'model', type=iface.get('model', 'virtio'))

        if iface.get('boot_order'):
            ET.SubElement(iface_elem, 'boot', order=str(iface['boot_order']))

    def _add_graphics(self, devices: ET.Element, graphics: dict) -> None:
        """添加图形设备."""
        gtype = graphics.get('type', 'vnc')
        if gtype == 'none':
            return

        attrs = {'type': gtype}
        if graphics.get('port'):
            attrs['port'] = str(graphics['port'])
        else:
            attrs['port'] = '-1'
            attrs['autoport'] = 'yes'
        if graphics.get('listen'):
            attrs['listen'] = graphics['listen']
        if graphics.get('passwd'):
            attrs['passwd'] = graphics['passwd']

        graphics_elem = ET.SubElement(devices, 'graphics', **attrs)

        if graphics.get('listen'):
            ET.SubElement(graphics_elem, 'listen', type='address', address=graphics['listen'])

    def _add_video(self, devices: ET.Element, video: dict) -> None:
        """添加视频设备."""
        video_elem = ET.SubElement(devices, 'video')
        model_attrs = {'type': video.get('model', 'qxl')}
        if video.get('vram'):
            model_attrs['vram'] = str(video['vram'])
        if video.get('heads'):
            model_attrs['heads'] = str(video['heads'])
        ET.SubElement(video_elem, 'model', **model_attrs)

    def _add_controller(self, devices: ET.Element, ctrl: dict) -> None:
        """添加控制器."""
        attrs = {'type': ctrl.get('type', 'usb')}
        if ctrl.get('model'):
            attrs['model'] = ctrl['model']
        if ctrl.get('index'):
            attrs['index'] = str(ctrl['index'])
        ET.SubElement(devices, 'controller', **attrs)

    def _add_serial(self, devices: ET.Element, serial: dict) -> None:
        """添加串口."""
        serial_type = serial.get('type', 'pty')
        serial_elem = ET.SubElement(devices, 'serial', type=serial_type)

        if serial_type == 'pty':
            ET.SubElement(serial_elem, 'target', port=str(serial.get('port', 0)))
        elif serial_type == 'tcp':
            ET.SubElement(serial_elem, 'protocol', type=serial.get('protocol', 'telnet'))
            source_attrs = {
                'mode': serial.get('mode', 'bind'),
                'host': serial.get('host', '0.0.0.0'),
            }
            if serial.get('service'):
                source_attrs['service'] = str(serial['service'])
            ET.SubElement(serial_elem, 'source', **source_attrs)

    def _add_console(self, devices: ET.Element, console: dict) -> None:
        """添加控制台."""
        console_type = console.get('type', 'pty')
        console_elem = ET.SubElement(devices, 'console', type=console_type)
        target_attrs = {'type': console.get('target_type', 'serial')}
        if console.get('port'):
            target_attrs['port'] = str(console['port'])
        ET.SubElement(console_elem, 'target', **target_attrs)

    def _add_input(self, devices: ET.Element, inp: dict) -> None:
        """添加输入设备."""
        attrs = {'type': inp.get('type', 'tablet'), 'bus': inp.get('bus', 'usb')}
        ET.SubElement(devices, 'input', **attrs)

    def _add_hostdev(self, devices: ET.Element, hostdev: dict) -> None:
        """添加主机设备直通."""
        dev_type = hostdev.get('type', 'pci')
        mode = hostdev.get('mode', 'subsystem')

        hostdev_elem = ET.SubElement(devices, 'hostdev', mode=mode, type=dev_type)

        if dev_type == 'pci':
            managed = hostdev.get('managed', 'yes')
            hostdev_elem.set('managed', managed)
            source = ET.SubElement(hostdev_elem, 'source')
            addr_attrs = {}
            if hostdev.get('domain'):
                addr_attrs['domain'] = hostdev['domain']
            if hostdev.get('bus'):
                addr_attrs['bus'] = hostdev['bus']
            if hostdev.get('slot'):
                addr_attrs['slot'] = hostdev['slot']
            if hostdev.get('function'):
                addr_attrs['function'] = hostdev['function']
            if addr_attrs:
                ET.SubElement(source, 'address', **addr_attrs)
            # Boot order
            if hostdev.get('boot_order'):
                ET.SubElement(hostdev_elem, 'boot', order=str(hostdev['boot_order']))
            # ROM BAR
            if hostdev.get('rom_bar'):
                ET.SubElement(hostdev_elem, 'rom', bar=hostdev['rom_bar'], file=hostdev.get('rom_file', ''))

        elif dev_type == 'usb':
            source = ET.SubElement(hostdev_elem, 'source')
            startup_policy = hostdev.get('startup_policy', 'optional')
            guest_reset = hostdev.get('guest_reset', False)
            if startup_policy:
                source.set('startupPolicy', startup_policy)
            if guest_reset:
                source.set('guestReset', 'on')
            vendor_product = hostdev.get('vendor_product', '')
            if vendor_product and ':' in vendor_product:
                vendor, product = vendor_product.split(':')
                ET.SubElement(source, 'vendor', id=f'0x{vendor}')
                ET.SubElement(source, 'product', id=f'0x{product}')
            # Boot order
            if hostdev.get('boot_order'):
                ET.SubElement(hostdev_elem, 'boot', order=str(hostdev['boot_order']))

        elif dev_type == 'scsi':
            source = ET.SubElement(hostdev_elem, 'source')
            protocol = hostdev.get('protocol')
            if protocol == 'iscsi':
                source.set('protocol', 'iscsi')
                source.set('name', hostdev.get('name', ''))
                host = hostdev.get('host')
                port = hostdev.get('port', '3260')
                if host:
                    ET.SubElement(source, 'host', name=host, port=str(port))
                # Auth
                auth = hostdev.get('auth')
                if auth:
                    auth_elem = ET.SubElement(source, 'auth', username=auth.get('username', ''))
                    ET.SubElement(auth_elem, 'secret', type='iscsi', usage=auth.get('secret', ''))
                # Initiator
                initiator = hostdev.get('initiator')
                if initiator:
                    init_elem = ET.SubElement(source, 'initiator')
                    ET.SubElement(init_elem, 'iqn', name=initiator.get('name', ''))
            else:
                # Local SCSI
                adapter = hostdev.get('adapter')
                if adapter:
                    ET.SubElement(source, 'adapter', name=adapter)
                addr_attrs = {
                    'bus': hostdev.get('bus', '0'),
                    'target': hostdev.get('target', '0'),
                    'unit': hostdev.get('unit', '0'),
                }
                ET.SubElement(source, 'address', **addr_attrs)
            # Readonly
            if hostdev.get('readonly'):
                ET.SubElement(hostdev_elem, 'readonly')
            # Address
            addr_type = hostdev.get('address_type', 'drive')
            addr_attrs = {'type': addr_type}
            if hostdev.get('controller'):
                addr_attrs['controller'] = str(hostdev['controller'])
            if hostdev.get('addr_bus'):
                addr_attrs['bus'] = str(hostdev['addr_bus'])
            if hostdev.get('addr_target'):
                addr_attrs['target'] = str(hostdev['addr_target'])
            if hostdev.get('addr_unit'):
                addr_attrs['unit'] = str(hostdev['addr_unit'])
            ET.SubElement(devices, 'address', **addr_attrs)

        elif dev_type == 'scsi_host':
            source = ET.SubElement(hostdev_elem, 'source')
            source.set('protocol', hostdev.get('protocol', 'vhost'))
            wwpn = hostdev.get('wwpn')
            if wwpn:
                source.set('wwpn', wwpn)

        elif dev_type == 'mdev':
            model = hostdev.get('model', 'vfio-pci')
            hostdev_elem.set('model', model)
            source = ET.SubElement(hostdev_elem, 'source')
            uuid = hostdev.get('uuid')
            if uuid:
                ET.SubElement(source, 'address', uuid=uuid)
            # CCW address for vfio-ccw
            if model == 'vfio-ccw' and hostdev.get('ccw'):
                ccw = hostdev['ccw']
                addr_attrs = {
                    'type': 'ccw',
                    'cssid': ccw.get('cssid', '0xfe'),
                    'ssid': ccw.get('ssid', '0x0'),
                    'devno': ccw.get('devno', '0x0001'),
                }
                ET.SubElement(devices, 'address', **addr_attrs)

    def _add_memory_backing(self, config: dict) -> None:
        """添加内存后端配置."""
        backing_config = config.get('memory_backing', {})
        if not backing_config or not backing_config.get('hugepages'):
            return

        backing = ET.SubElement(self.domain, 'memoryBacking')

        hugepages_list = backing_config.get('hugepages', [])
        if hugepages_list:
            hugepages = ET.SubElement(backing, 'hugepages')
            for page in hugepages_list:
                if page.get('size'):
                    attrs = {'size': page['size'], 'unit': page.get('unit', 'MiB')}
                    if page.get('nodeset'):
                        attrs['nodeset'] = page['nodeset']
                    ET.SubElement(hugepages, 'page', **attrs)

        if backing_config.get('nosharepages'):
            ET.SubElement(backing, 'nosharepages')
        if backing_config.get('locked'):
            ET.SubElement(backing, 'locked')
        if backing_config.get('discard'):
            ET.SubElement(backing, 'discard')

        source_type = backing_config.get('source_type')
        if source_type and source_type != 'anonymous':
            ET.SubElement(backing, 'source', type=source_type)

        access_mode = backing_config.get('access_mode')
        if access_mode:
            ET.SubElement(backing, 'access', mode=access_mode)

        allocation_mode = backing_config.get('allocation_mode')
        if allocation_mode:
            alloc_attrs = {'mode': allocation_mode}
            threads = backing_config.get('allocation_threads')
            if threads:
                alloc_attrs['threads'] = threads
            ET.SubElement(backing, 'allocation', **alloc_attrs)

    def _add_memory_tuning(self, config: dict) -> None:
        """添加内存优化配置."""
        tuning_config = config.get('memory_tuning', {})
        if not any(tuning_config.values()):
            return

        memtune = ET.SubElement(self.domain, 'memtune')

        if tuning_config.get('hard_limit'):
            ET.SubElement(memtune, 'hard_limit', unit='KiB').text = tuning_config['hard_limit']
        if tuning_config.get('soft_limit'):
            ET.SubElement(memtune, 'soft_limit', unit='KiB').text = tuning_config['soft_limit']
        if tuning_config.get('swap_hard_limit'):
            ET.SubElement(memtune, 'swap_hard_limit', unit='KiB').text = tuning_config[
                'swap_hard_limit'
            ]
        if tuning_config.get('min_guarantee'):
            ET.SubElement(memtune, 'min_guarantee', unit='KiB').text = tuning_config[
                'min_guarantee'
            ]

    def _add_cpu_tuning(self, config: dict) -> None:
        """添加CPU优化配置."""
        tuning_config = config.get('cpu_tuning', {})
        if not any(tuning_config.values()):
            return

        cputune = ET.SubElement(self.domain, 'cputune')

        if tuning_config.get('vcpupin'):
            pins = tuning_config['vcpupin'].split(',')
            for pin in pins:
                if '=' in pin:
                    vcpu, cpuset = pin.split('=')
                    ET.SubElement(cputune, 'vcpupin', vcpu=vcpu.strip(), cpuset=cpuset.strip())

        if tuning_config.get('emulatorpin'):
            ET.SubElement(cputune, 'emulatorpin', cpuset=tuning_config['emulatorpin'])

        if tuning_config.get('shares'):
            ET.SubElement(cputune, 'shares').text = tuning_config['shares']
        if tuning_config.get('period'):
            ET.SubElement(cputune, 'period').text = tuning_config['period']
        if tuning_config.get('quota'):
            ET.SubElement(cputune, 'quota').text = tuning_config['quota']

        if tuning_config.get('scheduler'):
            sched_attrs = {'scheduler': tuning_config['scheduler']}
            if tuning_config.get('priority'):
                sched_attrs['priority'] = tuning_config['priority']
            ET.SubElement(cputune, 'vcpusched', **sched_attrs)

    def _add_numa_tuning(self, config: dict) -> None:
        """添加NUMA优化配置."""
        numa_config = config.get('numa_node_tuning', {})
        if not numa_config:
            return

        numatune = ET.SubElement(self.domain, 'numatune')

        mode = numa_config.get('mode', 'strict')
        nodeset = numa_config.get('nodeset')
        placement = numa_config.get('placement')

        attrs = {'mode': mode}
        if nodeset:
            attrs['nodeset'] = nodeset
        if placement:
            attrs['placement'] = placement
        ET.SubElement(numatune, 'memory', **attrs)

        cellid = numa_config.get('cellid')
        cpus = numa_config.get('cpus')
        memory = numa_config.get('memory')

        if cellid and cpus and memory:
            memnode = ET.SubElement(numatune, 'memnode', cellid=cellid, mode=mode)
            if nodeset:
                memnode.set('nodeset', nodeset)

    def _add_block_io_tuning(self, config: dict) -> None:
        """添加块IO优化配置."""
        io_config = config.get('block_io_tuning', {})
        if not any(io_config.values()):
            return

        blkiotune = ET.SubElement(self.domain, 'blkiotune')

        if io_config.get('weight'):
            ET.SubElement(blkiotune, 'weight').text = io_config['weight']

        if io_config.get('device_path') and io_config.get('device_weight'):
            device = ET.SubElement(blkiotune, 'device')
            ET.SubElement(device, 'path').text = io_config['device_path']
            ET.SubElement(device, 'weight').text = io_config['device_weight']

            if io_config.get('read_bytes_sec'):
                ET.SubElement(device, 'read_bytes_sec').text = io_config['read_bytes_sec']
            if io_config.get('write_bytes_sec'):
                ET.SubElement(device, 'write_bytes_sec').text = io_config['write_bytes_sec']
            if io_config.get('read_iops_sec'):
                ET.SubElement(device, 'read_iops_sec').text = io_config['read_iops_sec']
            if io_config.get('write_iops_sec'):
                ET.SubElement(device, 'write_iops_sec').text = io_config['write_iops_sec']

    def _add_iothreads(self, config: dict) -> None:
        """添加IO线程配置."""
        iothreads_config = config.get('iothreads_allocation', {})
        iothreads = iothreads_config.get('iothreads', 0)

        if iothreads <= 0:
            return

        ET.SubElement(self.domain, 'iothreads').text = str(iothreads)

        thread_pool_min = iothreads_config.get('thread_pool_min')
        thread_pool_max = iothreads_config.get('thread_pool_max')

        if thread_pool_min or thread_pool_max:
            default_iothread = ET.SubElement(self.domain, 'defaultiothread')
            if thread_pool_min:
                default_iothread.set('thread_pool_min', str(thread_pool_min))
            if thread_pool_max:
                default_iothread.set('thread_pool_max', str(thread_pool_max))

    def _add_resource(self, config: dict) -> None:
        """添加资源配置."""
        resource_config = config.get('resource_partitioning', {})
        fc_config = config.get('fibre_channel_vmid', {})

        if not resource_config.get('partition') and not fc_config.get('appid'):
            return

        resource = ET.SubElement(self.domain, 'resource')

        if resource_config.get('partition'):
            ET.SubElement(resource, 'partition').text = resource_config['partition']

        if fc_config.get('appid'):
            ET.SubElement(resource, 'fibrechannel', appid=fc_config['appid'])

    def _add_security(self, config: dict) -> None:
        """添加安全配置."""
        security_config = config.get('security_label', {})
        if not security_config or security_config.get('type') == 'none':
            return

        attrs = {'type': security_config.get('type', 'dynamic')}
        if security_config.get('model'):
            attrs['model'] = security_config['model']
        if security_config.get('relabel'):
            attrs['relabel'] = 'yes'

        seclabel = ET.SubElement(self.domain, 'seclabel', **attrs)

        if security_config.get('label'):
            ET.SubElement(seclabel, 'label').text = security_config['label']
        if security_config.get('imagelabel'):
            ET.SubElement(seclabel, 'imagelabel').text = security_config['imagelabel']
        if security_config.get('baselabel_value'):
            ET.SubElement(seclabel, 'baselabel').text = security_config['baselabel_value']

        key_wrap_config = config.get('key_wrap', {})
        if key_wrap_config and key_wrap_config.get('key_name'):
            key_attrs = {'name': key_wrap_config['key_name']}
            if key_wrap_config.get('uuid'):
                key_attrs['uuid'] = key_wrap_config['uuid']
            if key_wrap_config.get('usage'):
                key_attrs['usage'] = key_wrap_config['usage']
            key = ET.SubElement(self.domain, 'key', **key_attrs)

            cipher = key_wrap_config.get('cipher')
            key_size = key_wrap_config.get('key_size')
            mode = key_wrap_config.get('mode')
            hash_alg = key_wrap_config.get('hash')

            if cipher or key_size or mode or hash_alg:
                cipher_attrs = {}
                if cipher:
                    cipher_attrs['name'] = cipher
                if key_size:
                    cipher_attrs['size'] = key_size
                if mode:
                    cipher_attrs['mode'] = mode
                if hash_alg:
                    cipher_attrs['hash'] = hash_alg
                ET.SubElement(key, 'cipher', **cipher_attrs)

    def _add_launch_security(self, config: dict) -> None:
        """添加启动安全配置."""
        launch_config = config.get('launch_security', {})
        if not launch_config:
            return

        attrs = {'type': launch_config.get('type', 'sev')}

        if launch_config.get('policy'):
            attrs['policy'] = launch_config['policy']
        if launch_config.get('cbitpos') and launch_config.get('cbitpos_value'):
            attrs['cbitpos'] = launch_config['cbitpos_value']
        if launch_config.get('reduced_phys_bits') and launch_config.get('reduced_phys_bits_value'):
            attrs['reducedPhysBits'] = launch_config['reduced_phys_bits_value']

        launch_security = ET.SubElement(self.domain, 'launchSecurity', **attrs)

        if launch_config.get('dh_cert'):
            ET.SubElement(launch_security, 'dhCert').text = launch_config['dh_cert']
        if launch_config.get('session'):
            ET.SubElement(launch_security, 'session').text = launch_config['session']

    def _pretty_print(self) -> str:
        """格式化输出XML."""
        xml_str = ET.tostring(self.domain, encoding='unicode')
        parsed = minidom.parseString(xml_str)
        return parsed.toprettyxml(indent='  ')


def build_libvirt_xml(config: dict) -> str:
    """构建 libvirt domain XML.

    Args:
        config: 包含所有Tab配置的字典

    Returns:
        格式化后的 XML 字符串
    """
    generator = LibvirtXMLGenerator()
    return generator.generate(config)
