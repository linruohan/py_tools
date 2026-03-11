"""VmPanel - 虚拟机 XML 配置生成面板."""

import subprocess

from tkinter import END, filedialog, messagebox

import customtkinter as ctk

from .styles import (
    BG_COLOR_CONTENT,
    BG_COLOR_MAIN,
    CTK_FONT_BOLD,
    CTK_FONT_MAIN,
    CTK_FONT_MONO,
    CTK_FONT_SMALL,
)
from .tab_toggle import TabTogglePanel
from .xml_generator import LibvirtXMLGenerator


class VmPanel(ctk.CTkFrame):
    """虚拟机 XML 配置生成面板."""

    def __init__(self, parent: ctk.CTk) -> None:
        """初始化 VmPanel."""
        super().__init__(parent)
        self.corner_radius = 10
        self.fg_color = 'transparent'

        # 主布局：1 行 1 列
        self.grid_columnconfigure(0, weight=1)

        self.vm_data = {}
        self._updating_xml = False  # 防止递归更新

        # Tab 管理
        self.tab_instances = {}  # 存储已创建的 Tab 实例
        self.tab_enabled = {}  # 存储 Tab 启用状态

        # 从 TabTogglePanel 获取默认配置
        self.tabs_default_config = {
            tab_key: config.get('default_on', False)
            for tab_key, config in TabTogglePanel.TABS_CONFIG.items()
        }

        # 初始化 UI
        self.init_ui()

    def init_ui(self) -> None:
        """初始化界面."""
        # 主框架
        main_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_MAIN, corner_radius=8)
        main_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # 配置 VmPanel 自身的网格权重，确保 main_frame 能正确扩展
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # 配置内部网格 - 合理分配权重让控件占满空间
        main_frame.grid_rowconfigure(0, weight=0)  # 工具栏
        main_frame.grid_rowconfigure(1, weight=0)  # Tab 开关面板
        main_frame.grid_rowconfigure(2, weight=1)  # Tab 配置区（主要区域）
        main_frame.grid_rowconfigure(3, weight=1)  # XML 预览区
        main_frame.grid_rowconfigure(4, weight=0)  # 信息栏
        main_frame.grid_columnconfigure(0, weight=1)

        # 确保 tabview 内部的 tab 页面也能正确扩展
        # 需要在 tabview 创建后配置其内部页面

        # 顶部工具栏
        self._create_toolbar(main_frame)

        # Tab 开关面板
        self.tab_toggle_panel = TabTogglePanel(
            main_frame,
            on_tab_toggle_callback=self._on_tab_toggle,
        )
        self.tab_toggle_panel.grid(row=1, column=0, padx=15, pady=(5, 10), sticky='ew')

        # Tab 配置区
        self.tabview = ctk.CTkTabview(
            main_frame,
            segmented_button_selected_color=('#3B8ED0', '#1F6AA5'),
            segmented_button_unselected_color=('#DCE4EE', '#2B2B2B'),
            text_color=('gray10', '#DCE4EE'),
        )
        self.tabview.grid(row=2, column=0, padx=15, pady=(5, 10), sticky='nsew')

        # 初始化默认启用的 Tab 状态
        for tab_key, default_enabled in self.tabs_default_config.items():
            self.tab_enabled[tab_key] = default_enabled

        # 添加默认启用的 Tab
        first_tab = None
        for tab_key, enabled in self.tab_enabled.items():
            if enabled:
                tab_name = TabTogglePanel.TABS_CONFIG[tab_key]['name']
                tab = self.tabview.add(tab_name)
                self.tab_instances[tab_key] = {'tab': tab, 'widget': None}

                # 配置网格
                tab.grid_columnconfigure(0, weight=1)
                tab.grid_rowconfigure(0, weight=1)

                # 记录第一个 tab
                if first_tab is None:
                    first_tab = tab_name

        # 在初始化 tab 内容之前，先切换到第一个 tab，确保 tab 页面已激活
        if first_tab:
            self.tabview.set(first_tab)

        # 初始化各个 Tab 的内容
        self._init_tabs()

        # 底部 XML 预览区
        self._create_xml_preview(main_frame)

        # 底部信息栏
        self._create_info_bar(main_frame)

        # 绑定所有基础配置的变化事件，实现动态 XML 预览
        self._bind_basic_events()

        # 初始生成 XML
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

    def _on_tab_toggle(self, tab_key: str, enabled: bool) -> None:
        """Tab 开关改变时的回调，参考 001.py 的 toggle_tab 实现."""
        tab_config = TabTogglePanel.TABS_CONFIG.get(tab_key)
        if not tab_config:
            return

        tab_name = tab_config['name']

        if enabled:
            # 开关打开：添加/恢复 Tab
            # 检查 Tab 是否已在 tab_instances 中
            if tab_key not in self.tab_instances:
                # Tab 不存在，创建新 Tab
                tab = self.tabview.add(tab_name)
                self.tab_instances[tab_key] = {'tab': tab, 'widget': None}

                # 配置网格
                tab.grid_columnconfigure(0, weight=1)
                tab.grid_rowconfigure(0, weight=1)

                # 创建 Tab 内容
                self._create_tab_content(tab_key, tab)

                # 切换到此 Tab
                self.tabview.set(tab_name)
            elif self.tab_instances[tab_key].get('widget') is None:
                # Tab 在 tab_instances 中但 widget 不存在，需要重新创建
                # 对于默认 Tab，tab 可能已经在 tabview 中（只是被隐藏了）
                tab = self.tab_instances[tab_key]['tab']

                # 如果 tab 也不存在了，需要重新添加
                try:
                    self.tabview.tab(tab_name)
                except ValueError:
                    # tab 不存在，重新添加
                    tab = self.tabview.add(tab_name)
                    self.tab_instances[tab_key]['tab'] = tab

                # 重新创建 Tab 内容
                self._create_tab_content(tab_key, tab)

                # 切换到此 Tab
                self.tabview.set(tab_name)

            self.tab_enabled[tab_key] = True
            self.update_info(f'已启用 Tab: {tab_name}')
        else:
            # 开关关闭：隐藏 Tab
            if tab_key in self.tab_instances:
                tab_widget = self.tab_instances[tab_key].get('widget')
                if tab_widget:
                    tab_widget.destroy()
                    self.tab_instances[tab_key]['widget'] = None

                # 尝试从 tabview 中删除 tab
                try:
                    self.tabview.delete(tab_name)
                except ValueError:
                    # 标签页不存在，无需处理
                    pass

            self.tab_enabled[tab_key] = False
            self.update_info(f'已禁用 Tab: {tab_name}')

        # 更新 XML 预览
        self._update_xml_preview()

    def _create_tab_content(self, tab_key: str, tab_parent) -> None:
        """创建 Tab 内容."""
        tab_config = TabTogglePanel.TABS_CONFIG.get(tab_key)
        if not tab_config:
            return

        tab_class = tab_config.get('class')
        has_callback = tab_config.get('has_callback', False)

        # 如果 Tab 类未实现（为 None），显示占位符
        if tab_class is None:
            placeholder = ctk.CTkLabel(
                tab_parent,
                text=f'{tab_config["name"]} - 功能开发中...\n(To be implemented)',
                font=CTK_FONT_MAIN,
                text_color='#888888',
            )
            placeholder.grid(row=0, column=0, padx=20, pady=20)
            self.tab_instances[tab_key] = {'tab': tab_parent, 'widget': placeholder}
            return

        if has_callback:
            tab_instance = tab_class(tab_parent, on_change_callback=self._update_xml_preview)
        else:
            tab_instance = tab_class(tab_parent)

        # 确保 tab_parent 的 grid 配置正确
        tab_parent.grid_columnconfigure(0, weight=1)
        tab_parent.grid_rowconfigure(0, weight=1)

        tab_instance.grid(row=0, column=0, sticky='nsew')
        self.tab_instances[tab_key]['widget'] = tab_instance

        # 更新引用
        self._update_tab_references()

    def _init_tabs(self) -> None:
        """初始化所有 Tab."""
        # 通过统一方法创建所有 Tab 内容
        for tab_key in TabTogglePanel.TABS_CONFIG:
            tab_info = self.tab_instances.get(tab_key)
            if tab_info:
                tab_widget = tab_info['tab']
                if tab_widget:
                    self._create_tab_content(tab_key, tab_widget)

        # 更新引用
        self._update_tab_references()

    def _update_tab_references(self) -> None:
        """更新 Tab 引用."""
        # Basic Tab
        if 'general_metadata' in self.tab_instances and self.tab_instances['general_metadata'].get(
            'widget'
        ):
            self.basic_tab = self.tab_instances['general_metadata']['widget']
            self.name_entry = self.basic_tab.vm_name_entry
            self.title_entry = self.basic_tab.vm_desc_entry
            self.uuid_entry = self.basic_tab.uuid_entry
            self.machine_entry = self.basic_tab.machine_type
            self.virt_type_entry = self.basic_tab.virt_type
            self.chipset_entry = self.basic_tab.chipset_type
            self.vcpu_entry = self.basic_tab.vcpu_entry
            self.cpu_mode_entry = self.basic_tab.cpu_mode
            self.memory_entry = self.basic_tab.memory_combo
            self.current_memory_entry = self.basic_tab.current_memory_combo
            self.max_memory_entry = self.basic_tab.max_memory_combo
            self.swap_entry = self.basic_tab.swap_entry

        # Storage Tab
        if 'storage' in self.tab_instances and self.tab_instances['storage'].get('widget'):
            self.storage_tab = self.tab_instances['storage']['widget']

        # Devices Tab
        if 'devices' in self.tab_instances and self.tab_instances['devices'].get('widget'):
            self.devices_tab = self.tab_instances['devices']['widget']
            self.graphics_type = self.devices_tab.graphics_type
            self.graphics_listen = self.devices_tab.graphics_listen
            self.graphics_port = self.devices_tab.graphics_port
            self.video_model = self.devices_tab.video_model
            self.vram_entry = self.devices_tab.vram_entry
            self.usb_controller = self.devices_tab.usb_controller
            self.usb_entry = self.devices_tab.usb_entry
            self.usb_list = self.devices_tab.usb_list
            self.usb_display = self.devices_tab.usb_display
            self.disable_usb_check = self.devices_tab.disable_usb_check
            self.disable_sound_check = self.devices_tab.disable_sound_check
            self.serial_type = self.devices_tab.serial_type
            self.serial_port = self.devices_tab.serial_port
            self.tpm_model = self.devices_tab.tpm_model
            self.tpm_version = self.devices_tab.tpm_version
            self.audio_model = self.devices_tab.audio_model

    def _create_xml_preview(self, parent) -> None:
        """创建 XML 预览区."""
        preview_frame = ctk.CTkFrame(parent, fg_color=BG_COLOR_CONTENT, corner_radius=8)
        preview_frame.grid(row=3, column=0, padx=15, pady=(0, 10), sticky='nsew')

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
        )
        self.xml_textbox.grid(row=1, column=0, padx=10, pady=(0, 10), sticky='nsew')
        preview_frame.grid_rowconfigure(1, weight=1)
        preview_frame.grid_columnconfigure(0, weight=1)

    def _create_info_bar(self, parent) -> None:
        """创建底部信息栏."""
        self.info_frame = ctk.CTkFrame(
            parent, fg_color=BG_COLOR_CONTENT, corner_radius=0, height=30
        )
        self.info_frame.grid(row=4, column=0, sticky='ew')
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

    def _bind_basic_events(self) -> None:
        """绑定基础配置的变化事件，实现动态 XML 预览."""
        # 绑定 Basic Tab 中的控件
        if hasattr(self, 'basic_tab'):
            # Basic Tab 的所有输入框已经在 basic_tab.py 中绑定了 KeyRelease 事件
            # 这里只需要确保文本框的变化能触发更新
            pass

        # 绑定 Devices Tab 中的控件
        if hasattr(self, 'devices_tab'):
            # 绑定 Entry 的 KeyRelease 事件
            entry_widgets = []
            if hasattr(self, 'graphics_listen'):
                entry_widgets.append(self.graphics_listen)
            if hasattr(self, 'graphics_port'):
                entry_widgets.append(self.graphics_port)
            if hasattr(self, 'vram_entry'):
                entry_widgets.append(self.vram_entry)

            for widget in entry_widgets:
                widget.bind('<KeyRelease>', lambda e: self._update_xml_preview())

            # 绑定 OptionMenu 的变化事件
            option_widgets = []
            if hasattr(self, 'graphics_type'):
                option_widgets.append(self.graphics_type)
            if hasattr(self, 'video_model'):
                option_widgets.append(self.video_model)
            if hasattr(self, 'usb_controller'):
                option_widgets.append(self.usb_controller)
            if hasattr(self, 'serial_type'):
                option_widgets.append(self.serial_type)
            if hasattr(self, 'tpm_model'):
                option_widgets.append(self.tpm_model)
            if hasattr(self, 'tpm_version'):
                option_widgets.append(self.tpm_version)
            if hasattr(self, 'audio_model'):
                option_widgets.append(self.audio_model)

            for widget in option_widgets:
                widget.configure(command=lambda *args: self._update_xml_preview())

            # 绑定 Checkbox 的变化事件
            checkbox_widgets = []
            if hasattr(self, 'disable_usb_check'):
                checkbox_widgets.append(self.disable_usb_check)
            if hasattr(self, 'disable_sound_check'):
                checkbox_widgets.append(self.disable_sound_check)

            for widget in checkbox_widgets:
                widget.configure(command=self._update_xml_preview)

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

    # ========== 设备配置方法 ==========
    def add_usb(self) -> None:
        """添加 USB 设备."""
        if hasattr(self, 'devices_tab'):
            self.devices_tab.add_usb()

    # ========== 核心功能方法 ==========
    def clear_all(self) -> None:
        """清空所有配置."""
        if messagebox.askyesno('确认', '确定要清空所有配置吗？'):
            # 清空 Devices Tab
            if hasattr(self, 'devices_tab'):
                self.devices_tab.graphics_type.set('vnc')
                self.devices_tab.graphics_listen.delete(0, END)
                self.devices_tab.graphics_listen.insert(0, '0.0.0.0')
                self.devices_tab.video_model.set('qxl')
                self.devices_tab.vram_entry.delete(0, END)
                self.devices_tab.vram_entry.insert(0, '64')
                self.devices_tab.usb_controller.set('qemu-xhci')
                self.devices_tab.disable_usb_check.deselect()
                self.devices_tab.disable_sound_check.deselect()
                self.devices_tab.usb_list.clear()
                self.devices_tab.usb_display.configure(text='')
                self.devices_tab.usb_entry.delete(0, END)

            # 清空 XML 预览
            self.xml_textbox.delete('1.0', END)

            self.update_info('已清空所有配置')

    def collect_vm_data(self) -> dict:
        """收集虚拟机配置数据 - 通过各Tab的to_xml方法."""
        data = {}

        for tab_key, tab_info in self.tab_instances.items():
            if not self.tab_enabled.get(tab_key, False):
                continue

            widget = tab_info.get('widget')
            if widget and hasattr(widget, 'to_xml'):
                try:
                    xml_config = widget.to_xml()
                    if isinstance(xml_config, dict):
                        for key, value in xml_config.items():
                            if key in data:
                                if isinstance(data[key], dict) and isinstance(value, dict):
                                    data[key].update(value)
                                else:
                                    data[key] = value
                            else:
                                data[key] = value
                except Exception:
                    pass

        return data

    def generate_xml(self) -> None:
        """生成 XML 配置."""
        try:
            self.vm_data = self.collect_vm_data()
            generator = LibvirtXMLGenerator()
            xml_str = generator.generate(self.vm_data)
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
            initialfile=f'{self.vm_data.get("name", "vm")}.xml',
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
                vm_name = self.vm_data.get('name', 'vm')
                messagebox.showinfo(
                    '成功',
                    f'虚拟机 {vm_name} 定义成功!\n\n请运行以下命令启动:\n  virsh start {vm_name}',
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
