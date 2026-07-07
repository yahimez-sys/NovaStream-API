# 🚀 NovaStream API

Backend de **NovaStream**, un gestor de descargas multimedia desarrollado con **FastAPI**, **yt-dlp** y **FFmpeg**.

Permite analizar videos, obtener todas las calidades disponibles, descargar contenido, monitorear el progreso en tiempo real mediante WebSocket y administrar múltiples descargas mediante un sistema de Jobs.

---

# Características

- 🎬 Análisis de videos
- 📺 Obtención de todas las resoluciones disponibles
- 🎵 Descarga de audio MP3
- 📹 Descarga de video
- ⚡ Descargas en segundo plano
- 📊 Progreso en tiempo real
- 🌐 WebSocket
- 📂 Administración de Jobs
- 📝 Sistema de Logs
- 🔄 Arquitectura modular

---

# Tecnologías

- Python 3.13
- FastAPI
- Uvicorn
- yt-dlp
- FFmpeg
- WebSockets

---

# Estructura

```
NovaStream-API/

api/
core/
downloads/
logs/
models/
services/
utils/

app.py
requirements.txt
render.yaml
README.md
```

---

# Instalación

Crear entorno virtual

```bash
python -m venv venv
```

Activarlo

Windows

```bash
venv\Scripts\activate
```

Linux

```bash
source venv/bin/activate
```

Instalar dependencias

```bash
pip install -r requirements.txt
```

Ejecutar

```bash
uvicorn app:app --reload
```

---

# Documentación

```
http://localhost:8000/docs
```

---

# WebSocket

```
ws://localhost:8000/ws
```

---

# Estado del Proyecto

Actualmente NovaStream API se encuentra en desarrollo activo.

Próximas características:

- Cola de descargas
- Pausar/Reanudar
- Cancelar descarga
- Multiusuario
- Historial
- Soporte para más plataformas
- Acelerador de descargas
- Integración completa con NovaStream Web

---

# Licencia

Proyecto desarrollado con fines educativos y de investigación.