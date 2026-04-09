# Guía de Instalación - Modelo 2.0

## 🖥️ Opción 1: Instalación Local (Desarrollo)

### Requisitos Previos
- Python 3.9+
- pip
- virtualenv (recomendado)

### Pasos

```bash
# 1. Clonar el repositorio
git clone <URL-REPO>
cd modelo-2-0-energia

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Ejecutar aplicación
streamlit run streamlit_app.py
```

**Acceso**: http://localhost:8501

---

## 🚀 Opción 2: Instalación en Servidor Linux (Producción)

### Requisitos Previos
- Ubuntu 20.04+ o similar
- Python 3.9+
- Nginx
- systemd

### Pasos Detallados

#### 1. Preparar el Servidor

```bash
# Actualizar sistema
sudo apt-get update
sudo apt-get upgrade -y

# Instalar Python y herramientas
sudo apt-get install -y python3.11 python3.11-venv python3-pip
sudo apt-get install -y nginx certbot python3-certbot-nginx
sudo apt-get install -y git
```

#### 2. Clonar y Configurar Proyecto

```bash
# Crear usuario para la aplicación
sudo useradd -m -s /bin/bash streamlit_user

# Clonar repositorio
cd /opt
sudo git clone <URL-REPO> modelo-2-0
sudo chown -R streamlit_user:streamlit_user modelo-2-0
cd modelo-2-0

# Crear entorno virtual
python3.11 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
deactivate
```

#### 3. Configurar Systemd

Crear archivo `/etc/systemd/system/streamlit-modelo-2-0.service`:

```ini
[Unit]
Description=Streamlit Modelo 2.0
After=network.target

[Service]
Type=simple
User=streamlit_user
WorkingDirectory=/opt/modelo-2-0
ExecStart=/opt/modelo-2-0/venv/bin/streamlit run streamlit_app.py \
  --server.port=8501 \
  --server.headless=true \
  --server.runOnSave=false

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Habilitar servicio:

```bash
sudo systemctl daemon-reload
sudo systemctl enable streamlit-modelo-2-0
sudo systemctl start streamlit-modelo-2-0
sudo systemctl status streamlit-modelo-2-0
```

#### 4. Configurar Nginx (Reverse Proxy)

Crear archivo `/etc/nginx/sites-available/modelo-2-0`:

```nginx
server {
    listen 80;
    server_name tu-dominio.com www.tu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # Para archivos estáticos si los hay
    location /_stcore/static/ {
        proxy_pass http://127.0.0.1:8501/_stcore/static/;
    }
}
```

Habilitar sitio:

```bash
sudo ln -s /etc/nginx/sites-available/modelo-2-0 /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 5. Configurar HTTPS (SSL)

```bash
# Obtener certificado Let's Encrypt
sudo certbot certonly --nginx -d tu-dominio.com -d www.tu-dominio.com

# Renovar archivo Nginx con SSL
sudo certbot --nginx -d tu-dominio.com -d www.tu-dominio.com

# Configuración automática de renovación
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

#### 6. Firewall

```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### Verificación

```bash
# Ver logs
sudo journalctl -u streamlit-modelo-2-0 -f

# Ver estado de servicios
sudo systemctl status nginx
sudo systemctl status streamlit-modelo-2-0

# Probar acceso
curl https://tu-dominio.com
```

---

## 🐳 Opción 3: Docker (Recomendado)

### Crear Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app.py", \
     "--server.port=8501", \
     "--server.headless=true"]
```

### Crear docker-compose.yml

```yaml
version: '3.8'

services:
  streamlit:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./data:/app/data
      - ./outputs:/app/outputs
    environment:
      - PYTHONUNBUFFERED=1
    restart: unless-stopped
```

### Ejecutar

```bash
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener
docker-compose down
```

**Acceso**: http://localhost:8501

---

## 🌐 Opción 4: Streamlit Cloud (Gratuito)

1. **Crear cuenta**: https://streamlit.io/cloud
2. **Conectar GitHub**: Autorizar Streamlit
3. **Deploy**:
   - New app → Select repository → Select main file
4. **Configurar secretos** (si aplica)
5. **Public URL** asignada automáticamente

---

## 📋 Checklist Post-Instalación

- [ ] Aplicación carga sin errores
- [ ] Archivos Excel se cargan correctamente
- [ ] Dashboard muestra datos
- [ ] Micro-redes se calculan
- [ ] Exportación funciona
- [ ] Certificado SSL válido (producción)
- [ ] Backups configurados

## 🔧 Mantenimiento

### Actualizar Aplicación

```bash
cd /opt/modelo-2-0
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart streamlit-modelo-2-0
```

### Backup de Datos

```bash
# Crear backup automático
crontab -e
# Agregar línea:
0 2 * * * tar -czf /backup/modelo-2-0-$(date +\%Y\%m\%d).tar.gz /opt/modelo-2-0/data/
```

### Monitoreo

```bash
# Ver uso de recursos
watch -n 1 'ps aux | grep streamlit'

# Ver logs de errores
sudo journalctl -u streamlit-modelo-2-0 -n 100 --no-pager
```

---

## ⚠️ Troubleshooting

### Problema: Conexión rechazada

```bash
# Verificar si servicio está corriendo
sudo systemctl status streamlit-modelo-2-0

# Reiniciar
sudo systemctl restart streamlit-modelo-2-0

# Ver logs
sudo journalctl -u streamlit-modelo-2-0 -f
```

### Problema: Nginx 502 Bad Gateway

```bash
# Verificar Nginx
sudo nginx -t

# Ver logs de Nginx
sudo tail -f /var/log/nginx/error.log
```

### Problema: Memoria insuficiente

```bash
# Ver uso
free -h

# Aumentar swap si es necesario
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

---

## 📞 Soporte

Para problemas o preguntas:
- Issues en GitHub
- Email: soporte@institucion.org
- Documentación: Ver /docs

---

**Versión**: 2.0 | **Fecha**: Abril 2024
