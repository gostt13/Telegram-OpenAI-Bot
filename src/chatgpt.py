from openai import OpenAI
from pathlib import Path
import os
from typing import Optional, Literal
from telegram import Update
from telegram.ext import ContextTypes

class chat:
    def __generator(self, token: Optional[int] = 50, message: Optional[str] = None) -> str:
        self.messages.append({"role": "user", "content": message}) if message is not None else False
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            max_tokens=token,
            temperature=0.6,
        )
        self.messages.pop() if message is not None else False
        return response.choices[0].message.content.strip()
    
    def __setup__(self) -> Literal[None]:
        self.model = "gpt-3.5-turbo"
        self.image_model = "dall-e-3"
        self.messages = [{"role": "system","content": "Don't repeat yourself, be helpful and be assistant for my chatbot"}]
        self.__generator(token=1)
        
    def __init__(self) -> Literal[None]:
        self.client = OpenAI(api_key=os.environ['TOKENOPENAI'])
        self.__setup__()
    
    def bot(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        user = update.message.from_user
        user_message = update.message.text
        message_to_user = "This user {} sent this message {}".format(update.message.from_user.username, user_message)
        response = self.__generator(256, message_to_user)
        return response
    
    def generate(self, message: str) -> str:
        response = self.client.images.generate(
            model=self.image_model,
            prompt=message,
            size="1024x1024",
            quality="standard",
            n=1,
            )
        image_url = response.data[0].url
        return image_url
    
    def tts(self, message: str) -> str:
        speech_file_path = Path(__file__).parent / "tts_from_user.mp3"
        response = self.client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=message,
        )
        response.stream_to_file(speech_file_path)
        return speech_file_path
    
    # WORK IN PROGRESS
    # def stt(self, audio_file):
    #     audio_file = str(audio_file)
    #     if ".ogg" in audio_file:
    #         audio_file = audio_file.replace(".ogg", ".mp3")
    #     response = self.client.audio.speech.create(
    #         model="whisper-1",
    #         file=open(audio_file, "rb"),
    #         response_format="text"
    #     )
    #     # transcript = response.data[0].text
    #     return response
    
        
    
