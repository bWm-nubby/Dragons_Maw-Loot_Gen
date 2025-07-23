@echo off
setlocal ENABLEDELAYEDEXPANSION

:: ========================================================
::  Advanced Dungeons & Dragons 2nd Edition Loot Generator
:: ========================================================

:: --- Configuration ---
set "PORTABLE_PYTHON_DIR=.\python\python-3.12.10-embed-amd64"
set "VENV_DIR=.\venv"
set "SCRIPT_TO_RUN=app.py"
set "REQUIREMENTS_FILE=requirements.txt"
:: ---------------------

set "PORTABLE_PYTHON_EXE=!PORTABLE_PYTHON_DIR!\python.exe"
set "PORTABLE_PIP_EXE=!PORTABLE_PYTHON_DIR!\Scripts\pip.exe"
set "PORTABLE_GET_PIP_SCRIPT=!PORTABLE_PYTHON_DIR!\get-pip.py"
set "VENV_ACTIVATE_SCRIPT=!VENV_DIR!\Scripts\activate.bat"

cls
echo ===========================================
echo          Approaching the chest...
echo ===========================================
echo.

if exist "!PORTABLE_PYTHON_EXE!" (
    if not exist "!PORTABLE_PIP_EXE!" (
        echo The lock is simple, gathering my tools.
        if not exist "!PORTABLE_GET_PIP_SCRIPT!" (
            echo I can't find my lockpicks! I must have left them behind.
            echo.
            echo "!PORTABLE_GET_PIP_SCRIPT!" is missing or broken.
            echo Recommend redownloading the app from github.com.
            pause
            exit /b 1
        )
        "!PORTABLE_PYTHON_EXE!" "!PORTABLE_GET_PIP_SCRIPT!"
        if ERRORLEVEL 1 (
            echo My tools are broken! I can't get this chest open.
            echo.
            echo "!PORTABLE_GET_PIP_SCRIPT!" is missing or broken.
            echo Recommend checking your internet connection or redownloading the app from github.com.
            echo "!ERRORLEVEL!"
            pause
            exit /b 1
        )
    echo Attempting to pick the lock...
    "!PORTABLE_PYTHON_EXE!" -m pip install -r "!REQUIREMENTS_FILE!" --no-warn-script-location"
    if ERRORLEVEL 1 (
        echo I've triggered a trap! The tumblers have reset.
        echo.
        echo "!REQUIREMENTS_FILE!" unable to be installed.
        echo Recommend checking your internet connection and trying again.
        pause
        exit /b 1
        )
    )
    echo The tumblers are set. The lock is ready to be opened.
    echo.
    echo Turning the lock...
    set "PYTHONPATH=!CD!"
    "!PORTABLE_PYTHON_EXE!" "!SCRIPT_TO_RUN!"
    pause

) else (
    echo The lock is complex, I'll need to gather my tools.
    if not exist "!VENV_DIR!" (
        echo Discovered a trap. Attempting to disarm it...
        python -m venv venv
        if ERRORLEVEL 1 (
            echo I've triggered a trap!
            echo.
            echo Ensure Python-3.12.10 is installed and added to system PATH or download portable version of the app from github.com.
            pause
            exit /b 1

        ) else (
            call "!VENV_ACTIVATE_SCRIPT!"
            echo The trap has been disarmed. Now to pick the lock.
            python -m pip install -r "!REQUIREMENTS_FILE!" --no-warn-script
            if ERRORLEVEL 1 (
                echo I've triggered a trap!
                echo.
                echo "!REQUIREMENTS_FILE!" unable to be installed.
                echo Recommend checking your internet connection and trying again.
                pause
                exit /b 1
                )
        )

    ) else (
    call "!VENV_ACTIVATE_SCRIPT!"
    echo Attempting to pick the lock...
    if ERRORLEVEL 1 (
        echo I've triggered a trap!
        echo.
        echo "!VENV_ACTIVATE_SCRIPT!" unsuccessful.
        echo Recommend deleting the "!VENV_DIR!" try again.
        pause
        exit /b 1
        )
    )
    echo =========================================================
    echo   The tumblers are set. The lock is ready to be opened.
    echo.
    echo                    Turning the lock...
    echo =========================================================
    python "!SCRIPT_TO_RUN!"
    pause
)
