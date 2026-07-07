import threading
import uuid

from core.task import Task, TaskStatus


class Worker:

    def __init__(self):

        self.id = str(uuid.uuid4())

        self.task = None

        self.thread = None

        self.busy = False

    # ==========================================
    # ¿Está libre?
    # ==========================================

    def available(self):

        return not self.busy

    # ==========================================
    # Ejecutar tarea
    # ==========================================

    def run(self, target, task: Task):

        if self.busy:

            return False

        self.busy = True

        self.task = task

        task.worker_id = self.id

        task.start()

        self.thread = threading.Thread(

            target=self._execute,

            args=(target, task),

            daemon=True

        )

        self.thread.start()

        return True

    # ==========================================
    # Ejecución real
    # ==========================================

    def _execute(self, target, task):

        try:

            target(task)

            if task.status == TaskStatus.RUNNING:

                task.complete()

        except Exception:

            task.fail()

        finally:

            self.busy = False

            self.task = None

    # ==========================================
    # Información
    # ==========================================

    def info(self):

        return {

            "id": self.id,

            "busy": self.busy,

            "task": self.task.id if self.task else None

        }