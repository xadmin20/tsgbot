import config, csv
#/list
def admin_send_all():
    with open(config.file_db, "r", encoding='utf-8', newline="") as r_file:
        file_reader = csv.reader(r_file, delimiter=",")
        for row in file_reader:
            text = row[0]
            return text
#admin_send_all()
#/msg <ID>    <сообщение>    - отправка сообщения от имени бота пользователю с ID.
def admin_msg_id(id, message):
    return id, message


#send_all()