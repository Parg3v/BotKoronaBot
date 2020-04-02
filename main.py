import COVID19Py
import telebot
from telebot import types
covid19 = COVID19Py.COVID19()

bot = telebot.TeleBot('1195171503:AAGJnefGQyx-_7AUv_LdjOChVsO5Igifz_Q')

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('Во всём мире')
    btn2 = types.KeyboardButton('Армения')
    btn3 = types.KeyboardButton('Россия')
    btn4 = types.KeyboardButton('Япония')
    markup.add(btn1, btn2, btn3, btn4)
    send_msg = f'<b>Привет <em>{message.from_user.first_name} </em>!</b>\n <b>Нажми на любую из <em>стран</em>, чтобы получить <em>информацию </em>про каронавирус в этой <em>стране</em></b>'
    bot.send_message(message.chat.id, send_msg, parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def mess(message):
    final_message = ""
    get_message_bot = message.text.strip().lower()
    if get_message_bot == "россия":
        location = covid19.getLocationByCountryCode("RU")
    elif get_message_bot == "армения":
        location = covid19.getLocationByCountryCode("BY")
    elif get_message_bot == "япония":
        location = covid19.getLocationByCountryCode("JP")
    else:
        location = covid19.getLatest()
        final_message = f"<u>Данные по всему миру:</u>\n<b>Заболевших: </b>{location['confirmed']:,}\n<b>Сметрей: </b>{location['deaths']:,}"

    if final_message == "":
        date = location[0]['last_updated'].split("T")
        time = date[1].split(".")
        final_message = f"<u>Данные по стране:</u>\nНаселение: {location[0]['country_population']:,}\n" \
                        f"Последнее обновление: {date[0]} {time[0]}\nПоследние данные:\n<b>" \
                        f"Заболевших: </b>{location[0]['latest']['confirmed']:,}\n<b>Сметрей: </b>" \
                        f"{location[0]['latest']['deaths']:,}"

    bot.send_message(message.chat.id, final_message, parse_mode='html')

bot.polling(none_stop=True)