"""网络接口模块 - 包括各种网络连接类型和配置选项"""

import customtkinter as ctk

from components.base_tab import BaseConfigTab
from utils.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class NetworkInterfacesTab(BaseConfigTab):
    """网络接口配置主tab"""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, on_change_callback, **kwargs)
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面"""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            frame, text='Network Interfaces', font=CTK_FONT_BOLD, text_color='#2196f3'
        ).grid(row=0, column=0, padx=10, pady=5, sticky='w')

        ctk.CTkLabel(
            frame,
            text='网络接口配置允许为虚拟机设置各种网络连接类型.\n'
            '支持虚拟网络、桥接、用户空间连接等多种网络类型.',
            font=CTK_FONT_SMALL,
            text_color='#666666',
        ).grid(row=1, column=0, padx=10, pady=5, sticky='w')


class VirtualNetworkTab(BaseConfigTab):
    """虚拟网络配置"""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, on_change_callback, **kwargs)
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面"""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(frame, text='Virtual Network', font=CTK_FONT_BOLD, text_color='#2196f3').grid(
            row=0, column=0, columnspan=4, padx=10, pady=5, sticky='w'
        )

        # Network Name
        ctk.CTkLabel(frame, text='Network Name:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.network_name = ctk.CTkEntry(
            frame, placeholder_text='default', width=150, font=CTK_FONT_SMALL
        )
        self.network_name.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.network_name.bind('<KeyRelease>', lambda e: self._trigger_change())

        # MAC Address
        ctk.CTkLabel(frame, text='MAC Address:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.mac_address = ctk.CTkEntry(
            frame, placeholder_text='52:54:00:12:34:56', width=150, font=CTK_FONT_SMALL
        )
        self.mac_address.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.mac_address.bind('<KeyRelease>', lambda e: self._trigger_change())

    def get_config(self) -> dict:
        """获取配置"""
        return {
            'type': 'network',
            'source': 'network',
            'network': self.network_name.get().strip() or 'default',
            'mac': self.mac_address.get().strip(),
        }


class BridgeToLANTab(BaseConfigTab):
    """桥接到LAN配置"""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, on_change_callback, **kwargs)
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面"""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(frame, text='Bridge to LAN', font=CTK_FONT_BOLD, text_color='#4caf50').grid(
            row=0, column=0, columnspan=4, padx=10, pady=5, sticky='w'
        )

        # Bridge Name
        ctk.CTkLabel(frame, text='Bridge Name:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.bridge_name = ctk.CTkEntry(
            frame, placeholder_text='br0', width=150, font=CTK_FONT_SMALL
        )
        self.bridge_name.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.bridge_name.bind('<KeyRelease>', lambda e: self._trigger_change())

        # MAC Address
        ctk.CTkLabel(frame, text='MAC Address:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.mac_address = ctk.CTkEntry(
            frame, placeholder_text='52:54:00:12:34:56', width=150, font=CTK_FONT_SMALL
        )
        self.mac_address.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.mac_address.bind('<KeyRelease>', lambda e: self._trigger_change())

    def get_config(self) -> dict:
        """获取配置"""
        return {
            'type': 'network',
            'source': 'bridge',
            'bridge': self.bridge_name.get().strip() or 'br0',
            'mac': self.mac_address.get().strip(),
        }


class SLIRPConnectionTab(BaseConfigTab):
    """使用SLIRP的用户空间连接配置"""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, on_change_callback, **kwargs)
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面"""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            frame, text='Userspace connection using SLIRP', font=CTK_FONT_BOLD, text_color='#ff9800'
        ).grid(row=0, column=0, columnspan=4, padx=10, pady=5, sticky='w')

        # MAC Address
        ctk.CTkLabel(frame, text='MAC Address:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.mac_address = ctk.CTkEntry(
            frame, placeholder_text='52:54:00:12:34:56', width=150, font=CTK_FONT_SMALL
        )
        self.mac_address.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.mac_address.bind('<KeyRelease>', lambda e: self._trigger_change())

        # MTU
        ctk.CTkLabel(frame, text='MTU:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.mtu = ctk.CTkEntry(frame, placeholder_text='1500', width=100, font=CTK_FONT_SMALL)
        self.mtu.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.mtu.bind('<KeyRelease>', lambda e: self._trigger_change())

    def get_config(self) -> dict:
        """获取配置"""
        return {
            'type': 'network',
            'source': 'user',
            'mac': self.mac_address.get().strip(),
            'mtu': self.mtu.get().strip() or '1500',
        }


class PasstConnectionTab(BaseConfigTab):
    """使用passt的用户空间连接配置"""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, on_change_callback, **kwargs)
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面"""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            frame, text='Userspace connection using passt', font=CTK_FONT_BOLD, text_color='#9c27b0'
        ).grid(row=0, column=0, columnspan=4, padx=10, pady=5, sticky='w')

        # MAC Address
        ctk.CTkLabel(frame, text='MAC Address:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.mac_address = ctk.CTkEntry(
            frame, placeholder_text='52:54:00:12:34:56', width=150, font=CTK_FONT_SMALL
        )
        self.mac_address.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.mac_address.bind('<KeyRelease>', lambda e: self._trigger_change())

        # Passt Arguments
        ctk.CTkLabel(frame, text='Passt Args:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.passt_args = ctk.CTkEntry(
            frame, placeholder_text='--mtu=1500', width=200, font=CTK_FONT_SMALL
        )
        self.passt_args.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.passt_args.bind('<KeyRelease>', lambda e: self._trigger_change())

    def get_config(self) -> dict:
        """获取配置"""
        return {
            'type': 'network',
            'source': 'passt',
            'mac': self.mac_address.get().strip(),
            'passt_args': self.passt_args.get().strip(),
        }


class DirectAttachmentTab(BaseConfigTab):
    """直接附加到物理接口配置"""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, on_change_callback, **kwargs)
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面"""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            frame,
            text='Direct attachment to physical interface',
            font=CTK_FONT_BOLD,
            text_color='#ff5722',
        ).grid(row=0, column=0, columnspan=4, padx=10, pady=5, sticky='w')

        # Interface Name
        ctk.CTkLabel(frame, text='Interface:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.interface = ctk.CTkEntry(
            frame, placeholder_text='eth0', width=150, font=CTK_FONT_SMALL
        )
        self.interface.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.interface.bind('<KeyRelease>', lambda e: self._trigger_change())

        # MAC Address
        ctk.CTkLabel(frame, text='MAC Address:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.mac_address = ctk.CTkEntry(
            frame, placeholder_text='52:54:00:12:34:56', width=150, font=CTK_FONT_SMALL
        )
        self.mac_address.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.mac_address.bind('<KeyRelease>', lambda e: self._trigger_change())

    def get_config(self) -> dict:
        """获取配置"""
        return {
            'type': 'network',
            'source': 'direct',
            'dev': self.interface.get().strip() or 'eth0',
            'mac': self.mac_address.get().strip(),
        }


