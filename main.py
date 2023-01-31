import telebot
import os
import datetime

API_KEY = os.environ.get('API_KEY')
bot = telebot.TeleBot(API_KEY)
ADMIN_ID = os.environ.get('ADMIN_ID')


def save_user_id(chat_id):
    with open("users.txt", "a") as f:
        f.write(str(chat_id) + "\n")


@bot.message_handler(commands=['users'])
def count_users(message):
    if message.from_user.id == int(ADMIN_ID):
        with open("users.txt", "r") as f:
            user_ids = [line.strip() for line in f.readlines()]
            response = f'Number of Users: {len(user_ids)}'
            bot.send_message(chat_id=message.chat.id, text=response)


@bot.message_handler(content_types=['text', 'video', 'voice', 'photo', 'sticker'])
def respond(message):
    username = message.from_user.username
    user_first_name = message.from_user.first_name
    user_chat_id = message.from_user.id
    current_time = datetime.datetime.now().strftime("%Y-%m-%d")

    if message.forward_from:
        user_first_name = message.forward_from.first_name
        user_chat_id = message.forward_from.id
        response = f'ID: {user_chat_id}\n'
        response += f'First: {user_first_name}\n'
        response += f'Time: {current_time}\n'
        response += f'username: {username}\n'
    else:
        response = f'ID: {user_chat_id}\n'
        response += f'First: {user_first_name}\n'
        response += f'Time: {current_time}\n'
        response += f'username: {username}\n'

        with open("users.txt", "r") as f:
            user_ids = [line.strip() for line in f.readlines()]
            if str(user_chat_id) not in user_ids:
                save_user_id(user_chat_id)

    bot.send_message(chat_id=message.chat.id, text=response)


if __name__ == '__main__':
    bot.polling()
