@echo off
REM Uso: upload_arduino.bat [compile|upload|all] caminho_do_sketch portaCOM

IF "%~1"=="" (
    echo Uso: %~nx0 [compile^|upload^|all] caminho_do_sketch portaCOM
    exit /b 1
)
IF "%~2"=="" (
    echo Uso: %~nx0 [compile^|upload^|all] caminho_do_sketch portaCOM
    exit /b 1
)
IF "%~3"=="" (
    echo Uso: %~nx0 [compile^|upload^|all] caminho_do_sketch portaCOM
    exit /b 1
)

set ACTION=%~1
set SKETCH_PATH=%~2
set COM_PORT=%~3
set BOARD=arduino:avr:uno

REM Pasta de build (criada se não existir)
set BUILD_DIR=%~dp0build



echo Acao: %ACTION%
echo Sketch: %SKETCH_PATH%
echo Porta: %COM_PORT%

IF /I "%ACTION%"=="compile" (
    echo Compilando apenas...
    arduino-cli compile --fqbn %BOARD% %SKETCH_PATH%  --build-path %BUILD_DIR%
    goto :EOF
)

IF /I "%ACTION%"=="upload" (
    echo Gravando apenas...
    arduino-cli upload %SKETCH_PATH% -p %COM_PORT% --fqbn %BOARD%
    goto :EOF
)

IF /I "%ACTION%"=="all" (
    echo Compilando e gravando...
    arduino-cli compile --fqbn %BOARD% --port %COM_PORT% --upload %SKETCH_PATH%  --build-path %BUILD_DIR% --verify --verbose
    goto :EOF
)

echo Acao invalida: %ACTION%
echo Use: compile, upload ou all
exit /b 1