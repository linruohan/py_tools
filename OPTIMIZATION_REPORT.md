# 项目结构优化报告

## 优化日期
2026-03-14

---

## 第二次优化（本次）

### 1. 资源文件整合
- 将 `test_images/` 目录中的所有图片复制到 `resources/images/`
- 更新 `main.py` 中的图片路径引用:`'test_images'` → `'resources/images'`
- 删除 `test_images/` 目录

### 2. model/vm_model 目录结构简化

**优化前**:31 个 Python 文件全部在根目录,结构混乱

**优化后**:按功能分组为 4 个子目录
```
model/vm_model/
├── __init__.py          # 统一导出接口
├── core/                # 核心模块
│   ├── vm_config.py     - VM 配置管理类
│   ├── domain.py        - Domain 数据模型
│   └── converter.py     - 配置转换工具
├── configs/             # 配置类（24 个文件）
│   ├── basic_config.py
│   ├── cpu_allocation_config.py
│   ├── memory_allocation_config.py
│   ├── os_booting_config.py
│   └── devices_config.py
├── cpu/                 - CPU 相关模型
└── devices/             - 设备模型
```

### 3. 导入路径更新
- `model/vm_model/__init__.py` - 导入路径指向新的子目录
- `model/vm_model/core/vm_config.py` - 导入 configs 模块
- `panels/vm_panel/vm_panel.py` - 导入路径更新

---

## 第一次优化（之前完成）

### 新增目录
- `core/`、`services/`、`utils/`、`resources/`、`scripts/`、`tests/`

### 文件移动
- `drag.py` → `example/drag_example.py`
- `test_vm_*.py` → `tests/`
- `001.py` → `example/001_example.py`

### 新增文件
- `pyproject.toml`、`requirements.txt`、`scripts/build.py`

### 配置更新
- `.gitignore`、`readme.md`、`CLAUDE.md`

---

## 第三次优化（本次会话完成）

### 1. devices_tab.py 大文件拆分

**优化前**:`panels/vm_panel/tabs/devices_tab.py` - 1933 行,75KB

**优化后**:拆分为 6 个模块
```
panels/vm_panel/tabs/devices/
├── __init__.py         (19 行)   - 模块导出
├── main.py             (337 行)  - DevicesTab 主类
├── hostdev.py          (820 行)  - USB/PCI/SCSI/MDEV 设备直通
├── disk.py             (543 行)  - 磁盘设备和配置对话框
├── graphics.py         (98 行)   - 图形显示配置
└── others.py           (163 行)  - 串口/TPM/控制器等其他设备
```

原始 `devices_tab.py` 保留作为兼容层,从新模块导入所有类。

### 2. 导入路径修复

修复了以下导入路径问题:
- `model/vm_model/configs/devices_config.py`: `.devices.*` → `..devices.*`
- `model/vm_model/core/converter.py`: `model.vm_model.domain` → `.domain`
- `model/vm_model/core/domain.py`: `.cpu.numa` → `..cpu.numa`
- `model/vm_model/__init__.py`: `ConfigConverter` → `DomainConfigConverter`
- `panels/vm_panel/vm_panel.py`: 更新 styles、tab_toggle、xml_generator 导入路径
- `panels/vm_panel/tabs/*.py`: 批量修复相对导入为绝对导入

### 3. 代码质量验证

- 所有核心模块导入测试通过
- 应用可正常启动运行
- Ruff 检查剩余警告均为代码风格建议,不影响功能

---

## 后续建议

1. **添加类型注解** - 为核心模块添加完整类型注解
2. **添加单元测试** - 为核心模块添加 pytest 测试
3. **CI/CD 配置** - 添加 GitHub Actions 工作流

```
py_tools/
├── CLAUDE.md               # Claude 配置说明
├── README.md               # 项目文档
├── pyproject.toml          # 项目配置
├── requirements.txt        # 依赖列表
├── ruff.toml               # Ruff 配置
├── main.py                 # 应用入口
├── main.spec               # PyInstaller 配置
│
├── core/                   # 核心应用模块
├── panels/                 # UI 面板层
│   ├── home_panel.py
│   ├── json_panel.py
│   └── vm_panel/
│       ├── tabs/           # 24 个 Tab
│       └── frames/         # 可复用组件
├── model/                  # 数据模型层
│   └── vm_model/
│       ├── core/           # 核心模块
│       ├── configs/        # 配置类
│       ├── cpu/
│       └── devices/
├── services/               # 业务逻辑层
├── utils/                  # 工具函数
├── tests/                  # 测试代码
├── example/                # 示例代码
├── resources/              # 资源文件
│   ├── icons/
│   └── images/
└── scripts/                # 构建脚本
```

## 优化效果

| 指标 | 优化前 | 优化后 | 改善 |
|------|--------|--------|------|
| model/vm_model 根目录文件数 | 31 | 0 | 100% 减少 |
| 资源文件位置 | test_images/ | resources/images/ | 统一管理 |
| Python 文件总数 | 132 | 134 | +2 (新增脚本) |

## 开发命令

```bash
# 代码检查
ruff check
ruff check --fix
ruff format

# 构建脚本
python -m scripts.build check
python -m scripts.build lint
python -m scripts.build test
python -m scripts.build build
```

## 第四次优化（本次会话完成）

### 1. 清理空目录和未使用文件

**删除空目录**:
- `core/` - 空目录,仅有 `__init__.py`
- `services/` - 空目录,仅有 `__init__.py`

**删除未使用文件**:
- `utils/xml_builder.py` (18KB) - 与 `xml_generator.py` 功能重复,且未被任何模块引用

**清理缓存**:
- 删除所有 `__pycache__/` 目录

### 2. 重构 vm_panel.py 中的重复代码

**优化前**:`_on_tab_toggle()` 和 `_init_tabs()` 方法中各有 24 行导入代码和 24 行字典定义

**优化后**:提取为模块级 `_get_tab_classes()` 函数,使用延迟导入模式

```python
# Tab 类映射 - 延迟导入
_TAB_CLASSES = None


def _get_tab_classes():
    """获取 Tab 类映射（延迟导入）."""
    global _TAB_CLASSES
    if _TAB_CLASSES is None:
        from .tabs import (...)  # 导入所有 Tab 类
        _TAB_CLASSES = {...}  # 构建映射字典
    return _TAB_CLASSES
```

**效果**:
- 减少约 100 行重复代码
- 使用延迟导入,避免循环导入问题
- 代码更易维护

### 3. 更新文档

- `CLAUDE.md` - 更新项目结构说明,移除已删除的目录
- `OPTIMIZATION_REPORT.md` - 添加本次优化记录

## 优化效果汇总

| 指标 | 优化前 | 优化后 | 改善 |
|------|--------|--------|------|
| 目录数量 | 41 | 39 | -2 (空目录) |
| Python 文件数 | 134 | 133 | -1 (重复文件) |
| vm_panel.py 行数 | ~630 | ~530 | -100 行 |
| utils/ 文件数 | 2 | 1 | 删除重复 |
| __pycache__ | 15 个 | 0 个 | 100% 清理 |

## 最终项目结构
