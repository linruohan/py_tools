"""快速修复脚本 - 自动修复常见代码问题"""

import subprocess
import sys

from pathlib import Path


def run_command(cmd: list[str], description: str) -> bool:
    """运行命令并显示结果

    Args:
        cmd: 命令列表
        description: 命令描述

    Returns:
        是否成功
    """
    print(f'\n{"=" * 60}')
    print(f'执行: {description}')
    print(f'命令: {" ".join(cmd)}')
    print(f'{"=" * 60}\n')

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,
            encoding='utf-8',
            errors='replace',  # 替换无法解码的字符
        )

        if result.stdout:
            print(result.stdout)

        if result.stderr:
            print(result.stderr, file=sys.stderr)

        if result.returncode == 0:
            print(f'✅ {description} - 成功')
            return True
        else:
            print(f'❌ {description} - 失败 (退出码: {result.returncode})')
            return False

    except Exception as e:
        print(f'❌ {description} - 异常: {e}')
        return False


def main():
    """主函数"""
    print('🚀 PyTools 快速修复脚本')
    print('=' * 60)

    # 检查是否在项目根目录
    if not Path('main.py').exists():
        print('❌ 错误: 请在项目根目录运行此脚本')
        sys.exit(1)

    results = []

    # 1. 运行 Ruff 检查
    results.append(run_command(['ruff', 'check', '.'], 'Ruff 代码检查'))

    # 2. 自动修复 Ruff 问题
    results.append(run_command(['ruff', 'check', '.', '--fix'], 'Ruff 自动修复'))

    # 3. 格式化代码
    results.append(run_command(['ruff', 'format', '.'], 'Ruff 代码格式化'))

    # 4. 再次检查
    results.append(run_command(['ruff', 'check', '.'], 'Ruff 最终检查'))

    # 5. 运行测试(如果存在)
    if Path('tests').exists():
        # 检查是否安装了 pytest-cov
        import importlib.util

        if importlib.util.find_spec('pytest_cov') is not None:
            results.append(
                run_command(
                    ['pytest', 'tests/', '-v', '--cov=.', '--cov-report=term-missing'],
                    '运行测试(带覆盖率)',
                )
            )
        else:
            results.append(run_command(['pytest', 'tests/', '-v'], '运行测试'))

    # 总结
    print('\n' + '=' * 60)
    print('📊 修复结果总结')
    print('=' * 60)

    success_count = sum(results)
    total_count = len(results)

    print(f'成功: {success_count}/{total_count}')

    if success_count == total_count:
        print('✅ 所有检查通过!')
        sys.exit(0)
    else:
        print('⚠️ 部分检查失败,请查看上面的错误信息')
        sys.exit(1)


if __name__ == '__main__':
    main()
