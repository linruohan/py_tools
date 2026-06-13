"""测试表单构建器组件."""

import os
import pytest
import customtkinter as ctk

from components.form_builder import FormBuilder

# 检查是否在无显示器的 headless 环境中
def is_headless():
    """检测是否在无显示器的 headless 环境中运行."""
    # 检查常见 CI 环境变量
    ci_envs = ['CI', 'GITHUB_ACTIONS', 'GITLAB_CI', 'JENKINS_URL', 'BUILD_NUMBER']
    if any(os.environ.get(var) for var in ci_envs):
        # 在 CI 环境中，使用更严格的检测
        if os.name == 'nt':
            try:
                import ctypes
                user32 = ctypes.windll.user32
                return user32.GetSystemMetrics(0) == 0
            except Exception:
                return True
        else:
            return os.environ.get('DISPLAY') is None

    # 检测 MSYS/Git Bash 环境（Windows 子系统不支持 tkinter 事件）
    if os.name == 'nt' and os.environ.get('MSYSTEM'):
        return True

    return False

SKIP_IF_HEADLESS = pytest.mark.skipif(
    is_headless(),
    reason="需要图形显示器环境"
)


def test_create_label_entry():
    """测试创建标签 + 输入框组合."""
    root = ctk.CTk()
    frame = ctk.CTkFrame(root)
    frame.pack()

    builder = FormBuilder()
    entry = builder.create_label_entry(
        parent=frame,
        label_text='测试标签:',
        default_value='默认值',
        row=0,
        column=0,
    )

    assert entry is not None
    assert entry.get() == '默认值'

    # 清理
    root.destroy()


@SKIP_IF_HEADLESS
def test_create_label_entry_with_callback():
    """测试创建带回调的输入框."""
    root = ctk.CTk()
    frame = ctk.CTkFrame(root)
    frame.pack()

    callback_called = []

    def on_change(value):
        callback_called.append(value)

    builder = FormBuilder()
    entry = builder.create_label_entry(
        parent=frame,
        label_text='测试:',
        default_value='initial',
        row=0,
        on_change=on_change,
    )

    # 模拟输入
    entry.delete(0, 'end')
    entry.insert(0, 'new value')

    # 触发 KeyRelease 事件
    entry.event_generate('<KeyRelease>')

    assert len(callback_called) > 0
    assert 'new value' in callback_called

    # 清理
    root.destroy()


def test_create_label_combobox():
    """测试创建标签 + 下拉框组合."""
    root = ctk.CTk()
    frame = ctk.CTkFrame(root)
    frame.pack()

    builder = FormBuilder()
    combobox = builder.create_label_combobox(
        parent=frame,
        label_text='选择:',
        values=['选项 1', '选项 2', '选项 3'],
        default_value='选项 2',
        row=0,
        column=0,
    )

    assert combobox is not None
    assert combobox.get() == '选项 2'

    # 清理
    root.destroy()


@SKIP_IF_HEADLESS
def test_create_label_combobox_with_callback():
    """测试创建带回调的下拉框."""
    root = ctk.CTk()
    frame = ctk.CTkFrame(root)
    frame.pack()

    callback_called = []

    def on_change(value):
        callback_called.append(value)

    builder = FormBuilder()
    combobox = builder.create_label_combobox(
        parent=frame,
        label_text='选择:',
        values=['选项 1', '选项 2', '选项 3'],
        default_value='选项 1',
        row=0,
        on_change=on_change,
    )

    # 改变选择
    combobox.set('选项 3')

    assert len(callback_called) > 0

    # 清理
    root.destroy()


def test_create_label_switch():
    """测试创建标签 + 开关组合."""
    root = ctk.CTk()
    frame = ctk.CTkFrame(root)
    frame.pack()

    builder = FormBuilder()
    switch = builder.create_label_switch(
        parent=frame,
        label_text='启用:',
        default_value=True,
        row=0,
        column=0,
    )

    assert switch is not None
    assert switch.get() == 1  # 选中状态

    # 清理
    root.destroy()


def test_create_label_switch_with_callback():
    """测试创建带回调的开关."""
    root = ctk.CTk()
    frame = ctk.CTkFrame(root)
    frame.pack()

    callback_called = []

    def on_change(value):
        callback_called.append(value)

    builder = FormBuilder()
    switch = builder.create_label_switch(
        parent=frame,
        label_text='启用:',
        default_value=False,
        row=0,
        on_change=on_change,
    )

    # 切换开关
    switch.toggle()

    assert len(callback_called) > 0
    assert True in callback_called

    # 清理
    root.destroy()


def test_create_label_textbox():
    """测试创建标签 + 文本框组合."""
    root = ctk.CTk()
    frame = ctk.CTkFrame(root)
    frame.pack()

    builder = FormBuilder()
    textbox = builder.create_label_textbox(
        parent=frame,
        label_text='说明:',
        default_value='默认文本',
        row=0,
        column=0,
        width=300,
        height=100,
    )

    assert textbox is not None
    content = textbox.get("1.0", "end").strip()
    assert content == '默认文本'

    # 清理
    root.destroy()


def test_form_builder_grid_layout():
    """测试表单构建器的网格布局."""
    root = ctk.CTk()
    frame = ctk.CTkFrame(root)
    frame.pack()

    builder = FormBuilder()

    # 创建多个表单项
    entry1 = builder.create_label_entry(
        parent=frame,
        label_text='第一行:',
        row=0,
        column=0,
    )

    entry2 = builder.create_label_entry(
        parent=frame,
        label_text='第二行:',
        row=1,
        column=0,
    )

    # 验证网格位置
    info1 = entry1.grid_info()
    info2 = entry2.grid_info()

    assert info1['row'] == 0
    assert info2['row'] == 1

    # 清理
    root.destroy()


def test_form_builder_custom_width():
    """测试自定义宽度."""
    root = ctk.CTk()
    frame = ctk.CTkFrame(root)
    frame.pack()

    builder = FormBuilder()
    entry = builder.create_label_entry(
        parent=frame,
        label_text='宽输入框:',
        width=400,
        row=0,
        column=0,
    )

    # 验证宽度(CTkEntry 的 winfo_width 可能需要更新后才能获取)
    entry.update()
    assert entry.winfo_width() > 200  # 应该比默认宽度大

    # 清理
    root.destroy()
