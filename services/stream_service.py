from services.yt_service import YTService


class StreamService:

    @staticmethod
    def _is_video(f: dict) -> bool:
        return f.get("vcodec") and f.get("vcodec") != "none"

    @staticmethod
    def _is_audio(f: dict) -> bool:
        return f.get("acodec") and f.get("acodec") != "none"

    @staticmethod
    def _get_quality(f: dict) -> int:
        return f.get("height") or 0

    @staticmethod
    def get_streams(url: str):

        data = YTService.analyze(url)

        if isinstance(data, dict) and data.get("error"):
            return {
                "success": False,
                "video": [],
                "audio": [],
                "message": data["message"]
            }

        formats = [
            f for f in data.get("formats", [])
            if f.get("url") or f.get("manifest_url")
        ]

        video_streams = []
        audio_streams = []

        seen = set()

        for f in formats:

            url_f = f.get("url") or f.get("manifest_url")
            if not url_f:
                continue

            vcodec = f.get("vcodec")
            acodec = f.get("acodec")
            ext = f.get("ext")
            format_id = f.get("format_id")
            protocol = f.get("protocol")

            key = (format_id, protocol, vcodec, acodec)

            # 🔥 evita duplicados reales sin destruir calidades
            if key in seen:
                continue
            seen.add(key)

            video = StreamService._is_video(f)
            audio = StreamService._is_audio(f)

            quality = StreamService._get_quality(f)
            abr = f.get("abr") or f.get("tbr") or 0

            item = {
                "format_id": format_id,
                "ext": ext,
                "url": url_f,
                "protocol": protocol,
                "filesize": f.get("filesize") or f.get("filesize_approx"),
            }

            # 🎥 VIDEO STREAMS (TODOS los que tengan video codec)
            if video:
                item.update({
                    "quality": quality,
                    "fps": f.get("fps"),
                    "vcodec": vcodec,
                    "acodec": acodec,
                    "tbr": f.get("tbr") or 0,
                    "type": "video"
                })
                video_streams.append(item)

            # 🔊 AUDIO STREAMS (TODOS los que tengan audio codec)
            if audio:
                item.update({
                    "abr": abr,
                    "acodec": acodec,
                    "asr": f.get("asr"),
                    "audio_channels": f.get("audio_channels"),
                    "type": "audio"
                })
                audio_streams.append(item)

        # 📊 orden correcto tipo YouTube
        video_streams.sort(
            key=lambda x: (x["quality"], x.get("fps") or 0, x.get("tbr") or 0),
            reverse=True
        )

        audio_streams.sort(
            key=lambda x: (x.get("abr") or 0, x.get("tbr") or 0),
            reverse=True
        )

        return {
            "success": True,
            "video": video_streams,
            "audio": audio_streams
        }