@echo off
setlocal

REM TO DO BEFORE LAUNCHING THE SCRIPT
    REM 1. Set the main Python script name
set "main_name=guitar_tab_writer"
    REM 2. Set the icon name
set "icon_name=GuitarTabWriter"
    REM 3.Set the exe name (or comment in case the .exe file name is the GrandParent folder name)
set "exe_name=Guitar Tab Writer"
    REM 4. Choose the with(out) builder command (line ~40-45)


REM -----


REM PREPARATION
    REM Handle french characters
chcp 65001 > nul

    REM Be sure to execute from the batch file's directory, even in administrator mode
pushd "%~dp0"
cd



REM BUILD THE EXE FILE
    REM Copy Python files from 40_SRC to the current directory (50_BUILD)
copy ..\40_SRC\*.py .\

    REM Install the EXE builder (PyInstaller)
pip install pyinstaller

    REM Add the location of PyInstaller to the path
for /f "tokens=2*" %%i in ('pip show pyinstaller ^| findstr "Location"') do set PATH=%PATH%;%%i;%%i\..\Scripts

    REM Delete the (eventually) previous exe file
del *.exe

    REM Build the pyinstaller command
        REM => WITH terminal
REM set "pyinstaller_command=pyinstaller --onefile --icon=..\..\..\_Icons\%icon_name%.ico %main_name%.py"
        REM => WithOUT terminal
set "pyinstaller_command=pyinstaller --onefile --windowed --noconsole --icon=..\..\..\_Icons\%icon_name%.ico %main_name%.py"

    REM Execute the pyinstaller command
%pyinstaller_command%

PAUSE

    REM Move the resulting exe file in this directory
move .\dist\*.exe .\

    REM Delete now unused files/directories
del *.spec
rd /S /Q .\build
rd /S /Q .\dist


echo .
echo .   === Exécutable créé et déplacé dans ce répertoire. ===
echo .


REM POST-OPERATIONS
    REM Move the Python files into the .\SRC directory
rd /S /Q .\SRC
mkdir .\SRC
move .\*.py .\SRC\

    REM Rename the main.exe file as the parent folder
setlocal enabledelayedexpansion

    REM Get the grandparent folder name (in case there is no .exe name defined)
IF NOT DEFINED exe_name (
    for %%I in ("%~dp0..") do set "exe_name=%%~nxI"
)

@echo on
REM setlocal enabledelayedexpansion

    REM Rename the main.exe file
ren "%~dp0%main_name%.exe" "%exe_name%.exe"

endlocal

popd
PAUSE
