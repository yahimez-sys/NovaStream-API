import threading


class BackgroundDownloader:

    def __init__(self):
        self.threads = {}

    def start(self, job_id, target, *args):

        thread = threading.Thread(
            target=target,
            args=args,
            daemon=True
        )

        self.threads[job_id] = thread

        thread.start()

    def get(self, job_id):

        return self.threads.get(job_id)

    def is_alive(self, job_id):

        thread = self.get(job_id)

        if thread is None:
            return False

        return thread.is_alive()


background = BackgroundDownloader()