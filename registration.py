from main import *

def create_session():
	try:
		_account_number = int(input(Fore.YELLOW + "Введите номер аккаунта: "))
		session = str(SESSION_NAME + str(_account_number))
		client = TelegramClient(session, API_ID, API_HASH)
		client.start()
		client.get_entity("https://t.me/Litecoin_click_bot?start=kXh2R")
		client.send_message("BOT_TITLE", "/start")
		print(Fore.GREEN + f"Сессия '{SESSION_NAME}{number}' создана!")
	except:
		raise
		print(Fore.RED + "Ошибка при создании сессии...")
	finally:
		print(Fore.YELLOW)
