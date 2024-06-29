import requests
import json


class APIException(Exception):
    #Пользовательское исключение для обработки ошибок, связанных с API.

    def __init__(self, message):
        super().__init__(message)
        self.message = message


class Converter:
    #Класс для получения цен из API и конвертации валют.

    @staticmethod
    def get_price(base, quote, amount):
        # Преобразуем валюты к нижнему регистру для корректной обработки
        base = base.lower()
        quote = quote.lower()

        # Проверка на одинаковые валюты
        if base == quote:
            raise APIException("Конвертация одинаковых валют невозможна.")

        # Проверка корректности числа amount
        try:
            amount = float(amount)
        except ValueError:
            raise APIException("Некорректное количество валюты.")

        # Формируем URL запроса к API
        url = f"https://api.exchangerate-api.com/v4/latest/{base}"
        response = requests.get(url)
        if response.status_code != 200:
            raise APIException("Ошибка при запросе к API.")

        data = json.loads(response.text)
        rates = data.get('rates')
        if not rates:
            raise APIException("Некорректный ответ от API.")

        # Получаем обменный курс для запрошенной валюты
        conversion_rate = rates.get(quote.upper())
        if conversion_rate is None:
            raise APIException(f"Валюта {quote} недоступна для конвертации.")

        # Возвращаем итоговую сумму
        return conversion_rate * amount


# Словарь доступных валют
CURRENCIES = {
    "евро": "eur",
    "доллар": "usd",
    "рубль": "rub"
}