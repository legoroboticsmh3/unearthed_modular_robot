@echo off
:: Simple Git Helper Script for Kids with File Selection, Git Pull, and Git Log

:menu
echo ==============================
echo   Git Helper Script
echo ==============================
echo 1) Commit changes
echo 2) Pull latest changes from remote
echo 3) Show last 25 commits (one line)
echo 4) Exit
echo ==============================
set /p choice="Choose an option: "

if "%choice%"=="1" goto commit
if "%choice%"=="2" goto pull
if "%choice%"=="3" goto log
if "%choice%"=="4" exit /b
goto menu

:commit
echo.
echo Checking for changes...
echo ==============================
git status --short
echo ==============================

:: Check if there are any changes
for /f %%i in ('git status --porcelain') do (
    set changes=1
)
if not defined changes (
    echo No changes to commit.
    goto menu
)

echo.
set /p name="Enter your name: "
set /p msg="Enter a short message: "

echo.
echo Now select which files to include in the commit:

:: Loop over all changed/untracked files
for /f "tokens=1,* delims= " %%a in ('git status --short') do (
    set file=%%b
    call :askFile "%%b"
)

:: If no files staged, exit early
git diff --cached --quiet
if %errorlevel%==0 (
    echo.
    echo No files selected. Nothing to commit.
    goto menu
)

:: Get current date and time
for /f "tokens=1-3 delims=/ " %%a in ("%date%") do (
    set curdate=%%a-%%b-%%c
)
for /f "tokens=1-2 delims=:." %%a in ("%time%") do (
    set curtime=%%a:%%b
)

:: Build commit message
set commitmsg=[%curdate% %curtime%] %name% - %msg%

echo.
echo Committing with message: %commitmsg%
git commit -m "%commitmsg%"

echo.
echo Pushing changes...
git push

echo.
echo Commit complete!
goto menu

:pull
echo.
echo Pulling latest changes from remote...
git pull
echo.
echo Pull complete!
goto menu

:log
echo.
echo Showing last 25 commits (one line):
git log -25 --oneline
echo.
goto menu

:askFile
setlocal
set fname=%~1
set /p include="Include %fname% in commit? (Y/N): "
if /i "%include%"=="Y" (
    git add "%fname%"
    echo Added %fname%
) else (
    echo Skipped %fname%
)
endlocal
goto :eof

