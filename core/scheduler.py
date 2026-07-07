import threading
import time

from core.queue import queue
from core.worker_pool import pool
from services.download_service import DownloadService


class Scheduler:

    def __init__(self):

        self.running = False

        self.thread = None

    # ==========================================
    # Iniciar Scheduler
    # ==========================================

    def start(self):

        if self.running:

            return

        self.running = True

        self.thread = threading.Thread(

            target=self._loop,

            daemon=True

        )

        self.thread.start()

    # ==========================================
    # Detener Scheduler
    # ==========================================

    def stop(self):

        self.running = False

    # ==========================================
    # Loop principal
    # ==========================================

    def _loop(self):

        while self.running:

            worker = pool.available()

            if worker is not None:

                task = queue.next()

                if task is not None:

                    worker.run(

                        DownloadService.download_job,

                        task

                    )

            time.sleep(0.2)


scheduler = Scheduler()