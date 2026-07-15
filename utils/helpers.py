"""
=========================================================
NovaStream API
Archivo: utils/helpers.py
=========================================================
"""

import re


def sanitize_filename(name: str, fallback: str = "download") -> str:

    name = (name or "").strip()

    if not name:

        name = fallback

    name = re.sub(r'[\\/:*?"<>|]', "_", name)

    name = name.strip(" .")

    return name[:150] or fallback
