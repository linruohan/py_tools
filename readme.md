## 格式化

```bash
ruff check # 检查语法
ruff check --fix # 检查语法,并修复
ruff format # 格式化代码
```

## pyinstaller打包(推荐)

### 生成main.spec

pyinstaller --noconfirm --onedir --windowed --add-data "c:/software/Python3/lib/site-packages/customtkinter;customtkinter/"
--add-data "d:/codehub/py_tools/test_images;test_images/" -i "d:/codehub/py_tools/mytool.ico" "main.py"

### 打包

pyinstaller main.spec

## nuitka 打包(不推荐)
> 打包后无法运行

```bash
"--follow-imports",  # 跟踪导入
"--enable-plugin=tk-inter",  # 启用 Tkinter 支持
"--include-package=customtkinter",  # 包含 customtkinter
f"--include-data-dir=src/utils/turnstilePatch=turnstilePatch",  # 包含数据目录
f"--include-data-files=src/core/names-dataset.txt=names-dataset.txt",  # 包含具体的 txt 文件
f"--include-data-dir=src/config=src/config",  # 包含配置目录
"--warn-unusual-code",  # 警告不寻常的代码
"--warn-implicit-exceptions",  # 警告隐式异常
"--nofollow-import-to=tkinter.test",  # 排除测试模块
"--nofollow-import-to=PIL.ImageQt",  # 排除 Qt 相关
"--remove-output",  # 删除之前的输出
f"--output-dir={output_dir}",  # 输出目录
f'--output-file="{app_name}"',  # 输出文件名
# macos
"--macos-create-app-bundle",  # 创建 macOS 应用包
"--macos-app-icon=src/assets/app_icon.icns",  # 设置应用图标
f"--macos-app-name={app_name}.app",  # 设置应用名称
# windows
"--standalone",  # 独立可执行文件
"--mingw64",  # 使用 MinGW64
"--windows-console-mode=disable",  # Windows 禁用控制台
"--windows-icon-from-ico=src/assets/app_icon.ico",  # Windows 应用图标
```

python -m nuitka --follow-imports --enable-plugin=tk-inter --include-package=customtkinter --include-data-dir=test_images=test_images --include-data-files=readme.md=readme.md --warn-unusual-code --warn-implicit-exceptions --nofollow-import-to=tkinter.test --nofollow-import-to=PIL.ImageQt --remove-output --output-dir=dist --output-file=PyTools --standalone --mingw64 --windows-console-mode=disable --windows-icon-from-ico=mytool.ico main.py


## VM 虚拟机
https://www.libvirt.org/formatdomain.html

### 🔧 基础配置（默认启用）
1. 基础信息 - 虚拟机的基本元数据配置
2. 系统引导 - 操作系统引导配置
3. CPU 分配 - CPU 资源分配设置
4. 内存分配 - 内存资源分配设置
5. 设备 - 各类设备配置
### 📊 高级配置（可选启用）
6. SMBIOS 系统信息 - SMBIOS 系统信息配置
7. IO 线程分配 - I/O 线程资源分配
8. CPU 优化 - CPU 性能调优参数
9. 内存后端 - 内存后端存储配置
10. 内存优化 - 内存性能调优
11. NUMA 节点优化 - NUMA 架构相关优化
12. 块 I/O 优化 - 块设备 I/O 性能调优
13. 资源分区 - 资源隔离与分区配置
14. 光纤通道 VMID - 光纤通道虚拟机标识
15. CPU 模型与拓扑 - CPU 模型和拓扑结构
16. 事件配置 - 系统事件配置
17. 电源管理 - 电源管理策略
18. 磁盘节流组管理 - 磁盘 I/O 限流组配置
19. 虚拟化特性 - Hypervisor 特性配置
20. 时间同步 - 时间同步机制配置
21. 性能监控事件 - 性能监控相关事件
22. 安全标签 - 安全标签配置
23. 密钥封装 - 密钥封装配置
24. 启动安全 - 启动时安全配置