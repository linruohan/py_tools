"""VmPanel - 虚拟机 XML 配置生成面板."""

import subprocess
import uuid
from tkinter import END, filedialog, messagebox

import customtkinter as ctk

from .styles import CTK_FONT_MAIN, CTK_FONT_BOLD, CTK_FONT_MONO, CTK_FONT_SMALL
from .styles import BG_COLOR_MAIN, BG_COLOR_CONTENT
from .xml_builder import build_libvirt_xml
from .tabs import (
    BasicTab,
    OSTab,
    StorageTab,
    NetworkTab,
    DevicesTab,
    FeaturesTab,
    HostdevTab,
    MemoryTab,
    ClockTab,
)


class VmPanel(ctk.CTkFrame):
    """虚拟机 XML 配置生成面板."""

    def __init__(self, parent: ctk.CTk) -> None:
        """初始化 VmPanel."""
        super().__init__(parent)
        self.corner_radius = 10
        self.fg_color = 'transparent'

        # 主布局：1 行 1 列
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.vm_data = {}
        self._updating_xml = False  # 防止递归更新

        # 初始化 UI
        self.init_ui()

    def init_ui(self) -> None:
        """初始化界面."""
        # 主框架
        main_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_MAIN, corner_radius=8)
        main_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # 配置内部网格
        main_frame.grid_rowconfigure(2, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # 顶部工具栏
        self._create_toolbar(main_frame)

        # Tab 配置区
        self.tabview = ctk.CTkTabview(
            main_frame,
            segmented_button_selected_color=('#3B8ED0', '#1F6AA5'),
            segmented_button_unselected_color=('#DCE4EE', '#2B2B2B'),
            text_color=('gray10', '#DCE4EE'),
        )
        self.tabview.grid(row=1, column=0, padx=15, pady=10, sticky='nsew')

        # 添加配置 Tab - 按 libvirt 规范分类
        self.tab_basic = self.tabview.add('基础配置')
        self.tab_os = self.tabview.add('引导/OS')
        self.tab_storage = self.tabview.add('存储')
        self.tab_network = self.tabview.add('网络')
        self.tab_devices = self.tabview.add('设备')
        self.tab_features = self.tabview.add('功能特性')
        self.tab_hostdev = self.tabview.add('PCI 直通')
        self.tab_memory = self.tabview.add('内存管理')
        self.tab_clock = self.tabview.add('时钟/看门狗')

        # 配置每个 Tab 的网格
        for tab_name in ['基础配置', '引导/OS', '存储', '网络', '设备', '功能特性', 'PCI 直通', '内存管理', '时钟/看门狗']:
            tab = self.tabview.tab(tab_name)
            tab.grid_columnconfigure(0, weight=1)
            tab.grid_rowconfigure(0, weight=1)

        # 初始化各个 Tab
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

    def _init_tabs(self) -> None:
        """初始化所有 Tab."""
        # 基础配置 Tab
        self.basic_tab = BasicTab(self.tab_basic)
        self.basic_tab.grid(row=0, column=0, sticky='nsew')

        # 引导/OS Tab
        self.os_tab = OSTab(self.tab_os)
        self.os_tab.grid(row=0, column=0, sticky='nsew')

        # 存储 Tab
        self.storage_tab = StorageTab(self.tab_storage, on_change_callback=self._update_xml_preview)
        self.storage_tab.grid(row=0, column=0, sticky='nsew')

        # 网络 Tab
        self.network_tab = NetworkTab(self.tab_network, on_change_callback=self._update_xml_preview)
        self.network_tab.grid(row=0, column=0, sticky='nsew')

        # 设备 Tab
        self.devices_tab = DevicesTab(self.tab_devices, on_change_callback=self._update_xml_preview)
        self.devices_tab.grid(row=0, column=0, sticky='nsew')

        # 功能特性 Tab
        self.features_tab = FeaturesTab(self.tab_features, on_change_callback=self._update_xml_preview)
        self.features_tab.grid(row=0, column=0, sticky='nsew')

        # PCI 直通 Tab
        self.hostdev_tab = HostdevTab(self.tab_hostdev, on_change_callback=self._update_xml_preview)
        self.hostdev_tab.grid(row=0, column=0, sticky='nsew')

        # 内存管理 Tab
        self.memory_tab = MemoryTab(self.tab_memory, on_change_callback=self._update_xml_preview)
        self.memory_tab.grid(row=0, column=0, sticky='nsew')

        # 时钟/看门狗 Tab
        self.clock_tab = ClockTab(self.tab_clock, on_change_callback=self._update_xml_preview)
        self.clock_tab.grid(row=0, column=0, sticky='nsew')

        # 保存引用以便访问
        self.vm_name_entry = self.basic_tab.vm_name_entry
        self.vm_desc_entry = self.basic_tab.vm_desc_entry
        self.uuid_entry = self.basic_tab.uuid_entry
        self.machine_type = self.basic_tab.machine_type
        self.virt_type = self.basic_tab.virt_type
        self.chipset_type = self.basic_tab.chipset_type
        self.vcpu_entry = self.basic_tab.vcpu_entry
        self.cpu_mode = self.basic_tab.cpu_mode
        self.memory_entry = self.basic_tab.memory_entry
        self.current_memory_entry = self.basic_tab.current_memory_entry
        self.max_memory_entry = self.basic_tab.max_memory_entry
        self.swap_entry = self.basic_tab.swap_entry

        self.firmware_type = self.os_tab.firmware_type
        self.secure_boot = self.os_tab.secure_boot
        self.boot_device_1 = self.os_tab.boot_device_1
        self.boot_device_2 = self.os_tab.boot_device_2
        self.boot_device_3 = self.os_tab.boot_device_3
        self.boot_timeout_entry = self.os_tab.boot_timeout_entry

        self.disk_frame = self.storage_tab.disk_frame
        self.network_frame = self.network_tab.network_frame

        self.graphics_type = self.devices_tab.graphics_type
        self.graphics_listen = self.devices_tab.graphics_listen
        self.video_model = self.devices_tab.video_model
        self.vram_entry = self.devices_tab.vram_entry
        self.usb_controller = self.devices_tab.usb_controller
        self.usb_entry = self.devices_tab.usb_entry
        self.usb_list = self.devices_tab.usb_list
        self.usb_display = self.devices_tab.usb_display
        self.disable_usb_check = self.devices_tab.disable_usb_check
        self.disable_sound_check = self.devices_tab.disable_sound_check

        self.acpi_check = self.features_tab.acpi_check
        self.apic_check = self.features_tab.apic_check
        self.hyperv_check = self.features_tab.hyperv_check
        self.iommu_check = self.features_tab.iommu_check

        self.hostdev_frame = self.hostdev_tab.hostdev_frame

        self.balloon_check = self.memory_tab.balloon_check
        self.balloon_target_entry = self.memory_tab.balloon_target_entry

        self.watchdog_model = self.clock_tab.watchdog_model
        self.watchdog_action = self.clock_tab.watchdog_action
        self.rtc_clock = self.clock_tab.rtc_clock
        self.kvm_clock_check = self.clock_tab.kvm_clock_check

    def _create_xml_preview(self, parent) -> None:
        """创建 XML 预览区."""
        preview_frame = ctk.CTkFrame(parent, fg_color=BG_COLOR_CONTENT, corner_radius=8)
        preview_frame.grid(row=2, column=0, padx=15, pady=(0, 10), sticky='nsew')
        parent.grid_rowconfigure(2, weight=1)

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

    def _bind_basic_events(self) -> None:
        """绑定基础配置的变化事件，实现动态 XML 预览."""
        # 绑定 Entry 的 KeyRelease 事件
        entry_widgets = [
            self.vm_name_entry, self.vm_desc_entry, self.uuid_entry,
            self.vcpu_entry, self.memory_entry, self.current_memory_entry,
            self.max_memory_entry, self.swap_entry, self.boot_timeout_entry,
            self.graphics_listen, self.vram_entry, self.balloon_target_entry,
        ]
        for widget in entry_widgets:
            widget.bind('<KeyRelease>', lambda e: self._update_xml_preview())

        # 绑定 OptionMenu 的变化事件（使用 lambda 忽略参数）
        option_widgets = [
            self.virt_type, self.machine_type, self.chipset_type,
            self.cpu_mode, self.firmware_type,
            self.boot_device_1, self.boot_device_2, self.boot_device_3,
            self.graphics_type, self.video_model, self.usb_controller,
            self.watchdog_model, self.watchdog_action, self.rtc_clock,
        ]
        for widget in option_widgets:
            widget.configure(command=lambda *args: self._update_xml_preview())

        # 绑定 Checkbox 的变化事件
        checkbox_widgets = [
            self.secure_boot, self.disable_usb_check, self.disable_sound_check,
            self.acpi_check, self.apic_check, self.hyperv_check, self.iommu_check,
            self.balloon_check, self.kvm_clock_check,
        ]
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
            return build_libvirt_xml(data)
        except Exception:
            return '<!-- 配置不完整或无效，请检查输入 -->'

    # ========== 存储配置方法 ==========
    def add_disk(self) -> None:
        """添加磁盘配置行."""
        self.storage_tab.add_disk()

    def add_cdrom(self) -> None:
        """添加光驱配置行."""
        self.storage_tab.add_cdrom()

    # ========== 网络配置方法 ==========
    def add_network(self) -> None:
        """添加网络配置行."""
        self.network_tab.add_network()

    # ========== 高级配置方法 ==========
    def add_hostdev(self) -> None:
        """添加 PCI 直通设备."""
        self.hostdev_tab.add_hostdev()

    def add_usb(self) -> None:
        """添加 USB 设备."""
        self.devices_tab.add_usb()

    # ========== 核心功能方法 ==========
    def clear_all(self) -> None:
        """清空所有配置."""
        if messagebox.askyesno('确认', '确定要清空所有配置吗？'):
            # 清空基础配置 Tab
            self.basic_tab.vm_name_entry.delete(0, END)
            self.basic_tab.vm_desc_entry.delete(0, END)
            self.basic_tab.uuid_entry.delete(0, END)
            self.basic_tab.machine_type.set('q35')
            self.basic_tab.virt_type.set('hvm')
            self.basic_tab.chipset_type.set('Q35')
            self.basic_tab.vcpu_entry.delete(0, END)
            self.basic_tab.vcpu_entry.insert(0, '2')
            self.basic_tab.cpu_mode.set('host-model')
            self.basic_tab.memory_entry.delete(0, END)
            self.basic_tab.memory_entry.insert(0, '2048')
            self.basic_tab.current_memory_entry.delete(0, END)
            self.basic_tab.current_memory_entry.insert(0, '2048')
            self.basic_tab.max_memory_entry.delete(0, END)
            self.basic_tab.max_memory_entry.insert(0, '4096')
            self.basic_tab.swap_entry.delete(0, END)
            self.basic_tab.swap_entry.insert(0, '0')

            # 清空引导/OS Tab
            self.os_tab.firmware_type.set('BIOS')
            self.os_tab.secure_boot.deselect()
            self.os_tab.boot_device_1.set('hd')
            self.os_tab.boot_device_2.set('cdrom')
            self.os_tab.boot_device_3.set('none')
            self.os_tab.boot_timeout_entry.delete(0, END)
            self.os_tab.boot_timeout_entry.insert(0, '-1')

            # 清空存储 Tab
            for entry in self.storage_tab.disk_frame.disk_entries[:]:
                self.storage_tab.disk_frame.remove_disk(entry['frame'])

            # 清空网络 Tab
            for entry in self.network_tab.network_frame.network_entries[:]:
                self.network_tab.network_frame.remove_network(entry['frame'])

            # 清空设备 Tab
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

            # 清空功能特性 Tab
            self.features_tab.acpi_check.select()
            self.features_tab.apic_check.select()
            self.features_tab.hyperv_check.deselect()
            self.features_tab.iommu_check.deselect()

            # 清空 PCI 直通 Tab
            for entry in self.hostdev_tab.hostdev_frame.hostdev_entries[:]:
                self.hostdev_tab.hostdev_frame.remove_hostdev(entry['frame'])

            # 清空内存管理 Tab
            self.memory_tab.balloon_check.deselect()
            self.memory_tab.balloon_target_entry.delete(0, END)
            self.memory_tab.balloon_target_entry.insert(0, '2048')
            self.memory_tab.balloon_target_entry.configure(state='disabled')

            # 清空时钟/看门狗 Tab
            self.clock_tab.watchdog_model.set('none')
            self.clock_tab.watchdog_action.set('reset')
            self.clock_tab.rtc_clock.set('utc')
            self.clock_tab.kvm_clock_check.select()

            # 清空 XML 预览
            self.xml_textbox.delete('1.0', END)

            self.update_info('已清空所有配置')

    def collect_vm_data(self) -> dict:
        """收集虚拟机配置数据."""
        vm_name = self.vm_name_entry.get().strip()
        if not vm_name:
            raise ValueError('虚拟机名称不能为空!')

        # 收集 UUID（如果没有则生成）
        uuid_val = self.uuid_entry.get().strip()
        if not uuid_val:
            uuid_val = str(uuid.uuid4())

        # 收集引导设备
        boot_devices = []
        for dev in [self.boot_device_1.get(), self.boot_device_2.get(), self.boot_device_3.get()]:
            if dev and dev != 'none':
                boot_devices.append(dev)

        return {
            'name': vm_name,
            'description': self.vm_desc_entry.get().strip(),
            'uuid': uuid_val,
            'vcpu': int(self.vcpu_entry.get().strip() or '2'),
            'cpu_mode': self.cpu_mode.get(),
            'memory': int(self.memory_entry.get().strip() or '2048'),
            'current_memory': int(self.current_memory_entry.get().strip() or self.memory_entry.get().strip() or '2048'),
            'max_memory': int(self.max_memory_entry.get().strip() or '4096'),
            'swap': int(self.swap_entry.get().strip() or '0'),
            'virt_type': self.virt_type.get(),
            'machine': self.machine_type.get().strip() or 'q35',
            'chipset': self.chipset_type.get(),
            'firmware': self.firmware_type.get(),
            'secure_boot': self.secure_boot.get(),
            'boot_devices': boot_devices,
            'boot_timeout': int(self.boot_timeout_entry.get().strip() or '-1'),
            'disks': self.storage_tab.get_disks(),
            'networks': self.network_tab.get_networks(),
            'hostdevs': self.hostdev_tab.get_hostdevs(),
            'graphics': self.devices_tab.get_graphics_config(),
            'usb': self.devices_tab.get_usb_config(),
            'features': self.features_tab.get_features(),
            'watchdog': self.clock_tab.get_watchdog_config(),
            'balloon': self.memory_tab.get_balloon_config(),
            'clock': self.clock_tab.get_clock_config(),
        }

    def generate_xml(self) -> None:
        """生成 XML 配置."""
        try:
            self.vm_data = self.collect_vm_data()
            xml_str = build_libvirt_xml(self.vm_data)
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
                    '成功', f'虚拟机 {vm_name} 定义成功!\n\n请运行以下命令启动:\n  virsh start {vm_name}'
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
