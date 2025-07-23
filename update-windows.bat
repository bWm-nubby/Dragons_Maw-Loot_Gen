@echo off
:: This script checks for updates from the GitHub repository and applies them.

echo Checking for updates...
echo.

:: The core git command to download and merge changes.
git pull

echo.
echo Update process complete.
echo If you see errors above, please report them as an issue on GitHub.
echo.
pause
