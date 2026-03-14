"""模块 6: 其他设备 - 图形、视频、USB、串口、TPM、声音等."""

import customtkinter as ctk

from ..styles import BG_COLOR_CONTENT, CTK_FONT_MAIN, CTK_FONT_SMALL


class DevicesModule(ctk.CTkFrame):
    """其他设备模块."""

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
        self.graphics_tab = self.tabview.add("图形显示")
        self.video_tab = self.tabview.add("视频设备")
        self.usb_tab = self.tabview.add("USB/串口")
        self.input_tab = self.tabview.add("输入/声音")

        # 初始化 UI
        self._init_graphics_tab()
        self._init_video_tab()
        self._init_usb_tab()
        self._init_input_tab()

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

    def _init_usb_tab(self):
        """初始化 USB/串口 Tab."""
        self.usb_tab.grid_columnconfigure(0, weight=1)
        self.usb_tab.grid_columnconfigure(1, weight=1)

        # USB 控制器类型
        ctk.CTkLabel(self.usb_tab, text="USB 控制器:", font=CTK_FONT_MAIN, width=120, anchor="w").grid(
            row=0, column=0, padx=10, pady=8, sticky="w"
        )
        self.usb_controller_combo = ctk.CTkOptionMenu(
            self.usb_tab,
            values=["qemu-xhci", "piix3-uhci", "piix4-uhci", "nec-xhci", "ich9-ehci1", "none"],
            width=150, font=CTK_FONT_SMALL,
            command=lambda *args: self._trigger_change()
        )
        self.usb_controller_combo.set("qemu-xhci")
        self.usb_controller_combo.grid(row=0, column=1, padx=10, pady=8, sticky="w")

        # 禁用 USB
        self.disable_usb_check = ctk.CTkCheckBox(
            self.usb_tab, text="禁用 USB 支持", font=CTK_FONT_SMALL
        )
        self.disable_usb_check.grid(row=1, column=0, columnspan=2, padx=10, pady=8, sticky="w")
        self.disable_usb_check.configure(command=self._trigger_change)

        # 分隔线
        separator = ctk.CTkFrame(self.usb_tab, height=2, fg_color="#444444")
        separator.grid(row=2, column=0, columnspan=2, padx=10, pady=15, sticky="ew")

        # 串口类型
        ctk.CTkLabel(self.usb_tab, text="串口类型:", font=CTK_FONT_MAIN, width=120, anchor="w").grid(
            row=3, column=0, padx=10, pady=8, sticky="w"
        )
        self.serial_type_combo = ctk.CTkOptionMenu(
            self.usb_tab, values=["pty", "stdio", "file", "tcp", "udp", "unix", "spicevmc", "none"],
            width=150, font=CTK_FONT_SMALL,
            command=lambda *args: self._trigger_change()
        )
        self.serial_type_combo.set("pty")
        self.serial_type_combo.grid(row=3, column=1, padx=10, pady=8, sticky="w")

        # 串口端口
        ctk.CTkLabel(self.usb_tab, text="端口号:", font=CTK_FONT_MAIN, width=120, anchor="w").grid(
            row=4, column=0, padx=10, pady=8, sticky="w"
        )
        self.serial_port_entry = ctk.CTkEntry(self.usb_tab, width=100, font=CTK_FONT_SMALL)
        self.serial_port_entry.grid(row=4, column=1, padx=10, pady=8, sticky="w")
        self.serial_port_entry.insert(0, "0")
        self.serial_port_entry.bind("<KeyRelease>", lambda e: self._trigger_change())

    def _init_input_tab(self):
        """初始化输入/声音 Tab."""
        self.input_tab.grid_columnconfigure(0, weight=1)
        self.input_tab.grid_columnconfigure(1, weight=1)

        # TPM 模型
        ctk.CTkLabel(self.input_tab, text="TPM 模型:", font=CTK_FONT_MAIN, width=120, anchor="w").grid(
            row=0, column=0, padx=10, pady=8, sticky="w"
        )
        self.tpm_model_combo = ctk.CTkOptionMenu(
            self.input_tab, values=["tpm-crb", "tpm-tis", "tpm-spapr", "none"],
            width=150, font=CTK_FONT_SMALL,
            command=lambda *args: self._trigger_change()
        )
        self.tpm_model_combo.set("tpm-crb")
        self.tpm_model_combo.grid(row=0, column=1, padx=10, pady=8, sticky="w")

        # TPM 版本
        ctk.CTkLabel(self.input_tab, text="TPM 版本:", font=CTK_FONT_MAIN, width=120, anchor="w").grid(
            row=1, column=0, padx=10, pady=8, sticky="w"
        )
        self.tpm_version_combo = ctk.CTkOptionMenu(
            self.input_tab, values=["1.2", "2.0"], width=100, font=CTK_FONT_SMALL,
            command=lambda *args: self._trigger_change()
        )
        self.tpm_version_combo.set("2.0")
        self.tpm_version_combo.grid(row=1, column=1, padx=10, pady=8, sticky="w")

        # 禁用声音
        self.disable_sound_check = ctk.CTkCheckBox(
            self.input_tab, text="禁用声音设备", font=CTK_FONT_SMALL
        )
        self.disable_sound_check.grid(row=2, column=0, columnspan=2, padx=10, pady=8, sticky="w")
        self.disable_sound_check.configure(command=self._trigger_change)

        # 音频模型
        ctk.CTkLabel(self.input_tab, text="音频模型:", font=CTK_FONT_MAIN, width=120, anchor="w").grid(
            row=3, column=0, padx=10, pady=8, sticky="w"
        )
        self.audio_model_combo = ctk.CTkOptionMenu(
            self.input_tab, values=["ich9", "ich6", "ac97", "virtio", "pcspk"],
            width=150, font=CTK_FONT_SMALL,
            command=lambda *args: self._trigger_change()
        )
        self.audio_model_combo.set("ich9")
        self.audio_model_combo.grid(row=3, column=1, padx=10, pady=8, sticky="w")

        # 键盘
        ctk.CTkLabel(self.input_tab, text="键盘:", font=CTK_FONT_MAIN, width=120, anchor="w").grid(
            row=4, column=0, padx=10, pady=8, sticky="w"
        )
        self.keyboard_combo = ctk.CTkOptionMenu(
            self.input_tab, values=["virtio", "ps2", "usb", "none"],
            width=150, font=CTK_FONT_SMALL,
            command=lambda *args: self._trigger_change()
        )
        self.keyboard_combo.set("virtio")
        self.keyboard_combo.grid(row=4, column=1, padx=10, pady=8, sticky="w")

        # 鼠标
        ctk.CTkLabel(self.input_tab, text="鼠标:", font=CTK_FONT_MAIN, width=120, anchor="w").grid(
            row=5, column=0, padx=10, pady=8, sticky="w"
        )
        self.mouse_combo = ctk.CTkOptionMenu(
            self.input_tab, values=["virtio", "ps2", "usb", "tablet"],
            width=150, font=CTK_FONT_SMALL,
            command=lambda *args: self._trigger_change()
        )
        self.mouse_combo.set("tablet")
        self.mouse_combo.grid(row=5, column=1, padx=10, pady=8, sticky="w")

    def _trigger_change(self, *args):
        """触发变化回调."""
        if self.on_change_callback:
            self.on_change_callback()

    def get_config(self) -> dict:
        """获取配置数据."""
        return {
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

        if "video" in config:
            v = config["video"]
            if "model" in v:
                self.video_model_combo.set(v["model"])
            if "vram" in v:
                self.vram_entry.delete(0, ctk.END)
                self.vram_entry.insert(0, str(v["vram"]))
