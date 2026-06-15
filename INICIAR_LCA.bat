@echo off
chcp 65001 >nul
title LCA Social 2.1
cd /d "%~dp0"
echo ==================================================
echo    LCA Social 2.1  -  Iniciando aplicacion...
echo ==================================================
echo.
echo  Se abrira automaticamente en tu navegador.
echo  NO cierres esta ventana mientras uses la app.
echo  Para detener: cierra esta ventana o pulsa Ctrl+C.
echo.
python -m streamlit run streamlit_app.py --server.headless false
echo.
echo (La aplicacion se detuvo. Ya puedes cerrar esta ventana.)
pause
