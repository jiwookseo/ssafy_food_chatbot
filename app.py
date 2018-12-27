from flask import Flask, render_template, request
import csv, json
import requests
import os
from tele_config import *
from food import *
from pprint import pprint as pp

app=Flask(__name__)
@app.route('/')
def index():
    return render_template("index.html")

#webhook
#setwebhook > 웹훅 설정 > 텔레그래에게 알림 설정
# 텔레그램이 우리에게 알림을 줄 대 사용할 루트
# 만약 특정 유저가 우리 봇으로 메세지를 보내게 되면
# 텔레그램이 우리에게 json으로 알림을 보내온다.

@app.route('/setwebhook')
def setwebhook():
    return getTelegram('setWebhook?url={}/{}'.format(my_url,tele_key)), 200
    
@app.route("/{}".format(tele_key), methods=['POST'])
def telegram():
    doc = request.get_json()
    chatName, chatId, chatMsg = getData(doc)
    if chatMsg[-2:] == "식단":
        foodMsg(chatName, chatId, chatMsg[0:2])
    else:
        msg="잘못된 명령어입니다.\n"
        msg+="사용 가능한 명령어 : 식단 (어제, 오늘, 내일, 모레 식단 입력가능)"
        getTelegram(sendParams(chatId,"{} 님 죄송합니다.\n {}".format(chatName,msg)))
    return '', 200
    
@app.route('/deletewebhook')
def delete_webhook():
    return getTelegram('deleteWebhook?url={}/{}'.format(my_url,tele_key)), 200