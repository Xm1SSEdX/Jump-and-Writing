@echo off
setlocal
cd /d "%~dp0"

echo === Artiixs Bounce: building Windows EXE ===
py -m pip install --upgrade pip
if errorlevel 1 goto error
py -m pip install -r requirements.txt
if errorlevel 1 goto error

py -m PyInstaller --noconfirm --clean --onefile --windowed --name ArtiixsBounce win_main.py
if errorlevel 1 goto error

echo.
echo Build complete: dist\ArtiixsBounce.exe
pause
exit /b 0

:error
echo.
echo Build failed. Check the error above.
pause
exit /b 1
