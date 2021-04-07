from telethon.sync import TelegramClient
from conf import *


def read_message(_account_number, chat_name, _limit):
	with TelegramClient(f'.anon{_account_number}', api_id, api_hash) as client:
		msgs = client.get_messages(str(chat_name), limit = _limit)  # default limit = 1
		print(msgs)
