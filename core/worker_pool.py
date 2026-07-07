from core.worker import Worker


class WorkerPool:

    def __init__(self, workers: int = 4):

        self.workers = [

            Worker()

            for _ in range(workers)

        ]

    # ==========================================
    # Obtener un Worker libre
    # ==========================================

    def available(self):

        for worker in self.workers:

            if worker.available():

                return worker

        return None

    # ==========================================
    # Workers ocupados
    # ==========================================

    def busy(self):

        return [

            worker

            for worker in self.workers

            if worker.busy

        ]

    # ==========================================
    # Workers libres
    # ==========================================

    def free(self):

        return [

            worker

            for worker in self.workers

            if not worker.busy

        ]

    # ==========================================
    # Cantidad total
    # ==========================================

    def count(self):

        return len(self.workers)

    # ==========================================
    # Cantidad ocupados
    # ==========================================

    def busy_count(self):

        return len(self.busy())

    # ==========================================
    # Cantidad libres
    # ==========================================

    def free_count(self):

        return len(self.free())

    # ==========================================
    # Información completa
    # ==========================================

    def info(self):

        return [

            worker.info()

            for worker in self.workers

        ]


pool = WorkerPool()