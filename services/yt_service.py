import os
from copy import deepcopy
from typing import Any, Dict, Iterable, List, Tuple

import yt_dlp

from utils.config import YTDLP_COOKIES_FILE


class YTService:

    CLIENT_GROUPS: Tuple[Tuple[str, ...], ...] = (
        ("web",),
        ("android",),
        ("tv",),
        ("ios",),
        ("mweb",),
    )

    @staticmethod
    def _build_options(player_clients: Iterable[str]) -> Dict[str, Any]:
        opts = {
            "quiet": True,
            "no_warnings": True,
            "noplaylist": True,
            "extract_flat": False,
            "socket_timeout": 20,
            "youtube_include_dash_manifest": True,
            "extractor_args": {
                "youtube": {
                    "player_client": list(player_clients),
                    "formats": ["missing_pot", "duplicate", "incomplete"]
                }
            },
        }

        if YTDLP_COOKIES_FILE and os.path.isfile(YTDLP_COOKIES_FILE):
            opts["cookiefile"] = YTDLP_COOKIES_FILE

        return opts

    @staticmethod
    def _extract_with_clients(url: str, player_clients: Iterable[str]) -> Dict[str, Any]:
        ydl_opts = YTService._build_options(player_clients)

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(url, download=False)

    @staticmethod
    def _format_key(fmt: Dict[str, Any]) -> Tuple[Any, ...]:
        return (
            fmt.get("format_id"),
            fmt.get("protocol"),
            fmt.get("ext"),
            fmt.get("width"),
            fmt.get("height"),
            fmt.get("fps"),
            fmt.get("vcodec"),
            fmt.get("acodec"),
            fmt.get("abr"),
            fmt.get("tbr"),
            fmt.get("format_note"),
            fmt.get("language"),
            fmt.get("url") or fmt.get("manifest_url"),
        )

    @staticmethod
    def _merge_info(base_info: Dict[str, Any], incoming_info: Dict[str, Any]) -> Dict[str, Any]:
        merged = deepcopy(base_info)
        merged_formats: List[Dict[str, Any]] = []
        seen_formats = set()

        for source in (base_info.get("formats", []), incoming_info.get("formats", [])):
            for fmt in source:
                key = YTService._format_key(fmt)

                if key in seen_formats:
                    continue

                seen_formats.add(key)
                merged_formats.append(fmt)

        merged["formats"] = merged_formats

        for field in (
            "title",
            "description",
            "thumbnail",
            "duration",
            "uploader",
            "view_count",
            "upload_date",
        ):
            if not merged.get(field) and incoming_info.get(field):
                merged[field] = incoming_info.get(field)

        return merged

    @staticmethod
    def analyze(url: str):
        merged_info = None
        errors = []

        for clients in YTService.CLIENT_GROUPS:
            try:
                info = YTService._extract_with_clients(url, clients)

                if merged_info is None:
                    merged_info = info
                else:
                    merged_info = YTService._merge_info(merged_info, info)
            except Exception as e:
                errors.append(f"{'/'.join(clients)}: {str(e)}")

        if merged_info is not None:
            return merged_info

        return {
            "error": True,
            "message": errors[-1] if errors else "No se pudo analizar el video"
        }
