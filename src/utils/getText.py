from pathlib import Path
from typing import Dict, Union
from openai import OpenAI
import asyncio
client = OpenAI()

async def getText(rawText: str) -> Union[Dict[str, str], None] :
  completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "Звідайся, якщо допоможу! Ти гід, що розповідає про культурні пам'ятки та визначні місця Одеси – міста в Україні."},
      {"role": "user", "content": f"Розповіси про {rawText}"}
    ]
  )
  text = completion.choices[0].message.content
  audio_folder = Path(__file__).parent.parent / 'audio' / f'{str}.mp3'
  if text:
    response = client.audio.speech.create(
      model="tts-1-hd",
      voice="fable",
      input= text
    )
    response.stream_to_file(audio_folder)
  else:
     return
  path = str(audio_folder)
  return {"text": text, "path": path }

async def main():
    result = await getText('Потемкинська сходини')
    print(result)

# Виклик асинхронної функції
asyncio.run(main())