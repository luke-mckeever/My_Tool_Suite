@echo off
SETLOCAL ENABLEEXTENSIONS

echo Installing required Python packages...
pip install -r requirements.txt

echo.
echo [✔] Setup complete!
echo.


ENDLOCAL
pause
