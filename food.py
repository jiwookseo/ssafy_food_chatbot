import requests
from bs4 import BeautifulSoup as bs
from collections import OrderedDict
import numpy as np
import datetime
from tele_config import *
import json
SSAFY_ID=os.getenv("SSAFY_ID")
SSAFY_PWD=os.getenv("SSAFY_PWD")
LOGIN_DATA={'userId': SSAFY_ID,'userPwd': SSAFY_PWD}
LOGIN_URL = 'https://edu.ssafy.com/comm/login/SecurityLoginCheck.do'
s = requests.Session()
res = s.post(LOGIN_URL, data=LOGIN_DATA, verify=False, allow_redirects=False)
# print(res.raise_for_status())

url = 'https://edu.ssafy.com/edu/board/notice/detail.do?brdItmSeq=331'
res2 = s.get(url).text
doc = bs(res2, 'html.parser')
result_food=doc.find_all("table")
foodlist=result_food[1]
trs = foodlist.find_all('tr')

days=trs[0].text
days=days.split("\n")
days=days[2:-1]
days_array=np.array(days)
for i in range(5):
    days_array[i]=days_array[i][1:]

menu=[]
for i in range(2,20):
    menu.append(trs[i].text.split("\n")[1:-1])
menu[0]=menu[0][3:]
menu[8]=menu[8][1:]
menu_array=np.array([])
for i in range(16):
    menu_array=np.append(menu_array,np.array(menu[i]))
menu_array=menu_array.reshape((16,5)).T
menu_array=menu_array.reshape((5,2,8))
menu_dict={}
for i in range(5):
    menu_dict[i]=menu_array[i].reshape((2,8))


def foodMsg(chat_name, chat_id, day):
    dt = datetime.datetime.now()
    wd=dt.weekday()
    check=True
    if day=="내일":
        wd+=1
        if wd>=5:
            getTelegram(sendParams(chat_id,"월-금요일 식단만 확인 가능합니다."))
            check=False
    elif day=="어제":
        wd-=1
        if wd<0:
            getTelegram(sendParams(chat_id,"월-금요일 식단만 확인 가능합니다."))
            check=False
    elif day=="모레":
        wd+=2
        if wd>=5:
            getTelegram(sendParams(chat_id,"월-금요일 식단만 확인 가능합니다."))
            check=False
    if check:
        message=""
        message+="{}님 안녕하세요 \n\n".format(chat_name)
        message+="{}의 A형 식단은\n".format(days_array[wd])
        for i in range(7):
            message+=menu_dict[wd][0][i][1:]+"\n"
        message+="총 칼로리는 {}입니다.\n\n".format(menu_dict[wd][0][-1][1:])
        message+="{}의 B형 식단은\n".format(days_array[wd])
        for i in range(7):
            message+=menu_dict[wd][1][i][1:]+"\n"
        message+="총 칼로리는 {}입니다.\n\n".format(menu_dict[wd][1][-1][1:])
        message+="인싸봇 올림. 좋은 하루 되세요 :)"
        getTelegram(sendParams(chat_id,message))