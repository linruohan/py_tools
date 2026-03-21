"""设备租约模块 - 设备租约配置."""

import customtkinter as ctk

from components.base_tab import BaseConfigTab
from utils.styles import BG_COLOR_CONTENT, CTK_FONT_MAIN, CTK_FONT_SMALL


class DeviceLeasesTab(BaseConfigTab):
    """设备租约配置 Tab - 支持设备租约配置."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, on_change_callback, **kwargs)
        self.lease_list = []

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
            text='Add Lease',
            command=self._add_lease,
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
        self.lease_display = ctk.CTkLabel(
            self.content_frame,
            text='暂无设备租约',
            font=CTK_FONT_SMALL,
            text_color='#aaaaaa',
            anchor='w',
        )
        self.lease_display.grid(row=0, column=0, sticky='w', padx=10, pady=10)

    def _add_lease(self):
        """Add device lease configuration dialog."""
        dialog = ctk.CTkToplevel(self)
        dialog.title('Add Device Lease')
        dialog.geometry('500x300')
        dialog.transient(self)
        dialog.grab_set()

        DeviceLeaseConfigDialog(dialog, self._on_lease_added)

    def _on_lease_added(self, lease_config):
        """设备租约添加完成回调."""
        self.lease_list.append(lease_config)
        self._update_display()
        self._trigger_change()

    def _clear_list(self):
        """清空设备租约列表."""
        self.lease_list.clear()
        self._update_display()
        self._trigger_change()

    def _update_display(self):
        """更新显示."""
        # 清除旧的显示
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        if not self.lease_list:
            label = ctk.CTkLabel(
                self.content_frame,
                text='暂无设备租约',
                font=CTK_FONT_SMALL,
                text_color='#aaaaaa',
                anchor='w',
            )
            label.grid(row=0, column=0, sticky='w', padx=10, pady=10)
            return

        # 显示所有设备租约
        for i, lease in enumerate(self.lease_list):
            lease_frame = ctk.CTkFrame(self.content_frame, fg_color='transparent')
            lease_frame.grid(row=i, column=0, sticky='ew', padx=10, pady=5)

            # 设备租约类型标签
            type_label = f'[{lease.get("type", "iscsi")}]'
            target = lease.get('target', '')
            initiator = lease.get('initiator', '')

            lease_text = f'{type_label}: {target} -> {initiator}'

            label = ctk.CTkLabel(
                lease_frame,
                text=lease_text,
                font=CTK_FONT_MAIN,
                anchor='w',
            )
            label.grid(row=0, column=0, sticky='w')

            # 删除按钮
            del_btn = ctk.CTkButton(
                lease_frame,
                text='删除',
                width=60,
                fg_color='#f44336',
                hover_color='#d32f2f',
                font=CTK_FONT_SMALL,
                command=lambda idx=i: self._remove_lease(idx),
            )
            del_btn.grid(row=0, column=1, padx=10)

    def _remove_lease(self, index):
        """删除指定索引的设备租约."""
        self.lease_list.pop(index)
        self._update_display()
        self._trigger_change()

    def get_config(self) -> dict:
        """获取配置."""
        return {
            'type': 'device_leases',
            'leases': self.lease_list.copy(),
        }

    def load_config(self, config: dict) -> None:
        """加载配置."""
        if 'leases' in config:
            self.lease_list = config['leases'].copy()
            self._update_display()


class DeviceLeaseConfigDialog:
    """设备租约配置对话框."""

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

        # Lease Type
        ctk.CTkLabel(info_frame, text='Type:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=0, column=0, padx=5, pady=5, sticky='w'
        )
        self.type_menu = ctk.CTkOptionMenu(
            info_frame,
            values=['iscsi', 'fc', 'scsi'],
            width=100,
            font=CTK_FONT_SMALL,
        )
        self.type_menu.set('iscsi')
        self.type_menu.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        # Target
        ctk.CTkLabel(info_frame, text='Target:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=1, column=0, padx=5, pady=5, sticky='w'
        )
        self.target_entry = ctk.CTkEntry(
            info_frame,
            placeholder_text='iqn.2003-01.org.linux-iscsi.test:target1',
            width=300,
            font=CTK_FONT_SMALL,
        )
        self.target_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        # Initiator
        ctk.CTkLabel(info_frame, text='Initiator:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=2, column=0, padx=5, pady=5, sticky='w'
        )
        self.initiator_entry = ctk.CTkEntry(
            info_frame,
            placeholder_text='iqn.2003-01.org.linux-iscsi.test:initiator1',
            width=300,
            font=CTK_FONT_SMALL,
        )
        self.initiator_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')

        # Address
        ctk.CTkLabel(info_frame, text='Address:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=3, column=0, padx=5, pady=5, sticky='w'
        )
        self.address_entry = ctk.CTkEntry(
            info_frame, placeholder_text='192.168.1.1', width=150, font=CTK_FONT_SMALL
        )
        self.address_entry.grid(row=3, column=1, padx=5, pady=5, sticky='w')

        # Port
        ctk.CTkLabel(info_frame, text='Port:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=4, column=0, padx=5, pady=5, sticky='w'
        )
        self.port_entry = ctk.CTkEntry(
            info_frame, placeholder_text='3260', width=100, font=CTK_FONT_SMALL
        )
        self.port_entry.grid(row=4, column=1, padx=5, pady=5, sticky='w')

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

    def _confirm(self):
        """确认添加."""
        lease_type = self.type_menu.get()

        config = {
            'type': lease_type,
            'target': self.target_entry.get().strip(),
            'initiator': self.initiator_entry.get().strip(),
            'address': self.address_entry.get().strip(),
            'port': self.port_entry.get().strip(),
        }

        self.on_confirm_callback(config)
        self.dialog.destroy()
