from fastapi import APIRouter

from core.manager import manager
from utils.logger import logger

router = APIRouter()


# ==========================================================
# Obtener todos los Jobs
# ==========================================================

@router.get("/jobs")
def get_jobs():

    logger.info("Solicitud de lista de Jobs.")

    try:

        jobs = []

        for job in manager.jobs.values():

            jobs.append({

                "id": job.id,
                "title": job.title,
                "status": job.status,
                "progress": round(job.progress, 2),
                "speed": job.speed,
                "eta": job.eta,
                "quality": job.quality,
                "url": job.url

            })

        logger.info(

            f"Se devolvieron {len(jobs)} Jobs."

        )

        return {

            "success": True,

            "total": len(jobs),

            "jobs": jobs

        }

    except Exception as e:

        logger.error(

            f"Error obteniendo Jobs: {str(e)}"

        )

        return {

            "success": False,

            "message": str(e)

        }


# ==========================================================
# Obtener un Job
# ==========================================================

@router.get("/job/{job_id}")
def get_job(job_id: str):

    logger.info(

        f"Consulta Job={job_id}"

    )

    try:

        job = manager.get(job_id)

        if job is None:

            logger.warning(

                f"Job inexistente: {job_id}"

            )

            return {

                "success": False,

                "message": "Job no encontrado."

            }

        return {

            "success": True,

            "job": {

                "id": job.id,
                "title": job.title,
                "status": job.status,
                "progress": round(job.progress, 2),
                "speed": job.speed,
                "eta": job.eta,
                "quality": job.quality,
                "url": job.url,
                "file": job.file

            }

        }

    except Exception as e:

        logger.error(

            f"Error Job={job_id}: {str(e)}"

        )

        return {

            "success": False,

            "message": str(e)

        }