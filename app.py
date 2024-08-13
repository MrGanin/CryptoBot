import telebot
from config import TOKEN, keys
from extensions import APIExeption, API


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start','help'])
def echo_test(message: telebot.types.Message):
    text = ('Чтобы начать работу введите команду боту в следующем формате:\n '
            '\n<название валюты><в какую валюту перевести><количество переводимой валюты>\n'
            '\nПример сообщения: "доллар рубль 100"\n'
            '\nУвидеть список всех доступных валют /values')
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key ))

    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIExeption('Неправильно введены параметры.')

        quote, base, amount = values
        total_base = API.get_price(quote, base, amount)*float(amount)
    except APIExeption as e:
        bot.send_message(message.chat.id, f'Ошибка пользователя.\n{e}')

    except Exception as e:
        bot.send_message(message.chat.id, f'Не удалось обработать команду.\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling()
