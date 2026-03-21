"""控制器设备模块 - 控制器配置."""

import customtkinter as ctk

from components.base_tab import BaseConfigTab
from utils.styles import BG_COLOR_CONTENT, CTK_FONT_MAIN, CTK_FONT_SMALL


class ControllersTab(BaseConfigTab):
    """控制器配置 Tab - 支持各种控制器配置."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, on_change_callback, **kwargs)
        self.controller_list = []

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
            text='Add Controller',
            command=self._add_controller,
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
        self.controller_display = ctk.CTkLabel(
            self.content_frame,
            text='暂无控制器',
            font=CTK_FONT_SMALL,
            text_color='#aaaaaa',
            anchor='w',
        )
        self.controller_display.grid(row=0, column=0, sticky='w', padx=10, pady=10)

    def _add_controller(self):
        """Add controller configuration dialog."""
        dialog = ctk.CTkToplevel(self)
        dialog.title('Add Controller')
        dialog.geometry('500x300')
        dialog.transient(self)
        dialog.grab_set()

        ControllerConfigDialog(dialog, self._on_controller_added)

    def _on_controller_added(self, controller_config):
        """控制器添加完成回调."""
        self.controller_list.append(controller_config)
        self._update_display()
        self._trigger_change()

    def _clear_list(self):
        """清空控制器列表."""
        self.controller_list.clear()
        self._update_display()
        self._trigger_change()

    def _update_display(self):
        """更新显示."""
        # 清除旧的显示
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        if not self.controller_list:
            label = ctk.CTkLabel(
                self.content_frame,
                text='暂无控制器',
                font=CTK_FONT_SMALL,
                text_color='#aaaaaa',
                anchor='w',
            )
            label.grid(row=0, column=0, sticky='w', padx=10, pady=10)
            return

        # 显示所有控制器
        for i, controller in enumerate(self.controller_list):
            ctrl_frame = ctk.CTkFrame(self.content_frame, fg_color='transparent')
            ctrl_frame.grid(row=i, column=0, sticky='ew', padx=10, pady=5)

            # 控制器类型标签
            type_label = f'[{controller.get("type", "pci")}]'
            model = controller.get('model', '')
            index = controller.get('index', '')

            controller_text = f'{type_label}: {model}'
            if index:
                controller_text += f' (Index: {index})'

            label = ctk.CTkLabel(
                ctrl_frame,
                text=controller_text,
                font=CTK_FONT_MAIN,
                anchor='w',
            )
            label.grid(row=0, column=0, sticky='w')

            # 删除按钮
            del_btn = ctk.CTkButton(
                ctrl_frame,
                text='删除',
                width=60,
                fg_color='#f44336',
                hover_color='#d32f2f',
                font=CTK_FONT_SMALL,
                command=lambda idx=i: self._remove_controller(idx),
            )
            del_btn.grid(row=0, column=1, padx=10)

    def _remove_controller(self, index):
        """删除指定索引的控制器."""
        self.controller_list.pop(index)
        self._update_display()
        self._trigger_change()

    def get_config(self) -> dict:
        """获取配置."""
        return {
            'type': 'controllers',
            'controllers': self.controller_list.copy(),
        }

    def load_config(self, config: dict) -> None:
        """加载配置."""
        if 'controllers' in config:
            self.controller_list = config['controllers'].copy()
            self._update_display()


class ControllerConfigDialog:
    """控制器配置对话框."""

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

        # Controller Type
        ctk.CTkLabel(info_frame, text='Type:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=0, column=0, padx=5, pady=5, sticky='w'
        )
        self.type_menu = ctk.CTkOptionMenu(
            info_frame,
            values=[
                'pci',
                'usb',
                'scsi',
                'ide',
                'sata',
                'fdc',
                'ccid',
                'virtio-serial',
                'virtio-blk',
                'virtio-net',
            ],
            width=150,
            font=CTK_FONT_SMALL,
            command=self._on_type_changed,
        )
        self.type_menu.set('pci')
        self.type_menu.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        # Model
        ctk.CTkLabel(info_frame, text='Model:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=1, column=0, padx=5, pady=5, sticky='w'
        )
        self.model_menu = ctk.CTkOptionMenu(
            info_frame,
            values=[
                '',
                'virtio',
                'e1000',
                'e1000e',
                'rtl8139',
                'pcnet',
                'ide',
                'scsi',
                'sata',
                'usb-ohci',
                'usb-uhci',
                'usb-ehci',
                'usb-xhci',
            ],
            width=150,
            font=CTK_FONT_SMALL,
        )
        self.model_menu.set('')
        self.model_menu.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        # Index
        ctk.CTkLabel(info_frame, text='Index:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=2, column=0, padx=5, pady=5, sticky='w'
        )
        self.index_entry = ctk.CTkEntry(
            info_frame, placeholder_text='0', width=100, font=CTK_FONT_SMALL
        )
        self.index_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')

        # Address
        ctk.CTkLabel(info_frame, text='Address:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=3, column=0, padx=5, pady=5, sticky='w'
        )
        self.address_entry = ctk.CTkEntry(
            info_frame, placeholder_text='0000:00:00.0', width=150, font=CTK_FONT_SMALL
        )
        self.address_entry.grid(row=3, column=1, padx=5, pady=5, sticky='w')

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
        # 根据控制器类型设置默认模型
        model_map = {
            'pci': '',
            'usb': 'usb-xhci',
            'scsi': 'virtio-scsi',
            'ide': 'ide',
            'sata': 'sata',
            'fdc': '',
            'ccid': '',
            'virtio-serial': 'virtio-serial',
            'virtio-blk': 'virtio-blk',
            'virtio-net': 'virtio-net',
        }
        default_model = model_map.get(new_type, '')
        self.model_menu.set(default_model)

    def _confirm(self):
        """确认添加."""
        controller_type = self.type_menu.get()

        config = {
            'type': controller_type,
            'model': self.model_menu.get(),
            'index': self.index_entry.get().strip(),
            'address': self.address_entry.get().strip(),
        }

        self.on_confirm_callback(config)
        self.dialog.destroy()
