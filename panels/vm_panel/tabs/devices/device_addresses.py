"""设备地址模块 - 设备地址配置."""

import customtkinter as ctk

from components.base_tab import BaseConfigTab
from utils.styles import BG_COLOR_CONTENT, CTK_FONT_MAIN, CTK_FONT_SMALL


class DeviceAddressesTab(BaseConfigTab):
    """设备地址配置 Tab - 支持设备地址配置."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, on_change_callback, **kwargs)
        self.address_list = []

        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # 工具栏
        toolbar = ctk.CTkFrame(self, fg_color='transparent')
        toolbar.grid(row=0, column=0, sticky='ew', padx=5, pady=5)

        add_btn = ctk.CTkButton(
            toolbar,
            text='Add Address',
            command=self._add_address,
            fg_color='#4caf50',
            hover_color='#388e3c',
            width=120,
        )
        add_btn.pack(side='left', padx=5)

        clear_btn = ctk.CTkButton(
            toolbar,
            text='Clear List',
            command=self._clear_list,
            fg_color='#f44336',
            hover_color='#d32f2f',
            width=100,
        )
        clear_btn.pack(side='left', padx=5)

        # 内容区域
        self.content_frame = ctk.CTkScrollableFrame(
            self, fg_color=BG_COLOR_CONTENT, corner_radius=6
        )
        self.content_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)

        # 设备列表显示
        self.address_display = ctk.CTkLabel(
            self.content_frame,
            text='暂无设备地址',
            font=CTK_FONT_SMALL,
            text_color='#aaaaaa',
            anchor='w',
        )
        self.address_display.grid(row=0, column=0, sticky='w', padx=10, pady=10)

    def _add_address(self):
        """Add device address configuration dialog."""
        dialog = ctk.CTkToplevel(self)
        dialog.title('Add Device Address')
        dialog.geometry('500x300')
        dialog.transient(self)
        dialog.grab_set()

        DeviceAddressConfigDialog(dialog, self._on_address_added)

    def _on_address_added(self, address_config):
        """设备地址添加完成回调."""
        self.address_list.append(address_config)
        self._update_display()
        self._trigger_change()

    def _clear_list(self):
        """清空设备地址列表."""
        self.address_list.clear()
        self._update_display()
        self._trigger_change()

    def _update_display(self):
        """更新显示."""
        # 清除旧的显示
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        if not self.address_list:
            label = ctk.CTkLabel(
                self.content_frame,
                text='暂无设备地址',
                font=CTK_FONT_SMALL,
                text_color='#aaaaaa',
                anchor='w',
            )
            label.grid(row=0, column=0, sticky='w', padx=10, pady=10)
            return

        # 显示所有设备地址
        for i, address in enumerate(self.address_list):
            addr_frame = ctk.CTkFrame(self.content_frame, fg_color='transparent')
            addr_frame.grid(row=i, column=0, sticky='ew', padx=10, pady=5)

            # 设备地址类型标签
            type_label = f'[{address.get("type", "pci")}]'
            domain = address.get('domain', '')
            bus = address.get('bus', '')
            slot = address.get('slot', '')
            function = address.get('function', '')

            address_text = f'{type_label}: {domain}:{bus}:{slot}.{function}' if type_label == '[pci]' else f'{type_label}: {address.get("address", "")}'

            label = ctk.CTkLabel(
                addr_frame,
                text=address_text,
                font=CTK_FONT_MAIN,
                anchor='w',
            )
            label.grid(row=0, column=0, sticky='w')

            # 删除按钮
            del_btn = ctk.CTkButton(
                addr_frame,
                text='删除',
                width=60,
                fg_color='#f44336',
                hover_color='#d32f2f',
                font=CTK_FONT_SMALL,
                command=lambda idx=i: self._remove_address(idx),
            )
            del_btn.grid(row=0, column=1, padx=10)

    def _remove_address(self, index):
        """删除指定索引的设备地址."""
        self.address_list.pop(index)
        self._update_display()
        self._trigger_change()

    def get_config(self) -> dict:
        """获取配置."""
        return {
            'type': 'device_addresses',
            'addresses': self.address_list.copy(),
        }


class DeviceAddressConfigDialog:
    """设备地址配置对话框."""

    def __init__(self, dialog, on_confirm_callback):
        self.dialog = dialog
        self.on_confirm_callback = on_confirm_callback
        self.config = {}
        self._init_ui()

    def _init_ui(self):
        """初始化 UI."""
        # 基本信息
        info_frame = ctk.CTkFrame(self.dialog, fg_color='transparent')
        info_frame.grid(row=0, column=0, sticky='ew', padx=20, pady=10)
        info_frame.grid_columnconfigure(1, weight=1)

        # Address Type
        ctk.CTkLabel(info_frame, text='Type:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=0, column=0, padx=5, pady=5, sticky='w'
        )
        self.type_menu = ctk.CTkOptionMenu(
            info_frame,
            values=['pci', 'usb', 'virtio', 'scsi', 'ide', 'sata', 'fdc', 'ccid'],
            width=120,
            font=CTK_FONT_SMALL,
            command=self._on_type_changed,
        )
        self.type_menu.set('pci')
        self.type_menu.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        # PCI 地址字段
        self.pci_frame = ctk.CTkFrame(info_frame, fg_color='transparent')
        self.pci_frame.grid(row=1, column=0, columnspan=2, sticky='ew', padx=5, pady=5)
        self.pci_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(self.pci_frame, text='Domain:', font=CTK_FONT_MAIN, width=60, anchor='w').grid(
            row=0, column=0, padx=5, pady=2, sticky='w'
        )
        self.domain_entry = ctk.CTkEntry(
            self.pci_frame,
            placeholder_text='0x0000',
            width=100,
            font=CTK_FONT_SMALL
        )
        self.domain_entry.grid(row=0, column=1, padx=5, pady=2, sticky='w')

        ctk.CTkLabel(self.pci_frame, text='Bus:', font=CTK_FONT_MAIN, width=60, anchor='w').grid(
            row=0, column=2, padx=5, pady=2, sticky='w'
        )
        self.bus_entry = ctk.CTkEntry(
            self.pci_frame,
            placeholder_text='0x00',
            width=80,
            font=CTK_FONT_SMALL
        )
        self.bus_entry.grid(row=0, column=3, padx=5, pady=2, sticky='w')

        ctk.CTkLabel(self.pci_frame, text='Slot:', font=CTK_FONT_MAIN, width=60, anchor='w').grid(
            row=0, column=4, padx=5, pady=2, sticky='w'
        )
        self.slot_entry = ctk.CTkEntry(
            self.pci_frame,
            placeholder_text='0x00',
            width=80,
            font=CTK_FONT_SMALL
        )
        self.slot_entry.grid(row=0, column=5, padx=5, pady=2, sticky='w')

        ctk.CTkLabel(self.pci_frame, text='Function:', font=CTK_FONT_MAIN, width=60, anchor='w').grid(
            row=0, column=6, padx=5, pady=2, sticky='w'
        )
        self.function_entry = ctk.CTkEntry(
            self.pci_frame,
            placeholder_text='0x0',
            width=80,
            font=CTK_FONT_SMALL
        )
        self.function_entry.grid(row=0, column=7, padx=5, pady=2, sticky='w')

        # 其他类型地址字段
        self.other_frame = ctk.CTkFrame(info_frame, fg_color='transparent')
        self.other_frame.grid(row=2, column=0, columnspan=2, sticky='ew', padx=5, pady=5)
        self.other_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(self.other_frame, text='Address:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=0, column=0, padx=5, pady=5, sticky='w'
        )
        self.address_entry = ctk.CTkEntry(
            self.other_frame,
            placeholder_text='Address',
            width=300,
            font=CTK_FONT_SMALL
        )
        self.address_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        # 初始隐藏其他类型地址字段
        self.other_frame.grid_remove()

        # 按钮
        btn_frame = ctk.CTkFrame(self.dialog, fg_color='transparent')
        btn_frame.grid(row=1, column=0, sticky='e', padx=20, pady=10)

        ctk.CTkButton(
            btn_frame,
            text='Cancel',
            command=self.dialog.destroy,
            width=80,
            fg_color='#9e9e9e',
            hover_color='#757575',
        ).pack(side='right', padx=5)

        ctk.CTkButton(
            btn_frame,
            text='OK',
            command=self._confirm,
            width=80,
            fg_color='#4caf50',
            hover_color='#388e3c',
        ).pack(side='right', padx=5)

    def _on_type_changed(self, new_type):
        """类型改变."""
        if new_type == 'pci':
            self.pci_frame.grid()
            self.other_frame.grid_remove()
        else:
            self.pci_frame.grid_remove()
            self.other_frame.grid()

    def _confirm(self):
        """确认添加."""
        address_type = self.type_menu.get()

        if address_type == 'pci':
            config = {
                'type': address_type,
                'domain': self.domain_entry.get().strip(),
                'bus': self.bus_entry.get().strip(),
                'slot': self.slot_entry.get().strip(),
                'function': self.function_entry.get().strip(),
            }
        else:
            config = {
                'type': address_type,
                'address': self.address_entry.get().strip(),
            }

        self.on_confirm_callback(config)
        self.dialog.destroy()
