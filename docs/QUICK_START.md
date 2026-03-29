# PyTools 快速开始指南

## 🚀 快速修复（立即可做）

### 1. 修复代码质量问题

```bash
# 运行快速修复脚本
python scripts/quick_fix.py

# 或手动执行
ruff check . --fix      # 自动修复
ruff format .           # 格式化代码
```

### 2. 安装 Pre-commit Hooks

```bash
# 安装 pre-commit
pip install pre-commit

# 启用 hooks
pre-commit install

# 运行所有 hooks
pre-commit run --all-files
```

### 3. 配置开发环境

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 或使用 requirements
pip install -r requirements.txt
pip install pytest pytest-cov ruff mypy
```

## 📝 开发工作流

### 代码检查

```bash
# Ruff 检查
ruff check .

# Ruff 自动修复
ruff check . --fix

# Ruff 格式化
ruff format .

# MyPy 类型检查（可选）
mypy .
```

### 运行测试

```bash
# 运行所有测试
pytest tests/ -v

# 运行特定测试文件
pytest tests/test_vm_config.py -v

# 生成覆盖率报告
pytest tests/ --cov=. --cov-report=html

# 查看覆盖率报告
# 打开 htmlcov/index.html
```

### 构建应用

```bash
# 使用 PyInstaller 打包
pyinstaller main.spec

# 运行打包后的应用
./dist/PyTools/PyTools.exe  # Windows
./dist/PyTools/PyTools       # Linux/macOS
```

## 🔧 常见问题

### Q: Ruff 检测到错误怎么办？

```bash
# 查看详细错误信息
ruff check . --show-fixes

# 自动修复（大部分问题）
ruff check . --fix

# 手动修复剩余问题
```

### Q: 测试失败怎么办？

```bash
# 查看详细测试输出
pytest tests/ -v -s

# 运行特定测试
pytest tests/test_vm_config.py::test_basic_config -v

# 调试模式
pytest tests/ --pdb
```

### Q: 如何添加新功能？

1. 创建新分支
   ```bash
   git checkout -b feature/new-feature
   ```

2. 编写代码和测试
   ```python
   # 在 tests/ 目录添加测试
   def test_new_feature():
       assert True
   ```

3. 运行检查
   ```bash
   ruff check . --fix
   pytest tests/ -v
   ```

4. 提交代码
   ```bash
   git add .
   git commit -m "feat: add new feature"
   git push origin feature/new-feature
   ```

## 📚 更多资源

- [改进方案](../改进.md) - 详细的改进计划
- [README](../README.md) - 项目说明
- [CLAUDE.md](../CLAUDE.md) - AI 助手指南
- [libvirt 文档](https://www.libvirt.org/formatdomain.html) - VM 配置参考

## 🎯 下一步

1. ✅ 运行快速修复脚本
2. ✅ 安装 pre-commit hooks
3. ✅ 运行测试确保一切正常
4. 📖 阅读改进方案了解长期计划
5. 🚀 开始开发新功能
