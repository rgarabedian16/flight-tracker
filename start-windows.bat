@echo off
rem Double-click to run the flight tracker on Windows. Close this window to stop it.
cd /d "%~dp0"
where python >nul 2>nul
if errorlevel 1 (
  echo Python is not installed. Install "Python 3" from the Microsoft Store, then double-click this file again.
  start ms-windows-store://search/?query=python
  pause
  exit /b
)
start "" http://localhost:8000
python server.py
pause
