"""安全标签配置 Tab - Security Label."""

import customtkinter as ctk

from ..styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class SecurityLabelTab(ctk.CTkFrame):
    """安全标签配置 Tab - SELinux/AppArmor 安全标签."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent')
        self.on_change_callback = on_change_callback

        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        left_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        left_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        left_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            left_frame, text='安全标签配置', font=CTK_FONT_BOLD, text_color='#64b5f6'
        ).grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w')

        ctk.CTkLabel(left_frame, text='类型:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.label_type = ctk.CTkOptionMenu(
            left_frame,
            values=['dynamic', 'static', 'none'],
            width=100,
            font=CTK_FONT_SMALL,
        )
        self.label_type.set('dynamic')
        self.label_type.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.label_type.configure(command=self._trigger_change)

        ctk.CTkLabel(left_frame, text='模型:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.model = ctk.CTkOptionMenu(
            left_frame,
            values=['selinux', 'apparmor', 'dac'],
            width=100,
            font=CTK_FONT_SMALL,
        )
        self.model.set('selinux')
        self.model.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.model.configure(command=self._trigger_change)

        ctk.CTkLabel(left_frame, text='标签:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=3, column=0, padx=10, pady=5, sticky='w'
        )
        self.label = ctk.CTkEntry(
            left_frame, placeholder_text='system_u:system_r:svirt_t:s0', width=250
        )
        self.label.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        self.label.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(left_frame, text='镜像标签:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=4, column=0, padx=10, pady=5, sticky='w'
        )
        self.imagelabel = ctk.CTkEntry(left_frame, placeholder_text='镜像文件标签', width=250)
        self.imagelabel.grid(row=4, column=1, padx=5, pady=5, sticky='w')
        self.imagelabel.bind('<KeyRelease>', lambda e: self._trigger_change())

        right_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        right_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)

        ctk.CTkLabel(right_frame, text='选项', font=CTK_FONT_BOLD, text_color='#4caf50').grid(
            row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w'
        )

        self.relabel = ctk.CTkCheckBox(
            right_frame, text='重新标记文件', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.relabel.grid(row=1, column=0, padx=10, pady=5, sticky='w')

        self.baselabel = ctk.CTkCheckBox(
            right_frame, text='使用基础标签', font=CTK_FONT_SMALL, command=self._trigger_change
        )
        self.baselabel.grid(row=2, column=0, padx=10, pady=5, sticky='w')

        ctk.CTkLabel(right_frame, text='基础标签:', font=CTK_FONT_MAIN, width=100, anchor='w').grid(
            row=3, column=0, padx=10, pady=5, sticky='w'
        )
        self.baselabel_value = ctk.CTkEntry(right_frame, placeholder_text='基础标签值', width=200)
        self.baselabel_value.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        self.baselabel_value.bind('<KeyRelease>', lambda e: self._trigger_change())

        info_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        info_frame.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=5, pady=5)

        ctk.CTkLabel(info_frame, text='说明', font=CTK_FONT_BOLD, text_color='#ff9800').grid(
            row=0, column=0, padx=10, pady=5, sticky='w'
        )

        info_text = (
            '类型说明:\n'
            '• dynamic: 动态分配安全标签 (默认)\n'
            '• static: 使用静态安全标签\n'
            '• none: 禁用安全标签\n\n'
            '模型说明:\n'
            '• selinux: SELinux 安全模块\n'
            '• apparmor: AppArmor 安全模块\n'
            '• dac: 自主访问控制'
        )
        ctk.CTkLabel(
            info_frame,
            text=info_text,
            font=CTK_FONT_SMALL,
            text_color='#888888',
            justify='left',
        ).grid(row=1, column=0, padx=10, pady=5, sticky='w')

    def _trigger_change(self):
        """触发变化回调."""
        if self.on_change_callback:
            self.on_change_callback()

    def get_config(self) -> dict:
        """获取配置数据."""
        return {
            'type': self.label_type.get(),
            'model': self.model.get(),
            'label': self.label.get().strip(),
            'imagelabel': self.imagelabel.get().strip(),
            'relabel': self.relabel.get(),
            'baselabel': self.baselabel.get(),
            'baselabel_value': self.baselabel_value.get().strip(),
        }
