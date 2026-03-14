"""VmPanel - 虚拟机 XML 配置生成面板 (24 Tab 版本)."""

import subprocess

from tkinter import END, filedialog, messagebox

import customtkinter as ctk

from model.vm_model.vm_config import VMConfig

from .styles import (
    BG_COLOR_CONTENT,
    BG_COLOR_MAIN,
    CTK_FONT_BOLD,
    CTK_FONT_MONO,
    CTK_FONT_SMALL,
)
from .tab_toggle import TabTogglePanel
from .xml_generator import LibvirtXMLGenerator

# 24 个 Tab 配置
TABS_CONFIG = {
    # 基础 Tab (默认启用)
    'general_metadata': {'name': 'General Metadata', 'class': 'BasicTab', 'default_on': True},
    'os_booting': {'name': 'Os Booting', 'class': 'OSTab', 'default_on': True},
    'devices': {'name': 'Devices', 'class': 'DevicesTab', 'default_on': True},
    'cpu_allocation': {'name': 'CPU Allocation', 'class': 'CPUAllocationTab', 'default_on': True},
    'memory_allocation': {
        'name': 'Memory Allocation',
        'class': 'MemoryAllocationTab',
        'default_on': True,
    },
    # 高级调优 Tab (默认禁用)
    'smbios_system': {
        'name': 'SMBIOS System Information',
        'class': 'SMBIOSSystemTab',
        'default_on': False,
    },
    'iothreads_allocation': {
        'name': 'IOThreads Allocation',
        'class': 'IOThreadsAllocationTab',
        'default_on': False,
    },
    'cpu_tuning': {'name': 'CPU Tuning', 'class': 'CPUTuningTab', 'default_on': False},
    'memory_backing': {'name': 'Memory Backing', 'class': 'MemoryBackingTab', 'default_on': False},
    'memory_tuning': {'name': 'Memory Tuning', 'class': 'MemoryTuningTab', 'default_on': False},
    'numa_node_tuning': {
        'name': 'NUMA Node Tuning',
        'class': 'NUMANodeTuningTab',
        'default_on': False,
    },
    'block_io_tuning': {
        'name': 'Block I/O Tuning',
        'class': 'BlockIOTuningTab',
        'default_on': False,
    },
    'resource_partitioning': {
        'name': 'Resource Partitioning',
        'class': 'ResourcePartitioningTab',
        'default_on': False,
    },
    'fibre_channel_vmid': {
        'name': 'Fibre Channel VMID',
        'class': 'FibreChannelVMIDTab',
        'default_on': False,
    },
    'cpu_model_topology': {
        'name': 'CPU Model and Topology',
        'class': 'CPUModelTopologyTab',
        'default_on': False,
    },
    'events_configuration': {
        'name': 'Events Configuration',
        'class': 'EventsConfigurationTab',
        'default_on': False,
    },
    'power_management': {
        'name': 'Power Management',
        'class': 'PowerManagementTab',
        'default_on': False,
    },
    'disk_throttle_group': {
        'name': 'Disk Throttle Group',
        'class': 'DiskThrottleGroupTab',
        'default_on': False,
    },
    'hypervisor_features': {
        'name': 'Hypervisor Features',
        'class': 'HypervisorFeaturesTab',
        'default_on': False,
    },
    'time_keeping': {'name': 'Time Keeping', 'class': 'TimeKeepingTab', 'default_on': False},
    'performance_monitoring': {
        'name': 'Performance Monitoring',
        'class': 'PerformanceMonitoringTab',
        'default_on': False,
    },
    'security_label': {'name': 'Security Label', 'class': 'SecurityLabelTab', 'default_on': False},
    'key_wrap': {'name': 'Key Wrap', 'class': 'KeyWrapTab', 'default_on': False},
    'launch_security': {
        'name': 'Launch Security',
        'class': 'LaunchSecurityTab',
        'default_on': False,
    },
}


