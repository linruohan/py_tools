"""安全标签配置 Tab - Security Label.

支持 SELinux/AppArmor/DAC 安全标签配置。
参考：https://www.libvirt.org/formatdomain.html#security-label
"""

from typing import ClassVar

import customtkinter as ctk

from components.base_tab import SectionConfig, StandardConfigTab


class SecurityLabelTab(StandardConfigTab):
    """安全标签配置 Tab - SELinux/AppArmor/DAC 安全标签."""

    SECTIONS: ClassVar[dict] = {
        'basic': SectionConfig(
            title='安全标签配置',
            fields=[],
            color='#64b5f6',
        ),
    }

    def _init_sections_ui(self) -> None:
        """初始化基于 Sections 的 UI."""
        super()._init_sections_ui()

        basic_frame = self.section_frames['basic']
        basic_row = 1
        self._create_basic_section(basic_frame, basic_row)
        basic_row += 1
        self._create_info_section(basic_frame, basic_row)
        basic_row += 1
        self.section_rows['basic'] = basic_row

    def _create_basic_section(self, parent: ctk.CTkFrame, row: int) -> None:
        """创建基本信息区域 - 紧凑布局."""
        # 单行布局：类型 + 模型 + 标签 + 基础标签 + relabel + 镜像标签
        frame = ctk.CTkFrame(parent, fg_color='transparent')
        frame.grid(row=row, column=0, columnspan=2, padx=10, pady=3, sticky='ew')

        # 类型
        ctk.CTkLabel(frame, text='类型:', font=('', 11), width=40, anchor='w').pack(
            side='left', padx=(0, 2)
        )
        self.label_type = ctk.CTkOptionMenu(
            frame,
            values=['None', 'none', 'dynamic', 'static'],
            width=90,
            font=('', 10),
            command=self._on_type_changed,
        )
        self.label_type.set('None')
        self.label_type.pack(side='left', padx=2)

        # 模型
        ctk.CTkLabel(frame, text='模型:', font=('', 11), width=40, anchor='w').pack(
            side='left', padx=(8, 2)
        )
        self.model = ctk.CTkOptionMenu(
            frame,
            values=['selinux', 'apparmor', 'dac'],
            width=90,
            font=('', 10),
            command=self._trigger_change,
        )
        self.model.set('selinux')
        self.model.pack(side='left', padx=2)

        # 标签 (static 类型使用)
        ctk.CTkLabel(frame, text='标签:', font=('', 11), width=40, anchor='w').pack(
            side='left', padx=(8, 2)
        )
        self.label = ctk.CTkEntry(
            frame,
            placeholder_text='system_u:system_r:svirt_t:s0:c392,c662',
            width=240,
            font=('', 10),
        )
        self.label.pack(side='left', padx=2)
        self.label.bind('<KeyRelease>', lambda e: self._trigger_change())

        # 基础标签 (dynamic 类型使用)
        ctk.CTkLabel(frame, text='基础标签:', font=('', 11), width=50, anchor='w').pack(
            side='left', padx=(8, 2)
        )
        self.baselabel_value = ctk.CTkEntry(
            frame,
            placeholder_text='system_u:system_r:my_svirt_t:s0',
            width=200,
            font=('', 10),
        )
        self.baselabel_value.pack(side='left', padx=2)
        self.baselabel_value.bind('<KeyRelease>', lambda e: self._trigger_change())

        # relabel 选项
        self.relabel = ctk.CTkCheckBox(
            frame,
            text='relabel',
            font=('', 10),
            command=self._trigger_change,
        )
        self.relabel.pack(side='left', padx=(8, 2))

        # imagelabel (只读)
        ctk.CTkLabel(frame, text='镜像标签:', font=('', 11), width=50, anchor='w').pack(
            side='left', padx=(8, 2)
        )
        self.imagelabel = ctk.CTkEntry(
            frame, placeholder_text='(只读)', width=120, font=('', 10), state='disabled'
        )
        self.imagelabel.pack(side='left', padx=2)

    def _create_info_section(self, parent: ctk.CTkFrame, row: int) -> None:
        """创建说明区域."""
        info_text = """类型说明：None=不生成 XML；none=禁用安全标签 <seclabel type='none'/>；dynamic=动态分配 (relabel=yes, baselabel 可选)；static=静态指定 (label 必需，relabel 默认 no)
模型说明：selinux(默认，格式 user:role:type:level)；apparmor(配置文件路径)；dac(格式 owner:group 如 root:root)
注意：imagelabel 为运行时输出信息 (只读)；多个 seclabel 可用于多个安全驱动"""

        ctk.CTkLabel(
            parent,
            text=info_text,
            font=('', 9),
            text_color='#888888',
            justify='left',
            anchor='nw',
            wraplength=800,
        ).grid(row=row, column=0, columnspan=2, padx=10, pady=5, sticky='nw')

    def _on_type_changed(self, value: str) -> None:
        """类型改变时的处理."""
        is_none_upper = value == 'None'
        is_none_lower = value == 'none'
        is_dynamic = value == 'dynamic'
        is_static = value == 'static'

        # 模型：None 和 none 类型禁用
        self.model.configure(state='disabled' if (is_none_upper or is_none_lower) else 'normal')

        # 标签 (label): 仅 static 类型需要
        if is_static:
            self.label.configure(state='normal')
        else:
            self.label.configure(state='disabled')

        # 基础标签 (baselabel): 仅 dynamic 类型需要
        if is_dynamic:
            self.baselabel_value.configure(state='normal')
        else:
            self.baselabel_value.configure(state='disabled')

        # relabel: static 类型可选，dynamic 类型固定 yes，None/none 类型禁用
        if is_static:
            self.relabel.configure(state='normal')
        elif is_dynamic:
            self.relabel.select()  # dynamic 类型 relabel 固定为 yes
            self.relabel.configure(state='disabled')
        else:
            self.relabel.deselect()
            self.relabel.configure(state='disabled')

        # imagelabel: 仅显示，始终禁用
        self.imagelabel.configure(state='disabled')

        self._trigger_change()

    def get_config(self) -> dict:
        """获取配置数据."""
        return {
            'type': self.label_type.get(),
            'model': self.model.get(),
            'label': self.label.get().strip(),
            'baselabel': self.baselabel_value.get().strip(),
            'relabel': self.relabel.get(),
        }

    def to_xml(self) -> dict:
        """生成 XML 配置字典.

        根据 type 生成对应结构的 seclabel 配置:
        - None: 不生成任何 XML
        - none: 返回 {'security_label': {'type': 'none'}}
        - dynamic: 生成带 baselabel 的配置 (如设置的话)，relabel 固定 yes
        - static: 生成带 label 和 relabel 的配置
        """
        config = self.get_config()
        sec_type = config.get('type', 'None')

        # None 类型：不生成任何 XML
        if sec_type == 'None':
            return {}

        # none 类型：生成 type='none'
        if sec_type == 'none':
            return {'security_label': {'type': 'none'}}

        seclabel_config = {
            'type': sec_type,
            'model': config.get('model', 'selinux'),
        }

        if sec_type == 'dynamic':
            # dynamic 类型：relabel 固定为 yes
            seclabel_config['relabel'] = True

            # baselabel 可选
            baselabel = config.get('baselabel', '')
            if baselabel:
                seclabel_config['baselabel'] = baselabel

        elif sec_type == 'static':
            # static 类型：relabel 默认 no
            relabel = config.get('relabel', False)
            seclabel_config['relabel'] = relabel

            # label 必需
            label = config.get('label', '')
            if label:
                seclabel_config['label'] = label

        return {'security_label': seclabel_config}

    def load_config(self, config: dict) -> None:
        """加载配置数据到 UI.

        Args:
            config: 包含安全标签配置的字典，可以是:
                - {'security_label': {...}}
                - {'seclabel': {...}}
                - 直接是 seclabel 的配置字典
        """
        sec_config = config.get('security_label') or config.get('seclabel', config)

        sec_type = sec_config.get('type', 'None')
        if sec_type not in ('None', 'none', 'dynamic', 'static'):
            sec_type = 'None'

        self.label_type.set(sec_type)
        self._on_type_changed(sec_type)

        model = sec_config.get('model', 'selinux')
        if model in ('selinux', 'apparmor', 'dac'):
            self.model.set(model)

        # static 类型的 label
        label = sec_config.get('label', '')
        if label:
            self.label.delete(0, ctk.END)
            self.label.insert(0, label)

        # dynamic 类型的 baselabel
        baselabel = sec_config.get('baselabel', '')
        if baselabel:
            self.baselabel_value.delete(0, ctk.END)
            self.baselabel_value.insert(0, baselabel)

        # relabel
        relabel = sec_config.get('relabel', False)
        if sec_type == 'static' and relabel:
            self.relabel.select()
        else:
            self.relabel.deselect()
