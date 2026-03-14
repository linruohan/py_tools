"""模块 3: CPU 与内存 - vCPU、CPU 拓扑、内存配置、NUMA 策略."""

import customtkinter as ctk

from ..styles import BG_COLOR_CONTENT, CTK_FONT_MAIN, CTK_FONT_SMALL


class CPUMemoryModule(ctk.CTkFrame):
    """CPU 与内存模块."""

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
        self.cpu_tab = self.tabview.add("CPU 配置")
        self.memory_tab = self.tabview.add("内存配置")
        self.numa_tab = self.tabview.add("NUMA 策略")

        # 初始化 UI
        self._init_cpu_tab()
        self._init_memory_tab()
        self._init_numa_tab()

    def _init_cpu_tab(self):
        """初始化 CPU 配置 Tab."""
        self.cpu_tab.grid_columnconfigure(0, weight=1)
        self.cpu_tab.grid_columnconfigure(1, weight=1)

        # vCPU 数量
        ctk.CTkLabel(self.cpu_tab, text="vCPU 数量:", font=CTK_FONT_MAIN, width=120, anchor="w").grid(
            row=0, column=0, padx=10, pady=8, sticky="w"
        )
        self.vcpu_entry = ctk.CTkEntry(self.cpu_tab, width=150, font=CTK_FONT_SMALL)
        self.vcpu_entry.grid(row=0, column=1, padx=10, pady=8, sticky="w")
        self.vcpu_entry.insert(0, "2")
        self.vcpu_entry.bind("<KeyRelease>", lambda e: self._trigger_change())

        # CPU 模式
        ctk.CTkLabel(self.cpu_tab, text="CPU 模式:", font=CTK_FONT_MAIN, width=120, anchor="w").grid(
            row=1, column=0, padx=10, pady=8, sticky="w"
        )
        self.cpu_mode_combo = ctk.CTkOptionMenu(
            self.cpu_tab,
            values=["host-passthrough", "host-model", "custom", "host-model-required"],
            width=200,
            font=CTK_FONT_SMALL,
        )
        self.cpu_mode_combo.set("host-model")
        self.cpu_mode_combo.grid(row=1, column=1, padx=10, pady=8, sticky="w")
        self.cpu_mode_combo.configure(command=self._trigger_change)

        # CPU 拓扑
        topo_frame = ctk.CTkFrame(self.cpu_tab, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        topo_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        topo_frame.grid_columnconfigure(1, weight=1)
        topo_frame.grid_columnconfigure(3, weight=1)

        ctk.CTkLabel(topo_frame, text="CPU 拓扑:", font=CTK_FONT_MAIN, text_color="#64b5f6").grid(
            row=0, column=0, columnspan=4, padx=10, pady=5, sticky="w"
        )

        # Sockets
        ctk.CTkLabel(topo_frame, text="插槽:", font=CTK_FONT_SMALL, width=60, anchor="w").grid(
            row=1, column=0, padx=10, pady=5, sticky="w"
        )
        self.cpu_sockets_entry = ctk.CTkEntry(topo_frame, width=80, font=CTK_FONT_SMALL)
        self.cpu_sockets_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.cpu_sockets_entry.insert(0, "1")
        self.cpu_sockets_entry.bind("<KeyRelease>", lambda e: self._trigger_change())

        # Cores
        ctk.CTkLabel(topo_frame, text="核心:", font=CTK_FONT_SMALL, width=60, anchor="w").grid(
            row=1, column=2, padx=10, pady=5, sticky="w"
        )
        self.cpu_cores_entry = ctk.CTkEntry(topo_frame, width=80, font=CTK_FONT_SMALL)
        self.cpu_cores_entry.grid(row=1, column=3, padx=5, pady=5, sticky="w")
        self.cpu_cores_entry.insert(0, "2")
        self.cpu_cores_entry.bind("<KeyRelease>", lambda e: self._trigger_change())

        # Threads
        ctk.CTkLabel(topo_frame, text="线程:", font=CTK_FONT_SMALL, width=60, anchor="w").grid(
            row=2, column=0, padx=10, pady=5, sticky="w"
        )
        self.cpu_threads_entry = ctk.CTkEntry(topo_frame, width=80, font=CTK_FONT_SMALL)
        self.cpu_threads_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.cpu_threads_entry.insert(0, "1")
        self.cpu_threads_entry.bind("<KeyRelease>", lambda e: self._trigger_change())

    def _init_memory_tab(self):
        """初始化内存配置 Tab."""
        self.memory_tab.grid_columnconfigure(0, weight=1)
        self.memory_tab.grid_columnconfigure(1, weight=1)

        # 内存大小
        ctk.CTkLabel(self.memory_tab, text="内存大小:", font=CTK_FONT_MAIN, width=120, anchor="w").grid(
            row=0, column=0, padx=10, pady=8, sticky="w"
        )
        mem_size_frame = ctk.CTkFrame(self.memory_tab, fg_color="transparent")
        mem_size_frame.grid(row=0, column=1, padx=10, pady=8, sticky="w")
        mem_size_frame.grid_columnconfigure(0, weight=1)
        self.memory_entry = ctk.CTkEntry(mem_size_frame, width=100, font=CTK_FONT_SMALL)
        self.memory_entry.grid(row=0, column=0, padx=(0, 5), sticky="w")
        self.memory_entry.insert(0, "2048")
        self.memory_entry.bind("<KeyRelease>", lambda e: self._trigger_change())
        self.memory_unit_combo = ctk.CTkOptionMenu(
            mem_size_frame, values=["KiB", "MiB", "GiB"], width=70, font=CTK_FONT_SMALL
        )
        self.memory_unit_combo.set("MiB")
        self.memory_unit_combo.grid(row=0, column=1, sticky="w")
        self.memory_unit_combo.configure(command=self._trigger_change)

        # 当前内存
        ctk.CTkLabel(self.memory_tab, text="当前内存:", font=CTK_FONT_MAIN, width=120, anchor="w").grid(
            row=1, column=0, padx=10, pady=8, sticky="w"
        )
        current_mem_frame = ctk.CTkFrame(self.memory_tab, fg_color="transparent")
        current_mem_frame.grid(row=1, column=1, padx=10, pady=8, sticky="w")
        current_mem_frame.grid_columnconfigure(0, weight=1)
        self.current_memory_entry = ctk.CTkEntry(current_mem_frame, width=100, font=CTK_FONT_SMALL)
        self.current_memory_entry.grid(row=0, column=0, padx=(0, 5), sticky="w")
        self.current_memory_entry.insert(0, "2048")
        self.current_memory_entry.bind("<KeyRelease>", lambda e: self._trigger_change())
        ctk.CTkLabel(current_mem_frame, text="MiB", width=50, font=CTK_FONT_SMALL).grid(
            row=0, column=1, sticky="w"
        )

        # 最大内存
        ctk.CTkLabel(self.memory_tab, text="最大内存:", font=CTK_FONT_MAIN, width=120, anchor="w").grid(
            row=2, column=0, padx=10, pady=8, sticky="w"
        )
        max_mem_frame = ctk.CTkFrame(self.memory_tab, fg_color="transparent")
        max_mem_frame.grid(row=2, column=1, padx=10, pady=8, sticky="w")
        max_mem_frame.grid_columnconfigure(0, weight=1)
        self.max_memory_entry = ctk.CTkEntry(max_mem_frame, width=100, font=CTK_FONT_SMALL)
        self.max_memory_entry.grid(row=0, column=0, padx=(0, 5), sticky="w")
        self.max_memory_entry.insert(0, "4096")
        self.max_memory_entry.bind("<KeyRelease>", lambda e: self._trigger_change())
        ctk.CTkLabel(max_mem_frame, text="MiB", width=50, font=CTK_FONT_SMALL).grid(
            row=0, column=1, sticky="w"
        )

        # 交换内存
        ctk.CTkLabel(self.memory_tab, text="交换内存:", font=CTK_FONT_MAIN, width=120, anchor="w").grid(
            row=3, column=0, padx=10, pady=8, sticky="w"
        )
        swap_mem_frame = ctk.CTkFrame(self.memory_tab, fg_color="transparent")
        swap_mem_frame.grid(row=3, column=1, padx=10, pady=8, sticky="w")
        swap_mem_frame.grid_columnconfigure(0, weight=1)
        self.swap_entry = ctk.CTkEntry(swap_mem_frame, width=100, font=CTK_FONT_SMALL)
        self.swap_entry.grid(row=0, column=0, padx=(0, 5), sticky="w")
        self.swap_entry.insert(0, "0")
        self.swap_entry.bind("<KeyRelease>", lambda e: self._trigger_change())
        ctk.CTkLabel(swap_mem_frame, text="MiB", width=50, font=CTK_FONT_SMALL).grid(
            row=0, column=1, sticky="w"
        )

        # 快速设置按钮
        btn_frame = ctk.CTkFrame(self.memory_tab, fg_color=BG_COLOR_CONTENT)
        btn_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        btn_frame.grid_columnconfigure(0, weight=1)

        mem_presets = [
            ("512M", 512),
            ("1G", 1024),
            ("2G", 2048),
            ("4G", 4096),
            ("8G", 8192),
            ("16G", 16384),
            ("32G", 32768),
        ]

        for i, (label, value) in enumerate(mem_presets):
            btn = ctk.CTkButton(
                btn_frame,
                text=label,
                width=60,
                font=CTK_FONT_SMALL,
                fg_color="transparent",
                border_width=1,
                hover_color=BG_COLOR_CONTENT,
                command=lambda v=value: self._set_memory_preset(v),
            )
            btn.grid(row=0, column=i, padx=5, pady=5)

    def _init_numa_tab(self):
        """初始化 NUMA 策略 Tab."""
        self.numa_tab.grid_columnconfigure(0, weight=1)

        # NUMA 模式
        numa_mode_frame = ctk.CTkFrame(self.numa_tab, fg_color="transparent")
        numa_mode_frame.grid(row=0, column=0, padx=10, pady=8, sticky="w")
        numa_mode_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(numa_mode_frame, text="NUMA 模式:", font=CTK_FONT_MAIN, width=100, anchor="w").grid(
            row=0, column=0, padx=5, pady=5, sticky="w"
        )
        self.numa_mode_combo = ctk.CTkOptionMenu(
            numa_mode_frame,
            values=["strict", "interleave", "preferred", "passthrough"],
            width=150,
            font=CTK_FONT_SMALL,
        )
        self.numa_mode_combo.set("strict")
        self.numa_mode_combo.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.numa_mode_combo.configure(command=self._trigger_change)

        # NUMA 节点列表
        ctk.CTkLabel(self.numa_tab, text="NUMA 节点:", font=CTK_FONT_MAIN, text_color="#64b5f6").grid(
            row=1, column=0, padx=10, pady=8, sticky="w"
        )

        self.numa_nodes_frame = ctk.CTkFrame(self.numa_tab, fg_color=BG_COLOR_CONTENT)
        self.numa_nodes_frame.grid(row=2, column=0, padx=10, pady=8, sticky="ew")
        self.numa_nodes_frame.grid_columnconfigure(1, weight=1)

        # 添加 NUMA 节点按钮
        add_numa_btn = ctk.CTkButton(
            self.numa_tab,
            text="+ 添加 NUMA 节点",
            width=150,
            font=CTK_FONT_SMALL,
            command=self._add_numa_node,
        )
        add_numa_btn.grid(row=3, column=0, padx=10, pady=8, sticky="w")

        # NUMA 节点列表
        self.numa_nodes = []
        self._add_numa_node()  # 添加一个默认节点

    def _set_memory_preset(self, value):
        """设置内存预设值."""
        self.memory_entry.delete(0, ctk.END)
        self.memory_entry.insert(0, str(value))
        self.current_memory_entry.delete(0, ctk.END)
        self.current_memory_entry.insert(0, str(value))
        self.max_memory_entry.delete(0, ctk.END)
        self.max_memory_entry.insert(0, str(value * 2))
        self._trigger_change()

    def _add_numa_node(self):
        """添加 NUMA 节点配置行."""
        row = len(self.numa_nodes)
        node_frame = ctk.CTkFrame(self.numa_nodes_frame, fg_color="transparent")
        node_frame.grid(row=row, column=0, columnspan=2, padx=5, pady=3, sticky="ew")
        node_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(node_frame, text=f"节点{row}:", width=60, font=CTK_FONT_SMALL).grid(
            row=0, column=0, padx=5, sticky="e"
        )

        # 内存
        numa_mem_entry = ctk.CTkEntry(node_frame, width=100, font=CTK_FONT_SMALL, placeholder_text="内存 (MB)")
        numa_mem_entry.grid(row=0, column=1, padx=5, sticky="ew")
        numa_mem_entry.insert(0, "1024")
        numa_mem_entry.bind("<KeyRelease>", lambda e: self._trigger_change())

        # CPU 掩码
        cpumask_entry = ctk.CTkEntry(node_frame, width=120, font=CTK_FONT_SMALL, placeholder_text="CPU 掩码")
        cpumask_entry.grid(row=0, column=2, padx=5, sticky="ew")
        cpumask_entry.insert(0, "0-1")
        cpumask_entry.bind("<KeyRelease>", lambda e: self._trigger_change())

        # 删除按钮
        del_btn = ctk.CTkButton(
            node_frame,
            text="×",
            width=30,
            font=CTK_FONT_SMALL,
            fg_color="#757575",
            hover_color="#616161",
            command=lambda: self._remove_numa_node(node_frame),
        )
        del_btn.grid(row=0, column=3, padx=5, sticky="e")

        self.numa_nodes.append({
            "frame": node_frame,
            "memory": numa_mem_entry,
            "cpumask": cpumask_entry,
        })

    def _remove_numa_node(self, node_frame):
        """删除 NUMA 节点."""
        for i, node in enumerate(self.numa_nodes):
            if node["frame"] == node_frame:
                node["frame"].destroy()
                self.numa_nodes.pop(i)
                # 重新编号
                for j, n in enumerate(self.numa_nodes):
                    label = n["frame"].winfo_children()[0]
                    label.configure(text=f"节点{j}:")
                self._trigger_change()
                break

    def _trigger_change(self, *args):
        """触发变化回调."""
        if self.on_change_callback:
            self.on_change_callback()

    def get_config(self) -> dict:
        """获取配置数据."""
        # 解析内存值
        mem_value = int(self.memory_entry.get().strip() or "0")
        mem_unit = self.memory_unit_combo.get()
        if mem_unit == "GiB":
            mem_value *= 1024
        elif mem_unit == "KiB":
            mem_value //= 1024

        return {
            "vcpu": int(self.vcpu_entry.get().strip() or "2"),
            "cpu_mode": self.cpu_mode_combo.get(),
            "cpu_topology": {
                "sockets": int(self.cpu_sockets_entry.get().strip() or "1"),
                "cores": int(self.cpu_cores_entry.get().strip() or "2"),
                "threads": int(self.cpu_threads_entry.get().strip() or "1"),
            },
            "memory": mem_value,
            "current_memory": int(self.current_memory_entry.get().strip() or "0"),
            "max_memory": int(self.max_memory_entry.get().strip() or "0"),
            "swap": int(self.swap_entry.get().strip() or "0"),
            "numa_mode": self.numa_mode_combo.get(),
            "numa_nodes": [
                {
                    "memory": int(n["memory"].get().strip() or "0"),
                    "cpumask": n["cpumask"].get().strip(),
                }
                for n in self.numa_nodes
            ],
        }

    def to_xml(self) -> dict:
        """生成 XML 配置字典."""
        config = self.get_config()
        result = {
            "cpu_allocation": {
                "current_vcpu": config["vcpu"],
                "max_vcpu": config["vcpu"],
                "topology": config["cpu_topology"],
            },
            "memory_allocation": {
                "memory": config["memory"] * 1024,
                "current_memory": config["current_memory"] * 1024,
                "max_memory": config["max_memory"] * 1024,
                "unit": "KiB",
            },
            "cpu_model_topology": {
                "model": {"mode": config["cpu_mode"]},
            },
        }
        if config["numa_nodes"]:
            result["numa_node_tuning"] = {
                "mode": config["numa_mode"],
                "nodes": config["numa_nodes"],
            }
        return result

    def load_config(self, config: dict):
        """加载配置数据到 UI."""
        if "vcpu" in config:
            self.vcpu_entry.delete(0, ctk.END)
            self.vcpu_entry.insert(0, str(config["vcpu"]))
        if "cpu_topology" in config:
            topo = config["cpu_topology"]
            if "sockets" in topo:
                self.cpu_sockets_entry.delete(0, ctk.END)
                self.cpu_sockets_entry.insert(0, str(topo["sockets"]))
            if "cores" in topo:
                self.cpu_cores_entry.delete(0, ctk.END)
                self.cpu_cores_entry.insert(0, str(topo["cores"]))
            if "threads" in topo:
                self.cpu_threads_entry.delete(0, ctk.END)
                self.cpu_threads_entry.insert(0, str(topo["threads"]))
