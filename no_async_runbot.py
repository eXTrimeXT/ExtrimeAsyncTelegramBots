from colorama import init, Fore, Style
from no_async_main import *
from conf import *
from sleep import *


if __name__ == "__main__":
	print(f"Начинающий бот: {account_number}")
	print(f"Всего ботов: {max_account_number}")
	print(f"Каждый будет делать {max_cycle} цикла(ов)" + Fore.YELLOW)
	run(account_number, max_account_number, max_cycle, time_sleep)
	# asyncio.run(main()) 
