"""模块 8: 元数据与配置 - SMBIOS 信息、自定义元数据."""

import customtkinter as ctk

from ..styles import BG_COLOR_CONTENT, CTK_FONT_MAIN, CTK_FONT_SMALL


class MetadataModule(ctk.CTkFrame):
    """元数据与配置模块."""

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
        self.smbios_tab = self.tabview.add("SMBIOS 信息")
        self.custom_tab = self.tabview.add("自定义元数据")

        # 初始化 UI
        self._init_smbios_tab()
        self._init_custom_tab()

    def _init_smbios_tab(self):
        """初始化 SMBIOS 信息 Tab."""
        self.smbios_tab.grid_columnconfigure(0, weight=1)
        self.smbios_tab.grid_columnconfigure(1, weight=1)

        # 制造商
        ctk.CTkLabel(self.smbios_tab, text="制造商:", font=CTK_FONT_MAIN, width=120, anchor="w").grid(
            row=0, column=0, padx=10, pady=8, sticky="w"
        )
        self.smbios_vendor_entry = ctk.CTkEntry(self.smbios_tab, placeholder_text="QEMU", width=300, font=CTK_FONT_SMALL)
        self.smbios_vendor_entry.grid(row=0, column=1, padx=10, pady=8, sticky="w")
        self.smbios_vendor_entry.insert(0, "QEMU")
        self.smbios_vendor_entry.bind("<KeyRelease>", lambda e: self._trigger_change())

        # 产品名称
        ctk.CTkLabel(self.smbios_tab, text="产品名称:", font=CTK_FONT_MAIN, width=120, anchor="w").grid(
            row=1, column=0, padx=10, pady=8, sticky="w"
        )
        self.smbios_product_entry = ctk.CTkEntry(self.smbios_tab, placeholder_text="Standard PC", width=300, font=CTK_FONT_SMALL)
        self.smbios_product_entry.grid(row=1, column=1, padx=10, pady=8, sticky="w")
        self.smbios_product_entry.insert(0, "Standard PC")
        self.smbios_product_entry.bind("<KeyRelease>", lambda e: self._trigger_change())

        # 版本
        ctk.CTkLabel(self.smbios_tab, text="版本:", font=CTK_FONT_MAIN, width=120, anchor="w").grid(
            row=2, column=0, padx=10, pady=8, sticky="w"
        )
        self.smbios_version_entry = ctk.CTkEntry(self.smbios_tab, placeholder_text="pc-q35", width=300, font=CTK_FONT_SMALL)
        self.smbios_version_entry.grid(row=2, column=1, padx=10, pady=8, sticky="w")
        self.smbios_version_entry.insert(0, "pc-q35")
        self.smbios_version_entry.bind("<KeyRelease>", lambda e: self._trigger_change())

        # 序列号
        ctk.CTkLabel(self.smbios_tab, text="序列号:", font=CTK_FONT_MAIN, width=120, anchor="w").grid(
            row=3, column=0, padx=10, pady=8, sticky="w"
        )
        self.smbios_serial_entry = ctk.CTkEntry(self.smbios_tab, placeholder_text="自动生成", width=300, font=CTK_FONT_SMALL)
        self.smbios_serial_entry.grid(row=3, column=1, padx=10, pady=8, sticky="w")
        self.smbios_serial_entry.insert(0, "")
        self.smbios_serial_entry.bind("<KeyRelease>", lambda e: self._trigger_change())

        # UUID
        ctk.CTkLabel(self.smbios_tab, text="UUID:", font=CTK_FONT_MAIN, width=120, anchor="w").grid(
            row=4, column=0, padx=10, pady=8, sticky="w"
        )
        self.smbios_uuid_entry = ctk.CTkEntry(self.smbios_tab, placeholder_text="自动生成", width=300, font=CTK_FONT_SMALL)
        self.smbios_uuid_entry.grid(row=4, column=1, padx=10, pady=8, sticky="w")
        self.smbios_uuid_entry.insert(0, "")
        self.smbios_uuid_entry.bind("<KeyRelease>", lambda e: self._trigger_change())

        # SKU
        ctk.CTkLabel(self.smbios_tab, text="SKU:", font=CTK_FONT_MAIN, width=120, anchor="w").grid(
            row=5, column=0, padx=10, pady=8, sticky="w"
        )
        self.smbios_sku_entry = ctk.CTkEntry(self.smbios_tab, placeholder_text="可选", width=300, font=CTK_FONT_SMALL)
        self.smbios_sku_entry.grid(row=5, column=1, padx=10, pady=8, sticky="w")
        self.smbios_sku_entry.insert(0, "")
        self.smbios_sku_entry.bind("<KeyRelease>", lambda e: self._trigger_change())

        # 家族
        ctk.CTkLabel(self.smbios_tab, text="家族:", font=CTK_FONT_MAIN, width=120, anchor="w").grid(
            row=6, column=0, padx=10, pady=8, sticky="w"
        )
        self.smbios_family_entry = ctk.CTkEntry(self.smbios_tab, placeholder_text="可选", width=300, font=CTK_FONT_SMALL)
        self.smbios_family_entry.grid(row=6, column=1, padx=10, pady=8, sticky="w")
        self.smbios_family_entry.insert(0, "")
        self.smbios_family_entry.bind("<KeyRelease>", lambda e: self._trigger_change())

    def _init_custom_tab(self):
        """初始化自定义元数据 Tab."""
        self.custom_tab.grid_columnconfigure(0, weight=1)
        self.custom_tab.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            self.custom_tab,
            text="在此输入自定义 XML 元数据片段:",
            font=CTK_FONT_MAIN,
            text_color="#64b5f6",
        ).grid(row=0, column=0, padx=10, pady=8, sticky="w")

        self.custom_metadata_textbox = ctk.CTkTextbox(
            self.custom_tab,
            font=CTK_FONT_SMALL,
            fg_color=BG_COLOR_CONTENT,
            text_color="#f0f0f0",
            border_color="#333333",
            border_width=1,
            corner_radius=6,
        )
        self.custom_metadata_textbox.grid(row=1, column=0, padx=10, pady=8, sticky="nsew")
        self.custom_metadata_textbox.bind("<KeyRelease>", lambda e: self._trigger_change())

        # 示例按钮
        btn_frame = ctk.CTkFrame(self.custom_tab, fg_color="transparent")
        btn_frame.grid(row=2, column=0, padx=10, pady=8, sticky="w")

        ctk.CTkButton(
            btn_frame,
            text="插入 OVF 示例",
            width=120,
            font=CTK_FONT_SMALL,
            fg_color="transparent",
            border_width=1,
            command=self._insert_ovf_example,
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="清空",
            width=80,
            font=CTK_FONT_SMALL,
            fg_color="#757575",
            hover_color="#616161",
            command=self._clear_custom_metadata,
        ).pack(side="left", padx=5)

    def _insert_ovf_example(self):
        """插入 OVF 环境示例."""
        example = """<ovf:Environment xmlns:ovf="http://schemas.dmtf.org/ovf/environment/1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <ovf:Property ovf:key="hostname" ovf:value="myvm"/>
  <ovf:Property ovf:key="username" ovf:value="admin"/>
</ovf:Environment>"""
        self.custom_metadata_textbox.insert("1.0", example)
        self._trigger_change()

    def _clear_custom_metadata(self):
        """清空自定义元数据."""
        self.custom_metadata_textbox.delete("1.0", ctk.END)
        self._trigger_change()

    def _trigger_change(self, *args):
        """触发变化回调."""
        if self.on_change_callback:
            self.on_change_callback()

    def get_config(self) -> dict:
        """获取配置数据."""
        smbios_config = {
            "vendor": self.smbios_vendor_entry.get().strip(),
            "product": self.smbios_product_entry.get().strip(),
            "version": self.smbios_version_entry.get().strip(),
            "serial": self.smbios_serial_entry.get().strip(),
            "uuid": self.smbios_uuid_entry.get().strip(),
            "sku": self.smbios_sku_entry.get().strip(),
            "family": self.smbios_family_entry.get().strip(),
        }

        custom_metadata = self.custom_metadata_textbox.get("1.0", ctk.END).strip()

        return {
            "smbios": smbios_config,
            "custom_metadata": custom_metadata if custom_metadata else None,
        }

    def to_xml(self) -> dict:
        """生成 XML 配置字典."""
        config = self.get_config()
        result = {}

        # SMBIOS
        smbios = config["smbios"]
        if any(smbios.values()):
            result["smbios_system"] = smbios

        # 自定义元数据
        if config["custom_metadata"]:
            result["custom_metadata"] = config["custom_metadata"]

        return result

    def load_config(self, config: dict):
        """加载配置数据到 UI."""
        if "smbios" in config:
            s = config["smbios"]
            if "vendor" in s:
                self.smbios_vendor_entry.delete(0, ctk.END)
                self.smbios_vendor_entry.insert(0, s["vendor"])
            if "product" in s:
                self.smbios_product_entry.delete(0, ctk.END)
                self.smbios_product_entry.insert(0, s["product"])
            if "version" in s:
                self.smbios_version_entry.delete(0, ctk.END)
                self.smbios_version_entry.insert(0, s["version"])
            if "serial" in s:
                self.smbios_serial_entry.delete(0, ctk.END)
                self.smbios_serial_entry.insert(0, s["serial"])
