@echo off
set SCRIPT_DIR=%~dp0
set LOG_FILE=%SCRIPT_DIR%weekly-reports\run.log

echo === HALOS Market Intelligence Agent === >> "%LOG_FILE%"
echo Started: %DATE% %TIME% >> "%LOG_FILE%"

"C:\Users\richard_lee\AppData\Local\Programs\Python\Python313\python.exe" "%SCRIPT_DIR%market_intel_agent.py" >> "%LOG_FILE%" 2>&1

echo Finished: %DATE% %TIME% >> "%LOG_FILE%"
echo. >> "%LOG_FILE%"
