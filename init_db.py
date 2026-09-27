# -*- coding: utf-8 -*-
"""
init_db.py —— 数据库初始化脚本
用法：python init_db.py
功能：创建 SQLite 数据库并灌入课程/任务/练习/文件/面试种子数据。
可重复运行（先删除旧库重建）。
"""
import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "coal_data.db")

from content import courses as c_courses
from content import tasks as c_tasks
from content import exercises as c_exercises
from content import files as c_files
from content import interview as c_interview

SCHEMA = """
CREATE TABLE IF NOT EXISTS courses(
  id INTEGER PRIMARY KEY, name TEXT, day_range TEXT, objective TEXT,
  knowledge TEXT, websites TEXT, chapters TEXT, example_code TEXT,
  practice TEXT, completion_standard TEXT, common_errors TEXT, interview_questions TEXT
);
CREATE TABLE IF NOT EXISTS tasks(
  day INTEGER PRIMARY KEY, title TEXT, today_goal TEXT, study_content TEXT,
  coding_task TEXT, estimated_time TEXT, submit_result TEXT, acceptance TEXT,
  status TEXT DEFAULT 'pending', start_time TEXT, done_time TEXT
);
CREATE TABLE IF NOT EXISTS exercises(
  id INTEGER PRIMARY KEY, title TEXT, background TEXT, initial_code TEXT,
  answer TEXT, explanation TEXT, result_output TEXT
);
CREATE TABLE IF NOT EXISTS project_files(
  id INTEGER PRIMARY KEY AUTOINCREMENT, path TEXT, purpose TEXT, template TEXT
);
CREATE TABLE IF NOT EXISTS interview_meta(
  key TEXT PRIMARY KEY, value TEXT
);
CREATE TABLE IF NOT EXISTS interview_q(
  id INTEGER PRIMARY KEY AUTOINCREMENT, category TEXT, question TEXT, answer TEXT
);
CREATE TABLE IF NOT EXISTS daily_log(
  date TEXT PRIMARY KEY, days INTEGER
);
"""


def main():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA)
    cur = conn.cursor()

    for c in c_courses.COURSES:
        cur.execute(
            "INSERT INTO courses(id,name,day_range,objective,knowledge,websites,chapters,"
            "example_code,practice,completion_standard,common_errors,interview_questions) "
            "VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
            (c["id"], c["name"], c["day_range"], c["objective"], c["knowledge"],
             c["websites"], c["chapters"], c["example_code"], c["practice"],
             c["completion_standard"], c["common_errors"], c["interview_questions"]),
        )

    for t in c_tasks.TASKS:
        cur.execute(
            "INSERT INTO tasks(day,title,today_goal,study_content,coding_task,"
            "estimated_time,submit_result,acceptance,status) "
            "VALUES(?,?,?,?,?,?,?,?, 'pending')",
            (t["day"], t["title"], t["today_goal"], t["study_content"], t["coding_task"],
             t["estimated_time"], t["submit_result"], t["acceptance"]),
        )

    for e in c_exercises.EXERCISES:
        cur.execute(
            "INSERT INTO exercises(id,title,background,initial_code,answer,explanation,result_output) "
            "VALUES(?,?,?,?,?,?,?)",
            (e["id"], e["title"], e["background"], e["initial_code"],
             e["answer"], e["explanation"], e["result_output"]),
        )

    cur.execute("INSERT INTO project_files(path,purpose,template) VALUES('(项目目录结构)','自动展示项目目录树',?)",
                (c_files.PROJECT_TREE,))
    for f in c_files.PROJECT_FILES:
        cur.execute("INSERT INTO project_files(path,purpose,template) VALUES(?,?,?)",
                    (f["path"], f["purpose"], f["template"]))

    cur.execute("INSERT INTO interview_meta VALUES('intro_3min', ?)", (c_interview.INTRO_3MIN,))
    cat_map = [
        ("tech", c_interview.TECH_QUESTIONS),
        ("sql", c_interview.SQL_QUESTIONS),
        ("python", c_interview.PYTHON_QUESTIONS),
        ("dq", c_interview.DQ_QUESTIONS),
        ("followup", c_interview.FOLLOW_UP_QUESTIONS),
    ]
    for cat, qs in cat_map:
        for q, a in qs:
            cur.execute("INSERT INTO interview_q(category,question,answer) VALUES(?,?,?)", (cat, q, a))

    conn.commit()
    conn.close()

    print("数据库初始化完成：", DB_PATH)
    print("课程:", len(c_courses.COURSES), " 任务:", len(c_tasks.TASKS),
          " 练习:", len(c_exercises.EXERCISES),
          " 文件:", len(c_files.PROJECT_FILES) + 1, " 面试题:", len(c_interview.TECH_QUESTIONS)
          + len(c_interview.SQL_QUESTIONS) + len(c_interview.PYTHON_QUESTIONS)
          + len(c_interview.DQ_QUESTIONS) + len(c_interview.FOLLOW_UP_QUESTIONS))


if __name__ == "__main__":
    main()
