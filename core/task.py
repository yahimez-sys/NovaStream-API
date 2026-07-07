from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class TaskPriority(str, Enum):

    LOW = "low"

    NORMAL = "normal"

    HIGH = "high"


class TaskStatus(str, Enum):

    QUEUED = "queued"

    WAITING = "waiting"

    RUNNING = "running"

    PAUSED = "paused"

    COMPLETED = "completed"

    FAILED = "failed"

    CANCELLED = "cancelled"


@dataclass
class Task:

    # =====================================
    # Identificación
    # =====================================

    id: str

    job_id: str

    url: str

    quality: str = "best"

    # =====================================
    # Prioridad
    # =====================================

    priority: TaskPriority = TaskPriority.NORMAL

    # =====================================
    # Estado
    # =====================================

    status: TaskStatus = TaskStatus.QUEUED

    # =====================================
    # Cola
    # =====================================

    queue_position: int = 0

    worker_id: str = ""

    # =====================================
    # Reintentos
    # =====================================

    retry_count: int = 0

    max_retries: int = 3

    # =====================================
    # Tiempo
    # =====================================

    created_at: datetime = field(default_factory=datetime.now)

    started_at: datetime | None = None

    finished_at: datetime | None = None

    # =====================================
    # Métodos
    # =====================================

    def start(self):

        self.status = TaskStatus.RUNNING

        self.started_at = datetime.now()

    def complete(self):

        self.status = TaskStatus.COMPLETED

        self.finished_at = datetime.now()

    def fail(self):

        self.status = TaskStatus.FAILED

        self.finished_at = datetime.now()

    def cancel(self):

        self.status = TaskStatus.CANCELLED

        self.finished_at = datetime.now()

    def pause(self):

        self.status = TaskStatus.PAUSED

    def resume(self):

        self.status = TaskStatus.RUNNING

    def can_retry(self):

        return self.retry_count < self.max_retries

    def increase_retry(self):

        self.retry_count += 1