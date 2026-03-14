"""设备模块 - 合并存储设备、网络接口和其他设备配置."""

import uuid

from tkinter import filedialog

import customtkinter as ctk

from ..styles import BG_COLOR_CONTENT, CTK_FONT_MAIN, CTK_FONT_SMALL


class CombinedDevicesModule(ctk.CTkFrame):
    """设备模块 - 统一管理存储、网络和其他设备配置."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="transparent")
        self.on_change_callback = on_change_callback

        # 创建 Tab 视图
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=0, column=0, sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 添加子 Tab - 合并存储、网络、其他设备
        self.storage_tab = self.tabview.add("磁盘设备")
        self.network_tab = self.tabview.add("网络接口")
        self.graphics_tab = self.tabview.add("图形显示")
        self.video_tab = self.tabview.add("视频设备")
        self.usb_serial_tab = self.tabview.add("USB/串口")
        self.input_sound_tab = self.tabview.add("输入/声音")

        # 存储设备
        self.disks = []
        self._disk_counter = 0

        # 网络接口
        self.interfaces = []
        self._iface_counter = 0

        # 初始化 UI
        self._init_storage_tab()
        self._init_network_tab()
        self._init_graphics_tab()
        self._init_video_tab()
        self._init_usb_serial_tab()
        self._init_input_sound_tab()

    # ========== 磁盘设备 Tab ==========
    def _init_storage_tab(self):
        """初始化磁盘设备 Tab."""
        self.storage_tab.grid_columnconfigure(0, weight=1)

        # 标题
        ctk.CTkLabel(
            self.storage_tab,
            text="已配置的磁盘设备:",
            font=CTK_FONT_MAIN,
            text_color="#64b5f6"
        ).grid(row=0, column=0, padx=10, pady=8, sticky="w")

        # 磁盘列表容器
        self.disks_container = ctk.CTkScrollableFrame(
            self.storage_tab, fg_color=BG_COLOR_CONTENT, corner_radius=6
        )
        self.disks_container.grid(row=1, column=0, padx=10, pady=8, sticky="nsew")
        self.disks_container.grid_columnconfigure(0, weight=1)
        self.storage_tab.grid_rowconfigure(1, weight=1)

        # 添加默认磁盘
        self._add_disk()

        # 添加磁盘表单区域
        self._create_add_disk_form()

    def _create_add_disk_form(self):
        """创建添加磁盘表单."""
        form_frame = ctk.CTkFrame(self.storage_tab, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        form_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        form_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            form_frame, text="添加新磁盘", font=CTK_FONT_MAIN, text_color="#64b5f6"
        ).grid(row=0, column=0, columnspan=4, padx=10, pady=5, sticky="w")

        # 类型
        ctk.CTkLabel(form_frame, text="类型:", font=CTK_FONT_SMALL, width=50, anchor="w").grid(
            row=1, column=0, padx=5, pady=2, sticky="w"
        )
        self.new_disk_type = ctk.CTkOptionMenu(
            form_frame, values=["file", "block", "network"], width=100, font=CTK_FONT_SMALL
        )
        self.new_disk_type.set("file")
        self.new_disk_type.grid(row=1, column=1, padx=5, pady=2, sticky="w")

        # 格式
        ctk.CTkLabel(form_frame, text="格式:", font=CTK_FONT_SMALL, width=50, anchor="w").grid(
            row=1, column=2, padx=5, pady=2, sticky="w"
        )
        self.new_disk_format = ctk.CTkOptionMenu(
            form_frame, values=["raw", "qcow2", "qed", "vdi", "vmdk", "vpc"], width=80, font=CTK_FONT_SMALL
        )
        self.new_disk_format.set("raw")
        self.new_disk_format.grid(row=1, column=3, padx=5, pady=2, sticky="w")

        # 路径
        ctk.CTkLabel(form_frame, text="路径:", font=CTK_FONT_SMALL, width=50, anchor="w").grid(
            row=2, column=0, padx=5, pady=2, sticky="w"
        )
        path_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        path_frame.grid(row=2, column=1, columnspan=2, padx=5, pady=2, sticky="ew")
        path_frame.grid_columnconfigure(0, weight=1)
        self.new_disk_path = ctk.CTkEntry(path_frame, placeholder_text="/path/to/disk.img", font=CTK_FONT_SMALL)
        self.new_disk_path.grid(row=0, column=0, padx=(0, 5), sticky="ew")
        ctk.CTkButton(
            path_frame, text="浏览", width=50, font=CTK_FONT_SMALL,
            command=self._browse_disk_path
        ).grid(row=0, column=1, sticky="e")

        # 总线
        ctk.CTkLabel(form_frame, text="总线:", font=CTK_FONT_SMALL, width=50, anchor="w").grid(
            row=2, column=3, padx=5, pady=2, sticky="w"
        )
        self.new_disk_bus = ctk.CTkOptionMenu(
            form_frame, values=["virtio", "ide", "sata", "scsi", "usb"], width=80, font=CTK_FONT_SMALL
        )
        self.new_disk_bus.set("virtio")
        self.new_disk_bus.grid(row=2, column=4, padx=5, pady=2, sticky="w")

        # 设备类型
        ctk.CTkLabel(form_frame, text="设备:", font=CTK_FONT_SMALL, width=50, anchor="w").grid(
            row=3, column=0, padx=5, pady=2, sticky="w"
        )
        self.new_device_type = ctk.CTkOptionMenu(
            form_frame, values=["disk", "cdrom", "floppy", "lun"], width=100, font=CTK_FONT_SMALL
        )
        self.new_device_type.set("disk")
        self.new_device_type.grid(row=3, column=1, padx=5, pady=2, sticky="w")

        # 缓存
        ctk.CTkLabel(form_frame, text="缓存:", font=CTK_FONT_SMALL, width=50, anchor="w").grid(
            row=3, column=2, padx=5, pady=2, sticky="w"
        )
        self.new_cache_mode = ctk.CTkOptionMenu(
            form_frame, values=["none", "writeback", "writethrough", "directsync", "unsafe"],
            width=100, font=CTK_FONT_SMALL
        )
        self.new_cache_mode.set("none")
        self.new_cache_mode.grid(row=3, column=3, padx=5, pady=2, sticky="w")

        # 复选框
        check_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        check_frame.grid(row=4, column=0, columnspan=3, padx=5, pady=2, sticky="w")

        self.new_readonly = ctk.CTkCheckBox(check_frame, text="只读", font=CTK_FONT_SMALL)
        self.new_readonly.grid(row=0, column=0, padx=10, sticky="w")

        self.new_shareable = ctk.CTkCheckBox(check_frame, text="共享", font=CTK_FONT_SMALL)
        self.new_shareable.grid(row=0, column=1, padx=10, sticky="w")

        self.new_discard = ctk.CTkCheckBox(check_frame, text="TRIM", font=CTK_FONT_SMALL)
        self.new_discard.grid(row=0, column=2, padx=10, sticky="w")

        # 添加按钮
        ctk.CTkButton(
            form_frame,
            text="添加此磁盘",
            width=100,
            font=CTK_FONT_SMALL,
            fg_color="#4caf50",
            hover_color="#388e3c",
            command=self._add_disk_from_form,
        ).grid(row=4, column=3, padx=5, pady=2, sticky="e")

    def _browse_disk_path(self):
        """浏览磁盘文件路径."""
        file_path = filedialog.askopenfilename(
            title="选择磁盘文件",
            filetypes=[("磁盘镜像", "*.img *.qcow2 *.raw *.vdi *.vmdk"), ("所有文件", "*.*")],
        )
        if file_path:
            self.new_disk_path.delete(0, ctk.END)
            self.new_disk_path.insert(0, file_path)

    def _add_disk_from_form(self):
        """从表单添加磁盘."""
        self._add_disk({
            "type": self.new_disk_type.get(),
            "format": self.new_disk_format.get(),
            "bus": self.new_disk_bus.get(),
            "device_type": self.new_device_type.get(),
            "path": self.new_disk_path.get().strip(),
            "cache": self.new_cache_mode.get(),
            "readonly": self.new_readonly.get(),
            "shareable": self.new_shareable.get(),
            "discard": self.new_discard.get(),
        })
        self._trigger_change()

    def _add_disk(self, config=None):
        """添加磁盘配置."""
        if config is None:
            config = {
                "type": "file",
                "format": "raw",
                "bus": "virtio",
                "device_type": "disk",
                "path": "",
                "cache": "none",
                "readonly": False,
                "shareable": False,
                "discard": False,
            }

        disk_id = self._disk_counter
        self._disk_counter += 1

        disk_frame = ctk.CTkFrame(self.disks_container, fg_color="transparent")
        disk_frame.grid(row=disk_id, column=0, padx=10, pady=10, sticky="ew")
        disk_frame.grid_columnconfigure(1, weight=1)

        # 标题
        ctk.CTkLabel(
            disk_frame, text=f"磁盘 {disk_id + 1}", font=CTK_FONT_MAIN, text_color="#64b5f6"
        ).grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky="w")

        # 类型和格式
        ctk.CTkLabel(disk_frame, text="类型:", font=CTK_FONT_SMALL, width=50, anchor="w").grid(
            row=1, column=0, padx=5, pady=2, sticky="w"
        )
        disk_type_combo = ctk.CTkOptionMenu(
            disk_frame, values=["file", "block", "network"], width=100, font=CTK_FONT_SMALL,
            command=lambda *args: self._trigger_change()
        )
        disk_type_combo.set(config["type"])
        disk_type_combo.grid(row=1, column=1, padx=5, pady=2, sticky="w")

        ctk.CTkLabel(disk_frame, text="格式:", font=CTK_FONT_SMALL, width=50, anchor="w").grid(
            row=1, column=2, padx=5, pady=2, sticky="w"
        )
        disk_format_combo = ctk.CTkOptionMenu(
            disk_frame, values=["raw", "qcow2", "qed", "vdi", "vmdk", "vpc"], width=80, font=CTK_FONT_SMALL,
            command=lambda *args: self._trigger_change()
        )
        disk_format_combo.set(config["format"])
        disk_format_combo.grid(row=1, column=3, padx=5, pady=2, sticky="w")

        # 路径和总线
        ctk.CTkLabel(disk_frame, text="路径:", font=CTK_FONT_SMALL, width=50, anchor="w").grid(
            row=2, column=0, padx=5, pady=2, sticky="w"
        )
        path_frame = ctk.CTkFrame(disk_frame, fg_color="transparent")
        path_frame.grid(row=2, column=1, columnspan=2, padx=5, pady=2, sticky="ew")
        path_frame.grid_columnconfigure(0, weight=1)
        disk_path_entry = ctk.CTkEntry(path_frame, placeholder_text="/path/to/disk.img", font=CTK_FONT_SMALL)
        disk_path_entry.grid(row=0, column=0, padx=(0, 5), sticky="ew")
        disk_path_entry.insert(0, config["path"])
        disk_path_entry.bind("<KeyRelease>", lambda e: self._trigger_change())
        ctk.CTkButton(
            path_frame, text="浏览", width=50, font=CTK_FONT_SMALL,
            command=lambda: self._browse_entry_path(disk_path_entry)
        ).grid(row=0, column=1, sticky="e")

        ctk.CTkLabel(disk_frame, text="总线:", font=CTK_FONT_SMALL, width=50, anchor="w").grid(
            row=2, column=3, padx=5, pady=2, sticky="w"
        )
        disk_bus_combo = ctk.CTkOptionMenu(
            disk_frame, values=["virtio", "ide", "sata", "scsi", "usb"], width=80, font=CTK_FONT_SMALL,
            command=lambda *args: self._trigger_change()
        )
        disk_bus_combo.set(config["bus"])
        disk_bus_combo.grid(row=2, column=4, padx=5, pady=2, sticky="w")

        # 设备类型和缓存
        ctk.CTkLabel(disk_frame, text="设备:", font=CTK_FONT_SMALL, width=50, anchor="w").grid(
            row=3, column=0, padx=5, pady=2, sticky="w"
        )
        device_type_combo = ctk.CTkOptionMenu(
            disk_frame, values=["disk", "cdrom", "floppy", "lun"], width=100, font=CTK_FONT_SMALL,
            command=lambda *args: self._trigger_change()
        )
        device_type_combo.set(config["device_type"])
        device_type_combo.grid(row=3, column=1, padx=5, pady=2, sticky="w")

        ctk.CTkLabel(disk_frame, text="缓存:", font=CTK_FONT_SMALL, width=50, anchor="w").grid(
            row=3, column=2, padx=5, pady=2, sticky="w"
        )
        cache_mode_combo = ctk.CTkOptionMenu(
            disk_frame, values=["none", "writeback", "writethrough", "directsync", "unsafe"],
            width=100, font=CTK_FONT_SMALL,
            command=lambda *args: self._trigger_change()
        )
        cache_mode_combo.set(config["cache"])
        cache_mode_combo.grid(row=3, column=3, padx=5, pady=2, sticky="w")

        # 复选框
        check_frame = ctk.CTkFrame(disk_frame, fg_color="transparent")
        check_frame.grid(row=4, column=0, columnspan=3, padx=5, pady=2, sticky="w")

        readonly_check = ctk.CTkCheckBox(check_frame, text="只读", font=CTK_FONT_SMALL,
                                          command=lambda: self._trigger_change())
        readonly_check.grid(row=0, column=0, padx=10, sticky="w")
        if config["readonly"]:
            readonly_check.select()

        shareable_check = ctk.CTkCheckBox(check_frame, text="共享", font=CTK_FONT_SMALL,
                                           command=lambda: self._trigger_change())
        shareable_check.grid(row=0, column=1, padx=10, sticky="w")
        if config["shareable"]:
            shareable_check.select()

        discard_check = ctk.CTkCheckBox(check_frame, text="TRIM", font=CTK_FONT_SMALL,
                                         command=lambda: self._trigger_change())
        discard_check.grid(row=0, column=2, padx=10, sticky="w")
        if config["discard"]:
            discard_check.select()

        # 删除按钮
        del_btn = ctk.CTkButton(
            disk_frame, text="删除", width=60, fg_color="#757575", hover_color="#616161",
            font=CTK_FONT_SMALL,
            command=lambda: self._remove_disk(disk_frame),
        )
        del_btn.grid(row=4, column=4, padx=5, pady=2, sticky="e")

        # 存储磁盘引用
        self.disks.append({
            "frame": disk_frame,
            "type": disk_type_combo,
            "format": disk_format_combo,
            "path": disk_path_entry,
            "bus": disk_bus_combo,
            "device_type": device_type_combo,
            "cache": cache_mode_combo,
            "readonly": readonly_check,
            "shareable": shareable_check,
            "discard": discard_check,
        })

    def _browse_entry_path(self, entry_widget):
        """浏览文件路径."""
        file_path = filedialog.askopenfilename(
            title="选择磁盘文件",
            filetypes=[("磁盘镜像", "*.img *.qcow2 *.raw *.vdi *.vmdk"), ("所有文件", "*.*")],
        )
        if file_path:
            entry_widget.delete(0, ctk.END)
            entry_widget.insert(0, file_path)
            self._trigger_change()

    def _remove_disk(self, disk_frame):
        """删除磁盘."""
        for i, disk in enumerate(self.disks):
            if disk["frame"] == disk_frame:
                disk["frame"].destroy()
                self.disks.pop(i)
                # 重新编号
                for j, d in enumerate(self.disks):
                    label = d["frame"].winfo_children()[0]
                    label.configure(text=f"磁盘 {j + 1}")
                self._trigger_change()
                break

    # ========== 网络接口 Tab ==========
    def _init_network_tab(self):
        """初始化网络接口 Tab."""
        self.network_tab.grid_columnconfigure(0, weight=1)

        # 标题
        ctk.CTkLabel(
            self.network_tab,
            text="已配置的网络接口:",
            font=CTK_FONT_MAIN,
            text_color="#64b5f6"
        ).grid(row=0, column=0, padx=10, pady=8, sticky="w")

        # 网卡列表容器
        self.interfaces_container = ctk.CTkScrollableFrame(
            self.network_tab, fg_color=BG_COLOR_CONTENT, corner_radius=6
        )
        self.interfaces_container.grid(row=1, column=0, padx=10, pady=8, sticky="nsew")
        self.interfaces_container.grid_columnconfigure(0, weight=1)
        self.network_tab.grid_rowconfigure(1, weight=1)

        # 添加默认网卡
        self._add_interface()

        # 添加网卡表单区域
        self._create_add_interface_form()

    def _create_add_interface_form(self):
        """创建添加网卡表单."""
        form_frame = ctk.CTkFrame(self.network_tab, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        form_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        form_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            form_frame, text="添加新网卡", font=CTK_FONT_MAIN, text_color="#64b5f6"
        ).grid(row=0, column=0, columnspan=4, padx=10, pady=5, sticky="w")

        # 网络类型
        ctk.CTkLabel(form_frame, text="网络类型:", font=CTK_FONT_SMALL, width=80, anchor="w").grid(
            row=1, column=0, padx=5, pady=2, sticky="w"
        )
        self.new_network_type = ctk.CTkOptionMenu(
            form_frame, values=["network", "bridge", "direct", "user", "internal"],
            width=120, font=CTK_FONT_SMALL
        )
        self.new_network_type.set("network")
        self.new_network_type.grid(row=1, column=1, padx=5, pady=2, sticky="w")

        # 源网络
        ctk.CTkLabel(form_frame, text="源网络:", font=CTK_FONT_SMALL, width=80, anchor="w").grid(
            row=1, column=2, padx=5, pady=2, sticky="w"
        )
        self.new_source = ctk.CTkEntry(form_frame, placeholder_text="default", width=150, font=CTK_FONT_SMALL)
        self.new_source.grid(row=1, column=3, padx=5, pady=2, sticky="w")
        self.new_source.insert(0, "default")

        # 设备模型
        ctk.CTkLabel(form_frame, text="模型:", font=CTK_FONT_SMALL, width=80, anchor="w").grid(
            row=2, column=0, padx=5, pady=2, sticky="w"
        )
        self.new_model = ctk.CTkOptionMenu(
            form_frame, values=["virtio", "e1000", "rtl8139", "vmxnet3", "ne2k_pci"],
            width=120, font=CTK_FONT_SMALL
        )
        self.new_model.set("virtio")
        self.new_model.grid(row=2, column=1, padx=5, pady=2, sticky="w")

        # MAC 地址
        ctk.CTkLabel(form_frame, text="MAC:", font=CTK_FONT_SMALL, width=80, anchor="w").grid(
            row=2, column=2, padx=5, pady=2, sticky="w"
        )
        mac_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        mac_frame.grid(row=2, column=3, padx=5, pady=2, sticky="w")
        mac_frame.grid_columnconfigure(0, weight=1)
        self.new_mac = ctk.CTkEntry(mac_frame, placeholder_text="自动生成", width=140, font=CTK_FONT_SMALL)
        self.new_mac.grid(row=0, column=0, padx=(0, 5), sticky="w")
        ctk.CTkButton(
            mac_frame, text="生成", width=50, font=CTK_FONT_SMALL, command=self._generate_mac
        ).grid(row=0, column=1, sticky="w")

        # 带宽
        ctk.CTkLabel(form_frame, text="带宽 (Mbps):", font=CTK_FONT_SMALL, width=80, anchor="w").grid(
            row=3, column=0, padx=5, pady=2, sticky="w"
        )
        self.new_bandwidth = ctk.CTkEntry(form_frame, placeholder_text="0=无限制", width=100, font=CTK_FONT_SMALL)
        self.new_bandwidth.grid(row=3, column=1, padx=5, pady=2, sticky="w")
        self.new_bandwidth.insert(0, "0")

        # 添加按钮
        ctk.CTkButton(
            form_frame,
            text="添加此网卡",
            width=100,
            font=CTK_FONT_SMALL,
            fg_color="#4caf50",
            hover_color="#388e3c",
            command=self._add_interface_from_form,
        ).grid(row=3, column=3, padx=5, pady=2, sticky="e")

    def _generate_mac(self):
        """生成随机 MAC 地址."""
        mac = [0x52, 0x54, 0x00] + [uuid.uuid4().int & 0xFF for _ in range(3)]
        mac_str = ":".join(f"{b:02x}" for b in mac)
        self.new_mac.delete(0, ctk.END)
        self.new_mac.insert(0, mac_str)
        self._trigger_change()

    def _add_interface_from_form(self):
        """从表单添加网卡."""
        self._add_interface({
            "type": self.new_network_type.get(),
            "source": self.new_source.get().strip(),
            "model": self.new_model.get(),
            "mac": self.new_mac.get().strip(),
            "bandwidth": self.new_bandwidth.get().strip(),
        })
        self._trigger_change()

    def _add_interface(self, config=None):
        """添加网络接口配置."""
        if config is None:
            config = {
                "type": "network",
                "source": "default",
                "model": "virtio",
                "mac": "",
                "bandwidth": "0",
            }

        iface_id = self._iface_counter
        self._iface_counter += 1

        iface_frame = ctk.CTkFrame(self.interfaces_container, fg_color="transparent")
        iface_frame.grid(row=iface_id, column=0, padx=10, pady=10, sticky="ew")
        iface_frame.grid_columnconfigure(1, weight=1)

        # 标题
        ctk.CTkLabel(
            iface_frame, text=f"网卡 {iface_id + 1}", font=CTK_FONT_MAIN, text_color="#64b5f6"
        ).grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky="w")

        # 网络类型和源
        ctk.CTkLabel(iface_frame, text="类型:", font=CTK_FONT_SMALL, width=60, anchor="w").grid(
            row=1, column=0, padx=5, pady=2, sticky="w"
        )
        network_type_combo = ctk.CTkOptionMenu(
            iface_frame, values=["network", "bridge", "direct", "user", "internal"],
            width=100, font=CTK_FONT_SMALL,
            command=lambda *args: self._trigger_change()
        )
        network_type_combo.set(config["type"])
        network_type_combo.grid(row=1, column=1, padx=5, pady=2, sticky="w")

        ctk.CTkLabel(iface_frame, text="源:", font=CTK_FONT_SMALL, width=40, anchor="w").grid(
            row=1, column=2, padx=5, pady=2, sticky="w"
        )
        source_entry = ctk.CTkEntry(iface_frame, width=120, font=CTK_FONT_SMALL)
        source_entry.grid(row=1, column=3, padx=5, pady=2, sticky="w")
        source_entry.insert(0, config["source"])
        source_entry.bind("<KeyRelease>", lambda e: self._trigger_change())

        # 设备模型和 MAC
        ctk.CTkLabel(iface_frame, text="模型:", font=CTK_FONT_SMALL, width=60, anchor="w").grid(
            row=2, column=0, padx=5, pady=2, sticky="w"
        )
        model_combo = ctk.CTkOptionMenu(
            iface_frame, values=["virtio", "e1000", "rtl8139", "vmxnet3", "ne2k_pci"],
            width=100, font=CTK_FONT_SMALL,
            command=lambda *args: self._trigger_change()
        )
        model_combo.set(config["model"])
        model_combo.grid(row=2, column=1, padx=5, pady=2, sticky="w")

        ctk.CTkLabel(iface_frame, text="MAC:", font=CTK_FONT_SMALL, width=40, anchor="w").grid(
            row=2, column=2, padx=5, pady=2, sticky="w"
        )
        mac_frame = ctk.CTkFrame(iface_frame, fg_color="transparent")
        mac_frame.grid(row=2, column=3, padx=5, pady=2, sticky="w")
        mac_frame.grid_columnconfigure(0, weight=1)
        mac_entry = ctk.CTkEntry(mac_frame, width=110, font=CTK_FONT_SMALL)
        mac_entry.grid(row=0, column=0, padx=(0, 5), sticky="w")
        mac_entry.insert(0, config["mac"])
        mac_entry.bind("<KeyRelease>", lambda e: self._trigger_change())
        ctk.CTkButton(
            mac_frame, text="生成", width=50, font=CTK_FONT_SMALL,
            command=lambda: self._generate_mac_entry(mac_entry)
        ).grid(row=0, column=1, sticky="w")

        # 带宽限制
        ctk.CTkLabel(iface_frame, text="带宽 (Mbps):", font=CTK_FONT_SMALL, width=80, anchor="w").grid(
            row=3, column=0, padx=5, pady=2, sticky="w"
        )
        bandwidth_entry = ctk.CTkEntry(iface_frame, width=100, font=CTK_FONT_SMALL)
        bandwidth_entry.grid(row=3, column=1, padx=5, pady=2, sticky="w")
        bandwidth_entry.insert(0, config["bandwidth"])
        bandwidth_entry.bind("<KeyRelease>", lambda e: self._trigger_change())

        # 删除按钮
        del_btn = ctk.CTkButton(
            iface_frame, text="删除", width=60, fg_color="#757575", hover_color="#616161",
            font=CTK_FONT_SMALL,
            command=lambda: self._remove_interface(iface_frame),
        )
        del_btn.grid(row=3, column=4, padx=5, pady=2, sticky="e")

        # 存储网卡引用
        self.interfaces.append({
            "frame": iface_frame,
            "network_type": network_type_combo,
            "source": source_entry,
            "model": model_combo,
            "mac": mac_entry,
            "bandwidth": bandwidth_entry,
        })
        self._trigger_change()

    def _generate_mac_entry(self, entry_widget):
        """生成随机 MAC 地址."""
        mac = [0x52, 0x54, 0x00] + [uuid.uuid4().int & 0xFF for _ in range(3)]
        mac_str = ":".join(f"{b:02x}" for b in mac)
        entry_widget.delete(0, ctk.END)
        entry_widget.insert(0, mac_str)
        self._trigger_change()

    def _remove_interface(self, iface_frame):
        """删除网络接口."""
        for i, iface in enumerate(self.interfaces):
            if iface["frame"] == iface_frame:
                iface["frame"].destroy()
                self.interfaces.pop(i)
                # 重新编号
                for j, n in enumerate(self.interfaces):
                    label = n["frame"].winfo_children()[0]
                    label.configure(text=f"网卡 {j + 1}")
                self._trigger_change()
                break

    # ========== 图形显示 Tab ==========
    def _init_graphics_tab(self):
        """初始化图形显示 Tab."""
        self.graphics_tab.grid_columnconfigure(0, weight=1)
        self.graphics_tab.grid_columnconfigure(1, weight=1)

        # 图形类型
        ctk.CTkLabel(self.graphics_tab, text="图形类型:", font=CTK_FONT_MAIN, width=120, anchor="w").grid(
            row=0, column=0, padx=10, pady=8, sticky="w"
        )
        self.graphics_type_combo = ctk.CTkOptionMenu(
            self.graphics_tab, values=["vnc", "spice", "rdp", "none"],
            width=150, font=CTK_FONT_SMALL,
            command=lambda *args: self._trigger_change()
        )
        self.graphics_type_combo.set("vnc")
        self.graphics_type_combo.grid(row=0, column=1, padx=10, pady=8, sticky="w")

        # 监听地址
        ctk.CTkLabel(self.graphics_tab, text="监听地址:", font=CTK_FONT_MAIN, width=120, anchor="w").grid(
            row=1, column=0, padx=10, pady=8, sticky="w"
        )
        self.graphics_listen_entry = ctk.CTkEntry(self.graphics_tab, width=200, font=CTK_FONT_SMALL)
        self.graphics_listen_entry.grid(row=1, column=1, padx=10, pady=8, sticky="w")
        self.graphics_listen_entry.insert(0, "0.0.0.0")
        self.graphics_listen_entry.bind("<KeyRelease>", lambda e: self._trigger_change())

        # 端口
        ctk.CTkLabel(self.graphics_tab, text="端口:", font=CTK_FONT_MAIN, width=120, anchor="w").grid(
            row=2, column=0, padx=10, pady=8, sticky="w"
        )
        self.graphics_port_entry = ctk.CTkEntry(self.graphics_tab, width=100, font=CTK_FONT_SMALL)
        self.graphics_port_entry.grid(row=2, column=1, padx=10, pady=8, sticky="w")
        self.graphics_port_entry.insert(0, "5900")
        self.graphics_port_entry.bind("<KeyRelease>", lambda e: self._trigger_change())

        # 密码
        ctk.CTkLabel(self.graphics_tab, text="密码 (可选):", font=CTK_FONT_MAIN, width=120, anchor="w").grid(
            row=3, column=0, padx=10, pady=8, sticky="w"
        )
        self.graphics_pass_entry = ctk.CTkEntry(self.graphics_tab, width=200, font=CTK_FONT_SMALL, show="*")
        self.graphics_pass_entry.grid(row=3, column=1, padx=10, pady=8, sticky="w")
        self.graphics_pass_entry.bind("<KeyRelease>", lambda e: self._trigger_change())

    # ========== 视频设备 Tab ==========
    def _init_video_tab(self):
        """初始化视频设备 Tab."""
        self.video_tab.grid_columnconfigure(0, weight=1)
        self.video_tab.grid_columnconfigure(1, weight=1)

        # 视频模型
        ctk.CTkLabel(self.video_tab, text="视频模型:", font=CTK_FONT_MAIN, width=120, anchor="w").grid(
            row=0, column=0, padx=10, pady=8, sticky="w"
        )
        self.video_model_combo = ctk.CTkOptionMenu(
            self.video_tab, values=["qxl", "virtio", "vmvga", "bochs", "cirrus", "vga"],
            width=150, font=CTK_FONT_SMALL,
            command=lambda *args: self._trigger_change()
        )
        self.video_model_combo.set("qxl")
        self.video_model_combo.grid(row=0, column=1, padx=10, pady=8, sticky="w")

        # 显存大小
        ctk.CTkLabel(self.video_tab, text="显存 (MB):", font=CTK_FONT_MAIN, width=120, anchor="w").grid(
            row=1, column=0, padx=10, pady=8, sticky="w"
        )
        self.vram_entry = ctk.CTkEntry(self.video_tab, width=100, font=CTK_FONT_SMALL)
        self.vram_entry.grid(row=1, column=1, padx=10, pady=8, sticky="w")
        self.vram_entry.insert(0, "64")
        self.vram_entry.bind("<KeyRelease>", lambda e: self._trigger_change())

        # 主显示
        ctk.CTkLabel(self.video_tab, text="主显示:", font=CTK_FONT_MAIN, width=120, anchor="w").grid(
            row=2, column=0, padx=10, pady=8, sticky="w"
        )
        self.primary_video_check = ctk.CTkCheckBox(self.video_tab, text="设为主显示", font=CTK_FONT_SMALL)
        self.primary_video_check.select()
        self.primary_video_check.grid(row=2, column=1, padx=10, pady=8, sticky="w")
        self.primary_video_check.configure(command=self._trigger_change)

    # ========== USB/串口 Tab ==========
    def _init_usb_serial_tab(self):
        """初始化 USB/串口 Tab."""
        self.usb_serial_tab.grid_columnconfigure(0, weight=1)
        self.usb_serial_tab.grid_columnconfigure(1, weight=1)

        # USB 控制器类型
        ctk.CTkLabel(self.usb_serial_tab, text="USB 控制器:", font=CTK_FONT_MAIN, width=120, anchor="w").grid(
            row=0, column=0, padx=10, pady=8, sticky="w"
        )
        self.usb_controller_combo = ctk.CTkOptionMenu(
            self.usb_serial_tab,
            values=["qemu-xhci", "piix3-uhci", "piix4-uhci", "nec-xhci", "ich9-ehci1", "none"],
            width=150, font=CTK_FONT_SMALL,
            command=lambda *args: self._trigger_change()
        )
        self.usb_controller_combo.set("qemu-xhci")
        self.usb_controller_combo.grid(row=0, column=1, padx=10, pady=8, sticky="w")

        # 禁用 USB
        self.disable_usb_check = ctk.CTkCheckBox(
            self.usb_serial_tab, text="禁用 USB 支持", font=CTK_FONT_SMALL
        )
        self.disable_usb_check.grid(row=1, column=0, columnspan=2, padx=10, pady=8, sticky="w")
        self.disable_usb_check.configure(command=self._trigger_change)

        # 分隔线
        separator = ctk.CTkFrame(self.usb_serial_tab, height=2, fg_color="#444444")
        separator.grid(row=2, column=0, columnspan=2, padx=10, pady=15, sticky="ew")

        # 串口类型
        ctk.CTkLabel(self.usb_serial_tab, text="串口类型:", font=CTK_FONT_MAIN, width=120, anchor="w").grid(
            row=3, column=0, padx=10, pady=8, sticky="w"
        )
        self.serial_type_combo = ctk.CTkOptionMenu(
            self.usb_serial_tab, values=["pty", "stdio", "file", "tcp", "udp", "unix", "spicevmc", "none"],
            width=150, font=CTK_FONT_SMALL,
            command=lambda *args: self._trigger_change()
        )
        self.serial_type_combo.set("pty")
        self.serial_type_combo.grid(row=3, column=1, padx=10, pady=8, sticky="w")

        # 串口端口
        ctk.CTkLabel(self.usb_serial_tab, text="端口号:", font=CTK_FONT_MAIN, width=120, anchor="w").grid(
            row=4, column=0, padx=10, pady=8, sticky="w"
        )
        self.serial_port_entry = ctk.CTkEntry(self.usb_serial_tab, width=100, font=CTK_FONT_SMALL)
        self.serial_port_entry.grid(row=4, column=1, padx=10, pady=8, sticky="w")
        self.serial_port_entry.insert(0, "0")
        self.serial_port_entry.bind("<KeyRelease>", lambda e: self._trigger_change())

    # ========== 输入/声音 Tab ==========
    def _init_input_sound_tab(self):
        """初始化输入/声音 Tab."""
        self.input_sound_tab.grid_columnconfigure(0, weight=1)
        self.input_sound_tab.grid_columnconfigure(1, weight=1)

        # TPM 模型
        ctk.CTkLabel(self.input_sound_tab, text="TPM 模型:", font=CTK_FONT_MAIN, width=120, anchor="w").grid(
            row=0, column=0, padx=10, pady=8, sticky="w"
        )
        self.tpm_model_combo = ctk.CTkOptionMenu(
            self.input_sound_tab, values=["tpm-crb", "tpm-tis", "tpm-spapr", "none"],
            width=150, font=CTK_FONT_SMALL,
            command=lambda *args: self._trigger_change()
        )
        self.tpm_model_combo.set("tpm-crb")
        self.tpm_model_combo.grid(row=0, column=1, padx=10, pady=8, sticky="w")

        # TPM 版本
        ctk.CTkLabel(self.input_sound_tab, text="TPM 版本:", font=CTK_FONT_MAIN, width=120, anchor="w").grid(
            row=1, column=0, padx=10, pady=8, sticky="w"
        )
        self.tpm_version_combo = ctk.CTkOptionMenu(
            self.input_sound_tab, values=["1.2", "2.0"], width=100, font=CTK_FONT_SMALL,
            command=lambda *args: self._trigger_change()
        )
        self.tpm_version_combo.set("2.0")
        self.tpm_version_combo.grid(row=1, column=1, padx=10, pady=8, sticky="w")

        # 禁用声音
        self.disable_sound_check = ctk.CTkCheckBox(
            self.input_sound_tab, text="禁用声音设备", font=CTK_FONT_SMALL
        )
        self.disable_sound_check.grid(row=2, column=0, columnspan=2, padx=10, pady=8, sticky="w")
        self.disable_sound_check.configure(command=self._trigger_change)

        # 音频模型
        ctk.CTkLabel(self.input_sound_tab, text="音频模型:", font=CTK_FONT_MAIN, width=120, anchor="w").grid(
            row=3, column=0, padx=10, pady=8, sticky="w"
        )
        self.audio_model_combo = ctk.CTkOptionMenu(
            self.input_sound_tab, values=["ich9", "ich6", "ac97", "virtio", "pcspk"],
            width=150, font=CTK_FONT_SMALL,
            command=lambda *args: self._trigger_change()
        )
        self.audio_model_combo.set("ich9")
        self.audio_model_combo.grid(row=3, column=1, padx=10, pady=8, sticky="w")

        # 键盘
        ctk.CTkLabel(self.input_sound_tab, text="键盘:", font=CTK_FONT_MAIN, width=120, anchor="w").grid(
            row=4, column=0, padx=10, pady=8, sticky="w"
        )
        self.keyboard_combo = ctk.CTkOptionMenu(
            self.input_sound_tab, values=["virtio", "ps2", "usb", "none"],
            width=150, font=CTK_FONT_SMALL,
            command=lambda *args: self._trigger_change()
        )
        self.keyboard_combo.set("virtio")
        self.keyboard_combo.grid(row=4, column=1, padx=10, pady=8, sticky="w")

        # 鼠标
        ctk.CTkLabel(self.input_sound_tab, text="鼠标:", font=CTK_FONT_MAIN, width=120, anchor="w").grid(
            row=5, column=0, padx=10, pady=8, sticky="w"
        )
        self.mouse_combo = ctk.CTkOptionMenu(
            self.input_sound_tab, values=["virtio", "ps2", "usb", "tablet"],
            width=150, font=CTK_FONT_SMALL,
            command=lambda *args: self._trigger_change()
        )
        self.mouse_combo.set("tablet")
        self.mouse_combo.grid(row=5, column=1, padx=10, pady=8, sticky="w")

    # ========== 通用方法 ==========
    def _trigger_change(self, *args):
        """触发变化回调."""
        if self.on_change_callback:
            self.on_change_callback()

    def get_config(self) -> dict:
        """获取配置数据."""
        # 磁盘配置
        disks_config = []
        for disk in self.disks:
            disks_config.append({
                "type": disk["type"].get(),
                "format": disk["format"].get(),
                "path": disk["path"].get().strip(),
                "bus": disk["bus"].get(),
                "device_type": disk["device_type"].get(),
                "cache": disk["cache"].get(),
                "readonly": disk["readonly"].get(),
                "shareable": disk["shareable"].get(),
                "discard": disk["discard"].get(),
            })

        # 网络配置
        interfaces_config = []
        for iface in self.interfaces:
            interfaces_config.append({
                "type": iface["network_type"].get(),
                "source": iface["source"].get().strip(),
                "model": iface["model"].get(),
                "mac": iface["mac"].get().strip(),
                "bandwidth": iface["bandwidth"].get().strip(),
            })

        return {
            "disks": disks_config,
            "interfaces": interfaces_config,
            "graphics": {
                "type": self.graphics_type_combo.get(),
                "listen": self.graphics_listen_entry.get().strip(),
                "port": self.graphics_port_entry.get().strip(),
                "password": self.graphics_pass_entry.get().strip(),
            },
            "video": {
                "model": self.video_model_combo.get(),
                "vram": int(self.vram_entry.get().strip() or "64"),
                "primary": self.primary_video_check.get(),
            },
            "usb": {
                "controller": self.usb_controller_combo.get(),
                "disabled": self.disable_usb_check.get(),
            },
            "serial": {
                "type": self.serial_type_combo.get(),
                "port": self.serial_port_entry.get().strip(),
            },
            "tpm": {
                "model": self.tpm_model_combo.get(),
                "version": self.tpm_version_combo.get(),
            },
            "audio": {
                "disabled": self.disable_sound_check.get(),
                "model": self.audio_model_combo.get(),
            },
            "input": {
                "keyboard": self.keyboard_combo.get(),
                "mouse": self.mouse_combo.get(),
            },
        }

    def to_xml(self) -> dict:
        """生成 XML 配置字典."""
        config = self.get_config()
        devices = {}

        # 磁盘设备
        if config["disks"]:
            devices["disks"] = config["disks"]

        # 网络接口
        if config["interfaces"]:
            devices["interfaces"] = config["interfaces"]

        # 图形设备
        if config["graphics"]["type"] != "none":
            devices["graphics"] = config["graphics"]

        # 视频设备
        devices["video"] = config["video"]

        # USB 控制器
        if not config["usb"]["disabled"]:
            devices["usb_controller"] = config["usb"]["controller"]

        # 串口
        if config["serial"]["type"] != "none":
            devices["serial"] = config["serial"]

        # TPM
        if config["tpm"]["model"] != "none":
            devices["tpm"] = config["tpm"]

        # 音频
        if not config["audio"]["disabled"]:
            devices["audio"] = config["audio"]

        # 输入设备
        devices["input"] = config["input"]

        return {"devices": devices}

    def load_config(self, config: dict):
        """加载配置数据到 UI."""
        # 加载磁盘
        if "disks" in config:
            for disk in self.disks:
                disk["frame"].destroy()
            self.disks = []
            self._disk_counter = 0
            for disk_data in config["disks"]:
                self._add_disk(disk_data)

        # 加载网卡
        if "interfaces" in config:
            for iface in self.interfaces:
                iface["frame"].destroy()
            self.interfaces = []
            self._iface_counter = 0
            for iface_data in config["interfaces"]:
                self._add_interface(iface_data)

        # 加载图形
        if "graphics" in config:
            g = config["graphics"]
            if "type" in g:
                self.graphics_type_combo.set(g["type"])
            if "listen" in g:
                self.graphics_listen_entry.delete(0, ctk.END)
                self.graphics_listen_entry.insert(0, g["listen"])
            if "port" in g:
                self.graphics_port_entry.delete(0, ctk.END)
                self.graphics_port_entry.insert(0, g["port"])

        # 加载视频
        if "video" in config:
            v = config["video"]
            if "model" in v:
                self.video_model_combo.set(v["model"])
            if "vram" in v:
                self.vram_entry.delete(0, ctk.END)
                self.vram_entry.insert(0, str(v["vram"]))
