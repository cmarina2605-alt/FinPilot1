@echo off
echo INSTALLING FINPILOT AI...
python -m venv venv
call venv\Scripts\activate
pip install --upgrade pip
pip install --force-reinstall -r requirements.txt

echo.
echo DONE! NOW RUN start.bat
cmd /k
