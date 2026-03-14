"""Module 2: OS & Boot - Firmware, bootloader, kernel boot, container boot, and common OS configuration."""

from tkinter import filedialog

import customtkinter as ctk

from ..styles import CTK_FONT_MAIN, CTK_FONT_SMALL


class OSBootModule(ctk.CTkFrame):
    """OS & Boot Module."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent')
        self.on_change_callback = on_change_callback

        # Create Tab view
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=0, column=0, sticky='nsew')
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Add sub-tabs
        self.common_tab = self.tabview.add('OS type')
        self.guest_firmware_tab = self.tabview.add('Guest firmware')
        self.direct_kernel_tab = self.tabview.add('Direct kernel boot')
        self.host_bootloader_tab = self.tabview.add('Host bootloader')
        self.container_boot_tab = self.tabview.add('Container boot')
        self.advanced_tab = self.tabview.add('Advanced')

        # Initialize UI
        self._init_common_tab()
        self._init_guest_firmware_tab()
        self._init_direct_kernel_tab()
        self._init_host_bootloader_tab()
        self._init_container_boot_tab()
        self._init_advanced_tab()

    def _init_common_tab(self):
        """Initialize Common OS type tab."""
        self.common_tab.grid_columnconfigure(0, weight=1)
        self.common_tab.grid_columnconfigure(1, weight=1)

        # OS Type
        ctk.CTkLabel(
            self.common_tab, text='OS Type:', font=CTK_FONT_MAIN, width=120, anchor='w'
        ).grid(row=0, column=0, padx=10, pady=8, sticky='w')
        self.os_type = ctk.CTkOptionMenu(
            self.common_tab,
            values=['hvm', 'linux', 'windows', 'xen', 'exe'],
            width=200,
            font=CTK_FONT_SMALL,
            command=self._trigger_change,
        )
        self.os_type.set('hvm')
        self.os_type.grid(row=0, column=1, padx=10, pady=8, sticky='w')

        # Architecture
        ctk.CTkLabel(
            self.common_tab, text='Architecture:', font=CTK_FONT_MAIN, width=120, anchor='w'
        ).grid(row=1, column=0, padx=10, pady=8, sticky='w')
        self.arch = ctk.CTkOptionMenu(
            self.common_tab,
            values=['x86_64', 'aarch64', 'i686', 'armv7l', 'ppc64', 'ppc64le', 's390x'],
            width=200,
            font=CTK_FONT_SMALL,
            command=self._trigger_change,
        )
        self.arch.set('x86_64')
        self.arch.grid(row=1, column=1, padx=10, pady=8, sticky='w')

        # Machine Type
        ctk.CTkLabel(
            self.common_tab, text='Machine:', font=CTK_FONT_MAIN, width=120, anchor='w'
        ).grid(row=2, column=0, padx=10, pady=8, sticky='w')
        self.machine_type = ctk.CTkOptionMenu(
            self.common_tab,
            values=['q35', 'pc', 'pc-i440fx-8.0', 'pc-q35-8.0', 'virt', 'virt-9.0'],
            width=200,
            font=CTK_FONT_SMALL,
            command=self._trigger_change,
        )
        self.machine_type.set('q35')
        self.machine_type.grid(row=2, column=1, padx=10, pady=8, sticky='w')

    def _init_guest_firmware_tab(self):
        """Initialize Guest firmware tab."""
        self.guest_firmware_tab.grid_columnconfigure(0, weight=1)
        self.guest_firmware_tab.grid_columnconfigure(1, weight=1)

        # Firmware Type (auto-selection)
        ctk.CTkLabel(
            self.guest_firmware_tab, text='Firmware:', font=CTK_FONT_MAIN, width=120, anchor='w'
        ).grid(row=0, column=0, padx=10, pady=8, sticky='w')
        self.firmware_type = ctk.CTkSegmentedButton(
            self.guest_firmware_tab, values=['BIOS', 'UEFI', 'auto'], font=CTK_FONT_SMALL
        )
        self.firmware_type.set('auto')
        self.firmware_type.grid(row=0, column=1, padx=10, pady=8, sticky='w')
        self.firmware_type.configure(command=self._trigger_change)

        # Loader Path (for manual UEFI)
        ctk.CTkLabel(
            self.guest_firmware_tab, text='Loader Path:', font=CTK_FONT_MAIN, width=120, anchor='w'
        ).grid(row=1, column=0, padx=10, pady=8, sticky='w')
        loader_frame = ctk.CTkFrame(self.guest_firmware_tab, fg_color='transparent')
        loader_frame.grid(row=1, column=1, padx=10, pady=8, sticky='w')
        loader_frame.grid_columnconfigure(0, weight=1)
        self.loader_entry = ctk.CTkEntry(
            loader_frame, placeholder_text='/usr/share/OVMF/OVMF_CODE.fd', width=300
        )
        self.loader_entry.grid(row=0, column=0, padx=(0, 5), sticky='w')
        self.loader_entry.bind('<KeyRelease>', lambda e: self._trigger_change())
        ctk.CTkButton(
            loader_frame, text='Browse', width=60, font=CTK_FONT_SMALL, command=self._browse_loader
        ).grid(row=0, column=1, sticky='w')

        # NVRAM Path (for manual UEFI)
        ctk.CTkLabel(
            self.guest_firmware_tab, text='NVRAM Path:', font=CTK_FONT_MAIN, width=120, anchor='w'
        ).grid(row=2, column=0, padx=10, pady=8, sticky='w')
        nvram_frame = ctk.CTkFrame(self.guest_firmware_tab, fg_color='transparent')
        nvram_frame.grid(row=2, column=1, padx=10, pady=8, sticky='w')
        nvram_frame.grid_columnconfigure(0, weight=1)
        self.nvram_entry = ctk.CTkEntry(
            nvram_frame, placeholder_text='/var/lib/libvirt/nvram/guest_VARS.fd', width=300
        )
        self.nvram_entry.grid(row=0, column=0, padx=(0, 5), sticky='w')
        self.nvram_entry.bind('<KeyRelease>', lambda e: self._trigger_change())
        ctk.CTkButton(
            nvram_frame, text='Browse', width=60, font=CTK_FONT_SMALL, command=self._browse_nvram
        ).grid(row=0, column=1, sticky='w')

        # NVRAM Template
        ctk.CTkLabel(
            self.guest_firmware_tab, text='NVRAM Template:', font=CTK_FONT_MAIN, width=120, anchor='w'
        ).grid(row=3, column=0, padx=10, pady=8, sticky='w')
        nvram_tpl_frame = ctk.CTkFrame(self.guest_firmware_tab, fg_color='transparent')
        nvram_tpl_frame.grid(row=3, column=1, padx=10, pady=8, sticky='w')
        nvram_tpl_frame.grid_columnconfigure(0, weight=1)
        self.nvram_tpl_entry = ctk.CTkEntry(
            nvram_tpl_frame, placeholder_text='/usr/share/OVMF/OVMF_VARS.fd', width=300
        )
        self.nvram_tpl_entry.grid(row=0, column=0, padx=(0, 5), sticky='w')
        self.nvram_tpl_entry.bind('<KeyRelease>', lambda e: self._trigger_change())
        ctk.CTkButton(
            nvram_tpl_frame, text='Browse', width=60, font=CTK_FONT_SMALL, command=self._browse_nvram_tpl
        ).grid(row=0, column=1, sticky='w')

        # Loader Type
        ctk.CTkLabel(
            self.guest_firmware_tab, text='Loader Type:', font=CTK_FONT_MAIN, width=120, anchor='w'
        ).grid(row=4, column=0, padx=10, pady=8, sticky='w')
        self.loader_type = ctk.CTkOptionMenu(
            self.guest_firmware_tab,
            values=['pflash', 'rom'],
            width=100,
            font=CTK_FONT_SMALL,
            command=self._trigger_change,
        )
        self.loader_type.set('pflash')
        self.loader_type.grid(row=4, column=1, padx=10, pady=8, sticky='w')

        # Secure Boot
        ctk.CTkLabel(
            self.guest_firmware_tab, text='Secure Boot:', font=CTK_FONT_MAIN, width=120, anchor='w'
        ).grid(row=5, column=0, padx=10, pady=8, sticky='w')
        self.secure_boot_check = ctk.CTkCheckBox(
            self.guest_firmware_tab, text='Enable', font=CTK_FONT_SMALL
        )
        self.secure_boot_check.grid(row=5, column=1, padx=10, pady=8, sticky='w')
        self.secure_boot_check.configure(command=self._trigger_change)

        # Stateless (no NVRAM)
        ctk.CTkLabel(
            self.guest_firmware_tab, text='Stateless:', font=CTK_FONT_MAIN, width=120, anchor='w'
        ).grid(row=6, column=0, padx=10, pady=8, sticky='w')
        self.stateless_check = ctk.CTkCheckBox(
            self.guest_firmware_tab, text='Discard NVRAM on shutdown', font=CTK_FONT_SMALL
        )
        self.stateless_check.grid(row=6, column=1, padx=10, pady=8, sticky='w')
        self.stateless_check.configure(command=self._trigger_change)

    def _init_direct_kernel_tab(self):
        """Initialize Direct kernel boot tab."""
        self.direct_kernel_tab.grid_columnconfigure(0, weight=1)
        self.direct_kernel_tab.grid_columnconfigure(1, weight=1)

        # Kernel Path
        ctk.CTkLabel(
            self.direct_kernel_tab, text='Kernel Path:', font=CTK_FONT_MAIN, width=120, anchor='w'
        ).grid(row=0, column=0, padx=10, pady=8, sticky='w')
        kernel_frame = ctk.CTkFrame(self.direct_kernel_tab, fg_color='transparent')
        kernel_frame.grid(row=0, column=1, padx=10, pady=8, sticky='w')
        kernel_frame.grid_columnconfigure(0, weight=1)
        self.kernel_path_entry = ctk.CTkEntry(
            kernel_frame, placeholder_text='/boot/vmlinuz-...', width=300
        )
        self.kernel_path_entry.grid(row=0, column=0, padx=(0, 5), sticky='w')
        self.kernel_path_entry.bind('<KeyRelease>', lambda e: self._trigger_change())
        ctk.CTkButton(
            kernel_frame, text='Browse', width=60, font=CTK_FONT_SMALL, command=self._browse_kernel
        ).grid(row=0, column=1, sticky='w')

        # Initrd Path
        ctk.CTkLabel(
            self.direct_kernel_tab, text='Initrd Path:', font=CTK_FONT_MAIN, width=120, anchor='w'
        ).grid(row=1, column=0, padx=10, pady=8, sticky='w')
        initrd_frame = ctk.CTkFrame(self.direct_kernel_tab, fg_color='transparent')
        initrd_frame.grid(row=1, column=1, padx=10, pady=8, sticky='w')
        initrd_frame.grid_columnconfigure(0, weight=1)
        self.initrd_path_entry = ctk.CTkEntry(
            initrd_frame, placeholder_text='/boot/initrd.img-...', width=300
        )
        self.initrd_path_entry.grid(row=0, column=0, padx=(0, 5), sticky='w')
        self.initrd_path_entry.bind('<KeyRelease>', lambda e: self._trigger_change())
        ctk.CTkButton(
            initrd_frame, text='Browse', width=60, font=CTK_FONT_SMALL, command=self._browse_initrd
        ).grid(row=0, column=1, sticky='w')

        # Kernel Command Line
        ctk.CTkLabel(
            self.direct_kernel_tab, text='Kernel Cmdline:', font=CTK_FONT_MAIN, width=120, anchor='w'
        ).grid(row=2, column=0, padx=10, pady=8, sticky='w')
        self.cmdline_entry = ctk.CTkEntry(
            self.direct_kernel_tab, placeholder_text='root=/dev/sda1 quiet splash', width=400
        )
        self.cmdline_entry.grid(row=2, column=1, padx=10, pady=8, sticky='w')
        self.cmdline_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        # Shim (for secure boot chaining)
        ctk.CTkLabel(
            self.direct_kernel_tab, text='Shim:', font=CTK_FONT_MAIN, width=120, anchor='w'
        ).grid(row=3, column=0, padx=10, pady=8, sticky='w')
        shim_frame = ctk.CTkFrame(self.direct_kernel_tab, fg_color='transparent')
        shim_frame.grid(row=3, column=1, padx=10, pady=8, sticky='w')
        shim_frame.grid_columnconfigure(0, weight=1)
        self.shim_entry = ctk.CTkEntry(
            shim_frame, placeholder_text='/path/to/shim.efi', width=300
        )
        self.shim_entry.grid(row=0, column=0, padx=(0, 5), sticky='w')
        self.shim_entry.bind('<KeyRelease>', lambda e: self._trigger_change())
        ctk.CTkButton(
            shim_frame, text='Browse', width=60, font=CTK_FONT_SMALL, command=self._browse_shim
        ).grid(row=0, column=1, sticky='w')

        # DTB Path
        ctk.CTkLabel(
            self.direct_kernel_tab, text='DTB Path:', font=CTK_FONT_MAIN, width=120, anchor='w'
        ).grid(row=4, column=0, padx=10, pady=8, sticky='w')
        dtb_frame = ctk.CTkFrame(self.direct_kernel_tab, fg_color='transparent')
        dtb_frame.grid(row=4, column=1, padx=10, pady=8, sticky='w')
        dtb_frame.grid_columnconfigure(0, weight=1)
        self.dtb_path_entry = ctk.CTkEntry(
            dtb_frame, placeholder_text='/boot/dtb/...', width=300
        )
        self.dtb_path_entry.grid(row=0, column=0, padx=(0, 5), sticky='w')
        self.dtb_path_entry.bind('<KeyRelease>', lambda e: self._trigger_change())
        ctk.CTkButton(
            dtb_frame, text='Browse', width=60, font=CTK_FONT_SMALL, command=self._browse_dtb
        ).grid(row=0, column=1, sticky='w')

    def _init_host_bootloader_tab(self):
        """Initialize Host bootloader tab."""
        self.host_bootloader_tab.grid_columnconfigure(0, weight=1)
        self.host_bootloader_tab.grid_columnconfigure(1, weight=1)

        # Bootloader Path
        ctk.CTkLabel(
            self.host_bootloader_tab, text='Bootloader:', font=CTK_FONT_MAIN, width=120, anchor='w'
        ).grid(row=0, column=0, padx=10, pady=8, sticky='w')
        bootloader_frame = ctk.CTkFrame(self.host_bootloader_tab, fg_color='transparent')
        bootloader_frame.grid(row=0, column=1, padx=10, pady=8, sticky='w')
        bootloader_frame.grid_columnconfigure(0, weight=1)
        self.bootloader_entry = ctk.CTkEntry(
            bootloader_frame, placeholder_text='/usr/bin/pygrub', width=300
        )
        self.bootloader_entry.grid(row=0, column=0, padx=(0, 5), sticky='w')
        self.bootloader_entry.bind('<KeyRelease>', lambda e: self._trigger_change())
        ctk.CTkButton(
            bootloader_frame, text='Browse', width=60, font=CTK_FONT_SMALL, command=self._browse_bootloader
        ).grid(row=0, column=1, sticky='w')

        # Bootloader Args
        ctk.CTkLabel(
            self.host_bootloader_tab, text='Bootloader Args:', font=CTK_FONT_MAIN, width=120, anchor='w'
        ).grid(row=1, column=0, padx=10, pady=8, sticky='w')
        self.bootloader_args_entry = ctk.CTkEntry(
            self.host_bootloader_tab, placeholder_text='--append single', width=400
        )
        self.bootloader_args_entry.grid(row=1, column=1, padx=10, pady=8, sticky='w')
        self.bootloader_args_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

    def _init_container_boot_tab(self):
        """Initialize Container boot tab."""
        self.container_boot_tab.grid_columnconfigure(0, weight=1)
        self.container_boot_tab.grid_columnconfigure(1, weight=1)

        # Init (path to init binary)
        ctk.CTkLabel(
            self.container_boot_tab, text='Init:', font=CTK_FONT_MAIN, width=120, anchor='w'
        ).grid(row=0, column=0, padx=10, pady=8, sticky='w')
        self.init_entry = ctk.CTkEntry(
            self.container_boot_tab, placeholder_text='/bin/systemd', width=300
        )
        self.init_entry.grid(row=0, column=1, padx=10, pady=8, sticky='w')
        self.init_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        # Init Args (multi-value)
        ctk.CTkLabel(
            self.container_boot_tab, text='Init Args:', font=CTK_FONT_MAIN, width=120, anchor='w'
        ).grid(row=1, column=0, padx=10, pady=8, sticky='w')
        self.init_args_entry = ctk.CTkEntry(
            self.container_boot_tab, placeholder_text='--unit emergency.service (comma separated)', width=300
        )
        self.init_args_entry.grid(row=1, column=1, padx=10, pady=8, sticky='w')
        self.init_args_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        # Init Env
        ctk.CTkLabel(
            self.container_boot_tab, text='Init Env:', font=CTK_FONT_MAIN, width=120, anchor='w'
        ).grid(row=2, column=0, padx=10, pady=8, sticky='w')
        self.init_env_entry = ctk.CTkEntry(
            self.container_boot_tab, placeholder_text='MYENV=some value (comma separated)', width=300
        )
        self.init_env_entry.grid(row=2, column=1, padx=10, pady=8, sticky='w')
        self.init_env_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        # Init Dir
        ctk.CTkLabel(
            self.container_boot_tab, text='Init Dir:', font=CTK_FONT_MAIN, width=120, anchor='w'
        ).grid(row=3, column=0, padx=10, pady=8, sticky='w')
        self.init_dir_entry = ctk.CTkEntry(
            self.container_boot_tab, placeholder_text='/my/custom/cwd', width=300
        )
        self.init_dir_entry.grid(row=3, column=1, padx=10, pady=8, sticky='w')
        self.init_dir_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        # Init User
        ctk.CTkLabel(
            self.container_boot_tab, text='Init User:', font=CTK_FONT_MAIN, width=120, anchor='w'
        ).grid(row=4, column=0, padx=10, pady=8, sticky='w')
        self.init_user_entry = ctk.CTkEntry(
            self.container_boot_tab, placeholder_text='tester or 1000', width=200
        )
        self.init_user_entry.grid(row=4, column=1, padx=10, pady=8, sticky='w')
        self.init_user_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        # Init Group
        ctk.CTkLabel(
            self.container_boot_tab, text='Init Group:', font=CTK_FONT_MAIN, width=120, anchor='w'
        ).grid(row=5, column=0, padx=10, pady=8, sticky='w')
        self.init_group_entry = ctk.CTkEntry(
            self.container_boot_tab, placeholder_text='users or 1000', width=200
        )
        self.init_group_entry.grid(row=5, column=1, padx=10, pady=8, sticky='w')
        self.init_group_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

    def _init_advanced_tab(self):
        """Initialize Advanced tab."""
        self.advanced_tab.grid_columnconfigure(0, weight=1)
        self.advanced_tab.grid_columnconfigure(1, weight=1)

        # Boot Order
        ctk.CTkLabel(
            self.advanced_tab, text='Boot Order:', font=CTK_FONT_MAIN, width=120, anchor='w'
        ).grid(row=0, column=0, padx=10, pady=8, sticky='w')
        boot_frame = ctk.CTkFrame(self.advanced_tab, fg_color='transparent')
        boot_frame.grid(row=0, column=1, padx=10, pady=8, sticky='w')

        self.boot_order_entries = []
        for i in range(4):
            entry = ctk.CTkEntry(boot_frame, width=100, font=CTK_FONT_SMALL, placeholder_text='hd/cdrom/floppy/network')
            entry.grid(row=0, column=i, padx=2, sticky='w')
            entry.bind('<KeyRelease>', lambda e: self._trigger_change())
            self.boot_order_entries.append(entry)
        # Set default values
        self.boot_order_entries[0].insert(0, 'hd')
        self.boot_order_entries[1].insert(0, 'cdrom')

        # Boot Menu
        ctk.CTkLabel(
            self.advanced_tab, text='Boot Menu:', font=CTK_FONT_MAIN, width=120, anchor='w'
        ).grid(row=1, column=0, padx=10, pady=8, sticky='w')
        self.boot_menu_check = ctk.CTkCheckBox(
            self.advanced_tab, text='Enable boot menu', font=CTK_FONT_SMALL
        )
        self.boot_menu_check.grid(row=1, column=1, padx=10, pady=8, sticky='w')
        self.boot_menu_check.configure(command=self._trigger_change)

        # Boot Timeout
        ctk.CTkLabel(
            self.advanced_tab, text='Boot Timeout (ms):', font=CTK_FONT_MAIN, width=120, anchor='w'
        ).grid(row=2, column=0, padx=10, pady=8, sticky='w')
        self.boot_timeout_entry = ctk.CTkEntry(self.advanced_tab, width=100, font=CTK_FONT_SMALL)
        self.boot_timeout_entry.grid(row=2, column=1, padx=10, pady=8, sticky='w')
        self.boot_timeout_entry.insert(0, '3000')
        self.boot_timeout_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        # SMBIOS Mode
        ctk.CTkLabel(
            self.advanced_tab, text='SMBIOS Mode:', font=CTK_FONT_MAIN, width=120, anchor='w'
        ).grid(row=3, column=0, padx=10, pady=8, sticky='w')
        self.smbios_mode = ctk.CTkOptionMenu(
            self.advanced_tab,
            values=['emulate', 'host', 'sysinfo'],
            width=150,
            font=CTK_FONT_SMALL,
            command=self._trigger_change,
        )
        self.smbios_mode.set('emulate')
        self.smbios_mode.grid(row=3, column=1, padx=10, pady=8, sticky='w')

        # BIOS useserial
        ctk.CTkLabel(
            self.advanced_tab, text='BIOS Serial:', font=CTK_FONT_MAIN, width=120, anchor='w'
        ).grid(row=4, column=0, padx=10, pady=8, sticky='w')
        self.bios_useserial_check = ctk.CTkCheckBox(
            self.advanced_tab, text='Use serial for BIOS messages', font=CTK_FONT_SMALL
        )
        self.bios_useserial_check.grid(row=4, column=1, padx=10, pady=8, sticky='w')
        self.bios_useserial_check.configure(command=self._trigger_change)

        # BIOS reboot timeout
        ctk.CTkLabel(
            self.advanced_tab, text='BIOS Reboot Timeout (ms):', font=CTK_FONT_MAIN, width=120, anchor='w'
        ).grid(row=5, column=0, padx=10, pady=8, sticky='w')
        self.bios_reboot_timeout_entry = ctk.CTkEntry(self.advanced_tab, width=100, font=CTK_FONT_SMALL)
        self.bios_reboot_timeout_entry.grid(row=5, column=1, padx=10, pady=8, sticky='w')
        self.bios_reboot_timeout_entry.insert(0, '-1')
        self.bios_reboot_timeout_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        # ACPI Tables
        ctk.CTkLabel(
            self.advanced_tab, text='ACPI Tables:', font=CTK_FONT_MAIN, width=120, anchor='w'
        ).grid(row=6, column=0, padx=10, pady=8, sticky='w')
        self.acpi_tables_entry = ctk.CTkEntry(
            self.advanced_tab, placeholder_text='type:path (comma separated)', width=400
        )
        self.acpi_tables_entry.grid(row=6, column=1, padx=10, pady=8, sticky='w')
        self.acpi_tables_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        # ID Mapping (for containers)
        ctk.CTkLabel(
            self.advanced_tab, text='ID Mapping:', font=CTK_FONT_MAIN, width=120, anchor='w'
        ).grid(row=7, column=0, padx=10, pady=8, sticky='w')
        idmap_frame = ctk.CTkFrame(self.advanced_tab, fg_color='transparent')
        idmap_frame.grid(row=7, column=1, padx=10, pady=8, sticky='w')
        idmap_frame.grid_columnconfigure(0, weight=1)
        idmap_frame.grid_columnconfigure(1, weight=1)
        idmap_frame.grid_columnconfigure(2, weight=1)

        ctk.CTkLabel(idmap_frame, text='UID:', font=CTK_FONT_SMALL).grid(row=0, column=0, padx=2, sticky='w')
        self.idmap_uid_start = ctk.CTkEntry(idmap_frame, width=60, font=CTK_FONT_SMALL, placeholder_text='start')
        self.idmap_uid_start.grid(row=1, column=0, padx=2, sticky='w')
        self.idmap_uid_start.insert(0, '0')
        self.idmap_uid_target = ctk.CTkEntry(idmap_frame, width=60, font=CTK_FONT_SMALL, placeholder_text='target')
        self.idmap_uid_target.grid(row=1, column=1, padx=2, sticky='w')
        self.idmap_uid_target.insert(0, '1000')
        self.idmap_uid_count = ctk.CTkEntry(idmap_frame, width=60, font=CTK_FONT_SMALL, placeholder_text='count')
        self.idmap_uid_count.grid(row=1, column=2, padx=2, sticky='w')
        self.idmap_uid_count.insert(0, '10')

        ctk.CTkLabel(idmap_frame, text='GID:', font=CTK_FONT_SMALL).grid(row=2, column=0, padx=2, sticky='w')
        self.idmap_gid_start = ctk.CTkEntry(idmap_frame, width=60, font=CTK_FONT_SMALL, placeholder_text='start')
        self.idmap_gid_start.grid(row=3, column=0, padx=2, sticky='w')
        self.idmap_gid_start.insert(0, '0')
        self.idmap_gid_target = ctk.CTkEntry(idmap_frame, width=60, font=CTK_FONT_SMALL, placeholder_text='target')
        self.idmap_gid_target.grid(row=3, column=1, padx=2, sticky='w')
        self.idmap_gid_target.insert(0, '1000')
        self.idmap_gid_count = ctk.CTkEntry(idmap_frame, width=60, font=CTK_FONT_SMALL, placeholder_text='count')
        self.idmap_gid_count.grid(row=3, column=2, padx=2, sticky='w')
        self.idmap_gid_count.insert(0, '10')

        for entry in [self.idmap_uid_start, self.idmap_uid_target, self.idmap_uid_count,
                      self.idmap_gid_start, self.idmap_gid_target, self.idmap_gid_count]:
            entry.bind('<KeyRelease>', lambda e: self._trigger_change())

    # ========== File Browser Callbacks ==========
    def _browse_loader(self):
        """Browse loader firmware file."""
        file_path = filedialog.askopenfilename(
            title='Select Loader Firmware File',
            filetypes=[('All Files', '*.*')],
        )
        if file_path:
            self.loader_entry.delete(0, ctk.END)
            self.loader_entry.insert(0, file_path)
            self._trigger_change()

    def _browse_nvram(self):
        """Browse NVRAM file."""
        file_path = filedialog.askopenfilename(
            title='Select NVRAM File',
            filetypes=[('All Files', '*.*')],
        )
        if file_path:
            self.nvram_entry.delete(0, ctk.END)
            self.nvram_entry.insert(0, file_path)
            self._trigger_change()

    def _browse_nvram_tpl(self):
        """Browse NVRAM template file."""
        file_path = filedialog.askopenfilename(
            title='Select NVRAM Template File',
            filetypes=[('All Files', '*.*')],
        )
        if file_path:
            self.nvram_tpl_entry.delete(0, ctk.END)
            self.nvram_tpl_entry.insert(0, file_path)
            self._trigger_change()

    def _browse_bootloader(self):
        """Browse bootloader file."""
        file_path = filedialog.askopenfilename(
            title='Select Bootloader File',
            filetypes=[('All Files', '*.*')],
        )
        if file_path:
            self.bootloader_entry.delete(0, ctk.END)
            self.bootloader_entry.insert(0, file_path)
            self._trigger_change()

    def _browse_kernel(self):
        """Browse kernel file."""
        file_path = filedialog.askopenfilename(
            title='Select Kernel File',
            filetypes=[('All Files', '*.*')],
        )
        if file_path:
            self.kernel_path_entry.delete(0, ctk.END)
            self.kernel_path_entry.insert(0, file_path)
            self._trigger_change()

    def _browse_initrd(self):
        """Browse initrd file."""
        file_path = filedialog.askopenfilename(
            title='Select Initrd File',
            filetypes=[('All Files', '*.*')],
        )
        if file_path:
            self.initrd_path_entry.delete(0, ctk.END)
            self.initrd_path_entry.insert(0, file_path)
            self._trigger_change()

    def _browse_shim(self):
        """Browse shim file."""
        file_path = filedialog.askopenfilename(
            title='Select Shim File',
            filetypes=[('All Files', '*.*')],
        )
        if file_path:
            self.shim_entry.delete(0, ctk.END)
            self.shim_entry.insert(0, file_path)
            self._trigger_change()

    def _browse_dtb(self):
        """Browse DTB file."""
        file_path = filedialog.askopenfilename(
            title='Select DTB File',
            filetypes=[('All Files', '*.*')],
        )
        if file_path:
            self.dtb_path_entry.delete(0, ctk.END)
            self.dtb_path_entry.insert(0, file_path)
            self._trigger_change()

    def _trigger_change(self, *args):
        """Trigger change callback."""
        if self.on_change_callback:
            self.on_change_callback()

    def get_config(self) -> dict:
        """Get configuration data."""
        boot_order = [e.get().strip() for e in self.boot_order_entries if e.get().strip()]

        # Parse ACPI tables
        acpi_tables = []
        acpi_text = self.acpi_tables_entry.get().strip()
        if acpi_text:
            for item in acpi_text.split(','):
                if ':' in item:
                    t_type, t_path = item.split(':', 1)
                    acpi_tables.append({'type': t_type.strip(), 'path': t_path.strip()})

        # Parse init args
        init_args = []
        init_args_text = self.init_args_entry.get().strip()
        if init_args_text:
            init_args = [a.strip() for a in init_args_text.split(',')]

        # Parse init env
        init_env = []
        init_env_text = self.init_env_entry.get().strip()
        if init_env_text:
            for item in init_env_text.split(','):
                if '=' in item:
                    name, value = item.split('=', 1)
                    init_env.append({'name': name.strip(), 'value': value.strip()})

        return {
            # Common OS type
            'os_type': self.os_type.get(),
            'arch': self.arch.get(),
            'machine': self.machine_type.get(),

            # Guest firmware
            'firmware': self.firmware_type.get().lower(),
            'loader_path': self.loader_entry.get().strip(),
            'loader_type': self.loader_type.get(),
            'loader_secure': self.secure_boot_check.get(),
            'loader_stateless': self.stateless_check.get(),
            'nvram_path': self.nvram_entry.get().strip(),
            'nvram_template': self.nvram_tpl_entry.get().strip(),

            # Direct kernel boot
            'kernel_path': self.kernel_path_entry.get().strip(),
            'initrd_path': self.initrd_path_entry.get().strip(),
            'cmdline': self.cmdline_entry.get().strip(),
            'shim_path': self.shim_entry.get().strip(),
            'dtb_path': self.dtb_path_entry.get().strip(),

            # Host bootloader
            'bootloader': self.bootloader_entry.get().strip(),
            'bootloader_args': self.bootloader_args_entry.get().strip(),

            # Container boot
            'container_init': self.init_entry.get().strip(),
            'container_initargs': init_args,
            'container_initenv': init_env,
            'container_initdir': self.init_dir_entry.get().strip(),
            'container_inituser': self.init_user_entry.get().strip(),
            'container_initgroup': self.init_group_entry.get().strip(),

            # Advanced
            'boot_order': boot_order,
            'boot_menu': self.boot_menu_check.get(),
            'boot_timeout': int(self.boot_timeout_entry.get().strip() or '3000'),
            'smbios_mode': self.smbios_mode.get(),
            'bios_useserial': self.bios_useserial_check.get(),
            'bios_reboot_timeout': int(self.bios_reboot_timeout_entry.get().strip() or '-1'),
            'acpi_tables': acpi_tables,
            'idmap_uid_start': int(self.idmap_uid_start.get().strip() or '0'),
            'idmap_uid_target': int(self.idmap_uid_target.get().strip() or '0'),
            'idmap_uid_count': int(self.idmap_uid_count.get().strip() or '0'),
            'idmap_gid_start': int(self.idmap_gid_start.get().strip() or '0'),
            'idmap_gid_target': int(self.idmap_gid_target.get().strip() or '0'),
            'idmap_gid_count': int(self.idmap_gid_count.get().strip() or '0'),
        }

    def to_xml(self) -> dict:
        """Generate XML configuration dictionary."""
        config = self.get_config()

        os_config = {
            'type': config['os_type'],
            'arch': config['arch'],
            'machine': config['machine'],
        }

        # Firmware configuration
        firmware = config['firmware']
        if firmware == 'auto':
            os_config['firmware'] = 'efi' if config['loader_path'] or config['nvram_path'] else 'bios'
        else:
            os_config['firmware'] = firmware

        # Loader configuration (for manual UEFI)
        if config['loader_path'] or firmware == 'uefi':
            loader = {
                'path': config['loader_path'],
                'type': config['loader_type'],
                'readonly': True,
            }
            if config['loader_secure']:
                loader['secure'] = True
            if config['loader_stateless']:
                loader['stateless'] = True
            os_config['loader'] = loader

        # NVRAM configuration
        if config['nvram_path'] or config['nvram_template']:
            nvram = {}
            if config['nvram_path']:
                nvram['path'] = config['nvram_path']
            if config['nvram_template']:
                nvram['template'] = config['nvram_template']
            os_config['nvram'] = nvram

        # Boot order
        if config['boot_order']:
            os_config['boot_devices'] = config['boot_order']

        # Boot menu
        if config['boot_menu']:
            os_config['bootmenu'] = {
                'enable': True,
                'timeout': config['boot_timeout'],
            }

        # SMBIOS
        if config['smbios_mode']:
            os_config['smbios'] = {'mode': config['smbios_mode']}

        # BIOS configuration
        if config['bios_useserial'] or config['bios_reboot_timeout'] != -1:
            bios = {}
            if config['bios_useserial']:
                bios['useserial'] = True
            if config['bios_reboot_timeout'] >= 0:
                bios['rebootTimeout'] = config['bios_reboot_timeout']
            os_config['bios'] = bios

        # Direct kernel boot configuration
        if config['kernel_path']:
            os_config['kernel'] = config['kernel_path']
        if config['initrd_path']:
            os_config['initrd'] = config['initrd_path']
        if config['cmdline']:
            os_config['cmdline'] = config['cmdline']
        if config['shim_path']:
            os_config['shim'] = config['shim_path']
        if config['dtb_path']:
            os_config['dtb'] = config['dtb_path']

        # Host bootloader configuration
        if config['bootloader']:
            os_config['bootloader'] = config['bootloader']
        if config['bootloader_args']:
            os_config['bootloader_args'] = config['bootloader_args']

        # Container boot configuration
        if config['container_init']:
            os_config['init'] = config['container_init']
        if config['container_initargs']:
            os_config['initargs'] = config['container_initargs']
        if config['container_initenv']:
            os_config['initenv'] = config['container_initenv']
        if config['container_initdir']:
            os_config['initdir'] = config['container_initdir']
        if config['container_inituser']:
            os_config['inituser'] = config['container_inituser']
        if config['container_initgroup']:
            os_config['initgroup'] = config['container_initgroup']

        # ID mapping
        if config['idmap_uid_count'] > 0 and config['idmap_gid_count'] > 0:
            os_config['idmap'] = {
                'uid': {
                    'start': config['idmap_uid_start'],
                    'target': config['idmap_uid_target'],
                    'count': config['idmap_uid_count'],
                },
                'gid': {
                    'start': config['idmap_gid_start'],
                    'target': config['idmap_gid_target'],
                    'count': config['idmap_gid_count'],
                },
            }

        # ACPI tables
        if config['acpi_tables']:
            os_config['acpi'] = {'tables': config['acpi_tables']}

        return {'os_booting': os_config}

    def load_config(self, config: dict):
        """Load configuration data into UI."""
        # Common OS type
        if 'type' in config:
            self.os_type.set(config['type'])
        if 'arch' in config:
            self.arch.set(config['arch'])
        if 'machine' in config:
            self.machine_type.set(config['machine'])

        # Guest firmware
        if 'firmware' in config:
            fw = config['firmware']
            if fw in ['efi', 'uefi']:
                self.firmware_type.set('UEFI')
            elif fw == 'bios':
                self.firmware_type.set('BIOS')
            else:
                self.firmware_type.set('auto')
        if 'loader' in config:
            loader = config['loader']
            if isinstance(loader, dict):
                if 'path' in loader:
                    self.loader_entry.delete(0, ctk.END)
                    self.loader_entry.insert(0, loader['path'])
                if 'type' in loader:
                    self.loader_type.set(loader['type'])
                if loader.get('secure'):
                    self.secure_boot_check.select()
                if loader.get('stateless'):
                    self.stateless_check.select()
            else:
                self.loader_entry.delete(0, ctk.END)
                self.loader_entry.insert(0, loader)
        if 'nvram' in config:
            nvram = config['nvram']
            if isinstance(nvram, dict):
                if 'path' in nvram:
                    self.nvram_entry.delete(0, ctk.END)
                    self.nvram_entry.insert(0, nvram['path'])
                if 'template' in nvram:
                    self.nvram_tpl_entry.delete(0, ctk.END)
                    self.nvram_tpl_entry.insert(0, nvram['template'])
            else:
                self.nvram_entry.delete(0, ctk.END)
                self.nvram_entry.insert(0, nvram)

        # Direct kernel boot
        if 'kernel' in config:
            self.kernel_path_entry.delete(0, ctk.END)
            self.kernel_path_entry.insert(0, config['kernel'])
        if 'initrd' in config:
            self.initrd_path_entry.delete(0, ctk.END)
            self.initrd_path_entry.insert(0, config['initrd'])
        if 'cmdline' in config:
            self.cmdline_entry.delete(0, ctk.END)
            self.cmdline_entry.insert(0, config['cmdline'])
        if 'shim' in config:
            self.shim_entry.delete(0, ctk.END)
            self.shim_entry.insert(0, config['shim'])
        if 'dtb' in config:
            self.dtb_path_entry.delete(0, ctk.END)
            self.dtb_path_entry.insert(0, config['dtb'])

        # Host bootloader
        if 'bootloader' in config:
            self.bootloader_entry.delete(0, ctk.END)
            self.bootloader_entry.insert(0, config['bootloader'])
        if 'bootloader_args' in config:
            self.bootloader_args_entry.delete(0, ctk.END)
            self.bootloader_args_entry.insert(0, config['bootloader_args'])

        # Container boot
        if 'init' in config:
            self.init_entry.delete(0, ctk.END)
            self.init_entry.insert(0, config['init'])
        if 'initargs' in config:
            self.init_args_entry.delete(0, ctk.END)
            self.init_args_entry.insert(0, ', '.join(config['initargs']))
        if 'initenv' in config:
            env_strs = [f"{e.get('name', '')}={e.get('value', '')}" for e in config['initenv']]
            self.init_env_entry.delete(0, ctk.END)
            self.init_env_entry.insert(0, ', '.join(env_strs))
        if 'initdir' in config:
            self.init_dir_entry.delete(0, ctk.END)
            self.init_dir_entry.insert(0, config['initdir'])
        if 'inituser' in config:
            self.init_user_entry.delete(0, ctk.END)
            self.init_user_entry.insert(0, config['inituser'])
        if 'initgroup' in config:
            self.init_group_entry.delete(0, ctk.END)
            self.init_group_entry.insert(0, config['initgroup'])

        # Advanced
        if 'boot_devices' in config:
            for i, device in enumerate(config['boot_devices'][:4]):
                if i < len(self.boot_order_entries):
                    self.boot_order_entries[i].delete(0, ctk.END)
                    self.boot_order_entries[i].insert(0, device)
        if 'bootmenu' in config:
            bootmenu = config['bootmenu']
            if isinstance(bootmenu, dict) and bootmenu.get('enable'):
                self.boot_menu_check.select()
                if 'timeout' in bootmenu:
                    self.boot_timeout_entry.delete(0, ctk.END)
                    self.boot_timeout_entry.insert(0, str(bootmenu['timeout']))
        if 'smbios' in config:
            smbios = config['smbios']
            if isinstance(smbios, dict) and 'mode' in smbios:
                self.smbios_mode.set(smbios['mode'])
        if 'bios' in config:
            bios = config['bios']
            if isinstance(bios, dict):
                if bios.get('useserial'):
                    self.bios_useserial_check.select()
                if 'rebootTimeout' in bios:
                    self.bios_reboot_timeout_entry.delete(0, ctk.END)
                    self.bios_reboot_timeout_entry.insert(0, str(bios['rebootTimeout']))
        if 'acpi' in config:
            acpi = config['acpi']
            if isinstance(acpi, dict) and 'tables' in acpi:
                table_strs = [f"{t.get('type', '')}:{t.get('path', '')}" for t in acpi['tables']]
                self.acpi_tables_entry.delete(0, ctk.END)
                self.acpi_tables_entry.insert(0, ', '.join(table_strs))
        if 'idmap' in config:
            idmap = config['idmap']
            if isinstance(idmap, dict):
                if 'uid' in idmap:
                    uid = idmap['uid']
                    self.idmap_uid_start.delete(0, ctk.END)
                    self.idmap_uid_start.insert(0, str(uid.get('start', 0)))
                    self.idmap_uid_target.delete(0, ctk.END)
                    self.idmap_uid_target.insert(0, str(uid.get('target', 0)))
                    self.idmap_uid_count.delete(0, ctk.END)
                    self.idmap_uid_count.insert(0, str(uid.get('count', 0)))
                if 'gid' in idmap:
                    gid = idmap['gid']
                    self.idmap_gid_start.delete(0, ctk.END)
                    self.idmap_gid_start.insert(0, str(gid.get('start', 0)))
                    self.idmap_gid_target.delete(0, ctk.END)
                    self.idmap_gid_target.insert(0, str(gid.get('target', 0)))
                    self.idmap_gid_count.delete(0, ctk.END)
                    self.idmap_gid_count.insert(0, str(gid.get('count', 0)))
