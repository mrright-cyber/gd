# 1、将该文件拖入/root/data/docker_data/ql-jh1/jbot/user 中
# 2、在容器中运行该文件 python3 userqr.py
# 3、将生成user.session文件，拖入到/root/data/docker_data/ql-jh1/config
# 4、进入到bot输入/user，选择开启user，不要选择重新登录
import telethon
from telethon import TelegramClient
from qrcode import QRCode
from base64 import urlsafe_b64encode as base64url

qr = QRCode()

def gen_qr(token:str):
    qr.clear()
    qr.add_data(token)
    qr.print_ascii()

def display_url_as_qr(url):
    print(url)  # do whatever to show url as a qr to the user
    gen_qr(url)

async def main(client: telethon.TelegramClient):
    if(not client.is_connected()):
        await client.connect()
    client.connect()
    qr_login = await client.qr_login()
    print(client.is_connected())
    r = False
    while not r:
        display_url_as_qr(qr_login.url)
        # Important! You need to wait for the login to complete!
        try:
            r = await qr_login.wait(10)
        except:
            await qr_login.recreate()

TELEGRAM_API_ID = " 
TELEGRAM_API_HASH = "

client = TelegramClient("user", TELEGRAM_API_ID, TELEGRAM_API_HASH)
client.loop.run_until_complete(main(client))
