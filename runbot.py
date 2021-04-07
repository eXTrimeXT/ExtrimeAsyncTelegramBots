from colorama import init, Fore, Style
from main import *
from conf import *
from sleep import *
import asyncio


async def main():
    # Запланируйте три звонка * одновременно *:
    await asyncio.gather(
    	run(account_number, max_account_number, max_cycle, time_sleep),)
    	# run(account_number+1, max_account_number, max_cycle, time_sleep),)


if __name__ == "__main__":
	print(f"Начинающий бот: {account_number}")
	print(f"Всего ботов: {max_account_number}")
	print(f"Очереди будут состоять из {BOT_QUEUE} ботов")
	print(f"Каждый будет делать {max_cycle} цикла(ов)" + Fore.YELLOW)
	# run(account_number, max_account_number, max_cycle, time_sleep)
	asyncio.run(main()) 
