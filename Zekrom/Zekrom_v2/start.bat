@echo off
goto main

:main
call :activate_venv
call :start_zekrom
goto end

:activate_venv
call .venv\Scripts\activate.bat
goto :eof

:start_zekrom
TITLE Zekrom.py
py Zekrom.py
goto :eof

:end
timeout /t 5 /nobreak
