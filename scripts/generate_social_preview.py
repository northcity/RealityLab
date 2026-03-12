"""Generate a social preview image for RealityLab using DALL-E 3."""

import os
import urllib.request
from pathlib import Path

import httpx
from openai import OpenAI

API_KEY = os.environ.get("OPENAI_API_KEY", "")
PROXY = os.environ.get("OPENAI_PROXY", "http://127.0.0.1:3213")
OUTPUT_DIR = Path(__file__).resolve().parent.parent

PROMPT = (
    "A futuristic digital laboratory floating in outer space, "
    "glowing cyan and neon-green data streams orbit around a large transparent glass sphere "
    "that contains a miniature holographic planet Earth, "
    "surrounding floating holographic charts and dashboards display anomaly scores, "
    "the whole scene uses a deep dark blue background with electric blue and emerald green accents, "
    "clean minimal sci-fi style, cinematic volumetric lighting, no text, no watermark, 4K quality"
)


def main() -> None:
    client = OpenAI(
        api_key=API_KEY,
        http_client=httpx.Client(proxy=PROXY, timeout=120.0),
    )

    print("Generating social preview image via DALL-E 3...")
    response = client.images.generate(
        model="dall-e-3",
        prompt=PROMPT,
        size="1792x1024",
        quality="hd",
        n=1,
    )

    url = response.data[0].url
    dest = OUTPUT_DIR / "social-preview.png"
    print(f"Downloading to {dest} ...")
    urllib.request.urlretrieve(url, str(dest))
    print("Done!")


if __name__ == "__main__":
    main()
