from telethon import TelegramClient
from colorama import init, Fore
from conf import api_id, api_hash

init()

def create_session():
	try:
		number = int(input(Fore.YELLOW + "Введите номер аккаунта: "))
		with TelegramClient(f'.anon{number}', api_id, api_hash) as client:
		    client.loop.run_until_complete(client.send_message('me', 'Hello'))
		print(Fore.GREEN + f"Сессия '.anon{number}' создана!")
	except:
		print(Fore.RED + "Ошибка при создании сессии...")
	finally:
		print(Fore.YELLOW)
