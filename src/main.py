from chatgpt import chat
from texts import *
import logging
import geocoder
import requests
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes, InlineQueryHandler
import os
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
class telegrambot:
    def __init__(self):
        self.URL = "https://api.openweathermap.org/data/3.0/onecall?lat={}&lon={}&exclude={}&appid={}"
        self.Chat = chat()
    
    async def start(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Hi, I'm Beta version of this Bot!")
    
    async def about(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, text=about)

    async def caps(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
        text_caps = ' '.join(context.args).upper()
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

    async def image(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
        image_request = ' '.join(context.args)
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=self.Chat.generate(image_request))
        
    async def chatgpt(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
        content = self.Chat.bot(update, context)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=content)
        
    async def tts(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
        message_user = ' '.join(context.args)
        content = self.Chat.tts(message_user)
        await context.bot.send_audio(chat_id=update.effective_chat.id, audio=open(content, 'rb'))
        os.remove(content)
        
    async def weather_location(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            latitude = update.message.location.latitude
            longitude = update.message.location.longitude
            user_location_info = geocoder.osm([latitude, longitude], method='reverse')

            user_city = user_location_info.city

            user_id = update.message.from_user.id
            result = requests.get(self.URL.format(latitude, longitude, "minutely,hourly,daily", os.environ['WEATHER_API']))
            result.raise_for_status()  # Raise an exception if the request failed
            weather = result.json()
        except Exception as e:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Failed to get weather data: {e}")

        data = """
        Temperature now: {} °C, Wind speed {} m/s
        """.format(round(weather["current"]["temp"]-273,1), weather["current"]["wind_speed"])

        await context.bot.send_message(chat_id = update.effective_chat.id, text=data)
        
    async def stt(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
        # message = update.effective_message
        # if message.voice.duration > 300:
        #     context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I can't process it.")
        # else:
        #     context.bot.get_file(update.message.document.file_id).download()
        #     file_path = update.message.document.file_path
        #     transcript = self.Chat.stt(file_path)
        #     await context.bot.send_message(chat_id=update.effective_chat.id, text=transcript)
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, This function in work, stay tuned!")
        
    async def unknown(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")
        
    async def inline_caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.inline_query.query
        if not query:
            return
        results = []
        results.append(
            InlineQueryResultArticle(
                id=query.upper(),
                title='Caps',
                input_message_content=InputTextMessageContent(query.upper())
            )
        )
        await context.bot.answer_inline_query(update.inline_query.id, results)
    
    def main(self):
        application = ApplicationBuilder().token(os.environ['TOKENTG']).build()
            
        chat_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), self.chatgpt)
        application.add_handler(chat_handler)
        
        about_handler = CommandHandler('about', self.about)
        application.add_handler(about_handler)
        
        audio_handler = CommandHandler('tts', self.tts)
        application.add_handler(audio_handler)
        
        stt_handler = MessageHandler(filters.VOICE, self.stt)
        application.add_handler(stt_handler)
            
        start_handler = CommandHandler('start', self.start)
        application.add_handler(start_handler)
        
        caps_handler = CommandHandler('caps', self.caps)
        application.add_handler(caps_handler)
        
        image_handler = CommandHandler('image', self.image)
        application.add_handler(image_handler)
        
        unknown_handler = MessageHandler(filters.COMMAND, self.unknown)
        application.add_handler(unknown_handler)
        
        weather_handler = MessageHandler(filters.LOCATION, self.weather_location)
        application.add_handler(weather_handler)
            
        inline_caps_handler = InlineQueryHandler(self.inline_caps)
        application.add_handler(inline_caps_handler)
            
        application.run_polling()
