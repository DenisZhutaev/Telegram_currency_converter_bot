import telebot
from telebot import types
from config import keys, TOKEN
from extensions import APIException, CryptoConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def echo_test(message: telebot.types.Message):
    # Создаем объект клавиатуры и список кнопок
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('/values', '/start')

    text = 'Чтобы конвертировать валюту введите команду боту через пробел в следующем формате\n' \
           '<имя валюты>' \
           '<в какую валюту перевести>' \
           '<количество переводимой валюты>' \
           '\nУвидеть список всех доступных валют: /values'

    # Отправляем сообщение с клавиатурой
    bot.reply_to(message, text, reply_markup=markup)


@bot.message_handler(commands=['values'])
def echo_test(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    if message.text == 'Валюты':
        echo_test()
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Слишком много параметров.')

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()
