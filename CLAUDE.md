# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

基于 `customtkinter` 的桌面应用工具箱，提供现代化 UI 界面。

## 开发命令

### 代码检查与格式化
```bash
ruff check           # 检查语法错误
ruff check --fix     # 检查并自动修复
ruff format          # 格式化代码
```

### 运行应用
```bash
python main.py       # 运行主应用
python drag.py       # 运行拖拽示例
python example/simple_example.py  # 运行简单示例
```

### 打包
```bash
# PyInstaller 方式
pyinstaller main.spec

# Nuitka 方式
python -m nuitka --follow-imports --enable-plugin=tk-inter --include-package=customtkinter --include-data-dir=test_images=test_images --include-data-files=readme.md=readme.md --warn-unusual-code --warn-implicit-exceptions --nofollow-import-to=tkinter.test --nofollow-import-to=PIL.ImageQt --remove-output --output-dir=dist --output-file=PyTools --standalone --windows-console-mode=disable --windows-icon-from-ico=mytool.ico main.py
```

## 代码架构

### 核心结构
- `main.py` - 应用入口，使用 `CTk` 创建主窗口，含左侧导航栏和多面板切换逻辑
- `panels/` - 功能面板模块
  - `home_panel.py` - 主页面板，包含多 Tab 展示各种 CTk 组件
  - `json_panel.py` - JSON 解析与 Excel 导出工具
  - `vm_panel.py` - KVM/QEMU 虚拟机 XML 配置生成器
- `drag.py` - 拖拽排序功能示例
- `example/` - customtkinter 示例代码

### 技术栈
- `customtkinter` - 现代化 Tkinter UI 框架
- `PIL/Pillow` - 图像处理
- `pandas` + `openpyxl` - Excel 文件生成
- `tkinter` - 标准 GUI 库
- `xml.etree.ElementTree` / `minidom` - XML 生成与格式化
- `libvirt` / `virsh` - 虚拟机管理 (可选)

### VmPanel 虚拟机配置
- 基础配置：名称、描述、vCPU、内存、机器类型、固件 (BIOS/UEFI)
- 磁盘配置：支持多磁盘，类型 (qcow2/raw/vmdk)、总线 (virtio/sata/ide/scsi)
- 网络配置：支持多网卡，模式 (NAT/Bridge/Macvtap)、MAC 地址生成
- 高级配置：PCI 直通、USB 设备、ACPI/APIC/Hyper-V/IOMMU 特性
- XML 生成：生成标准 libvirt domain XML
- 保存/创建：保存 XML 文件或通过 virsh 创建虚拟机

### 关键模式
- 采用 `CTkFrame` 网格布局 (`grid`) 组织界面
- 使用 `CTkTabview` 实现多 Tab 切换
- 深色/浅色主题通过 `set_appearance_mode()` 控制
