from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from time import sleep
import requests
from colorama import init, Fore, Style
import os

init()  # colorama

# путь до драйвера
pathWebDriver = "/home/extrime/mnt/NTFS_FILE_SYSTEM/Programming/Bots_Telegram/EATB/Chrome88"
options = webdriver.ChromeOptions()  # настройки для браузера
options.add_argument('headless')  # для открытия headless-браузера(без окна)
# Чтобы запустить графический режим уберите: options=options
browser = webdriver.Chrome(executable_path = pathWebDriver, options=options)
os.system("clear")

# Общая переменная xpath
xpath = "/html/body/table[2]/tbody/tr[3]/td/table/tbody/tr["
# Массив со всеми IP, PORT
list_proxy = []


# открываем сайт
def openUrl():
	print(Fore.YELLOW + "** Открываем сайт **")
	browser.get("https://spys.one/proxies/")  # переходим на сайт


def setFilters(number):
	print("** Настраиваем фильтры **")
	type_http = Select(browser.find_element_by_xpath(f"{xpath}1]/td[2]/font/select[6]"))
	type_http.select_by_value("1")  # 0=Все 1=HTTP 2=SOCKS- протокол связи HTTP
	ANM = Select(browser.find_element_by_xpath(f"{xpath}1]/td[2]/font/select[3]"))
	ANM.select_by_value(str(number))  # 3=ANM - анонимный, 4=HIA - высокоанонимный тип прокси
	amount_proxy = Select(browser.find_element_by_xpath(f"{xpath}1]/td[2]/font/select[1]"))
	amount_proxy.select_by_value("5")  # 0=25 1=50 2=100 3=200 4=300 5=500 


def parseProxy():
	print(Fore.RED + "*** Парсим прокси ***\n" + Fore.YELLOW)
	for i in range(4, 504):  # 4, 504
		browser.implicitly_wait(10)
		address = browser.find_element_by_xpath(f"{xpath}{i}]/td[1]/font").text
		print(f"IP[{i-3}] >> {address} ")
		list_proxy.append(address)


def checkProxy(start, end):
	print(Fore.RED + "Отсеиваем прокси..." + Fore.YELLOW)
	browser.get("https://hidemy.name/ru/proxy-checker/")
	browser.implicitly_wait(20)
	# Снимаем галочку с Socks4, Socks5, неработающие
	browser.find_element_by_css_selector("body > div.wrap > div.services_checker.services > div > form > div.row_1 > div.col_2 > div > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > label > span.icon").click()
	browser.find_element_by_css_selector("body > div.wrap > div.services_checker.services > div > form > div.row_1 > div.col_2 > div > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > label > span.icon").click()
	# browser.find_element_by_css_selector("body > div.wrap > div.services_checker.services > div > form > div.row_1 > div.col_2 > div > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > label > span.icon").click()
	input_proxy = browser.find_element_by_css_selector("#f_in")
	sleep(2)
	for i in range(start, end):
		input_proxy.send_keys(f"{list_proxy[i]}\n")
		sleep(0.1)

	browser.find_element_by_css_selector("#chkb1").click()
	print("Проверка началась...")
	while True:
		percent = int(browser.find_element_by_css_selector("#s_persent").text)
		if percent != int(browser.find_element_by_css_selector("#s_persent").text):
			print(Fore.YELLOW + f"Выполнено {percent} процентов")
		if percent == 100:
			print(Fore.GREEN + f"Выполнено 100 процентов\n[от {start} до {end}]" + Fore.YELLOW)
			break

	for i in range(1, 101):
		speed = browser.find_element_by_xpath(f"/html/body/div[1]/div[4]/div/div[4]/table/tbody/tr[{i}]/td[4]/div/p").text
		speed = int(speed.replace(" мс", ""))
		no_good_check = browser.find_element_by_xpath(f"/html/body/div[1]/div[4]/div/div[4]/table/tbody/tr[{i}]/td[5]/span").text
		# print(f"Speed = {speed}")
		if speed < 500 and no_good_check != "Не прошёл проверку":
			ip = browser.find_element_by_xpath(f"/html/body/div[1]/div[4]/div/div[4]/table/tbody/tr[{i}]/td[1]").text
			port = browser.find_element_by_xpath(f"/html/body/div[1]/div[4]/div/div[4]/table/tbody/tr[{i}]/td[2]").text
			writeProxy(ip, port, speed)


def writeProxy(ip, port, speed):
	f = open("MyProxy.py", "a")
	f.write(f"['{ip}', {port}], \n")
	f.close()
	f = open("myProxy.txt", "a")
	f.write(f"{ip}:{port}\n")
	f.close()
	print("Прокси " + Fore.GREEN + f"{ip}:{port}" + Fore.YELLOW + " был записан в файлы " + Fore.GREEN + "MyProxy.[py/txt]" + Fore.YELLOW + " со скоростью = " + Fore.GREEN + f"{speed} мс" + Fore.YELLOW)

# Чисто для красоты, хочу чтобы глазу было приятно :D
def console_picture():
    print(Style.BRIGHT + Fore.GREEN)
    print(
        """
    ____  ____  ____ _  ____  __
   / __ \/ __ \/ __ \ |/ /\ \/ /
  / /_/ / /_/ / / / /   /  \  / 
 / ____/ _, _/ /_/ /   |   / /  
/_/   /_/ |_|\____/_/|_|  /_/ 
       _  ________     _              
  ___ | |/ /_  __/____(_)___ ___  ___ 
 / _ \|   / / / / ___/ / __ `__ \/ _ \\\
 
/  __/   | / / / /  / / / / / / /  __/
\___/_/|_|/_/ /_/  /_/_/ /_/ /_/\___/ 
""")
    print(Fore.YELLOW)
    sleep(0.5)
    f = open("MyProxy.py", "w")
    f.write('list_proxy = [\n')
    f.close()
    f = open("myProxy.txt", "w")
    f.write("")
    f.close()


console_picture()
for i in (3, 4):
	openUrl()
	setFilters(i)  ## TODO: 3 и 4 т.к. число 5 считается как выколотая точка! Учи Python блин!
	parseProxy()

	for j in (0, 100, 200, 300, 400):
		checkProxy(j, j+100)



f = open("MyProxy.py", "a")
f.write("]")
f.close()

input("The end. Press key...")  # нужно для окна(NO headless), чтобы оно не закрывалось
browser.close()  # закрываем драйвер