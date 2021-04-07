from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from telethon import sync, events, TelegramClient
from colorama import init, Fore, Style
from datetime import datetime
import urllib.request
import subprocess, sys
import time
import sqlite3
import re
import requests
import pytz
import os
import asyncio
from conf import *
from registration import *

init()


async def client_authorization(_account_number):
    _account_number -= 1
    print(f"Очередь аккаунта № {Accounts[_account_number][0]}")
    phone = Accounts[_account_number][1]
    session = str(".anon" + str(_account_number+1))
    # client = TelegramClient(session, api_id, api_hash, proxy=("http", proxy[1][0], proxy[1][1]))
    # print(f"{_account_number+1}: "+ "Прокси: " + Fore.RED +"128.199.254.103:" + str(23352) + Fore.GREEN)
    # client = TelegramClient(session, api_id, api_hash, proxy=("http", "128.199.254.103", 23352))
    client = TelegramClient(session, api_id, api_hash)
    print(f"Входим в аккаунт: {phone}")
    return client


async def change_account(_account_number, no_tasks, cycle, count_bad_status_code):
    str_change_account = f"{_account_number}: Переходим на аккаунт {_account_number+1}. " + Fore.RED + "Причина:" + Fore.YELLOW
    if no_tasks >= 2:
        print(f"{str_change_account} Нет заданий уже: {no_tasks}")
        return True
    if cycle != max_cycle:
        print(f"{_account_number}: Пройдено циклов: {cycle}")
    if cycle == max_cycle:
        print(f"{str_change_account} Пройдено циклов: {cycle}")
        return True
    if count_bad_status_code >= max_bad_status_code:
        print(f"{str_change_account} Было " + Fore.RED + f"{count_bad_status_code}" + Fore.YELLOW + " плохих статус кодов")
        return True
    return False


def get_now_time():
    return datetime.now(pytz.timezone('Europe/Moscow')).strftime('%Y-%m-%d %H:%M:%S')


async def ending(account_number, max_account_number, count, time_sleep):
    await asyncio.sleep(1)
    account_number += BOT_QUEUE
    if account_number > max_account_number:
        count += 1
        print(Fore.GREEN + f"WHILE завершился: {count}\n" + Fore.YELLOW)
        await withdraw(max_account_number)
        print(f"Начало: {start_time}\nСейчас: {get_now_time()}" + Fore.YELLOW)
        print("\n" + Fore.RED + f"У нас перерыв на кофе {time_sleep} минут!" + Fore.YELLOW)
        await asyncio.sleep(60 * time_sleep)  # ждем 5 минут (60 * 5)
    return account_number, count


