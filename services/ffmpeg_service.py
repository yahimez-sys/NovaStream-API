"""
=========================================================
NovaStream API
Archivo: ffmpeg_service.py
Descripción:
Utilidades para FFmpeg.
=========================================================
"""

import subprocess

from utils.logger import logger


class FFmpegService:

    @staticmethod
    def check():

        try:

            result = subprocess.run(

                ["ffmpeg", "-version"],

                capture_output=True,

                text=True

            )

            return result.returncode == 0

        except Exception:

            return False

    # ==========================================

    @staticmethod
    def version():

        try:

            result = subprocess.run(

                ["ffmpeg", "-version"],

                capture_output=True,

                text=True

            )

            return result.stdout.splitlines()[0]

        except Exception:

            return "FFmpeg no encontrado"

    # ==========================================

    @staticmethod
    def duration(file_path):

        try:

            result = subprocess.run(

                [

                    "ffprobe",

                    "-v", "error",

                    "-show_entries",

                    "format=duration",

                    "-of",

                    "default=noprint_wrappers=1:nokey=1",

                    file_path

                ],

                capture_output=True,

                text=True

            )

            return float(result.stdout.strip())

        except Exception as e:

            logger.error(

                f"No fue posible obtener duración: {e}"

            )

            return 0