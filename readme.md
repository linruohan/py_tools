## 格式化

```bash
ruff check # 检查语法
ruff check --fix # 检查语法,并修复
ruff format # 格式化代码
```

## pyinstaller打包

### 生成main.spec

pyinstaller --noconfirm --onedir --windowed --add-data "c:/software/Python3/lib/site-packages/customtkinter;customtkinter/"
--add-data "d:/codehub/py_tools/test_images;test_images/" -i "d:/codehub/py_tools/mytool.ico" "main.py"

### 打包

pyinstaller main.spec

## nuitka 打包

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
