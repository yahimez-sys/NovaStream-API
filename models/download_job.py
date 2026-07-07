from dataclasses import dataclass


@dataclass
class DownloadJob:

    id: str

    url: str

    title: str = ""

    status: str = "waiting"

    progress: float = 0

    speed: str = ""

    eta: str = ""

    downloaded: int = 0

    total: int = 0

    filename: str = ""

    quality: str = ""

    type: str = "video"

    error: str = ""