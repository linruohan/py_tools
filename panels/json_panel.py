"""Json Panel"""

import json
import re
from tkinter import END, MULTIPLE, Listbox, filedialog, messagebox

import customtkinter as ctk
import pandas as pd


class DragSortListbox(Listbox):
    """支持拖动排序的Listbox子类"""

    def __init__(self, master, **kwargs):
        default_kwargs = {
                    "bg": "#1a1a1a",       # 深黑色背景（匹配ctk dark主题）
                    "fg": "#ffffff",       # 白色文字
                    "selectbackground": "#3a3a3a",  # 选中项背景色（浅灰）
                    "selectforeground": "#ffffff",  # 选中项文字色
                    "activestyle": "none", # 取消选中时的虚线框
                    "bd": 0,               # 去掉边框
                    "highlightthickness": 0, # 去掉聚焦边框
                }
        # 合并默认样式和传入的参数（传入的参数会覆盖默认值）
        default_kwargs.update(kwargs)
        super().__init__(master, **default_kwargs)
        self.fg_color = "transparent"
        self.bind("<Button-1>", self._on_click)
        self.bind("<B1-Motion>", self._on_drag)
        self.drag_index = None  # 记录拖动项的初始索引

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
        self.fg_color = "transparent"

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.init_ui()

    def init_ui(self):
        # ========== 顶部JSON输入区域 ==========
        input_frame = ctk.CTkFrame(self)
        input_frame.pack(fill="x", padx=20, pady=10)

        input_label = ctk.CTkLabel(input_frame, text="JSON 输入:", font=("Arial", 12, "bold"))
        input_label.pack(anchor="w", padx=10, pady=5)

        # JSON输入文本框
        self.json_textbox = ctk.CTkTextbox(input_frame, height=150, font=("Consolas", 10))
        self.json_textbox.pack(fill="both", padx=10, pady=5, expand=True)

        # 功能按钮
        btn_frame = ctk.CTkFrame(input_frame)
        btn_frame.pack(side="right", padx=10, pady=5)

        parse_btn = ctk.CTkButton(btn_frame, text="解析 JSON", command=self.parse_json)
        parse_btn.pack(side="left", padx=5)

        self.back_btn = ctk.CTkButton(btn_frame, text="返回主Key", command=self.back_to_main_keys, state="disabled")
        self.back_btn.pack(side="left", padx=5)

        # ========== 中间Key展示区域 ==========
        middle_frame = ctk.CTkFrame(self)
        middle_frame.pack(fill="both", padx=20, pady=10, expand=True)

        # Key列表区域
        key_frame = ctk.CTkFrame(middle_frame)
        key_frame.pack(fill="both", padx=10, pady=10, expand=True)

        self.key_label = ctk.CTkLabel(key_frame, text="JSON 主Key列表（支持拖动排序）", font=("Arial", 12, "bold"))
        self.key_label.pack(anchor="w", padx=10, pady=5)

        # 排序按钮（保留升序/降序，新增拖动排序）
        sort_frame = ctk.CTkFrame(key_frame)
        sort_frame.pack(fill="x", padx=10, pady=5)

        sort_asc_btn = ctk.CTkButton(sort_frame, text="升序排序", command=lambda: self.sort_keys("asc"), width=80)
        sort_asc_btn.pack(side="left", padx=5)

        sort_desc_btn = ctk.CTkButton(sort_frame, text="降序排序", command=lambda: self.sort_keys("desc"), width=80)
        sort_desc_btn.pack(side="left", padx=5)

        # Key列表框（替换为支持拖动排序的自定义Listbox）
        self.key_listbox = DragSortListbox(key_frame, selectmode=MULTIPLE, font=("Consolas", 10))
        self.key_listbox.pack(fill="both", padx=10, pady=5, expand=True)
        self.key_listbox.bind("<<ListboxSelect>>", self.on_key_select)

        # ========== 底部操作区域 ==========
        bottom_frame = ctk.CTkFrame(self)
        bottom_frame.pack(fill="x", padx=20, pady=10)

        # 生成Excel按钮
        generate_btn = ctk.CTkButton(
            bottom_frame, text="生成 Excel 文件", command=self.generate_excel, font=("Arial", 12, "bold"), height=40
        )
        generate_btn.pack(padx=10, pady=10)

    def parse_json(self):
        """解析输入的JSON文本"""
        try:
            # 清空列表
            self.key_listbox.delete(0, END)

            # 获取文本框内容
            json_text = self.json_textbox.get("1.0", END).strip()
            if not json_text:
                messagebox.showwarning("警告", "请输入JSON文本！")
                return

            # 解析JSON
            self.json_data = json.loads(json_text)

            # 检查是否为字典类型
            if not isinstance(self.json_data, dict):
                messagebox.showwarning("警告", "JSON根节点必须是对象（字典）类型！")
                return

            # 获取所有原始主Key并显示
            self.original_main_keys = list(self.json_data.keys())
            self.current_selected_list_key = None
            self.current_list_data = None
            self.current_list_keys = []

            # 显示原始主Key（标记列表类型）
            for key in self.original_main_keys:
                value_type = " [LIST]" if isinstance(self.json_data[key], list) else ""
                self.key_listbox.insert(END, f"{key}{value_type}")

            # 更新UI状态
            self.key_label.configure(text="JSON 主Key列表（支持拖动排序）")
            self.back_btn.configure(state="disabled")

            messagebox.showinfo("成功", "JSON解析成功！")

        except json.JSONDecodeError as e:
            messagebox.showerror("错误", f"JSON格式错误：{e!s}")
        except Exception as e:
            messagebox.showerror("错误", f"解析失败：{e!s}")

    def on_key_select(self, event):
        """选中Key后的回调函数"""
        selected_indices = self.key_listbox.curselection()
        if not selected_indices:
            return

        selected_index = selected_indices[0]
        selected_key_display = self.key_listbox.get(selected_index)

        # 如果当前显示的是原始主Key
        if self.current_selected_list_key is None:
            # 清理类型标记，获取纯Key名称
            pure_key = re.sub(r" \[LIST\]$", "", selected_key_display)

            # 检查该Key是否为列表类型
            if pure_key in self.json_data and isinstance(self.json_data[pure_key], list):
                list_data = self.json_data[pure_key]
                # 确保列表非空且第一个元素是字典
                if len(list_data) > 0 and isinstance(list_data[0], dict):
                    self.current_selected_list_key = pure_key
                    self.current_list_data = list_data
                    self.current_list_keys = list(list_data[0].keys())

                    # 清空列表并显示该列表的内部Key
                    self.key_listbox.delete(0, END)
                    for key in self.current_list_keys:
                        self.key_listbox.insert(END, key)

                    # 更新UI
                    self.key_label.configure(text=f"{pure_key} 列表的内部Key（支持拖动排序）")
                    self.back_btn.configure(state="normal")

    def back_to_main_keys(self):
        """返回显示原始主Key列表"""
        # 清空列表
        self.key_listbox.delete(0, END)

        # 重新显示原始主Key
        for key in self.original_main_keys:
            value_type = " [LIST]" if isinstance(self.json_data[key], list) else ""
            self.key_listbox.insert(END, f"{key}{value_type}")

        # 重置状态
        self.key_label.configure(text="JSON 主Key列表（支持拖动排序）")
        self.back_btn.configure(state="disabled")
        self.current_selected_list_key = None
        self.current_list_data = None
        self.current_list_keys = []

    def sort_keys(self, sort_type):
        """对当前显示的Key进行升序/降序排序"""
        if self.current_selected_list_key:
            # 排序列表内部Key
            if not self.current_list_keys:
                messagebox.showwarning("警告", "暂无Key可排序！")
                return

            if sort_type == "asc":
                self.current_list_keys.sort()
            else:
                self.current_list_keys.sort(reverse=True)

            # 重新显示
            self.key_listbox.delete(0, END)
            for key in self.current_list_keys:
                self.key_listbox.insert(END, key)
        else:
            # 排序原始主Key
            if not self.original_main_keys:
                messagebox.showwarning("警告", "暂无Key可排序！")
                return

            if sort_type == "asc":
                self.original_main_keys.sort()
            else:
                self.original_main_keys.sort(reverse=True)

            # 重新显示
            self.key_listbox.delete(0, END)
            for key in self.original_main_keys:
                value_type = " [LIST]" if isinstance(self.json_data[key], list) else ""
                self.key_listbox.insert(END, f"{key}{value_type}")

    def generate_excel(self):
        """根据选中的Key生成Excel文件"""
        try:
            if not self.json_data:
                messagebox.showwarning("警告", "请先解析有效的JSON数据！")
                return

            # 情况1：选中了列表Key（如authors），显示的是列表内部Key
            if self.current_selected_list_key and self.current_list_data:
                # 获取选中的列表内部Key
                selected_indices = self.key_listbox.curselection()
                if not selected_indices:
                    messagebox.showwarning("警告", "请至少选择一个列表内部Key！")
                    return

                # 收集选中的Key
                selected_keys = [self.key_listbox.get(idx) for idx in selected_indices]

                # 提取数据
                excel_data = []
                for item in self.current_list_data:
                    if isinstance(item, dict):
                        row_data = {k: item.get(k, "") for k in selected_keys}
                        excel_data.append(row_data)

                if not excel_data:
                    messagebox.showwarning("警告", "没有可导出的数据！")
                    return

                # 转换为DataFrame
                df = pd.DataFrame(excel_data)

                # 选择保存路径
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".xlsx",
                    filetypes=[("Excel文件", "*.xlsx"), ("所有文件", "*.*")],
                    title="保存Excel文件",
                    initialfile=f"{self.current_selected_list_key}.xlsx",
                )

                if file_path:
                    # 写入Excel文件（工作表名使用选中的列表Key）
                    with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
                        safe_sheet_name = self.current_selected_list_key[:31]
                        df.to_excel(writer, sheet_name=safe_sheet_name, index=False)

                    messagebox.showinfo("成功", f"Excel文件已生成：{file_path}")

            # 情况2：显示的是原始主Key
            else:
                selected_indices = self.key_listbox.curselection()
                if not selected_indices:
                    messagebox.showwarning("警告", "请先选择一个列表类型的主Key！")
                    return

                messagebox.showinfo("提示", "请先选中一个列表类型的主Key（如authors），进入其内部Key列表后再导出！")

        except Exception as e:
            messagebox.showerror("错误", f"生成Excel失败：{e!s}")
