from threading import Lock

from core.manager import manager
from utils.logger import logger


class DownloadController:

    def __init__(self):

        self.lock = Lock()

        self.active = {}

    # ==========================================
    # Registrar descarga
    # ==========================================

    def register(self, job_id, task):

        with self.lock:

            self.active[job_id] = task

            logger.info(

                f"Download registrada | Job={job_id}"

            )

    # ==========================================
    # Obtener Task activa
    # ==========================================

    def get(self, job_id):

        return self.active.get(job_id)

    # ==========================================
    # Eliminar descarga
    # ==========================================

    def unregister(self, job_id):

        with self.lock:

            if job_id in self.active:

                del self.active[job_id]

                logger.info(

                    f"Download eliminada | Job={job_id}"

                )

    # ==========================================
    # Pausar
    # ==========================================

    def pause(self, job_id):

        job = manager.get(job_id)

        if job:

            job.pause()

            logger.info(

                f"Download pausada | Job={job_id}"

            )

            return True

        return False

    # ==========================================
    # Reanudar
    # ==========================================

    def resume(self, job_id):

        job = manager.get(job_id)

        if job:

            job.resume()

            logger.info(

                f"Download reanudada | Job={job_id}"

            )

            return True

        return False

    # ==========================================
    # Cancelar
    # ==========================================

    def cancel(self, job_id):

        job = manager.get(job_id)

        if job:

            job.cancel()

            logger.info(

                f"Download cancelada | Job={job_id}"

            )

            return True

        return False

    # ==========================================
    # Cantidad activas
    # ==========================================

    def count(self):

        return len(self.active)

    # ==========================================
    # Todas
    # ==========================================

    def all(self):

        return self.active


controller = DownloadController()