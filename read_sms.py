from main import *


def read_message(_account_number, chat_name, _limit):
	with TelegramClient(SESSION_NAME + f'{_account_number}', API_ID, API_HASH) as client:
		msgs = client.get_messages(str(chat_name), limit = _limit)  # default limit = 1
		print(msgs)
