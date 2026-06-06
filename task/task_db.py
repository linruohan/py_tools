"""Task Database - 任务数据库管理模块."""

import sqlite3

from pathlib import Path
from typing import Any


class TaskDatabase:
    """任务数据库管理类."""

    def __init__(self, db_path: str | None = None) -> None:
        """初始化数据库连接.

        Args:
            db_path: 数据库文件路径，默认为项目根目录下的 tasks.db
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
        """初始化任务表."""
        if self.conn is None:
            return

        cursor = self.conn.cursor()
        cursor.execute("""
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
        """)
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
            任务列表，每个任务是一个字典
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
        params = []

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
