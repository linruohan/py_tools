"""事件配置 Tab - 生命周期事件配置."""

import customtkinter as ctk

from components.base_tab import BaseConfigTab
from utils.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class EventsConfigurationTab(BaseConfigTab):
    """事件配置 Tab."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, on_change_callback, **kwargs)

        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面."""
        self.grid_columnconfigure(0, weight=1)

        left_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        left_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

        ctk.CTkLabel(left_frame, text='事件配置', font=CTK_FONT_BOLD, text_color='#64b5f6').pack(
            anchor='w', padx=10, pady=5
        )

        # 第一行:关机时、重启时、崩溃时、锁失败时(使用 pack 左对齐)
        events_frame = ctk.CTkFrame(left_frame, fg_color='transparent')
        events_frame.pack(anchor='w', padx=10, pady=5)

        # 关机时
        ctk.CTkLabel(events_frame, text='关机时:', font=CTK_FONT_MAIN, width=60, anchor='w').pack(
            side='left', padx=(0, 5)
        )
        self.on_poweroff = ctk.CTkOptionMenu(
            events_frame,
            values=['None', 'destroy', 'restart', 'preserve', 'rename-restart'],
            width=100,
            font=CTK_FONT_SMALL,
            command=self._on_poweroff_changed,
        )
        self.on_poweroff.set('None')
        self.on_poweroff.pack(side='left', padx=(0, 15))

        # 重启时
        ctk.CTkLabel(events_frame, text='重启时:', font=CTK_FONT_MAIN, width=60, anchor='w').pack(
            side='left', padx=(0, 5)
        )
        self.on_reboot = ctk.CTkOptionMenu(
            events_frame,
            values=['None', 'destroy', 'restart', 'preserve', 'rename-restart'],
            width=100,
            font=CTK_FONT_SMALL,
            command=self._on_reboot_changed,
        )
        self.on_reboot.set('None')
        self.on_reboot.pack(side='left', padx=(0, 15))

        # 崩溃时
        ctk.CTkLabel(events_frame, text='崩溃时:', font=CTK_FONT_MAIN, width=60, anchor='w').pack(
            side='left', padx=(0, 5)
        )
        self.on_crash = ctk.CTkOptionMenu(
            events_frame,
            values=[
                'None',
                'destroy',
                'restart',
                'preserve',
                'rename-restart',
                'coredump-destroy',
                'coredump-restart',
            ],
            width=100,
            font=CTK_FONT_SMALL,
        )
        self.on_crash.set('None')
        self.on_crash.pack(side='left', padx=(0, 15))
        self.on_crash.configure(command=self._trigger_change)

        # 锁失败时
        ctk.CTkLabel(events_frame, text='锁失败时:', font=CTK_FONT_MAIN, width=60, anchor='w').pack(
            side='left', padx=(0, 5)
        )
        self.on_lockfailure = ctk.CTkOptionMenu(
            events_frame,
            values=['None', 'poweroff', 'restart', 'pause', 'ignore'],
            width=100,
            font=CTK_FONT_SMALL,
        )
        self.on_lockfailure.set('None')
        self.on_lockfailure.pack(side='left')
        self.on_lockfailure.configure(command=self._trigger_change)

        # 说明文本区域
        info_label = ctk.CTkLabel(
            left_frame,
            text='动作说明:\n'
            '• destroy: 终止并释放所有资源  • restart: 终止后以相同配置重启\t'
            '• preserve: 终止并保留资源供分析 \t• rename-restart: 终止后以新名称重启 (仅 libxl)\n'
            '• coredump-destroy: 生成核心转储后终止 (since 0.8.4)\t'
            '• coredump-restart: 生成核心转储后重启 (since 0.8.4)\n\n'
            '锁失败动作 (on_lockfailure, since 1.0.0):\n'
            '• poweroff: 强制关闭电源  \t• restart: 重启以重新获取锁\t'
            '• pause: 暂停等待手动恢复  \t• ignore: 忽略并继续运行\n\n'
            '注意:\n'
            '• 并非所有管理程序都支持所有事件和动作\n'
            '• QEMU/KVM/HVF: on_poweroff=restart 与 on_reboot=destroy 互斥\n'
            '• 可通过 virDomainSetLifecycleAction API 配置 (since 3.9.0)',
            font=CTK_FONT_SMALL,
            text_color='#888888',
            justify='left',
        )
        info_label.pack(anchor='w', padx=10, pady=5)

    def _on_poweroff_changed(self, value: str) -> None:
        """关机时选项变化回调,处理互斥关系.

        Args:
            value: 新选择的值
        """
        if value == 'restart':
            if self.on_reboot.get() == 'destroy':
                self.on_reboot.set('None')
        self._trigger_change(value)

    def _on_reboot_changed(self, value: str) -> None:
        """重启时选项变化回调,处理互斥关系.

        Args:
            value: 新选择的值
        """
        if value == 'destroy':
            if self.on_poweroff.get() == 'restart':
                self.on_poweroff.set('None')
        self._trigger_change(value)

    def get_config(self) -> dict:
        """获取配置数据."""
        return {
            'on_poweroff': self.on_poweroff.get(),
            'on_reboot': self.on_reboot.get(),
            'on_crash': self.on_crash.get(),
            'on_lockfailure': self.on_lockfailure.get(),
        }

    def to_xml(self) -> dict:
        """生成 XML 配置字典.

        None 选项表示不生成对应的 XML 元素.
        """
        config = {}

        on_poweroff = self.on_poweroff.get()
        if on_poweroff and on_poweroff != 'None':
            config['on_poweroff'] = on_poweroff

        on_reboot = self.on_reboot.get()
        if on_reboot and on_reboot != 'None':
            config['on_reboot'] = on_reboot

        on_crash = self.on_crash.get()
        if on_crash and on_crash != 'None':
            config['on_crash'] = on_crash

        on_lockfailure = self.on_lockfailure.get()
        if on_lockfailure and on_lockfailure != 'None':
            config['on_lockfailure'] = on_lockfailure

        return {'events_configuration': config}
