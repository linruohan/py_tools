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
python -m nuitka --follow-imports --enable-plugin=tk-inter --include-package=customtkinter \
  --include-data-dir=test_images=test_images --include-data-files=readme.md=readme.md \
  --warn-unusual-code --warn-implicit-exceptions --nofollow-import-to=tkinter.test \
  --nofollow-import-to=PIL.ImageQt --remove-output --output-dir=dist --output-file=PyTools \
  --standalone --windows-console-mode=disable --windows-icon-from-ico=mytool.ico main.py
```

## 代码架构

### 核心结构
- `main.py` - 应用入口，使用 `CTk` 创建主窗口，含左侧导航栏和多面板切换逻辑
- `panels/` - 功能面板模块
  - `home_panel.py` - 主页面板，包含多 Tab 展示各种 CTk 组件
  - `json_panel.py` - JSON 解析与 Excel 导出工具
  - `vm_panel/` - KVM/QEMU 虚拟机 XML 配置生成模块（24 个可配置 Tab）
- `model/vm_model/` - 虚拟机配置数据模型层
- `drag.py` - 拖拽排序功能示例
- `example/` - customtkinter 示例代码

### VmPanel 虚拟机配置（24 个 Tab）

**默认启用的基础 Tab**：
- 基础信息 (`general_metadata`) - 名称、描述、UUID、机型、虚拟化类型、vCPU、内存
- 系统引导 (`os_booting`) - 固件 (BIOS/UEFI)、引导设备、超时设置
- CPU 分配 (`cpu_allocation`) - vCPU、拓扑结构
- 内存分配 (`memory_allocation`) - 内存大小、交换内存
- 设备 (`devices`) - 图形显示 (vnc/spice)、视频模型、USB、串口、TPM

**可选高级 Tab**：
- SMBIOS 系统信息、IO 线程分配、CPU 优化、内存后端、内存优化
- NUMA 节点优化、块 IO 优化、资源分区、光纤通道 VMID、CPU 模型与拓扑
- 事件配置、电源管理、磁盘节流组、虚拟化特性、时间同步
- 性能监控、安全标签、密钥包装、启动安全

### model/vm_model 数据模型层

采用组合模式管理配置：
- `vm_config.py` - VMConfig 统一配置管理类
- `basic_config.py` - 基础配置（名称、UUID、机型等）
- `cpu_allocation_config.py` - CPU 分配配置
- `memory_allocation_config.py` - 内存分配配置
- `os_booting_config.py` - OS 引导配置
- `devices_config.py` - 设备配置
- `domain.py` - Domain 数据模型（含枚举类型、数据类）
- `cpu/` - CPU 相关模型（cpu.py、numa.py）
- `devices/` - 设备模型（disk.py、interface.py、graphics.py、video.py 等）
- `converter.py` - 配置转换工具

### xml_generator.py XML 生成器

- `LibvirtXMLGenerator` 类生成标准 libvirt domain XML
- 支持动态 XML 预览，配置变更时自动更新
- 支持保存 XML 文件或通过 `virsh define` 创建虚拟机

### 技术栈
- `customtkinter` - 现代化 Tkinter UI 框架
- `PIL/Pillow` - 图像处理
- `pandas` + `openpyxl` - Excel 文件生成
- `xml.etree.ElementTree` / `minidom` - XML 生成与格式化
- `libvirt` / `virsh` - 虚拟机管理 (可选)

### 关键模式
- 采用 `CTkFrame` 网格布局 (`grid`) 组织界面
- 使用 `CTkTabview` 实现多 Tab 切换
- `TabTogglePanel` 管理 24 个 Tab 的显示/隐藏
- 深色/浅色主题通过 `set_appearance_mode()` 控制

## libvirt 文档参考
https://www.libvirt.org/formatdomain.html
