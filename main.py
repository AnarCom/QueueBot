from DbConnection import DbConn
from migrations import execute_migrations
import telebot
from telebot import types
import os
from entities import User, Queue

bot = telebot.TeleBot(os.environ['TELEGRAM_TOKEN'])
if __name__ == '__main__':
    DbConn()
    results = DbConn().cursor.fetchall()
    print(results)
    execute_migrations(DbConn().cursor)


def get_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    return markup.add(
        types.KeyboardButton("/user_info"),
        types.KeyboardButton("/change_name"),
        types.KeyboardButton("Занять место в очереди"),
        types.KeyboardButton("Посмотреть очередь"),
        # types.KeyboardButton("Сдвинуть очередь на 1"),
        types.KeyboardButton("Я ответил!"),
        types.KeyboardButton("Выйти из очереди")
    )


@bot.message_handler(commands=['start'])
def start_command(message):
    chat_id = message.chat.id
    if User.select(User.id == chat_id).exists():
        bot.send_message(
            message.chat.id,
            "Регистрация пройдена, обратного пути нема"
        )
    else:
        bot.send_message(chat_id,
                         "_Irtegov os bot_\n" +
                         "Ваш лучший помошник в деле сдачи лаб по осям :)",
                         parse_mode="markdown"
                         )
        msg = bot.send_message(message.chat.id,
                               "_registration_\n" +
                               "Напиши свое имя и ~в отличае от моего автора \(кожанного мешка\)~ я тебя "
                               "запомню",
                               parse_mode="MarkdownV2"
                               )
        User.create(
            name=None,
            id=message.chat.id
        )
        bot.register_next_step_handler(msg, process_name_step)


def process_name_step(message):
    name = message.text
    user = User.select().where(User.id == message.chat.id).get()
    user.name = name
    user.save()
    bot.send_message(
        message.chat.id,
        "Оке, я сохранил...",
        reply_markup=get_menu()
    )


@bot.message_handler(commands=['user_info'])
def user_info_step(message):
    user = User.select().where(User.id == message.chat.id).get()
    bot.send_message(message.chat.id,
                     "*username:* " + user.name,
                     parse_mode="MarkdownV2",
                     reply_markup=get_menu()
                     )


@bot.message_handler(commands=["change_name"])
def change_name_handler(message):
    msg = bot.send_message(message.chat.id,
                           "Введите новое имя:"
                           )
    bot.register_next_step_handler(msg, process_name_step)


@bot.message_handler(func=lambda message: True)
def commands_handler(message):
    chat_id = message.chat.id
    text = message.text
    if message.chat.type == 'private':
        if text == 'Занять место в очереди':
            if Queue.select(Queue.user_id == chat_id).exists():
                bot.send_message(chat_id, "Вы уже в очереди, чтобы попасть в конец выйдите и войдите в нее :)")
            else:
                Queue.create(
                    user_id=chat_id
                )
                bot.send_message(chat_id, "Добавил")
            send_queue_list(chat_id)
        elif text == 'Посмотреть очередь':
            send_queue_list(chat_id)
        # elif text == 'Сдвинуть очередь на 1':
        #     queue_pop()
        elif text == 'Я ответил!':
            queue_self_pop(chat_id)
        elif text == 'Выйти из очереди':
            queue_self_pop(chat_id)
        else:
            bot.send_message(
                chat_id,
                "Я конечно бог, но такие каманды я не знаю ~кожанный мешок~",
                parse_mode="MarkdownV2"
            )


def send_queue_list(chat_id):
    queue_positions = (Queue
                       .select()
                       .join(User)
                       .order_by(Queue.id.desc()))
    text = "Очередь:\n"
    j = 1
    for i in queue_positions:
        username = (
            User.get(User.id == i.user_id)
        ).name
        if i.user_id == chat_id:
            text += '[{}]: *{}*\n'.format(j, username)
        else:
            text += '[{}]: {}\n'.format(j, username)
        j += 1
    bot.send_message(
        chat_id,
        text,
        reply_markup=get_menu(),
        parse_mode="MarkdownV2"
    )


def queue_self_pop(chat_id):
    queue_positions = (Queue
                       .select()
                       .join(User)
                       .order_by(Queue.id.desc()))
    if len(queue_positions) != 0:
        if queue_positions[0].user_id == chat_id:
            bot.send_message(
                chat_id,
                "Понял, удалил",
                reply_markup=get_menu(),
                parse_mode="MarkdownV2"
            )
        else:
            bot.send_message(
                chat_id,
                "Отвечать мимо очереди не круто, как-нибудь я впилю алерты на всю группу, честное слово"
                "Х(",
                reply_markup=get_menu(),
                parse_mode="MarkdownV2"
            )
        Queue.delete().where(
            Queue.user_id == chat_id
        ).execute()
    send_queue_list(chat_id)


bot.polling()
