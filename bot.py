import telebot
from config import TOKEN
from extensions import APIException, Converter, CURRENCIES

# Инициализируем бота
bot = telebot.TeleBot(TOKEN)


# Обработчик команд /start и /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    text = (
        "Добро пожаловать! Я бот для конвертации валют.\n"
        "Чтобы узнать цену, отправьте сообщение в формате:\n"
        "<имя валюты> <в какую валюту перевести> <количество>\n"
        "Пример: евро доллар 100\n"
        "Доступные команды:\n"
        "/values - Показать доступные валюты\n"
    )
    bot.reply_to(message, text)


# Обработчик команды /values, который показывает доступные валюты
@bot.message_handler(commands=['values'])
def values(message):
    text = "Доступные валюты:\n"
    for currency in CURRENCIES.keys():
        text += f"- {currency}\n"
    bot.reply_to(message, text)


# Обработчик сообщений, который выполняет конвертацию валют
@bot.message_handler(func=lambda message: True)
def convert(message):
    try:
        # Разбиваем сообщение на части
        values = message.text.lower().split()
        if len(values) != 3:
            raise APIException(
                "Неверное количество параметров. Используйте формат: <имя валюты> <в какую валюту перевести> <количество>")

        base, quote, amount = values
        base = CURRENCIES.get(base)
        quote = CURRENCIES.get(quote)
        if not base or not quote:
            raise APIException("Неверно указана валюта. Используйте команду /values для просмотра доступных валют.")

        # Преобразуем количество в число и выполняем конвертацию
        amount = float(amount)
        total = Converter.get_price(base, quote, amount)

    except APIException as e:
        bot.reply_to(message, f"Ошибка: {e.message}")
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {str(e)}")
    else:
        # Отправляем результат конвертации пользователю
        text = f"Цена {amount} {values[0]} в {values[1]}: {total}"
        bot.reply_to(message, text)


# Запуск бота
bot.infinity_polling()