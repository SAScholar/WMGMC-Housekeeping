import pywikibot
import requests
import re
from pyrogram import Client, filters, idle
from configuration import *

site = pywikibot.Site("meta")
page = pywikibot.Page(site, "Wikimedian%27s_Group_of_Mainland_China/New")

app = Client("approveSession", api_id=api_id, api_hash=api_hash, bot_token=token)

def matchConfirm(input_string):
    match = re.search(r'/confirm\s+(.*)', input_string)
    if match:
        return match.group(1)
    return None

async def getInviteLink(username):
    api = f'https://api.telegram.org/bot{token}/createChatInviteLink'
    params = {
        'chat_id': disscusionGroup,
        'name': username
    }
    response = requests.get(api, params=params)
    response = response.json()
    inviteLink = response['result']['invite_link']
    return inviteLink

@app.on_message(filters.command("enable"))
async def start(client, message):
    await message.reply("已识别本群组。")

@app.on_message(filters.command("confirm"))
async def confirm(client, message):
    matches = matchConfirm(message.text)
    if message.from_user.id in confirmUser:
        username = matches
        invitelink = await getInviteLink(username)
        user = pywikibot.User(site, username)
        if user.isEmailable():
            user.sendMail("您加入WMGMC的申请已被批准", f"如题，我谨代表中国大陆维基媒体用户组理事会，批准您的入组申请。感谢您的耐心等待和对我们的支持，如果您有Telegram账户，还可以加入我们的Telegram群组，加入链接附在文末，再次感谢您的耐心等待！%0A{invitelink}", ccme=True)
            await message.reply("已批准。")
        else:
            await message.reply("已批准，但是因为用户未开启邮件功能，无法发送通知邮件。")
    else:
        await message.reply("错误")
        print("未知错误。")

app.start()
app.run()
