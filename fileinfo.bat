@echo off
setlocal enabledelayedexpansion

echo Suggest a readme for the following code.A good README file should be clear, concise, and well-A good README file should be clear, concise, and well-organized. It should include a descriptive title and overview of the project, installation instructions, usage guidelines, and API documentation if applicable. Configuration details, examples, and use cases should be provided to help users understand and apply the project effectively. Contributing guidelines, testing instructions, and troubleshooting tips are essential for fostering collaboration and addressing common issues. Including the project's license, acknowledgments, references, and contact information adds value to the README. 

REM Initialize an empty list of processed files
set "processedFiles="


REM Read .gitignore file to get ignored files and directories
for /f "usebackq delims=" %%G in (".gitignore") do (
    if not "%%G"=="" (
        set "ignoredItems=!ignoredItems!%%G;"
    )
)

REM Optional second argument specifies max lines per file
set "linesToRead=%2"
if not defined linesToRead ( 
    set "linesToRead=20"
)

REM Function to recursively process files
:processFiles
echo Directory: "%~1"
for /R "%~1" %%G in (*.py) do (
    call :processFile "%%G"
)
goto :eof

:processFile
set "filePath=%~1"
set "relativePath=!filePath:%cd%\=!"
echo "!processedFiles!" | findstr /C:"!filePath!" > nul
if !errorlevel! equ 1 (
    REM Add the file path to the list of processed files
    set "processedFiles=!processedFiles!!filePath!;"

    REM Check if the file or directory is ignored
    echo "!ignoredItems!" | findstr /C:"!relativePath:\=/!" > nul
    if !errorlevel! equ 1 (
        echo File: %relativePath%
        echo.
        call :processFileContents "%filePath%"
    )
)
goto :eof


:processFileContents
set "counter=0"
for /f "delims=" %%A in ('type "%~1"') do (
    if !counter! lss !linesToRead! (
        echo %%A
        set /a counter+=1
    ) else (
        goto :eof
    )
)
goto :eof

REM Call the function to process files recursively
call :processFiles "%CD%" "%1"

REM Recursive call to process subdirectories
for /R "%CD%" %%D in (.) do (
    if exist "%%D\" (
        REM Recursive call to process files in subdirectory
        call :processFiles "%%D"
    )
)