async def run(_account_number, max_account_number, max_cycle, time_sleep):
    count = 0
    account_number = _account_number
    while True:
        count_good_status_code = 0  # кол-во статус кодок = 200
        count_bad_status_code = 0  # кол-во статус кодов != 200
        cycle = 0  # кол-во циклов
        no_tasks = 0  # нет заданий уже

        if account_number > max_account_number:
            account_number = 1

        client = await client_authorization(account_number)
        await client.start()
        print(Fore.GREEN + f"### {account_number}: Клиент вошёл ###" + Fore.YELLOW)  # или RESET

        dlgs = await client.get_dialogs()
        for dlg in dlgs:
            if dlg.title == BOT_TITLE:
                tegmo = dlg
                # print("TEGMO = ", tegmo)
        await client.send_message(BOT_TITLE, "🖥 Visit sites")
        await asyncio.sleep(30)
        while True:
            await asyncio.sleep(6)
            if await change_account(account_number, no_tasks, cycle, count_bad_status_code):
                await client.disconnect()
                print(Fore.GREEN + f"{account_number}: Клиент отключился\n" + Fore.YELLOW)
                break

            msgs = await client.get_messages(tegmo, limit=1)
            for mes in msgs:
                if re.search(r'\bseconds to get your reward\b', mes.message):
                    print(Fore.GREEN + f"{account_number}: Найдена НАГРАДА!" + Fore.YELLOW)
                    str_a = str(mes.message).replace('You must stay on the site for', '')
                    str_a = str_a.replace('seconds to get your reward.', '')
                    waitin = int(str_a)
                    print(f"{account_number}: Ждать придется: {waitin} секунд...")
                    await client.send_message(BOT_TITLE, "/visit")
                    await asyncio.sleep(3)
                    msgs2 = await client.get_messages(tegmo, limit=1)
                    for mes2 in msgs2:
                        button_data = mes2.reply_markup.rows[1].buttons[1].data
                        message_id = mes2.id
                        print(f"{account_number}: Перехожу по ссылке")
                        await asyncio.sleep(2)
                        url_rec = messages[0].reply_markup.rows[0].buttons[0].url
                        await asyncio.sleep(6)
                        fp = urllib.request.urlopen(url_rec)
                        mystr = fp.read().decode("utf8")
                        fp.close()
                        if re.search(r'\bSwitch to reCAPTCHA\b', mystr):
                            from telethon.tl.functions.messages import GetBotCallbackAnswerRequest
                            resp = await client(GetBotCallbackAnswerRequest(BOT_TITLE, message_id, data = button_data))
                            await asyncio.sleep(2)
                            print(Fore.RED + f"{account_number}: КАПЧА!" + Fore.YELLOW)

                        else:
                            await asyncio.sleep(waitin + 2)

                elif re.search(r'\bSorry\b', mes.message):
                    no_tasks += 1
                    print(Fore.RED + f"{account_number}: Найдено Sorry: {no_tasks}" + Fore.YELLOW)

                else:
                    await asyncio.sleep(4)
                    messages = await client.get_messages(BOT_NAME)
                    url_rec = messages[0].reply_markup.rows[0].buttons[0].url
                    file_urls = open("urls.txt")
                    file_url = file_urls.read()
                    if file_url == url_rec:
                        print(Fore.RED + f"{account_number}: Найдено повторение ссылки!" + Fore.YELLOW)
                        msgs2 = await client.get_messages(tegmo, limit=1)
                        for mes2 in msgs2:
                            button_data = mes2.reply_markup.rows[1].buttons[1].data
                            message_id = mes2.id
                            from telethon.tl.functions.messages import GetBotCallbackAnswerRequest
                            resp = await client(GetBotCallbackAnswerRequest(tegmo, message_id, data = button_data))
                            await asyncio.sleep(2)
                    else:
                        status_code = str(requests.get(url_rec).json)
                        status_code = status_code.replace("<bound method Response.json of <Response [", "")
                        status_code = int(status_code.replace("]>>", ""))
                        if status_code == 200 or status_code == 503:
                            print(Fore.BLUE + f"{account_number}: Статус код = {status_code}" + Fore.YELLOW)
                            file_urls = open("urls.txt", 'w')
                            file_urls.write(url_rec)
                            file_urls.close()
                            print(Fore.GREEN + f"{account_number}: Новая запись в файле сделана" + Fore.YELLOW)
                            await asyncio.sleep(15)
                            count_good_status_code += 1
                            print(f"{account_number}: Это запись номер " + Fore.RED + f"{count_good_status_code}" + Fore.YELLOW)
                            file = open("count_good_status_code.py", "a")
                            file.write(f"\n# Аккаунт номер {account_number}\n")
                            file.write(f"count_good_status_code += {1}")
                            file.close()
                        else:
                            count_bad_status_code += 1
                            print(Fore.RED + f"{account_number}: Статус код = {status_code} | Кажется, серверу нужно дать перерыв[{count_bad_status_code}]..." + Fore.YELLOW)
                            if count_bad_status_code > 6:
                                break
                        if account_number >= max_account_number:
                            break

        account_number, count = await ending(account_number, max_account_number, count, time_sleep)


async def withdraw(max_account_number):
    general_balance = 0  # переменная общего баланса
    coin = 0  # Счетчик баланса 
    print("Проверяем баланс у " + Fore.RED + f"{max_account_number}" + Fore.YELLOW + " ботов!")

    for account_number in range(0, max_account_number):
        client = await client_authorization(account_number+1)  # авторизация бота
        await client.start()

        dlgs = await client.get_dialogs()
        for dlg in dlgs:
            if dlg.title == BOT_TITLE:
                tegmo = dlg

        await client.send_message(BOT_TITLE, "/balance")
        await asyncio.sleep(3)
        msgs = await client.get_messages(tegmo, limit=1)
        for mes in msgs:
            convert_coin = str(mes.message).replace('Available balance: ', '')
            coin = float(convert_coin.replace("LTC", ''))  # из строки вырезаем только число
            print(coin)
            general_balance += coin

            if coin >= MINIMAL_BALANCE:
                await client.send_message(BOT_TITLE, "💵 Withdraw")
                time.sleep(3)
                await client.send_message(BOT_TITLE, LTC_ADDRESS)
                out_coin = float(float(round(coin, 5)) - 0.00001)
                print(Fore.RED + f"Выводим: {out_coin}" + Fore.YELLOW)

                file = open('withdraw.txt', "a")
                file.write(f"Время: {get_now_time()}. Выводим {out_coin} LTC с аккаунта {Accounts[account_number][1]}\n")
                file.close()

                time.sleep(3)
                await client.send_message(BOT_TITLE, str(out_coin))
                time.sleep(3)
                await client.send_message(BOT_TITLE, "✅ Confirm")
                time.sleep(3)
                await client.send_message(BOT_TITLE, "🏠 Menu")
                time.sleep(3)
        await client.disconnect()
        print(Fore.GREEN + "### Клиент отключился ###" + Fore.YELLOW)
        time.sleep(1)
    file_balance = open("balance.txt", "a")
    file_balance.write(f"{get_now_time()}: {round(general_balance, 8)}")
    file_balance.close()
    print(Fore.GREEN + f"Общий баланс = {round(general_balance, 8)} LTC" + Fore.YELLOW)

