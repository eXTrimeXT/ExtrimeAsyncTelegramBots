from main import *

options = webdriver.ChromeOptions()  # настройки для браузера
options.add_argument('headless')  # для открытия headless-браузера(без окна)
browser = webdriver.Chrome(executable_path="./Chrome88", options=options)  # фоновый режим
print(int(3.2))
browser.get("https://www.google.com/search?q=ltc&oq=ltc&aqs=chrome.0.35i39l2j0l3j0i1i10j0l4.519j0j1&sourceid=chrome&ie=UTF-8")
course = str(browser.find_element_by_xpath("/html/body/div[7]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div/div/div[1]/div/div[1]/div[1]/div[2]/span[1]").text)
course = course.replace(" ", "")
print(f"Курс LTC/RUB = {course}")