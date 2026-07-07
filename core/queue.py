import threading

from core.database import database
from core.task import Task, TaskStatus, TaskPriority


class TaskQueue:

    def __init__(self):

        self.tasks = []

        self.lock = threading.Lock()

    # ==========================================
    # Agregar tarea
    # ==========================================

    def add(self, task: Task):

        with self.lock:

            self.tasks.append(task)

            self._sort()

            self._update_positions()

        database.save_task(task)

    # ==========================================
    # Obtener siguiente tarea
    # ==========================================

    def next(self):

        with self.lock:

            for task in self.tasks:

                if task.status == TaskStatus.QUEUED:

                    task.status = TaskStatus.WAITING

                    database.save_task(task)

                    return task

        return None

    # ==========================================
    # Eliminar tarea
    # ==========================================

    def remove(self, task_id: str):

        with self.lock:

            self.tasks = [

                task

                for task in self.tasks

                if task.id != task_id

            ]

            self._update_positions()

        database.delete_task(task_id)

    # ==========================================
    # Buscar tarea
    # ==========================================

    def get(self, task_id: str):

        for task in self.tasks:

            if task.id == task_id:

                return task

        return None

    # ==========================================
    # Todas
    # ==========================================

    def all(self):

        return self.tasks

    # ==========================================
    # Pendientes
    # ==========================================

    def pending(self):

        return [

            task

            for task in self.tasks

            if task.status in (

                TaskStatus.QUEUED,

                TaskStatus.WAITING

            )

        ]

    # ==========================================
    # Ordenar
    # ==========================================

    def _sort(self):

        priority_order = {

            TaskPriority.HIGH: 0,

            TaskPriority.NORMAL: 1,

            TaskPriority.LOW: 2

        }

        self.tasks.sort(

            key=lambda task: (

                priority_order[task.priority],

                task.created_at

            )

        )

    # ==========================================
    # Actualizar posiciones
    # ==========================================

    def _update_positions(self):

        for index, task in enumerate(

            self.tasks,

            start=1

        ):

            task.queue_position = index

            database.save_task(task)

    # ==========================================
    # Cantidad
    # ==========================================

    def count(self):

        return len(self.tasks)

    # ==========================================
    # Limpiar
    # ==========================================

    def clear(self):

        with self.lock:

            self.tasks.clear()


queue = TaskQueue()