class PCIPassthroughTab(BaseConfigTab):
    """PCI Passthrough网络配置"""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, on_change_callback, **kwargs)
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面"""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(frame, text='PCI Passthrough', font=CTK_FONT_BOLD, text_color='#795548').grid(
            row=0, column=0, columnspan=4, padx=10, pady=5, sticky='w'
        )

        # PCI Address
        ctk.CTkLabel(frame, text='PCI Address:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.pci_address = ctk.CTkEntry(
            frame, placeholder_text='0000:00:00.0', width=150, font=CTK_FONT_SMALL
        )
        self.pci_address.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.pci_address.bind('<KeyRelease>', lambda e: self._trigger_change())

        # ROM BAR
        ctk.CTkLabel(frame, text='ROM BAR:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.rom_bar = ctk.CTkOptionMenu(
            frame,
            values=['on', 'off'],
            width=100,
            font=CTK_FONT_SMALL,
            command=self._trigger_change,
        )
        self.rom_bar.set('off')
        self.rom_bar.grid(row=2, column=1, padx=5, pady=5, sticky='w')

    def get_config(self) -> dict:
        """获取配置"""
        return {
            'type': 'network',
            'source': 'hostdev',
            'pci_address': self.pci_address.get().strip(),
            'rom_bar': self.rom_bar.get(),
        }


class NetworkQoSTab(BaseConfigTab):
    """网络服务质量配置"""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, on_change_callback, **kwargs)
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面"""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            frame, text='Quality of service', font=CTK_FONT_BOLD, text_color='#607d8b'
        ).grid(row=0, column=0, columnspan=4, padx=10, pady=5, sticky='w')

        # Bandwidth Limit
        ctk.CTkLabel(
            frame, text='Bandwidth Limit:', font=CTK_FONT_MAIN, width=100, anchor='w'
        ).grid(row=1, column=0, padx=10, pady=5, sticky='w')
        self.bandwidth = ctk.CTkEntry(
            frame, placeholder_text='1024', width=100, font=CTK_FONT_SMALL
        )
        self.bandwidth.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.bandwidth.bind('<KeyRelease>', lambda e: self._trigger_change())

        # Unit
        ctk.CTkLabel(frame, text='Unit:', font=CTK_FONT_MAIN, width=50, anchor='w').grid(
            row=1, column=2, padx=5, pady=5, sticky='w'
        )
        self.bandwidth_unit = ctk.CTkOptionMenu(
            frame,
            values=['kbps', 'mbps', 'gbps'],
            width=80,
            font=CTK_FONT_SMALL,
            command=self._trigger_change,
        )
        self.bandwidth_unit.set('mbps')
        self.bandwidth_unit.grid(row=1, column=3, padx=5, pady=5, sticky='w')

    def get_config(self) -> dict:
        """获取配置"""
        return {
            'type': 'qos',
            'bandwidth': self.bandwidth.get().strip(),
            'unit': self.bandwidth_unit.get(),
        }
