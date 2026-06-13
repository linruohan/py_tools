"""光纤通道 VMID 配置 Tab - Fibre Channel VMID."""

import customtkinter as ctk

from components.base_tab import BaseConfigTab
from utils.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class FibreChannelVMIDTab(BaseConfigTab):
    """光纤通道 VMID 配置 Tab - FC SAN QoS 和访问控制."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, on_change_callback, **kwargs)
        self._changing_option = False  # 防止递归触发

    def _init_ui(self) -> None:
        """初始化界面."""
        # 主配置框
        main_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        main_frame.pack(fill='both', expand=True, padx=5, pady=5)

        # 标题
        ctk.CTkLabel(
            main_frame, text='FC VMID 配置', font=CTK_FONT_BOLD, text_color='#64b5f6'
        ).pack(anchor='w', padx=10, pady=5)

        # 配置行:FC VMID 启用状态 + App ID 输入
        config_frame = ctk.CTkFrame(main_frame, fg_color='transparent')
        config_frame.pack(anchor='w', padx=10, pady=5)

        ctk.CTkLabel(config_frame, text='FC VMID:', font=CTK_FONT_MAIN, width=80, anchor='w').pack(
            side='left', padx=(0, 5)
        )
        self.enabled_var = ctk.StringVar(value='none')
        self.enabled_combo = ctk.CTkComboBox(
            config_frame,
            values=['none', 'enabled'],
            variable=self.enabled_var,
            width=120,
            command=self._on_enabled_changed,
        )
        self.enabled_combo.pack(side='left', padx=5)

        ctk.CTkLabel(config_frame, text='App ID:', font=CTK_FONT_MAIN, width=60, anchor='w').pack(
            side='left', padx=(10, 5)
        )
        self.appid = ctk.CTkEntry(config_frame, placeholder_text='最大 128 字节', width=200)
        self.appid.pack(side='left', padx=5)
        self.appid.bind('<KeyRelease>', lambda e: self._trigger_change())
        # 初始禁用 App ID 输入框
        self.appid.configure(state='disabled')

        # 功能说明
        info_frame = ctk.CTkFrame(main_frame, fg_color='transparent')
        info_frame.pack(anchor='w', padx=10, pady=10)

        info_title = ctk.CTkLabel(
            info_frame, text='功能说明:', font=CTK_FONT_BOLD, text_color='#4caf50'
        )
        info_title.pack(anchor='w')

        info_text = (
            'FC SAN 可以根据 VMID 提供:不同的 QoS 级别、访问控制、收集每 VM 级别的遥测数据\n'
            'App ID 说明:单个字符串,最大 128 字节,由内核用于创建 VMID\n'
            '使用此功能需要:支持 Fibre Channel 的硬件、CONFIG_BLK_CGROUP_FC_APPID\n'
            '自 libvirt 7.7.0 版本起支持'
        )
        info_label = ctk.CTkLabel(
            info_frame,
            text=info_text,
            font=CTK_FONT_SMALL,
            text_color='#888888',
            justify='left',
            anchor='w',
        )
        info_label.pack(anchor='w', fill='x')

    def _on_enabled_changed(self, value: str) -> None:
        """启用状态改变时的处理."""
        if self._changing_option:
            return
        self._changing_option = True
        try:
            if value == 'enabled':
                # 启用时允许输入 App ID
                self.appid.configure(state='normal')
                self.appid.focus_set()
            else:
                # 禁用时清空并禁用 App ID 输入框
                self.appid.delete(0, 'end')
                self.appid.configure(state='disabled')
            # 触发 XML 更新
            self._trigger_change()
        finally:
            self._changing_option = False

    def get_config(self) -> dict:
        """获取配置数据."""
        return {
            'appid': self.appid.get().strip(),
        }

    def to_xml(self) -> dict:
        """生成 XML 配置字典."""
        appid_value = self.appid.get().strip()

        # 如果没有设置 App ID 或处于禁用状态,返回空字典
        # 这样 vm_config.update_from_tab 不会更新配置
        # 最终 xml_generator._add_resource 不会生成 fibrechannel 元素
        if not appid_value or self.enabled_var.get() == 'none':
            return {
                'fibre_channel_vmid': {'appid': ''},
            }

        # 如果设置了 App ID,生成 fibre_channel_vmid 配置
        # 格式:{'fibre_channel_vmid': {'appid': 'xxx'}}
        return {
            'fibre_channel_vmid': {'appid': appid_value},
        }
