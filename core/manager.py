import threading
import uuid

from core.job import Job
from core.database import database


class JobManager:

    def __init__(self):

        self.jobs = {}

        self.lock = threading.Lock()

    # =======================================
    # Crear un Job
    # =======================================

    def create_job(self, url: str, quality: str = "best"):

        job = Job(

            id=str(uuid.uuid4()),

            url=url,

            quality=quality

        )

        with self.lock:

            self.jobs[job.id] = job

        # Guardar en SQLite

        database.save_job(job)

        return job

    # =======================================

    def get(self, job_id: str):

        return self.jobs.get(job_id)

    # =======================================

    def exists(self, job_id: str):

        return job_id in self.jobs

    # =======================================

    def remove(self, job_id: str):

        with self.lock:

            if job_id in self.jobs:

                del self.jobs[job_id]

        database.delete_job(job_id)

    # =======================================

    def clear(self):

        with self.lock:

            self.jobs.clear()

    # =======================================

    def list(self):

        return [

            job.to_dict()

            for job in self.jobs.values()

        ]

    # =======================================

    def count(self):

        return len(self.jobs)

    # =======================================

    def update_progress(

        self,

        job_id,

        progress,

        downloaded,

        total,

        speed,

        eta

    ):

        job = self.get(job_id)

        if job:

            job.update_progress(

                progress,

                downloaded,

                total,

                speed,

                eta

            )

            database.save_job(job)

    # =======================================

    def pause(self, job_id):

        job = self.get(job_id)

        if job:

            job.pause()

            database.save_job(job)

    # =======================================

    def resume(self, job_id):

        job = self.get(job_id)

        if job:

            job.resume()

            database.save_job(job)

    # =======================================

    def cancel(self, job_id):

        job = self.get(job_id)

        if job:

            job.cancel()

            database.save_job(job)

    # =======================================

    def complete(self, job_id):

        job = self.get(job_id)

        if job:

            job.complete()

            database.save_job(job)

    # =======================================

    def fail(self, job_id, message):

        job = self.get(job_id)

        if job:

            job.fail(message)

            database.save_job(job)


manager = JobManager()