from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import requests
from colorama import init, Fore, Style
import os

init()  # colorama

# путь до драйвера
pathWebDriver = "/home/extrime/mnt/NTFS_FILE_SYSTEM/Programming/Bots_Telegram/SOAD/packages/Chrome88"
options = webdriver.ChromeOptions()  # настройки для браузера
options.add_argument('headless')  # для открытия headless-браузера(без окна)
# Чтобы запустить графический режим уберите: chrome_options=options
browser = webdriver.Chrome(executable_path = pathWebDriver, chrome_options=options)
os.system("clear")

# Общая переменная xpath
xpath = "/html/body/table[2]/tbody/tr[3]/td/table/tbody/tr["
# Массив со всеми IP, PORT
list_proxy = []


# открываем сайт
def openUrl():
	print(Fore.YELLOW + "** Открываем сайт **")
	browser.implicitly_wait(10)
	browser.get("https://spys.one/proxies/")  # переходим на сайт
	# проверяем наличие того, что мы попали на страницу
	assert "Бесплатные HTTP, HTTPS, SOCKS прокси сервера, списки обновляемых IP адресов проксей онлайн" in browser.title
	browser.implicitly_wait(10)


def setFilters(number):
	print("** Настраиваем фильтры **")
	type_http = Select(browser.find_element_by_xpath(f"{xpath}1]/td[2]/font/select[6]"))
	type_http.select_by_value("1")  # 0=Все 1=HTTP 2=SOCKS- протокол связи HTTP

	ANM = Select(browser.find_element_by_xpath(f"{xpath}1]/td[2]/font/select[3]"))
	ANM.select_by_value(str(number))  # 3=ANM - анонимный, 4=HIA - высокоанонимный тип прокси

	amount_proxy = Select(browser.find_element_by_xpath(f"{xpath}1]/td[2]/font/select[1]"))
	amount_proxy.select_by_value("3")  # 0=25 1=50 2=100 3=200 4=300 5=500 


def parseProxy():
	print(Fore.RED + "*** Парсим прокси ***\n" + Fore.YELLOW)
	for i in range(4, 204):  # 4, 204
		browser.implicitly_wait(10)
		address = str(browser.find_element_by_xpath(f"{xpath}{i}]/td[1]/font").text)
		print(f"IP[{i-3}] >> {address} ")
		list_proxy.append(address)


def checkProxy(timeout):
	print(Fore.RED + "\n*** Проверяем прокси ***\n" + Fore.YELLOW)
	for i in range(0, 200):  # 200 потому, что amount_proxy.select_by_value("3")
		proxy = list_proxy[i]
		request = requests.get("https://www.google.com/", proxies={"http": proxy}, timeout=timeout)
		print(f"[{i+1}/200]Проверка (" + Fore.RED + f"{proxy}" + Fore.YELLOW + ") | Статус код -->> " + Fore.GREEN + f"{request.status_code}" + Fore.YELLOW)
		writeProxy(proxy, request.status_code)


def writeProxy(proxy, status_code):
	if int(status_code) == 200:
		f = open("MyProxy.py", "a")
		f.write(f"'{proxy}', \n")
		f.close()
		print("Прокси " + Fore.GREEN + f"{proxy}" + Fore.YELLOW + " был записан в файл " + Fore.GREEN + "MyProxy.py" + Fore.YELLOW + " со статус кодом = " + Fore.GREEN + f"{status_code}" + Fore.YELLOW)

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
    time.sleep(0.5)
    f = open("MyProxy.py", "w")
    f.write('list_proxy = [')
    f.close()


console_picture()
openUrl()
for i in range(3, 5):
	setFilters(i)  ## TODO: 3 и 4 т.к. число 5 считается как выколотая точка! Учи Python блин!
	parseProxy()
	checkProxy(10)
	list_proxy = []

f = open("MyProxy.py", "a")
f.write("]")
f.close()

input("The end. Press key...")  # нужно для окна(NO headless), чтобы оно не закрывалось
assert "No results found." not in browser.page_source  # мы не попали на страницу :(
browser.close()  # закрываем драйвер