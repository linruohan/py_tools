# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

基于 `customtkinter` 的桌面应用工具箱，提供现代化 UI 界面。包含三个主要功能面板：Home（组件展示）、JSON（解析与 Excel 导出）、VM（KVM/QEMU 虚拟机 XML 配置生成器）。

## 开发命令

### 代码检查与格式化
```bash
ruff check           # 检查语法错误
ruff check --fix     # 检查并自动修复
ruff format          # 格式化代码
```

### 构建脚本
```bash
python -m scripts.build check      # Ruff 检查
python -m scripts.build fix        # 检查并修复
python -m scripts.build format     # 格式化
python -m scripts.build test       # 运行测试
python -m scripts.build lint       # 运行所有检查
python -m scripts.build build      # PyInstaller 打包
```

### 运行与测试
```bash
python main.py                     # 运行主应用
python -m pytest tests/ -v         # 运行所有测试
python -m pytest tests/test_vm_config.py -v  # 运行单个测试文件
```

### 打包
```bash
pyinstaller main.spec              # 使用现有 spec 打包
```

## 代码架构

### 应用结构
- `main.py` - 应用入口，`App` 类继承自 `ctk.CTk`，管理左侧导航栏和三个主面板切换
- `panels/` - 三大功能面板：`HomePanel`、`JsonPanel`、`VmPanel`
- `model/vm_model/` - VM 配置数据模型层，采用组合模式
- `utils/` - 工具模块（XML 生成器、解析器）
- `components/` - 可复用 UI 组件
- `example/` - customtkinter 示例代码
- `resources/` - 资源文件（图片、图标）
- `scripts/` - 构建脚本

### VM Panel 架构（24 Tab）

**面板组成**:
- `vm_panel.py` - 主面板，集成 `TabTogglePanel` 管理 24 个 Tab 的显示/隐藏
- `tabs/` - 24 个配置 Tab，每个 Tab 继承自 `components/base_tab.py` 的 `BaseTab`
- `frames/` - 可复用帧组件（`disk_frame.py`、`network_frame.py`、`hostdev_frame.py`）
- `tabs/devices/` - 设备配置子模块

**默认启用的基础 Tab**: `general_metadata`、`os_booting`、`cpu_allocation`、`memory_allocation`、`devices`

**可选高级 Tab**: 共 19 个，包括 SMBIOS、IOThreads、NUMA、性能监控等

### 数据模型层 (model/vm_model)

采用组合模式，由 `VMConfig` 统一管理：

```
model/vm_model/
├── core/
│   ├── vm_config.py   - VMConfig 统一配置管理类
│   └── domain.py      - Domain 数据模型（枚举、数据类）
├── configs/           - 各模块配置类（basic、cpu、memory、devices 等）
├── cpu/               - CPU 模型（topology、numa）
└── devices/           - 设备模型（disk、graphics、interface 等）
```

**配置流程**: UI Tab → `tab_data` → `VMConfig.update_from_tab()` → `LibvirtXMLGenerator.generate()`

### 关键组件

- `components/tab_toggle.py` - `TabTogglePanel` 类管理 24 Tab 的启用/禁用状态，通过复选框控制
- `components/base_tab.py` - `BaseTab` 基类，定义 `get_tab_data()` 接口供所有 Tab 继承
- `utils/xml_generator.py` - `LibvirtXMLGenerator` 类根据配置生成 libvirt domain XML

### 技术栈
- `customtkinter>=5.2.0` - GUI 框架
- `PIL/Pillow>=10.0.0` - 图像处理
- `pandas>=2.0.0` + `openpyxl>=3.1.0` - Excel 生成
- `xml.etree.ElementTree` / `minidom` - XML 生成与格式化

## 开发模式

- 使用 `CTkFrame.grid()` 网格布局组织界面
- `CTkTabview` 实现 Tab 切换
- 深色/浅色主题通过 `ctk.set_appearance_mode()` 控制
- 资源路径使用 `Path(__file__).resolve().parent / 'resources'` 确保跨平台

## libvirt 参考
https://www.libvirt.org/formatdomain.html

## GitHub Actions
推送 `v*` 标签自动构建 Windows exe 并创建 Release，支持在 Actions 页面手动触发。
