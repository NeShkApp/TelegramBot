# My bot
# https://t.me/Weather_Exchange_API_Bot
import telebot
from telebot import types
import random
import requests
import datetime
import time
# from pprint import pprint

weather_entry = False
exchange_entry = False

bot = telebot.TeleBot('yourTelegramBotAPI')
open_weather_token = 'yourOpenWeatherAPI'

@bot.message_handler(commands=['start'])
def start(message):
    global weather_entry
    global exchange_entry

    weather_entry = False
    exchange_entry = False

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item1 = types.KeyboardButton('Random value🎲')
    item2 = types.KeyboardButton('Exchange rate📊')
    item3 = types.KeyboardButton('Information💾')
    item4 = types.KeyboardButton('Weather🌤')

    markup.add(item1, item2, item3, item4)
    bot.send_message(message.chat.id, f"Hello, <b>{message.from_user.first_name}</b> \U0001F44B\n\nList of my functions:\n"
                                      f"/start\n/link\n\nI can help you with some your quetions\n"
                                      f"Maybe you want to see the weather in your city or the current exchange rate?", parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['link'])
def getlink(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Link', url='https://github.com/NeShkApp'))
    bot.send_message(message.chat.id, "My github link: ", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def bot_message(message):
    global weather_entry
    global exchange_entry

    if message.chat.type == 'private':
        if message.text == 'Random value🎲':
            bot.send_message(message.chat.id, '\U0001F3B2')
            time.sleep(1)
            bot.send_message(message.chat.id, f"Random value🎲:\n"
                                              f"Your number is: <b>{str(random.randint(0, 10))}</b>", parse_mode='html')

        elif message.text == 'Exchange rate📊':
            exchange_entry = True
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('USD')
            item2 = types.KeyboardButton('EUR')
            item3 = types.KeyboardButton('BTC')
            back = types.KeyboardButton('Back⬅')

            markup.add(item1, item2, item3, back)
            bot.send_message(message.chat.id, 'Exchange rate📊:', reply_markup=markup)

        elif message.text == 'Information💾':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('Message💬')
            item2 = types.KeyboardButton('Favourite animal\U0001F99C')
            back = types.KeyboardButton('Back⬅')

            markup.add(item1, item2, back)
            bot.send_message(message.chat.id, 'Information💾: ', reply_markup=markup)

        elif message.text == 'Message💬':
            bot.send_message(message.chat.id, message, parse_mode='html')
        elif message.text == 'Favourite animal\U0001F99C':
            bot.send_message(message.chat.id, '<b>Parrot \U0001F99C</b>', parse_mode='html')

        elif message.text == 'Weather🌤':
            weather_entry = True
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            back = types.KeyboardButton('Back⬅')
            markup.add(back)
            bot.send_message(message.chat.id, 'Input your city: ', reply_markup=markup)

        elif message.text == 'Back⬅':

            weather_entry = False
            exchange_entry = False

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            item1 = types.KeyboardButton('Random value🎲')
            item2 = types.KeyboardButton('Exchange rate📊')
            item3 = types.KeyboardButton('Information💾')
            item4 = types.KeyboardButton('Weather🌤')

            markup.add(item1, item2, item3, item4)
            bot.send_message(message.chat.id, "Back⬅", parse_mode='html', reply_markup=markup)


        elif weather_entry:
            if message.text == 'Back⬅':
                pass
            else:
                # print(message.text)
                weatherStr = get_print_weather(message.text)
                bot.send_message(message.chat.id, weatherStr, parse_mode='html')

        elif exchange_entry:
            if message.text == 'Back⬅':
                pass
            else:
                # print(message.text)
                exchangeStr = get_exchange(message.text)
                bot.send_message(message.chat.id, exchangeStr, parse_mode='html')

        elif message.text == 'Hi':
            bot.send_message(message.chat.id, f'Hello, {message.from_user.first_name}')

        else:
            bot.send_message(message.chat.id, "I don't understand you")


@bot.message_handler(content_types=['photo'])
def get_user_photo(message):
    bot.reply_to(message, "Have a nice photo!")

@bot.message_handler(content_types=['document'])
def get_user_photo(message):
    bot.reply_to(message, "It's a document!")

@bot.message_handler(content_types=['audio'])
def handle_sticker(message):
    bot.reply_to(message, "It's my favourite music!")

@bot.message_handler(content_types=['sticker'])
def handle_sticker(message):
    bot.send_sticker(message.chat.id, message.sticker.file_id)

def get_print_weather(city):
    codes_to_emoji = {
        "Clear": "Clear \U00002600",
        "Clouds": "Clouds \U00002601",
        "Rain": "Rain \U00002614",
        "Hard rain": "Hard rain \U00002614",
        "Thunder": "Thunder \U000026A1",
        "Snow": "Snow \U0001F328",
        "Mist": "Mist \U0001F32B"
    }

    try:
        r = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric'
        )
        data = r.json()
        # pprint(data)

        weather_description = data['weather'][0]['main']
        if weather_description in codes_to_emoji:
            wd = codes_to_emoji[weather_description]
        else:
            wd = "I don't know about this weather😭"

        city = data['name']
        feels = data['main']['feels_like']
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        wind = data['wind']['speed']
        sunriset = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunsett = datetime.datetime.fromtimestamp(data['sys']['sunset'])

        return(
            f'<b>Date:</b> {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}\n'
            f'<b>City:</b> {city}\n'
            f'<b>Feels like:</b> {feels} °C\n'
            f'<b>Temperature:</b> {temp} °C\n{wd}\n'
            f'<b>Humidity:</b> {humidity} %\n'
            f'<b>Wind speed:</b> {wind} m/s\n'
            f'<b>Sunrise time:</b> {sunriset}\n'
            f'<b>Sunset time:</b> {sunsett}\n'
            f'Have a good day❤')

    except Exception as ex:
        print(ex)
        return('⚠Name of city are wrong⚠')

def get_exchange(message):
    try:
        r = requests.get('https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5')
        data = r.json()
        # pprint(data)

        for valut in data:
            if message == valut['ccy']:
                Buy = round(float(valut['buy']), 3)
                Sale = round(float(valut['sale']), 3)
                return (f'Date: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}\n'
                        f'<b>{valut["ccy"]}</b> in <b>{valut["base_ccy"]}</b>💰\n'
                        f'Buy: <b>{Buy}</b>\n'
                        f'Sale: <b>{Sale}</b>')

    except Exception as ex:
        print(ex)
        return('⚠Invalid input⚠')

bot.polling(none_stop=True)

