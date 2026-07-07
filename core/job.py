from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional

from core.enums import JobStatus


@dataclass
class Job:

    # ==========================
    # Identificación
    # ==========================

    id: str
    url: str

    title: str = ""

    quality: str = "best"

    file: str = ""

    thumbnail: str = ""

    # ==========================
    # Estado
    # ==========================

    status: JobStatus = JobStatus.CREATED

    error: str = ""

    # ==========================
    # Progreso
    # ==========================

    progress: float = 0.0

    downloaded: int = 0

    total_size: int = 0

    speed: str = "0 KB/s"

    eta: str = "--:--"

    # ==========================
    # Información del archivo
    # ==========================

    extension: str = ""

    filesize: int = 0

    # ==========================
    # Fechas
    # ==========================

    created_at: datetime = field(default_factory=datetime.now)

    started_at: Optional[datetime] = None

    finished_at: Optional[datetime] = None

    # ==========================
    # Métodos
    # ==========================

    def start(self):

        self.status = JobStatus.DOWNLOADING
        self.started_at = datetime.now()

    def pause(self):

        self.status = JobStatus.PAUSED

    def resume(self):

        self.status = JobStatus.DOWNLOADING

    def cancel(self):

        self.status = JobStatus.CANCELLED
        self.finished_at = datetime.now()

    def complete(self):

        self.status = JobStatus.COMPLETED
        self.progress = 100
        self.finished_at = datetime.now()

    def fail(self, message: str):

        self.status = JobStatus.FAILED
        self.error = message
        self.finished_at = datetime.now()

    def update_progress(

        self,

        progress: float,

        downloaded: int,

        total_size: int,

        speed: str,

        eta: str

    ):

        self.progress = progress

        self.downloaded = downloaded

        self.total_size = total_size

        self.speed = speed

        self.eta = eta

    def to_dict(self):

        data = asdict(self)

        data["status"] = self.status.value

        data["created_at"] = self.created_at.isoformat()

        data["started_at"] = (
            self.started_at.isoformat()
            if self.started_at
            else None
        )

        data["finished_at"] = (
            self.finished_at.isoformat()
            if self.finished_at
            else None
        )

        return data