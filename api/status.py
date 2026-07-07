from fastapi import APIRouter

from core.manager import manager
from utils.logger import logger

router = APIRouter()


# ==========================================================
# Estado de un Job
# ==========================================================

@router.get("/status/{job_id}")
def get_status(job_id: str):

    logger.info(
        f"Consulta de estado | Job={job_id}"
    )

    try:

        job = manager.get(job_id)

        if not job:

            logger.warning(
                f"Job no encontrado | Job={job_id}"
            )

            return {

                "success": False,

                "message": "Job no encontrado."

            }

        logger.info(
            f"Estado enviado | Job={job_id}"
        )

        return {

            "success": True,

            "data": job.to_dict()

        }

    except Exception as e:

        logger.error(
            f"Error obteniendo estado | Job={job_id} | Error={str(e)}"
        )

        return {

            "success": False,

            "message": str(e)

        }