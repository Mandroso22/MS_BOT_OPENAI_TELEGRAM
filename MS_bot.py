import os
import logging
import asyncio
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, filters, ContextTypes, Application
from dotenv import load_dotenv
from agents import Agent
from openai import OpenAI


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

agent = Agent(name="Assistant", instructions="You are a helpful assistant")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salut, je suis le bot de l'agence MS ! Que puis-je faire pour toi ?")

async def ia_agent(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = update.message.text
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system","content": "Tu es un assistant professionnel, concis, qui répond uniquement à la demande, sans bavardage."},
            {"role": "user", "content": question}
        ]
    )
    await update.message.reply_text(response.choices[0].message.content)

def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ia_agent))
    application.run_polling()

if __name__ == '__main__':
    main()