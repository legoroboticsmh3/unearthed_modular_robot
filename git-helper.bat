@echo off
:: Simple Git Helper Script for Kids with File Selection

:menu
echo ==============================
echo   Git Helper Script
echo ==============================
echo 1) Commit changes
echo 2) Show last 25 commits (one line)
echo 3) Exit
echo ==============================
set /p choice="Choose an option: "

if "%choice%"=="1" goto commit
if "%choice%"=="2" goto log
if "%choice%"=="3" exit
goto menu

:commit
echo.
set /p name="Enter your name: "
set /p msg="Enter a short message: "

echo.
echo Checking for changes...
echo ==============================
git status --short
echo ==============================

echo.
echo Now select which files to include in the commit:

:: Loop over all changed/untracked files
for /f "tokens=1,* delims= " %%a in ('git status --short') do (
    set status=%%a
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

:log
echo.
echo Showing last 25 commits (one line):
git log -25 --oneline
echo.
goto menu