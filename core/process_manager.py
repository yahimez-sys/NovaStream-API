import subprocess
import threading

from utils.logger import logger


class ProcessManager:

    def __init__(self):

        self.processes = {}

        self.lock = threading.Lock()

    # ==========================================
    # Iniciar proceso
    # ==========================================

    def start(self, job_id: str, command: list):

        logger.info(

            f"Iniciando proceso | Job={job_id}"

        )

        process = subprocess.Popen(

            command,

            stdout=subprocess.PIPE,

            stderr=subprocess.STDOUT,

            stdin=subprocess.PIPE,

            text=True,

            universal_newlines=True,

            bufsize=1

        )

        with self.lock:

            self.processes[job_id] = process

        return process

    # ==========================================
    # Obtener proceso
    # ==========================================

    def get(self, job_id):

        return self.processes.get(job_id)

    # ==========================================
    # ¿Sigue vivo?
    # ==========================================

    def running(self, job_id):

        process = self.get(job_id)

        if process is None:

            return False

        return process.poll() is None

    # ==========================================
    # Finalizar
    # ==========================================

    def terminate(self, job_id):

        process = self.get(job_id)

        if process:

            logger.info(

                f"Terminando proceso | Job={job_id}"

            )

            process.terminate()

    # ==========================================
    # Matar
    # ==========================================

    def kill(self, job_id):

        process = self.get(job_id)

        if process:

            logger.info(

                f"Forzando cierre | Job={job_id}"

            )

            process.kill()

    # ==========================================
    # Esperar
    # ==========================================

    def wait(self, job_id):

        process = self.get(job_id)

        if process:

            return process.wait()

        return None

    # ==========================================
    # Eliminar
    # ==========================================

    def unregister(self, job_id):

        with self.lock:

            if job_id in self.processes:

                del self.processes[job_id]

    # ==========================================
    # Cantidad
    # ==========================================

    def count(self):

        return len(self.processes)


process_manager = ProcessManager()