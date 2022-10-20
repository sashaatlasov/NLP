# via https://betterprogramming.pub/how-to-get-data-from-telegram-82af55268a4b

import configparser
from telethon import TelegramClient
import pandas as pd
from tqdm.auto import tqdm
import re

config = configparser.ConfigParser()
config.read("/Users/sasaatlasov/Documents/Jupyter/Текстовые данные/ДЗ №1/config.ini")
api_id = int(config['Telegram']['api_id'])
api_hash = str(config['Telegram']['api_hash'])
phone = config['Telegram']['phone']
username = config['Telegram']['username']

client = TelegramClient(username, api_id, api_hash)
client.start()
print("Client Created")


def ck_url(x):
    re_equ = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    ck_url_tf = re.findall(re_equ, x)
    if ck_url_tf:
        return True
    else:
        return False


df = pd.DataFrame({'message': [], 'category': []})


def get_samples(url, category, limit=None):
    for i, j in tqdm(enumerate(client.iter_messages(url, limit=limit))):
        if j.message is not None and not ck_url(j.message):
            msg = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", re.sub(r'\n', '', j.message)).split())
            global df
            df = pd.concat([df, pd.DataFrame({'message': [msg], 'category': [category]})], ignore_index=True, axis=0)


get_samples('https://t.me/CryptoVIPsignalTA', 1, 10000)
get_samples('https://t.me/bitcoin_industry', 1, 3500)
get_samples('https://t.me/auroritychat', 0, 10000)
get_samples('https://t.me/EnglishChatRoomForLearn', 0, 6000)
get_samples('https://t.me/beautitips', 2, 10000)
get_samples('https://t.me/randomchatsenglish', 0, 10000)
get_samples('https://t.me/pythongroup', 0, 10000)

df.to_csv('/Users/sasaatlasov/Desktop/tg.csv')
