# -*- coding: utf-8 -*-
"""
db.py —— SQLite 数据库连接辅助模块
提供统一的连接获取、行字典化与初始化调用入口。
"""
import sqlite3
import os

# 数据库文件固定放在项目根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "coal_data.db")


def get_conn():
    """获取一个数据库连接（含外键约束），返回 (conn, cursor)。"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn, conn.cursor()


def init_db():
    """初始化数据库：建表 + 灌入种子数据。见 init_db.py。"""
    import init_db
    init_db.main()


def query(sql, params=()):
    """执行查询，返回 dict 列表。"""
    conn, cur = get_conn()
    cur.execute(sql, params)
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


def execute(sql, params=()):
    """执行写操作，提交并返回影响行数。"""
    conn, cur = get_conn()
    cur.execute(sql, params)
    conn.commit()
    affected = cur.rowcount
    conn.close()
    return affected


if __name__ == "__main__":
    init_db()
    print("数据库已初始化：", DB_PATH)
