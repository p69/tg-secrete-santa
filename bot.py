from dotenv import load_dotenv
load_dotenv()
import os
from telegram.ext import Updater, CommandHandler, Filters
import random

TOKEN = os.getenv('TELEGRAM_TOKEN')
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Dictionary to store user data
user_data = {}

# Command to start registration
def register(update, context):
    user_id = update.message.from_user.id
    user_info = ' '.join(context.args)
    if ':' not in user_info:
        update.message.reply_text("Please use ':' to separate your name and address.")
        return
    user_data[user_id] = user_info
    update.message.reply_text("You're registered! Wait for your Secret Santa match.")
    
# Command to start Secret Santa
def secret_santa(update, context):
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
        context.bot.send_message(giver_id, f"Your Secret Santa match: {user_data[receiver_id]}")

    update.message.reply_text("Secret Santa matches have been sent!")

# Adding handlers
dispatcher.add_handler(CommandHandler('register', register, Filters.chat_type.groups))
dispatcher.add_handler(CommandHandler('secretsanta', secret_santa, Filters.chat_type.groups))

# Start the bot
updater.start_polling()
