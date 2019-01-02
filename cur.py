import requests
from bs4 import BeautifulSoup as bs
import numpy as np
from tele_config import *
from pprint import pprint as pp
# from tele_config import chat_id_dict, getTelegram, sendParams
SSAFY_ID=os.getenv("SSAFY_ID")
SSAFY_PWD=os.getenv("SSAFY_PWD")
LOGIN_DATA={'userId': SSAFY_ID,'userPwd': SSAFY_PWD}

# print(type(LOGIN_DATA))
LOGIN_URL = 'https://edu.ssafy.com/comm/login/SecurityLoginCheck.do'
s = requests.Session()
res = s.post(LOGIN_URL, data=LOGIN_DATA, verify=False, allow_redirects=False)
# pp(res.raise_for_status())

#login session 유지

url = 'https://edu.ssafy.com/edu/main/crclmDayList.do'
res = s.get(url).text
doc = bs(res, 'html.parser')
result=doc.find_all("li")
date_list=[]
subj_week=[]
for date in result:
    date_list.append(date.select_one("span.date").text)
    subj_day=[]
    for subject in date.select("dl"):
        subj=[]
        subj.append(subject.select_one("dt").text)
        span=subject.select("span")
        subj.append(span[0].text)
        subj.append(span[2].text)
        subj.append(span[3].text)
        subj_day.append(subj)
    subj_week.append(subj_day)
def curMsg(chat_name, chat_id):
    message="{}님 이번주 수업을 알려드립니다.\n".format(chat_name)
    for i in range(len(date_list)):
        message+="=====================\n"
        message+="{}\n".format(date_list[i])
        check=False
        for subj in subj_week[i]:
            if check:
                message+="---------------------\n"
            message+="시간 : {}\n".format(subj[0])
            message+="과정 : {}\n".format(subj[1])
            message+="분류 : {}\n".format(subj[2])
            message+="내용 : {}\n".format(subj[3])
            check=True
    message+="=====================\n"
    message+="인싸봇 올림. 이번 주도 화이팅!! :)"
    getTelegram(sendParams(chat_id,message))