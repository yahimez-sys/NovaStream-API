"""
=========================================================
NovaStream API
Archivo: utils/config.py
=========================================================
"""

from pathlib import Path
import os

from dotenv import load_dotenv

# ==========================================================
# Cargar variables de entorno
# ==========================================================

load_dotenv()

# ==========================================================
# Información API
# ==========================================================

API_NAME = os.getenv("API_NAME", "NovaStream API")

API_VERSION = os.getenv("API_VERSION", "1.0.0")

# ==========================================================
# Directorios
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

TEMP_DIR = BASE_DIR / "temp"

DOWNLOADS_DIR = BASE_DIR / "downloads"

LOGS_DIR = BASE_DIR / "logs"

TEMP_DIR.mkdir(exist_ok=True)

DOWNLOADS_DIR.mkdir(exist_ok=True)

LOGS_DIR.mkdir(exist_ok=True)

# ==========================================================
# yt-dlp
# ==========================================================

YTDLP_COMMAND = os.getenv("YTDLP_COMMAND", "yt-dlp")

# ==========================================================
# FFmpeg
# ==========================================================

FFMPEG_COMMAND = os.getenv("FFMPEG_COMMAND", "ffmpeg")

# ==========================================================
# Descargas
# ==========================================================

MAX_FILE_SIZE_MB = int(
    os.getenv("MAX_FILE_SIZE_MB", 2048)
)

MAX_DOWNLOAD_TIME = int(
    os.getenv("MAX_DOWNLOAD_TIME", 600)
)

DEFAULT_AUDIO_FORMAT = os.getenv(
    "DEFAULT_AUDIO_FORMAT",
    "mp3"
)

DEFAULT_VIDEO_FORMAT = os.getenv(
    "DEFAULT_VIDEO_FORMAT",
    "mp4"
)

# ==========================================================
# Servidor
# ==========================================================

HOST = os.getenv("HOST", "0.0.0.0")

PORT = int(os.getenv("PORT", 8000))

DEBUG = os.getenv(
    "DEBUG",
    "True"
).lower() == "true"

# ==========================================================
# Headers
# ==========================================================

DEFAULT_HEADERS = {

    "User-Agent":

    "NovaStream/1.0 (FastAPI; yt-dlp)"

}