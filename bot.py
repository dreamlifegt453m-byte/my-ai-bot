import os
import logging
from flask import Flask
from threading import Thread
import google.generativeai as genai
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

# إعداد السيرفر الوهمي (لحل مشكلة البورتات في Render)
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is active and running!"

def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

# إعدادات الذكاء الاصطناعي وتليجرام
# تأكد أنك وضعت التوكن في Environment في موقع Render
TOKEN = os.getenv("TELEGRAM_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

async def start(update, context):
    await update.message.reply_text("مرحباً! أنا بوت ذكاء اصطناعي، اسألني أي شيء.")

async def handle_message(update, context):
    user_text = update.message.text
    try:
        response = model.generate_content(user_text)
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text("عذراً، حدث خطأ في معالجة الطلب.")

if __name__ == '__main__':
    # تشغيل السيرفر الوهمي في الخلفية
    Thread(target=run_web, daemon=True).start()
    
    # إعداد البوت
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("البوت يعمل الآن بنجاح...")
    # إضافة drop_pending_updates لحل مشكلة التعارض (Conflict)
    application.run_polling(drop_pending_updates=True)

