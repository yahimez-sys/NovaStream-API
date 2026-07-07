from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from api.analyze import router as analyze_router
from api.stream import router as stream_router
from api.download import router as download_router
from api.jobs import router as jobs_router
from api.status import router as status_router
from api.ws import router as ws_router

from core.recovery import recovery
from core.scheduler import scheduler

from utils.logger import logger

# ==========================================================
# Inicialización de NovaStream
# ==========================================================

@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("=" * 60)
    logger.info("Iniciando NovaStream API...")
    logger.info("=" * 60)

    try:

        # Recuperar Jobs y Tasks pendientes

        recovery.recover()

        logger.info("Recovery completado correctamente.")

    except Exception as e:

        logger.error(f"Error durante Recovery: {e}")

    try:

        # Iniciar Scheduler

        scheduler.start()

        logger.info("Scheduler iniciado correctamente.")

    except Exception as e:

        logger.error(f"Error iniciando Scheduler: {e}")

    yield

    logger.info("=" * 60)
    logger.info("NovaStream detenido.")
    logger.info("=" * 60)


# ==========================================================
# NovaStream API
# ==========================================================

app = FastAPI(

    title="NovaStream API",

    description="API para análisis y descarga de videos utilizando yt-dlp y FFmpeg.",

    version="1.0.0",

    docs_url="/docs",

    redoc_url="/redoc",

    lifespan=lifespan

)

# ==========================================================
# Ruta principal
# ==========================================================

@app.get("/", tags=["General"])
async def home():

    return {

        "success": True,

        "application": "NovaStream API",

        "version": "1.0.0",

        "status": "online",

        "documentation": "/docs"

    }


# ==========================================================
# Estado del servidor
# ==========================================================

@app.get("/status", tags=["General"])
async def status():

    return JSONResponse(

        status_code=200,

        content={

            "success": True,

            "server": "online",

            "api": "NovaStream",

            "version": "1.0.0"

        }

    )


# ==========================================================
# Routers
# ==========================================================

app.include_router(analyze_router)

app.include_router(stream_router)

app.include_router(download_router)

app.include_router(jobs_router)

app.include_router(status_router)

app.include_router(ws_router)