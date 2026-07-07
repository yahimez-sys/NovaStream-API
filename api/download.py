from fastapi import APIRouter
from pydantic import BaseModel

import uuid

from core.manager import manager
from core.scheduler import scheduler
from core.queue import queue
from core.task import Task

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