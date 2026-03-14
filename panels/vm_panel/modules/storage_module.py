"""模块 4: 存储设备 - 磁盘配置管理."""

import customtkinter as ctk
from tkinter import filedialog

from ..styles import BG_COLOR_CONTENT, CTK_FONT_MAIN, CTK_FONT_SMALL


class StorageModule(ctk.CTkFrame):
    """存储设备模块."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="transparent")
        self.on_change_callback = on_change_callback

        # 创建 Tab 视图
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=0, column=0, sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 添加子 Tab
        self.disk_list_tab = self.tabview.add("磁盘列表")
        self.disk_add_tab = self.tabview.add("添加磁盘")

        # 磁盘列表
        self.disks = []
        self._disk_counter = 0

        # 初始化 UI
        self._init_disk_list_tab()
        self._init_disk_add_tab()

    def _init_disk_list_tab(self):
        """初始化磁盘列表 Tab."""
        self.disk_list_tab.grid_columnconfigure(0, weight=1)

        # 提示信息
        ctk.CTkLabel(
            self.disk_list_tab,
            text="已配置的磁盘设备:",
            font=CTK_FONT_MAIN,
            text_color="#64b5f6"
        ).grid(row=0, column=0, padx=10, pady=8, sticky="w")

        # 磁盘列表容器
        self.disks_container = ctk.CTkScrollableFrame(
            self.disk_list_tab, fg_color=BG_COLOR_CONTENT, corner_radius=6
        )
        self.disks_container.grid(row=1, column=0, padx=10, pady=8, sticky="nsew")
        self.disks_container.grid_columnconfigure(0, weight=1)

        # 添加默认磁盘
        self._add_disk()

    def _init_disk_add_tab(self):
        """初始化添加磁盘 Tab."""
        self.disk_add_tab.grid_columnconfigure(0, weight=1)
        self.disk_add_tab.grid_columnconfigure(1, weight=1)

        # 磁盘类型
        ctk.CTkLabel(self.disk_add_tab, text="磁盘类型:", font=CTK_FONT_MAIN, width=120, anchor="w").grid(
            row=0, column=0, padx=10, pady=8, sticky="w"
        )
        self.new_disk_type = ctk.CTkOptionMenu(
            self.disk_add_tab, values=["file", "block", "network"], width=200, font=CTK_FONT_SMALL
        )
        self.new_disk_type.set("file")
        self.new_disk_type.grid(row=0, column=1, padx=10, pady=8, sticky="w")

        # 存储格式
        ctk.CTkLabel(self.disk_add_tab, text="存储格式:", font=CTK_FONT_MAIN, width=120, anchor="w").grid(
            row=1, column=0, padx=10, pady=8, sticky="w"
        )
        self.new_disk_format = ctk.CTkOptionMenu(
            self.disk_add_tab, values=["raw", "qcow2", "qed", "vdi", "vmdk", "vpc"], width=200, font=CTK_FONT_SMALL
        )
        self.new_disk_format.set("raw")
        self.new_disk_format.grid(row=1, column=1, padx=10, pady=8, sticky="w")

        # 目标总线
        ctk.CTkLabel(self.disk_add_tab, text="目标总线:", font=CTK_FONT_MAIN, width=120, anchor="w").grid(
            row=2, column=0, padx=10, pady=8, sticky="w"
        )
        self.new_disk_bus = ctk.CTkOptionMenu(
            self.disk_add_tab, values=["virtio", "ide", "sata", "scsi", "usb"], width=200, font=CTK_FONT_SMALL
        )
        self.new_disk_bus.set("virtio")
        self.new_disk_bus.grid(row=2, column=1, padx=10, pady=8, sticky="w")

        # 设备类型
        ctk.CTkLabel(self.disk_add_tab, text="设备类型:", font=CTK_FONT_MAIN, width=120, anchor="w").grid(
            row=3, column=0, padx=10, pady=8, sticky="w"
        )
        self.new_device_type = ctk.CTkOptionMenu(
            self.disk_add_tab, values=["disk", "cdrom", "floppy", "lun"], width=200, font=CTK_FONT_SMALL
        )
        self.new_device_type.set("disk")
        self.new_device_type.grid(row=3, column=1, padx=10, pady=8, sticky="w")

        # 文件路径
        ctk.CTkLabel(self.disk_add_tab, text="文件路径:", font=CTK_FONT_MAIN, width=120, anchor="w").grid(
            row=4, column=0, padx=10, pady=8, sticky="w"
        )
        path_frame = ctk.CTkFrame(self.disk_add_tab, fg_color="transparent")
        path_frame.grid(row=4, column=1, padx=10, pady=8, sticky="ew")
        path_frame.grid_columnconfigure(0, weight=1)
        self.new_disk_path = ctk.CTkEntry(path_frame, placeholder_text="/path/to/disk.img", width=300)
        self.new_disk_path.grid(row=0, column=0, padx=(0, 5), sticky="w")
        ctk.CTkButton(
            path_frame, text="浏览", width=60, font=CTK_FONT_SMALL, command=self._browse_path
        ).grid(row=0, column=1, sticky="w")

        # 缓存模式
        ctk.CTkLabel(self.disk_add_tab, text="缓存模式:", font=CTK_FONT_MAIN, width=120, anchor="w").grid(
            row=5, column=0, padx=10, pady=8, sticky="w"
        )
        self.new_cache_mode = ctk.CTkOptionMenu(
            self.disk_add_tab,
            values=["none", "writeback", "writethrough", "directsync", "unsafe"],
            width=200, font=CTK_FONT_SMALL
        )
        self.new_cache_mode.set("none")
        self.new_cache_mode.grid(row=5, column=1, padx=10, pady=8, sticky="w")

        # 复选框
        check_frame = ctk.CTkFrame(self.disk_add_tab, fg_color="transparent")
        check_frame.grid(row=6, column=0, columnspan=2, padx=10, pady=8, sticky="w")

        self.new_readonly = ctk.CTkCheckBox(check_frame, text="只读", font=CTK_FONT_SMALL)
        self.new_readonly.grid(row=0, column=0, padx=10, sticky="w")

        self.new_shareable = ctk.CTkCheckBox(check_frame, text="共享", font=CTK_FONT_SMALL)
        self.new_shareable.grid(row=0, column=1, padx=10, sticky="w")

        self.new_discard = ctk.CTkCheckBox(check_frame, text="启用 TRIM", font=CTK_FONT_SMALL)
        self.new_discard.grid(row=0, column=2, padx=10, sticky="w")

        # 添加按钮
        ctk.CTkButton(
            self.disk_add_tab,
            text="添加此磁盘",
            width=150,
            font=CTK_FONT_SMALL,
            fg_color="#4caf50",
            hover_color="#388e3c",
            command=self._add_disk_from_form,
        ).grid(row=7, column=0, columnspan=2, padx=10, pady=20, sticky="w")

    def _browse_path(self):
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

    def _trigger_change(self, *args):
        """触发变化回调."""
        if self.on_change_callback:
            self.on_change_callback()

    def get_config(self) -> dict:
        """获取配置数据."""
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
        return {"disks": disks_config}

    def to_xml(self) -> dict:
        """生成 XML 配置字典."""
        config = self.get_config()
        return {"devices": {"disks": config["disks"]}}

    def load_config(self, config: dict):
        """加载配置数据到 UI."""
        # 清空现有磁盘
        for disk in self.disks:
            disk["frame"].destroy()
        self.disks = []
        self._disk_counter = 0

        # 加载新配置
        if "disks" in config:
            for disk_data in config["disks"]:
                self._add_disk(disk_data)
