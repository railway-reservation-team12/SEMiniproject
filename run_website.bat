@echo off
setlocal
title Velocity Luxury Rail - Web Server
cd /d "%~dp0"
echo ============================================================================
echo   VELOCITY LUXURY RAILWAY RESERVATION SYSTEM
echo   Team 12 - PES University - Software Engineering Mini-Project
echo ============================================================================
echo.

:: Reuse this project's server, but do not mistake any listener on port 8000 for it.
powershell -NoProfile -Command "try { $r = Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/trains' -TimeoutSec 2; if ($r.success) { exit 0 }; exit 1 } catch { exit 1 }"
if not errorlevel 1 goto already_running

powershell -NoProfile -Command "$c = New-Object Net.Sockets.TcpClient; try { $c.Connect('127.0.0.1', 8000); exit 0 } catch { exit 1 } finally { $c.Dispose() }"
if not errorlevel 1 goto port_in_use

where python >nul 2>&1
if not errorlevel 1 goto launch_with_python
if exist "%LocalAppData%\Programs\Python\Python312\python.exe" goto launch_with_installed_python
where py >nul 2>&1
if not errorlevel 1 goto launch_with_py

echo Python 3 was not found. Install Python or add it to PATH, then run this file again.
pause
exit /b 1

:launch_with_py
call :open_browser_when_ready
py -3 "%~dp0web\server.py"
set "SERVER_EXIT=%ERRORLEVEL%"
goto server_stopped

:launch_with_python
call :open_browser_when_ready
python "%~dp0web\server.py"
set "SERVER_EXIT=%ERRORLEVEL%"
goto server_stopped

:launch_with_installed_python
call :open_browser_when_ready
"%LocalAppData%\Programs\Python\Python312\python.exe" "%~dp0web\server.py"
set "SERVER_EXIT=%ERRORLEVEL%"
goto server_stopped

:open_browser_when_ready
echo Starting local server at http://localhost:8000...
echo Using the project's own folder for its data and web files.
echo Keep this window open while using the site. Press Ctrl+C to stop.
echo.
start "" powershell.exe -NoProfile -WindowStyle Hidden -Command "$until = (Get-Date).AddSeconds(30); while ((Get-Date) -lt $until) { try { $r = Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/trains' -TimeoutSec 1; if ($r.success) { Start-Process 'http://localhost:8000'; exit } } catch {}; Start-Sleep -Milliseconds 300 }"
exit /b

:server_stopped
echo.
echo The website server has stopped.
pause
exit /b %SERVER_EXIT%

:already_running
echo This project's server is already running. Opening the website.
start "" http://localhost:8000
endlocal
exit /b 0

:port_in_use
echo Port 8000 is occupied by another application, not this website.
echo Close that application or its server, then double-click this file again.
pause
exit /b 1
