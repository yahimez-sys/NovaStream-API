# 🚀 NovaStream API

Backend oficial de **NovaStream**, desarrollado con **FastAPI**, **yt-dlp** y **FFmpeg**.

NovaStream API permite analizar contenido multimedia, obtener información detallada de videos, recuperar todas las calidades disponibles, descargar audio y video, monitorear el progreso en tiempo real mediante **WebSockets** y administrar múltiples descargas utilizando un sistema de **Jobs**.

---

# ✨ Características

* 🎬 Análisis de videos
* 📺 Obtención de todas las resoluciones disponibles
* 🎵 Descarga de audio en MP3
* 📹 Descarga de video en múltiples calidades
* ⚡ Descargas en segundo plano
* 📊 Progreso en tiempo real
* 🌐 Comunicación mediante WebSocket
* 📂 Administración de Jobs
* 📝 Sistema de Logs
* 💾 Recuperación de descargas
* 🗄️ Persistencia mediante SQLite
* 🔄 Arquitectura modular y escalable

---

# 🛠️ Tecnologías

* Python 3
* FastAPI
* Uvicorn
* yt-dlp
* FFmpeg
* SQLite
* WebSockets

---

# 📁 Estructura del Proyecto

```text
NovaStream-API/

├── api/
├── core/
├── engine/
├── mappers/
├── models/
├── services/
├── utils/
│
├── app.py
├── requirements.txt
├── render.yaml
├── README.md
└── .gitignore
```

---

# ⚙️ Instalación

## 1. Clonar el repositorio

```bash
git clone https://github.com/TU_USUARIO/NovaStream-API.git
cd NovaStream-API
```

## 2. Crear el entorno virtual

```bash
python -m venv venv
```

## 3. Activar el entorno virtual

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

## 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

# ▶️ Ejecutar la API

```bash
uvicorn app:app --reload
```

La API estará disponible en:

```
http://localhost:8000
```

---

# 📚 Documentación

Swagger UI

```
http://localhost:8000/docs
```

ReDoc

```
http://localhost:8000/redoc
```

---

# 🔌 WebSocket

```
ws://localhost:8000/ws
```

---

# 📡 Endpoints principales

| Método | Endpoint       | Descripción                             |
| ------ | -------------- | --------------------------------------- |
| POST   | `/analyze`     | Analizar un video                       |
| POST   | `/stream`      | Obtener todas las calidades disponibles |
| POST   | `/download`    | Iniciar una descarga                    |
| GET    | `/jobs`        | Listar todas las descargas              |
| GET    | `/job/{id}`    | Obtener información de una descarga     |
| GET    | `/status/{id}` | Consultar el estado de una descarga     |
| WS     | `/ws`          | Progreso en tiempo real                 |

---

# 🌍 Despliegue

NovaStream API está preparada para ejecutarse en:

* Render
* Docker (próximamente)
* VPS Linux
* Servidores Windows

---

# 📈 Estado del Proyecto

## 🚧 Versión 1.0 Beta

La versión **1.0 Beta** incluye todas las funciones principales del backend y actualmente se encuentra en fase de estabilización.

### Funciones implementadas

* ✅ Análisis de videos
* ✅ Obtención de Streams
* ✅ Descarga de Audio
* ✅ Descarga de Video
* ✅ WebSocket en tiempo real
* ✅ Administración de Jobs
* ✅ Sistema de Logs
* ✅ SQLite
* ✅ Recuperación de Descargas
* ✅ Background Worker
* ✅ Integración con FFmpeg

### Próximas características

* ⏸️ Pausar y reanudar descargas
* ❌ Cancelación de descargas
* 🚀 Motor de descargas NovaEngine v2
* 👥 Multiusuario
* 📜 Historial de descargas
* 🔐 Sistema de autenticación
* 🌐 Integración completa con NovaStream Web
* 📦 API pública documentada

---

# 🤝 Contribuciones

Las contribuciones, sugerencias y reportes de errores son bienvenidos.

Si encuentras un problema o deseas proponer una mejora, puedes abrir un **Issue** o enviar un **Pull Request**.

---

# 📄 Licencia

Este proyecto se distribuye bajo la **Licencia MIT**.

---

# ❤️ Proyecto

NovaStream es un proyecto desarrollado con fines educativos y de investigación, enfocado en la creación de un gestor multimedia moderno, modular y escalable basado en tecnologías abiertas.
