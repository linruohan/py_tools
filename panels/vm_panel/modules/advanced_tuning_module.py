"""模块 7: 高级调优 - CPU/内存/IO 调优、虚拟化特性."""

import customtkinter as ctk

from ..styles import BG_COLOR_CONTENT, CTK_FONT_MAIN, CTK_FONT_SMALL


class AdvancedTuningModule(ctk.CTkFrame):
    """高级调优模块."""

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
        self.cpu_tune_tab = self.tabview.add("CPU 调优")
        self.mem_tune_tab = self.tabview.add("内存调优")
        self.blkio_tune_tab = self.tabview.add("块 IO 调优")
        self.features_tab = self.tabview.add("虚拟化特性")

        # 初始化 UI
        self._init_cpu_tune_tab()
        self._init_mem_tune_tab()
        self._init_blkio_tune_tab()
        self._init_features_tab()

    def _init_cpu_tune_tab(self):
        """初始化 CPU 调优 Tab."""
        self.cpu_tune_tab.grid_columnconfigure(0, weight=1)
        self.cpu_tune_tab.grid_columnconfigure(1, weight=1)

        # CPU 调度器
        ctk.CTkLabel(self.cpu_tune_tab, text="CPU 调度器:", font=CTK_FONT_MAIN, width=120, anchor="w").grid(
            row=0, column=0, padx=10, pady=8, sticky="w"
        )
        self.cpu_scheduler_combo = ctk.CTkOptionMenu(
            self.cpu_tune_tab, values=["default", "fifo", "rt", "batch", "idle"],
            width=150, font=CTK_FONT_SMALL,
            command=lambda *args: self._trigger_change()
        )
        self.cpu_scheduler_combo.set("default")
        self.cpu_scheduler_combo.grid(row=0, column=1, padx=10, pady=8, sticky="w")

        # vCPU 绑定
        ctk.CTkLabel(self.cpu_tune_tab, text="vCPU 绑定:", font=CTK_FONT_MAIN, width=120, anchor="w").grid(
            row=1, column=0, padx=10, pady=8, sticky="w"
        )
        self.vcpu_cpuset_entry = ctk.CTkEntry(
            self.cpu_tune_tab, placeholder_text="0-3 或 0,2,4,6", width=200, font=CTK_FONT_SMALL
        )
        self.vcpu_cpuset_entry.grid(row=1, column=1, padx=10, pady=8, sticky="w")
        self.vcpu_cpuset_entry.bind("<KeyRelease>", lambda e: self._trigger_change())

        # 周期限制
        ctk.CTkLabel(self.cpu_tune_tab, text="周期限制 (us):", font=CTK_FONT_MAIN, width=120, anchor="w").grid(
            row=2, column=0, padx=10, pady=8, sticky="w"
        )
        self.cpu_quota_entry = ctk.CTkEntry(
            self.cpu_tune_tab, placeholder_text="-1=无限制", width=100, font=CTK_FONT_SMALL
        )
        self.cpu_quota_entry.grid(row=2, column=1, padx=10, pady=8, sticky="w")
        self.cpu_quota_entry.insert(0, "-1")
        self.cpu_quota_entry.bind("<KeyRelease>", lambda e: self._trigger_change())

    def _init_mem_tune_tab(self):
        """初始化内存调优 Tab."""
        self.mem_tune_tab.grid_columnconfigure(0, weight=1)
        self.mem_tune_tab.grid_columnconfigure(1, weight=1)

        # 硬限制
        ctk.CTkLabel(self.mem_tune_tab, text="硬限制 (KiB):", font=CTK_FONT_MAIN, width=120, anchor="w").grid(
            row=0, column=0, padx=10, pady=8, sticky="w"
        )
        self.mem_hard_limit_entry = ctk.CTkEntry(
            self.mem_tune_tab, placeholder_text="-1=无限制", width=150, font=CTK_FONT_SMALL
        )
        self.mem_hard_limit_entry.grid(row=0, column=1, padx=10, pady=8, sticky="w")
        self.mem_hard_limit_entry.insert(0, "-1")
        self.mem_hard_limit_entry.bind("<KeyRelease>", lambda e: self._trigger_change())

        # 软限制
        ctk.CTkLabel(self.mem_tune_tab, text="软限制 (KiB):", font=CTK_FONT_MAIN, width=120, anchor="w").grid(
            row=1, column=0, padx=10, pady=8, sticky="w"
        )
        self.mem_soft_limit_entry = ctk.CTkEntry(
            self.mem_tune_tab, placeholder_text="-1=无限制", width=150, font=CTK_FONT_SMALL
        )
        self.mem_soft_limit_entry.grid(row=1, column=1, padx=10, pady=8, sticky="w")
        self.mem_soft_limit_entry.insert(0, "-1")
        self.mem_soft_limit_entry.bind("<KeyRelease>", lambda e: self._trigger_change())

        # 内存权重
        ctk.CTkLabel(self.mem_tune_tab, text="权重:", font=CTK_FONT_MAIN, width=120, anchor="w").grid(
            row=2, column=0, padx=10, pady=8, sticky="w"
        )
        self.mem_weight_entry = ctk.CTkEntry(
            self.mem_tune_tab, placeholder_text="默认 100", width=100, font=CTK_FONT_SMALL
        )
        self.mem_weight_entry.grid(row=2, column=1, padx=10, pady=8, sticky="w")
        self.mem_weight_entry.insert(0, "100")
        self.mem_weight_entry.bind("<KeyRelease>", lambda e: self._trigger_change())

    def _init_blkio_tune_tab(self):
        """初始化块 IO 调优 Tab."""
        self.blkio_tune_tab.grid_columnconfigure(0, weight=1)
        self.blkio_tune_tab.grid_columnconfigure(1, weight=1)

        # IO 权重
        ctk.CTkLabel(self.blkio_tune_tab, text="IO 权重:", font=CTK_FONT_MAIN, width=120, anchor="w").grid(
            row=0, column=0, padx=10, pady=8, sticky="w"
        )
        self.io_weight_entry = ctk.CTkEntry(
            self.blkio_tune_tab, placeholder_text="默认 100", width=100, font=CTK_FONT_SMALL
        )
        self.io_weight_entry.grid(row=0, column=1, padx=10, pady=8, sticky="w")
        self.io_weight_entry.insert(0, "100")
        self.io_weight_entry.bind("<KeyRelease>", lambda e: self._trigger_change())

        # 读取 IOPS 限制
        ctk.CTkLabel(self.blkio_tune_tab, text="读 IOPS 限制:", font=CTK_FONT_MAIN, width=120, anchor="w").grid(
            row=1, column=0, padx=10, pady=8, sticky="w"
        )
        self.read_iops_entry = ctk.CTkEntry(
            self.blkio_tune_tab, placeholder_text="0=无限制", width=100, font=CTK_FONT_SMALL
        )
        self.read_iops_entry.grid(row=1, column=1, padx=10, pady=8, sticky="w")
        self.read_iops_entry.insert(0, "0")
        self.read_iops_entry.bind("<KeyRelease>", lambda e: self._trigger_change())

        # 写 IOPS 限制
        ctk.CTkLabel(self.blkio_tune_tab, text="写 IOPS 限制:", font=CTK_FONT_MAIN, width=120, anchor="w").grid(
            row=2, column=0, padx=10, pady=8, sticky="w"
        )
        self.write_iops_entry = ctk.CTkEntry(
            self.blkio_tune_tab, placeholder_text="0=无限制", width=100, font=CTK_FONT_SMALL
        )
        self.write_iops_entry.grid(row=2, column=1, padx=10, pady=8, sticky="w")
        self.write_iops_entry.insert(0, "0")
        self.write_iops_entry.bind("<KeyRelease>", lambda e: self._trigger_change())

    def _init_features_tab(self):
        """初始化虚拟化特性 Tab."""
        self.features_tab.grid_columnconfigure(0, weight=1)

        # 特性复选框列表
        features_frame = ctk.CTkFrame(self.features_tab, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        features_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        features_frame.grid_columnconfigure(1, weight=1)

        self.features_checks = {}
        feature_labels = [
            ("acpi", "ACPI (高级配置与电源管理)", True),
            ("apic", "APIC (高级可编程中断控制器)", True),
            ("pit", "PIT (可编程间隔定时器)", True),
            ("hpet", "HPET (高精度事件定时器)", True),
            ("vmport_disabled", "禁用 VMPort", True),
            ("hyperv", "启用 Hyper-V 兼容", False),
            ("smram", "启用 SMRAM", False),
        ]

        for i, (key, label, default) in enumerate(feature_labels):
            check = ctk.CTkCheckBox(features_frame, text=label, font=CTK_FONT_SMALL)
            if default:
                check.select()
            check.grid(row=i, column=0, columnspan=2, padx=10, pady=5, sticky="w")
            check.configure(command=self._trigger_change)
            self.features_checks[key] = check

    def _trigger_change(self, *args):
        """触发变化回调."""
        if self.on_change_callback:
            self.on_change_callback()

    def get_config(self) -> dict:
        """获取配置数据."""
        return {
            "cpu_tuning": {
                "scheduler": self.cpu_scheduler_combo.get(),
                "cpuset": self.vcpu_cpuset_entry.get().strip(),
                "quota": int(self.cpu_quota_entry.get().strip() or "-1"),
            },
            "memory_tuning": {
                "hard_limit": int(self.mem_hard_limit_entry.get().strip() or "-1"),
                "soft_limit": int(self.mem_soft_limit_entry.get().strip() or "-1"),
                "weight": int(self.mem_weight_entry.get().strip() or "100"),
            },
            "blkio_tuning": {
                "weight": int(self.io_weight_entry.get().strip() or "100"),
                "read_iops": int(self.read_iops_entry.get().strip() or "0"),
                "write_iops": int(self.write_iops_entry.get().strip() or "0"),
            },
            "features": {key: check.get() for key, check in self.features_checks.items()},
        }

    def to_xml(self) -> dict:
        """生成 XML 配置字典."""
        config = self.get_config()
        result = {}

        # CPU 调优
        cpu_tuning = {}
        if config["cpu_tuning"]["cpuset"]:
            cpu_tuning["cpuset"] = config["cpu_tuning"]["cpuset"]
        if config["cpu_tuning"]["quota"] != -1:
            cpu_tuning["quota"] = config["cpu_tuning"]["quota"]
        if cpu_tuning:
            result["cpu_tuning"] = cpu_tuning

        # 内存调优
        mem_tuning = {}
        if config["memory_tuning"]["hard_limit"] != -1:
            mem_tuning["hard_limit"] = config["memory_tuning"]["hard_limit"]
        if config["memory_tuning"]["soft_limit"] != -1:
            mem_tuning["soft_limit"] = config["memory_tuning"]["soft_limit"]
        if config["memory_tuning"]["weight"] != 100:
            mem_tuning["weight"] = config["memory_tuning"]["weight"]
        if mem_tuning:
            result["memory_tuning"] = mem_tuning

        # 块 IO 调优
        blkio_tuning = {}
        if config["blkio_tuning"]["weight"] != 100:
            blkio_tuning["weight"] = config["blkio_tuning"]["weight"]
        if config["blkio_tuning"]["read_iops"] != 0:
            blkio_tuning["read_iops"] = config["blkio_tuning"]["read_iops"]
        if config["blkio_tuning"]["write_iops"] != 0:
            blkio_tuning["write_iops"] = config["blkio_tuning"]["write_iops"]
        if blkio_tuning:
            result["blkio_tuning"] = blkio_tuning

        # 虚拟化特性
        result["features"] = config["features"]

        return result

    def load_config(self, config: dict):
        """加载配置数据到 UI."""
        if "features" in config:
            f = config["features"]
            for key, check in self.features_checks.items():
                if key in f:
                    if f[key]:
                        check.select()
                    else:
                        check.deselect()
