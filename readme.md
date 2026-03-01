## 格式化

```bash
ruff check # 检查语法
ruff check --fix # 检查语法,并修复
ruff format # 格式化代码
```

## 生成main.spec

pyinstaller --noconfirm --onedir --windowed --add-data "c:/software/Python3/lib/site-packages/customtkinter;customtkinter/"
--add-data "d:/codehub/py_tools/test_images;test_images/" -i "d:/codehub/py_tools/mytool.ico" "main.py"

## 打包

pyinstaller main.spec
