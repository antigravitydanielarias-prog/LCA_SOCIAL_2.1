FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY . .

# Crear directorios necesarios
RUN mkdir -p data/uploads data/templates outputs

# Exponer puerto
EXPOSE 8501

# Configuración de Streamlit
RUN mkdir -p ~/.streamlit && \
    echo "[server]\n\
port = 8501\n\
headless = true\n\
runOnSave = false\n\
enableXsrfProtection = true\n\
\n\
[logger]\n\
level = \"info\"\n\
\n\
[client]\n\
showErrorDetails = true" > ~/.streamlit/config.toml

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Comando por defecto
CMD ["streamlit", "run", "streamlit_app.py", \
     "--server.port=8501", \
     "--server.headless=true"]
