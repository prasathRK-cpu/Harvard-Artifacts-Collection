@echo off
title Harvard Artifacts Database Setup
color 0A

echo =====================================
echo   Launching Database Creation Script
echo =====================================
echo.

REM Change to the script’s directory
cd /d "%~dp0"
echo Current folder: %CD%

REM Get today's date in YYYY-MM-DD format
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (
    set TODAY=%%c-%%a-%%b
)

REM Check if the database file exists
if exist "harvard_db.sqlite3" (
    echo Database file exists. Creating a backup...
    set BACKUP_NAME=harvard_db_backup_%TODAY%.sqlite3
    echo Copying "harvard_db.sqlite3" to "%BACKUP_NAME%"...
    copy "harvard_db.sqlite3" "%BACKUP_NAME%"
    if %errorlevel% neq 0 (
        echo ❌ Failed to create backup. Check file name and path.
    ) else (
        echo Backup created successfully: %BACKUP_NAME%
    )
) else (
    echo No existing database found. No backup needed.
)

REM Run the Python script to create a new database
python Database_creation.py
if %errorlevel% neq 0 (
    echo Error: Python script failed!
    pause
    exit /b %errorlevel%
)

echo.
echo Database created successfully!
pause
