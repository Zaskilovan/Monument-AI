""" This module is responsible for getting the text from the user and returning the text and audio path. """

import os
from typing import Dict, Union
from uuid import uuid4

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=openai_key)


async def getText(rawText: str) -> Union[Dict[str, str], None]:
    """
    Generate text and audio based on the given raw text.

    Args:
        rawText (str): The raw text to generate information about.

    Returns:
        Union[Dict[str, str], None]: A dictionary containing the generated text and the path to the generated audio file, or None if no text is generated.
    """
    rawText = rawText.replace("-", " ")
    raw_text_list = rawText.split()
    if raw_text_list[0] == "The":
        rawText = "Потьомкінськи сходи"
    if raw_text_list[0] == "Opera":
        rawText = "Одеський оперний театр"

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Звідайся, якщо допоможу! Ти гід, що розповідає про культурні пам'ятки та визначні місця Одеси – міста в Україні.",
            },
            {"role": "user", "content": f"Розповіси про {rawText}"},
        ],
    )
    text = completion.choices[0].message.content
    os.makedirs("audio", exist_ok=True)
    audio_folder = f"audio/{uuid4()}.mp3"
    if text:
        response = client.audio.speech.create(
            model="tts-1-hd", voice="fable", input=text
        )
        response.stream_to_file(audio_folder)
    else:
        return None
    path = str(audio_folder)
    return {"text": text, "audio_path": path}
