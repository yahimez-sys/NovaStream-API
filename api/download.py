import os
import uuid

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask
from pydantic import BaseModel

from core.enums import JobStatus
from core.manager import manager
from core.scheduler import scheduler
from core.queue import queue
from core.task import Task

from utils.helpers import sanitize_filename
from utils.logger import logger


router = APIRouter()


class DownloadRequest(BaseModel):

    url: str

    quality: str = "best"


@router.post("/download")
def download(request: DownloadRequest):

    logger.info(

        f"Nueva solicitud de descarga | "
        f"Calidad={request.quality}"

    )

    # ==========================================
    # Crear Job
    # ==========================================

    job = manager.create_job(

        request.url,

        request.quality

    )

    logger.info(

        f"Job creado correctamente | "
        f"Job={job.id}"

    )

    # ==========================================
    # Crear Task
    # ==========================================

    task = Task(

        id=str(uuid.uuid4()),

        job_id=job.id,

        url=job.url,

        quality=job.quality

    )

    # ==========================================
    # Agregar a la cola
    # ==========================================

    queue.add(task)

    logger.info(

        f"Tarea agregada a la cola | "
        f"Task={task.id}"

    )

    # ==========================================
    # Iniciar Scheduler
    # ==========================================

    scheduler.start()

    logger.info(

        "Scheduler activo."

    )

    return {

        "success": True,

        "message": "Descarga agregada a la cola.",

        "job_id": job.id,

        "task_id": task.id,

        "queue_position": task.queue_position

    }


# ==========================================================
# Entregar el archivo descargado
# ==========================================================

@router.get("/download/{job_id}/file")
def download_file(job_id: str):

    job = manager.get(job_id)

    if job is None:

        raise HTTPException(

            status_code=404,

            detail="Job no encontrado."

        )

    if job.status != JobStatus.COMPLETED:

        raise HTTPException(

            status_code=409,

            detail=f"El archivo aún no está listo (estado: {job.status.value})."

        )

    if not job.file or not os.path.isfile(job.file):

        raise HTTPException(

            status_code=404,

            detail="El archivo no está disponible (pudo haber expirado o ya fue descargado)."

        )

    filename = sanitize_filename(job.title, job.id) + job.extension

    logger.info(
        f"Entregando archivo | Job={job.id} | Archivo={filename}"
    )

    def _cleanup(path: str, job_id: str):

        try:

            os.remove(path)

        except OSError:

            pass

        manager.clear_file(job_id)

    return FileResponse(

        path=job.file,

        filename=filename,

        media_type="application/octet-stream",

        background=BackgroundTask(_cleanup, job.file, job.id)

    )