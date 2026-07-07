"""
=========================================================
NovaStream API
Archivo: models/responses.py
Descripción:
Modelos de respuesta (Response Models)
=========================================================
"""

from typing import Any

from pydantic import BaseModel


class AnalyzeResponse(BaseModel):
    """
    Respuesta estándar del análisis de un video.
    """

    success: bool
    message: str
    data: Any | None = None