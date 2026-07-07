"""
=========================================================
NovaStream API
Video Mapper PRO (Streaming Edition)
=========================================================
"""

from typing import Any, Dict, List


class VideoMapper:

    @staticmethod
    def _get_resolution_height(f):
        """Extrae altura del video para ordenar"""
        return f.get("height") or 0

    @staticmethod
    def map(video: Dict[str, Any]) -> Dict[str, Any]:

        formats = video.get("formats", [])

        video_streams = []
        audio_streams = []

        # =========================
        # SEPARAR FORMATS
        # =========================
        for f in formats:

            vcodec = f.get("vcodec")
            acodec = f.get("acodec")

            # VIDEO
            if vcodec != "none" and f.get("height"):

                video_streams.append({
                    "format_id": f.get("format_id"),
                    "ext": f.get("ext"),
                    "quality": f.get("height"),
                    "url": f.get("url"),
                    "fps": f.get("fps"),
                    "filesize": f.get("filesize"),
                    "type": "video"
                })

            # AUDIO
            if acodec != "none" and vcodec == "none":

                audio_streams.append({
                    "format_id": f.get("format_id"),
                    "ext": f.get("ext"),
                    "abr": f.get("abr"),
                    "url": f.get("url"),
                    "filesize": f.get("filesize"),
                    "type": "audio"
                })

        # =========================
        # ORDENAR VIDEO (720 → 4K)
        # =========================
        video_streams = sorted(
            video_streams,
            key=lambda x: x.get("quality", 0),
            reverse=True
        )

        # =========================
        # ORDENAR AUDIO (mejor primero)
        # =========================
        audio_streams = sorted(
            audio_streams,
            key=lambda x: x.get("abr") or 0,
            reverse=True
        )

        # =========================
        # LIMPIEZA DE DESCRIPCIÓN
        # =========================
        description = video.get("description") or ""
        description = description[:300]  # evitar payload gigante

        return {

            "id": video.get("id"),
            "title": video.get("title"),
            "description": description,

            "duration": video.get("duration"),
            "uploader": video.get("uploader"),

            "thumbnail": video.get("thumbnail"),
            "views": video.get("view_count"),
            "upload_date": video.get("upload_date"),

            # STREAMING PRO
            "video_streams": video_streams,
            "audio_streams": audio_streams
        }