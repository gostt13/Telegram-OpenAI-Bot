from main import telegrambot
from dotenv import load_dotenv

load_dotenv()

if __name__ == '__main__':
    bot = telegrambot()
    bot.main()