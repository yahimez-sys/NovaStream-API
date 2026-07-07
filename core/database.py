import sqlite3
from pathlib import Path
from threading import Lock

from utils.config import BASE_DIR


DB_PATH = BASE_DIR / "novastream.db"


class Database:

    def __init__(self):

        self.lock = Lock()

        self.connection = sqlite3.connect(

            DB_PATH,

            check_same_thread=False

        )

        self.connection.row_factory = sqlite3.Row

        self.create_tables()

    # ==========================================
    # Crear tablas
    # ==========================================

    def create_tables(self):

        cursor = self.connection.cursor()

        cursor.execute("""

        CREATE TABLE IF NOT EXISTS jobs(

            id TEXT PRIMARY KEY,

            url TEXT,

            title TEXT,

            quality TEXT,

            status TEXT,

            progress REAL,

            file TEXT,

            created_at TEXT

        )

        """)

        cursor.execute("""

        CREATE TABLE IF NOT EXISTS tasks(

            id TEXT PRIMARY KEY,

            job_id TEXT,

            priority TEXT,

            status TEXT,

            queue_position INTEGER,

            worker_id TEXT,

            created_at TEXT

        )

        """)

        self.connection.commit()

    # ==========================================
    # Guardar Job
    # ==========================================

    def save_job(self, job):

        with self.lock:

            self.connection.execute(

                """

                INSERT OR REPLACE INTO jobs

                VALUES(?,?,?,?,?,?,?,?)

                """,

                (

                    job.id,

                    job.url,

                    job.title,

                    job.quality,

                    job.status.value,

                    job.progress,

                    job.file,

                    job.created_at.isoformat()

                )

            )

            self.connection.commit()

    # ==========================================
    # Guardar Task
    # ==========================================

    def save_task(self, task):

        with self.lock:

            self.connection.execute(

                """

                INSERT OR REPLACE INTO tasks

                VALUES(?,?,?,?,?,?,?)

                """,

                (

                    task.id,

                    task.job_id,

                    task.priority.value,

                    task.status.value,

                    task.queue_position,

                    task.worker_id,

                    task.created_at.isoformat()

                )

            )

            self.connection.commit()

    # ==========================================
    # Eliminar Job
    # ==========================================

    def delete_job(self, job_id):

        with self.lock:

            self.connection.execute(

                "DELETE FROM jobs WHERE id=?",

                (job_id,)

            )

            self.connection.commit()

    # ==========================================
    # Eliminar Task
    # ==========================================

    def delete_task(self, task_id):

        with self.lock:

            self.connection.execute(

                "DELETE FROM tasks WHERE id=?",

                (task_id,)

            )

            self.connection.commit()

    # ==========================================
    # Obtener Jobs
    # ==========================================

    def jobs(self):

        cursor = self.connection.execute(

            "SELECT * FROM jobs"

        )

        return cursor.fetchall()

    # ==========================================
    # Obtener Tasks
    # ==========================================

    def tasks(self):

        cursor = self.connection.execute(

            "SELECT * FROM tasks"

        )

        return cursor.fetchall()

    # ==========================================
    # Cerrar BD
    # ==========================================

    def close(self):

        self.connection.close()


database = Database()