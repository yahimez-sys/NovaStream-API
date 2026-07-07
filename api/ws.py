from fastapi import APIRouter
from fastapi import WebSocket
from fastapi import WebSocketDisconnect

import asyncio

from core.websocket_manager import ws_manager
from utils.logger import logger

router = APIRouter()


# ==========================================================
# WebSocket
# ==========================================================

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    logger.info("Nueva conexión WebSocket.")

    # Registrar Event Loop (solo la primera vez)

    if ws_manager.loop is None:

        ws_manager.set_loop(
            asyncio.get_running_loop()
        )

    await ws_manager.connect(websocket)

    try:

        while True:

            # Mantener viva la conexión

            await websocket.receive_text()

    except WebSocketDisconnect:

        logger.info("WebSocket desconectado.")

        ws_manager.disconnect(websocket)

    except Exception as e:

        logger.error(
            f"WebSocket Error: {str(e)}"
        )

        ws_manager.disconnect(websocket)