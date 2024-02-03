from openai import OpenAI as gpt
from tokens import *
import time
from pathlib import Path

class chat:
    def __generator__(self, message, token) -> str:
        response = self.client.completions.create(
            model="davinci-002",
            prompt=message,
            max_tokens=token,
            temperature=1,
            presence_penalty=0,
            frequency_penalty=0,
            top_p=1
        )
        return response.choices[0].text.strip(" ,")
    
    def __setup__(self) -> None:
        system = "As a system role don't repeat yourself, don't try to complete user's message, don't even try to complete user's message and predict it, just send a new one, be friendly, don't be rude, be a very helpful friend!"
        self.__generator__(system, 1)
        
    def __init__(self) -> None:
        self.client = gpt(api_key=TOKENOPENAI)
        self.__setup__()
    
    def bot(self, update, context) -> str:
        user = update.message.from_user
        user_message = update.message.text
        message_to_user = "This user {} sent this message {}, don't try to complete it, don't try to predict it, and don't try to put down this user".format(update.message.from_user.username, user_message)
        response = self.__generator__(message_to_user, 256)
        time.sleep(5)
        return response
    
    def generate(self, message):
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=message,
            size="1024x1024",
            quality="standard",
            n=1,
            )
        image_url = response.data[0].url
        return image_url
    
    def tts(self, message):
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
    
        
    
