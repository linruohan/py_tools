"""模块 5: 网络接口 - 网卡配置管理."""

import customtkinter as ctk
import uuid

from ..styles import BG_COLOR_CONTENT, CTK_FONT_MAIN, CTK_FONT_SMALL


class NetworkModule(ctk.CTkFrame):
    """网络接口模块."""

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
        self.interface_list_tab = self.tabview.add("网卡列表")
        self.interface_add_tab = self.tabview.add("添加网卡")

        # 网卡列表
        self.interfaces = []
        self._iface_counter = 0

        # 初始化 UI
        self._init_interface_list_tab()
        self._init_interface_add_tab()

    def _init_interface_list_tab(self):
        """初始化网卡列表 Tab."""
        self.interface_list_tab.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self.interface_list_tab,
            text="已配置的网络接口:",
            font=CTK_FONT_MAIN,
            text_color="#64b5f6"
        ).grid(row=0, column=0, padx=10, pady=8, sticky="w")

        # 网卡列表容器
        self.interfaces_container = ctk.CTkScrollableFrame(
            self.interface_list_tab, fg_color=BG_COLOR_CONTENT, corner_radius=6
        )
        self.interfaces_container.grid(row=1, column=0, padx=10, pady=8, sticky="nsew")
        self.interfaces_container.grid_columnconfigure(0, weight=1)

        # 添加默认网卡
        self._add_interface()

    def _init_interface_add_tab(self):
        """初始化添加网卡 Tab."""
        self.interface_add_tab.grid_columnconfigure(0, weight=1)
        self.interface_add_tab.grid_columnconfigure(1, weight=1)

        # 网络类型
        ctk.CTkLabel(self.interface_add_tab, text="网络类型:", font=CTK_FONT_MAIN, width=120, anchor="w").grid(
            row=0, column=0, padx=10, pady=8, sticky="w"
        )
        self.new_network_type = ctk.CTkOptionMenu(
            self.interface_add_tab, values=["network", "bridge", "direct", "user", "internal"],
            width=200, font=CTK_FONT_SMALL
        )
        self.new_network_type.set("network")
        self.new_network_type.grid(row=0, column=1, padx=10, pady=8, sticky="w")

        # 源网络
        ctk.CTkLabel(self.interface_add_tab, text="源网络/网桥:", font=CTK_FONT_MAIN, width=120, anchor="w").grid(
            row=1, column=0, padx=10, pady=8, sticky="w"
        )
        self.new_source = ctk.CTkEntry(self.interface_add_tab, placeholder_text="default", width=200, font=CTK_FONT_SMALL)
        self.new_source.grid(row=1, column=1, padx=10, pady=8, sticky="w")
        self.new_source.insert(0, "default")

        # 设备模型
        ctk.CTkLabel(self.interface_add_tab, text="设备模型:", font=CTK_FONT_MAIN, width=120, anchor="w").grid(
            row=2, column=0, padx=10, pady=8, sticky="w"
        )
        self.new_model = ctk.CTkOptionMenu(
            self.interface_add_tab, values=["virtio", "e1000", "rtl8139", "vmxnet3", "ne2k_pci"],
            width=200, font=CTK_FONT_SMALL
        )
        self.new_model.set("virtio")
        self.new_model.grid(row=2, column=1, padx=10, pady=8, sticky="w")

        # MAC 地址
        ctk.CTkLabel(self.interface_add_tab, text="MAC 地址:", font=CTK_FONT_MAIN, width=120, anchor="w").grid(
            row=3, column=0, padx=10, pady=8, sticky="w"
        )
        mac_frame = ctk.CTkFrame(self.interface_add_tab, fg_color="transparent")
        mac_frame.grid(row=3, column=1, padx=10, pady=8, sticky="w")
        mac_frame.grid_columnconfigure(0, weight=1)
        self.new_mac = ctk.CTkEntry(mac_frame, placeholder_text="自动生成", width=200, font=CTK_FONT_SMALL)
        self.new_mac.grid(row=0, column=0, padx=(0, 5), sticky="w")
        ctk.CTkButton(
            mac_frame, text="生成", width=60, font=CTK_FONT_SMALL, command=self._generate_mac
        ).grid(row=0, column=1, sticky="w")

        # 带宽限制
        ctk.CTkLabel(self.interface_add_tab, text="带宽限制 (Mbps):", font=CTK_FONT_MAIN, width=120, anchor="w").grid(
            row=4, column=0, padx=10, pady=8, sticky="w"
        )
        self.new_bandwidth = ctk.CTkEntry(self.interface_add_tab, placeholder_text="0=无限制", width=200, font=CTK_FONT_SMALL)
        self.new_bandwidth.grid(row=4, column=1, padx=10, pady=8, sticky="w")
        self.new_bandwidth.insert(0, "0")

        # 添加按钮
        ctk.CTkButton(
            self.interface_add_tab,
            text="添加此网卡",
            width=150,
            font=CTK_FONT_SMALL,
            fg_color="#4caf50",
            hover_color="#388e3c",
            command=self._add_interface_from_form,
        ).grid(row=5, column=0, columnspan=2, padx=10, pady=20, sticky="w")

    def _generate_mac(self):
        """生成随机 MAC 地址."""
        mac = [0x52, 0x54, 0x00] + [uuid.uuid4().int & 0xFF for _ in range(3)]
        mac_str = ":".join(f"{b:02x}" for b in mac)
        self.new_mac.delete(0, ctk.END)
        self.new_mac.insert(0, mac_str)

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
        ctk.CTkLabel(iface_frame, text="网络类型:", font=CTK_FONT_SMALL, width=80, anchor="w").grid(
            row=1, column=0, padx=5, pady=2, sticky="w"
        )
        network_type_combo = ctk.CTkOptionMenu(
            iface_frame, values=["network", "bridge", "direct", "user", "internal"],
            width=100, font=CTK_FONT_SMALL,
            command=lambda *args: self._trigger_change()
        )
        network_type_combo.set(config["type"])
        network_type_combo.grid(row=1, column=1, padx=5, pady=2, sticky="w")

        ctk.CTkLabel(iface_frame, text="源网络:", font=CTK_FONT_SMALL, width=80, anchor="w").grid(
            row=1, column=2, padx=5, pady=2, sticky="w"
        )
        source_entry = ctk.CTkEntry(iface_frame, width=150, font=CTK_FONT_SMALL)
        source_entry.grid(row=1, column=3, padx=5, pady=2, sticky="ew")
        source_entry.insert(0, config["source"])
        source_entry.bind("<KeyRelease>", lambda e: self._trigger_change())

        # 设备模型和 MAC
        ctk.CTkLabel(iface_frame, text="设备模型:", font=CTK_FONT_SMALL, width=80, anchor="w").grid(
            row=2, column=0, padx=5, pady=2, sticky="w"
        )
        model_combo = ctk.CTkOptionMenu(
            iface_frame, values=["virtio", "e1000", "rtl8139", "vmxnet3", "ne2k_pci"],
            width=100, font=CTK_FONT_SMALL,
            command=lambda *args: self._trigger_change()
        )
        model_combo.set(config["model"])
        model_combo.grid(row=2, column=1, padx=5, pady=2, sticky="w")

        ctk.CTkLabel(iface_frame, text="MAC 地址:", font=CTK_FONT_SMALL, width=80, anchor="w").grid(
            row=2, column=2, padx=5, pady=2, sticky="w"
        )
        mac_frame = ctk.CTkFrame(iface_frame, fg_color="transparent")
        mac_frame.grid(row=2, column=3, padx=5, pady=2, sticky="ew")
        mac_frame.grid_columnconfigure(0, weight=1)
        mac_entry = ctk.CTkEntry(mac_frame, width=140, font=CTK_FONT_SMALL)
        mac_entry.grid(row=0, column=0, padx=(0, 5), sticky="ew")
        mac_entry.insert(0, config["mac"])
        mac_entry.bind("<KeyRelease>", lambda e: self._trigger_change())
        ctk.CTkButton(
            mac_frame, text="生成", width=50, font=CTK_FONT_SMALL,
            command=lambda: self._generate_mac_entry(mac_entry)
        ).grid(row=0, column=1, sticky="e")

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

    def _trigger_change(self, *args):
        """触发变化回调."""
        if self.on_change_callback:
            self.on_change_callback()

    def get_config(self) -> dict:
        """获取配置数据."""
        interfaces_config = []
        for iface in self.interfaces:
            interfaces_config.append({
                "type": iface["network_type"].get(),
                "source": iface["source"].get().strip(),
                "model": iface["model"].get(),
                "mac": iface["mac"].get().strip(),
                "bandwidth": iface["bandwidth"].get().strip(),
            })
        return {"interfaces": interfaces_config}

    def to_xml(self) -> dict:
        """生成 XML 配置字典."""
        config = self.get_config()
        return {"devices": {"interfaces": config["interfaces"]}}

    def load_config(self, config: dict):
        """加载配置数据到 UI."""
        # 清空现有网卡
        for iface in self.interfaces:
            iface["frame"].destroy()
        self.interfaces = []
        self._iface_counter = 0

        # 加载新配置
        if "interfaces" in config:
            for iface_data in config["interfaces"]:
                self._add_interface(iface_data)
