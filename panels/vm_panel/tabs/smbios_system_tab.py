"""SMBIOS 系统信息配置 Tab - BIOS、系统、主板、机箱、OEM Strings 和 FwCfg 信息."""

import customtkinter as ctk

from components.base_tab import BaseConfigTab
from utils.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN


class SMBIOSSystemTab(BaseConfigTab):
    """SMBIOS 系统信息配置 Tab - 合并所有 section 为一个面板."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, on_change_callback, **kwargs)

    def _init_ui(self) -> None:
        """初始化界面 - 所有 section 合并为一个，每个组的元素在同一行，pack 布局左对齐."""
        # 创建主滚动框架
        main_frame = ctk.CTkScrollableFrame(self, fg_color='transparent')
        main_frame.pack(fill='both', expand=True, padx=5, pady=5)

        # ========== BIOS 信息 (SMBIOS Block 0) ==========
        bios_frame = ctk.CTkFrame(main_frame, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        bios_frame.pack(fill='x', padx=5, pady=5, anchor='w')

        ctk.CTkLabel(
            bios_frame, text='BIOS 信息 (SMBIOS Block 0)', font=CTK_FONT_BOLD, text_color='#64b5f6'
        ).pack(anchor='w', padx=10, pady=(10, 5))

        self._create_row(
            bios_frame,
            [
                ('厂商 (vendor):', 'vendor', 'LENOVO'),
                ('版本 (version):', 'version', 'BIOS 版本'),
                ('日期 (date):', 'date', 'mm/dd/yyyy'),
                ('发布版本 (release):', 'release', '10.22'),
            ],
        )

        # ========== 系统信息 (SMBIOS Block 1) ==========
        system_frame = ctk.CTkFrame(main_frame, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        system_frame.pack(fill='x', padx=5, pady=5, anchor='w')

        ctk.CTkLabel(
            system_frame, text='系统信息 (SMBIOS Block 1)', font=CTK_FONT_BOLD, text_color='#4caf50'
        ).pack(anchor='w', padx=10, pady=(10, 5))

        self._create_row(
            system_frame,
            [
                ('制造商 (manufacturer):', 'system_manufacturer', 'Fedora'),
                ('产品名 (product):', 'system_product', 'Virt-Manager'),
                ('版本 (version):', 'system_version', '0.9.4'),
                ('序列号 (serial):', 'system_serial', '序列号'),
                ('UUID:', 'system_uuid', '自动生成'),
                ('SKU:', 'system_sku', 'SKU 编号'),
                ('家族 (family):', 'system_family', '产品家族'),
            ],
        )

        # ========== 主板信息 (SMBIOS Block 2) ==========
        baseboard_frame = ctk.CTkFrame(main_frame, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        baseboard_frame.pack(fill='x', padx=5, pady=5, anchor='w')

        ctk.CTkLabel(
            baseboard_frame,
            text='主板信息 (SMBIOS Block 2)',
            font=CTK_FONT_BOLD,
            text_color='#ff9800',
        ).pack(anchor='w', padx=10, pady=(10, 5))

        self._create_row(
            baseboard_frame,
            [
                ('制造商 (manufacturer):', 'baseboard_manufacturer', 'LENOVO'),
                ('产品名 (product):', 'baseboard_product', '20BE0061MC'),
                ('版本 (version):', 'baseboard_version', '0B98401 Pro'),
                ('序列号 (serial):', 'baseboard_serial', 'W1KS427111E'),
                ('资产标签 (asset):', 'baseboard_asset', '资产标签'),
                ('位置 (location):', 'baseboard_location', '机箱位置'),
            ],
        )

        # ========== 机箱信息 (SMBIOS Block 3) ==========
        chassis_frame = ctk.CTkFrame(main_frame, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        chassis_frame.pack(fill='x', padx=5, pady=5, anchor='w')

        ctk.CTkLabel(
            chassis_frame,
            text='机箱信息 (SMBIOS Block 3)',
            font=CTK_FONT_BOLD,
            text_color='#9c27b0',
        ).pack(anchor='w', padx=10, pady=(10, 5))

        self._create_row(
            chassis_frame,
            [
                ('制造商 (manufacturer):', 'chassis_manufacturer', 'Dell Inc.'),
                ('版本 (version):', 'chassis_version', '2.12'),
                ('序列号 (serial):', 'chassis_serial', '65X0XF2'),
                ('资产标签 (asset):', 'chassis_asset', '40000101'),
                ('SKU:', 'chassis_sku', 'Type3Sku1'),
            ],
        )

        # ========== OEM Strings (SMBIOS Block 11) ==========
        oem_frame = ctk.CTkFrame(main_frame, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        oem_frame.pack(fill='x', padx=5, pady=5, anchor='w')

        ctk.CTkLabel(
            oem_frame,
            text='OEM Strings (SMBIOS Block 11)',
            font=CTK_FONT_BOLD,
            text_color='#e91e63',
        ).pack(anchor='w', padx=10, pady=(10, 5))

        self.oem_strings_frame = ctk.CTkFrame(oem_frame, fg_color='transparent')
        self.oem_strings_frame.pack(fill='x', padx=10, pady=5, anchor='w')
        self.oem_entries = []
        self._add_oem_entry(self.oem_strings_frame)

        add_oem_btn = ctk.CTkButton(
            oem_frame,
            text='添加 OEM 字符串',
            command=self._add_oem_entry_handler,
            width=150,
            font=CTK_FONT_MAIN,
        )
        add_oem_btn.pack(anchor='w', padx=10, pady=(0, 10))

        # ========== FwCfg 配置 ==========
        fwcfg_frame = ctk.CTkFrame(main_frame, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        fwcfg_frame.pack(fill='x', padx=5, pady=5, anchor='w')

        ctk.CTkLabel(fwcfg_frame, text='FwCfg 配置', font=CTK_FONT_BOLD, text_color='#00bcd4').pack(
            anchor='w', padx=10, pady=(10, 5)
        )

        info_label = ctk.CTkLabel(
            fwcfg_frame,
            text=(
                'FwCfg 用于向虚拟机传递固件配置数据。'
                '名称必须以 opt/ 开头，'
                '建议使用 opt/$RFQDN/$name 格式避免冲突。'
            ),
            font=CTK_FONT_MAIN,
            text_color='#888888',
            justify='left',
            wraplength=500,
        )
        info_label.pack(anchor='w', padx=10, pady=5)

        self.fwcfg_entries_frame = ctk.CTkFrame(fwcfg_frame, fg_color='transparent')
        self.fwcfg_entries_frame.pack(fill='x', padx=10, pady=5, anchor='w')
        self.fwcfg_entries = []
        self._add_fwcfg_entry(self.fwcfg_entries_frame)

        add_fwcfg_btn = ctk.CTkButton(
            fwcfg_frame,
            text='添加 FwCfg 条目',
            command=self._add_fwcfg_entry_handler,
            width=150,
            font=CTK_FONT_MAIN,
        )
        add_fwcfg_btn.pack(anchor='w', padx=10, pady=(0, 10))

    def _create_row(self, parent, fields):
        """创建一行输入框 - 所有字段在同一行.

        Args:
            parent: 父容器
            fields: 字段列表，每个元素为 (label_text, attr_name, placeholder)
        """
        row_frame = ctk.CTkFrame(parent, fg_color='transparent')
        row_frame.pack(fill='x', padx=10, pady=3, anchor='w')

        for label_text, attr_name, placeholder in fields:
            # 标签
            label = ctk.CTkLabel(row_frame, text=label_text, font=CTK_FONT_MAIN, anchor='w')
            label.pack(side='left', padx=(5, 5))

            # 输入框
            entry = ctk.CTkEntry(row_frame, placeholder_text=placeholder, width=150)
            entry.pack(side='left', padx=5)
            entry.bind('<KeyRelease>', lambda e: self._trigger_change())

            # None 复选框
            none_var = ctk.BooleanVar(value=False)
            none_check = ctk.CTkCheckBox(
                row_frame, text='None', variable=none_var, command=self._trigger_change, width=50
            )
            none_check.pack(side='left', padx=5)

            setattr(self, f'{attr_name}_entry', entry)
            setattr(self, f'{attr_name}_none', none_var)

    def _add_oem_entry(self, parent):
        """添加 OEM 字符串输入行."""
        row_frame = ctk.CTkFrame(parent, fg_color='transparent')
        row_frame.pack(fill='x', padx=5, pady=2)

        entry = ctk.CTkEntry(row_frame, placeholder_text='myappname:some arbitrary data', width=400)
        entry.pack(side='left', padx=5)
        entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        none_var = ctk.BooleanVar(value=False)
        none_check = ctk.CTkCheckBox(
            row_frame, text='None', variable=none_var, command=self._trigger_change, width=50
        )
        none_check.pack(side='left', padx=10)

        remove_btn = ctk.CTkButton(
            row_frame,
            text='删除',
            command=lambda: self._remove_oem_entry(row_frame),
            width=60,
            font=CTK_FONT_MAIN,
        )
        remove_btn.pack(side='left', padx=5)

        self.oem_entries.append((entry, none_var, row_frame))
        return entry, none_var, row_frame

    def _add_oem_entry_handler(self):
        """添加 OEM 字符串条目."""
        self._add_oem_entry(self.oem_strings_frame)
        self._trigger_change()

    def _remove_oem_entry(self, frame):
        """删除 OEM 字符串条目."""
        for i, (_entry, _none_var, f) in enumerate(self.oem_entries):
            if f == frame:
                self.oem_entries.pop(i)
                frame.destroy()
                break
        self._trigger_change()

    def _add_fwcfg_entry(self, parent):
        """添加 FwCfg 输入行."""
        row_frame = ctk.CTkFrame(parent, fg_color='transparent')
        row_frame.pack(fill='x', padx=5, pady=2)

        name_entry = ctk.CTkEntry(row_frame, placeholder_text='opt/com.example/name', width=200)
        name_entry.pack(side='left', padx=5)
        name_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        value_label = ctk.CTkLabel(row_frame, text='值:', font=CTK_FONT_MAIN)
        value_label.pack(side='left', padx=(10, 5))

        value_entry = ctk.CTkEntry(row_frame, placeholder_text='直接值', width=150)
        value_entry.pack(side='left', padx=5)
        value_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        file_label = ctk.CTkLabel(row_frame, text='或文件:', font=CTK_FONT_MAIN)
        file_label.pack(side='left', padx=(10, 5))

        file_entry = ctk.CTkEntry(row_frame, placeholder_text='/tmp/config.ign', width=150)
        file_entry.pack(side='left', padx=5)
        file_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        none_var = ctk.BooleanVar(value=False)
        none_check = ctk.CTkCheckBox(
            row_frame, text='None', variable=none_var, command=self._trigger_change, width=50
        )
        none_check.pack(side='left', padx=10)

        remove_btn = ctk.CTkButton(
            row_frame,
            text='删除',
            command=lambda: self._remove_fwcfg_entry(row_frame),
            width=60,
            font=CTK_FONT_MAIN,
        )
        remove_btn.pack(side='left', padx=5)

        self.fwcfg_entries.append((name_entry, value_entry, file_entry, none_var, row_frame))
        return name_entry, value_entry, file_entry, none_var, row_frame

    def _add_fwcfg_entry_handler(self):
        """添加 FwCfg 条目."""
        self._add_fwcfg_entry(self.fwcfg_entries_frame)
        self._trigger_change()

    def _remove_fwcfg_entry(self, frame):
        """删除 FwCfg 条目."""
        for i, (_name, _value, _file, _none_var, f) in enumerate(self.fwcfg_entries):
            if f == frame:
                self.fwcfg_entries.pop(i)
                frame.destroy()
                break
        self._trigger_change()

    def get_config(self) -> dict:
        """获取配置数据."""
        config = {}

        # 收集 BIOS 信息
        bios = {}
        for field in ['vendor', 'version', 'date', 'release']:
            entry = getattr(self, f'{field}_entry', None)
            none_var = getattr(self, f'{field}_none', None)
            if entry:
                val = entry.get().strip()
                if val and not (none_var and none_var.get()):
                    bios[field] = val

        # 收集系统信息
        system = {}
        for field in ['manufacturer', 'product', 'version', 'serial', 'uuid', 'sku', 'family']:
            entry = getattr(self, f'system_{field}_entry', None)
            none_var = getattr(self, f'system_{field}_none', None)
            if entry:
                val = entry.get().strip()
                if val and not (none_var and none_var.get()):
                    system[field] = val

        # 收集主板信息
        base_board = {}
        for field in ['manufacturer', 'product', 'version', 'serial', 'asset', 'location']:
            entry = getattr(self, f'baseboard_{field}_entry', None)
            none_var = getattr(self, f'baseboard_{field}_none', None)
            if entry:
                val = entry.get().strip()
                if val and not (none_var and none_var.get()):
                    base_board[field] = val

        # 收集机箱信息
        chassis = {}
        for field in ['manufacturer', 'version', 'serial', 'asset', 'sku']:
            entry = getattr(self, f'chassis_{field}_entry', None)
            none_var = getattr(self, f'chassis_{field}_none', None)
            if entry:
                val = entry.get().strip()
                if val and not (none_var and none_var.get()):
                    chassis[field] = val

        # 收集 OEM Strings
        oem_strings = []
        for entry, none_var, _ in self.oem_entries:
            val = entry.get().strip()
            if val and not none_var.get():
                oem_strings.append(val)

        # 收集 FwCfg 条目
        fwcfg_entries = []
        for name, value, file, none_var, _ in self.fwcfg_entries:
            name_val = name.get().strip()
            value_val = value.get().strip()
            file_val = file.get().strip()
            if name_val and not none_var.get():
                fwcfg_entries.append(
                    {
                        'name': name_val,
                        'value': value_val if value_val else None,
                        'file': file_val if file_val else None,
                    }
                )

        # 构建 sysinfo 配置
        has_smbios_content = bios or system or base_board or chassis or oem_strings
        has_fwcfg_content = bool(fwcfg_entries)

        # 优先使用 FwCfg，如果只有 SMBIOS 内容则使用 SMBIOS
        if has_fwcfg_content:
            sysinfo_data = {'type': 'fwcfg', 'fwcfg_entries': fwcfg_entries}
        elif has_smbios_content:
            sysinfo_data = {'type': 'smbios'}
            if bios:
                sysinfo_data['bios'] = bios
            if system:
                sysinfo_data['system'] = system
            if base_board:
                sysinfo_data['base_board'] = base_board
            if chassis:
                sysinfo_data['chassis'] = chassis
            if oem_strings:
                sysinfo_data['oem_strings'] = oem_strings
        else:
            sysinfo_data = {}

        config['sysinfo'] = sysinfo_data

        # 同时设置 os.smbios mode 为 sysinfo
        if has_smbios_content:
            config['smbios_mode'] = 'sysinfo'

        return config

    def to_xml(self) -> dict:
        """生成 XML 配置字典."""
        return self.get_config()

    def load_config(self, config: dict) -> None:
        """加载配置数据."""
        # 清空现有 OEM 条目
        for _, _, frame in list(self.oem_entries):
            frame.destroy()
        self.oem_entries = []

        # 清空现有 FwCfg 条目
        for _, _, _, _, frame in list(self.fwcfg_entries):
            frame.destroy()
        self.fwcfg_entries = []

        # 重置所有 BIOS 字段
        for field in ['vendor', 'version', 'date', 'release']:
            entry = getattr(self, f'{field}_entry', None)
            none_var = getattr(self, f'{field}_none', None)
            if entry:
                entry.delete(0, 'end')
                entry.insert(0, '')
            if none_var:
                none_var.set(False)

        # 重置所有系统字段
        for field in ['manufacturer', 'product', 'version', 'serial', 'uuid', 'sku', 'family']:
            entry = getattr(self, f'system_{field}_entry', None)
            none_var = getattr(self, f'system_{field}_none', None)
            if entry:
                entry.delete(0, 'end')
                entry.insert(0, '')
            if none_var:
                none_var.set(False)

        # 重置所有主板字段
        for field in ['manufacturer', 'product', 'version', 'serial', 'asset', 'location']:
            entry = getattr(self, f'baseboard_{field}_entry', None)
            none_var = getattr(self, f'baseboard_{field}_none', None)
            if entry:
                entry.delete(0, 'end')
                entry.insert(0, '')
            if none_var:
                none_var.set(False)

        # 重置所有机箱字段
        for field in ['manufacturer', 'version', 'serial', 'asset', 'sku']:
            entry = getattr(self, f'chassis_{field}_entry', None)
            none_var = getattr(self, f'chassis_{field}_none', None)
            if entry:
                entry.delete(0, 'end')
                entry.insert(0, '')
            if none_var:
                none_var.set(False)

        if not config:
            return

        # 加载 BIOS 配置
        bios = config.get('bios', {})
        for field in ['vendor', 'version', 'date', 'release']:
            entry = getattr(self, f'{field}_entry', None)
            none_var = getattr(self, f'{field}_none', None)
            if entry and field in bios:
                entry.delete(0, 'end')
                entry.insert(0, bios[field])
                if none_var:
                    none_var.set(False)

        # 加载系统配置
        system = config.get('system', {})
        for field in ['manufacturer', 'product', 'version', 'serial', 'uuid', 'sku', 'family']:
            entry = getattr(self, f'system_{field}_entry', None)
            none_var = getattr(self, f'system_{field}_none', None)
            if entry and field in system:
                entry.delete(0, 'end')
                entry.insert(0, system[field])
                if none_var:
                    none_var.set(False)

        # 加载主板配置
        base_board = config.get('base_board', {})
        for field in ['manufacturer', 'product', 'version', 'serial', 'asset', 'location']:
            entry = getattr(self, f'baseboard_{field}_entry', None)
            none_var = getattr(self, f'baseboard_{field}_none', None)
            if entry and field in base_board:
                entry.delete(0, 'end')
                entry.insert(0, base_board[field])
                if none_var:
                    none_var.set(False)

        # 加载机箱配置
        chassis = config.get('chassis', {})
        for field in ['manufacturer', 'version', 'serial', 'asset', 'sku']:
            entry = getattr(self, f'chassis_{field}_entry', None)
            none_var = getattr(self, f'chassis_{field}_none', None)
            if entry and field in chassis:
                entry.delete(0, 'end')
                entry.insert(0, chassis[field])
                if none_var:
                    none_var.set(False)

        # 加载 OEM Strings
        oem_strings = config.get('oem_strings', [])
        for oem_str in oem_strings:
            entry, none_var, _ = self._add_oem_entry(self.oem_strings_frame)
            entry.insert(0, oem_str)

        # 加载 FwCfg 条目
        fwcfg_entries = config.get('fwcfg_entries', [])
        for fwcfg in fwcfg_entries:
            name, value, file, none_var, _ = self._add_fwcfg_entry(self.fwcfg_entries_frame)
            name.insert(0, fwcfg.get('name', ''))
            if fwcfg.get('value'):
                value.insert(0, fwcfg['value'])
            if fwcfg.get('file'):
                file.insert(0, fwcfg['file'])
