#!/bin/bash

# Script de instalación automática para Modelo 2.0 en Linux/macOS

echo ""
echo "========================================"
echo "  MODELO 2.0 - Instalación Automática"
echo "  Sistema de Energía Comunitaria"
echo "========================================"
echo ""

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 no está instalado"
    echo ""
    echo "En Ubuntu/Debian:"
    echo "  sudo apt-get install python3 python3-pip python3-venv"
    echo ""
    echo "En macOS:"
    echo "  brew install python3"
    echo ""
    exit 1
fi

echo "✓ Python detectado"
python3 --version

# Crear entorno virtual
echo ""
echo "[1/4] Creando entorno virtual..."
if [ -d "venv" ]; then
    echo "   Entorno virtual ya existe, saltando..."
else
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "ERROR: No se pudo crear entorno virtual"
        exit 1
    fi
    echo "✓ Entorno virtual creado"
fi

# Activar entorno virtual
echo ""
echo "[2/4] Activando entorno virtual..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "ERROR: No se pudo activar entorno virtual"
    exit 1
fi
echo "✓ Entorno virtual activado"

# Instalar dependencias
echo ""
echo "[3/4] Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: No se pudieron instalar las dependencias"
    exit 1
fi
echo "✓ Dependencias instaladas"

# Crear directorios
echo ""
echo "[4/4] Creando directorios necesarios..."
mkdir -p data/uploads
mkdir -p data/templates
mkdir -p outputs
echo "✓ Directorios creados"

# Hacer ejecutable el archivo de configuración
chmod +x streamlit_app.py

# Completado
echo ""
echo "========================================"
echo "  ✅ INSTALACIÓN COMPLETADA"
echo "========================================"
echo ""
echo "Para iniciar la aplicación, ejecuta:"
echo ""
echo "    source venv/bin/activate"
echo "    streamlit run streamlit_app.py"
echo ""
echo "Luego abre en tu navegador:"
echo "    http://localhost:8501"
echo ""
