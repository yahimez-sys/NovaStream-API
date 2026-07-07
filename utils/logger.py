"""
=========================================================
NovaStream API
Archivo: utils/logger.py

Descripción:
Sistema de registros (logs) del proyecto.
=========================================================
"""

import logging
from logging.handlers import RotatingFileHandler

from utils.config import LOGS_DIR

# ==========================================================
# Archivo de log
# ==========================================================

LOG_FILE = LOGS_DIR / "novastream.log"

# ==========================================================
# Logger principal
# ==========================================================

logger = logging.getLogger("NovaStream")

if not logger.handlers:

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(

        "[%(asctime)s] %(levelname)s | %(filename)s:%(lineno)d | %(message)s",

        "%Y-%m-%d %H:%M:%S"

    )

    # ======================================================
    # Archivo de logs
    # ======================================================

    file_handler = RotatingFileHandler(

        LOG_FILE,

        maxBytes=5 * 1024 * 1024,

        backupCount=5,

        encoding="utf-8"

    )

    file_handler.setFormatter(formatter)

    # ======================================================
    # Consola
    # ======================================================

    console_handler = logging.StreamHandler()

    console_handler.setFormatter(formatter)

    # ======================================================
    # Agregar handlers
    # ======================================================

    logger.addHandler(file_handler)

    logger.addHandler(console_handler)

# ==========================================================
# Funciones auxiliares
# ==========================================================

def debug(message: str):

    logger.debug(message)


def info(message: str):

    logger.info(message)


def warning(message: str):

    logger.warning(message)


def error(message: str):

    logger.error(message)


def critical(message: str):

    logger.critical(message)