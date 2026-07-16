import glob
import os
import uuid
from time import perf_counter
from typing import Iterable, Tuple

import yt_dlp

from core.manager import manager
from core.progress import ProgressHook
from utils.config import YTDLP_COOKIES_FILE
from utils.logger import logger


class DownloadService:

    # =========================================
    # Clientes yt-dlp (evitar bloqueo "confirma
    # que no eres un robot" de YouTube)
    #
    # android/ios primero: no dependen del
    # challenge JS del cliente "web", que es el
    # que más activa la verificación anti-bot
    # desde IPs de datacenter (como las de Render).
    # =========================================

    CLIENT_GROUPS: Tuple[Tuple[str, ...], ...] = (
        ("android",),
        ("ios",),
        ("web",),
        ("tv",),
        ("mweb",),
    )

    # =========================================
    # Limpiar restos de un intento anterior
    # =========================================

    @staticmethod
    def _cleanup_partial(output_dir: str, file_id: str):

        pattern = os.path.join(output_dir, f"{file_id}.*")

        for f in glob.glob(pattern):

            try:

                os.remove(f)

            except OSError:

                pass

    # =========================================
    # Buscar archivo descargado
    # =========================================

    @staticmethod
    def _find_downloaded_file(output_dir: str, file_id: str):

        pattern = os.path.join(output_dir, f"{file_id}.*")

        files = [
            f for f in glob.glob(pattern)
            if not f.endswith((".part", ".ytdl", ".temp"))
        ]

        if not files:
            return None

        priority = [
            ".mp4",
            ".mkv",
            ".webm",
            ".mp3",
            ".m4a",
            ".aac",
            ".opus",
            ".wav"
        ]

        for ext in priority:

            for file in files:

                if file.lower().endswith(ext):

                    return file

        return files[0]

    # =========================================
    # Calidad
    # =========================================

    @staticmethod
    def _build_format(quality: str):

        formats = {

            "audio": "bestaudio/best",

            "360": "bestvideo[height<=360]+bestaudio/best",

            "480": "bestvideo[height<=480]+bestaudio/best",

            "720": "bestvideo[height<=720]+bestaudio/best",

            "1080": "bestvideo[height<=1080]+bestaudio/best",

            "1440": "bestvideo[height<=1440]+bestaudio/best",

            "4k": "bestvideo[height<=2160]+bestaudio/best",

            "best": "bestvideo+bestaudio/best"

        }

        return formats.get(quality, formats["best"])

    # =========================================
    # Opciones yt-dlp
    # =========================================

    @staticmethod
    def _build_options(job, output_dir, file_id, hook, player_clients: Iterable[str]):

        fmt = DownloadService._build_format(job.quality)

        ydl_opts = {

            "format": fmt,

            "outtmpl": os.path.join(
                output_dir,
                file_id + ".%(ext)s"
            ),

            "progress_hooks": [hook],

            "quiet": True,

            "no_warnings": True,

            "continuedl": True,

            "retries": 10,

            "fragment_retries": 10,

            "concurrent_fragment_downloads": 8,

            "socket_timeout": 30,

            "noplaylist": True,

            "ignoreerrors": False,

            "extractor_args": {

                "youtube": {

                    "player_client": list(player_clients),
                    "formats": ["missing_pot", "duplicate", "incomplete"]

                }

            },

        }

        if YTDLP_COOKIES_FILE and os.path.isfile(YTDLP_COOKIES_FILE):
            ydl_opts["cookiefile"] = YTDLP_COOKIES_FILE

        # Video

        if job.quality != "audio":

            ydl_opts["merge_output_format"] = "mp4"

        # Audio

        else:

            ydl_opts["postprocessors"] = [

                {

                    "key": "FFmpegExtractAudio",

                    "preferredcodec": "mp3",

                    "preferredquality": "320"

                }

            ]

        return ydl_opts

    # =========================================
    # ¿Vale la pena reintentar con otro cliente?
    #
    # El bloqueo "Sign in to confirm you're not
    # a bot" es a nivel de cuenta/cookie/IP, no
    # de cliente: cambiar de cliente no lo evita
    # y solo suma peticiones que pueden empeorar
    # que la cuenta se marque como sospechosa.
    # =========================================

    @staticmethod
    def _is_bot_check_error(error: Exception) -> bool:

        message = str(error).lower()

        return (
            "confirm you" in message
            and "not a bot" in message
        )

    # =========================================
    # Descarga con fallback de clientes
    # =========================================

    @staticmethod
    def _download_with_fallback(job, output_dir, file_id, hook):

        last_error = None

        for index, clients in enumerate(DownloadService.CLIENT_GROUPS):

            if index > 0:

                logger.warning(

                    f"Reintentando descarga con cliente "
                    f"'{'/'.join(clients)}' | Job={job.id}"

                )

                DownloadService._cleanup_partial(output_dir, file_id)

            ydl_opts = DownloadService._build_options(

                job,

                output_dir,

                file_id,

                hook,

                clients

            )

            try:

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:

                    return ydl.extract_info(

                        job.url,

                        download=True

                    )

            except Exception as e:

                last_error = e

                logger.warning(

                    f"Falló descarga con cliente "
                    f"'{'/'.join(clients)}' | "
                    f"Job={job.id} | Error={str(e)}"

                )

                if DownloadService._is_bot_check_error(e):

                    logger.warning(

                        f"Bloqueo anti-bot detectado, se detiene el "
                        f"reintento con otros clientes | Job={job.id}"

                    )

                    break

        raise last_error

    # =========================================
    # Descarga principal
    # =========================================

    @staticmethod
    def download_job(task):

        # Obtener Job desde la Task

        job = manager.get(task.job_id)

        if job is None:

            logger.error(

                f"Job no encontrado | Task={task.id}"

            )

            task.fail()

            return

        output_dir = "downloads"

        os.makedirs(output_dir, exist_ok=True)

        file_id = str(uuid.uuid4())

        hook = ProgressHook(job)

        start_time = perf_counter()

        logger.info(

            f"Iniciando descarga | "

            f"Job={job.id} | "

            f"Task={task.id}"

        )

        try:

            job.start()

            task.start()

            info = DownloadService._download_with_fallback(

                job,

                output_dir,

                file_id,

                hook

            )

            file_path = DownloadService._find_downloaded_file(

                output_dir,

                file_id

            )

            if not file_path:

                logger.error(

                    f"Archivo no encontrado | "

                    f"Job={job.id}"

                )

                manager.fail(

                    job.id,

                    "No se encontró el archivo descargado."

                )

                task.fail()

                return

            # =====================================
            # Datos finales
            # =====================================

            job.file = file_path

            job.title = info.get("title", "")

            job.thumbnail = info.get("thumbnail", "")

            job.extension = os.path.splitext(file_path)[1]

            try:

                job.filesize = os.path.getsize(file_path)

            except OSError:

                job.filesize = 0

                logger.warning(

                    f"No fue posible obtener el tamaño | "

                    f"Job={job.id}"

                )

            # =====================================
            # Completar
            # =====================================

            job.complete()

            task.complete()

            elapsed = perf_counter() - start_time

            logger.info(

                f"Descarga completada | "

                f"Job={job.id} | "

                f"Tiempo={elapsed:.2f}s"

            )

        except Exception as e:

            manager.fail(

                job.id,

                str(e)

            )

            task.fail()

            logger.error(

                f"Error descarga | "

                f"Job={job.id} | "

                f"Error={str(e)}"

            )