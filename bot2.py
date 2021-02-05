import csv
import telebot
from telebot import types
import datetime
import config
from admin import admin_send_all
from bot_registration import add_file, count_data, reed_file_all_menu
import os
import logging
from config import get_logger

logging.basicConfig(filename="sample.log", level=logging.INFO)
logging.debug("This is a debug message")
logging.info("Informational message")
logging.error("An error has happened!")


bot = telebot.TeleBot(config.token2)
water = ""
edit_cool_water = ""
edit_hot_water = ""
@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/send':
        global water
        water = message.text
        keyboard = types.InlineKeyboardMarkup()
        cool_water = types.InlineKeyboardButton(text='Холодная вода', callback_data='cool_water')
        hot_water = types.InlineKeyboardButton(text='Горячая вода', callback_data='hot_water')
        keyboard.add(cool_water)
        keyboard.add(hot_water)
        next_act = "Выберите какие показания Вы подаете"
        bot.send_message(message.from_user.id, text=next_act, reply_markup=keyboard)
    elif message.text == "/tel":
        with open(config.file_tel, "r", encoding='utf-8', newline="") as r_file:
            file_reader = csv.reader(r_file)
            for row in file_reader:
                text = f"{row[0]} тел: {row[1]}"
                bot.send_message(message.from_user.id, text)
    elif message.text == "/info":
        with open(config.file_info, encoding='utf-8', newline="") as file:
            for row in file:
                bot.send_message(message.from_user.id, row)
    elif message.text == "/prov":
        with open(config.file_prov, encoding='utf-8', newline="") as file:
            for row in file:
                bot.send_message(message.from_user.id, row)
    elif message.text == "/help":
        with open(config.file_comm, "r", encoding='utf-8', newline="") as r_file:
            file_reader = csv.reader(r_file)
            for row in file_reader:
                text = f"[Команда:  {row[0]}]  [Описание: {row[1]}]"
                bot.send_message(message.from_user.id, text)
    elif message.text == "/admin":
        if str(message.chat.id) == str(config.admin):
            with open(config.file_admin, encoding='utf-8', newline="") as file:
                for row in file:
                    bot.send_message(message.from_user.id, row)
        else:
            bot.send_message(message.from_user.id, "Вы кто такой, давай до свидания!")
    elif message.text == '/reg':
        bot.send_message(message.from_user.id, "Введите Вашу квартиру(аппартаменты, офис и тд):")
        bot.register_next_step_handler(message, get_address)  # следующий шаг – функция get_address
    #Если Бот не знает команды
    else:
        bot.send_message(message.from_user.id, "Я не понимаю Вас, напишите /help  чтобы узнать все мои команды.")

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        id = call.message.chat.id
        time_is_telegram = call.message.date
        # call.data это callback_data, которую мы указали при объявлении кнопки
        # .... #код сохранения данных, или их обработки
        add_file(id, address, emailis, telis, time_is_telegram)
        bot.send_message(call.message.chat.id, "Спасибо, Ваши данные записаны! Ждите подтверждения от Администратора.",
                         reply_markup=None)
        send = config.admin
        a = datetime.datetime.today().strftime("%d.%m.%Y")
        b = datetime.datetime.today().strftime("%H:%M:%S")
        dateis = a + " " + b
        bot.send_message(send,
                         f"Пришла новая заявка!!! Айди: {id}, Адрес: {address}, Телефон: {telis}, Почта: {emailis}, Время: {dateis}")
    elif call.data == "no":
        # ... #переспрашиваем
        bot.send_message(call.message.chat.id, "Ваша запись не активна, пожалуйста повторите заново.",
                         reply_markup=None)
    if call.data == "cool_water":
        id = call.message.chat.id
        #вызываем функцию для запроса показаний
        send = config.admin
        print(f"Новые показания холодной воды от: {id}")
        #bot.send_message(send, f"Новые показания от: {id}")
        bot.register_next_step_handler(call.message, add_cool_water)


    elif call.data == "hot_water":
            id = call.message.chat.id
            # вызываем функцию для запроса показаний
            send = config.admin
            print(f"Новые показания горячей воды от: {id}")
            #bot.send_message(send, f"Новые показания от: {id}")
            bot.register_next_step_handler(call.message, add_hot_water)
#... #переспрашиваем

        #bot.send_message(call.message.chat.id, "Ваша запись не активна, пожалуйста повторите заново.", reply_markup=None)
def add_cool_water(call):
    global edit_cool_water
    edit_cool_water = call.text
    bot.send_message(call.from_user.id, f"Ваши показания: {edit_cool_water}м3, приложите фотографию счетчика.")
    bot.register_next_step_handler(call, cool_water_photo)

