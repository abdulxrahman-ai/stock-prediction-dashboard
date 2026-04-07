from __future__ import annotations

import base64
import io
import os
from typing import Optional

from PIL import Image


def _to_data_url(image_bytes: bytes) -> str:
    return "data:image/png;base64," + base64.b64encode(image_bytes).decode("utf-8")


def analyze_candlestick_image(image_bytes: bytes) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return (
            "Image analysis is enabled in the interface, but no OPENAI_API_KEY was found. "
            "Set that environment variable to get AI analysis of uploaded candlestick chart screenshots. "
            "Without that key, the dashboard keeps all other features free."
        )

    from openai import OpenAI

    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    max_side = 1400
    img.thumbnail((max_side, max_side))
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")

    client = OpenAI(api_key=api_key)
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": (
                            "You are a professional market-structure assistant. Analyze candlestick chart screenshots. "
                            "Do not claim certainty or guaranteed returns. Respond in concise professional prose with: "
                            "1) trend, 2) momentum, 3) support/resistance if visible, 4) risk note, 5) a cautious buy/hold/sell leaning."
                        ),
                    }
                ],
            },
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "Analyze this candlestick chart screenshot."},
                    {"type": "input_image", "image_url": _to_data_url(buffer.getvalue())},
                ],
            },
        ],
        temperature=0.2,
    )
    return response.output_text.strip()
