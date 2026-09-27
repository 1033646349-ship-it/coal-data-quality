@echo off
chcp 65001 >nul
echo ============================================
echo  煤矿大数据管理项目学习平台 - Windows 启动
echo ============================================
cd /d "%~dp0"

REM 优先使用 Anaconda 3.9 创建项目独立虚拟环境（不污染系统 Python）
if not exist .venv\Scripts\python.exe (
    echo [首次运行] 创建独立虚拟环境 .venv ...
    if exist D:\anaconda3\python.exe (
        D:\anaconda3\python.exe -m venv .venv
    ) else (
        python -m venv .venv
    )
    if not exist .venv\Scripts\python.exe (
        echo 虚拟环境创建失败，请检查 Python 是否已安装。
        pause
        exit /b 1
    )
)

REM 安装依赖
echo [安装依赖] ...
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 (
    echo 依赖安装失败，请检查网络或 Python 环境。
    pause
    exit /b 1
)

REM 初始化数据库
if not exist coal_data.db (
    echo [初始化数据库] ...
    .venv\Scripts\python.exe init_db.py
)

REM 生成示例数据
if not exist data\coal_production.csv (
    echo [生成示例数据] ...
    .venv\Scripts\python.exe data\gen_sample_data.py
)

REM 启动学习平台
echo.
echo [启动] 浏览器将自动打开 http://127.0.0.1:5001
start "" http://127.0.0.1:5001
.venv\Scripts\python.exe app.py

pause
