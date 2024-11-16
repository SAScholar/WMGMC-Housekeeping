import pywikibot
import time
import json
from pyrogram import Client
import schedule
from configuration import *

site = pywikibot.Site("meta")
page = pywikibot.Page(site, "Wikimedian%27s_Group_of_Mainland_China/New")

app = Client(
    "pendingSession",
    api_id=api_id, api_hash=api_hash,
    bot_token=token
)

def getUpdates():
    with open("requests.json", "r") as dump:
        requestsData = json.load(dump)
    oldid = page.latest_revision_id
    if oldid != requestsData["revid"]:
        requester = page.latest_revision.user
        requestID = page.latest_revision_id
        requestContent = page.getOldVersion(requestID)
        if requester in requestContent:
            requestsData["revid"] = requestID
            json.dump(requestsData, open("requests.json", "w"))
            return requester
        else:
            return False
    else:
        return False
    
async def stopPoll(pollid):
    await app.stop_poll(chat_id=reviewGroup, message_id=pollid)
    return schedule.CancelJob

async def requestCheck(username):
    information = await app.send_poll(chat_id=reviewGroup, question=f"是否批准{username}的加入请求？", options=["批准", "拒绝"], is_anonymous=False)
    with open("requests.json", "r") as dump:
        requestsData = json.load(dump)
    requestsData["pending"].append({"user": username, "timestamp": time.timestamp, "pollid": information.id})
    schedule.every(3).days.do(stopPoll, pollid=information.id)

async def main():
    while True:
        update = getUpdates()
        if update:
            await requestCheck(update)
        else:
            schedule.run_pending()
            time.sleep(1)

if __name__ == "__main__":
    app.start()
    app.run(main())
    