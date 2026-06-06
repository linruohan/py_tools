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
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                completed INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def add_task(self, text: str) -> int:
        """添加新任务.

        Args:
            text: 任务内容

        Returns:
            新任务的 ID
        """
        if self.conn is None:
            return -1

        cursor = self.conn.cursor()
        cursor.execute(
            'INSERT INTO tasks (text, completed) VALUES (?, 0)',
            (text,)
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
            'SELECT id, text, completed FROM tasks ORDER BY created_at ASC'
        )
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    def update_task(self, task_id: int, completed: bool | None = None, text: str | None = None) -> None:
        """更新任务.

        Args:
            task_id: 任务 ID
            completed: 完成状态
            text: 任务内容
        """
        if self.conn is None:
            return

        cursor = self.conn.cursor()
        updates = []
        params = []

        if completed is not None:
            updates.append('completed = ?')
            params.append(1 if completed else 0)

        if text is not None:
            updates.append('text = ?')
            params.append(text)

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
