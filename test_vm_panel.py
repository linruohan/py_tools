#!/usr/bin/env python3
"""测试 VM 面板的 XML 生成功能"""

import sys
import os

# 添加当前目录到 Python 路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from panels.vm_panel.vm_panel import VmPanel

import customtkinter as ctk

# 创建测试窗口
root = ctk.CTk()
root.title('VM Panel Test')
root.geometry('800x600')

# 创建 VM 面板
vm_panel = VmPanel(root)
vm_panel.pack(fill='both', expand=True)

# 测试添加网卡
print("Testing VM Panel XML generation...")

# 手动触发 XML 更新
vm_panel._update_xml_preview()

# 获取 XML 内容
xml_content = vm_panel.xml_textbox.get('1.0', 'end')
print(f"XML generated successfully! Length: {len(xml_content)}")

# 显示前 500 个字符
print("\n--- XML Preview (first 500 chars) ---")
print(xml_content[:500])

print("\n--- Tab instances ---")
for tab_key, tab_info in vm_panel.tab_instances.items():
    print(f"  {tab_key}: {tab_info['widget'].__class__.__name__}")

print("\nTest completed!")

# 不运行主循环，只测试
# root.mainloop()
