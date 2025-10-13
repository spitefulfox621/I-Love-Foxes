@echo OFF
echo hello world
echo %CD%
pause
cd ..\
echo %CD%
pause
Reshiram-VENV\Scripts\activate
echo %CD%
pause
py Reshiram\Reshiram.py
deactivate
pause