# Чисто для красоты, хочу чтобы глазу было приятно :D
def console_picture():
    print(Style.BRIGHT + Fore.GREEN)
    os.system("clear")
    print("""
       _  ________     _              
  ___ | |/ /_  __/____(_)___ ___  ___ 
 / _ \|   / / / / ___/ / __ `__ \/ _ \\\
 
/  __/   | / / / /  / / / / / / /  __/
\___/_/|_|/_/ /_/  /_/_/ /_/ /_/\___/
    ___   _______  ___   ________
   /   | / ___/\ \/ / | / / ____/
  / /| | \__ \  \  /  |/ / /     
 / ___ |___/ /  / / /|  / /___   
/_/  |_/____/  /_/_/ |_/\____/ 
  ______________    ________________  ___    __  ___
 /_  __/ ____/ /   / ____/ ____/ __ \/   |  /  |/  /
  / / / __/ / /   / __/ / / __/ /_/ / /| | / /|_/ / 
 / / / /___/ /___/ /___/ /_/ / _, _/ ___ |/ /  / /  
/_/ /_____/_____/_____/\____/_/ |_/_/  |_/_/  /_/
    ____  ____  ___________
   / __ )/ __ \/_  __/ ___/
  / __  / / / / / /  \__ \ 
 / /_/ / /_/ / / /  ___/ / 
/_____/\____/ /_/  /____/ 
""")
    print(Fore.YELLOW)
    time.sleep(0.5)

# Создаем перерывы для ботов, нужно для того, чтобы ботов не забанили за спам, пусть лучше отходнут и дождутся новых заданий
def drink_coffee():
    this_time_sleep = int(input("Сколько минут можно пить кофе? >> " + Fore.BLUE))
    if this_time_sleep == 0:
        print("Мы можем умереть без кофе!!!")
    else:
        print(f"Перерыв на кофе = {this_time_sleep} минут...")
    print(Fore.YELLOW)
    return this_time_sleep

# Пишем функцию ожидания, например если нужно куда-то идти, то можно установить таймер на запуск ботов
def wait():
    time_wait = int(input("Через сколько минут приступать к работе? >> " + Fore.BLUE))
    if time_wait == 0 or time_wait == None:
        print(Fore.RED + "Приступаем к работе!" + Fore.GREEN)
    else:
        print(f"Ждем {time_wait} минут...")
        time.sleep(time_wait * 60)
        print(Fore.RED + "Приступаем к работе!" + Fore.GREEN)

# Записываем время в секундах, сколько можно делать перерывы ботам 
def config(time_sleep):
    file = open("sleep.py", "w")
    file.write(f"time_sleep = {time_sleep}")
    file.close()


# Удобная оболочка для пользователя
def shell():
    # Выбираем что мы будем делать...
    choose = 0
    try:
        choose = int(input(
            "1) Запустить ботов...\n" + 
            "2) Узнать баланс...\n" +
            "3) Создать новую сессию...\n" + 
            "4) Выход из программы...\n-->> " + Fore.YELLOW))
    except ValueError:
        print(Fore.RED + "Вы ввели неверное значение!" + Fore.YELLOW)
        shell()

    if choose == 1:
        config(drink_coffee())  # записываем в файл то, сколько можно отдыхать ботам...
        wait()  # момент ожидания
        # Запускаем скрипт-оболочку, запускаем его всегда, это нужно для того, чтобы при ошибки он продолжал работать...
        while True:
            print(f"Время старта: {start_time}")
            process = subprocess.Popen([sys.executable, "runbot.py"])
            process.wait()
    elif choose == 2:
        print(Fore.GREEN + "Узнаем баланс:\n" + Fore.YELLOW)

        asyncio.run(withdraw(max_account_number))  # считаем баланс со всех аккаунтов
        input("Чтобы выбрать другую операцию нажмите на любую кнопку..." + Fore.YELLOW)
        os.system("clear")  # очищаем терминал
        shell()  # снова запуск
    elif choose == 3:
        create_session()
        shell()
    elif choose == 4:
        exit  # выходим
    else:
        print("Вы ввели неверное число! Попробуйте еще раз...\n")  # анти-дурак
        os.system("clear")
        shell()

# Засекаем начало старта...
start_time = get_now_time()

# Запускаем скрипт, только если он именно main.py
if __name__ == "__main__":
    console_picture()
    shell()
