import random
from telegram.ext import Application, CommandHandler, ContextTypes, filters
from telegram import Update
import os
from dotenv import load_dotenv
load_dotenv()

# Dictionary to store user data
user_data = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello! I am your Secret Santa bot.')


async def register(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    user_info = ' '.join(context.args)
    if ':' not in user_info:
        update.message.reply_text(
            "Please use ':' to separate your name and address.")
        return
    user_data[user_id] = user_info
    update.message.reply_text(
        "You're registered! Wait for your Secret Santa match.")


async def secret_santa(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    user_ids = list(user_data.keys())

    # Check if all members are registered
    if len(user_data) < len(context.bot.get_chat_members_count(chat_id) - 1):
        update.message.reply_text("Not all group members are registered yet.")
        return

    # Ensuring no one gets their own name
    while True:
        random.shuffle(user_ids)
        if all(user_id != user_ids[(i + 1) % len(user_ids)] for i, user_id in enumerate(user_ids)):
            break

    # Send Secret Santa matches in a private message
    for i in range(len(user_ids)):
        giver_id = user_ids[i]
        receiver_id = user_ids[(i + 1) % len(user_ids)]
        context.bot.send_message(
            giver_id, f"Your Secret Santa match: {user_data[receiver_id]}")

    update.message.reply_text("Secret Santa matches have been sent!")

if __name__ == '__main__':
    application = Application.builder().token(os.getenv('TELEGRAM_TOKEN')).build()

    application.add_handler(CommandHandler(
        'start', start, filters.ChatType.GROUP))
    application.add_handler(CommandHandler(
        'register', register, filters.ChatType.GROUP))
    application.add_handler(CommandHandler(
        'secretsanta', secret_santa, filters.ChatType.GROUP))

    application.run_polling()
