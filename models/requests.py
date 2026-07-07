"""
=========================================================
NovaStream API
Archivo: models/requests.py
Descripción:
Modelos de entrada (Request Models)
=========================================================
"""

from pydantic import BaseModel, HttpUrl


class AnalyzeRequest(BaseModel):
    """
    Modelo para analizar un video.
    """

    url: HttpUrl