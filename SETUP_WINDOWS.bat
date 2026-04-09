@echo off
REM Script de instalación automática para Modelo 2.0 en Windows

setlocal enabledelayedexpansion

echo.
echo ========================================
echo  MODELO 2.0 - Instalación Automática
echo  Sistema de Energía Comunitaria
echo ========================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: Python no está instalado o no está en PATH
    echo.
    echo Por favor descarga Python 3.9+ desde: https://www.python.org/
    echo Asegúrate de marcar "Add Python to PATH" durante la instalación
    pause
    exit /b 1
)

echo ✓ Python detectado
python --version

REM Crear entorno virtual
echo.
echo [1/4] Creando entorno virtual...
if exist venv (
    echo   Entorno virtual ya existe, saltando...
) else (
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: No se pudo crear entorno virtual
        pause
        exit /b 1
    )
    echo ✓ Entorno virtual creado
)

REM Activar entorno virtual
echo.
echo [2/4] Activando entorno virtual...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: No se pudo activar entorno virtual
    pause
    exit /b 1
)
echo ✓ Entorno virtual activado

REM Instalar dependencias
echo.
echo [3/4] Instalando dependencias...
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: No se pudieron instalar las dependencias
    pause
    exit /b 1
)
echo ✓ Dependencias instaladas

REM Crear directorios
echo.
echo [4/4] Creando directorios necesarios...
if not exist "data\uploads" mkdir "data\uploads"
if not exist "data\templates" mkdir "data\templates"
if not exist "outputs" mkdir "outputs"
echo ✓ Directorios creados

REM Completado
echo.
echo ========================================
echo  ✅ INSTALACIÓN COMPLETADA
echo ========================================
echo.
echo Para iniciar la aplicación, ejecuta:
echo.
echo    streamlit run streamlit_app.py
echo.
echo Luego abre en tu navegador:
echo    http://localhost:8501
echo.
echo.
pause