class VmPanel(ctk.CTkFrame):
    """虚拟机 XML 配置生成面板 - 24 Tab 版本."""

    def __init__(self, parent: ctk.CTk) -> None:
        """初始化 VmPanel."""
        super().__init__(parent)
        self.corner_radius = 10
        self.fg_color = 'transparent'

        # 主布局：1 行 1 列
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.vm_config = VMConfig()  # VM 配置管理实例
        self._updating_xml = False  # 防止递归更新

        # Tab 管理
        self.tab_instances = {}  # 存储已创建的 Tab 实例
        self.tab_enabled = {}  # 存储 Tab 启用状态

        # 初始化 UI
        self.init_ui()

    def init_ui(self) -> None:
        """初始化界面."""
        # 主框架 - 填满整个 VmPanel
        main_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_MAIN, corner_radius=8)
        main_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # 配置 VmPanel 的网格权重
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # 配置内部网格
        main_frame.grid_rowconfigure(0, weight=0)  # 工具栏
        main_frame.grid_rowconfigure(1, weight=0)  # Tab 开关面板
        main_frame.grid_rowconfigure(2, weight=1)  # Tab 配置区
        main_frame.grid_rowconfigure(3, weight=0)  # XML 预览区
        main_frame.grid_rowconfigure(4, weight=0)  # 信息栏
        main_frame.grid_columnconfigure(0, weight=1)

        # 顶部工具栏
        self._create_toolbar(main_frame)

        # Tab 开关面板
        self.tab_toggle_panel = TabTogglePanel(
            main_frame,
            on_tab_toggle_callback=self._on_tab_toggle,
        )
        self.tab_toggle_panel.grid(row=1, column=0, padx=15, pady=(5, 10), sticky='ew')

        # Tab 配置区 - 使用 CTkTabview
        self.tabview = ctk.CTkTabview(
            main_frame,
            segmented_button_selected_color=('#3B8ED0', '#1F6AA5'),
            segmented_button_unselected_color=('#DCE4EE', '#2B2B2B'),
            text_color=('gray10', '#DCE4EE'),
        )
        self.tabview.grid(row=2, column=0, padx=15, pady=(5, 10), sticky='nsew')

        # 初始化 Tab 状态
        for tab_key, config in TABS_CONFIG.items():
            self.tab_enabled[tab_key] = config.get('default_on', False)

        # 初始化各个 Tab
        self._init_tabs()

        # 底部 XML 预览区
        self._create_xml_preview(main_frame)

        # 底部信息栏
        self._create_info_bar(main_frame)

        # 初始生成 XML
        self._update_xml_preview()

    def _on_tab_toggle(self, tab_key: str, enabled: bool) -> None:
        """Tab 开关改变时的回调."""
        tab_config = TABS_CONFIG.get(tab_key)
        if not tab_config:
            return

        tab_name = tab_config['name']

        if enabled:
            # 开关打开：添加 Tab
            tab = self.tabview.add(tab_name)
            tab.grid_columnconfigure(0, weight=1)
            tab.grid_rowconfigure(0, weight=1)

            # 导入 Tab 类
            from .tabs import (
                BasicTab,
                BlockIOTuningTab,
                CPUAllocationTab,
                CPUModelTopologyTab,
                CPUTuningTab,
                DevicesTab,
                DiskThrottleGroupTab,
                EventsConfigurationTab,
                FibreChannelVMIDTab,
                HypervisorFeaturesTab,
                IOThreadsAllocationTab,
                KeyWrapTab,
                LaunchSecurityTab,
                MemoryAllocationTab,
                MemoryBackingTab,
                MemoryTuningTab,
                NUMANodeTuningTab,
                OSTab,
                PerformanceMonitoringTab,
                PowerManagementTab,
                ResourcePartitioningTab,
                SecurityLabelTab,
                SMBIOSSystemTab,
                TimeKeepingTab,
            )

            # Tab 类映射
            tab_classes = {
                'BasicTab': BasicTab,
                'BlockIOTuningTab': BlockIOTuningTab,
                'CPUAllocationTab': CPUAllocationTab,
                'CPUModelTopologyTab': CPUModelTopologyTab,
                'CPUTuningTab': CPUTuningTab,
                'DevicesTab': DevicesTab,
                'DiskThrottleGroupTab': DiskThrottleGroupTab,
                'EventsConfigurationTab': EventsConfigurationTab,
                'FibreChannelVMIDTab': FibreChannelVMIDTab,
                'HypervisorFeaturesTab': HypervisorFeaturesTab,
                'IOThreadsAllocationTab': IOThreadsAllocationTab,
                'KeyWrapTab': KeyWrapTab,
                'LaunchSecurityTab': LaunchSecurityTab,
                'MemoryAllocationTab': MemoryAllocationTab,
                'MemoryBackingTab': MemoryBackingTab,
                'MemoryTuningTab': MemoryTuningTab,
                'NUMANodeTuningTab': NUMANodeTuningTab,
                'OSTab': OSTab,
                'PerformanceMonitoringTab': PerformanceMonitoringTab,
                'PowerManagementTab': PowerManagementTab,
                'ResourcePartitioningTab': ResourcePartitioningTab,
                'SecurityLabelTab': SecurityLabelTab,
                'SMBIOSSystemTab': SMBIOSSystemTab,
                'TimeKeepingTab': TimeKeepingTab,
            }

            # 创建 Tab 实例
            tab_class = tab_classes.get(tab_config['class'])
            if tab_class:
                tab_instance = tab_class(
                    tab,
                    on_change_callback=self._update_xml_preview,
                )
                tab_instance.grid(row=0, column=0, sticky='nsew')
                self.tab_instances[tab_key] = {'tab': tab, 'widget': tab_instance}

                # 切换到该 Tab
                self.tabview.set(tab_name)
                self.update_info(f'已启用 Tab: {tab_name}')
        else:
            # 开关关闭：从 TabView 中移除 Tab
            if tab_key in self.tab_instances:
                try:
                    self.tabview.delete(tab_name)
                except Exception:
                    pass

                del self.tab_instances[tab_key]

            self.tab_enabled[tab_key] = False
            self.update_info(f'已禁用 Tab: {tab_name}')

        # 更新 XML 预览
        self._update_xml_preview()

    def _create_toolbar(self, parent) -> None:
        """创建顶部工具栏."""
        toolbar = ctk.CTkFrame(parent, fg_color='transparent')
        toolbar.grid(row=0, column=0, padx=15, pady=10, sticky='ew')
        toolbar.grid_columnconfigure(0, weight=1)

        # 标题
        title_label = ctk.CTkLabel(
            toolbar,
            text='虚拟机 XML 配置生成器',
            font=CTK_FONT_BOLD,
            text_color='#64b5f6',
        )
        title_label.grid(row=0, column=0, sticky='w')

        # 按钮组
        btn_frame = ctk.CTkFrame(toolbar, fg_color='transparent')
        btn_frame.grid(row=0, column=1, sticky='e')

        # 清空按钮
        clear_btn = ctk.CTkButton(
            btn_frame,
            text='清空',
            command=self.clear_all,
            fg_color='#757575',
            hover_color='#616161',
            width=80,
            font=CTK_FONT_SMALL,
        )
        clear_btn.pack(side='left', padx=5)

        # 生成 XML 按钮
        generate_btn = ctk.CTkButton(
            btn_frame,
            text='生成 XML',
            command=self.generate_xml,
            fg_color='#2196f3',
            hover_color='#1976d2',
            width=100,
            font=CTK_FONT_SMALL,
        )
        generate_btn.pack(side='left', padx=5)

        # 保存按钮
        save_btn = ctk.CTkButton(
            btn_frame,
            text='保存 XML',
            command=self.save_xml,
            fg_color='#4caf50',
            hover_color='#388e3c',
            width=100,
            font=CTK_FONT_SMALL,
        )
        save_btn.pack(side='left', padx=5)

        # 创建虚拟机按钮
        create_btn = ctk.CTkButton(
            btn_frame,
            text='创建虚拟机',
            command=self.create_vm,
            fg_color='#9c27b0',
            hover_color='#7b1fa2',
            width=100,
            font=CTK_FONT_SMALL,
        )
        create_btn.pack(side='left', padx=5)

    def _init_tabs(self) -> None:
        """初始化所有启用的 Tab."""
        # 导入所有 Tab 类
        from .tabs import (
            BasicTab,
            BlockIOTuningTab,
            CPUAllocationTab,
            CPUModelTopologyTab,
            CPUTuningTab,
            DevicesTab,
            DiskThrottleGroupTab,
            EventsConfigurationTab,
            FibreChannelVMIDTab,
            HypervisorFeaturesTab,
            IOThreadsAllocationTab,
            KeyWrapTab,
            LaunchSecurityTab,
            MemoryAllocationTab,
            MemoryBackingTab,
            MemoryTuningTab,
            NUMANodeTuningTab,
            OSTab,
            PerformanceMonitoringTab,
            PowerManagementTab,
            ResourcePartitioningTab,
            SecurityLabelTab,
            SMBIOSSystemTab,
            TimeKeepingTab,
        )

        # Tab 类映射
        tab_classes = {
            'BasicTab': BasicTab,
            'BlockIOTuningTab': BlockIOTuningTab,
            'CPUAllocationTab': CPUAllocationTab,
            'CPUModelTopologyTab': CPUModelTopologyTab,
            'CPUTuningTab': CPUTuningTab,
            'DevicesTab': DevicesTab,
            'DiskThrottleGroupTab': DiskThrottleGroupTab,
            'EventsConfigurationTab': EventsConfigurationTab,
            'FibreChannelVMIDTab': FibreChannelVMIDTab,
            'HypervisorFeaturesTab': HypervisorFeaturesTab,
            'IOThreadsAllocationTab': IOThreadsAllocationTab,
            'KeyWrapTab': KeyWrapTab,
            'LaunchSecurityTab': LaunchSecurityTab,
            'MemoryAllocationTab': MemoryAllocationTab,
            'MemoryBackingTab': MemoryBackingTab,
            'MemoryTuningTab': MemoryTuningTab,
            'NUMANodeTuningTab': NUMANodeTuningTab,
            'OSTab': OSTab,
            'PerformanceMonitoringTab': PerformanceMonitoringTab,
            'PowerManagementTab': PowerManagementTab,
            'ResourcePartitioningTab': ResourcePartitioningTab,
            'SecurityLabelTab': SecurityLabelTab,
            'SMBIOSSystemTab': SMBIOSSystemTab,
            'TimeKeepingTab': TimeKeepingTab,
        }

        first_tab = None
        for tab_key, config in TABS_CONFIG.items():
            if config.get('default_on', False):
                tab_name = config['name']
                tab = self.tabview.add(tab_name)
                tab.grid_columnconfigure(0, weight=1)
                tab.grid_rowconfigure(0, weight=1)

                # 创建 Tab 实例
                tab_class = tab_classes.get(config['class'])
                if tab_class:
                    tab_instance = tab_class(
                        tab,
                        on_change_callback=self._update_xml_preview,
                    )
                    tab_instance.grid(row=0, column=0, sticky='nsew')
                    self.tab_instances[tab_key] = {'tab': tab, 'widget': tab_instance}

                    if first_tab is None:
                        first_tab = tab_name

        # 切换到第一个 Tab
        if first_tab:
            self.tabview.set(first_tab)

    def _create_xml_preview(self, parent) -> None:
        """创建 XML 预览区."""
        preview_frame = ctk.CTkFrame(parent, fg_color=BG_COLOR_CONTENT, corner_radius=8)
        preview_frame.grid(row=2, column=0, padx=15, pady=(0, 10), sticky='nsew')

        # 预览区标题
        preview_label = ctk.CTkLabel(
            preview_frame,
            text='XML 预览',
            font=CTK_FONT_BOLD,
            text_color='#ffb74d',
        )
        preview_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')

        # XML 文本框
        self.xml_textbox = ctk.CTkTextbox(
            preview_frame,
            font=CTK_FONT_MONO,
            fg_color=BG_COLOR_CONTENT,
            text_color='#f0f0f0',
            border_color='#333333',
            border_width=1,
            corner_radius=6,
            height=200,
        )
        self.xml_textbox.grid(row=1, column=0, padx=10, pady=(0, 10), sticky='nsew')
        preview_frame.grid_rowconfigure(1, weight=1)
        preview_frame.grid_columnconfigure(0, weight=1)

    def _create_info_bar(self, parent) -> None:
        """创建底部信息栏."""
        self.info_frame = ctk.CTkFrame(
            parent, fg_color=BG_COLOR_CONTENT, corner_radius=0, height=30
        )
        self.info_frame.grid(row=3, column=0, sticky='ew')
        self.info_frame.grid_propagate(False)

        self.info_label = ctk.CTkLabel(
            self.info_frame,
            text='就绪',
            font=CTK_FONT_SMALL,
            text_color='#aaaaaa',
            anchor='w',
        )
        self.info_label.pack(fill='x', padx=20, pady=5)

    def update_info(self, text: str, is_success: bool = True) -> None:
        """更新底部信息栏."""
        color = '#4caf50' if is_success else '#f44336'
        self.info_label.configure(text=text, text_color=color)

    def _update_xml_preview(self) -> None:
        """更新 XML 预览（不显示错误消息）."""
        if self._updating_xml:
            return
        self._updating_xml = True
        try:
            xml_str = self._build_xml_preview()
            self.xml_textbox.delete('1.0', END)
            self.xml_textbox.insert('1.0', xml_str)
        except Exception:
            # 配置不完整时显示空或部分内容
            pass
        finally:
            self._updating_xml = False

    def _build_xml_preview(self) -> str:
        """构建 XML 预览（不抛出错误）."""
        try:
            data = self.collect_vm_data()
            generator = LibvirtXMLGenerator()
            return generator.generate(data)
        except Exception:
            return '<!-- 配置不完整或无效，请检查输入 -->'

    # ========== 核心功能方法 ==========
    def clear_all(self) -> None:
        """清空所有配置."""
        if messagebox.askyesno('确认', '确定要清空所有配置吗？'):
            # 重置配置
            self.vm_config.reset()

            # 清空各 Tab
            for tab in self.tab_instances.values():
                widget = tab.get('widget')
                if widget and hasattr(widget, 'load_config'):
                    widget.load_config({})

            # 清空 XML 预览
            self.xml_textbox.delete('1.0', END)

            self.update_info('已清空所有配置')

    def collect_vm_data(self) -> dict:
        """收集虚拟机配置数据 - 通过各 Tab 的 to_xml 方法."""
        # 重置配置
        self.vm_config.reset()

        for tab_key, tab_info in self.tab_instances.items():
            if not self.tab_enabled.get(tab_key, False):
                continue

            widget = tab_info.get('widget')
            if hasattr(widget, 'to_xml'):
                try:
                    xml_config = widget.to_xml()
                    if isinstance(xml_config, dict):
                        self.vm_config.update_from_tab(tab_key, xml_config)
                except Exception:
                    pass

        return self.vm_config.to_dict()

    def generate_xml(self) -> None:
        """生成 XML 配置."""
        try:
            vm_data = self.collect_vm_data()
            generator = LibvirtXMLGenerator()
            xml_str = generator.generate(vm_data)
            self.xml_textbox.delete('1.0', END)
            self.xml_textbox.insert('1.0', xml_str)
            self.update_info('XML 生成成功')
        except ValueError as e:
            messagebox.showerror('错误', str(e))
            self.update_info(str(e), False)
        except Exception as e:
            messagebox.showerror('错误', f'生成失败：{e!s}')
            self.update_info(f'生成失败：{e!s}', False)

    def save_xml(self) -> None:
        """保存 XML 到文件."""
        xml_content = self.xml_textbox.get('1.0', END).strip()
        if not xml_content:
            messagebox.showwarning('警告', '请先生成 XML!')
            self.update_info('请先生成 XML', False)
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension='.xml',
            filetypes=[('XML 文件', '*.xml'), ('所有文件', '*.*')],
            title='保存 XML 文件',
            initialfile=f'{self.vm_config.basic.get("name", "vm")}.xml',
        )

        if not file_path:
            self.update_info('已取消保存', False)
            return

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(xml_content)
            messagebox.showinfo('成功', f'XML 已保存到:\n{file_path}')
            self.update_info(f'保存成功：{file_path}')
        except Exception as e:
            messagebox.showerror('错误', f'保存失败：{e!s}')
            self.update_info(f'保存失败：{e!s}', False)

    def create_vm(self) -> None:
        """通过 virsh 创建虚拟机."""
        xml_content = self.xml_textbox.get('1.0', END).strip()
        if not xml_content:
            messagebox.showwarning('警告', '请先生成 XML!')
            self.update_info('请先生成 XML', False)
            return

        try:
            # 尝试定义虚拟机
            result = subprocess.run(
                ['virsh', 'define', '--file', '-'],
                input=xml_content,
                capture_output=True,
                text=True,
                check=False,
            )

            if result.returncode == 0:
                vm_name = self.vm_config.basic.get('name', 'vm')
                messagebox.showinfo(
                    '成功',
                    f'虚拟机 {vm_name} 定义成功！\n\n请运行以下命令启动:\n  virsh start {vm_name}',
                )
                self.update_info(f'虚拟机 {vm_name} 定义成功')
            else:
                error_msg = result.stderr.strip()
                messagebox.showerror('错误', f'定义虚拟机失败:\n{error_msg}')
                self.update_info(f'定义失败：{error_msg}', False)

        except FileNotFoundError:
            messagebox.showerror(
                '错误',
                '未找到 virsh 命令!\n请确保已安装 libvirt-client 并以管理员/root 身份运行。',
            )
            self.update_info('未找到 virsh 命令', False)
        except Exception as e:
            messagebox.showerror('错误', f'创建失败：{e!s}')
            self.update_info(f'创建失败：{e!s}', False)
