from fastapi import APIRouter
from pydantic import BaseModel
import asyncio

from services.stream_service import StreamService
from utils.logger import logger

router = APIRouter()


class StreamRequest(BaseModel):
    url: str


@router.post("/stream")
async def stream(request: StreamRequest):

    logger.info(
        f"Nueva solicitud de streams | URL={request.url}"
    )

    try:

        result = await asyncio.wait_for(

            asyncio.to_thread(

                StreamService.get_streams,

                request.url

            ),

            timeout=60

        )

        logger.info(
            "Streams obtenidos correctamente."
        )

        return {

            "success": True,

            "message": "Streams obtenidos correctamente.",

            "data": result

        }

    except asyncio.TimeoutError:

        logger.error(
            "Timeout obteniendo streams."
        )

        return {

            "success": False,

            "message": "Timeout obteniendo streams."

        }

    except Exception as e:

        logger.error(
            f"Stream Error: {str(e)}"
        )

        return {

            "success": False,

            "message": str(e)

        }
    