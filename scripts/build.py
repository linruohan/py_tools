#!/usr/bin/env python3
"""Build script for PyTools."""

import subprocess
import sys
from pathlib import Path


def run_command(cmd: list[str], description: str) -> bool:
    """Run a command and return success status."""
    print(f"\n{'='*50}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print(f"{'='*50}")

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(f"stderr: {e.stderr}")
        return False


def check() -> bool:
    """Run ruff check."""
    return run_command(["ruff", "check", "."], "Ruff Check")


def fix() -> bool:
    """Run ruff check and fix."""
    return run_command(["ruff", "check", "--fix", "."], "Ruff Check + Fix")


def format_code() -> bool:
    """Run ruff format."""
    return run_command(["ruff", "format", "."], "Ruff Format")


def test() -> bool:
    """Run pytest."""
    return run_command(["pytest", "tests/", "-v"], "Pytest")


def build() -> bool:
    """Build package with pyinstaller."""
    return run_command(["pyinstaller", "main.spec"], "PyInstaller Build")


def lint() -> bool:
    """Run all lint checks."""
    results = [check(), format_code()]
    return all(results)


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python -m scripts.build [check|fix|format|test|build|lint|all]")
        print("\nCommands:")
        print("  check   - Run ruff check")
        print("  fix     - Run ruff check and fix")
        print("  format  - Run ruff format")
        print("  test    - Run pytest")
        print("  build   - Build with pyinstaller")
        print("  lint    - Run all lint checks")
        print("  all     - Run check, fix, format, test")
        sys.exit(1)

    command = sys.argv[1]

    commands = {
        'check': check,
        'fix': fix,
        'format': format_code,
        'test': test,
        'build': build,
        'lint': lint,
        'all': lambda: all([check(), fix(), format_code(), test()]),
    }

    if command not in commands:
        print(f"Unknown command: {command}")
        sys.exit(1)

    success = commands[command]()
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