def add_hot_water(call):
    global edit_hot_water
    edit_hot_water = call.text
    bot.send_message(call.from_user.id, f"Ваши показания: {edit_hot_water}м3, приложите фотографию счетчика.")
    bot.register_next_step_handler(call, hot_water_photo)

@bot.message_handler(content_types=["photo", "text"])
def cool_water_photo(call):
    global water
    try:
        cool_water_photo = call.photo[0].file_id
        #bot.send_message(call.from_user.id, f"Ваши показания: {edit_cool_water}м3")
        #bot.send_message(call.chat.id, cool_water_photo)
        time_is_telegram = call.date
        a = datetime.datetime.today().strftime("%d.%m.%Y")
        b = datetime.datetime.today().strftime("%H:%M:%S")
        dateis = a + " " + b
        water = "cool"
        count_data(call.from_user.id, edit_cool_water, cool_water_photo, dateis, water)
        file_info = bot.get_file(call.photo[len(call.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        dir = str(call.from_user.id)
        src = 'number/' + dir + "/" + file_info.file_path
        new_dir = 'number/' + dir + "/photos"
        ##################
        if not os.path.isdir(new_dir):
            os.mkdir(new_dir)
        else:
            print(f"Каталог {new_dir} создан")
            ######################
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
            bot.reply_to(call.from_user.id, "Фото добавлено")
            bot.send_message(call.message.chat.id, "Спасибо, Ваши данные записаны! Ждите подтверждения от Администратора.", reply_markup=None)


    except Exception as error:
        #logger(error)
        #bot.send_message(call.chat.id, "Ошибка! Пожалуйста пришли фотографию счетчика!")
        #bot.register_next_step_handler(call, keyboard)
        print("Exception Info: {}".format(error))



def hot_water_photo(call):
    global water
    try:
        hot_water_photo = call.photo[0].file_id
        bot.send_message(call.from_user.id, f"Ваши показания: {edit_hot_water}м3, {call.from_user.id}")
        #bot.send_message(call.chat.id, hot_water_photo)
        time_is_telegram = call.date
        a = datetime.datetime.today().strftime("%d.%m.%Y")
        b = datetime.datetime.today().strftime("%H:%M:%S")
        dateis = a + " " + b
        water = "hot"
        count_data(call.from_user.id, edit_hot_water, hot_water_photo, dateis, water)
        file_info = bot.get_file(call.photo[len(call.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        dir = str(call.from_user.id)
        src = 'number/' + dir + "/" + file_info.file_path
        new_dir = 'number/' + dir + "/photos"
        ##################
        if not os.path.isdir(new_dir):
            os.mkdir(new_dir)
            print(f"Новый каталог {new_dir} создан.")
        else:
            ######################
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
        #bot.reply_to(call.from_user.id, "Фото добавлено")
        bot.send_message(call.from_user.id, "Спасибо, Ваши данные записаны! Ждите подтверждения от Администратора.", reply_markup=None)


    except Exception as error:
         #logger(error)
         #bot.send_message(call.chat.id, "Ошибка! Пожалуйста пришли фотографию счетчика!")
        #bot.register_next_step_handler(call, keyboard)
         print("Exception Info: {}".format(error))


def logger(message):
    dtn = datetime.datetime.now()
    botlogfile = open('TestBot.log', 'a')
    print(dtn.strftime("%d-%m-%Y %H:%M"), 'Пользователь ' + message.from_user.first_name, message.from_user.id, 'написал следующее: ' + message.text, file=botlogfile)
    botlogfile.close()



def get_address(message): #получаем address
    global address
    address = message.text
    bot.send_message(message.from_user.id, "Введите Ваш номер телефона (+79991234567)")
    bot.register_next_step_handler(message, get_telis)

def get_telis(message):    #получаем tel
    global telis
    telis = message.text
    #########################
    bot.send_message(message.from_user.id, "Ваша электронная почта:")
    bot.register_next_step_handler(message, get_emailis)

def get_emailis(message):    #получаем время
    global emailis
    emailis = message.text
    #bot.send_message(message.from_user.id, "config_psiho.nameis")
    bot.send_message(message.from_user.id, "Проверьте пожалуйста введенную Вами информацию, если она верна нажмите кнопку ДА, или кнопку НЕТ если хотите изменить информацию о записи.")
   # bot.register_next_step_handler(message, get_age);
# клавиатура
    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes') #кнопка «Да»
    keyboard.add(key_yes) #добавляем кнопку в клавиатуру
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)
    time_is_telegram = message.date
    id_is_telegram = message.chat
    question = "Ваш адрес: " + str(address) + ", Телефон: " + str(telis) + ", Ваша почта: " + str(emailis) + "?"
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

config.get_console_handler()
config.get_logger(__name__)
print("Starting bot --->>>")

bot.polling(none_stop=True, interval=0)
