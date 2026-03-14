"""SMBIOS 系统信息配置 Tab - BIOS、系统、主板、机箱信息."""

from typing import ClassVar

import customtkinter as ctk

from components.inner_tab_panel import InnerTabPanel
from components.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN


class BIOSInfoSubTab(ctk.CTkFrame):
    """BIOS 信息子 Tab."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent')
        self.on_change_callback = on_change_callback

        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        frame.grid(row=0, column=0, columnspan=2, sticky='nsew', padx=5, pady=5)
        frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            frame, text='BIOS 信息 (SMBIOS Block 0)', font=CTK_FONT_BOLD, text_color='#64b5f6'
        ).grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w')

        ctk.CTkLabel(frame, text='厂商:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.vendor = ctk.CTkEntry(frame, placeholder_text='LENOVO', width=200)
        self.vendor.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.vendor.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(frame, text='版本:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.version = ctk.CTkEntry(frame, placeholder_text='BIOS 版本', width=200)
        self.version.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.version.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(frame, text='日期:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=3, column=0, padx=10, pady=5, sticky='w'
        )
        self.date = ctk.CTkEntry(frame, placeholder_text='mm/dd/yyyy', width=200)
        self.date.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        self.date.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(frame, text='发布版本:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=4, column=0, padx=10, pady=5, sticky='w'
        )
        self.release = ctk.CTkEntry(frame, placeholder_text='10.22', width=200)
        self.release.grid(row=4, column=1, padx=5, pady=5, sticky='w')
        self.release.bind('<KeyRelease>', lambda e: self._trigger_change())

    def _trigger_change(self, *args):
        """触发变化回调."""
        if self.on_change_callback:
            self.on_change_callback()

    def get_config(self) -> dict:
        """获取配置数据."""
        return {
            'vendor': self.vendor.get().strip(),
            'version': self.version.get().strip(),
            'date': self.date.get().strip(),
            'release': self.release.get().strip(),
        }


class SystemInfoSubTab(ctk.CTkFrame):
    """系统信息子 Tab."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent')
        self.on_change_callback = on_change_callback

        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        frame.grid(row=0, column=0, columnspan=2, sticky='nsew', padx=5, pady=5)
        frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            frame, text='系统信息 (SMBIOS Block 1)', font=CTK_FONT_BOLD, text_color='#4caf50'
        ).grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w')

        ctk.CTkLabel(frame, text='制造商:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.manufacturer = ctk.CTkEntry(frame, placeholder_text='Fedora', width=200)
        self.manufacturer.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.manufacturer.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(frame, text='产品名:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.product = ctk.CTkEntry(frame, placeholder_text='Virt-Manager', width=200)
        self.product.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.product.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(frame, text='版本:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=3, column=0, padx=10, pady=5, sticky='w'
        )
        self.version = ctk.CTkEntry(frame, placeholder_text='0.9.4', width=200)
        self.version.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        self.version.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(frame, text='序列号:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=4, column=0, padx=10, pady=5, sticky='w'
        )
        self.serial = ctk.CTkEntry(frame, placeholder_text='序列号', width=200)
        self.serial.grid(row=4, column=1, padx=5, pady=5, sticky='w')
        self.serial.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(frame, text='UUID:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=5, column=0, padx=10, pady=5, sticky='w'
        )
        self.uuid = ctk.CTkEntry(frame, placeholder_text='自动生成', width=200)
        self.uuid.grid(row=5, column=1, padx=5, pady=5, sticky='w')
        self.uuid.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(frame, text='SKU:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=6, column=0, padx=10, pady=5, sticky='w'
        )
        self.sku = ctk.CTkEntry(frame, placeholder_text='SKU 编号', width=200)
        self.sku.grid(row=6, column=1, padx=5, pady=5, sticky='w')
        self.sku.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(frame, text='家族:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=7, column=0, padx=10, pady=5, sticky='w'
        )
        self.family = ctk.CTkEntry(frame, placeholder_text='产品家族', width=200)
        self.family.grid(row=7, column=1, padx=5, pady=5, sticky='w')
        self.family.bind('<KeyRelease>', lambda e: self._trigger_change())

    def _trigger_change(self, *args):
        """触发变化回调."""
        if self.on_change_callback:
            self.on_change_callback()

    def get_config(self) -> dict:
        """获取配置数据."""
        return {
            'manufacturer': self.manufacturer.get().strip(),
            'product': self.product.get().strip(),
            'version': self.version.get().strip(),
            'serial': self.serial.get().strip(),
            'uuid': self.uuid.get().strip(),
            'sku': self.sku.get().strip(),
            'family': self.family.get().strip(),
        }


class BaseBoardSubTab(ctk.CTkFrame):
    """主板信息子 Tab."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent')
        self.on_change_callback = on_change_callback

        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        frame.grid(row=0, column=0, columnspan=2, sticky='nsew', padx=5, pady=5)
        frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            frame, text='主板信息 (SMBIOS Block 2)', font=CTK_FONT_BOLD, text_color='#ff9800'
        ).grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w')

        ctk.CTkLabel(frame, text='制造商:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.manufacturer = ctk.CTkEntry(frame, placeholder_text='LENOVO', width=200)
        self.manufacturer.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.manufacturer.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(frame, text='产品名:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.product = ctk.CTkEntry(frame, placeholder_text='20BE0061MC', width=200)
        self.product.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.product.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(frame, text='版本:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=3, column=0, padx=10, pady=5, sticky='w'
        )
        self.version = ctk.CTkEntry(frame, placeholder_text='0B98401 Pro', width=200)
        self.version.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        self.version.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(frame, text='序列号:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=4, column=0, padx=10, pady=5, sticky='w'
        )
        self.serial = ctk.CTkEntry(frame, placeholder_text='W1KS427111E', width=200)
        self.serial.grid(row=4, column=1, padx=5, pady=5, sticky='w')
        self.serial.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(frame, text='资产标签:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=5, column=0, padx=10, pady=5, sticky='w'
        )
        self.asset = ctk.CTkEntry(frame, placeholder_text='资产标签', width=200)
        self.asset.grid(row=5, column=1, padx=5, pady=5, sticky='w')
        self.asset.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(frame, text='位置:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=6, column=0, padx=10, pady=5, sticky='w'
        )
        self.location = ctk.CTkEntry(frame, placeholder_text='机箱位置', width=200)
        self.location.grid(row=6, column=1, padx=5, pady=5, sticky='w')
        self.location.bind('<KeyRelease>', lambda e: self._trigger_change())

    def _trigger_change(self, *args):
        """触发变化回调."""
        if self.on_change_callback:
            self.on_change_callback()

    def get_config(self) -> dict:
        """获取配置数据."""
        return {
            'manufacturer': self.manufacturer.get().strip(),
            'product': self.product.get().strip(),
            'version': self.version.get().strip(),
            'serial': self.serial.get().strip(),
            'asset': self.asset.get().strip(),
            'location': self.location.get().strip(),
        }


class ChassisSubTab(ctk.CTkFrame):
    """机箱信息子 Tab."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent')
        self.on_change_callback = on_change_callback

        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        frame.grid(row=0, column=0, columnspan=2, sticky='nsew', padx=5, pady=5)
        frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            frame, text='机箱信息 (SMBIOS Block 3)', font=CTK_FONT_BOLD, text_color='#9c27b0'
        ).grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w')

        ctk.CTkLabel(frame, text='制造商:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.manufacturer = ctk.CTkEntry(frame, placeholder_text='Dell Inc.', width=200)
        self.manufacturer.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.manufacturer.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(frame, text='版本:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.version = ctk.CTkEntry(frame, placeholder_text='2.12', width=200)
        self.version.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.version.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(frame, text='序列号:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=3, column=0, padx=10, pady=5, sticky='w'
        )
        self.serial = ctk.CTkEntry(frame, placeholder_text='65X0XF2', width=200)
        self.serial.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        self.serial.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(frame, text='资产标签:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=4, column=0, padx=10, pady=5, sticky='w'
        )
        self.asset = ctk.CTkEntry(frame, placeholder_text='40000101', width=200)
        self.asset.grid(row=4, column=1, padx=5, pady=5, sticky='w')
        self.asset.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(frame, text='SKU:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=5, column=0, padx=10, pady=5, sticky='w'
        )
        self.sku = ctk.CTkEntry(frame, placeholder_text='Type3Sku1', width=200)
        self.sku.grid(row=5, column=1, padx=5, pady=5, sticky='w')
        self.sku.bind('<KeyRelease>', lambda e: self._trigger_change())

    def _trigger_change(self, *args):
        """触发变化回调."""
        if self.on_change_callback:
            self.on_change_callback()

    def get_config(self) -> dict:
        """获取配置数据."""
        return {
            'manufacturer': self.manufacturer.get().strip(),
            'version': self.version.get().strip(),
            'serial': self.serial.get().strip(),
            'asset': self.asset.get().strip(),
            'sku': self.sku.get().strip(),
        }


class SMBIOSSystemTab(ctk.CTkFrame):
    """SMBIOS 系统信息配置 Tab."""

    SUB_TABS_CONFIG: ClassVar[dict] = {
        'bios': {
            'name': 'BIOS',
            'class': BIOSInfoSubTab,
            'default': True,
        },
        'system': {
            'name': '系统',
            'class': SystemInfoSubTab,
            'default': False,
        },
        'baseboard': {
            'name': '主板',
            'class': BaseBoardSubTab,
            'default': False,
        },
        'chassis': {
            'name': '机箱',
            'class': ChassisSubTab,
            'default': False,
        },
    }

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent')
        self.on_change_callback = on_change_callback

        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.inner_panel = InnerTabPanel(
            self,
            tabs_config=self.SUB_TABS_CONFIG,
            on_change_callback=self.on_change_callback,
        )
        self.inner_panel.grid(row=0, column=0, sticky='nsew')

    def get_config(self) -> dict:
        """获取配置数据."""
        return self.inner_panel.collect_data()

    def to_xml(self) -> dict:
        """生成XML配置字典."""
        return {'smbios_system': self.get_config()}
