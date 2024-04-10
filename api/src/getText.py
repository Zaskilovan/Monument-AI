from pathlib import Path
from typing import Dict, Union 
from openai import OpenAI

import os 
from  uuid import uuid4


fastapi_key = os.getenv("FASTAPI_KEY")

client = OpenAI(api_key = fastapi_key)

async def getText(rawText: str) -> Union[Dict[str, str], None] :
    rawText = rawText.replace('-', ' ')
    raw_text_list = rawText.split()
    if raw_text_list[0] == "The":
       rawText = "Потьомкінськи сходи" 
    if raw_text_list[0] == "Opera":
       rawText = "Одеський оперний театр"
    # rawText = re.sub(r'\d+\.?\d*', '', rawText)

    completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": "Звідайся, якщо допоможу! Ти гід, що розповідає про культурні пам'ятки та визначні місця Одеси – міста в Україні."},
        {"role": "user", "content": f"Розповіси про {rawText}"}
      ]
    )
    text = completion.choices[0].message.content
    os.makedirs('audio', exist_ok=True)
    audio_folder = f'audio/{uuid4()}.mp3'
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
    return {"text": text, "audio_path": path}



# Виклик асинхронної функції
# if __name__ == "__main__":
#   async def main():
#     result = await getText('Потемкинська сходини')
#     print(result)

#   asyncio.run(main())

if __name__ == "__main__":
  text = "Opera theatre"

  if text == "Opera theatre":
      print("The text is 'Opera theatre'")
  else:
      print("The text is not 'Opera theatre'")