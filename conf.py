
# ДАННЫЕ, КОТОРЫЕ МЕНЯТЬ МОЖНО
account_number = 1 # начала диапозона
max_account_number = 8  #  максимальное кол-во аккаунтов
BOT_QUEUE = 1  # *Сколько ботов будут работать одновременно*
max_cycle = 4  #  максимальное кол-во циклов для бота
max_bad_status_code = 10  # максильное кол-во плохих HTTP статус кодов | менять можно, но хз зачем
LTC_ADDRESS = "MQLRETwKE3P2ThYKMnfysgZ9G3M6VZNpoD"  # Вам адресс LTC-криптокошелька

# НЕ МЕНЯЙ ЭТИ ДАННЫЕ, ИНАЧЕ ТЫ СЛОМАЕШЬ КОНФИГУРАЦИЮ
# Use your own values from my.telegram.org
""" CLIENT_CONF """                                 #configuration for telegram client 
api_id = 50322                                      #api id 
api_hash = '9ff1a639196c0779c86dd661af8522ba'       #api hash
MINIMAL_BALANCE = 0.00100010  # Комиссия = 0.00000008 | Эту переменную можно изменить, но только в том случае, если комиссия у LTC-бота стала больше...
BOT_NAME = "lite" # имя бота(пользователя): litecoin, dogecoin
BOT_NAME += "coin_click_bot"
BOT_TITLE = "LTC"  # заголовок БОТА: LTC, DOGE
BOT_TITLE += " Click Bot"  


# Рефералка для ботов: 
# https://t.me/Litecoin_click_bot?start=kXh2R 

# ["ID", "PHONE", "password"]
Accounts = (
    ["id", "номер телефона", "пароль от аккаунта"],
    ["1", "+79845879573509", "парольпароль"],
    ["2", "+7985822853743899", "пароль пароль"],)
