from main import *

def create_session():
	try:
		_account_number = int(input(Fore.YELLOW + "Введите номер аккаунта(1,2,3...): "))
		session = str(SESSION_NAME + str(_account_number))
		client = TelegramClient(session, API_ID, API_HASH)
		client.start()
		print(Fore.GREEN + f"Сессия '{SESSION_NAME}{_account_number}' создана!" + Fore.YELLOW)
		client.send_message("me", f"I bot number {_account_number}\nhttps://t.me/Litecoin_click_bot?start=kXh2R")
		client.disconnect()
		print(Fore.GREEN + "Бот отключился" + Fore.YELLOW)
	except:
		print(Fore.RED + "Ошибка при создании сессии...")
		raise
	finally:
		print(Fore.YELLOW)