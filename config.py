import logging
import sys
from logging.handlers import TimedRotatingFileHandler

TOKEN = "1450495246:AAHdu9wSGcW2r4N29S7QNwIPy8Ew7zZJHzo"
token = "1450495246:AAHdu9wSGcW2r4N29S7QNwIPy8Ew7zZJHzo"
#token TehnikaspbBot
token2 = "750917583:AAEL795-RhVOEmOwO16Oaywq9e_Xm4-eKoI"
mouthis = "Введите месяц:"
dateis = "Введите дату:"
timeis = "Введите время:"
nameis = "Введите Имя:"
telis = "Введите телефон:"
infois = "Введите информацию:"
id_is_telegram = "ID is telegram"
time_is_telegram = "Time is registration"
admin = "91124946"
file_db = "named.csv"
num_dir = "number/"
admin_channel = "@tsgtest"
file_tel = "menu/tel.csv"
file_comm = "menu/commands.csv"
file_info = "menu/info.txt"
file_admin = "menu/admin.txt"
file_prov = "menu/prov.txt"


FORMATTER = logging.Formatter("%(time)s — %(name)s — %(level)s — %(message)s")
LOG_FILE = "my_app.log"
def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler():
    file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
    file_handler.setFormatter(FORMATTER)
    return file_handler


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG) # лучше иметь больше логов, чем их нехватку
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())
    logger.propagate = False
    return logger
