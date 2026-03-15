# -*- coding: utf-8 -*-
"""Fix CPUFeatureSubTab to support add/remove features."""

import re

with open('panels/vm_panel/tabs/cpu_model_topology_tab.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 找到 CPUFeatureSubTab 类并替换
old_pattern = r'''class CPUFeatureSubTab\(BaseConfigTab\):
    """CPU 特性子 Tab\."""

    def __init__\(self, master, on_change_callback=None, \*\*kwargs\):
        super\(\).__init__\(master, on_change_callback, \*\*kwargs\)
        self.features_list = \[\]

        self\._init_ui\(\)

    def _init_ui\(self\) -> None:
        """初始化界面\."""
        self.grid_columnconfigure\(0, weight=1\)

        frame = ctk\.CTkFrame\(self, fg_color=BG_COLOR_CONTENT, corner_radius=6\)
        frame\.grid\(row=0, column=0, sticky='nsew', padx=5, pady=5\)
        frame\.grid_columnconfigure\(1, weight=1\)

        ctk\.CTkLabel\(frame, text='CPU 特性', font=CTK_FONT_BOLD, text_color='#ff9800'\)\.grid\(
            row=0, column=0, columnspan=4, padx=10, pady=5, sticky='w'
        \)

        ctk\.CTkLabel\(frame, text='特性名:', font=CTK_FONT_MAIN, width=80, anchor='w'\)\.grid\(
            row=1, column=0, padx=10, pady=5, sticky='w'
        \)
        self\.feature_name = ctk\.CTkEntry\(frame, placeholder_text='lahf_lm, pcid\.\.\.', width=150\)
        self\.feature_name\.grid\(row=1, column=1, padx=5, pady=5, sticky='w'\)
        self\.feature_name\.bind\('<KeyRelease>', lambda e: self\._trigger_change\(\)\)

        ctk\.CTkLabel\(frame, text='策略:', font=CTK_FONT_MAIN, width=60, anchor='w'\)\.grid\(
            row=1, column=2, padx=10, pady=5, sticky='w'
        \)
        self\.feature_policy = ctk\.CTkOptionMenu\(
            frame,
            values=\['require', 'optional', 'force', 'disable', 'forbid'\],
            width=100,
            font=CTK_FONT_SMALL,
        \)
        self\.feature_policy\.set\('require'\)
        self\.feature_policy\.grid\(row=1, column=3, padx=5, pady=5, sticky='w'\)
        self\.feature_policy\.configure\(command=self\._trigger_change\)

        add_btn = ctk\.CTkButton\(
            frame,
            text='添加',
            command=self\._add_feature,
            fg_color='#00bcd4',
            hover_color='#0097a7',
            width=70,
            font=CTK_FONT_SMALL,
        \)
        add_btn\.grid\(row=1, column=4, padx=5, pady=5\)

        self\.features_display = ctk\.CTkLabel\(
            frame, text='', font=CTK_FONT_SMALL, text_color='#aaaaaa', anchor='w'
        \)
        self\.features_display\.grid\(row=2, column=0, columnspan=5, padx=10, pady=5, sticky='w'\)

    def _add_feature\(self\):
        """添加 CPU 特性\."""
        name = self\.feature_name\.get\(\)\.strip\(\)
        if name:
            self\.features_list\.append\(
                \{
                    'name': name,
                    'policy': self\.feature_policy\.get\(\),
                \}
            \)
            self\.features_display\.configure\(
                text=f'已添加:\{", "\.join\(\[f\["name"\] for f in self\.features_list\]\)\}'
            \)
            self\.feature_name\.delete\(0, 'end'\)
            self\._trigger_change\(\)

    def get_config\(self\) -> dict:
        """获取配置数据\."""
        return \{
            'features': self\.features_list\.copy\(\),
        \}

    def load_config\(self, config: dict\) -> None:
        """加载配置数据\."""
        features = config\.get\('features', \[\]\)
        if features:
            self\.features_list = features\.copy\(\)
            self\.features_display\.configure\(
                text=f'已添加:\{", "\.join\(\[f\["name"\] for f in self\.features_list\]\)\}'
            \)'''

new_code = r'''class CPUFeatureSubTab(BaseConfigTab):
    """CPU 特性子 Tab."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, on_change_callback, **kwargs)
        self.features_list = []
        self.feature_widgets = {}

        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # 顶部框架：添加新 feature
        top_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        top_frame.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
        top_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(top_frame, text='CPU 特性', font=CTK_FONT_BOLD, text_color='#ff9800').grid(
            row=0, column=0, columnspan=5, padx=10, pady=5, sticky='w'
        )

        ctk.CTkLabel(top_frame, text='特性名:', font=CTK_FONT_MAIN, width=80, anchor='w').grid(
            row=1, column=0, padx=10, pady=5, sticky='w'
        )
        self.feature_name = ctk.CTkEntry(top_frame, placeholder_text='lahf_lm, pcid...', width=150)
        self.feature_name.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.feature_name.bind('<KeyRelease>', lambda e: self._on_enter_key(e))

        ctk.CTkLabel(top_frame, text='策略:', font=CTK_FONT_MAIN, width=60, anchor='w').grid(
            row=1, column=2, padx=10, pady=5, sticky='w'
        )
        self.feature_policy = ctk.CTkOptionMenu(
            top_frame,
            values=['require', 'optional', 'force', 'disable', 'forbid'],
            width=100,
            font=CTK_FONT_SMALL,
        )
        self.feature_policy.set('require')
        self.feature_policy.grid(row=1, column=3, padx=5, pady=5, sticky='w')

        add_btn = ctk.CTkButton(
            top_frame,
            text='添加',
            command=self._add_feature,
            fg_color='#00bcd4',
            hover_color='#0097a7',
            width=70,
            font=CTK_FONT_SMALL,
        )
        add_btn.grid(row=1, column=4, padx=5, pady=5)

        # 底部框架：显示已添加的 feature 列表
        bottom_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        bottom_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
        bottom_frame.grid_columnconfigure(0, weight=1)
        bottom_frame.grid_rowconfigure(0, weight=1)

        self.list_frame = ctk.CTkScrollableFrame(bottom_frame, fg_color='transparent')
        self.list_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        self.list_frame.grid_columnconfigure(0, weight=1)

        self._refresh_feature_list()

    def _on_enter_key(self, event):
        """按回车键添加 feature."""
        if event.keysym == 'Return':
            self._add_feature()

    def _add_feature(self):
        """添加 CPU 特性."""
        name = self.feature_name.get().strip()
        if not name:
            return

        # 检查是否已存在
        for feat in self.features_list:
            if feat['name'] == name:
                self.feature_name.delete(0, 'end')
                return

        self.features_list.append(
            {
                'name': name,
                'policy': self.feature_policy.get(),
            }
        )
        self.feature_name.delete(0, 'end')
        self._refresh_feature_list()
        self._trigger_change()

    def _remove_feature(self, index: int):
        """删除指定索引的 CPU 特性."""
        if 0 <= index < len(self.features_list):
            del self.features_list[index]
            self._refresh_feature_list()
            self._trigger_change()

    def _refresh_feature_list(self):
        """刷新 feature 列表显示."""
        # 清除所有现有控件
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        if not self.features_list:
            ctk.CTkLabel(
                self.list_frame,
                text='暂无已添加的特性',
                font=CTK_FONT_SMALL,
                text_color='#888888'
            ).grid(row=0, column=0, padx=10, pady=10, sticky='w')
            return

        # 显示每个 feature 及其删除按钮
        for i, feat in enumerate(self.features_list):
            row = i // 3  # 每行 3 个
            col = (i % 3) * 3  # 每个 feature 占 3 列

            # 创建 frame 包裹单个 feature
            feat_frame = ctk.CTkFrame(self.list_frame, fg_color='#2a2a2a', corner_radius=4)
            feat_frame.grid(row=row, column=col, padx=5, pady=5, sticky='ew')
            self.list_frame.grid_columnconfigure(col, weight=1)

            # 显示 feature 名和策略
            feat_text = f"{feat['name']} ({feat['policy']})"
            ctk.CTkLabel(
                feat_frame,
                text=feat_text,
                font=CTK_FONT_SMALL,
                text_color='#64b5f6'
            ).pack(side='left', padx=5, pady=2)

            # 删除按钮
            def make_remove_handler(idx):
                return lambda idx=idx: self._remove_feature(idx)

            del_btn = ctk.CTkButton(
                feat_frame,
                text='X',
                width=24,
                height=20,
                fg_color='#f44336',
                hover_color='#d32f2f',
                font=CTK_FONT_SMALL,
                command=make_remove_handler(i)
            )
            del_btn.pack(side='right', padx=2, pady=2)

    def get_config(self) -> dict:
        """获取配置数据."""
        return {
            'features': self.features_list.copy(),
        }

    def load_config(self, config: dict) -> None:
        """加载配置数据."""
        self.features_list = config.get('features', []).copy()
        self._refresh_feature_list()'''

# 使用更简单的方法：直接查找并替换类定义
start_marker = 'class CPUFeatureSubTab(BaseConfigTab):'
end_marker = 'class CPUCacheSubTab(BaseConfigTab):'

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print(f"Error: Could not find markers. start={start_idx}, end={end_idx}")
    exit(1)

# 构建新内容
new_content = content[:start_idx] + new_code + '\n\n' + content[end_idx:]

with open('panels/vm_panel/tabs/cpu_model_topology_tab.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Successfully updated CPUFeatureSubTab")
