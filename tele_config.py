import requests
import os
from pprint import pprint as pp

tele_key = os.getenv('TELEGRAM_TOKEN')
tele_user_id = os.getenv('TELEGRAM_MYID')
tele_myid = os.getenv('TELEGRAM_MYID')
tele_url="https://api.hphk.io/telegram"
my_url = "https://naver-shine1225.c9users.io"

#####################################################################################################

def getTelegram(method):
    url="{}/bot{}/{}".format(tele_url,tele_key,method)
    result=requests.get(url).json()
    return result

def sendParams(user_id,message):
    return "sendMessage?chat_id={}&text={}".format(user_id,message)
    
def getData(doc):
    try :
        msg=doc["message"].get("text")
        chat_data=doc["message"]["chat"]
    except KeyError :
        msg=doc["edited_message"].get("text")
        chat_data=doc["edited_message"]["chat"]
    name=chat_data["first_name"]
    if "last_name" in chat_data:
        name+=" "+chat_data["last_name"]
    return name, chat_data["id"], msg
    
def getId():
    update=getTelegram("getUpdates")
    pp(update)
    res=update["result"]
    chat_id=[]
    for doc in res:
        try :
            msg=doc["message"].get("text")
            chat_data=doc["message"]["chat"]
        except KeyError :
            msg=doc["edited_message"].get("text")
            chat_data=doc["edited_message"]["chat"]
        chat_id.append(chat_data["id"])
    return chat_id
#####################################################################################################