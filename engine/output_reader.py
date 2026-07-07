"""
=========================================================
NovaStream Engine
Archivo: output_reader.py
Descripción:
Lee en tiempo real la salida de yt-dlp.
=========================================================
"""

import threading

from engine.progress_parser import ProgressParser
from utils.logger import logger


class OutputReader:

    def __init__(self, process, callback):

        self.process = process

        self.callback = callback

        self.thread = None

        self.running = False

    # ==========================================
    # Iniciar lectura
    # ==========================================

    def start(self):

        if self.running:

            return

        self.running = True

        self.thread = threading.Thread(

            target=self._reader,

            daemon=True

        )

        self.thread.start()

    # ==========================================
    # Detener lectura
    # ==========================================

    def stop(self):

        self.running = False

    # ==========================================
    # Leer stdout
    # ==========================================

    def _reader(self):

        logger.info("OutputReader iniciado.")

        try:

            while self.running:

                line = self.process.stdout.readline()

                if not line:

                    break

                parsed = ProgressParser.parse(line)

                self.callback(parsed)

        except Exception as e:

            logger.error(

                f"OutputReader: {e}"

            )

        finally:

            self.running = False

            logger.info("OutputReader finalizado.")