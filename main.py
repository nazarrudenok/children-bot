import telebot
import json
import random
from config import TOKEN, connection, cursor

bot = telebot.TeleBot(TOKEN)

def rewriteTable() -> None:
    cursor.execute("TRUNCATE TABLE users")
    connection.commit()
    with open('jsons/children.json', 'r', encoding='utf-8') as f:
        children = json.load(f)
        for c in children['child']:
            cursor.execute("INSERT INTO users (name, presence, status) VALUES (%s, %s, %s)", (children['child'][c], 'п', '-'))
            connection.commit()

@bot.message_handler(commands=['start'])
def start(message: str) -> None:
    cht = message.chat.id

    username = message.from_user.username
    if username == None:
        username = message.from_user.first_name

    cursor.execute("SELECT * FROM chats WHERE username = %s", (username))
    allUsers = cursor.fetchall()

    if len(allUsers) == 0:
        cursor.execute("INSERT INTO chats (username, _id) VALUES (%s, %s)", (username, cht))
        connection.commit()
        bot.send_message(cht, cht)
        bot.send_message(cht, 'Привіт 👋\nЩодня Ви будете отримувати інформацію про чергових 😉')
    else:
        bot.send_message(cht, 'Ой! 🫢\nСхоже, Ви вже є у списку користувачів\nРеєстрація не потрібна 😉')

@bot.message_handler(commands=['appoint'])
def appoint(message: str) -> None:
    cht = message.chat.id

    if cht != 1001173176:
        bot.send_message(cht, 'Халепа! 🫢\nСхоже, ти не маєш достатньо повноважень, щоб застосувати цю команду 🤭')
    else:
        cursor.execute("SELECT * FROM users")
        allUsers = cursor.fetchall()
        if len(allUsers) < 2:
            rewriteTable()
            bot.send_message(cht, 'Список перезаписано успішно!  /appoint')
        else:
            cursor.execute("SELECT name FROM ready WHERE status = '-'")
            allReady = cursor.fetchall()
            if len(allReady) > 2:
                randomNamesR = random.sample(allReady, 2)
                first = randomNamesR[0][0]
                second = randomNamesR[1][0]

                cursor.execute("UPDATE ready SET status = '+' WHERE name = %s", (first))
                cursor.execute("UPDATE ready SET status = '+' WHERE name = %s", (second))
                connection.commit()

                cursor.execute("SELECT _id FROM chats")
                ChatIds = cursor.fetchall()
                for c in range(len(ChatIds)):
                    chatid = int(ChatIds[c][0])
                    bot.send_message(chatid, f'{first}\n{second}')
            else:
                cursor.execute("SELECT name FROM users WHERE presence = 'п'")
                allNames = cursor.fetchall()
                if len(allNames) < 2:
                    rewriteTable()
                    bot.send_message(cht, 'Список перезаписано успішно!  /appoint')
                else:
                    randomNames = random.sample(allNames, 2)

                    first = randomNames[0][0]
                    second = randomNames[1][0]

                    cursor.execute("INSERT INTO ready (name, status) VALUES (%s, %s)", (first, '+'))
                    cursor.execute("INSERT INTO ready (name, status) VALUES (%s, %s)", (second, '+'))

                    cursor.execute("DELETE FROM users WHERE name = %s OR name = %s", (first, second))
                    connection.commit()

                    cursor.execute("SELECT _id FROM chats")
                    ChatIds = cursor.fetchall()
                    for c in range(len(ChatIds)):
                        chatid = int(ChatIds[c][0])
                        bot.send_message(chatid, f'{first}\n{second}\nfrom main')

@bot.message_handler(commands=['presence'])
def presence(message: str) -> None:
    cht = message.chat.id

    if cht != 1001173176:
        bot.send_message(cht, 'Халепа! 🫢\nСхоже, ти не маєш достатньо повноважень, щоб застосувати цю команду 🤭')
    else:
        msg = bot.send_message(cht, 'Напиши відсутніх у форматі:\n<b><i>Прізвище Ім\'я</i></b>\n<b><i>Прізвище Ім\'я</i></b>\n<b><i>Прізвище Ім\'я</i></b>', parse_mode='HTML')
        bot.register_next_step_handler(msg, getMissing)

@bot.message_handler(commands=['change_status'])
def changeStatus(message: str) -> None:
    cht = message.chat.id

    if cht != 1001173176:
        bot.send_message(cht, 'Халепа! 🫢\nСхоже, ти не маєш достатньо повноважень, щоб застосувати цю команду 🤭')
    else:
        msg = bot.send_message(cht, 'Напиши халявщиків у форматі:\n<b><i>Прізвище Ім\'я</i></b>\n<b><i>Прізвище Ім\'я</i></b>\n<b><i>Прізвище Ім\'я</i></b>', parse_mode='HTML')
        bot.register_next_step_handler(msg, changeStatusFunc)

def getMissing(message: str) -> None:
    cht = message.chat.id
    text = message.text

    text = text.split('\n')
    for t in range(len(text)):
        user = text[t]
        
        cursor.execute("UPDATE users SET presence = 'н' WHERE name = %s", (user))
        connection.commit()

    bot.send_message(cht, f'Успішно записано відсутніх')

def changeStatusFunc(message: str) -> None:
    cht = message.chat.id
    text = message.text

    text = text.split('\n')
    for t in range(len(text)):
        user = text[t]

        cursor.execute("UPDATE ready SET status = '-' WHERE name = %s", (user))
        connection.commit()
    bot.send_message(cht, f'Успішно записано халявщиків 😉')

bot.polling()