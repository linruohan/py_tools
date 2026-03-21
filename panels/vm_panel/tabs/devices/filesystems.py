"""文件系统设备模块 - 文件系统配置."""

import customtkinter as ctk

from components.base_tab import BaseConfigTab
from utils.styles import BG_COLOR_CONTENT, CTK_FONT_MAIN, CTK_FONT_SMALL


class FilesystemsTab(BaseConfigTab):
    """文件系统配置 Tab - 支持文件系统设备配置."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, on_change_callback, **kwargs)
        self.filesystem_list = []

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
            text='Add Filesystem',
            command=self._add_filesystem,
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
        self.filesystem_display = ctk.CTkLabel(
            self.content_frame,
            text='暂无文件系统',
            font=CTK_FONT_SMALL,
            text_color='#aaaaaa',
            anchor='w',
        )
        self.filesystem_display.grid(row=0, column=0, sticky='w', padx=10, pady=10)

    def _add_filesystem(self):
        """Add filesystem configuration dialog."""
        dialog = ctk.CTkToplevel(self)
        dialog.title('Add Filesystem')
        dialog.geometry('600x400')
        dialog.transient(self)
        dialog.grab_set()

        FilesystemConfigDialog(dialog, self._on_filesystem_added)

    def _on_filesystem_added(self, filesystem_config):
        """文件系统添加完成回调."""
        self.filesystem_list.append(filesystem_config)
        self._update_display()
        self._trigger_change()

    def _clear_list(self):
        """清空文件系统列表."""
        self.filesystem_list.clear()
        self._update_display()
        self._trigger_change()

    def _update_display(self):
        """更新显示."""
        # 清除旧的显示
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        if not self.filesystem_list:
            label = ctk.CTkLabel(
                self.content_frame,
                text='暂无文件系统',
                font=CTK_FONT_SMALL,
                text_color='#aaaaaa',
                anchor='w',
            )
            label.grid(row=0, column=0, sticky='w', padx=10, pady=10)
            return

        # 显示所有文件系统
        for i, filesystem in enumerate(self.filesystem_list):
            fs_frame = ctk.CTkFrame(self.content_frame, fg_color='transparent')
            fs_frame.grid(row=i, column=0, sticky='ew', padx=10, pady=5)

            # 文件系统类型标签
            type_label = f'[{filesystem.get("type", "mount")}]'
            source_label = filesystem.get('source', '')
            target_label = filesystem.get('target', '')

            label = ctk.CTkLabel(
                fs_frame,
                text=f'{type_label}: {source_label} -> {target_label}',
                font=CTK_FONT_MAIN,
                anchor='w',
            )
            label.grid(row=0, column=0, sticky='w')

            # 删除按钮
            del_btn = ctk.CTkButton(
                fs_frame,
                text='删除',
                width=60,
                fg_color='#f44336',
                hover_color='#d32f2f',
                font=CTK_FONT_SMALL,
                command=lambda idx=i: self._remove_filesystem(idx),
            )
            del_btn.grid(row=0, column=1, padx=10)

    def _remove_filesystem(self, index):
        """删除指定索引的文件系统."""
        self.filesystem_list.pop(index)
        self._update_display()
        self._trigger_change()

    def get_config(self) -> dict:
        """获取配置."""
        return {
            'type': 'filesystems',
            'filesystems': self.filesystem_list.copy(),
        }


class FilesystemConfigDialog:
    """文件系统配置对话框."""

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

        # Filesystem Type
        ctk.CTkLabel(info_frame, text='Type:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=0, column=0, padx=5, pady=5, sticky='w'
        )
        self.type_menu = ctk.CTkOptionMenu(
            info_frame,
            values=['mount', 'template', 'transient'],
            width=120,
            font=CTK_FONT_SMALL,
            command=self._on_type_changed,
        )
        self.type_menu.set('mount')
        self.type_menu.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        # Source
        ctk.CTkLabel(info_frame, text='Source:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=1, column=0, padx=5, pady=5, sticky='w'
        )
        self.source_entry = ctk.CTkEntry(
            info_frame, placeholder_text='/path/to/filesystem', width=300, font=CTK_FONT_SMALL
        )
        self.source_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        # Target
        ctk.CTkLabel(info_frame, text='Target:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=2, column=0, padx=5, pady=5, sticky='w'
        )
        self.target_entry = ctk.CTkEntry(
            info_frame, placeholder_text='/mnt/filesystem', width=300, font=CTK_FONT_SMALL
        )
        self.target_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')

        # Format
        ctk.CTkLabel(info_frame, text='Format:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=3, column=0, padx=5, pady=5, sticky='w'
        )
        self.format_entry = ctk.CTkEntry(
            info_frame, placeholder_text='ext4', width=100, font=CTK_FONT_SMALL
        )
        self.format_entry.grid(row=3, column=1, padx=5, pady=5, sticky='w')

        # Access Mode
        ctk.CTkLabel(
            info_frame, text='Access Mode:', font=CTK_FONT_MAIN, width=80, anchor='w'
        ).grid(row=4, column=0, padx=5, pady=5, sticky='w')
        self.access_mode_menu = ctk.CTkOptionMenu(
            info_frame,
            values=['passthrough', 'mapped', 'squash'],
            width=120,
            font=CTK_FONT_SMALL,
        )
        self.access_mode_menu.set('passthrough')
        self.access_mode_menu.grid(row=4, column=1, padx=5, pady=5, sticky='w')

        # Read-only
        self.readonly_check = ctk.CTkCheckBox(info_frame, text='Read-only', font=CTK_FONT_SMALL)
        self.readonly_check.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky='w')

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
        pass

    def _confirm(self):
        """确认添加."""
        filesystem_type = self.type_menu.get()

        config = {
            'type': filesystem_type,
            'source': self.source_entry.get().strip(),
            'target': self.target_entry.get().strip(),
            'format': self.format_entry.get().strip(),
            'access_mode': self.access_mode_menu.get(),
            'readonly': self.readonly_check.get(),
        }

        self.on_confirm_callback(config)
        self.dialog.destroy()
