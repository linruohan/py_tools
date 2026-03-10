"""内存管理 Tab - 内存平衡."""

import customtkinter as ctk

from ..styles import CTK_FONT_MAIN, CTK_FONT_BOLD, CTK_FONT_SMALL, BG_COLOR_CONTENT


class MemoryTab(ctk.CTkFrame):
    """内存管理 Tab."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent')
        self.on_change_callback = on_change_callback

        # 控件引用
        self.balloon_check = None
        self.balloon_target_entry = None

        # 初始化 UI
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面."""
        # 配置 grid 权重
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)

        balloon_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=8)
        balloon_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=10)
        balloon_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            balloon_frame, text='内存平衡', font=CTK_FONT_BOLD, text_color='#9ccc65'
        ).grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky='w')

        # 启用内存平衡
        self.balloon_check = ctk.CTkCheckBox(
            balloon_frame, text='启用内存平衡', font=CTK_FONT_SMALL,
            command=self._toggle_balloon_entry
        )
        self.balloon_check.grid(row=1, column=0, padx=10, pady=5, sticky='w')

        # 目标内存
        ctk.CTkLabel(
            balloon_frame, text='目标内存 (MB):', font=CTK_FONT_MAIN, width=100, anchor='w'
        ).grid(row=1, column=1, padx=10, pady=5, sticky='w')
        self.balloon_target_entry = ctk.CTkEntry(balloon_frame, width=100, font=CTK_FONT_SMALL)
        self.balloon_target_entry.grid(row=1, column=2, padx=5, pady=5, sticky='w')
        self.balloon_target_entry.insert(0, '2048')
        self.balloon_target_entry.configure(state='disabled')

    def _toggle_balloon_entry(self):
        """切换内存平衡输入框状态."""
        if self.balloon_check.get():
            self.balloon_target_entry.configure(state='normal')
        else:
            self.balloon_target_entry.configure(state='disabled')
        self._trigger_change()

    def _trigger_change(self):
        """触发变化回调."""
        if self.on_change_callback:
            self.on_change_callback()

    def get_balloon_config(self):
        """获取内存平衡配置."""
        if self.balloon_check.get():
            return {
                'target': int(self.balloon_target_entry.get().strip() or '2048'),
            }
        return None
