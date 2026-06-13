"""Json Panel"""

import json
import re

from tkinter import END, MULTIPLE, Listbox, filedialog, messagebox

import customtkinter as ctk
import pandas as pd

# 全局字体配置(统一美化)
CTK_FONT_MAIN = ('Microsoft YaHei UI', 12)  # 主要字体
CTK_FONT_BOLD = ('Microsoft YaHei UI', 12, 'bold')  # 加粗字体
CTK_FONT_MONO = ('Consolas', 11)  # 等宽字体(JSON/Key显示)
CTK_FONT_SMALL = ('Microsoft YaHei UI', 10)  # 小字体

# 全局背景色常量(统一管理,便于修改)
BG_COLOR_MAIN = '#242424'  # 面板主背景
BG_COLOR_CONTENT = '#1e1e1e'  # JSON输入框/信息栏背景
BG_COLOR_SELECT = '#404040'  # 选中项背景


class DragSortListbox(Listbox):
    """支持拖动排序的Listbox子类(适配深色主题)"""

    def __init__(self, master, **kwargs):
        default_kwargs = {
            'bg': BG_COLOR_CONTENT,  # 统一使用内容背景色
            'fg': '#f0f0f0',  # 浅白色文字
            'selectbackground': BG_COLOR_SELECT,  # 选中项背景
            'selectforeground': '#ffffff',  # 选中项文字
            'activestyle': 'none',  # 取消选中虚线框
            'bd': 0,  # 去掉边框
            'highlightthickness': 0,  # 去掉聚焦边框
            'font': CTK_FONT_MONO,  # 统一等宽字体
            'relief': 'flat',  # 扁平样式
        }
        default_kwargs.update(kwargs)
        super().__init__(master, **default_kwargs)  # type: ignore[arg-type]

        self.drag_index = None  # 记录拖动项的初始索引
        self.bind('<Button-1>', self._on_click)
        self.bind('<B1-Motion>', self._on_drag)

    def _on_click(self, event):
        """鼠标点击时记录选中项索引"""
        self.drag_index = self.nearest(event.y)

    def _on_drag(self, event):
        """鼠标拖动时调整选中项位置"""
        if self.drag_index is None:
            return
        current_index = self.nearest(event.y)
        if current_index != self.drag_index:
            # 获取拖动项的内容
            drag_item = self.get(self.drag_index)
            # 删除原位置项
            self.delete(self.drag_index)
            # 插入到新位置
            self.insert(current_index, drag_item)
            # 更新拖动索引
            self.drag_index = current_index
            # 保持选中状态
            self.selection_set(current_index)


