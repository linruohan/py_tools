"""NUMA 节点优化配置 Tab - NUMA Node Tuning."""

import customtkinter as ctk

from components.base_tab import BaseConfigTab
from utils.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class NUMANodeTuningTab(BaseConfigTab):
    """NUMA 节点优化配置 Tab."""

    def _init_ui(self) -> None:
        """初始化界面 - 所有 section 合并为一个，使用 pack 布局，左对齐."""
        # 主容器
        main_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        main_frame.pack(fill='both', expand=True, padx=5, pady=5)

        # 标题
        ctk.CTkLabel(
            main_frame, text='NUMA 内存策略', font=CTK_FONT_BOLD, text_color='#64b5f6'
        ).pack(anchor='w', padx=10, pady=(10, 10))

        # 第一行：模式 | 节点集 | 放置
        row1_frame = ctk.CTkFrame(main_frame, fg_color='transparent')
        row1_frame.pack(fill='x', padx=10, pady=3)

        # 模式
        ctk.CTkLabel(row1_frame, text='模式:', font=CTK_FONT_MAIN, width=60, anchor='w').pack(
            side='left'
        )
        self.mode = ctk.CTkOptionMenu(
            row1_frame,
            values=['None', 'strict', 'interleave', 'preferred', 'restrictive'],
            width=100,
            font=CTK_FONT_SMALL,
            command=self._trigger_change,
        )
        self.mode.set('None')
        self.mode.pack(side='left', padx=(0, 10))

        # 节点集
        ctk.CTkLabel(row1_frame, text='节点集:', font=CTK_FONT_MAIN, width=60, anchor='w').pack(
            side='left'
        )
        self.nodeset = ctk.CTkEntry(row1_frame, placeholder_text='1-4,^3', width=120)
        self.nodeset.pack(side='left', padx=(0, 10))
        self.nodeset.bind('<KeyRelease>', lambda e: self._trigger_change())

        # 放置
        ctk.CTkLabel(row1_frame, text='放置:', font=CTK_FONT_MAIN, width=50, anchor='w').pack(
            side='left'
        )
        self.placement = ctk.CTkOptionMenu(
            row1_frame,
            values=['None', 'static', 'auto'],
            width=80,
            font=CTK_FONT_SMALL,
            command=self._trigger_change,
        )
        self.placement.set('None')
        self.placement.pack(side='left')

        # NUMA 节点配置区域标题
        node_title_frame = ctk.CTkFrame(main_frame, fg_color='transparent')
        node_title_frame.pack(fill='x', padx=10, pady=(15, 5))

        ctk.CTkLabel(
            node_title_frame,
            text='NUMA 节点配置 (memnode)',
            font=CTK_FONT_BOLD,
            text_color='#4caf50',
        ).pack(side='left')

        # 添加节点按钮
        self.add_node_btn = ctk.CTkButton(
            node_title_frame,
            text='+ 添加节点',
            width=80,
            height=24,
            font=CTK_FONT_SMALL,
            command=self._add_memnode_row,
        )
        self.add_node_btn.pack(side='right')

        # MemNode 条目容器
        self.memnode_container = ctk.CTkFrame(main_frame, fg_color='transparent')
        self.memnode_container.pack(fill='both', expand=True, padx=10, pady=5)

        self.memnode_rows = []  # 存储每个 memnode 行的控件

        # 说明区域
        info_frame = ctk.CTkFrame(main_frame, fg_color='transparent')
        info_frame.pack(fill='x', padx=10, pady=(10, 5))

        info_text = (
            '模式 (mode): interleave - 在所有节点间均衡分配 |\n'
            '           strict - 严格限制在指定节点，不足时失败 |\n'
            '           preferred - 优先使用指定节点，不足时使用其他 |\n'
            '           restrictive - 使用系统默认策略\n'
            '节点集 (nodeset): 指定 NUMA 节点范围，如 1-4,^3 表示节点 1-4 排除 3\n'
            '放置 (placement): static - 静态放置 | auto - 使用 numad 自动放置\n'
            'memnode: 针对每个客户机 NUMA 节点的内存分配策略'
        )
        ctk.CTkLabel(
            info_frame,
            text=info_text,
            font=CTK_FONT_SMALL,
            text_color='#888888',
            justify='left',
        ).pack(anchor='w')

    def _add_memnode_row(self, cellid: str = '', mode: str = 'strict', nodeset: str = '') -> None:
        """添加一个 memnode 配置行."""
        row_frame = ctk.CTkFrame(self.memnode_container, fg_color='transparent')
        row_frame.pack(fill='x', pady=2)

        # Cell ID
        ctk.CTkLabel(row_frame, text='Cell ID:', font=CTK_FONT_MAIN, width=60, anchor='w').pack(
            side='left'
        )
        cellid_entry = ctk.CTkEntry(row_frame, placeholder_text='0', width=60)
        cellid_entry.pack(side='left', padx=(0, 5))
        if cellid:
            cellid_entry.insert(0, cellid)
        cellid_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        # 模式
        ctk.CTkLabel(row_frame, text='模式:', font=CTK_FONT_MAIN, width=40, anchor='w').pack(
            side='left'
        )
        mode_option = ctk.CTkOptionMenu(
            row_frame,
            values=['None', 'strict', 'preferred', 'interleave', 'restrictive'],
            width=100,
            font=CTK_FONT_SMALL,
            command=self._trigger_change,
        )
        mode_option.set(mode)
        mode_option.pack(side='left', padx=(0, 5))

        # 节点集
        ctk.CTkLabel(row_frame, text='节点集:', font=CTK_FONT_MAIN, width=50, anchor='w').pack(
            side='left'
        )
        nodeset_entry = ctk.CTkEntry(row_frame, placeholder_text='1-4,^3', width=120)
        nodeset_entry.pack(side='left', padx=(0, 5))
        if nodeset:
            nodeset_entry.insert(0, nodeset)
        nodeset_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        # 删除按钮
        del_btn = ctk.CTkButton(
            row_frame,
            text='删除',
            width=50,
            height=24,
            fg_color='#e74c3c',
            hover_color='#c0392b',
            font=CTK_FONT_SMALL,
            command=lambda: self._remove_memnode_row(row_frame),
        )
        del_btn.pack(side='left')

        self.memnode_rows.append(
            {
                'frame': row_frame,
                'cellid': cellid_entry,
                'mode': mode_option,
                'nodeset': nodeset_entry,
            }
        )

    def _remove_memnode_row(self, row_frame: ctk.CTkFrame) -> None:
        """删除一个 memnode 配置行."""
        for i, row_data in enumerate(self.memnode_rows):
            if row_data['frame'] == row_frame:
                row_frame.destroy()
                self.memnode_rows.pop(i)
                self._trigger_change()
                break

    def get_config(self) -> dict:
        """获取配置数据."""
        mode_val = self.mode.get()
        placement_val = self.placement.get()
        nodeset_val = self.nodeset.get().strip()

        # 收集所有 memnode 条目
        memnodes = []
        for row_data in self.memnode_rows:
            cellid = row_data['cellid'].get().strip()
            if cellid:  # 只包含有 cellid 的条目
                node_mode = row_data['mode'].get()
                node_nodeset = row_data['nodeset'].get().strip()
                memnodes.append(
                    {
                        'cellid': cellid,
                        'mode': None if node_mode == 'None' else node_mode,
                        'nodeset': node_nodeset if node_nodeset else None,
                    }
                )

        return {
            'memory_mode': None if mode_val == 'None' else mode_val,
            'memory_nodeset': nodeset_val if nodeset_val else None,
            'memory_placement': None if placement_val == 'None' else placement_val,
            'memnodes': memnodes,
        }

    def to_xml(self) -> dict:
        """生成 XML 配置字典."""
        return {'numa_node_tuning': self.get_config()}

    def load_config(self, config: dict) -> None:
        """加载配置数据."""
        if not config:
            return

        numa_config = config.get('numa_node_tuning', config)

        # 设置基本配置
        memory_mode = numa_config.get('memory_mode')
        if memory_mode:
            self.mode.set(memory_mode)
        else:
            self.mode.set('None')

        memory_nodeset = numa_config.get('memory_nodeset', '')
        self.nodeset.delete(0, 'end')
        if memory_nodeset:
            self.nodeset.insert(0, memory_nodeset)

        memory_placement = numa_config.get('memory_placement')
        if memory_placement:
            self.placement.set(memory_placement)
        else:
            self.placement.set('None')

        # 清空现有 memnode 行
        for row_data in self.memnode_rows:
            row_data['frame'].destroy()
        self.memnode_rows.clear()

        # 添加 memnode 行
        memnodes = numa_config.get('memnodes', [])
        for node in memnodes:
            cellid = str(node.get('cellid', ''))
            mode = node.get('mode', 'strict')
            if not mode:
                mode = 'None'
            nodeset = node.get('nodeset', '')
            self._add_memnode_row(cellid=cellid, mode=mode, nodeset=nodeset or '')
