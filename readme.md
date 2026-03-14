# PyTools

基于 `customtkinter` 的桌面应用工具箱,提供现代化 UI 界面。

## 功能特性

- **Home Panel** - CTk 组件展示与示例
- **JSON Panel** - JSON 解析与 Excel 导出工具
- **VM Panel** - KVM/QEMU 虚拟机 XML 配置生成器（24 个可配置 Tab）

## 安装

### 基础安装

```bash
pip install -r requirements.txt
```

### 开发安装

```bash
pip install -e ".[dev]"
```

## 开发命令

### 代码检查与格式化

```bash
ruff check           # 检查语法错误
ruff check --fix     # 检查并自动修复
ruff format          # 格式化代码
```

### 运行应用

```bash
python main.py
```

### 运行测试

```bash
pytest tests/
```

## 打包

### PyInstaller 方式（推荐）

```bash
# 生成 main.spec
pyinstaller --noconfirm --onedir --windowed \
  --add-data "customtkinter;customtkinter/" \
  --add-data "test_images;test_images/" \
  --icon "resources/icons/mytool.ico" \
  main.py

# 打包
pyinstaller main.spec
```

## 项目结构

```
py_tools/
├── core/           # 核心应用模块
├── panels/         # UI 面板层
│   ├── home_panel.py
│   ├── json_panel.py
│   └── vm_panel/   # VM 配置面板（24 Tab）
├── model/          # 数据模型层
│   └── vm_model/   # VM 配置数据模型
├── services/       # 业务逻辑层
├── utils/          # 工具函数
├── tests/          # 测试代码
├── example/        # 示例代码
├── resources/      # 资源文件
└── scripts/        # 构建脚本
```

## VM 虚拟机配置

参考文档:https://www.libvirt.org/formatdomain.html

### 🔧 基础配置（默认启用）

| Tab | 说明 |
|-----|------|
| General Metadata | 名称、描述、UUID、机型、虚拟化类型、vCPU、内存 |
| OS Booting | 固件 (BIOS/UEFI)、引导设备、超时设置 |
| CPU Allocation | vCPU、拓扑结构 |
| Memory Allocation | 内存大小、交换内存 |
| Devices | 图形显示 (vnc/spice)、视频模型、USB、串口、TPM |

### 📊 高级配置（可选启用）

| Tab | 说明 |
|-----|------|
| SMBIOS System Information | SMBIOS 系统信息配置 |
| IOThreads Allocation | I/O 线程资源分配 |
| CPU Tuning | CPU 性能调优参数 |
| Memory Backing | 内存后端存储配置 |
| Memory Tuning | 内存性能调优 |
| NUMA Node Tuning | NUMA 架构相关优化 |
| Block I/O Tuning | 块设备 I/O 性能调优 |
| Resource Partitioning | 资源隔离与分区配置 |
| Fibre Channel VMID | 光纤通道虚拟机标识 |
| CPU Model and Topology | CPU 模型和拓扑结构 |
| Events Configuration | 系统事件配置 |
| Power Management | 电源管理策略 |
| Disk Throttle Group | 磁盘 I/O 限流组配置 |
| Hypervisor Features | Hypervisor 特性配置 |
| Time Keeping | 时间同步机制配置 |
| Performance Monitoring | 性能监控相关事件 |
| Security Label | 安全标签配置 |
| Key Wrap | 密钥封装配置 |
| Launch Security | 启动时安全配置 |

## 技术栈

- **GUI 框架**: customtkinter
- **图像处理**: PIL/Pillow
- **数据处理**: pandas + openpyxl
- **XML 处理**: xml.etree.ElementTree / minidom
- **虚拟机管理**: libvirt / virsh (可选)

## License

MIT License
