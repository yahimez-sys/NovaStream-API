from core.manager import manager
from core.enums import JobStatus
from core.events import events

from utils.logger import logger


class ProgressHook:

    def __init__(self, job):

        self.job = job

    def __call__(self, data):

        status = data.get("status")

        # ============================================
        # Descargando
        # ============================================

        if status == "downloading":

            downloaded = data.get("downloaded_bytes", 0)

            total = (
                data.get("total_bytes")
                or data.get("total_bytes_estimate")
                or 0
            )

            percent = (
                round(downloaded * 100 / total, 2)
                if total > 0
                else 0
            )

            speed = data.get("_speed_str", "0 KB/s")

            eta = data.get("_eta_str", "--")

            manager.update_progress(

                self.job.id,

                percent,

                downloaded,

                total,

                speed,

                eta

            )

            # Solo para depuración (no aparecerá en producción
            # porque el logger está configurado en INFO)
            logger.debug(
                f"Job={self.job.id} "
                f"{percent}% "
                f"{speed} "
                f"ETA {eta}"
            )

            # Emitimos evento para WebSocket
            events.emit(

                "download_progress",

                {
                    "job_id": self.job.id,
                    "status": "downloading",
                    "progress": percent,
                    "downloaded": downloaded,
                    "total": total,
                    "speed": speed,
                    "eta": eta
                }

            )

        # ============================================
        # Finalizó descarga (empieza merge)
        # ============================================

        elif status == "finished":

            self.job.status = JobStatus.MERGING

            logger.info(

                f"Descarga finalizada. "
                f"Iniciando FFmpeg Merge | "
                f"Job={self.job.id}"

            )

            events.emit(

                "download_merging",

                {
                    "job_id": self.job.id,
                    "status": "merging"
                }

            )

        # ============================================
        # Error
        # ============================================

        elif status == "error":

            logger.error(

                f"Error durante la descarga | "
                f"Job={self.job.id}"

            )

            self.job.fail("Error durante la descarga")

            events.emit(

                "download_error",

                {
                    "job_id": self.job.id,
                    "status": "error"
                }

            )