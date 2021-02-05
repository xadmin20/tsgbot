import csv, config, os.path, os
import datetime
file_bd = config.file_db

name = "name"
id = "91124946"
address = "spb"
email = "a@a"
tel = "+7"
info = "info"


def reed_file(id):
    with open(file_bd, "r") as openfile:
        reader = csv.reader(openfile, delimiter=",")
        for row in reader:
            if id == row[0]:
                print(id)


#reed_file(id)
# регистрация пользователей у бота
def add_file(id, addressis, emailis, telis, dateis):
    a = datetime.datetime.today().strftime("%d.%m.%Y")
    b = datetime.datetime.today().strftime("%H:%M:%S")
    dateis = a + " " + b
    new_dir = config.num_dir + str(id)
    #проверяем есть ть ли каталог с названием ID
    if not os.path.isdir(new_dir):
        os.mkdir(new_dir)
    else:
        print(f"Каталог {new_dir} создан")


    with open(config.file_db, 'a+', newline='', encoding='utf-8') as openfile:
        user = [id, addressis, emailis, telis, dateis]
        writer = csv.writer(openfile)
        writer.writerow(user)
        print("reg ok!")
        return


# add_file(id, name, address, email, tel, info)
#reed_file(id)
#тение базы полностью для админа
def reed_file_all_admin():
    with open(config.file_db, encoding='utf-8') as r_file:
    # Создаем объект reader, указываем символ-разделитель ","
        file_reader = csv.reader(r_file, delimiter=",")
    # Счетчик для подсчета количества строк и вывода заголовков столбцов
        count = 0
    # Считывание данных из CSV файла
        for row in file_reader:
            if count == 0:
                # Вывод строки, содержащей заголовки для столбцов
                print(f'Файл содержит столбцы: {", ".join(row)}')
            else:
            # Вывод строк
                print(f'ID={row[0]}, Адрес: {row[1]}, Электронная почта: {row[2]}, Телефон: {row[3]}, Дополнительная информация: {row[4]}.')
            count += 1
        print(f'Всего в базе {count} абонентов.')

def reed_file_all_menu(file):
    file_dir = "menu/" + file
    with open(file_dir, "r", encoding='utf-8', newline="") as r_file:
    # Создаем объект reader, указываем символ-разделитель ","
        file_reader = csv.reader(r_file, delimiter=",")
    # Счетчик для подсчета количества строк и вывода заголовков столбцов
    # Считывание данных из CSV файла
        for row in file_reader:
            text = f"{row[0]} тел: {row[1]} - {row[2]}"
            return text
#reed_file_all_admin()

#write info to base
def write_file(id, nameis, address, emailis, telis, infois):
    with open("config.file_db", mode="a", encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter=",", lineterminator="\r")
        file_writer.writerow([id, name, address, email, tel, info])
#write_file(id, name, address, email, tel, info)

def count_data(id, data_id, photo_id, time_is_telegram, water):
    id = str(id)
    id_file = config.num_dir + "/" + id + "/" + config.file_db
    with open(id_file, mode="a", encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter=",", lineterminator="\r")
        file_writer.writerow([id, data_id, photo_id, time_is_telegram, water])