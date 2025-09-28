import os
import re
from typing import Dict


# Minimal, explicit canonical names for the challenge
# Extend here if new variants appear
PLACE_CANONICAL_MAP: Dict[str, str] = {
    # Uluru / Kata Tjuta
    "uluru-kata tjuta national park (uluru)": "Uluru-Kata Tjuta",
    "uluru": "Uluru-Kata Tjuta",
    "ayers rock": "Uluru-Kata Tjuta",
    "uluru-kata tjuṯa": "Uluru-Kata Tjuta",
    "kata tjuta": "Uluru-Kata Tjuta",

    # Kakadu
    "kakadu": "Kakadu",
    "kakadu national park": "Kakadu",

    # Nitmiluk / Katherine Gorge
    "nitmiluk": "Nitmiluk (Katherine Gorge)",
    "nitmiluk katherine gorge": "Nitmiluk (Katherine Gorge)",
    "katherine gorge": "Nitmiluk (Katherine Gorge)",

    # West MacDonnell / Ormiston
    "west macdonnell national park": "West MacDonnell National Park",
    "west macdonnell": "West MacDonnell National Park",
    "ormiston gorge": "West MacDonnell National Park",

    # Devils Marbles / Karlu Karlu
    "devils marbles": "Devils Marbles (Karlu Karlu)",
    "karlu karlu": "Devils Marbles (Karlu Karlu)",

    # Alice Springs Desert Park
    "alice springs desert park": "Alice Springs Desert Park",
}


def normalize_place(raw_name: str) -> str:
    if not isinstance(raw_name, str):
        return ""
    name = raw_name.strip()
    key = name.lower()
    # quick de-accent of tjuta/tjuṯa variants
    key = key.replace("ṯ", "t")
    return PLACE_CANONICAL_MAP.get(key, name)


_whitespace_re = re.compile(r"\s+")


def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    # normalize whitespace, strip control chars
    cleaned = text.replace("\u200b", " ").replace("\ufeff", " ")
    cleaned = _whitespace_re.sub(" ", cleaned).strip()
    return cleaned


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


