"""
=========================================================
NovaStream Engine
Archivo: download_engine.py
Descripción:
Motor principal de descargas.
=========================================================
"""

import os
import uuid

from engine.command_builder import CommandBuilder
from engine.process_manager import process_manager
from engine.output_reader import OutputReader

from core.manager import manager
from core.events import events

from utils.logger import logger


class DownloadEngine:

    # =====================================================
    # Iniciar descarga
    # =====================================================

    @staticmethod
    def start(job):

        logger.info(

            f"Engine iniciado | Job={job.id}"

        )

        os.makedirs("downloads", exist_ok=True)

        filename = str(uuid.uuid4()) + ".%(ext)s"

        output = os.path.join(

            "downloads",

            filename

        )

        command = CommandBuilder.build(

            job,

            output

        )

        logger.info(

            "Comando generado:\n" +

            " ".join(command)

        )

        process = process_manager.start(

            job.id,

            command

        )

        job.start()

        reader = OutputReader(

            process,

            lambda data: DownloadEngine.handle_event(

                job,

                data

            )

        )

        reader.start()

        process.wait()

        reader.stop()

        process_manager.unregister(job.id)

        logger.info(

            f"Proceso finalizado | Job={job.id}"

        )

    # =====================================================
    # Procesar eventos
    # =====================================================

    @staticmethod
    def handle_event(job, data):

        event_type = data.get("type")

        # ----------------------------------------------

        if event_type == "progress":

            job.progress = data["progress"]

            manager.update_progress(

                job.id,

                data["progress"],

                0,

                0,

                data["speed"],

                data["eta"]

            )

            events.emit(

                "download_progress",

                {

                    "job_id": job.id,

                    **data

                }

            )

        # ----------------------------------------------

        elif event_type == "destination":

            job.file = data["file"]

        # ----------------------------------------------

        elif event_type == "merging":

            events.emit(

                "download_merging",

                {

                    "job_id": job.id

                }

            )

        # ----------------------------------------------

        elif event_type == "finished":

            job.complete()

            events.emit(

                "download_finished",

                {

                    "job_id": job.id

                }

            )

            logger.info(

                f"Descarga terminada | Job={job.id}"

            )

        # ----------------------------------------------

        elif event_type == "error":

            job.fail(

                data["message"]

            )

            events.emit(

                "download_error",

                {

                    "job_id": job.id,

                    "message": data["message"]

                }

            )

            logger.error(

                f"Error | Job={job.id} | {data['message']}"

            )


download_engine = DownloadEngine()