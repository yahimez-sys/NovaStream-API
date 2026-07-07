from core.database import database
from core.manager import manager
from core.queue import queue
from core.job import Job
from core.task import Task, TaskStatus, TaskPriority
from core.enums import JobStatus

from datetime import datetime


class RecoveryManager:

    # ==========================================
    # Recuperar Jobs
    # ==========================================

    def load_jobs(self):

        rows = database.jobs()

        for row in rows:

            if row["status"] in (

                JobStatus.COMPLETED.value,

                JobStatus.FAILED.value,

                JobStatus.CANCELLED.value

            ):

                continue

            job = Job(

                id=row["id"],

                url=row["url"],

                title=row["title"],

                quality=row["quality"]

            )

            job.status = JobStatus(row["status"])

            job.progress = row["progress"]

            job.file = row["file"]

            try:

                job.created_at = datetime.fromisoformat(

                    row["created_at"]

                )

            except:

                pass

            manager.jobs[job.id] = job

    # ==========================================
    # Recuperar Queue
    # ==========================================

    def load_tasks(self):

        rows = database.tasks()

        for row in rows:

            if row["status"] in (

                TaskStatus.COMPLETED.value,

                TaskStatus.FAILED.value,

                TaskStatus.CANCELLED.value

            ):

                continue

            task = Task(

                id=row["id"],

                job_id=row["job_id"],

                priority=TaskPriority(

                    row["priority"]

                )

            )

            task.status = TaskStatus.QUEUED

            task.queue_position = row["queue_position"]

            task.worker_id = row["worker_id"]

            try:

                task.created_at = datetime.fromisoformat(

                    row["created_at"]

                )

            except:

                pass

            queue.tasks.append(task)

        queue._sort()

        queue._update_positions()

    # ==========================================
    # Recuperar todo
    # ==========================================

    def recover(self):

        self.load_jobs()

        self.load_tasks()


recovery = RecoveryManager()