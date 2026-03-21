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
        self._add_key_wrap(config)
        self._add_perf(config)
        self._add_throttlegroups(config)

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
        dump_core = memory_config.get('dump_core')

        mem_elem = ET.SubElement(self.domain, 'memory', unit=unit)
        if dump_core is not None:
            mem_elem.set('dumpCore', 'on' if dump_core else 'off')
        mem_elem.text = str(memory)

        if 'current_memory' in memory_config:
            current_memory = memory_config.get('current_memory', memory)
            cm_elem = ET.SubElement(self.domain, 'currentMemory', unit=unit)
            cm_elem.text = str(current_memory)

        if 'max_memory' in memory_config:
            max_memory = memory_config.get('max_memory')
            if max_memory and max_memory > memory:
                slots = memory_config.get('memory_slots', 16)
                mm_elem = ET.SubElement(self.domain, 'maxMemory', slots=str(slots), unit=unit)
                mm_elem.text = str(max_memory)

    def _add_cpu(self, config: dict) -> None:
        """添加 CPU 配置."""
        cpu_alloc = config.get('cpu_allocation', {})
        cpu_model = config.get('cpu_model_topology', {})

        max_vcpu = cpu_alloc.get('max_vcpu')
        current_vcpu = cpu_alloc.get('current_vcpu')
        placement = cpu_alloc.get('placement')
        cpuset = cpu_alloc.get('cpuset')

        # 如果 max_vcpu 为 None，不生成 vcpu 元素
        if max_vcpu is None:
            return

        vcpu_count = max_vcpu
        vcpu_attrs = {}
        if placement:
            vcpu_attrs['placement'] = placement
        if cpuset:
            vcpu_attrs['cpuset'] = cpuset
        if current_vcpu is not None:
            vcpu_attrs['current'] = str(current_vcpu)

        vcpu = ET.SubElement(self.domain, 'vcpu', **vcpu_attrs)
        vcpu.text = str(vcpu_count)

        # 添加 vcpus 元素
        vcpu_instances = cpu_alloc.get('vcpu_instances', [])
        if vcpu_instances:
            vcpus_elem = ET.SubElement(self.domain, 'vcpus')
            for instance in vcpu_instances:
                vcpu_attrs = {
                    'id': str(instance.get('id', 0)),
                    'enabled': 'yes' if instance.get('enabled', True) else 'no',
                    'hotpluggable': 'yes' if instance.get('hotpluggable', False) else 'no',
                }
                if 'order' in instance:
                    vcpu_attrs['order'] = str(instance['order'])
                ET.SubElement(vcpus_elem, 'vcpu', **vcpu_attrs)

        # 检查是否需要创建 cpu 元素
        # 注意：topology 现在是 cpu_model 的顶层键，不是嵌套在 model 里
        topology = cpu_model.get('topology', {})
        # mode, match, check, migratable, deprecated_features 是 cpu_model 的顶层键
        cpu_mode = cpu_model.get('mode')
        cpu_match = cpu_model.get('match')
        cpu_check = cpu_model.get('check')
        cpu_migratable = cpu_model.get('migratable')
        cpu_deprecated_features = cpu_model.get('deprecated_features')
        # model_config 包含 model、vendor、vendor_id
        model_config = cpu_model.get('model', {})

        # 判断是否需要创建 <cpu> 元素
        need_cpu_elem = (
            topology
            or cpu_mode
            or cpu_match
            or cpu_check
            or cpu_migratable
            or cpu_deprecated_features
            or model_config.get('model')
            or model_config.get('vendor')
            or model_config.get('vendor_id')
            or cpu_model.get('feature', [])  # feature 现在是列表
            or cpu_model.get('cache', {}).get('mode')
            or cpu_model.get('maxphysaddr', {}).get('mode')
        )

        if not need_cpu_elem:
            return

        cpu_elem = ET.SubElement(self.domain, 'cpu')

        # 设置 cpu 元素的属性 (mode, match, check, migratable, deprecated_features)
        if cpu_mode:
            cpu_elem.set('mode', cpu_mode)
        if cpu_match:
            cpu_elem.set('match', cpu_match)
        if cpu_check:
            cpu_elem.set('check', cpu_check)
        if cpu_migratable:
            cpu_elem.set('migratable', cpu_migratable)
        if cpu_deprecated_features:
            cpu_elem.set('deprecated_features', cpu_deprecated_features)

        # 添加 topology 子元素
        if topology:
            sockets = topology.get('sockets', 1)
            dies = topology.get('dies', 1)
            clusters = topology.get('clusters', 1)
            cores = topology.get('cores', 1)
            threads = topology.get('threads', 1)

            ET.SubElement(
                cpu_elem,
                'topology',
                sockets=str(sockets),
                dies=str(dies),
                clusters=str(clusters),
                cores=str(cores),
                threads=str(threads),
            )

        # 添加 model 子元素
        if model_config.get('name'):
            model = ET.SubElement(cpu_elem, 'model')
            model.text = model_config['name']
            if model_config.get('fallback'):
                model.set('fallback', model_config['fallback'])
        # vendor 和 vendor_id 也移到 model_config 外层处理
        if model_config.get('vendor'):
            vendor = ET.SubElement(cpu_elem, 'vendor')
            vendor.text = model_config['vendor']
            if model_config.get('vendor_id'):
                vendor.set('id', model_config['vendor_id'])
        elif model_config.get('vendor_id'):
            # 只有 vendor_id 时也创建 vendor 元素
            ET.SubElement(cpu_elem, 'vendor', id=model_config['vendor_id'])

        # 添加 feature 子元素
        # feature 现在直接是一个列表
        features = cpu_model.get('feature', [])
        for feat in features:
            feat_attrs = {'name': feat['name']}
            if feat.get('policy'):
                feat_attrs['policy'] = feat['policy']
            ET.SubElement(cpu_elem, 'feature', **feat_attrs)

        # 添加 cache 子元素
        cache_config = cpu_model.get('cache', {})
        if cache_config.get('mode'):
            cache_attrs = {'mode': cache_config['mode']}
            if cache_config.get('level'):
                cache_attrs['level'] = str(cache_config['level'])
            ET.SubElement(cpu_elem, 'cache', **cache_attrs)

        # 添加 maxphysaddr 子元素
        maxphysaddr_config = cpu_model.get('maxphysaddr', {})
        if maxphysaddr_config.get('mode'):
            maxphysaddr_attrs = {'mode': maxphysaddr_config['mode']}
            if maxphysaddr_config.get('bits'):
                maxphysaddr_attrs['bits'] = maxphysaddr_config['bits']
            if maxphysaddr_config.get('limit'):
                maxphysaddr_attrs['limit'] = maxphysaddr_config['limit']
            ET.SubElement(cpu_elem, 'maxphysaddr', **maxphysaddr_attrs)

    def _add_os(self, config: dict) -> None:
        """添加操作系统配置."""
        os_booting = config.get('os_booting', {})

        os_elem = ET.SubElement(self.domain, 'os')

        # OS type, arch, machine
        os_type = os_booting.get('type', 'hvm')
        arch = os_booting.get('arch')
        machine = os_booting.get('machine')

        # 只在有值时才添加 arch 和 machine 属性（空字符串或 None 都不添加）
        type_attrs = {}
        if arch:
            type_attrs['arch'] = arch
        if machine:
            type_attrs['machine'] = machine
        type_elem = ET.SubElement(os_elem, 'type', **type_attrs)
        type_elem.text = os_type

        # Firmware auto-selection
        firmware = os_booting.get('firmware', '')
        if firmware:
            os_elem.set('firmware', firmware)

        # Firmware features
        firmware_features = os_booting.get('firmware_features', [])
        for feat in firmware_features:
            ET.SubElement(
                os_elem,
                'firmware',
                name=feat.get('name', ''),
                enabled=str(feat.get('enabled', '')).lower(),
            )

        # Loader configuration
        loader = os_booting.get('loader', {})
        secure_boot = os_booting.get('secure_boot', False)

        if isinstance(loader, dict) and loader.get('path'):
            loader_attrs = {}
            if loader.get('readonly') is not None:
                loader_attrs['readonly'] = 'yes' if loader['readonly'] else 'no'
            if loader.get('secure') or secure_boot:
                loader_attrs['secure'] = 'yes'
            if loader.get('type'):
                loader_attrs['type'] = loader['type']
            if loader.get('stateless'):
                loader_attrs['stateless'] = 'yes'
            if loader.get('format'):
                loader_attrs['format'] = loader['format']
            loader_elem = ET.SubElement(os_elem, 'loader', **loader_attrs)
            loader_elem.text = loader['path']
        elif os_booting.get('loader_path'):
            # Legacy support
            loader_attrs = {}
            if secure_boot:
                loader_attrs['secure'] = 'yes'
            loader_elem = ET.SubElement(os_elem, 'loader', **loader_attrs)
            loader_elem.text = os_booting['loader_path']
        elif secure_boot:
            # 如果没有loader路径但启用了secure_boot,创建一个带secure属性的loader元素
            ET.SubElement(os_elem, 'loader', secure='yes')

        # NVRAM configuration
        nvram = os_booting.get('nvram', {})
        if isinstance(nvram, dict) and (
            nvram.get('path') or nvram.get('template') or nvram.get('source')
        ):
            nvram_attrs = {}
            if nvram.get('type'):
                nvram_attrs['type'] = nvram['type']
            if nvram.get('template'):
                nvram_attrs['template'] = nvram['template']
            if nvram.get('templateFormat'):
                nvram_attrs['templateFormat'] = nvram['templateFormat']
            if nvram.get('format'):
                nvram_attrs['format'] = nvram['format']
            nvram_elem = ET.SubElement(os_elem, 'nvram', **nvram_attrs)
            # NVRAM source (for network/block backed) - 有 source 时 path 不作为文本内容
            nvram_source = nvram.get('source')
            if not nvram_source and nvram.get('path'):
                nvram_elem.text = nvram['path']
            if nvram_source:
                source_elem = ET.SubElement(nvram_elem, 'source')
                if nvram_source.get('protocol'):
                    source_elem.set('protocol', nvram_source['protocol'])
                if nvram_source.get('name'):
                    source_elem.set('name', nvram_source['name'])
                if nvram_source.get('file'):
                    source_elem.set('file', nvram_source['file'])
                if nvram_source.get('host'):
                    host_config = nvram_source['host']
                    if isinstance(host_config, dict):
                        host_elem = ET.SubElement(source_elem, 'host')
                        if host_config.get('name'):
                            host_elem.set('name', host_config['name'])
                        if host_config.get('port'):
                            host_elem.set('port', str(host_config['port']))
                    else:
                        ET.SubElement(source_elem, 'host', name=str(host_config))
                if nvram_source.get('auth'):
                    auth_config = nvram_source['auth']
                    auth_elem = ET.SubElement(source_elem, 'auth')
                    if auth_config.get('username'):
                        auth_elem.set('username', auth_config['username'])
                    if auth_config.get('secret'):
                        secret_config = auth_config['secret']
                        secret_elem = ET.SubElement(auth_elem, 'secret')
                        if secret_config.get('type'):
                            secret_elem.set('type', secret_config['type'])
                        if secret_config.get('usage'):
                            secret_elem.set('usage', secret_config['usage'])
        elif os_booting.get('nvram_path'):
            # Legacy support
            nvram_elem = ET.SubElement(os_elem, 'nvram')
            nvram_elem.text = os_booting['nvram_path']

        # Varstore (alternative to nvram)
        varstore = os_booting.get('varstore', {})
        if isinstance(varstore, dict) and varstore.get('path'):
            varstore_attrs = {'path': varstore['path']}
            if varstore.get('template'):
                varstore_attrs['template'] = varstore['template']
            ET.SubElement(os_elem, 'varstore', **varstore_attrs)

        # Boot devices
        boot_devices = os_booting.get('boot_devices', [])
        if isinstance(boot_devices, list):
            for dev in boot_devices:
                if isinstance(dev, dict):
                    ET.SubElement(os_elem, 'boot', dev=dev.get('dev', 'hd'))
                else:
                    ET.SubElement(os_elem, 'boot', dev=str(dev))

        # Boot menu
        bootmenu = os_booting.get('bootmenu', {})
        if isinstance(bootmenu, dict) and bootmenu.get('enable'):
            bootmenu_attrs = {'enable': 'yes'}
            timeout = bootmenu.get('timeout')
            if timeout is not None:
                # 转换为整数（可能是字符串）
                try:
                    timeout_val = int(timeout)
                    if timeout_val >= 0:
                        bootmenu_attrs['timeout'] = str(timeout_val)
                except (ValueError, TypeError):
                    pass
            ET.SubElement(os_elem, 'bootmenu', **bootmenu_attrs)

        # BIOS configuration
        bios = os_booting.get('bios', {})
        if isinstance(bios, dict):
            bios_attrs = {}
            if bios.get('useserial'):
                bios_attrs['useserial'] = 'yes'
            reboot_timeout = bios.get('rebootTimeout')
            if reboot_timeout is not None:
                # 转换为整数（可能是字符串）
                try:
                    timeout_val = int(reboot_timeout)
                    if timeout_val >= 0:
                        bios_attrs['rebootTimeout'] = str(timeout_val)
                except (ValueError, TypeError):
                    pass
            if bios_attrs:
                ET.SubElement(os_elem, 'bios', **bios_attrs)

        # SMBIOS
        smbios = os_booting.get('smbios', {})
        if isinstance(smbios, dict) and smbios.get('mode'):
            ET.SubElement(os_elem, 'smbios', mode=smbios['mode'])

        # Direct kernel boot
        kernel = os_booting.get('kernel')
        if kernel:
            ET.SubElement(os_elem, 'kernel').text = kernel
        initrd = os_booting.get('initrd')
        if initrd:
            ET.SubElement(os_elem, 'initrd').text = initrd
        cmdline = os_booting.get('cmdline')
        if cmdline:
            ET.SubElement(os_elem, 'cmdline').text = cmdline
        shim = os_booting.get('shim')
        if shim:
            ET.SubElement(os_elem, 'shim').text = shim
        dtb = os_booting.get('dtb')
        if dtb:
            ET.SubElement(os_elem, 'dtb').text = dtb

        # Host bootloader
        bootloader = os_booting.get('bootloader')
        host_bootloader = os_booting.get('host_bootloader')
        if host_bootloader and isinstance(host_bootloader, dict):
            bootloader_path = host_bootloader.get('path')
            if bootloader_path:
                ET.SubElement(self.domain, 'bootloader').text = bootloader_path
            bootloader_args = host_bootloader.get('args')
            if bootloader_args:
                ET.SubElement(self.domain, 'bootloader_args').text = bootloader_args
        elif bootloader:
            ET.SubElement(self.domain, 'bootloader').text = bootloader
            bootloader_args = os_booting.get('bootloader_args')
            if bootloader_args:
                ET.SubElement(self.domain, 'bootloader_args').text = bootloader_args

        # Container boot - 支持嵌套的 container 子字典和顶层字段两种格式
        container = os_booting.get('container', {})
        if isinstance(container, dict):
            # 优先从 container 子字典读取
            container_init = container.get('init')
            initargs = container.get('initargs', [])
            initenvs = container.get('initenvs', []) or container.get('initenv', [])
            initdir = container.get('initdir')
            inituser = container.get('inituser')
            initgroup = container.get('initgroup')
        else:
            # 兼容顶层字段格式
            container_init = os_booting.get('init')
            initargs = os_booting.get('initargs', [])
            initenvs = os_booting.get('initenv', [])
            initdir = os_booting.get('initdir')
            inituser = os_booting.get('inituser')
            initgroup = os_booting.get('initgroup')

        if container_init:
            ET.SubElement(os_elem, 'init').text = container_init
        if initargs:
            for arg in initargs:
                ET.SubElement(os_elem, 'initarg').text = arg
        if initenvs:
            for env in initenvs:
                ET.SubElement(os_elem, 'initenv', name=env.get('name', '')).text = env.get(
                    'value', ''
                )
        if initdir:
            ET.SubElement(os_elem, 'initdir').text = initdir
        if inituser:
            ET.SubElement(os_elem, 'inituser').text = inituser
        if initgroup:
            ET.SubElement(os_elem, 'initgroup').text = initgroup

        # ID mapping (for containers)
        idmap = os_booting.get('idmap', {})
        if isinstance(idmap, dict) and idmap.get('uid') and idmap.get('gid'):
            idmap_elem = ET.SubElement(os_elem, 'idmap')
            uid = idmap['uid']
            gid = idmap['gid']
            ET.SubElement(
                idmap_elem,
                'uid',
                start=str(uid.get('start', 0)),
                target=str(uid.get('target', 0)),
                count=str(uid.get('count', 0)),
            )
            ET.SubElement(
                idmap_elem,
                'gid',
                start=str(gid.get('start', 0)),
                target=str(gid.get('target', 0)),
                count=str(gid.get('count', 0)),
            )

        # ACPI tables
        acpi = os_booting.get('acpi', {})
        if isinstance(acpi, dict) and acpi.get('tables'):
            acpi_elem = ET.SubElement(os_elem, 'acpi')
            for table in acpi['tables']:
                if isinstance(table, dict):
                    ET.SubElement(
                        acpi_elem, 'table', type=table.get('type', 'raw')
                    ).text = table.get('path', '')

    def _add_features(self, config: dict) -> None:
        """添加虚拟化特性.

        支持以下特性组:
        - general: 通用特性 (pae, acpi, apic, hap, viridian, privnet, etc.)
        - hyperv: Hyper-V enlightenment 特性
        - kvm: KVM 特性
        - xen: Xen 特性
        - tcg: TCG 加速器特性
        """
        features_config = config.get('hypervisor_features', {})
        features_elem = None  # <features> 元素，按需创建

        def get_features_elem():
            """获取或创建 features 元素."""
            nonlocal features_elem
            if features_elem is None:
                features_elem = self.domain.find('features')
                if features_elem is None:
                    features_elem = ET.SubElement(self.domain, 'features')
            return features_elem

        # ========== 通用特性 ==========
        general = features_config.get('general', {})
        if any(general.values()):
            features = get_features_elem()

            # Boolean 特性 (on/off -> 生成元素，None/False -> 不生成)
            bool_features = [
                'pae',
                'acpi',
                'apic',
                'hap',
                'viridian',
                'privnet',
                'pvspinlock',
                'pmu',
                'vmport',
                'vmcoreinfo',
                'ras',
                'ioapic',
                'hpt',
                'htm',
                'nested-hv',
                'ccf-assist',
                'cfpc',
                'sbbc',
                'ibs',
                'ps2',
                'aia',
                'virtualization',
            ]
            for feat_name in bool_features:
                # 支持 boolean 和字符串 'on'/'off'
                val = general.get(feat_name)
                if val is True or val == 'on':
                    ET.SubElement(features, feat_name)

            # SMM 特性 (可能带 tseg 子元素)
            if general.get('smm') is True or general.get('smm') == 'on':
                smm_elem = ET.SubElement(features, 'smm', state='on')
                smm_tseg = general.get('smm_tseg')
                if smm_tseg:
                    tseg_elem = ET.SubElement(smm_elem, 'tseg', unit='MiB')
                    tseg_elem.text = smm_tseg

            # GIC (带 version 属性)
            gic_version = general.get('gic_version')
            if gic_version and gic_version != 'None':
                ET.SubElement(features, 'gic', version=gic_version)

            # IOAPIC (带 driver 属性)
            ioapic_driver = general.get('ioapic_driver')
            if ioapic_driver and ioapic_driver != 'None':
                ET.SubElement(features, 'ioapic', driver=ioapic_driver)

            # HPT (带 resizing 属性和 maxpagesize 子元素)
            hpt_resizing = general.get('hpt_resizing')
            hpt_maxpagesize = general.get('hpt_maxpagesize')
            if hpt_resizing or hpt_maxpagesize:
                hpt_attrs = {}
                if hpt_resizing and hpt_resizing != 'None':
                    hpt_attrs['resizing'] = hpt_resizing
                hpt_elem = ET.SubElement(features, 'hpt', **hpt_attrs)
                if hpt_maxpagesize and hpt_maxpagesize != 'None':
                    # 解析单位
                    if 'GiB' in hpt_maxpagesize:
                        maxps_elem = ET.SubElement(hpt_elem, 'maxpagesize', unit='GiB')
                        maxps_elem.text = hpt_maxpagesize.split()[0]
                    elif 'MiB' in hpt_maxpagesize:
                        maxps_elem = ET.SubElement(hpt_elem, 'maxpagesize', unit='MiB')
                        maxps_elem.text = hpt_maxpagesize.split()[0]
                    elif 'KiB' in hpt_maxpagesize:
                        maxps_elem = ET.SubElement(hpt_elem, 'maxpagesize', unit='KiB')
                        maxps_elem.text = hpt_maxpagesize.split()[0]
                    else:
                        maxps_elem = ET.SubElement(hpt_elem, 'maxpagesize', unit='KiB')
                        maxps_elem.text = hpt_maxpagesize

            # MSRs (bhyve, 带 unknown 属性)
            msrs_unknown = general.get('msrs_unknown')
            if msrs_unknown and msrs_unknown != 'None':
                ET.SubElement(features, 'msrs', unknown=msrs_unknown)

            # Async teardown (带 enabled 属性)
            async_teardown = general.get('async_teardown')
            if async_teardown and async_teardown != 'None':
                ET.SubElement(features, 'async-teardown', enabled=async_teardown)

            # TCG (带 tb-cache 子元素)
            tcg_tb_cache = general.get('tcg_tb_cache')
            if tcg_tb_cache:
                tcg_elem = ET.SubElement(features, 'tcg')
                tb_cache_elem = ET.SubElement(tcg_elem, 'tb-cache', unit='MiB')
                tb_cache_elem.text = tcg_tb_cache

        # ========== Hyper-V 特性 ==========
        hyperv = features_config.get('hyperv', {})
        hyperv_features_list = [
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
            'avic',
            'emsr_bitmap',
            'xmm_input',
        ]
        has_hyperv = any(hyperv.get(f) == 'on' for f in hyperv_features_list)
        has_hyperv = has_hyperv or bool(hyperv.get('vendor_id'))

        if has_hyperv:
            features = get_features_elem()
            hyperv_elem = ET.SubElement(features, 'hyperv')

            # 模式属性
            if hyperv.get('mode') and hyperv.get('mode') != 'None':
                hyperv_elem.set('mode', hyperv['mode'])

            # 标准特性 (state='on')
            for feat_name in hyperv_features_list:
                if hyperv.get(feat_name) == 'on':
                    ET.SubElement(hyperv_elem, feat_name, state='on')

            # Vendor ID (带 value 属性)
            vendor_id = hyperv.get('vendor_id')
            if vendor_id:
                ET.SubElement(hyperv_elem, 'vendor_id', state='on', value=vendor_id)

            # Spinlocks (带 retries 属性)
            if hyperv.get('spinlocks') == 'on':
                retries = hyperv.get('spinlocks_retries', '4096')
                # 找到刚创建的 spinlocks 元素并添加属性
                for elem in hyperv_elem:
                    if elem.tag == 'spinlocks':
                        elem.set('retries', retries)
                        break

            # TLBflush 子特性 (direct, extended)
            if hyperv.get('tlbflush') == 'on':
                for elem in hyperv_elem:
                    if elem.tag == 'tlbflush':
                        tlbflush_direct = hyperv.get('tlbflush_direct')
                        if tlbflush_direct and tlbflush_direct != 'None':
                            ET.SubElement(elem, 'direct', state=tlbflush_direct)
                        tlbflush_extended = hyperv.get('tlbflush_extended')
                        if tlbflush_extended and tlbflush_extended != 'None':
                            ET.SubElement(elem, 'extended', state=tlbflush_extended)
                        break

            # Stimer 子特性 (direct)
            if hyperv.get('stimer') == 'on':
                for elem in hyperv_elem:
                    if elem.tag == 'stimer':
                        stimer_direct = hyperv.get('stimer_direct')
                        if stimer_direct and stimer_direct != 'None':
                            ET.SubElement(elem, 'direct', state=stimer_direct)
                        break

        # ========== KVM 特性 ==========
        kvm = features_config.get('kvm', {})
        kvm_features_list = ['hidden', 'hint_dedicated', 'poll_control', 'pv_ipi', 'dirty_ring']
        has_kvm = any(kvm.get(f) == 'on' for f in kvm_features_list)

        if has_kvm:
            features = get_features_elem()
            kvm_elem = ET.SubElement(features, 'kvm')

            # KVM 特性 (state='on'/'off')
            for feat_name in ['hidden', 'hint_dedicated', 'poll_control', 'pv_ipi']:
                val = kvm.get(feat_name)
                if val and val != 'None':
                    ET.SubElement(kvm_elem, feat_name.replace('_', '-'), state=val)

            # Dirty ring (带 size 属性)
            if kvm.get('dirty_ring') == 'on':
                size = kvm.get('dirty_ring_size', '4096')
                ET.SubElement(kvm_elem, 'dirty-ring', state='on', size=size)

        # ========== Xen 特性 ==========
        xen = features_config.get('xen', {})
        xen_features_list = ['e820_host', 'passthrough']
        has_xen = any(xen.get(f) == 'on' for f in xen_features_list)

        if has_xen:
            features = get_features_elem()
            xen_elem = ET.SubElement(features, 'xen')

            # e820_host
            if xen.get('e820_host') == 'on':
                ET.SubElement(xen_elem, 'e820_host', state='on')

            # passthrough (带 mode 属性)
            if xen.get('passthrough') == 'on':
                passthrough_mode = xen.get('passthrough_mode')
                if passthrough_mode and passthrough_mode != 'None':
                    ET.SubElement(xen_elem, 'passthrough', state='on', mode=passthrough_mode)
                else:
                    ET.SubElement(xen_elem, 'passthrough', state='on')

    def _add_clock(self, config: dict) -> None:
        """添加时钟配置.

        支持以下配置:
        - offset: utc, localtime, timezone, variable, absolute
        - timers: rtc, pit, tsc, hpet, kvmclock
        """
        time_config = config.get('time_keeping', {})
        if not time_config:
            return

        offset = time_config.get('offset')
        if not offset:
            # offset 为 None 时不生成 clock 元素
            return

        clock_attrs = {'offset': offset}

        if offset == 'timezone' and time_config.get('timezone'):
            clock_attrs['timezone'] = time_config['timezone']
        elif offset == 'variable':
            adjustment = time_config.get('adjustment')
            if adjustment:
                clock_attrs['adjustment'] = adjustment
            basis = time_config.get('basis')
            if basis:
                clock_attrs['basis'] = basis
        elif offset == 'absolute':
            start = time_config.get('start')
            if start:
                clock_attrs['start'] = start

        clock = ET.SubElement(self.domain, 'clock', **clock_attrs)

        timers = time_config.get('timers', {})

        # RTC timer
        rtc = timers.get('rtc', {})
        rtc_present = rtc.get('present')
        rtc_tickpolicy = rtc.get('tickpolicy')
        rtc_track = rtc.get('track')

        if rtc_present == 'yes' or rtc_tickpolicy or rtc_track:
            rtc_attrs = {'name': 'rtc'}
            if rtc_tickpolicy:
                rtc_attrs['tickpolicy'] = rtc_tickpolicy
            if rtc_track:
                rtc_attrs['track'] = rtc_track
            if rtc_present == 'no':
                rtc_attrs['present'] = 'no'

            rtc_elem = ET.SubElement(clock, 'timer', **rtc_attrs)

            # 添加 catchup 子元素 (仅当 tickpolicy=catchup 时)
            if rtc_tickpolicy == 'catchup':
                catchup_threshold = rtc.get('catchup_threshold')
                catchup_slew = rtc.get('catchup_slew')
                catchup_limit = rtc.get('catchup_limit')

                if catchup_threshold or catchup_slew or catchup_limit:
                    catchup_attrs = {}
                    if catchup_threshold:
                        catchup_attrs['threshold'] = catchup_threshold
                    if catchup_slew:
                        catchup_attrs['slew'] = catchup_slew
                    if catchup_limit:
                        catchup_attrs['limit'] = catchup_limit

                    ET.SubElement(rtc_elem, 'catchup', **catchup_attrs)

        # PIT timer
        pit = timers.get('pit', {})
        pit_present = pit.get('present')
        pit_tickpolicy = pit.get('tickpolicy')

        if pit_present == 'yes' or pit_tickpolicy:
            pit_attrs = {'name': 'pit'}
            if pit_tickpolicy:
                pit_attrs['tickpolicy'] = pit_tickpolicy
            if pit_present == 'no':
                pit_attrs['present'] = 'no'

            ET.SubElement(clock, 'timer', **pit_attrs)

        # TSC timer
        tsc = timers.get('tsc', {})
        tsc_present = tsc.get('present')
        tsc_mode = tsc.get('mode')
        tsc_frequency = tsc.get('frequency')

        if tsc_present == 'yes' or tsc_mode or tsc_frequency:
            tsc_attrs = {'name': 'tsc'}
            if tsc_mode:
                tsc_attrs['mode'] = tsc_mode
            if tsc_frequency:
                tsc_attrs['frequency'] = tsc_frequency
            if tsc_present == 'no':
                tsc_attrs['present'] = 'no'

            ET.SubElement(clock, 'timer', **tsc_attrs)

        # HPET timer
        hpet = timers.get('hpet', {})
        hpet_present = hpet.get('present')

        if hpet_present == 'yes':
            ET.SubElement(clock, 'timer', name='hpet', present='yes')
        elif hpet_present == 'no':
            ET.SubElement(clock, 'timer', name='hpet', present='no')

        # kvmclock timer
        kvmclock = timers.get('kvmclock', {})
        kvmclock_present = kvmclock.get('present')

        if kvmclock_present == 'yes':
            ET.SubElement(clock, 'timer', name='kvmclock', present='yes')
        elif kvmclock_present == 'no':
            ET.SubElement(clock, 'timer', name='kvmclock', present='no')

    def _add_pm(self, config: dict) -> None:
        """添加电源管理配置.

        None 值表示不生成对应的 XML 元素。
        """
        pm_config = config.get('power_management', {})
        if not pm_config:
            return

        pm = ET.SubElement(self.domain, 'pm')

        # 只有配置了值才生成 suspend-to-mem 元素
        if 'suspend_to_mem' in pm_config:
            suspend_mem = pm_config.get('suspend_to_mem', 'yes')
            ET.SubElement(pm, 'suspend-to-mem', enabled=suspend_mem)

        # 只有配置了值才生成 suspend-to-disk 元素
        if 'suspend_to_disk' in pm_config:
            suspend_disk = pm_config.get('suspend_to_disk', 'yes')
            ET.SubElement(pm, 'suspend-to-disk', enabled=suspend_disk)

    def _add_events(self, config: dict) -> None:
        """添加事件配置.

        None 值表示不生成对应的 XML 元素。
        """
        events_config = config.get('events_configuration', {})
        if not events_config:
            return

        on_poweroff = events_config.get('on_poweroff')
        if on_poweroff and on_poweroff != 'None':
            ET.SubElement(self.domain, 'on_poweroff').text = on_poweroff

        on_reboot = events_config.get('on_reboot')
        if on_reboot and on_reboot != 'None':
            ET.SubElement(self.domain, 'on_reboot').text = on_reboot

        on_crash = events_config.get('on_crash')
        if on_crash and on_crash != 'None':
            ET.SubElement(self.domain, 'on_crash').text = on_crash

        on_lockfailure = events_config.get('on_lockfailure')
        if on_lockfailure and on_lockfailure != 'None':
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

        # 处理 disk_devices (来自 devices_tab 的磁盘设备)
        disk_devices = config.get('disk_devices', [])
        for disk in disk_devices:
            self._add_disk_device(devices, disk)

        # 支持复数和单数形式
        disks = devices_config.get('disks', devices_config.get('disk', []))
        for disk in disks:
            self._add_disk(devices, disk)

        interfaces = devices_config.get('interfaces', devices_config.get('interface', []))
        for iface in interfaces:
            self._add_interface(devices, iface)

        # graphics 可能是单个对象或列表(支持 graphics 和 graphic 两种字段名)
        graphics = devices_config.get('graphics', devices_config.get('graphic', None))
        if graphics:
            if isinstance(graphics, list):
                for g in graphics:
                    self._add_graphics(devices, g)
            else:
                self._add_graphics(devices, graphics)

        # videos 可能是单个对象或列表(支持 videos 和 video 两种字段名)
        videos = devices_config.get('videos', devices_config.get('video', []))
        if isinstance(videos, list):
            for video in videos:
                self._add_video(devices, video)
        elif videos:
            self._add_video(devices, videos)

        controllers = devices_config.get('controllers', devices_config.get('controller', []))
        for ctrl in controllers:
            self._add_controller(devices, ctrl)

        serials = devices_config.get('serials', devices_config.get('serial', []))
        for serial in serials:
            self._add_serial(devices, serial)

        # 添加默认的控制台
        console = ET.SubElement(devices, 'console', type='pty')
        ET.SubElement(console, 'target', type='serial', port='0')

        inputs = devices_config.get('inputs', devices_config.get('input', []))
        for inp in inputs:
            self._add_input(devices, inp)

        sounds = devices_config.get('sounds', devices_config.get('sound', []))
        for sound in sounds:
            ET.SubElement(devices, 'sound', model=sound.get('model', 'ich6'))

        hostdevs = devices_config.get('hostdevs', devices_config.get('hostdev', []))
        for hostdev in hostdevs:
            self._add_hostdev(devices, hostdev)

    def _add_disk_device(self, devices: ET.Element, disk: dict) -> None:
        """添加磁盘设备 (支持 file, block, network, volume, dir, nvme, vhostuser, vhostvdpa, ctl 类型)."""
        disk_type = disk.get('type', 'file')
        device_type = disk.get('device', 'disk')

        type_map = {
            'file': 'file',
            'block': 'block',
            'network': 'network',
            'volume': 'volume',
            'dir': 'dir',
            'nvme': 'nvme',
            'vhostuser': 'vhostuser',
            'vhostvdpa': 'vhostvdpa',
            'ctl': 'ctl',
        }

        disk_attrs = {'type': type_map.get(disk_type, 'file'), 'device': device_type}
        disk_elem = ET.SubElement(devices, 'disk', **disk_attrs)

        # 驱动 (仅 file 和 block 类型需要)
        if disk_type in ('file', 'block'):
            driver = disk.get('driver', 'qcow2')
            driver_attrs = {'name': 'qemu', 'type': driver}
            ET.SubElement(disk_elem, 'driver', **driver_attrs)

        # Source - 根据类型不同而不同
        if disk_type == 'file':
            source = disk.get('source', '')
            if source:
                ET.SubElement(disk_elem, 'source', file=source)
        elif disk_type == 'block':
            source = disk.get('source', '')
            if source:
                ET.SubElement(disk_elem, 'source', dev=source)
        elif disk_type == 'network':
            protocol = disk.get('protocol', 'rbd')
            source_name = disk.get('source', '')
            source_attrs = {'protocol': protocol, 'name': source_name}
            source_elem = ET.SubElement(disk_elem, 'source', **source_attrs)

            # 主机
            host = disk.get('host', '')
            port = disk.get('port', '')
            if host:
                host_attrs = {'name': host}
                if port:
                    host_attrs['port'] = port
                ET.SubElement(source_elem, 'host', **host_attrs)

            # 认证
            if disk.get('auth') and disk.get('username') and disk.get('secret'):
                auth_elem = ET.SubElement(source_elem, 'auth', username=disk['username'])
                ET.SubElement(auth_elem, 'secret', type='ceph', usage=disk['secret'])
        elif disk_type == 'volume':
            pool = disk.get('pool', '')
            volume = disk.get('volume', '')
            if pool and volume:
                ET.SubElement(disk_elem, 'source', pool=pool, volume=volume)
        elif disk_type == 'dir':
            source = disk.get('source', '')
            if source:
                ET.SubElement(disk_elem, 'source', dir=source)
        elif disk_type == 'nvme':
            namespace = disk.get('namespace', '1')
            pci = disk.get('pci', '')
            if pci:
                # 解析 PCI 地址
                pci_parts = pci.replace(':', '.').split('.')
                addr_attrs = {
                    'domain': f'0x{pci_parts[0]}',
                    'bus': f'0x{pci_parts[1]}',
                    'slot': f'0x{pci_parts[2]}',
                    'function': f'0x{pci_parts[3] if len(pci_parts) > 3 else "0"}',
                }
                source_elem = ET.SubElement(
                    disk_elem, 'source', type='pci', managed='yes', namespace=namespace
                )
                ET.SubElement(source_elem, 'address', **addr_attrs)
        elif disk_type == 'vhostuser':
            source = disk.get('source', '')
            if source:
                ET.SubElement(disk_elem, 'source', type='unix', path=source)
        elif disk_type == 'vhostvdpa':
            source = disk.get('source', '')
            if source:
                ET.SubElement(disk_elem, 'source', dev=source)
        elif disk_type == 'ctl':
            source = disk.get('source', '')
            if source:
                ET.SubElement(disk_elem, 'source', dev=source)

        # Target
        target_dev = disk.get('target_dev', 'vda')
        bus = disk.get('bus', 'virtio')
        ET.SubElement(disk_elem, 'target', dev=target_dev, bus=bus)

        # 只读
        if disk.get('readonly'):
            ET.SubElement(disk_elem, 'readonly')

        # 启动顺序
        boot_order = disk.get('boot_order')
        if boot_order:
            ET.SubElement(disk_elem, 'boot', order=boot_order)

        # 启动策略
        startup_policy = disk.get('startup_policy')
        if startup_policy:
            source_elem = disk_elem.find('source')
            if source_elem is not None:
                source_elem.set('startupPolicy', startup_policy)

    def _add_disk(self, devices: ET.Element, disk: dict) -> None:
        """添加磁盘设备."""
        # 支持 disk_type 和 type 两种字段
        disk_type_val = disk.get('disk_type') or disk.get('type', 'file')
        # 将 qcow2, raw 等格式转换为 file 类型
        if disk_type_val in ('qcow2', 'raw', 'qed', 'vdi', 'vmdk', 'vpc'):
            disk_type = 'file'
        else:
            disk_type = disk_type_val
        device = disk.get('device', 'disk')

        disk_attrs = {'type': disk_type, 'device': device}
        if disk.get('snapshot'):
            disk_attrs['snapshot'] = disk['snapshot']

        disk_elem = ET.SubElement(devices, 'disk', **disk_attrs)

        driver_attrs = {
            'name': disk.get('driver_name', 'qemu'),
            'type': disk.get('driver_type', disk.get('format', disk.get('type', 'qcow2'))),
        }
        if disk.get('cache'):
            driver_attrs['cache'] = disk['cache']
        if disk.get('io'):
            driver_attrs['io'] = disk['io']
        if disk.get('discard'):
            driver_attrs['discard'] = disk['discard']
        ET.SubElement(disk_elem, 'driver', **driver_attrs)

        # 支持 source_file 和 file 两种字段名
        source_file = disk.get('source_file') or disk.get('file') or disk.get('path')
        if disk_type == 'file' and source_file:
            ET.SubElement(disk_elem, 'source', file=source_file)
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

        # 支持 target_dev 和 target 两种字段名
        target_dev = disk.get('target_dev') or disk.get('target', 'vda')
        target_attrs = {'dev': target_dev, 'bus': disk.get('bus', 'virtio')}
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

        # 支持不同字段名
        source = iface.get('source')
        if iface_type == 'network':
            ET.SubElement(iface_elem, 'source', network=source or 'default')
        elif iface_type == 'bridge':
            ET.SubElement(iface_elem, 'source', bridge=source or iface.get('bridge', 'br0'))
        elif iface_type == 'direct':
            ET.SubElement(
                iface_elem, 'source', dev=iface.get('dev', 'eth0'), mode=iface.get('mode', 'bridge')
            )
        elif iface_type == 'user':
            ET.SubElement(iface_elem, 'source', network='user')
        elif iface_type == 'internal':
            ET.SubElement(iface_elem, 'source', dev=iface.get('dev', ''))

        model = iface.get('model', 'virtio')
        if isinstance(model, dict):
            model_type = model.get('type', 'virtio')
        else:
            model_type = model
        ET.SubElement(iface_elem, 'model', type=model_type)

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
                ET.SubElement(
                    hostdev_elem, 'rom', bar=hostdev['rom_bar'], file=hostdev.get('rom_file', '')
                )

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
        if not backing_config:
            return

        # 检查是否有任何非默认配置
        has_config = (
            backing_config.get('hugepages')
            or backing_config.get('nosharepages')
            or backing_config.get('locked')
            or backing_config.get('discard')
            or (
                backing_config.get('source_type')
                and backing_config.get('source_type') != 'anonymous'
            )
            or (
                backing_config.get('access_mode') and backing_config.get('access_mode') != 'private'
            )
            or (
                backing_config.get('allocation_mode')
                and backing_config.get('allocation_mode') != 'ondemand'
            )
            or backing_config.get('allocation_threads')
        )
        if not has_config:
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
        if access_mode and access_mode != 'private':
            ET.SubElement(backing, 'access', mode=access_mode)

        allocation_mode = backing_config.get('allocation_mode')
        if allocation_mode and allocation_mode != 'ondemand':
            alloc_attrs = {'mode': allocation_mode}
            threads = backing_config.get('allocation_threads')
            if threads:
                alloc_attrs['threads'] = threads
            ET.SubElement(backing, 'allocation', **alloc_attrs)

    def _add_memory_tuning(self, config: dict) -> None:
        """添加内存优化配置."""
        tuning_config = config.get('memory_tuning', {})
        if not tuning_config:
            return

        # 检查是否有有效配置（排除 None 和空值）
        has_valid_config = False
        for key in ['hard_limit', 'soft_limit', 'swap_hard_limit', 'min_guarantee']:
            item = tuning_config.get(key)
            if isinstance(item, dict) and item.get('value') and item.get('value') != '':
                has_valid_config = True
                break

        if not has_valid_config:
            return

        memtune = ET.SubElement(self.domain, 'memtune')

        # hard_limit
        hard_limit = tuning_config.get('hard_limit', {})
        if (
            isinstance(hard_limit, dict)
            and hard_limit.get('value')
            and hard_limit.get('value') != ''
        ):
            value = hard_limit['value']
            unit = hard_limit.get('unit', 'KiB')
            ET.SubElement(memtune, 'hard_limit', unit=unit).text = str(value)

        # soft_limit
        soft_limit = tuning_config.get('soft_limit', {})
        if (
            isinstance(soft_limit, dict)
            and soft_limit.get('value')
            and soft_limit.get('value') != ''
        ):
            value = soft_limit['value']
            unit = soft_limit.get('unit', 'KiB')
            ET.SubElement(memtune, 'soft_limit', unit=unit).text = str(value)

        # swap_hard_limit
        swap_hard_limit = tuning_config.get('swap_hard_limit', {})
        if (
            isinstance(swap_hard_limit, dict)
            and swap_hard_limit.get('value')
            and swap_hard_limit.get('value') != ''
        ):
            value = swap_hard_limit['value']
            unit = swap_hard_limit.get('unit', 'KiB')
            ET.SubElement(memtune, 'swap_hard_limit', unit=unit).text = str(value)

        # min_guarantee
        min_guarantee = tuning_config.get('min_guarantee', {})
        if (
            isinstance(min_guarantee, dict)
            and min_guarantee.get('value')
            and min_guarantee.get('value') != ''
        ):
            value = min_guarantee['value']
            unit = min_guarantee.get('unit', 'KiB')
            ET.SubElement(memtune, 'min_guarantee', unit=unit).text = str(value)

    def _add_cpu_tuning(self, config: dict) -> None:
        """添加 CPU 优化配置 (cputune).

        支持以下配置:
        - vcpupin: vCPU 亲和性绑定 (列表)
        - emulatorpin: 模拟器线程亲和性
        - iothreadpin: IOThread 亲和性 (列表)
        - shares: CPU 份额
        - period/quota: 每 vCPU 带宽控制
        - global_period/global_quota: 全局带宽控制
        - emulator_period/emulator_quota: 模拟器带宽控制
        - iothread_period/iothread_quota: IOThread 带宽控制
        - vcpusched/iothreadsched/emulatorsched: 调度器配置
        - cachetune: 缓存分配 (resctrl)
        - memorytune: 内存带宽分配 (resctrl)
        """
        tuning_config = config.get('cpu_tuning', {})
        if not tuning_config:
            return

        # 检查是否有任何有效配置
        has_config = False
        for key in [
            'vcpupin',
            'emulatorpin',
            'iothreadpin',
            'shares',
            'period',
            'quota',
            'global_period',
            'global_quota',
            'emulator_period',
            'emulator_quota',
            'iothread_period',
            'iothread_quota',
            'vcpusched',
            'iothreadsched',
            'emulatorsched',
            'cachetune',
            'memorytune',
        ]:
            if key in tuning_config:
                has_config = True
                break

        if not has_config:
            return

        cputune = ET.SubElement(self.domain, 'cputune')

        # ========== vcpupin (列表) ==========
        vcpupins = tuning_config.get('vcpupin', [])
        for pin in vcpupins:
            if isinstance(pin, dict):
                vcpu = pin.get('vcpu')
                cpuset = pin.get('cpuset')
                if vcpu is not None and cpuset:
                    ET.SubElement(cputune, 'vcpupin', vcpu=str(vcpu), cpuset=cpuset)

        # ========== emulatorpin ==========
        emulatorpin = tuning_config.get('emulatorpin')
        if emulatorpin:
            ET.SubElement(cputune, 'emulatorpin', cpuset=emulatorpin)

        # ========== iothreadpin (列表) ==========
        iothreadpins = tuning_config.get('iothreadpin', [])
        for pin in iothreadpins:
            if isinstance(pin, dict):
                iothread = pin.get('iothread')
                cpuset = pin.get('cpuset')
                if iothread is not None and cpuset:
                    ET.SubElement(cputune, 'iothreadpin', iothread=str(iothread), cpuset=cpuset)

        # ========== 带宽控制 ==========
        shares = tuning_config.get('shares')
        if shares is not None:
            ET.SubElement(cputune, 'shares').text = str(shares)
        period = tuning_config.get('period')
        if period is not None:
            ET.SubElement(cputune, 'period').text = str(period)
        quota = tuning_config.get('quota')
        if quota is not None:
            ET.SubElement(cputune, 'quota').text = str(quota)

        global_period = tuning_config.get('global_period')
        if global_period is not None:
            ET.SubElement(cputune, 'global_period').text = str(global_period)
        global_quota = tuning_config.get('global_quota')
        if global_quota is not None:
            ET.SubElement(cputune, 'global_quota').text = str(global_quota)

        emulator_period = tuning_config.get('emulator_period')
        if emulator_period is not None:
            ET.SubElement(cputune, 'emulator_period').text = str(emulator_period)
        emulator_quota = tuning_config.get('emulator_quota')
        if emulator_quota is not None:
            ET.SubElement(cputune, 'emulator_quota').text = str(emulator_quota)

        iothread_period = tuning_config.get('iothread_period')
        if iothread_period is not None:
            ET.SubElement(cputune, 'iothread_period').text = str(iothread_period)
        iothread_quota = tuning_config.get('iothread_quota')
        if iothread_quota is not None:
            ET.SubElement(cputune, 'iothread_quota').text = str(iothread_quota)

        # ========== 调度器配置 ==========
        vcpusched = tuning_config.get('vcpusched')
        if vcpusched and isinstance(vcpusched, dict):
            sched_attrs = {'scheduler': vcpusched.get('scheduler', 'batch')}
            if vcpusched.get('vcpus'):
                sched_attrs['vcpus'] = vcpusched['vcpus']
            priority = vcpusched.get('priority')
            if priority is not None and vcpusched.get('scheduler') in ('fifo', 'rr'):
                sched_attrs['priority'] = str(priority)
            ET.SubElement(cputune, 'vcpusched', **sched_attrs)

        iothreadsched = tuning_config.get('iothreadsched')
        if iothreadsched and isinstance(iothreadsched, dict):
            sched_attrs = {'scheduler': iothreadsched.get('scheduler', 'batch')}
            if iothreadsched.get('iothreads'):
                sched_attrs['iothreads'] = iothreadsched['iothreads']
            priority = iothreadsched.get('priority')
            if priority is not None and iothreadsched.get('scheduler') in ('fifo', 'rr'):
                sched_attrs['priority'] = str(priority)
            ET.SubElement(cputune, 'iothreadsched', **sched_attrs)

        emulatorsched = tuning_config.get('emulatorsched')
        if emulatorsched and isinstance(emulatorsched, dict):
            sched_attrs = {'scheduler': emulatorsched.get('scheduler', 'batch')}
            priority = emulatorsched.get('priority')
            if priority is not None and emulatorsched.get('scheduler') in ('fifo', 'rr'):
                sched_attrs['priority'] = str(priority)
            ET.SubElement(cputune, 'emulatorsched', **sched_attrs)

        # ========== 缓存调优 (cachetune) ==========
        cachetunes = tuning_config.get('cachetune', [])
        if cachetunes and isinstance(cachetunes, list):
            for ct in cachetunes:
                if not isinstance(ct, dict):
                    continue
                vcpus = ct.get('vcpus')
                if not vcpus:
                    continue
                cachetune_elem = ET.SubElement(cputune, 'cachetune', vcpus=vcpus)
                cache = ct.get('cache')
                if cache and isinstance(cache, dict):
                    cache_attrs = {
                        'level': str(cache.get('level', 3)),
                        'type': cache.get('type', 'both'),
                    }
                    if cache.get('id') is not None:
                        cache_attrs['id'] = str(cache['id'])
                    if cache.get('size'):
                        cache_attrs['size'] = str(cache['size'])
                    if cache.get('unit'):
                        cache_attrs['unit'] = cache['unit']
                    ET.SubElement(cachetune_elem, 'cache', **cache_attrs)
                monitor = ct.get('monitor')
                if monitor and isinstance(monitor, dict):
                    monitor_attrs = {
                        'level': str(monitor.get('level', 3)),
                        'vcpus': monitor.get('vcpus', vcpus),
                    }
                    ET.SubElement(cachetune_elem, 'monitor', **monitor_attrs)

        # ========== 内存带宽调优 (memorytune) ==========
        memorytunes = tuning_config.get('memorytune', [])
        if memorytunes and isinstance(memorytunes, list):
            for mt in memorytunes:
                if not isinstance(mt, dict):
                    continue
                vcpus = mt.get('vcpus')
                if not vcpus:
                    continue
                memorytune_elem = ET.SubElement(cputune, 'memorytune', vcpus=vcpus)
                node = mt.get('node')
                if node and isinstance(node, dict):
                    node_attrs = {
                        'id': str(node.get('id', 0)),
                    }
                    if node.get('bandwidth') is not None:
                        node_attrs['bandwidth'] = str(node['bandwidth'])
                    ET.SubElement(memorytune_elem, 'node', **node_attrs)

    def _add_numa_tuning(self, config: dict) -> None:
        """添加 NUMA 优化配置."""
        numa_config = config.get('numa_node_tuning', {})
        if not numa_config:
            return

        # 检查是否有有效配置
        memory_mode = numa_config.get('memory_mode')
        memory_nodeset = numa_config.get('memory_nodeset')
        memory_placement = numa_config.get('memory_placement')
        memnodes_list = numa_config.get('memnodes', [])

        has_memory_config = (
            (memory_mode and memory_mode != 'None')
            or memory_nodeset
            or (memory_placement and memory_placement != 'None')
        )
        has_memnodes = any(node.get('cellid') for node in memnodes_list)

        if not has_memory_config and not has_memnodes:
            return

        numatune = ET.SubElement(self.domain, 'numatune')

        # 添加 memory 元素
        if has_memory_config:
            memory_attrs = {}
            if memory_mode and memory_mode != 'None':
                memory_attrs['mode'] = memory_mode
            if memory_nodeset:
                memory_attrs['nodeset'] = memory_nodeset
            if memory_placement and memory_placement != 'None':
                memory_attrs['placement'] = memory_placement
            ET.SubElement(numatune, 'memory', **memory_attrs)

        # 添加 memnode 元素
        for node in memnodes_list:
            cellid = node.get('cellid')
            if not cellid:
                continue

            node_mode = node.get('mode')
            node_nodeset = node.get('nodeset')

            memnode_attrs = {'cellid': str(cellid)}
            if node_mode and node_mode != 'None':
                memnode_attrs['mode'] = node_mode
            if node_nodeset:
                memnode_attrs['nodeset'] = node_nodeset

            ET.SubElement(numatune, 'memnode', **memnode_attrs)

    def _add_block_io_tuning(self, config: dict) -> None:
        """添加块 IO 优化配置."""
        io_config = config.get('block_io_tuning', {})
        if not io_config:
            return

        # 检查是否有有效配置
        has_weight = io_config.get('weight')
        has_devices = io_config.get('devices', [])

        if not has_weight and not has_devices:
            return

        blkiotune = ET.SubElement(self.domain, 'blkiotune')

        # 全局权重
        if has_weight:
            ET.SubElement(blkiotune, 'weight').text = str(has_weight)

        # 支持多个设备条目
        for device in has_devices:
            if not device.get('path'):
                continue

            device_elem = ET.SubElement(blkiotune, 'device')
            ET.SubElement(device_elem, 'path').text = device['path']

            # 设备权重
            if device.get('weight'):
                ET.SubElement(device_elem, 'weight').text = str(device['weight'])

            # 读吞吐量
            if device.get('read_bytes_sec'):
                ET.SubElement(device_elem, 'read_bytes_sec').text = str(device['read_bytes_sec'])

            # 写吞吐量
            if device.get('write_bytes_sec'):
                ET.SubElement(device_elem, 'write_bytes_sec').text = str(device['write_bytes_sec'])

            # 读 IOPS
            if device.get('read_iops_sec'):
                ET.SubElement(device_elem, 'read_iops_sec').text = str(device['read_iops_sec'])

            # 写 IOPS
            if device.get('write_iops_sec'):
                ET.SubElement(device_elem, 'write_iops_sec').text = str(device['write_iops_sec'])

    def _add_iothreads(self, config: dict) -> None:
        """添加 IO 线程配置.

        支持以下配置:
        - iothreads: IOThread 总数
        - iothreadids: 自定义 IOThread ID 列表
        - defaultiothread: 默认事件 loop 的 worker 线程边界
        """
        iothreads_config = config.get('iothreads_allocation', {})
        if not iothreads_config:
            return

        iothreads = iothreads_config.get('iothreads')

        # 如果没有设置 iothreads 且没有其他配置，不生成 XML
        if iothreads is None:
            iothreadids = iothreads_config.get('iothreadids', [])
            defaultiothread = iothreads_config.get('defaultiothread')
            if not iothreadids and not defaultiothread:
                return

        # 生成 iothreads 元素
        if iothreads and iothreads > 0:
            ET.SubElement(self.domain, 'iothreads').text = str(iothreads)

        # 生成 iothreadids 元素
        iothreadids = iothreads_config.get('iothreadids', [])
        if iothreadids:
            iothreadids_elem = ET.SubElement(self.domain, 'iothreadids')
            for iothread in iothreadids:
                if not iothread.get('id'):
                    continue

                iothread_attrs = {'id': str(iothread['id'])}

                # 线程池边界
                if iothread.get('thread_pool_min') is not None:
                    iothread_attrs['thread_pool_min'] = str(iothread['thread_pool_min'])
                if iothread.get('thread_pool_max') is not None:
                    iothread_attrs['thread_pool_max'] = str(iothread['thread_pool_max'])

                iothread_elem = ET.SubElement(iothreadids_elem, 'iothread', **iothread_attrs)

                # poll 子元素
                poll_max = iothread.get('poll_max')
                poll_grow = iothread.get('poll_grow')
                poll_shrink = iothread.get('poll_shrink')

                if poll_max is not None or poll_grow is not None or poll_shrink is not None:
                    poll_attrs = {}
                    if poll_max is not None:
                        poll_attrs['max'] = str(poll_max)
                    if poll_grow is not None:
                        poll_attrs['grow'] = str(poll_grow)
                    if poll_shrink is not None:
                        poll_attrs['shrink'] = str(poll_shrink)
                    ET.SubElement(iothread_elem, 'poll', **poll_attrs)

        # 生成 defaultiothread 元素
        defaultiothread = iothreads_config.get('defaultiothread')
        if defaultiothread:
            default_attrs = {}
            if defaultiothread.get('thread_pool_min') is not None:
                default_attrs['thread_pool_min'] = str(defaultiothread['thread_pool_min'])
            if defaultiothread.get('thread_pool_max') is not None:
                default_attrs['thread_pool_max'] = str(defaultiothread['thread_pool_max'])

            if default_attrs:
                ET.SubElement(self.domain, 'defaultiothread', **default_attrs)

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
        """添加安全配置.

        参考：https://www.libvirt.org/formatdomain.html#security-label

        支持三种类型:
        - none: <seclabel type='none'/>
        - dynamic: libvirt 自动生成标签，relabel 固定为 yes
        - static: 手动指定标签，relabel 默认为 no
        """
        security_config = config.get('security_label') or config.get('seclabel', {})
        if not security_config:
            return

        sec_type = security_config.get('type', 'dynamic')

        # none 类型：生成 <seclabel type='none'/>
        if sec_type == 'none':
            ET.SubElement(self.domain, 'seclabel', type='none')
            return
        attrs = {'type': sec_type}
        if security_config.get('model'):
            attrs['model'] = security_config['model']
        # relabel 属性：dynamic 类型默认为 yes，static 类型默认为 no
        relabel = security_config.get('relabel')
        if sec_type == 'dynamic':
            # dynamic 类型 relabel 默认为 yes (复选框返回 0/1)
            if relabel == 0 or relabel is False:
                attrs['relabel'] = 'no'
            else:
                attrs['relabel'] = 'yes'
        elif sec_type == 'static':
            # static 类型 relabel 默认为 no (复选框返回 0/1)
            if relabel == 1 or relabel is True:
                attrs['relabel'] = 'yes'
            else:
                attrs['relabel'] = 'no'

        seclabel = ET.SubElement(self.domain, 'seclabel', **attrs)

        # label: static 类型必需，dynamic 类型可选
        if security_config.get('label'):
            ET.SubElement(seclabel, 'label').text = security_config['label']
        # imagelabel: 输出only 元素，但也可以指定
        if security_config.get('imagelabel'):
            ET.SubElement(seclabel, 'imagelabel').text = security_config['imagelabel']
        # baselabel: dynamic 类型的基础标签
        baselabel_value = security_config.get('baselabel') or security_config.get('baselabel_value')
        if baselabel_value:
            ET.SubElement(seclabel, 'baselabel').text = baselabel_value

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
        """添加启动安全配置.

        支持 AMD SEV/SEV-SNP, Intel TDX, IBM s390-pv 四种类型。
        参考：https://www.libvirt.org/formatdomain.html#launch-security
        """
        launch_config = config.get('launch_security', {})
        if not launch_config:
            return

        sec_type = launch_config.get('type', 'sev')
        attrs = {'type': sec_type}

        # ========== 仅作为属性的配置 ==========
        # 内核哈希 (仅 SEV/SEV-SNP 直接内核引导时有效) - 这是属性
        if launch_config.get('kernel_hashes'):
            attrs['kernelHashes'] = 'yes'

        # ========== 类型特有属性 ==========
        # SEV-SNP 特有属性
        if sec_type == 'sev-snp':
            if launch_config.get('author_key'):
                attrs['authorKey'] = 'yes'
            if launch_config.get('vcek') is False:
                attrs['vcek'] = 'no'

        # 创建 launchSecurity 元素
        launch_security = ET.SubElement(self.domain, 'launchSecurity', **attrs)

        # ========== 通用子元素 (SEV/SEV-SNP/TDX) ==========
        # policy - Guest 策略 (十六进制字符串)
        policy = launch_config.get('policy')
        if policy:
            ET.SubElement(launch_security, 'policy').text = policy

        # C-bit 位置 (加密位在页表条目中的位置)
        # 支持两种字段名：cbitpos_enabled/cbitpos_value (新) 或 cbitpos (旧)
        cbitpos_enabled = launch_config.get('cbitpos_enabled')
        cbitpos_value = launch_config.get('cbitpos_value')
        # 兼容旧格式
        if not cbitpos_enabled and 'cbitpos' in launch_config:
            cbitpos_val = launch_config.get('cbitpos')
            if cbitpos_val is not None and cbitpos_val != '':
                cbitpos_enabled = True
                cbitpos_value = str(cbitpos_val)

        if cbitpos_enabled and cbitpos_value:
            ET.SubElement(launch_security, 'cbitpos').text = cbitpos_value

        # 物理地址位减少量
        # 支持两种字段名：reduced_phys_bits_enabled/reduced_phys_bits_value (新) 或 reduced_phys_bits (旧)
        reduced_phys_bits_enabled = launch_config.get('reduced_phys_bits_enabled')
        reduced_phys_bits_value = launch_config.get('reduced_phys_bits_value')
        # 兼容旧格式
        if not reduced_phys_bits_enabled and 'reduced_phys_bits' in launch_config:
            rpb_val = launch_config.get('reduced_phys_bits')
            if rpb_val is not None and rpb_val != '':
                reduced_phys_bits_enabled = True
                reduced_phys_bits_value = str(rpb_val)

        if reduced_phys_bits_enabled and reduced_phys_bits_value:
            ET.SubElement(launch_security, 'reducedPhysBits').text = reduced_phys_bits_value

        # ========== SEV 特有子元素 ==========
        if sec_type == 'sev':
            # dhCert - Diffie-Hellman 密钥 (Base64 编码)
            dh_cert = launch_config.get('dh_cert')
            if dh_cert:
                ET.SubElement(launch_security, 'dhCert').text = dh_cert

            # session - 会话数据 (Base64 编码)
            session = launch_config.get('session')
            if session:
                ET.SubElement(launch_security, 'session').text = session

        # ========== SEV-SNP 特有子元素 ==========
        if sec_type == 'sev-snp':
            # guestVisibleWorkarounds - 16 字节 Base64 编码
            guest_visible_workarounds = launch_config.get('guest_visible_workarounds')
            if guest_visible_workarounds:
                ET.SubElement(
                    launch_security, 'guestVisibleWorkarounds'
                ).text = guest_visible_workarounds

            # idBlock - 96 字节 Base64 编码
            id_block = launch_config.get('id_block')
            if id_block:
                ET.SubElement(launch_security, 'idBlock').text = id_block

            # idAuth - 4096 字节 Base64 编码
            id_auth = launch_config.get('id_auth')
            if id_auth:
                ET.SubElement(launch_security, 'idAuth').text = id_auth

            # hostData - 32 字节 Base64 编码
            host_data = launch_config.get('host_data')
            if host_data:
                ET.SubElement(launch_security, 'hostData').text = host_data

        # ========== Intel TDX 特有子元素 ==========
        if sec_type == 'tdx':
            # mrConfigId - SHA384 Base64 摘要
            mr_config_id = launch_config.get('mr_config_id')
            if mr_config_id:
                ET.SubElement(launch_security, 'mrConfigId').text = mr_config_id

            # mrOwner - SHA384 Base64 摘要
            mr_owner = launch_config.get('mr_owner')
            if mr_owner:
                ET.SubElement(launch_security, 'mrOwner').text = mr_owner

            # mrOwnerConfig - SHA384 Base64 摘要
            mr_owner_config = launch_config.get('mr_owner_config')
            if mr_owner_config:
                ET.SubElement(launch_security, 'mrOwnerConfig').text = mr_owner_config

            # quoteGenerationService - QGS 守护进程套接字路径
            quote_generation_service = launch_config.get('quote_generation_service')
            if quote_generation_service:
                qgs_elem = ET.SubElement(launch_security, 'quoteGenerationService')
                qgs_elem.set('path', quote_generation_service)

        # ========== s390-pv ==========
        # IBM s390-pv 不需要额外的子元素，只需要 type='s390-pv'

    def _add_key_wrap(self, config: dict) -> None:
        """添加密钥包装配置 (S390 Platform).

        参考：https://www.libvirt.org/formatdomain.html#key-wrap
        """
        key_wrap_config = config.get('key_wrap', {})
        if not key_wrap_config:
            return

        cipher_list = key_wrap_config.get('cipher', [])
        if not cipher_list:
            return

        # 创建 keywrap 元素
        keywrap = ET.SubElement(self.domain, 'keywrap')

        # 添加 cipher 子元素
        for cipher in cipher_list:
            if isinstance(cipher, dict):
                cipher_attrs = {
                    'name': cipher.get('name', 'aes'),
                    'state': cipher.get('state', 'on'),
                }
                ET.SubElement(keywrap, 'cipher', **cipher_attrs)

    def _add_perf(self, config: dict) -> None:
        """添加性能监控配置.

        参考：https://www.libvirt.org/formatdomain.html#perf
        """
        perf_config = config.get('performance_monitoring', {})
        if not perf_config or not perf_config.get('enabled'):
            return

        events = perf_config.get('events', {})
        if not events:
            return

        # 创建 perf 元素
        perf = ET.SubElement(self.domain, 'perf')

        # 添加启用的事件 (events 字典的值现在是 'yes' 或 'no')
        for event_name, enabled_value in events.items():
            ET.SubElement(perf, 'event', name=event_name, enabled=enabled_value)

    def _add_throttlegroups(self, config: dict) -> None:
        """添加节流组配置.

        参考：https://www.libvirt.org/formatdomain.html#throttle-groups
        """
        throttlegroups_config = config.get('throttlegroups', {})
        if not throttlegroups_config:
            return

        # 支持 throttlegroups 和 throttle_groups 两种键名
        groups_list = throttlegroups_config.get('throttlegroups', [])
        if not groups_list:
            groups_list = throttlegroups_config.get('throttle_groups', [])
        if not groups_list:
            return

        # 创建 throttlegroups 元素
        throttlegroups_elem = ET.SubElement(self.domain, 'throttlegroups')

        # 添加每个节流组
        for group in groups_list:
            if not isinstance(group, dict):
                continue

            group_name = group.get('name')
            if not group_name:
                continue

            group_elem = ET.SubElement(throttlegroups_elem, 'throttlegroup')

            # 组名称
            name_elem = ET.SubElement(group_elem, 'group_name')
            name_elem.text = group_name

            # 总字节/秒
            total_bytes = group.get('total_bytes_sec')
            if total_bytes is not None and total_bytes != '':
                tb_elem = ET.SubElement(group_elem, 'total_bytes_sec')
                tb_elem.text = str(total_bytes)

            # 读字节/秒
            read_bytes = group.get('read_bytes_sec')
            if read_bytes is not None and read_bytes != '':
                rb_elem = ET.SubElement(group_elem, 'read_bytes_sec')
                rb_elem.text = str(read_bytes)

            # 写字节/秒
            write_bytes = group.get('write_bytes_sec')
            if write_bytes is not None and write_bytes != '':
                wb_elem = ET.SubElement(group_elem, 'write_bytes_sec')
                wb_elem.text = str(write_bytes)

            # 总 IOPS
            total_iops = group.get('total_iops_sec')
            if total_iops is not None and total_iops != '':
                ti_elem = ET.SubElement(group_elem, 'total_iops_sec')
                ti_elem.text = str(total_iops)

            # 读 IOPS
            read_iops = group.get('read_iops_sec')
            if read_iops is not None and read_iops != '':
                ri_elem = ET.SubElement(group_elem, 'read_iops_sec')
                ri_elem.text = str(read_iops)

            # 写 IOPS
            write_iops = group.get('write_iops_sec')
            if write_iops is not None and write_iops != '':
                wi_elem = ET.SubElement(group_elem, 'write_iops_sec')
                wi_elem.text = str(write_iops)

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
