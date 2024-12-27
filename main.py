import json
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext

# Ваш токен API
TOKEN = '8025391800:AAFiU9gXVuOYTt-HYjO48fkt99kfHo649nU'

# Команда для определения ID текущего чата
async def get_chat_id(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    await update.message.reply_text(f'ID текущего чата: {chat_id}')

# Обработчик входящих сообщений
async def handle_incoming_message(update: Update, context: CallbackContext) -> None:
    try:
        # Парсинг JSON-запроса
        request_data = json.loads(update.message.text)
        method = request_data.get('method')
        url = request_data.get('url')
        headers = request_data.get('headers')
        params = request_data.get('params')

        # Выполнение запроса к локальному API
        response = requests.request(method, url, headers=headers, params=params)

        # Отправка ответа обратно через Telegram-бота
        await context.bot.send_message(chat_id=update.message.chat_id, text=response.text)
    except Exception as e:
        await context.bot.send_message(chat_id=update.message.chat_id, text=f"Ошибка: {str(e)}")

# Инициализация приложения
application = ApplicationBuilder().token(TOKEN).build()

# Регистрация команды для определения ID чата
application.add_handler(CommandHandler('get_chat_id', get_chat_id))

# Регистрация обработчика для входящих сообщений
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_incoming_message))

# Запуск бота
application.run_polling()
