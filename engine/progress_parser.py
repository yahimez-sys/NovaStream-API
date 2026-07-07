"""
=========================================================
NovaStream Engine
Archivo: progress_parser.py
Descripción:
Convierte la salida de yt-dlp en datos estructurados.
=========================================================
"""

import re


class ProgressParser:

    # ==========================================
    # Expresiones regulares
    # ==========================================

    PROGRESS_RE = re.compile(

        r"\[download\]\s+(\d+(?:\.\d+)?)%\s+of\s+(.+?)\s+at\s+(.+?)\s+ETA\s+(.+)"

    )

    DESTINATION_RE = re.compile(

        r"\[download\]\s+Destination:\s+(.+)"

    )

    MERGING_RE = re.compile(

        r"\[Merger\]"

    )

    FINISHED_RE = re.compile(

        r"100%"

    )

    ERROR_RE = re.compile(

        r"ERROR:(.*)"

    )

    # ==========================================
    # Parsear línea
    # ==========================================

    @classmethod
    def parse(cls, line: str):

        line = line.strip()

        # --------------------------------------

        # Progreso

        # --------------------------------------

        match = cls.PROGRESS_RE.search(line)

        if match:

            return {

                "type": "progress",

                "progress": float(match.group(1)),

                "size": match.group(2),

                "speed": match.group(3),

                "eta": match.group(4)

            }

        # --------------------------------------

        # Archivo destino

        # --------------------------------------

        match = cls.DESTINATION_RE.search(line)

        if match:

            return {

                "type": "destination",

                "file": match.group(1)

            }

        # --------------------------------------

        # Merge

        # --------------------------------------

        if cls.MERGING_RE.search(line):

            return {

                "type": "merging"

            }

        # --------------------------------------

        # Error

        # --------------------------------------

        match = cls.ERROR_RE.search(line)

        if match:

            return {

                "type": "error",

                "message": match.group(1).strip()

            }

        # --------------------------------------

        # Finalizado

        # --------------------------------------

        if cls.FINISHED_RE.search(line):

            return {

                "type": "finished"

            }

        # --------------------------------------

        # Nada reconocido

        # --------------------------------------

        return {

            "type": "unknown",

            "raw": line

        }