class JsonPanel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.corner_radius = 0
        self.fg_color = 'transparent'

        # 主布局:左侧4/5,右侧1/5,底部信息栏跨两列
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)  # 底部信息栏高度固定
        self.grid_columnconfigure(0, weight=4)  # 左侧占4份
        self.grid_columnconfigure(1, weight=1)  # 右侧占1份

        # 导航历史栈，用于支持多级嵌套回退
        self.navigation_stack = []

        self.init_left_panel()  # 左侧JSON输入面板
        self.init_right_panel()  # 右侧Key列表+操作面板
        self.init_info_bar()  # 底部信息提示栏

    def init_left_panel(self):
        """初始化左侧JSON输入面板(占4/5)"""
        left_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_MAIN, corner_radius=8)
        left_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # 左侧面板布局配置
        left_frame.grid_rowconfigure(1, weight=1)  # JSON输入框占满剩余空间
        left_frame.grid_columnconfigure(0, weight=1)

        # 第一行:标题 + 解析按钮(右侧)
        top_frame = ctk.CTkFrame(left_frame, fg_color='transparent')
        top_frame.grid(row=0, column=0, padx=15, pady=10, sticky='ew')
        top_frame.grid_columnconfigure(0, weight=1)

        # 标题
        title_label = ctk.CTkLabel(
            top_frame,
            text='JSON Data Input',
            font=CTK_FONT_BOLD,
            text_color='#64b5f6',  # 浅蓝色标题
        )
        title_label.grid(row=0, column=0, sticky='w')

        # 解析按钮(第一行右侧)
        self.parse_btn = ctk.CTkButton(
            top_frame,
            text='Parse JSON',
            command=self.parse_json,
            font=CTK_FONT_MAIN,
            fg_color='#2196f3',
            hover_color='#1976d2',
            corner_radius=6,
            width=120,
            height=36,
        )
        self.parse_btn.grid(row=0, column=1, sticky='e')

        # 第二行:JSON输入文本框(占满剩余空间)
        self.json_textbox = ctk.CTkTextbox(
            left_frame,
            font=CTK_FONT_MONO,
            fg_color=BG_COLOR_CONTENT,  # 内容背景色
            text_color='#f0f0f0',
            border_color='#333333',
            border_width=1,
            corner_radius=6,
        )
        self.json_textbox.grid(row=1, column=0, padx=15, pady=(0, 15), sticky='nsew')

    def init_right_panel(self):
        """初始化右侧Key列表+操作面板(占1/5)"""
        right_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_MAIN, corner_radius=8)
        right_frame.grid(row=0, column=1, padx=(0, 10), pady=10, sticky='nsew')

        # 右侧面板布局配置
        right_frame.grid_rowconfigure(2, weight=1)  # Key列表占满剩余空间
        right_frame.grid_columnconfigure(0, weight=1)

        # 第一行:标题 + 返回主Key + 升序 + 降序(同一行)
        row1_frame = ctk.CTkFrame(right_frame, fg_color='transparent')
        row1_frame.grid(row=0, column=0, padx=15, pady=10, sticky='ew')
        row1_frame.grid_columnconfigure(0, weight=1)

        # 标题(左侧)
        self.key_label = ctk.CTkLabel(
            row1_frame,
            text='JSON Main Key List',
            font=CTK_FONT_BOLD,
            text_color='#81c784',  # 浅绿色标题
        )
        self.key_label.grid(row=0, column=0, sticky='w')

        # 按钮组(右侧)
        btn_group_frame = ctk.CTkFrame(row1_frame, fg_color='transparent')
        btn_group_frame.grid(row=0, column=1, sticky='e')

        # 返回主Key按钮
        self.back_btn = ctk.CTkButton(
            btn_group_frame,
            text='Back to Main Keys',
            command=self.back_to_main_keys,
            font=CTK_FONT_SMALL,
            fg_color='#ff9800',
            hover_color='#f57c00',
            corner_radius=6,
            state='disabled',
            width=80,
            height=30,
        )
        self.back_btn.pack(side='left', padx=(0, 5))

        # 升序按钮
        sort_asc_btn = ctk.CTkButton(
            btn_group_frame,
            text='Asc',
            command=lambda: self.sort_keys('asc'),
            font=CTK_FONT_SMALL,
            fg_color='#4caf50',
            hover_color='#388e3c',
            corner_radius=4,
            width=50,
            height=30,
        )
        sort_asc_btn.pack(side='left', padx=(0, 5))

        # 降序按钮
        sort_desc_btn = ctk.CTkButton(
            btn_group_frame,
            text='Desc',
            command=lambda: self.sort_keys('desc'),
            font=CTK_FONT_SMALL,
            fg_color='#f44336',
            hover_color='#d32f2f',
            corner_radius=4,
            width=50,
            height=30,
        )
        sort_desc_btn.pack(side='left')

        # 第二行:生成Excel按钮(末尾/右侧)
        row2_frame = ctk.CTkFrame(right_frame, fg_color='transparent')
        row2_frame.grid(row=1, column=0, padx=15, pady=(0, 10), sticky='ew')
        row2_frame.grid_columnconfigure(0, weight=1)

        generate_btn = ctk.CTkButton(
            row2_frame,
            text='生成 Excel',
            command=self.generate_excel,
            font=CTK_FONT_BOLD,
            fg_color='#9c27b0',
            hover_color='#7b1fa2',
            corner_radius=6,
            height=36,
            width=120,
        )
        generate_btn.grid(row=0, column=1, sticky='e')

        # 第三行:Key列表框(拖动排序)
        self.key_listbox = DragSortListbox(
            right_frame, selectmode=MULTIPLE, font=CTK_FONT_MONO, relief='flat'
        )
        self.key_listbox.grid(row=2, column=0, padx=15, pady=(0, 15), sticky='nsew')
        self.key_listbox.bind('<<ListboxSelect>>', self.on_key_select)

    def init_info_bar(self):
        """初始化底部信息提示栏"""
        # 核心修改:背景色改为和JSON输入框一致的 BG_COLOR_CONTENT (#1e1e1e)
        self.info_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=0, height=30)
        self.info_frame.grid(row=1, column=0, columnspan=2, padx=0, pady=0, sticky='ew')
        # 禁止框架高度被拉伸
        self.info_frame.grid_propagate(False)

        # 信息提示标签
        self.info_label = ctk.CTkLabel(
            self.info_frame,
            text='就绪',
            font=CTK_FONT_SMALL,
            text_color='#aaaaaa',
            anchor='w',
        )
        self.info_label.pack(fill='x', padx=20, pady=5)

    def update_info(self, text: str, is_success: bool = True):
        """更新底部信息栏内容
        Args:
            text: 提示文本
            is_success: True=成功(绿色),False=失败(红色)
        """
        color = '#4caf50' if is_success else '#f44336'
        self.info_label.configure(text=text, text_color=color)

    def parse_json(self):
        """解析输入的JSON文本"""
        try:
            # 清空列表
            self.key_listbox.delete(0, END)

            # 获取文本框内容
            json_text = self.json_textbox.get('1.0', END).strip()
            if not json_text:
                messagebox.showwarning('警告', '请输入JSON文本!')
                self.update_info('请输入JSON文本', False)
                return

            # 解析JSON
            self.json_data = json.loads(json_text)

            # 检查是否为字典类型
            if not isinstance(self.json_data, dict):
                messagebox.showwarning('警告', 'JSON根节点必须是对象(字典)类型!')
                self.update_info('JSON根节点必须是对象类型', False)
                return

            # 重置导航栈，保存根数据
            self.navigation_stack = []
            self.current_data = self.json_data
            self.current_keys = list(self.json_data.keys())

            # 显示原始主Key(标记类型)
            self._display_keys(self.current_keys, self.current_data)

            # 更新UI状态
            self.key_label.configure(text='JSON Main Key List (Drag to Sort)')
            self.back_btn.configure(state='disabled')

            messagebox.showinfo('成功', 'JSON解析成功!')
            self.update_info('JSON解析成功', True)

        except json.JSONDecodeError as e:
            err_msg = f'JSON格式错误:{e!s}'
            messagebox.showerror('错误', err_msg)
            self.update_info(err_msg, False)
        except Exception as e:
            err_msg = f'解析失败:{e!s}'
            messagebox.showerror('错误', err_msg)
            self.update_info(err_msg, False)

    def _display_keys(self, keys, data):
        """显示指定数据对象的Key列表，带类型标记"""
        self.key_listbox.delete(0, END)
        for key in keys:
            value = data.get(key)
            if isinstance(value, list):
                self.key_listbox.insert(END, f'{key} [LIST]')
            elif isinstance(value, dict):
                self.key_listbox.insert(END, f'{key} [DICT]')
            else:
                self.key_listbox.insert(END, key)

    def on_key_select(self, event):
        """选中Key后的回调函数，支持递归展开嵌套结构"""
        selected_indices = self.key_listbox.curselection()
        if not selected_indices:
            return

        selected_index = selected_indices[0]
        selected_key_display = self.key_listbox.get(selected_index)

        # 清理类型标记,获取纯Key名称
        pure_key = re.sub(r' \[(LIST|DICT)\]$', '', selected_key_display)

        # 检查该Key是否存在于当前数据中
        if pure_key not in self.current_data:
            return

        value = self.current_data[pure_key]

        # 情况1: 值是字典类型，展开显示其Key
        if isinstance(value, dict):
            # 保存当前状态到导航栈
            self.navigation_stack.append(
                {
                    'data': self.current_data,
                    'keys': self.current_keys,
                    'label': self.key_label.cget('text'),
                }
            )

            # 更新当前状态为嵌套字典
            self.current_data = value
            self.current_keys = list(value.keys())

            # 显示嵌套字典的Key（不自动选中，让用户选择要展开的Key）
            self._display_keys(self.current_keys, self.current_data)

            # 更新UI
            self.key_label.configure(text=f'{pure_key} Inner Keys')
            self.back_btn.configure(state='normal')
            self.update_info(f'已进入字典:{pure_key}', True)

        # 情况2: 值是列表类型
        elif isinstance(value, list):
            # 确保列表非空且第一个元素是字典
            if len(value) > 0 and isinstance(value[0], dict):
                # 保存当前状态到导航栈
                self.navigation_stack.append(
                    {
                        'data': self.current_data,
                        'keys': self.current_keys,
                        'label': self.key_label.cget('text'),
                    }
                )

                # 更新当前状态为列表数据
                self.current_data = value
                self.current_keys = list(value[0].keys())

                # 显示列表元素的Key（默认不选中，让用户自由选择）
                self._display_keys(self.current_keys, value[0])

                # 更新UI
                self.key_label.configure(text=f'{pure_key} Inner Keys')
                self.back_btn.configure(state='normal')
                self.update_info(f'已进入列表:{pure_key}', True)

    def back_to_main_keys(self):
        """返回上一级Key列表（支持多级嵌套回退）"""
        # 如果导航栈为空，说明已经在根节点
        if not self.navigation_stack:
            self.update_info('已经在根节点', False)
            return

        # 从导航栈弹出上一级状态
        prev_state = self.navigation_stack.pop()
        self.current_data = prev_state['data']
        self.current_keys = prev_state['keys']

        # 显示上一级的Key
        self._display_keys(self.current_keys, self.current_data)

        # 更新UI
        self.key_label.configure(text=prev_state['label'])
        # 如果导航栈为空，禁用返回按钮
        self.back_btn.configure(state='disabled' if not self.navigation_stack else 'normal')
        self.update_info('已返回上一级', True)

    def sort_keys(self, sort_type):
        """对当前显示的Key进行升序/降序排序"""
        try:
            if not self.current_keys:
                messagebox.showwarning('警告', '暂无Key可排序!')
                self.update_info('暂无Key可排序', False)
                return

            if sort_type == 'asc':
                self.current_keys.sort()
                self.update_info('Key已升序排列', True)
            else:
                self.current_keys.sort(reverse=True)
                self.update_info('Key已降序排列', True)

            # 重新显示
            self._display_keys(self.current_keys, self.current_data)
        except Exception as e:
            err_msg = f'排序失败:{e!s}'
            messagebox.showerror('错误', err_msg)
            self.update_info(err_msg, False)

    def generate_excel(self):
        """根据选中的Key生成Excel文件"""
        try:
            if not hasattr(self, 'json_data') or not self.json_data:
                messagebox.showwarning('警告', '请先解析有效的JSON数据!')
                self.update_info('请先解析JSON数据', False)
                return

            # 检查当前数据是否是列表类型（已进入列表内部）
            if isinstance(self.current_data, list) and len(self.current_data) > 0:
                # 获取选中的列表内部Key
                selected_indices = self.key_listbox.curselection()

                # 如果没有选中任何Key，导出所有字段；否则导出选中的字段
                if not selected_indices:
                    selected_keys = self.current_keys.copy()
                else:
                    selected_keys = [self.key_listbox.get(idx) for idx in selected_indices]

                # 提取数据
                excel_data = []
                for item in self.current_data:
                    if isinstance(item, dict):
                        row_data = {k: item.get(k, '') for k in selected_keys}
                        excel_data.append(row_data)

                if not excel_data:
                    messagebox.showwarning('警告', '没有可导出的数据!')
                    self.update_info('无数据可导出', False)
                    return

                # 转换为DataFrame
                df = pd.DataFrame(excel_data)

                # 获取当前列表的名称（从导航栈获取）
                list_name = 'data'
                if self.navigation_stack:
                    prev_state = self.navigation_stack[-1]
                    # 查找当前数据在上级数据中的Key名
                    for key, value in prev_state['data'].items():
                        if value is self.current_data:
                            list_name = key
                            break

                # 选择保存路径
                file_path = filedialog.asksaveasfilename(
                    defaultextension='.xlsx',
                    filetypes=[('Excel文件', '*.xlsx'), ('所有文件', '*.*')],
                    title='保存Excel文件',
                    initialfile=f'{list_name}.xlsx',
                )

                if not file_path:
                    self.update_info('已取消保存', False)
                    return

                # 写入Excel文件(工作表名使用列表名称)
                with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                    safe_sheet_name = list_name[:31]
                    df.to_excel(writer, sheet_name=safe_sheet_name, index=False)

                success_msg = f'生成成功:{file_path}'
                messagebox.showinfo('成功', success_msg)
                self.update_info(success_msg, True)

            # 情况2:显示的是字典类型的Key
            else:
                messagebox.showinfo(
                    '提示',
                    '请先选中一个列表类型的Key,进入其内部Key列表后再导出!',
                )
                self.update_info('请选择列表类型Key并进入内部', False)

        except Exception as e:
            err_msg = f'生成失败:{e!s}'
            messagebox.showerror('错误', err_msg)
            self.update_info(err_msg, False)
