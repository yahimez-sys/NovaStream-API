from fastapi import APIRouter
from pydantic import BaseModel
import asyncio

from services.yt_service import YTService
from utils.logger import logger

router = APIRouter()


class AnalyzeRequest(BaseModel):
    url: str


@router.post("/analyze")
async def analyze_video(request: AnalyzeRequest):

    logger.info(
        f"Nueva solicitud de análisis | URL={request.url}"
    )

    try:

        raw_data = await asyncio.wait_for(
            asyncio.to_thread(
                YTService.analyze,
                str(request.url)
            ),
            timeout=60
        )

        if isinstance(raw_data, dict) and raw_data.get("error"):

            logger.warning(
                f"Error al analizar URL | {raw_data.get('message')}"
            )

            return {
                "success": False,
                "message": raw_data["message"]
            }

        logger.info(
            "Análisis completado correctamente."
        )

        return {

            "success": True,

            "message": "Video analizado correctamente.",

            "data": raw_data

        }

    except asyncio.TimeoutError:

        logger.error(
            "Timeout durante el análisis."
        )

        return {

            "success": False,

            "message": "Timeout: YouTube tardó demasiado en responder."

        }

    except Exception as e:

        logger.error(
            f"Analyze Error: {str(e)}"
        )

        return {

            "success": False,

            "message": str(e)

        }