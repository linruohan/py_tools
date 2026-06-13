"""Task Database - 任务数据库管理模块."""

import sqlite3

from pathlib import Path
from typing import Any


class TaskDatabase:
    """任务数据库管理类."""

    def __init__(self, db_path: str | None = None) -> None:
        """初始化数据库连接.

        Args:
            db_path: 数据库文件路径,默认为项目根目录下的 tasks.db
        """
        if db_path is None:
            # 默认在项目根目录下创建数据库
            db_path = str(Path(__file__).resolve().parent.parent / 'tasks.db')

        self.db_path = db_path
        self.conn: sqlite3.Connection | None = None
        self._connect()
        self._init_table()

    def _connect(self) -> None:
        """连接数据库."""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row

    def _init_table(self) -> None:
        """初始化任务表和标签表."""
        if self.conn is None:
            return

        cursor = self.conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                description TEXT,
                due TEXT,
                priority INTEGER DEFAULT 0,
                labels TEXT,
                completed INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP
            )
        """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS labels (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                color TEXT,
                item_order INTEGER DEFAULT 0,
                is_deleted INTEGER DEFAULT 0,
                is_favorite INTEGER DEFAULT 0,
                backend_type TEXT,
                source_id TEXT
            )
        """
        )
        self.conn.commit()

    def add_task(
        self,
        content: str,
        description: str = '',
        due: str = '',
        priority: int = 0,
        labels: str = '',
    ) -> int:
        """添加新任务.

        Args:
            content: 任务内容
            description: 任务描述
            due: 截止日期
            priority: 优先级 (0-3)
            labels: 标签

        Returns:
            新任务的 ID
        """
        if self.conn is None:
            return -1

        cursor = self.conn.cursor()
        cursor.execute(
            """INSERT INTO tasks (content, description, due, priority, labels, completed)
               VALUES (?, ?, ?, ?, ?, 0)""",
            (content, description, due, priority, labels),
        )
        self.conn.commit()
        return cursor.lastrowid

    def get_all_tasks(self) -> list[dict[str, Any]]:
        """获取所有任务.

        Returns:
            任务列表,每个任务是一个字典
        """
        if self.conn is None:
            return []

        cursor = self.conn.cursor()
        cursor.execute(
            'SELECT id, content, description, due, priority, labels, completed FROM tasks ORDER BY created_at ASC'
        )
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    def update_task(
        self,
        task_id: int,
        completed: bool | None = None,
        content: str | None = None,
        description: str | None = None,
        due: str | None = None,
        priority: int | None = None,
        labels: str | None = None,
    ) -> None:
        """更新任务.

        Args:
            task_id: 任务 ID
            completed: 完成状态
            content: 任务内容
            description: 任务描述
            due: 截止日期
            priority: 优先级
            labels: 标签
        """
        if self.conn is None:
            return

        cursor = self.conn.cursor()
        updates = []
        params: list[Any] = []

        if completed is not None:
            updates.append('completed = ?')
            params.append(1 if completed else 0)
            if completed:
                updates.append('completed_at = CURRENT_TIMESTAMP')

        if content is not None:
            updates.append('content = ?')
            params.append(content)

        if description is not None:
            updates.append('description = ?')
            params.append(description)

        if due is not None:
            updates.append('due = ?')
            params.append(due)

        if priority is not None:
            updates.append('priority = ?')
            params.append(priority)

        if labels is not None:
            updates.append('labels = ?')
            params.append(labels)

        if updates:
            updates.append('updated_at = CURRENT_TIMESTAMP')
            params.append(task_id)

            query = f'UPDATE tasks SET {", ".join(updates)} WHERE id = ?'
            cursor.execute(query, params)
            self.conn.commit()

    def delete_task(self, task_id: int) -> None:
        """删除任务.

        Args:
            task_id: 任务 ID
        """
        if self.conn is None:
            return

        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        self.conn.commit()

    def add_label(
        self,
        label_id: str,
        name: str,
        color: str = '',
        item_order: int = 0,
        is_deleted: int = 0,
        is_favorite: int = 0,
        backend_type: str = '',
        source_id: str = '',
    ) -> None:
        """添加新标签.

        Args:
            label_id: 标签ID
            name: 标签名称
            color: 标签颜色
            item_order: 排序序号
            is_deleted: 是否删除 (0/1)
            is_favorite: 是否收藏 (0/1)
            backend_type: 后端类型
            source_id: 源ID
        """
        if self.conn is None:
            return

        cursor = self.conn.cursor()
        cursor.execute(
            """INSERT OR REPLACE INTO labels
               (id, name, color, item_order, is_deleted, is_favorite, backend_type, source_id)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (label_id, name, color, item_order, is_deleted, is_favorite, backend_type, source_id),
        )
        self.conn.commit()

    def get_all_labels(self, include_deleted: bool = False) -> list[dict[str, Any]]:
        """获取所有标签.

        Args:
            include_deleted: 是否包含已删除的标签

        Returns:
            标签列表,每个标签是一个字典
        """
        if self.conn is None:
            return []

        cursor = self.conn.cursor()
        if include_deleted:
            cursor.execute('SELECT * FROM labels ORDER BY item_order ASC')
        else:
            cursor.execute('SELECT * FROM labels WHERE is_deleted = 0 ORDER BY item_order ASC')
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    def get_label_by_id(self, label_id: str) -> dict[str, Any] | None:
        """根据ID获取标签.

        Args:
            label_id: 标签ID

        Returns:
            标签字典,如果不存在则返回None
        """
        if self.conn is None:
            return None

        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM labels WHERE id = ?', (label_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def update_label(
        self,
        label_id: str,
        name: str | None = None,
        color: str | None = None,
        item_order: int | None = None,
        is_deleted: int | None = None,
        is_favorite: int | None = None,
        backend_type: str | None = None,
        source_id: str | None = None,
    ) -> None:
        """更新标签.

        Args:
            label_id: 标签ID
            name: 标签名称
            color: 标签颜色
            item_order: 排序序号
            is_deleted: 是否删除
            is_favorite: 是否收藏
            backend_type: 后端类型
            source_id: 源ID
        """
        if self.conn is None:
            return

        cursor = self.conn.cursor()
        updates = []
        params: list[Any] = []

        if name is not None:
            updates.append('name = ?')
            params.append(name)

        if color is not None:
            updates.append('color = ?')
            params.append(color)

        if item_order is not None:
            updates.append('item_order = ?')
            params.append(item_order)

        if is_deleted is not None:
            updates.append('is_deleted = ?')
            params.append(is_deleted)

        if is_favorite is not None:
            updates.append('is_favorite = ?')
            params.append(is_favorite)

        if backend_type is not None:
            updates.append('backend_type = ?')
            params.append(backend_type)

        if source_id is not None:
            updates.append('source_id = ?')
            params.append(source_id)

        if updates:
            params.append(label_id)
            query = f'UPDATE labels SET {", ".join(updates)} WHERE id = ?'
            cursor.execute(query, params)
            self.conn.commit()

    def delete_label(self, label_id: str, soft_delete: bool = True) -> None:
        """删除标签.

        Args:
            label_id: 标签ID
            soft_delete: 是否软删除(True为软删除,False为硬删除)
        """
        if self.conn is None:
            return

        cursor = self.conn.cursor()
        if soft_delete:
            cursor.execute('UPDATE labels SET is_deleted = 1 WHERE id = ?', (label_id,))
        else:
            cursor.execute('DELETE FROM labels WHERE id = ?', (label_id,))
        self.conn.commit()

    def get_favorite_labels(self) -> list[dict[str, Any]]:
        """获取收藏的标签.

        Returns:
            收藏的标签列表
        """
        if self.conn is None:
            return []

        cursor = self.conn.cursor()
        cursor.execute(
            'SELECT * FROM labels WHERE is_favorite = 1 AND is_deleted = 0 ORDER BY item_order ASC'
        )
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    def close(self) -> None:
        """关闭数据库连接."""
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def __enter__(self) -> 'TaskDatabase':
        """进入上下文管理器."""
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """退出上下文管理器."""
        self.close()
