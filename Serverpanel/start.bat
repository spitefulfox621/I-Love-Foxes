@echo off
goto main

:main
    echo [SPITEFOX-BOOTSTRAP] Starting...
    call :selfcest
    call :activate_venv
    call :start_serverpanel
    goto end

:selfcest
    echo [SPITEFOX-BOOTSTRAP] running self-test
    call :venv_check
    goto :eof

:venv_check
    IF EXIST ".venv" (
        echo [SPITEFOX-BOOTSTRAP] .venv found
        ) ELSE (
            echo [SPITEFOX-BOOTSTRAP] .venv not found.
            call :create_venv
            )
    goto :eof

:create_venv
    echo [SPITEFOX-BOOTSTRAP] creating venv
    python -m venv .venv
    echo [SPITEFOX-BOOTSTRAP] activating venv
    call :activate_venv
    echo [SPITEFOX-BOOTSTRAP] updating pip
    python -m pip install --upgrade pip
    echo [SPITEFOX-BOOTSTRAP] installing dependencies
    pip install -r requirements.txt
    echo [SPITEFOX-BOOTSTRAP] venv fully set up
    goto :eof

:activate_venv
    call .venv\Scripts\activate.bat
    goto :eof

:start_serverpanel
    cls
    TITLE Serverpanel.py
    python Serverpanel.py
    goto :eof

:end
    echo [SPITEFOX-BOOTSTRAP] reached the end of the script
    timeout /t 5 /nobreak