
import telebot

from telebot import types
from datetime import datetime

bot = telebot.TeleBot('5359893641:AAEUOfY7NYFWIV5UoXqfAIYpbjqxRtqnRvw')  # token
TO_CHAT_ID = 1201195379


def mainmenu():
    keyboard = types.InlineKeyboardMarkup()  # выбираем тип клавиатуры
    about_hotel = types.InlineKeyboardButton(text='Об отеле\U0001F4AB', callback_data='btn1')
    contacts = types.InlineKeyboardButton(text='Контакты\U0001F514', callback_data='btn4')
    keyboard.add(about_hotel, contacts)
    restoran = types.InlineKeyboardButton(text='Ресторан\U0001F354', callback_data='btn3')
    uslugi = types.InlineKeyboardButton(text='Удобства и услуги\U0001F300', callback_data='btn6')
    keyboard.add(restoran, uslugi)
    area = types.InlineKeyboardButton(text='Что поблизости?\U0001F440', callback_data='btn2')
    time = types.InlineKeyboardButton(text='Местное время\U0001F552', callback_data='btn5')
    keyboard.add(time, area)
    call_admin = types.InlineKeyboardButton(text='Задать вопрос администратору \U0001F4AC', callback_data='btn7')
    keyboard.add(call_admin)
    return keyboard


@bot.message_handler(commands=['start'])
def start(message):
    keyboard_1 = mainmenu()
    # можно вставить картинку с приветствием 
    bot.send_message(message.chat.id,
                     'Привет я бот отеля <b>"Gratia"</b>, кликайте по кнопкам меню или задайте вопрос администратору',
                     reply_markup=keyboard_1, parse_mode='HTML')


@bot.message_handler(content_types=['text'])  # возвращает вопрос администратора
def all_messages(message):
    bot.forward_message(TO_CHAT_ID, message.chat.id, message.message_id)


@bot.callback_query_handler(func=lambda callback: callback.data)
def answer_callback(callback):
    if callback.data == 'btn4':
        kb = types.InlineKeyboardMarkup(row_width=2)
        gps_yandex = types.InlineKeyboardButton(text='Перейти в Yandex карты',
                                                url='https://yandex.ru/maps/-/CCUJVQgPHA')
        gps_google = types.InlineKeyboardButton(text='Перейти в Google карты',
                                                url='https://g.page/WhitePeakHotel?share')
        kb.add(gps_yandex, gps_google)
        bot.send_message(callback.message.chat.id, """
<b>Наши контакты:</b>
Адрес: г. Асирис, ул. Одиссея д.1
Сайт: nikbot-hotel.ru
Ресепшн: +79168697207
Отдел бронирования: +79168697207
email: nikbot.hotel@gmail.com
""", reply_markup=kb, parse_mode='HTML')

    elif callback.data == 'btn7':
        bot.send_message(callback.message.chat.id, 'Задайте свой вопрос')

    elif callback.data == 'btn5':  # возвращает сообщение с датой и временем в режиже реального времени
        bot.send_message(callback.message.chat.id,
                         '<b>Местное время:</b>\n' + str(datetime.now().strftime("%d.%m.%Y, %H:%M")), parse_mode='HTML')

    elif callback.data == 'btn2':  # возвращает сообщение с "Что поблизости?"
        # kb = types.InlineKeyboardMarkup(row_width=1)
        # weather_ = types.InlineKeyboardButton(text='необходимо спарсить сайт с погодой', callback_data='btn_weather')
        # kb.add(weather_)
        bot.send_message(callback.message.chat.id,
                         'Супермаркеты, Аптеки, Автовокзал')  # добавить картинки с изображениями

    elif callback.data == 'btn3':  # информация о ресторане или кафе, также возможен лобибар и буфет
        bot.send_message(callback.message.chat.id, """
Бар расположен на 1-ом этаже
Ресторан находится на территории отеля в 1-м корпусе
Завтрак в номер, для заказа свяжитесь с администратором по номеру тел. +79168697207
""")

    elif callback.data == 'btn1':
        photo_hotel = open('HOTEL.png', 'rb')
        bot.send_photo(callback.message.chat.id, photo_hotel)
        bot.send_message(callback.message.chat.id, """
Отель Gratia расположен в уютном районе Гротеска, в нескольких шагах от дизайнерских магазинов.
К услугам гостей номера и люксы с бесплатным Wi-Fi. При отеле работает бар-ресторан, где подают блюда средиземноморской кухни.
До исторического центра Гротеска несколько минут ходьбы.
Все номера в мягких тонах обставлены специально подобранной мебелью и оформлены в современном стиле.
В распоряжении гостей кондиционер, телевизор.
В некоторых номерах обустроена гостиная зона.
Ванная комната с ванной или душем укомплектована тапочками, бесплатными туалетно-косметическими принадлежностями и феном.
Стойка регистрации открыта круглосуточно. По запросу и за дополнительную плату организуется трансфер от/до аэропорта.
От отеля Gratia до Национального сада — 400 метров, а до центральной площади — 500 метров.
Расстояние до аэропорта имени Циклопа одноглазого составляет 38 км.
Расстояние до железнодорожного вокзала составляет 8 км.
Это любимая часть города Гротеска среди наших гостей согласно независимым отзывам.
""", parse_mode='HTML')
        kb = types.InlineKeyboardMarkup(row_width=1)  # добавляем кнопку с возвратом в меню
        return_back = types.InlineKeyboardButton(text='Главное меню', callback_data='return_back')
        kb.add(return_back)
        bot.send_message(callback.message.chat.id, 'вернуться в главное меню', reply_markup=kb)

    elif callback.data == 'btn6':
        uslugimenu = types.InlineKeyboardMarkup(row_width=2)
        free = types.InlineKeyboardButton(text='Бесплатные', callback_data='btn_free')
        not_free = types.InlineKeyboardButton(text='Платные', callback_data='btn_not_free')
        back = types.InlineKeyboardButton(text='Главное меню', callback_data='btn_back')
        uslugimenu.add(free, not_free, back)
        bot.send_message(callback.message.chat.id, 'Услуги отеля',
                         reply_markup=uslugimenu)

    elif callback.data == 'btn_free':
        bot.send_message(callback.message.chat.id, """
Бесплатный <b>wifi</b>
Бесплатная парковка на территории отеля
Утюг и гладильная доска на этаже
Уборка номера один раз в день
Камера хранения
Услуга "звонок-будильник"
""", parse_mode='HTML')

    elif callback.data == 'btn_not_free':
        bot.send_message(callback.message.chat.id, """
<b>Сейф у администратора</b>        
<b>Трансфер:</b> 
до ЖД вокзала г.Асириса - 1000р
до аэропорта им.Кандинского - 1700р
<b>Дополнительная уборка номера</b> - 350р
<b>Прачечная:</b> 
За дополнительную плату гости могут заказать услуги стирки. 
Для этого необходимо обратиться к администратору.

""", parse_mode='HTML')

    elif callback.data == 'btn_back':
        bot.send_message(callback.message.chat.id, 'вы вернулись в главное меню', reply_markup=mainmenu())

    elif callback.data == 'return_back':  # для кнопки  в разделе "Об отеле"
        bot.send_message(callback.message.chat.id, 'вы вернулись в главное меню', reply_markup=mainmenu())


bot.infinity_polling()